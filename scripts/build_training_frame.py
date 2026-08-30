#!/usr/bin/env python3
"""
EXP-012 - Monta o frame de treino do classificador v1 a partir do golden set
operacional de EXP-005 (results/EXP-005_annotation_form_filled_updated.csv).

NATUREZA: EXP-005_annotation_form_filled_updated.csv foi produzido com
assistencia de LLM. E o golden set OPERACIONAL desta iteracao exploratoria
v1, nao um gold standard humano definitivo (ver Decision Log D-0XX -
classificador definitivo da iteracao v1).

O QUE ESTE SCRIPT FAZ
  1. le os rotulos de EXP-005_annotation_form_filled_updated.csv (case_id ->
     security_relevance e demais campos humanos);
  2. le a chave case_id -> file_sha de EXP-005_pilot_sample.parquet;
  3. busca o TEXTO BRUTO (content) de cada file_sha no dataset original via
     DuckDB - o formulario e cego por desenho (R-11/D-021) e nao contem o
     corpo do texto;
  4. NAO reincorpora nenhum campo de EXP-005_strata_key.csv (tier,
     kw_density, domain_decl, fm_signal, grc_flag, code_review_flag,
     selection_reason) - esses sinais decidiram a SELECAO da amostra e
     vazariam informacao posterior/derivada para o classificador;
  5. exclui AMBIGUOUS (n=1) do conjunto supervisionado (suporte insuficiente
     para qualquer fold), mas mantem no arquivo de saida com
     used_in_training=false, para nao apagar o caso;
  6. deriva o rotulo binario SECURITY = PRIMARY+SECONDARY vs
     NON_SECURITY = MENTION+NONE.

SAIDA
  results/EXP-012_training_frame.parquet (gitignored: contem texto de
  terceiros, regeneravel por este script - mesma politica de EXP-002/EXP-005)

Uso:
    uv run --with duckdb --with pandas python scripts/build_training_frame.py
"""

import sys
from pathlib import Path

import duckdb
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "raw" / "gitskills" / "data"
RESULTS_DIR = ROOT / "results"

LABELS_CSV = RESULTS_DIR / "EXP-005_annotation_form_filled_updated.csv"
PILOT_PARQUET = RESULTS_DIR / "EXP-005_pilot_sample.parquet"
OUT_PARQUET = RESULTS_DIR / "EXP-012_training_frame.parquet"

# Colunas de EXP-005_strata_key.csv - NUNCA devem entrar aqui (vazamento de
# selecao). Listadas explicitamente para que uma futura mudanca de esquema
# quebre em vez de vazar em silencio.
FORBIDDEN_LEAK_COLUMNS = {
    "tier", "kw_density", "domain_decl", "fm_signal", "grc_flag",
    "code_review_flag", "selection_reason", "lang_group", "lang_primary",
    "lang_secondary", "lang_secondary_conf", "detector_agreement",
    "is_mixed", "minor_share", "has_scripts",
}


def main() -> int:
    if not LABELS_CSV.exists():
        print(f"ERRO: {LABELS_CSV} nao encontrado", file=sys.stderr)
        return 1
    if not PILOT_PARQUET.exists():
        print(f"ERRO: {PILOT_PARQUET} nao encontrado (gitignored, gerado por "
              f"scripts/build_pilot_sample.py)", file=sys.stderr)
        return 1

    labels = pd.read_csv(LABELS_CSV, dtype=str, keep_default_na=False)
    assert set(labels.columns) & FORBIDDEN_LEAK_COLUMNS == set(), (
        "EXP-005_annotation_form_filled_updated.csv contem coluna de "
        "selecao/triagem - vazamento potencial, abortando")
    labels = labels.replace({"": None})
    n_total = len(labels)

    con = duckdb.connect()
    con.execute("SET enable_progress_bar=false")
    pilot = con.execute(
        f"SELECT case_id, file_sha FROM read_parquet("
        f"'{PILOT_PARQUET.as_posix()}')"
    ).fetchdf()

    art_glob = (DATA_DIR / "artifacts" / "*.parquet").as_posix()
    shas = ", ".join(f"'{s}'" for s in pilot["file_sha"].tolist())
    content = con.execute(f"""
        SELECT file_sha, repo_full_name, path, content, name, description,
               body_chars
        FROM read_parquet('{art_glob}')
        WHERE dedup_primary = 1 AND file_sha IN ({shas})
    """).fetchdf()

    labels_dedup = labels.drop(columns=["name", "body_chars"])
    merged = (labels_dedup.merge(pilot, on="case_id", how="left", validate="1:1")
                          .merge(content, on="file_sha", how="left", validate="1:1"))

    missing_text = merged["content"].isna().sum()
    if missing_text:
        print(f"AVISO: {missing_text} casos sem content recuperado do "
              f"dataset original", file=sys.stderr)

    merged["text"] = merged["content"].fillna("")
    merged["used_in_training"] = merged["security_relevance"] != "AMBIGUOUS"
    merged["binary_label"] = merged["security_relevance"].map({
        "PRIMARY": "SECURITY", "SECONDARY": "SECURITY",
        "MENTION": "NON_SECURITY", "NONE": "NON_SECURITY",
    })

    out_cols = [
        "case_id", "file_sha", "repo_full_name", "path",
        "human_language", "security_relevance", "binary_label",
        "used_in_training", "body_chars", "name", "description", "text",
    ]
    merged = merged[out_cols]

    RESULTS_DIR.mkdir(exist_ok=True)
    merged.to_parquet(OUT_PARQUET, index=False)

    n_train = int(merged["used_in_training"].sum())
    print(f"casos totais: {n_total} | usados no treino/CV: {n_train} | "
          f"excluidos (AMBIGUOUS): {n_total - n_train}")
    print("\ndistribuicao security_relevance (todos):")
    print(merged["security_relevance"].value_counts().to_string())
    print("\ndistribuicao binary_label (used_in_training apenas):")
    print(merged.loc[merged["used_in_training"], "binary_label"]
          .value_counts().to_string())
    dup_repos = (merged["repo_full_name"].value_counts()
                 .loc[lambda s: s > 1])
    if len(dup_repos):
        print(f"\nAVISO: {len(dup_repos)} repositorio(s) aparecem mais de "
              f"uma vez na amostra (risco de nao-independencia):")
        print(dup_repos.to_string())
    else:
        print("\nnenhum repositorio duplicado na amostra "
              "(1 caso por repositorio)")
    print(f"\nOK -> {OUT_PARQUET.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
