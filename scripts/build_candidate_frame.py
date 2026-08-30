#!/usr/bin/env python3
"""
EXP-002 - Frame amostral de candidatas a Security Skill (candidate retrieval).

Keyword matching aqui NAO classifica nada: serve apenas para reduzir 1.877.981
representantes a um pool revisavel, com recall alto e precisao assumidamente baixa.
A classificacao e feita por leitura, conforme notes/Decisions/Codebook.md.

Produz:
  results/EXP-002_frame.json          - tamanhos do pool e dos estratos
  results/EXP-002_sample.parquet      - amostra estratificada deterministica
  results/EXP-002_sample_preview.md   - texto truncado para open coding manual

Uso:
    uv run --with duckdb python scripts/build_candidate_frame.py
    uv run --with duckdb python scripts/build_candidate_frame.py --per-stratum 15
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

# --- Candidate retrieval -----------------------------------------------------
# Recall-orientado. Termos deliberadamente amplos; o ruido e removido na leitura,
# nao aqui. Ver notes/Methodology/QI-2 Methodology.md secao "Candidate retrieval".
RETRIEVAL_TERMS = [
    "security", "secure", "vulnerab", "exploit", "attack", "threat",
    "authentication", "authorization", "authn", "authz", "access control",
    "encrypt", "decrypt", "cryptograph", "hashing",
    "injection", "xss", "csrf", "ssrf", "rce", "sanitiz", "escaping",
    "secret", "credential", "api key", "password", "token leak",
    "owasp", "cve", "cwe", "nist", "mitre",
    "pentest", "penetration test", "red team", "bug bounty", "ctf",
    "sast", "dast", "sca", "fuzzing", "malware", "ransomware",
    "hardening", "least privilege", "defense in depth", "threat model",
    "supply chain", "sbom", "typosquat", "dependency audit",
    "prompt injection", "jailbreak", "guardrail", "sandbox escape",
    "iam", "rbac", "audit log", "incident response", "forensic",
]

# Termos de alto ruido: entram no pool, mas sozinhos NAO qualificam como candidata
# forte. Medidos em EXP-001: `token` 20,69%, `audit` 16,24%, `permission` 10,07%.
NOISY_ALONE = ["token", "audit", "permission", "sandbox", "safety", "validate"]


def like_any(col: str, terms: list[str]) -> str:
    return " OR ".join(f"{col} LIKE '%{t}%'" for t in terms)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default=str(DEFAULT_DATA_DIR))
    ap.add_argument("--per-stratum", type=int, default=12,
                    help="itens amostrados por estrato (default 12)")
    args = ap.parse_args()

    data_dir = Path(args.data_dir)
    art = data_dir / "artifacts"
    if not list(art.glob("*.parquet")):
        print(f"ERRO: nenhum Parquet em {art}", file=sys.stderr)
        return 1

    A = f"read_parquet('{(art / '*.parquet').as_posix()}')"
    con = duckdb.connect()
    con.execute("SET enable_progress_bar=false")

    body_hit = like_any("lower(content)", RETRIEVAL_TERMS)
    fm_hit = like_any("lower(coalesce(name,'') || ' ' || coalesce(description,''))",
                      RETRIEVAL_TERMS)
    density = " + ".join(
        f"CASE WHEN lower(content) LIKE '%{t}%' THEN 1 ELSE 0 END"
        for t in RETRIEVAL_TERMS
    )

    con.execute(f"""
        CREATE TEMP TABLE cand AS
        SELECT file_sha, repo_full_name, path, name, description,
               body_chars, has_scripts, sibling_count, content,
               ({density}) AS kw_density,
               ({fm_hit}) AS fm_signal
        FROM {A}
        WHERE dedup_primary = 1 AND content IS NOT NULL AND ({body_hit} OR {fm_hit})
    """)

    # Estratos desenhados para expor as fronteiras, nao para representatividade.
    # A amostra e para DESCOBERTA (open coding), nao para estimar prevalencia.
    strata = {
        "S1_frontmatter_signal":
            "fm_signal",
        "S2_body_high_density":
            "NOT fm_signal AND kw_density >= 5",
        "S3_body_low_density":
            "NOT fm_signal AND kw_density BETWEEN 1 AND 2",
        "S4_with_scripts":
            "has_scripts = 1 AND kw_density >= 3",
    }

    out = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "duckdb_version": duckdb.__version__,
        "n_retrieval_terms": len(RETRIEVAL_TERMS),
        "noisy_alone_terms": NOISY_ALONE,
        "per_stratum": args.per_stratum,
    }

    out["n_primary_total"] = con.execute(
        f"SELECT count(*) FROM {A} WHERE dedup_primary = 1 AND content IS NOT NULL"
    ).fetchone()[0]
    out["n_candidate_pool"] = con.execute("SELECT count(*) FROM cand").fetchone()[0]
    out["pct_candidate_pool"] = round(
        100 * out["n_candidate_pool"] / out["n_primary_total"], 2)

    out["kw_density_distribution"] = [
        {"kw_density": d, "n": n} for d, n in con.execute(
            "SELECT least(kw_density, 15), count(*) FROM cand GROUP BY 1 ORDER BY 1"
        ).fetchall()
    ]

    out["strata"] = {}
    for label, pred in strata.items():
        n = con.execute(f"SELECT count(*) FROM cand WHERE {pred}").fetchone()[0]
        out["strata"][label] = {"predicate": pred, "n": n}

    # Amostra deterministica: ORDER BY hash(file_sha), sem seed externa.
    union = " UNION ALL ".join(
        f"""(SELECT '{label}' AS stratum, file_sha, repo_full_name, path, name,
                    description, body_chars, has_scripts, kw_density, content
             FROM cand WHERE {pred}
             ORDER BY hash(file_sha) LIMIT {args.per_stratum})"""
        for label, pred in strata.items()
    )
    con.execute(f"CREATE TEMP TABLE sample AS {union}")

    RESULTS_DIR.mkdir(exist_ok=True)
    sample_path = RESULTS_DIR / "EXP-002_sample.parquet"
    con.execute(
        f"COPY (SELECT * FROM sample) TO '{sample_path.as_posix()}' (FORMAT PARQUET)")
    out["n_sample"] = con.execute("SELECT count(*) FROM sample").fetchone()[0]

    # Preview truncado para leitura manual (open coding).
    rows = con.execute("""
        SELECT stratum, file_sha, name, description, body_chars, has_scripts,
               kw_density, substr(content, 1, 1400)
        FROM sample ORDER BY stratum, hash(file_sha)
    """).fetchall()
    lines = ["# EXP-002 - Amostra para open coding (QI-2)", "",
             "Gerado por `scripts/build_candidate_frame.py`. Texto truncado em 1400",
             "caracteres. **Amostra de descoberta, nao de prevalencia.**", ""]
    for st, sha, nm, desc, bc, hs, kd, txt in rows:
        lines += [
            f"## [{st}] `{sha[:12]}`", "",
            f"- **name:** {nm or '(sem front matter)'}",
            f"- **description:** {(desc or '(nenhuma)')[:300]}",
            f"- **body_chars:** {bc} · **has_scripts:** {hs} · **kw_density:** {kd}",
            "", "```markdown", (txt or "").strip(), "```", "",
        ]
    (RESULTS_DIR / "EXP-002_sample_preview.md").write_text(
        "\n".join(lines), encoding="utf-8")

    (RESULTS_DIR / "EXP-002_frame.json").write_text(
        json.dumps(out, indent=2, default=str), encoding="utf-8")

    print(f"pool: {out['n_candidate_pool']:,} / {out['n_primary_total']:,} "
          f"({out['pct_candidate_pool']}%)")
    for label, d in out["strata"].items():
        print(f"  {label:26s} {d['n']:>9,}")
    print(f"amostra: {out['n_sample']} -> {sample_path.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
