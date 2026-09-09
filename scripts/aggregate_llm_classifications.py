"""Agrega as saídas do ensemble de LLMs e decide unanimidade vs.
discordância (Decision Log D-026, mantido em D-027).

Lê um arquivo JSONL por modelo (um objeto por linha; schema em
"Classification Prompt.md" para o Codebook v2.5, ou
"Classification Prompt (D-026).md" Sec.4 para saídas antigas da v2.3),
casa por case_id, e separa:

  - casos unânimes: os modelos concordam na classe -> rótulo de consenso
    aceito sem revisão humana.
  - casos discordantes / incompletos / ausentes: vão para adjudicação
    humana (results/EXP-014_discordant_cases.jsonl), usando o
    Guia do Anotador Humano, Codebook v2.5.

Aceita DOIS ou TRÊS avaliadores (--gemini é opcional). Com dois não há
regra de maioria: toda divergência vai ao humano, e a estatística de
concordância aplicável é Cohen's kappa, não Fleiss'.

REGRA DE ADJUDICAÇÃO (D-029): a primeira classificação considera APENAS
`security_relevance`. As dimensões de apoio não disparam revisão humana --
serão refeitas na reclassificação taxonômica sobre PRIMARY+SECONDARY.
`evidence` continua sendo reportado na trilha de auditoria, mas como
informativo. Use --strict-all para que divergência nos campos informativos
também mande o caso a adjudicação.

Para os coeficientes de concordância (Cohen, Krippendorff, Gwet AC1,
Brennan-Prediger, McNemar) use scripts/compute_agreement.py.

Uso (dois avaliadores):
    python scripts/aggregate_llm_classifications.py \
        --gpt results/EXP-014_gpt_output.jsonl \
        --claude results/EXP-014_claude_output.jsonl

Nao requer dependencia externa (so stdlib) -- `uv run` e desnecessario, e
nesta maquina ele falhou silenciosamente com exit code 120 (ver EXP-013.md).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = REPO_ROOT / "results"

# Campos que DECIDEM discordancia.
#
# Sob o Codebook v2.5 (D-029) a adjudicacao da PRIMEIRA classificacao
# considera APENAS `security_relevance`. As dimensoes de apoio nao
# disparam revisao humana: serao refeitas na reclassificacao taxonomica
# posterior, sobre PRIMARY+SECONDARY.
#
# Historico: sob D-026 todas as dimensoes contavam (leitura literal de
# "qualquer dimensao"). O EXP-013 mediu kappa 0,070 em `confidence` e
# 0,36 em `rule_applied`; o EXP-014 mediu o resto e mostrou redundancia
# (security_focus == PRIMARY em 100/100) e medicao fraca
# (operation_level p_o=61%). Efeito da poda no EXP-014: a adjudicacao
# cai de 50 para 16 casos.
SCALAR_FIELDS = [
    "security_relevance",
]
# Campos presentes no schema mas fora da comparacao, por decisao
# metodologica (metadados) ou por nao-conformidade conhecida.
# `possible_non_english` e `secondary_mention_boundary` sairam do schema
# na v2.4; ficam listados para tolerar saidas antigas (EXP-013) sem que
# a ausencia deles contamine todo caso como INCOMPLETE.
UNCOMPARED_SCHEMA_FIELDS = [
    "confidence",
    "rule_applied",
    "frame_exclusion",
    # removidos do schema em v2.5 (D-029); listados para tolerar saidas
    # antigas sem contaminar todo caso como INCOMPLETE
    "security_focus",
    "operational_security",
    "operation_level",
    "grc_case",
    "security_functions",
    "security_concerns",
    "operational_capability",
    "possible_non_english",
    "secondary_mention_boundary",
]
# `evidence` e informativo: divergencia nele nao manda o caso a
# adjudicacao (D-029), mas continua reportada na trilha de auditoria.
CLOSED_LIST_FIELDS = []
OPEN_LIST_FIELDS = ["evidence"]
ALL_COMPARABLE_FIELDS = SCALAR_FIELDS + CLOSED_LIST_FIELDS + OPEN_LIST_FIELDS


def load_jsonl(path: Path) -> dict[str, dict]:
    records: dict[str, dict] = {}
    malformed = 0
    with path.open(encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as exc:
                malformed += 1
                print(f"  [{path.name}:{line_no}] linha JSON inválida: {exc}", file=sys.stderr)
                continue
            case_id = obj.get("case_id")
            if not case_id:
                print(f"  [{path.name}:{line_no}] sem case_id, ignorada", file=sys.stderr)
                continue
            if case_id in records:
                print(f"  [{path.name}:{line_no}] case_id duplicado ({case_id}), mantendo a primeira ocorrência", file=sys.stderr)
                continue
            records[case_id] = obj
    if malformed:
        print(f"  {path.name}: {malformed} linha(s) malformada(s) descartadas.", file=sys.stderr)
    return records


def _normalize_list(value) -> tuple:
    if value is None:
        return tuple()
    if isinstance(value, list):
        return tuple(sorted(str(v).strip().lower() for v in value))
    return (str(value).strip().lower(),)


def compare_case(case_id: str, outputs: dict[str, dict], strict_all: bool) -> dict:
    """outputs: {model_name: parsed_json_or_None}. Retorna um relatório.

    Um campo ausente (chave não presente no JSON de um modelo) é dado
    insuficiente, não um valor divergente — nunca é tratado como se o
    modelo tivesse respondido algo diferente dos outros. Um caso com
    qualquer campo comparável incompleto não pode ser certificado
    UNANIMOUS mesmo que os campos presentes concordem (ver EXP-013.md,
    achado sobre schema truncado do Gemini em LLM075-100).
    """
    missing = [m for m, v in outputs.items() if v is None]
    report = {"case_id": case_id, "missing_from": ";".join(missing)}

    if missing:
        report["status"] = "MISSING"
        report["diverging_fields"] = ";".join(missing and ["(caso ausente em pelo menos um modelo)"])
        report["incomplete_fields"] = ""
        return report

    diverging_fields = []
    incomplete_fields = []

    def present_values(field: str) -> dict | None:
        absent_from = [m for m, v in outputs.items() if field not in v]
        if absent_from:
            incomplete_fields.append(field)
            report[f"{field}__absent_from"] = ";".join(absent_from)
            return None
        return {m: v[field] for m, v in outputs.items()}

    for field in SCALAR_FIELDS:
        values = present_values(field)
        if values is None:
            continue
        if len(set(values.values())) > 1:
            diverging_fields.append(field)
            report[f"{field}__values"] = json.dumps(values, ensure_ascii=False)

    for field in CLOSED_LIST_FIELDS:
        values = present_values(field)
        if values is None:
            continue
        norm = {m: _normalize_list(v) for m, v in values.items()}
        if len(set(norm.values())) > 1:
            diverging_fields.append(field)
            report[f"{field}__values"] = json.dumps({m: list(v) for m, v in norm.items()}, ensure_ascii=False)

    open_diverging = []
    for field in OPEN_LIST_FIELDS:
        values = present_values(field)
        if values is None:
            continue
        norm = {m: _normalize_list(v) for m, v in values.items()}
        if len(set(norm.values())) > 1:
            open_diverging.append(field)
            report[f"{field}__values"] = json.dumps({m: list(v) for m, v in norm.items()}, ensure_ascii=False)
            if strict_all:
                diverging_fields.append(field)

    report["diverging_fields"] = ";".join(diverging_fields)
    report["diverging_open_vocab_fields_informational"] = ";".join(open_diverging)
    report["incomplete_fields"] = ";".join(incomplete_fields)

    if diverging_fields:
        report["status"] = "DISCORDANT"
    elif incomplete_fields:
        report["status"] = "INCOMPLETE"
    else:
        report["status"] = "UNANIMOUS"
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--gpt", required=True, type=Path)
    parser.add_argument("--claude", required=True, type=Path)
    parser.add_argument(
        "--gemini",
        type=Path,
        default=None,
        help="Opcional. Sem ele o agregador roda com DOIS avaliadores "
        "(re-teste do Codebook v2.4): nao ha regra de maioria, toda "
        "divergencia vai para adjudicacao humana, e a estatistica de "
        "concordancia aplicavel passa a ser Cohen's kappa, nao Fleiss'.",
    )
    parser.add_argument(
        "--strict-all",
        action="store_true",
        help="Leitura literal de D-026: divergência em campos de vocabulário livre "
        "(security_concerns, operational_capability) também conta como discordância. "
        "Default: esses campos são só informativos (ver docstring).",
    )
    parser.add_argument("--out-dir", type=Path, default=RESULTS_DIR)
    parser.add_argument(
        "--prefix",
        default="EXP-014",
        help="Prefixo dos arquivos de saida. O experimento que produziu as classificacoes, nao o que produziu a amostra.",
    )
    args = parser.parse_args()

    models = {"gpt": args.gpt, "claude": args.claude}
    if args.gemini is not None:
        models["gemini"] = args.gemini
    else:
        print(
            "Modo DOIS avaliadores (sem --gemini): sem regra de maioria, "
            "toda divergência vai a adjudicação humana. Use Cohen's kappa.",
            file=sys.stderr,
        )
    print("Carregando saídas...", file=sys.stderr)
    parsed = {name: load_jsonl(path) for name, path in models.items()}

    all_case_ids = sorted(set().union(*(set(d.keys()) for d in parsed.values())))
    print(f"{len(all_case_ids)} case_id distintos encontrados ao todo.", file=sys.stderr)

    reports = []
    for case_id in all_case_ids:
        outputs = {name: parsed[name].get(case_id) for name in models}
        reports.append(compare_case(case_id, outputs, strict_all=args.strict_all))

    n_unanimous = sum(1 for r in reports if r["status"] == "UNANIMOUS")
    n_discordant = sum(1 for r in reports if r["status"] == "DISCORDANT")
    n_incomplete = sum(1 for r in reports if r["status"] == "INCOMPLETE")
    n_missing = sum(1 for r in reports if r["status"] == "MISSING")

    args.out_dir.mkdir(exist_ok=True)

    # Consenso: casos unânimes, um rótulo por caso (dos três, todos iguais
    # nos campos comparados — usa a saída do primeiro modelo como registro,
    # já que são idênticas nos campos que importam).
    consensus_rows = []
    for r in reports:
        if r["status"] != "UNANIMOUS":
            continue
        case_id = r["case_id"]
        source = parsed["gpt"][case_id]  # equivalente às outras nos campos comparados
        row = {"case_id": case_id, "origin": "llm_consensus"}
        row.update({f: source.get(f) for f in ALL_COMPARABLE_FIELDS})
        for name in models:
            row[f"note_{name}"] = parsed[name][case_id].get("note")
        consensus_rows.append(row)

    discordant_rows = [r for r in reports if r["status"] in ("DISCORDANT", "INCOMPLETE", "MISSING")]

    # Trilha de auditoria completa — todo caso, incluindo divergências só
    # em campos de vocabulário livre que não decidiram o status (não
    # descartar essa informação: mostra o quanto os modelos concordam em
    # substância vs. em texto exato).
    with (args.out_dir / f"{args.prefix}_comparison_report.jsonl").open("w", encoding="utf-8") as f:
        for r in reports:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    with (args.out_dir / f"{args.prefix}_consensus_labels.jsonl").open("w", encoding="utf-8") as f:
        for row in consensus_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    with (args.out_dir / f"{args.prefix}_discordant_cases.jsonl").open("w", encoding="utf-8") as f:
        for row in discordant_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    summary = {
        "n_total": len(all_case_ids),
        "n_unanimous": n_unanimous,
        "n_discordant": n_discordant,
        "n_incomplete_from_some_model": n_incomplete,
        "n_missing_from_some_model": n_missing,
        "unanimous_rate": round(n_unanimous / len(all_case_ids), 3) if all_case_ids else None,
        "strict_all_open_vocab_fields": args.strict_all,
        "note": "n_discordant + n_incomplete + n_missing casos vao para adjudicacao humana "
        "(Guia do Anotador Humano), decidindo o caso inteiro, nao so o campo "
        "divergente (Decision Log D-026, mantido em D-027). confidence e "
        "rule_applied NAO decidem discordancia (D-027: metadados, kappa 0,070 "
        "e 0,36 no EXP-013). INCOMPLETE = pelo menos um "
        "campo comparavel ausente de pelo menos um modelo (dado insuficiente, "
        "nao tratado como divergencia de valor) mas os campos presentes nao "
        "divergiam entre si; nunca certificado UNANIMOUS so com dado parcial.",
    }
    (args.out_dir / f"{args.prefix}_aggregation_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(
        f"\nSaídas: {args.out_dir / f'{args.prefix}_consensus_labels.jsonl'} "
        f"(consenso) e {args.out_dir / f'{args.prefix}_discordant_cases.jsonl'} "
        f"(vão para adjudicação humana).",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
