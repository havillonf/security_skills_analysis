"""EXP-015 - Perfil de artefatos gerados dentro do quadro amostral.

Pergunta: quantos `SKILL.md` da populacao NAO sao arquivos de instrucao, e sim
saidas geradas (relatorios, dumps de pesquisa, documentos de contexto) que
foram salvas com esse nome?

Motivacao empirica: na amostra do EXP-013 (100 casos), LLM019 e um despejo de
resultados de pesquisa e LLM067 e um "Feature Context" gerado por workflow.
Nenhum dos dois e instrucao para um agente. O limiar de tamanho do D-028 nao
os alcanca (15.744 e 19.445 caracteres) porque ele exclui evidencia DE MENOS,
nao genero errado.

O que este script NAO faz: nao decide o quadro amostral. Ele mede o tamanho de
cada estrato e a cobertura de uma regra candidata, para que a decisao (que e do
pesquisador, e exige entrada no Decision Log) seja tomada com numero na mao.

Uso:
    uv run --with duckdb python scripts/profile_frame_artifacts.py

Saida:
    results/EXP-015_frame_artifact_profile.json   (agregados, versionado)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"
ARTIFACTS = "read_parquet('data/raw/gitskills/data/artifacts/*.parquet')"

# Janela do inicio do arquivo. Metadado de procedencia, quando existe, aparece
# no topo; varrer o conteudo inteiro custa mais e traz falso positivo de
# template (uma skill que ENSINA a gerar relatorio contem "Generated:" no meio).
HEAD_CHARS = 2500

# Marcadores de procedencia: o documento se descreve como tendo sido produzido.
# `replace` remove `*` e `#` antes do LIKE porque `**Generated**:` nao casa com
# '%generated:%' - foi assim que a primeira versao desta regra perdeu o LLM067.
PROVENANCE_MARKERS = [
    "generated:",
    "generated on ",
    "date range:",
    "input type:",
    "document metadata",
    "report generated",
    "analysis date",
]

# Marcadores de instrucao: o documento se dirige a um executor.
INSTRUCTION_MARKERS = [
    "when to use",
    "you should",
    "use this skill",
]

# Os dois nao-skills confirmados por leitura na amostra do EXP-013.
KNOWN_NON_SKILLS = {
    "a6d95f211f9307e10848664b636e6017dabd442d": "LLM019",
    "51554c7067a59f5cd39d11debd312a2f9c96d77c": "LLM067",
}
# Os doze da mesma amostra com `name` nulo que a leitura confirmou serem skills
# legitimas (front matter fora da spec, conteudo instrucional).
KNOWN_SKILLS_NAME_NULL = {
    "3382e8d55b6627021088e13db0ade57d8321355c": "LLM002",
    "341fb32d8d475abde39f7f1c29c0110a379070bd": "LLM004",
    "0a6450c4851a32f99f162b178f17a35161418a5f": "LLM008",
    "473b7b775c84ef4e913d2f394ae576c52379bc6c": "LLM021",
    "42f315174d0b6bb3be7d7280b13122889a3a1ddc": "LLM028",
    "cf076d64df1e0415729c54b76aba42c9b5557cc5": "LLM048",
    "1d5b3334b8c0abccd238370fd8eea1cac409eda7": "LLM057",
    "8e7408e2297decb787a5d9964f4e159f96811043": "LLM060",
    "fba0c3f3192cd5bd854286fcd318da428ed0096a": "LLM073",
    "f4920e8935f39d470ef7d2606ebcb75aab4ece56": "LLM078",
    "c8ffe506809ba8b5615906820a72a1aa848d7e31": "LLM079",
    "e37e8c49420234daa4788ab73b6a19d5960ccac2": "LLM084",
}


def _or_like(column: str, markers: list[str]) -> str:
    return " OR ".join(f"{column} LIKE '%{m}%'" for m in markers)


def main() -> None:
    started = time.time()
    con = duckdb.connect()
    con.execute("SET enable_progress_bar=false")

    head_expr = (
        f"lower(replace(replace(substr(content, 1, {HEAD_CHARS}), '*', ''), '#', ''))"
    )
    base = f"""
        SELECT
            file_sha,
            frontmatter_valid,
            name,
            body_chars,
            ({_or_like('head', PROVENANCE_MARKERS)}) AS provenance,
            ({_or_like('head', INSTRUCTION_MARKERS)}) AS instruction
        FROM (
            SELECT file_sha, frontmatter_valid, name, body_chars, {head_expr} AS head
            FROM {ARTIFACTS}
            WHERE dedup_primary = 1 AND content IS NOT NULL
        )
    """

    strata = con.execute(f"""
        SELECT frontmatter_valid, provenance, instruction, count(*) AS n
        FROM ({base}) GROUP BY 1, 2, 3 ORDER BY 1, 2, 3
    """).fetchall()
    total = sum(r[3] for r in strata)

    totals = con.execute(f"""
        SELECT
            count(*) AS n_population,
            count(*) FILTER (WHERE frontmatter_valid = 1)  AS n_frontmatter_valid,
            count(*) FILTER (WHERE name IS NULL)           AS n_name_null,
            count(*) FILTER (WHERE provenance)             AS n_provenance,
            count(*) FILTER (WHERE frontmatter_valid = 0 AND provenance)
                AS n_rule_candidate
        FROM ({base})
    """).fetchone()

    known = list(KNOWN_NON_SKILLS) + list(KNOWN_SKILLS_NAME_NULL)
    quoted = ", ".join(f"'{s}'" for s in known)
    checks = con.execute(f"""
        SELECT file_sha, frontmatter_valid, provenance, instruction
        FROM ({base}) WHERE file_sha IN ({quoted})
    """).fetchall()

    validation = []
    for sha, fm_valid, provenance, instruction in checks:
        truth = "not_a_skill" if sha in KNOWN_NON_SKILLS else "skill"
        label = KNOWN_NON_SKILLS.get(sha) or KNOWN_SKILLS_NAME_NULL[sha]
        flagged = bool(fm_valid == 0 and provenance)
        validation.append({
            "case_id": label,
            "file_sha": sha,
            "ground_truth": truth,
            "frontmatter_valid": int(fm_valid),
            "provenance": bool(provenance),
            "instruction": bool(instruction),
            "flagged_by_rule": flagged,
            "correct": flagged == (truth == "not_a_skill"),
        })
    validation.sort(key=lambda v: v["case_id"])

    tp = sum(v["flagged_by_rule"] and v["ground_truth"] == "not_a_skill" for v in validation)
    fp = sum(v["flagged_by_rule"] and v["ground_truth"] == "skill" for v in validation)
    fn = sum(not v["flagged_by_rule"] and v["ground_truth"] == "not_a_skill" for v in validation)

    payload = {
        "experiment": "EXP-015",
        "question": (
            "Quantos SKILL.md da populacao sao saidas geradas em vez de arquivos "
            "de instrucao, e uma regra em escala populacional consegue separa-los?"
        ),
        "population_frame": "dedup_primary = 1 AND content IS NOT NULL",
        "duckdb_version": duckdb.__version__,
        "head_chars": HEAD_CHARS,
        "provenance_markers": PROVENANCE_MARKERS,
        "instruction_markers": INSTRUCTION_MARKERS,
        "totals": {
            "n_population": totals[0],
            "n_frontmatter_valid": totals[1],
            "n_name_null": totals[2],
            "n_provenance": totals[3],
            "n_rule_candidate": totals[4],
            "pct_rule_candidate": round(100 * totals[4] / totals[0], 4),
        },
        "strata": [
            {
                "frontmatter_valid": r[0],
                "provenance": bool(r[1]),
                "instruction": bool(r[2]),
                "n": r[3],
                "pct": round(100 * r[3] / total, 4),
            }
            for r in strata
        ],
        "rule": "frontmatter_valid = 0 AND provenance",
        "validation_on_known_cases": {
            "n": len(validation),
            "true_positives": tp,
            "false_positives": fp,
            "false_negatives": fn,
            "caveat": (
                "n=14, todos do subgrupo `name` nulo da amostra do EXP-013, "
                "rotulados por leitura do pesquisador-assistente e NAO adjudicados. "
                "Precisao e recall aqui sao ilustrativos, nao estimativas."
            ),
            "cases": validation,
        },
        "elapsed_seconds": round(time.time() - started, 1),
    }

    RESULTS_DIR.mkdir(exist_ok=True)
    out = RESULTS_DIR / "EXP-015_frame_artifact_profile.json"
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"populacao                       {totals[0]:>10,}")
    print(f"front matter valido             {totals[1]:>10,}  ({100*totals[1]/totals[0]:.2f}%)")
    print(f"marcador de procedencia         {totals[3]:>10,}  ({100*totals[3]/totals[0]:.3f}%)")
    print(f"regra (fm=0 E procedencia)      {totals[4]:>10,}  ({100*totals[4]/totals[0]:.3f}%)")
    print(f"\nvalidacao em {len(validation)} casos conhecidos: "
          f"TP={tp} FP={fp} FN={fn}")
    print(f"\nOK -> results/{out.name}  [{payload['elapsed_seconds']}s]")


if __name__ == "__main__":
    main()
