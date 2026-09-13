"""EXP-014 - Consolida o gold set da QI-1 num arquivo unico e reproduzivel.

Junta as duas origens de rotulo previstas no D-026 e no D-031:

  - consenso entre os dois modelos (84 casos, EXP-014_consensus_labels.jsonl)
  - decisao humana nos 16 casos em que os modelos divergiram
    (EXP-014_adjudication_form.csv), feita por dois anotadores independentes
    (EXP-014_adjudication_victor.csv, EXP-014_adjudication_havillon.csv) com
    reconciliacao mutua onde discordaram

e aplica o quadro de analise do EXP-016: caso fora do quadro sai do gold set
(LLM078, 75 caracteres, abaixo do limiar do D-028).

Tambem registra as marcacoes de quadro que NAO removem o caso daqui:
  - truncated_undecidable (D-028) quando os DOIS modelos marcaram - o caso
    sai da populacao na estimativa e exige limites de Manski;
  - not_an_instruction_artifact (D-030) - marcado, exclusao adiada.

A estimativa do sumario e PRELIMINAR: trata a amostra como aleatoria simples
do quadro, e a maior parte dos rotulos vem de consenso de LLM nao verificado
por humano (risco declarado do D-026). Nao e a resposta da QI-1 - essa sai do
E-9.

Nunca escreve nos formularios de anotacao.

Uso:
    uv run --with duckdb python scripts/build_gold_set.py

Saidas:
    results/EXP-014_gold_set.csv            um caso por linha (versionado)
    results/EXP-014_gold_set_summary.json   contagens e estimativa preliminar
"""
from __future__ import annotations

import csv
import json
import math
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
SECURITY = {"PRIMARY", "SECONDARY"}
CLASSES = {"PRIMARY", "SECONDARY", "NONE"}
MARKING_FIX = re.compile(
    r"rotulo corrigido de (PRIMARY|SECONDARY|NONE) para (PRIMARY|SECONDARY|NONE)")

INPUTS = {
    "consensus": RESULTS / "EXP-014_consensus_labels.jsonl",
    "form": RESULTS / "EXP-014_adjudication_form.csv",
    "victor": RESULTS / "EXP-014_adjudication_victor.csv",
    "havillon": RESULTS / "EXP-014_adjudication_havillon.csv",
    "gpt": RESULTS / "EXP-014_gpt_output.jsonl",
    "claude": RESULTS / "EXP-014_claude_output.jsonl",
    "sample": RESULTS / "EXP-013_llm_sample.csv",
    "frame": RESULTS / "EXP-016_analysis_frame.parquet",
}

# Etiqueta que o formulario principal usa no inicio da nota, por origem.
# O script DERIVA a origem dos arquivos individuais e confere contra ela.
ORIGIN_TAG = {
    "human_agreement": "[CONCORDANCIA]",
    "human_agreement_after_marking_fix": "[CONCORDANCIA apos correcao",
    "human_reconciliation": "[RECONCILIACAO",
}


def read_jsonl(path: Path) -> dict[str, dict]:
    with path.open(encoding="utf-8") as f:
        objs = [json.loads(line) for line in f if line.strip()]
    return {o["case_id"]: o for o in objs}


def read_csv(path: Path) -> dict[str, dict]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return {r["case_id"].strip(): r for r in csv.DictReader(f)}


def original_label(row: dict) -> str:
    """Rotulo antes de qualquer correcao de marcacao registrada na nota."""
    current = row["security_relevance"].strip().upper()
    m = MARKING_FIX.search(row.get("note") or "")
    return m.group(1) if m else current


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    den = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, centre - half), min(1.0, centre + half))


def frame_membership(shas: list[str]) -> dict[str, tuple[bool, str]]:
    import duckdb

    con = duckdb.connect()
    con.execute("SET enable_progress_bar=false")
    quoted = ", ".join(f"'{s}'" for s in shas)
    rows = con.execute(
        f"SELECT file_sha, exclusion_reason "
        f"FROM read_parquet('{INPUTS['frame'].as_posix()}') "
        f"WHERE file_sha IN ({quoted})"
    ).fetchall()
    return {sha: (reason is None, reason or "") for sha, reason in rows}


def estimate(units: list[dict]) -> dict:
    n = len(units)
    k = sum(r["is_security_skill"] == "true" for r in units)
    kp = sum(r["security_relevance"] == "PRIMARY" for r in units)
    ks = sum(r["security_relevance"] == "SECONDARY" for r in units)

    def block(x: int) -> dict:
        lo, hi = wilson(x, n)
        return {"k": x, "proportion": round(x / n, 4), "wilson95": [round(lo, 4), round(hi, 4)]}

    return {"n": n, "security_skill": block(k), "primary": block(kp), "secondary": block(ks)}


def main() -> None:
    missing = [k for k, p in INPUTS.items() if not p.exists()]
    if missing:
        raise SystemExit(
            f"ERRO: insumo ausente: {', '.join(missing)}. O parquet do quadro e "
            "gitignored - regenerar com scripts/build_analysis_frame.py")

    consensus = read_jsonl(INPUTS["consensus"])
    form = read_csv(INPUTS["form"])
    victor = read_csv(INPUTS["victor"])
    havillon = read_csv(INPUTS["havillon"])
    gpt = read_jsonl(INPUTS["gpt"])
    claude = read_jsonl(INPUTS["claude"])
    sample = read_csv(INPUTS["sample"])

    failures: list[str] = []
    if set(consensus) & set(form):
        failures.append("caso presente no consenso E na adjudicacao")
    if set(form) != set(victor) or set(form) != set(havillon):
        failures.append("formulario principal e individuais nao tem os mesmos casos")
    all_ids = sorted(set(consensus) | set(form))
    if len(all_ids) != 100 or set(all_ids) != set(sample):
        failures.append(f"esperados os 100 casos da amostra; vieram {len(all_ids)}")

    membership = frame_membership([sample[c]["file_sha"] for c in all_ids if c in sample])

    rows = []
    for cid in all_ids:
        sha = sample[cid]["file_sha"]
        in_frame, reason = membership.get(sha, (False, "not_found_in_frame"))

        if cid in form:
            label = form[cid]["security_relevance"].strip().upper()
            frame_excl = form[cid]["frame_exclusion"].strip()
            v_now = victor[cid]["security_relevance"].strip().upper()
            h_now = havillon[cid]["security_relevance"].strip().upper()
            if original_label(victor[cid]) == original_label(havillon[cid]):
                origin = "human_agreement"
            elif v_now == h_now:
                origin = "human_agreement_after_marking_fix"
            else:
                origin = "human_reconciliation"
            if v_now == h_now and label != v_now:
                failures.append(f"{cid}: anotadores concordam ({v_now}) e o formulario diz {label}")
            if not form[cid]["note"].startswith(ORIGIN_TAG[origin]):
                failures.append(f"{cid}: origem derivada ({origin}) nao bate com a etiqueta da nota")
        else:
            label = consensus[cid]["security_relevance"].strip().upper()
            fg = (gpt.get(cid, {}).get("frame_exclusion") or "").strip()
            fc = (claude.get(cid, {}).get("frame_exclusion") or "").strip()
            frame_excl = fg if fg and fg == fc else ""
            origin = "llm_consensus"

        if label not in CLASSES:
            failures.append(f"{cid}: rotulo invalido {label!r}")
        rows.append({
            "case_id": cid,
            "file_sha": sha,
            "security_relevance": label,
            "is_security_skill": str(label in SECURITY).lower(),
            "frame_exclusion": frame_excl,
            "label_origin": origin,
            "in_analysis_frame": str(in_frame).lower(),
            "exclusion_reason": reason,
        })

    gold = [r for r in rows if r["in_analysis_frame"] == "true"]
    out_of_frame = {r["case_id"]: r["exclusion_reason"] for r in rows if r["in_analysis_frame"] != "true"}
    if len(gold) != 99 or list(out_of_frame) != ["LLM078"]:
        failures.append(f"esperado 99 no quadro e so LLM078 fora; veio {len(gold)} e fora={list(out_of_frame)}")
    if len({r["case_id"] for r in gold}) != len(gold):
        failures.append("case_id duplicado")

    if failures:
        raise SystemExit("ERRO - verificacoes falharam:\n  " + "\n  ".join(failures))

    with (RESULTS / "EXP-014_gold_set.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(gold[0]))
        writer.writeheader()
        writer.writerows(gold)

    truncated = [r["case_id"] for r in gold if r["frame_exclusion"] == "truncated_undecidable"]
    not_instr = [r["case_id"] for r in gold if r["frame_exclusion"] == "not_an_instruction_artifact"]

    base = [r for r in gold if r["frame_exclusion"] != "truncated_undecidable"]
    base_no_artifacts = [r for r in base if r["frame_exclusion"] != "not_an_instruction_artifact"]
    k_base = sum(r["is_security_skill"] == "true" for r in base)
    manski = {
        "note": ("D-028: casos truncated_undecidable tem desfecho desconhecido. Limites "
                 "sobre os casos do quadro, assumindo todos nao-Security e todos Security."),
        "cases": truncated,
        "n": len(gold),
        "lower": round(k_base / len(gold), 4),
        "upper": round((k_base + len(truncated)) / len(gold), 4),
    }

    summary = {
        "experiment": "EXP-014",
        "decisions": ["D-026", "D-028", "D-030", "D-031"],
        "n_input_cases": len(rows),
        "n_gold_in_frame": len(gold),
        "out_of_frame": out_of_frame,
        "by_class": dict(Counter(r["security_relevance"] for r in gold)),
        "by_origin": dict(Counter(r["label_origin"] for r in gold)),
        "frame_flags": {
            "truncated_undecidable": truncated,
            "not_an_instruction_artifact": not_instr,
        },
        "preliminary_estimate": {
            "WARNING": (
                "PRELIMINAR. Trata a amostra como aleatoria simples do quadro de analise "
                "(EXP-016). A maior parte dos rotulos vem de consenso de LLM sem "
                "verificacao humana (D-026). Nao e a resposta da QI-1."),
            "frame_population": 1550550,
            "main": {
                "definition": ("quadro sem truncated_undecidable; not_an_instruction_artifact "
                               "mantidos (D-030: exclusao adiada)"),
                **estimate(base),
            },
            "sensitivity_without_not_an_instruction_artifact": {
                "definition": "idem, excluindo tambem os not_an_instruction_artifact",
                **estimate(base_no_artifacts),
            },
            "manski_bounds_truncated": manski,
        },
    }
    (RESULTS / "EXP-014_gold_set_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    e = summary["preliminary_estimate"]["main"]
    s = e["security_skill"]
    print(f"gold set: {len(gold)} casos no quadro | fora: {out_of_frame}")
    print("classes :", summary["by_class"])
    print("origem  :", summary["by_origin"])
    print("marcas  :", summary["frame_flags"])
    print(f"preliminar (n={e['n']}): Security Skill {s['proportion']:.1%} "
          f"IC95 [{s['wilson95'][0]:.1%}, {s['wilson95'][1]:.1%}] | "
          f"PRIMARY {e['primary']['proportion']:.1%} | SECONDARY {e['secondary']['proportion']:.1%}")
    print(f"Manski ({', '.join(truncated)}): [{manski['lower']:.1%}, {manski['upper']:.1%}]")
    print("OK -> results/EXP-014_gold_set.csv, results/EXP-014_gold_set_summary.json")


if __name__ == "__main__":
    main()
