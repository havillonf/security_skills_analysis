"""EXP-013 (continuação) — Monta o formulário cego de adjudicação humana
(Decision Log D-026) a partir da saída de aggregate_llm_classifications.py.

Lê EXP-013_comparison_report.jsonl (todo caso, com status UNANIMOUS /
DISCORDANT / INCOMPLETE / MISSING) e EXP-013_llm_sample.csv (metadados não
sensíveis dos 100 casos), filtra os que precisam de adjudicação
(DISCORDANT, INCOMPLETE, MISSING) e produz um CSV cego — sem file_sha, sem
sinal de seleção/tier (D-020/D-021) e sem a resposta de nenhum dos três
modelos — nos moldes do formulário de EXP-005
(results/_arquivo/EXP-005_annotation_form.csv), para o pesquisador preencher lendo
o texto completo em results/EXP-013_llm_cases/<case_id>.md, seguindo
"Guia do Anotador Humano.md" (Codebook v2.4).

Uso:
    uv run python scripts/build_adjudication_form.py
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = REPO_ROOT / "results"

NEEDS_ADJUDICATION = {"DISCORDANT", "INCOMPLETE", "MISSING"}

FORM_COLUMNS = [
    # metadados nao sensiveis, para localizar o caso
    "case_id",
    "name",
    "body_chars",
    "status_reason",
    # --- os cinco campos da primeira classificacao (Codebook v2.5, D-029) ---
    "security_relevance",   # PRIMARY | SECONDARY | NONE
    "evidence",             # description | body | bundled_artifacts (; separa)
    "frame_exclusion",      # vazio | truncated_undecidable
    "confidence",           # high | medium | low -- metadado, nao medida
    "note",                 # papel + conteudo de seguranca (ou por que nao) + elemento concreto
    # instrumentacao opcional do piloto
    "annotation_seconds",
]


def load_sample_metadata(sample_csv: str) -> dict[str, dict]:
    meta = {}
    with (RESULTS_DIR / sample_csv).open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            meta[row["case_id"]] = row
    return meta


def load_comparison_report(report_jsonl: str) -> dict[str, dict]:
    reports = {}
    with (RESULTS_DIR / report_jsonl).open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            reports[obj["case_id"]] = obj
    return reports


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--prefix", default="EXP-014",
                    help="Prefixo do experimento de classificacao")
    ap.add_argument("--sample", default="EXP-013_llm_sample.csv",
                    help="CSV da amostra (pode ser de outro EXP)")
    args = ap.parse_args()

    meta = load_sample_metadata(args.sample)
    reports = load_comparison_report(f"{args.prefix}_comparison_report.jsonl")

    rows = []
    for case_id, report in sorted(reports.items()):
        if report["status"] not in NEEDS_ADJUDICATION:
            continue
        m = meta.get(case_id, {})
        rows.append(
            {
                "case_id": case_id,
                "name": m.get("name", ""),
                "body_chars": m.get("body_chars", ""),
                "status_reason": report["status"],
                "security_relevance": "",
                "evidence": "",
                "frame_exclusion": "",
                "confidence": "",
                "note": "",
                "annotation_seconds": "",
            }
        )

    out_path = RESULTS_DIR / f"{args.prefix}_adjudication_form.csv"
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FORM_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    by_status = {}
    for r in rows:
        by_status[r["status_reason"]] = by_status.get(r["status_reason"], 0) + 1

    print(f"{len(rows)} casos escritos em {out_path}")
    print("Por motivo:", by_status)
    print(
        "Lembrete (Guia do Anotador Humano, Codebook v2.5): classifique cada case_id "
        "lendo results/EXP-013_llm_cases/<case_id>.md do zero, sem consultar "
        "a saída de nenhum modelo antes de decidir."
    )


if __name__ == "__main__":
    main()
