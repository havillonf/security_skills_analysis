"""EXP-016 - Constroi o quadro de analise: aplica as exclusoes de frame em
SEQUENCIA e produz o denominador real da QI-1.

Ate aqui cada exclusao tinha sido medida isoladamente contra a populacao
inteira (D-025, D-028, D-030). Elas se sobrepoem - uma skill pode ser
nao-inglesa E pequena - entao os percentuais NAO podem ser subtraidos um do
outro. Este script aplica na ordem e reporta quantos saem em cada passo.

Etapas (a numeracao acompanha notes/03 - Methodology.md):

  1. Unidade de analise    dedup_primary = 1 AND content IS NOT NULL   (D-001)
  2. Somente ingles        is_purely_english = true                    (D-025)
  3. Evidencia minima      len(description) + body_chars >= LIMIAR     (D-028)
  4. Genero do documento   marca, NAO exclui                           (D-030)

Por que a etapa 4 marca em vez de excluir: a regra de procedencia tem
precisao alta e recall baixo (707 arquivos, 0,038% da populacao, contra os
~35 mil que a amostra sugere - ver EXP-015). Excluir so esses removeria 0,04%
e faria o quadro PARECER saneado. Entao ela vira ESTRATIFICADOR, no mesmo
espirito do D-014: contagem de positivos nao e taxa. A exclusao de verdade
espera a estimativa da taxa em F3.

A exclusao `truncated_undecidable` (D-028) NAO esta aqui de proposito: ela
depende de o anotador nao conseguir decidir, entao so existe durante a
anotacao, caso a caso. Nao ha como aplica-la em escala.

Uso:
    uv run --with duckdb python scripts/build_analysis_frame.py
    uv run --with duckdb python scripts/build_analysis_frame.py --min-evidence 200

Saidas:
    results/EXP-016_analysis_frame_summary.json   agregados (versionado)
    results/EXP-016_analysis_frame.parquet        rotulo por arquivo (gitignored)
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"
ARTIFACTS = "read_parquet('data/raw/gitskills/data/artifacts/*.parquet')"
ENGLISH_CSV = "results/EXP-013_population_english_filter.csv"

DEFAULT_MIN_EVIDENCE = 200  # D-028
HEAD_CHARS = 2500  # D-030 / EXP-015

# `**Generated**:` nao casa com '%generated:%' - o `:` fica fora do negrito.
# Por isso `*` e `#` sao removidos antes do LIKE. Sem isso a regra perde
# metade dos casos conhecidos (ver EXP-015).
PROVENANCE_MARKERS = [
    "generated:",
    "generated on ",
    "date range:",
    "input type:",
    "document metadata",
    "report generated",
    "analysis date",
]


def _or_like(column: str, markers: list[str]) -> str:
    return " OR ".join(f"{column} LIKE '%{m}%'" for m in markers)


def build(con: duckdb.DuckDBPyConnection, min_evidence: int) -> None:
    """Cria a view `frame` com um rotulo por arquivo da populacao base."""
    english_path = ROOT / ENGLISH_CSV
    if not english_path.exists():
        raise SystemExit(
            f"ERRO: {ENGLISH_CSV} nao existe.\n"
            "Ele e gitignored (95 MB) e regeneravel por "
            "scripts/filter_population_english.py - ver o cabecalho daquele "
            "script: a execucao leva horas e e mais estavel no WSL."
        )

    head_expr = (
        f"lower(replace(replace(substr(content, 1, {HEAD_CHARS}), '*', ''), '#', ''))"
    )
    con.execute(f"""
        CREATE OR REPLACE VIEW base AS
        SELECT
            file_sha,
            frontmatter_valid,
            name,
            length(coalesce(description, '')) + coalesce(body_chars, 0) AS evidence_chars,
            {head_expr} AS head
        FROM {ARTIFACTS}
        WHERE dedup_primary = 1 AND content IS NOT NULL
    """)
    con.execute(f"""
        CREATE OR REPLACE VIEW english AS
        SELECT file_sha, is_purely_english
        FROM read_csv('{ENGLISH_CSV}', header = true, auto_detect = true)
    """)
    con.execute(f"""
        CREATE OR REPLACE VIEW frame AS
        SELECT
            b.file_sha,
            b.frontmatter_valid,
            b.evidence_chars,
            coalesce(e.is_purely_english, false) AS is_purely_english,
            ({_or_like('b.head', PROVENANCE_MARKERS)}) AS provenance,
            -- etapa 2 e 3, na ordem; o primeiro criterio que barra e o que fica
            CASE
                WHEN NOT coalesce(e.is_purely_english, false) THEN 'not_english'
                WHEN b.evidence_chars < {min_evidence}        THEN 'below_min_evidence'
                ELSE NULL
            END AS exclusion_reason
        FROM base b
        LEFT JOIN english e USING (file_sha)
    """)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--min-evidence", type=int, default=DEFAULT_MIN_EVIDENCE,
                        help=f"limiar do D-028 (padrao {DEFAULT_MIN_EVIDENCE})")
    parser.add_argument("--out-dir", type=Path, default=RESULTS_DIR)
    args = parser.parse_args()

    started = time.time()
    con = duckdb.connect()
    con.execute("SET enable_progress_bar=false")
    build(con, args.min_evidence)

    # --- cascata: quantos sobram apos cada etapa, na ordem ---
    n_base = con.execute("SELECT count(*) FROM base").fetchone()[0]
    n_english = con.execute(
        "SELECT count(*) FROM frame WHERE is_purely_english").fetchone()[0]
    n_frame = con.execute(
        "SELECT count(*) FROM frame WHERE exclusion_reason IS NULL").fetchone()[0]

    # --- marginais: cada criterio contra a populacao inteira, isolado ---
    marginal = con.execute(f"""
        SELECT
            count(*) FILTER (WHERE NOT is_purely_english)            AS not_english,
            count(*) FILTER (WHERE evidence_chars < {args.min_evidence}) AS below_min,
            count(*) FILTER (WHERE NOT is_purely_english
                             AND evidence_chars < {args.min_evidence}) AS both
        FROM frame
    """).fetchone()

    # --- estratos de genero, DENTRO do quadro final (D-030) ---
    strata_rows = con.execute("""
        SELECT
            CASE
                WHEN frontmatter_valid = 1 AND NOT provenance THEN 'F1_presumed_instruction'
                WHEN frontmatter_valid = 1 AND provenance     THEN 'F1b_provenance_with_frontmatter'
                WHEN frontmatter_valid = 0 AND provenance     THEN 'F2_rule_candidate'
                ELSE 'F3_unknown'
            END AS genre_stratum,
            count(*) AS n
        FROM frame WHERE exclusion_reason IS NULL
        GROUP BY 1 ORDER BY 2 DESC
    """).fetchall()

    # --- verificacao de integridade ---
    checks = con.execute(f"""
        SELECT
            (SELECT count(*) FROM frame) = {n_base}                        AS join_preserva_linhas,
            (SELECT count(DISTINCT file_sha) FROM frame) = {n_base}        AS file_sha_unico,
            (SELECT count(*) FROM frame WHERE exclusion_reason IS NULL
                AND (NOT is_purely_english OR evidence_chars < {args.min_evidence})) = 0
                                                                           AS nenhum_excluido_no_quadro,
            (SELECT count(*) FROM english) = {n_base}                      AS csv_ingles_cobre_populacao
    """).fetchone()
    check_names = ["join_preserva_linhas", "file_sha_unico",
                   "nenhum_excluido_no_quadro", "csv_ingles_cobre_populacao"]
    failed = [n for n, ok in zip(check_names, checks) if not ok]

    out_dir = args.out_dir
    out_dir.mkdir(exist_ok=True)
    parquet_path = out_dir / "EXP-016_analysis_frame.parquet"
    con.execute(f"""
        COPY (
            SELECT file_sha, frontmatter_valid, evidence_chars, is_purely_english,
                   provenance, exclusion_reason,
                   CASE
                       WHEN frontmatter_valid = 1 AND NOT provenance THEN 'F1_presumed_instruction'
                       WHEN frontmatter_valid = 1 AND provenance     THEN 'F1b_provenance_with_frontmatter'
                       WHEN frontmatter_valid = 0 AND provenance     THEN 'F2_rule_candidate'
                       ELSE 'F3_unknown'
                   END AS genre_stratum
            FROM frame
        ) TO '{parquet_path.as_posix()}' (FORMAT PARQUET, COMPRESSION ZSTD)
    """)

    payload = {
        "experiment": "EXP-016",
        "question": "Qual e o denominador da QI-1 depois das exclusoes de frame, aplicadas em sequencia?",
        "duckdb_version": duckdb.__version__,
        "min_evidence_chars": args.min_evidence,
        "head_chars": HEAD_CHARS,
        "provenance_markers": PROVENANCE_MARKERS,
        "waterfall": [
            {"step": 1, "decision": "D-001", "criterion": "dedup_primary = 1 AND content IS NOT NULL",
             "remaining": n_base, "removed": 0},
            {"step": 2, "decision": "D-025", "criterion": "is_purely_english",
             "remaining": n_english, "removed": n_base - n_english},
            {"step": 3, "decision": "D-028", "criterion": f"length(description) + body_chars >= {args.min_evidence}",
             "remaining": n_frame, "removed": n_english - n_frame},
        ],
        "frame_size": n_frame,
        "frame_pct_of_base": round(100 * n_frame / n_base, 3),
        "marginal_counts": {
            "note": "cada criterio isolado contra a populacao base; SE SOBREPOEM, nao somar",
            "not_english": marginal[0],
            "below_min_evidence": marginal[1],
            "both": marginal[2],
        },
        "genre_strata_within_frame": {
            "note": ("D-030: MARCA, nao exclui. A exclusao espera a estimativa "
                     "da taxa de nao-instrucao em F3 (ver EXP-015)."),
            "strata": [{"stratum": s, "n": n, "pct_of_frame": round(100 * n / n_frame, 4)}
                       for s, n in strata_rows],
        },
        "not_applied_here": {
            "truncated_undecidable": (
                "D-028. Depende de o anotador nao conseguir decidir; so existe "
                "durante a anotacao, caso a caso. Nao ha versao em escala."
            ),
            "not_an_instruction_artifact": (
                "D-030. Marcado como estrato acima, nao excluido."
            ),
        },
        "integrity_checks": dict(zip(check_names, [bool(c) for c in checks])),
        "elapsed_seconds": round(time.time() - started, 1),
    }
    summary_path = out_dir / "EXP-016_analysis_frame_summary.json"
    summary_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    print("CASCATA (na ordem; e assim que o denominador se forma)")
    print(f"  1. unidade de analise (D-001)      {n_base:>10,}")
    print(f"  2. somente ingles     (D-025)      {n_english:>10,}   -{n_base - n_english:,}")
    print(f"  3. evidencia >= {args.min_evidence:<4}  (D-028)      {n_frame:>10,}   -{n_english - n_frame:,}")
    print(f"\n  QUADRO DE ANALISE                  {n_frame:>10,}   "
          f"({payload['frame_pct_of_base']}% da populacao base)")

    print("\nMARGINAIS (isolados; SE SOBREPOEM - nao somar)")
    print(f"  nao ingles                         {marginal[0]:>10,}")
    print(f"  abaixo do limiar                   {marginal[1]:>10,}")
    print(f"  os dois ao mesmo tempo             {marginal[2]:>10,}")

    print("\nESTRATOS DE GENERO dentro do quadro (D-030: marca, nao exclui)")
    for s, n in strata_rows:
        print(f"  {s:34} {n:>10,}   {100 * n / n_frame:6.3f}%")

    print("\nVERIFICACAO")
    for name, ok in zip(check_names, checks):
        print(f"  [{'OK ' if ok else 'FALHA'}] {name}")
    if failed:
        raise SystemExit(f"\nERRO: verificacao falhou: {', '.join(failed)}")

    print(f"\nOK -> results/{summary_path.name}")
    print(f"OK -> results/{parquet_path.name}  (gitignored)")
    print(f"[{payload['elapsed_seconds']}s]")


if __name__ == "__main__":
    main()
