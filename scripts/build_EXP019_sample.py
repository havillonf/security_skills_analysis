"""EXP-019 — Geração da Amostra Estatística para Anotação Manual (D-036, D-037).

Gera uma fila ordenada de candidatos (n_target=600) extraídos determinística
e reprodutivelmente da População Elegível (100% em inglês, dedup_primary=1,
tamanho >= 200 caracteres), sob o salt 'EXP-019'.

A fila de 600 casos garante margem suficiente para que os anotadores humanos
descartem itens que não sejam de desenvolvimento de software (Estágio 1 = false)
e completem a cota exata de 385 casos de SDLC (Estágio 1 = true), conforme D-037.

Gera também:
1. Arquivos individuais cegos em results/EXP-019_cases/CASE###.md
2. Planilhas de anotação independentes para Havillon e Victor
3. Relatório de rejeições (tamanho e idioma)
4. Sumário estatístico JSON

Uso:
    .venv/bin/python scripts/build_EXP019_sample.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import duckdb
import pandas as pd
from lingua import Language, LanguageDetectorBuilder

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_GLOB = str(REPO_ROOT / "data" / "artifacts.parquet")
RESULTS_DIR = REPO_ROOT / "results"
EXP_DIR = RESULTS_DIR / "EXP-019_cases"

# Tamanho do buffer da fila: 600 casos para garantir que cheguemos a 385 SDLC
N_TARGET = 600
INITIAL_BATCH = 1200
BATCH_STEP = 600
MAX_BATCH = 6000

# Limiares do Codebook v3.1 e D-025
MIN_TOTAL_CHARS = 200
MIN_PARAGRAPH_CHARS = 40
MIN_CONFIDENCE = 0.60

DETECTOR_LANGUAGES = [
    Language.ENGLISH, Language.CHINESE, Language.JAPANESE, Language.KOREAN,
    Language.GERMAN, Language.SPANISH, Language.PORTUGUESE, Language.FRENCH,
    Language.ITALIAN, Language.RUSSIAN, Language.VIETNAMESE, Language.TURKISH,
    Language.ARABIC, Language.DUTCH, Language.POLISH, Language.SWEDISH,
    Language.INDONESIAN, Language.HINDI, Language.THAI, Language.GREEK,
]

CODE_FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")
FRONTMATTER_RE = re.compile(r"^---\s*\n.*?\n---\s*\n", re.DOTALL)
URL_RE = re.compile(r"https?://\S+")
PATH_RE = re.compile(r"(?:[\w.-]+/)+[\w.-]+\.\w+")


def strip_non_prose(text: str) -> str:
    text = FRONTMATTER_RE.sub("", text, count=1)
    text = CODE_FENCE_RE.sub(" ", text)
    text = INLINE_CODE_RE.sub(" ", text)
    text = URL_RE.sub(" ", text)
    text = PATH_RE.sub(" ", text)
    return text


def is_purely_english(detector, prose: str) -> tuple[bool, list[dict]]:
    prose = prose.strip()
    if not prose:
        return False, [{"reason": "no_prose_after_stripping"}]

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", prose) if p.strip()]
    non_english_paragraphs = []
    for para in paragraphs:
        if len(para) < MIN_PARAGRAPH_CHARS:
            continue
        values = detector.compute_language_confidence_values(para)
        top = values[0]
        if top.language != Language.ENGLISH and top.value >= MIN_CONFIDENCE:
            non_english_paragraphs.append(
                {
                    "language": str(top.language),
                    "confidence": round(top.value, 3),
                    "length": len(para),
                    "preview": para[:120],
                }
            )
    return (len(non_english_paragraphs) == 0), non_english_paragraphs


def main() -> None:
    RESULTS_DIR.mkdir(exist_ok=True)
    EXP_DIR.mkdir(exist_ok=True)

    print("Carregando detector de idioma (lingua)...", file=sys.stderr)
    detector = LanguageDetectorBuilder.from_languages(*DETECTOR_LANGUAGES).build()

    con = duckdb.connect()

    accepted_rows = []
    rejected_rows = []
    seen_shas: set[str] = set()
    content_by_sha: dict[str, str] = {}

    batch_size = INITIAL_BATCH
    while len(accepted_rows) < N_TARGET and batch_size <= MAX_BATCH:
        print(f"Lendo lote de {batch_size} candidatos com salt 'EXP-019'...", file=sys.stderr)
        query = f"""
            SELECT file_sha, name, description, content
            FROM read_parquet('{DATA_GLOB}')
            WHERE dedup_primary = 1 AND content IS NOT NULL
            ORDER BY hash(file_sha || 'EXP-019')
            LIMIT {batch_size}
        """
        df = con.execute(query).fetchdf()

        accepted_rows.clear()
        rejected_rows.clear()
        seen_shas.clear()
        content_by_sha.clear()

        for _, row in df.iterrows():
            file_sha = row["file_sha"]
            if file_sha in seen_shas:
                continue
            seen_shas.add(file_sha)

            name = str(row["name"]) if pd.notna(row["name"]) else ""
            description = str(row["description"]) if pd.notna(row["description"]) else ""
            content = str(row["content"]) if pd.notna(row["content"]) else ""

            total_chars = len(description) + len(content)

            # Filtro 1: Tamanho mínimo (Codebook v3.1)
            if total_chars < MIN_TOTAL_CHARS:
                rejected_rows.append({
                    "file_sha": file_sha,
                    "name": name,
                    "reason": "too_short",
                    "total_chars": total_chars,
                    "rejection_evidence": f"Tamanho combinado ({total_chars} chars) < {MIN_TOTAL_CHARS}",
                })
                continue

            # Filtro 2: Idioma estritamente inglês (D-025)
            prose = strip_non_prose(f"{description}\n\n{content}")
            ok, evidence = is_purely_english(detector, prose)

            record = {
                "file_sha": file_sha,
                "name": name,
                "description": description,
                "body_chars": len(content),
            }

            if ok:
                accepted_rows.append(record)
                content_by_sha[file_sha] = content
            else:
                record["reason"] = "non_english"
                record["total_chars"] = total_chars
                record["rejection_evidence"] = json.dumps(evidence, ensure_ascii=False)
                rejected_rows.append(record)

            if len(accepted_rows) >= N_TARGET:
                break

        if len(accepted_rows) < N_TARGET:
            print(
                f"Obtidos {len(accepted_rows)}/{N_TARGET} casos aprovados no lote de {batch_size}. Expandindo lote...",
                file=sys.stderr,
            )
            batch_size += BATCH_STEP

    if len(accepted_rows) < N_TARGET:
        raise RuntimeError(f"Não foi possível reunir {N_TARGET} casos elegíveis mesmo com batch={batch_size}.")

    accepted_rows = accepted_rows[:N_TARGET]

    # Atribuir case_id sequencial
    for i, row in enumerate(accepted_rows, start=1):
        row["case_id"] = f"CASE{i:03d}"

    accepted_df = pd.DataFrame(accepted_rows)
    rejected_df = pd.DataFrame(rejected_rows)

    # 1) Amostra elegível (metadados)
    sample_csv = RESULTS_DIR / "EXP-019_sample.csv"
    accepted_df[["case_id", "file_sha", "name", "body_chars"]].to_csv(sample_csv, index=False)

    # 2) Log de rejeições
    rejected_csv = RESULTS_DIR / "EXP-019_rejected.csv"
    rejected_df.to_csv(rejected_csv, index=False)

    # 3) Casos cegos individuais em Markdown
    print(f"Escrevendo {len(accepted_rows)} arquivos de casos em {EXP_DIR}...", file=sys.stderr)
    for row in accepted_rows:
        case_file = EXP_DIR / f"{row['case_id']}.md"
        case_file.write_text(
            f"case_id: {row['case_id']}\n"
            f"name: {row['name']}\n"
            f"description: {row['description']}\n"
            f"---\n\n"
            f"{content_by_sha[row['file_sha']]}\n",
            encoding="utf-8",
        )

    # 4) Planilhas de anotação cega para os dois pesquisadores (Codebook v3.1)
    annotation_columns = [
        "case_id",
        "name",
        "body_chars",
        "is_software_development",  # true | false
        "has_security",             # true | false | (vazio se não-SDLC)
        "evidence",                 # description | body | bundled_artifacts
        "confidence",               # high | medium | low
        "note",                     # (1) o que faz; (2) por que é/não é SDLC; (3) conteúdo de segurança
    ]

    for annotator in ["havillon", "victor"]:
        form_df = pd.DataFrame({col: accepted_df[col] if col in accepted_df.columns else "" for col in annotation_columns})
        form_path = RESULTS_DIR / f"EXP-019_annotation_form_{annotator}.csv"
        form_df.to_csv(form_path, index=False)

    # 5) Sumário JSON
    summary = {
        "experiment": "EXP-019",
        "n_target_buffer": N_TARGET,
        "n_accepted_eligible": len(accepted_rows),
        "n_rejected_total": len(rejected_rows),
        "n_rejected_too_short": sum(1 for r in rejected_rows if r.get("reason") == "too_short"),
        "n_rejected_language": sum(1 for r in rejected_rows if r.get("reason") == "non_english"),
        "batch_size_needed": batch_size,
        "quota_target_sdlc": 385,
        "calibration_cases": "Primeiros 20 a 40 casos (CASE001 a CASE040)",
        "protocol": "Anotar ordenadamente a partir de CASE001. Se is_software_development=false, descartar e seguir para o próximo até acumular 385 casos com is_software_development=true.",
    }
    (RESULTS_DIR / "EXP-019_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print("OK! Amostra gerada com sucesso:", file=sys.stderr)
    print(f"- Casos aceitos na fila: {len(accepted_rows)}", file=sys.stderr)
    print(f"- Casos rejeitados (tamanho ou idioma): {len(rejected_rows)}", file=sys.stderr)
    print(f"- Diretório de casos: {EXP_DIR}", file=sys.stderr)
    print(f"- Formulário Havillon: {RESULTS_DIR}/EXP-019_annotation_form_havillon.csv", file=sys.stderr)
    print(f"- Formulário Victor: {RESULTS_DIR}/EXP-019_annotation_form_victor.csv", file=sys.stderr)


if __name__ == "__main__":
    main()

