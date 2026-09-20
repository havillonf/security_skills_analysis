"""
build_low_confidence_review.py — EXP-017
Monta o subconjunto de revisão humana para o EXP-017 (Q1-prompt-refinement).

Seleciona, entre os casos de CONSENSO de LLM no gold set (EXP-014), aqueles
em que pelo menos um modelo marcou confidence=low. Ordena: ambos low primeiro,
depois any-low, por case_id dentro de cada grupo.

Saída: results/EXP-017_low_confidence_review.csv

Colunas:
  case_id            — identificador do caso (LLMxxx)
  gold_label         — rótulo no gold set (PRIMARY/SECONDARY/NONE)
  is_security_skill  — true/false
  gpt_confidence     — high/medium/low
  claude_confidence  — high/medium/low
  both_low           — true se ambos marcaram low
  gpt_note           — justificativa do GPT
  claude_note        — justificativa do Claude
  gpt_evidence       — campos de evidência do GPT
  claude_evidence    — campos de evidência do Claude
  pattern_group      — grupo temático preliminar (ver EXP-017.md)
  fp_assessment      — [PREENCHER] correct | borderline | false_positive
  fp_reason          — [PREENCHER] justificativa em texto livre
  bring_to_victor    — [PREENCHER] true | false

Uso:
  python scripts/build_low_confidence_review.py

Não tem dependências externas além da stdlib.
"""

import csv
import json
from pathlib import Path

# ---------------------------------------------------------------------------
# Caminhos
# ---------------------------------------------------------------------------
ROOT = Path(__file__).parent.parent
GOLD_SET = ROOT / "results" / "EXP-014_gold_set.csv"
GPT_OUTPUT = ROOT / "results" / "EXP-014_gpt_output.jsonl"
CLAUDE_OUTPUT = ROOT / "results" / "EXP-014_claude_output.jsonl"
OUT_CSV = ROOT / "results" / "EXP-017_low_confidence_review.csv"


# ---------------------------------------------------------------------------
# Grupos temáticos (atribuídos manualmente a partir da análise das notes)
# Fonte: análise exploratória realizada na montagem do plano (2026-09-20)
# ---------------------------------------------------------------------------
PATTERN_GROUPS = {
    # restrição de comportamento de agente: read-only, escopo, ações destrutivas
    "LLM007": "restricao_de_agente",
    "LLM017": "restricao_de_agente",
    "LLM022": "restricao_de_agente",
    "LLM065": "restricao_de_agente",
    "LLM068": "restricao_de_agente",
    # consentimento antes de modificar (sem nomear ameaça)
    "LLM018": "consentimento_para_mudanca",
    "LLM037": "consentimento_para_mudanca",
    "LLM056": "consentimento_para_mudanca",
    "LLM100": "consentimento_para_mudanca",
    # gestão de chave/segredo (API key, SSH, secrets)
    "LLM014": "gestao_de_chave",
    "LLM055": "gestao_de_chave",
    "LLM057": "gestao_de_chave",
    # rate limiting sem nomear ameaça
    "LLM063": "rate_limit",
    # autenticação testada como um fluxo entre outros (não é o foco)
    "LLM001": "autenticacao_como_fluxo",
    "LLM077": "autenticacao_como_fluxo",
    "LLM097": "autenticacao_como_fluxo",
    # privacidade on-device enquadrada como controle de segurança
    "LLM050": "privacidade_on_device",
    # outros / não categorizados pela análise inicial
    "LLM012": "other",
    "LLM015": "other",   # NONE — incluído para controle
    "LLM030": "other",
    "LLM033": "other",
    "LLM081": "other",
    "LLM082": "other",
    "LLM092": "other",   # NONE truncated_undecidable — incluído para controle
}


def load_gold_set(path: Path) -> dict:
    with open(path, newline="", encoding="utf-8") as f:
        return {r["case_id"]: r for r in csv.DictReader(f)}


def load_jsonl(path: Path) -> dict:
    result = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                obj = json.loads(line)
                result[obj["case_id"]] = obj
    return result


def build_review_rows(gold: dict, gpt: dict, claude: dict) -> list[dict]:
    rows = []
    for case_id, g_row in gold.items():
        # Só casos de consenso LLM
        if g_row.get("label_origin") != "llm_consensus":
            continue

        g = gpt.get(case_id, {})
        c = claude.get(case_id, {})
        g_conf = g.get("confidence", "")
        c_conf = c.get("confidence", "")

        # Filtro: pelo menos um low
        if g_conf != "low" and c_conf != "low":
            continue

        both_low = g_conf == "low" and c_conf == "low"
        gold_label = g_row["security_relevance"]

        rows.append({
            "case_id": case_id,
            "gold_label": gold_label,
            "is_security_skill": g_row.get("is_security_skill", ""),
            "gpt_confidence": g_conf,
            "claude_confidence": c_conf,
            "both_low": str(both_low).lower(),
            "gpt_note": g.get("note", ""),
            "claude_note": c.get("note", ""),
            "gpt_evidence": ";".join(g.get("evidence", [])),
            "claude_evidence": ";".join(c.get("evidence", [])),
            "pattern_group": PATTERN_GROUPS.get(case_id, "unknown"),
            # --- campos a preencher manualmente ---
            "fp_assessment": "",   # correct | borderline | false_positive
            "fp_reason": "",       # justificativa em texto livre
            "bring_to_victor": "", # true | false
        })

    # Ordenação: both-low primeiro, depois any-low; dentro de cada grupo por case_id
    rows.sort(key=lambda r: (0 if r["both_low"] == "true" else 1, r["case_id"]))
    return rows


FIELDNAMES = [
    "case_id", "gold_label", "is_security_skill",
    "gpt_confidence", "claude_confidence", "both_low",
    "gpt_note", "claude_note", "gpt_evidence", "claude_evidence",
    "pattern_group",
    "fp_assessment", "fp_reason", "bring_to_victor",
]


def main() -> None:
    gold = load_gold_set(GOLD_SET)
    gpt = load_jsonl(GPT_OUTPUT)
    claude = load_jsonl(CLAUDE_OUTPUT)

    rows = build_review_rows(gold, gpt, claude)

    both_low_count = sum(1 for r in rows if r["both_low"] == "true")
    any_low_count = len(rows)

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    print(f"EXP-017 — subconjunto de revisão gerado: {OUT_CSV}")
    print(f"  Total de casos: {any_low_count}")
    print(f"  Both-low (alta prioridade): {both_low_count}")
    print(f"  Any-low (prioridade normal): {any_low_count - both_low_count}")
    print()
    print("Próximo passo: abrir o CSV e preencher fp_assessment / fp_reason / bring_to_victor")
    print("  - Comece pelos casos com both_low=true")
    print("  - Para cada caso, leia o SKILL.md em results/EXP-013_llm_cases/LLMxxx.md")


if __name__ == "__main__":
    main()

