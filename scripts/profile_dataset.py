#!/usr/bin/env python3
"""
Profiling estrutural do dataset GitSkills (EXP-001).

Gera todas as estatisticas citadas em notes/Datasets/ e notes/Experiments/EXP-001.
Nao carrega dados em memoria: todas as metricas sao agregacoes DuckDB sobre os
Parquet shards. Saida determinista em results/EXP-001_profile.json.

Uso:
    uv run --with duckdb python scripts/profile_dataset.py
    python scripts/profile_dataset.py --data-dir data/raw/gitskills/data
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_DIR = ROOT / "data" / "raw" / "gitskills" / "data"
RESULTS_DIR = ROOT / "results"

# Keywords exatamente como definidas no notebook 01_exploratory (celula 29),
# para permitir comparacao direta com o resultado invalido registrado la.
SECURITY_KEYWORDS = [
    "security", "vulnerability", "exploit", "authentication", "encryption",
    "injection", "xss", "csrf", "sanitize", "supply chain", "secret",
    "credential", "api key", "password", "prompt injection", "jailbreak",
    "guardrail", "owasp", "cve", "pentest", "sandbox", "permission",
    "audit", "token",
]


def sql_literal(pattern: str) -> str:
    return pattern.replace("'", "''")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default=str(DEFAULT_DATA_DIR))
    args = ap.parse_args()

    data_dir = Path(args.data_dir)
    tables = {
        "artifacts": data_dir / "artifacts" / "*.parquet",
        "artifact_siblings": data_dir / "artifact_siblings" / "*.parquet",
        "repos": data_dir / "repos" / "*.parquet",
    }
    for name, glob in tables.items():
        if not list(glob.parent.glob("*.parquet")):
            print(f"ERRO: nenhum Parquet em {glob.parent}", file=sys.stderr)
            print("Baixe o dataset antes de rodar o profiling.", file=sys.stderr)
            return 1

    A = f"read_parquet('{tables['artifacts'].as_posix()}')"
    S = f"read_parquet('{tables['artifact_siblings'].as_posix()}')"
    R = f"read_parquet('{tables['repos'].as_posix()}')"

    con = duckdb.connect()
    con.execute("SET enable_progress_bar=false")
    out: dict = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "duckdb_version": duckdb.__version__,
        "data_dir": str(data_dir),
    }

    # --- 1. Volumetria e chaves -------------------------------------------
    out["volumetria"] = dict(zip(
        ["n_rows", "n_repos", "n_distinct_sha", "n_primary", "n_content_fetched",
         "n_content_notnull", "n_frontmatter_valid", "n_history_fetched"],
        con.execute(f"""
            SELECT count(*), count(DISTINCT repo_full_name), count(DISTINCT file_sha),
                   sum(dedup_primary), sum(content_fetched), count(content),
                   sum(frontmatter_valid), sum(history_fetched)
            FROM {A}
        """).fetchone(),
    ))

    # --- 2. Integridade referencial artifacts -> repos ---------------------
    out["integridade_join"] = dict(zip(
        ["repos_in_artifacts", "rows_repos", "distinct_repos", "orphan_repos",
         "repos_metadata_missing"],
        con.execute(f"""
            SELECT
              (SELECT count(DISTINCT repo_full_name) FROM {A}),
              (SELECT count(*) FROM {R}),
              (SELECT count(DISTINCT full_name) FROM {R}),
              (SELECT count(*) FROM (SELECT DISTINCT repo_full_name FROM {A}) a
                 LEFT JOIN {R} r ON a.repo_full_name = r.full_name
                 WHERE r.full_name IS NULL),
              (SELECT sum(CASE WHEN metadata_fetched = 0 THEN 1 ELSE 0 END) FROM {R})
        """).fetchone(),
    ))

    # --- 3. Consistencia dedup_primary x content --------------------------
    out["dedup_x_content"] = [
        dict(zip(["dedup_primary", "content_fetched", "n_rows", "n_with_content"], r))
        for r in con.execute(f"""
            SELECT dedup_primary, content_fetched, count(*), count(content)
            FROM {A} GROUP BY 1, 2 ORDER BY 3 DESC
        """).fetchall()
    ]

    # --- 4. Distribuicao de tamanho de content (representantes) -----------
    out["content_length"] = dict(zip(
        ["n", "min", "p05", "p25", "p50", "p75", "p95", "max", "mean",
         "n_lt_80_chars", "n_symlink_like"],
        con.execute(f"""
            SELECT count(*), min(length(content)),
                   quantile_cont(length(content), 0.05), quantile_cont(length(content), 0.25),
                   median(length(content)), quantile_cont(length(content), 0.75),
                   quantile_cont(length(content), 0.95), max(length(content)),
                   avg(length(content)),
                   sum(CASE WHEN length(content) < 80 THEN 1 ELSE 0 END),
                   sum(CASE WHEN content LIKE '%SKILL.md' AND length(content) < 200
                            THEN 1 ELSE 0 END)
            FROM {A} WHERE content IS NOT NULL
        """).fetchone(),
    ))

    # --- 5. Prova do vies de amostragem do notebook 01 --------------------
    # head(5000) do Parquet != amostra aleatoria. Ver notes/Decisions/D-002.
    out["vies_head5000"] = {
        "primeiras_5000_linhas": dict(zip(
            ["n", "n_with_content", "avg_content_len", "median_content_len",
             "n_with_frontmatter_name", "n_repos", "n_distinct_discovered_at"],
            con.execute(f"""
                WITH f AS (SELECT * FROM {A} LIMIT 5000)
                SELECT count(*), count(content), avg(length(content)),
                       median(length(content)), count(name),
                       count(DISTINCT repo_full_name), count(DISTINCT discovered_at)
                FROM f
            """).fetchone(),
        )),
        "amostra_aleatoria_primaries": dict(zip(
            ["n", "n_with_content", "avg_content_len", "median_content_len",
             "n_with_frontmatter_name", "n_repos"],
            con.execute(f"""
                WITH s AS (
                  SELECT * FROM {A} WHERE dedup_primary = 1
                  ORDER BY hash(file_sha) LIMIT 5000
                )
                SELECT count(*), count(content), avg(length(content)),
                       median(length(content)), count(name),
                       count(DISTINCT repo_full_name)
                FROM s
            """).fetchone(),
        )),
    }

    # --- 6. Prevalencia de keywords sobre TODOS os representantes ---------
    parts = ", ".join(
        f"sum(CASE WHEN lc LIKE '%{sql_literal(k)}%' THEN 1 ELSE 0 END) AS k{i}"
        for i, k in enumerate(SECURITY_KEYWORDS)
    )
    any_expr = " OR ".join(f"lc LIKE '%{sql_literal(k)}%'" for k in SECURITY_KEYWORDS)
    row = con.execute(f"""
        WITH p AS (
          SELECT lower(content) AS lc FROM {A}
          WHERE dedup_primary = 1 AND content IS NOT NULL
        )
        SELECT {parts},
               sum(CASE WHEN {any_expr} THEN 1 ELSE 0 END) AS any_kw,
               count(*) AS total
        FROM p
    """).fetchone()
    total = row[-1]
    out["keyword_prevalence_primaries"] = {
        "denominator_n_primaries": total,
        "any_keyword": {"n": row[-2], "pct": round(100 * row[-2] / total, 2)},
        "por_keyword": sorted(
            [{"keyword": k, "n": n, "pct": round(100 * n / total, 2)}
             for k, n in zip(SECURITY_KEYWORDS, row[:len(SECURITY_KEYWORDS)])],
            key=lambda d: -d["n"],
        ),
    }

    # --- 7. Proposito declarado (frontmatter) vs mencao no corpo ----------
    out["proposito_vs_mencao"] = dict(zip(
        ["n_with_frontmatter", "n_security_in_frontmatter"],
        con.execute(f"""
            SELECT count(*),
                   sum(CASE WHEN lower(name || ' ' || description) LIKE '%security%'
                             OR lower(name || ' ' || description) LIKE '%vulnerab%'
                            THEN 1 ELSE 0 END)
            FROM {A}
            WHERE dedup_primary = 1 AND frontmatter_valid = 1
              AND name IS NOT NULL AND description IS NOT NULL
        """).fetchone(),
    ))

    # --- 8. Composicao: scripts e referencias (superficie de execucao) ----
    out["composicao"] = dict(zip(
        ["n_primary", "n_has_scripts", "n_has_references", "median_sibling_count",
         "max_sibling_count", "n_composition_truncated"],
        con.execute(f"""
            SELECT count(*), sum(has_scripts), sum(has_references),
                   median(sibling_count), max(sibling_count), sum(composition_truncated)
            FROM {A} WHERE dedup_primary = 1
        """).fetchone(),
    ))

    # --- 9. Duplicacao / reuso --------------------------------------------
    out["duplicacao"] = dict(zip(
        ["n_sha_com_copias", "n_linhas_em_sha_duplicado"],
        con.execute(f"""
            SELECT count(*), sum(c) FROM (
              SELECT file_sha, count(*) AS c FROM {A} GROUP BY 1 HAVING count(*) > 1
            )
        """).fetchone(),
    ))

    # --- 10. location_class e filename ------------------------------------
    out["location_class"] = [
        dict(zip(["location_class", "n"], r))
        for r in con.execute(
            f"SELECT location_class, count(*) FROM {A} GROUP BY 1 ORDER BY 2 DESC"
        ).fetchall()
    ]
    out["filename_variants"] = [
        dict(zip(["filename", "n"], r))
        for r in con.execute(
            f"SELECT filename, count(*) FROM {A} GROUP BY 1 ORDER BY 2 DESC"
        ).fetchall()
    ]

    # --- 11. Siblings ------------------------------------------------------
    out["siblings"] = [
        dict(zip(["entry_type", "n", "n_with_content"], r))
        for r in con.execute(
            f"SELECT entry_type, count(*), count(content) FROM {S} GROUP BY 1 ORDER BY 2 DESC"
        ).fetchall()
    ]

    # --- 12. Repos: concentracao de popularidade --------------------------
    out["repos_stars"] = dict(zip(
        ["n", "n_null_stars", "mean", "p50", "p75", "p90", "p99", "max", "pct_zero_stars"],
        con.execute(f"""
            SELECT count(*), sum(CASE WHEN stars IS NULL THEN 1 ELSE 0 END),
                   avg(stars), median(stars), quantile_cont(stars, 0.75),
                   quantile_cont(stars, 0.90), quantile_cont(stars, 0.99), max(stars),
                   100.0 * sum(CASE WHEN stars = 0 THEN 1 ELSE 0 END) / count(stars)
            FROM {R}
        """).fetchone(),
    ))

    RESULTS_DIR.mkdir(exist_ok=True)
    out_path = RESULTS_DIR / "EXP-001_profile.json"
    out_path.write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    print(f"OK -> {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
