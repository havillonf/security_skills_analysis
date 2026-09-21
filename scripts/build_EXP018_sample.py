"""EXP-018 — Amostra para o ensemble de 3 LLMs (E-5/E-6, Decision Log D-026).

Sorteia n=100 skills sobre a população restrita a inglês (Decision Log
D-025), com verificação de pureza de idioma por SEGMENTO de prosa (não só
por contagem de caracteres não latinos) — corrige a lacuna registrada em
D-025: o limiar antigo, emprestado de R-9, nunca capturaria uma frase em
italiano/portugues/espanhol embutida num texto majoritariamente ingles,
porque exige caracteres nao latinos. Aqui, qualquer segmento de prosa
suficientemente longo detectado como nao-ingles reprova o caso inteiro —
a skill sai da populacao, nao fica com uma flag.

Amostragem determinística (ORDER BY hash(file_sha || 'EXP-018')), sem seed externa,
reproduzível em qualquer máquina — mesma convenção do restante do
projeto (ver Decision Log D-005 nota tecnica).

Populacao de partida: dedup_primary = 1 AND content IS NOT NULL. Este e o
frame "status quo" (alternativa (a) de D-022, EM ABERTO) — D-022 nao foi
resolvida por este script; se for resolvida depois, esta amostra pode
precisar ser regerada.

Uso:
    uv run --with duckdb --with pandas --with lingua-language-detector \
        python scripts/build_llm_ensemble_sample.py
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
CASES_DIR = RESULTS_DIR / "EXP-018_llm_cases"

N_TARGET = 100
# Tamanho inicial do lote de candidatos e o passo de expansao caso o lote
# nao renda 100 casos aprovados. Determinismo preservado: sempre a mesma
# ordem (hash(file_sha)), so aumenta quantos itens dessa ordem sao lidos.
INITIAL_BATCH = 400
BATCH_STEP = 400
MAX_BATCH = 4000

# Paragrafo precisa ter pelo menos este numero de caracteres para entrar
# na checagem de idioma (evita falso positivo em fragmentos curtos - um
# acronimo, um titulo, um item de lista de uma linha).
MIN_PARAGRAPH_CHARS = 40

# Confianca minima exigida para o veredito de idioma de um paragrafo
# valer como evidencia de "nao ingles". Abaixo disso, o paragrafo e
# ambiguo demais para reprovar o caso sozinho.
MIN_CONFIDENCE = 0.60

# Linguas incluidas no detector: as que ja apareceram medidas no dataset
# (Multilingual Strategy Sec.3) mais o ingles. Restringir a lista (em vez
# de from_all_languages()) e mais rapido e nao perde cobertura conhecida.
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
    """Remove front matter, code, URLs e caminhos antes de detectar idioma.

    Mesmo pre-processamento descrito em Multilingual Strategy Sec.2 -
    texto cru enganaria o detector (codigo e "ingles" por natureza da
    sintaxe, independente do idioma da prosa ao redor).
    """
    text = FRONTMATTER_RE.sub("", text, count=1)
    text = CODE_FENCE_RE.sub(" ", text)
    text = INLINE_CODE_RE.sub(" ", text)
    text = URL_RE.sub(" ", text)
    text = PATH_RE.sub(" ", text)
    return text


def is_purely_english(detector, prose: str) -> tuple[bool, list[dict]]:
    """Retorna (aprovado, evidencia).

    Detecta idioma por PARÁGRAFO (não pelo algoritmo automático de
    segmentação de `detect_multiple_languages_of`, que se mostrou instável
    em texto técnico ruidoso — muitos falsos positivos em tabelas, listas
    e trechos curtos, tornando o filtro impraticavelmente restritivo).
    Aprovado = nenhum parágrafo suficientemente longo tem confiança >=
    MIN_CONFIDENCE para uma língua diferente de inglês.
    """
    prose = prose.strip()
    if not prose:
        # Sem prosa para avaliar (so codigo/frontmatter) - nao ha como
        # confirmar idioma; tratado como reprovado por cautela, nao
        # aprovado por ausencia de evidencia.
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
    CASES_DIR.mkdir(exist_ok=True)

    print("Carregando detector de idioma (lingua)...", file=sys.stderr)
    detector = LanguageDetectorBuilder.from_languages(*DETECTOR_LANGUAGES).build()

    con = duckdb.connect()

    accepted_rows = []
    rejected_rows = []
    seen_shas: set[str] = set()
    content_by_sha: dict[str, str] = {}

    batch_size = INITIAL_BATCH
    while len(accepted_rows) < N_TARGET and batch_size <= MAX_BATCH:
        print(f"Lendo os {batch_size} primeiros candidatos por hash(file_sha)...", file=sys.stderr)
        query = f"""
            SELECT file_sha, name, description, content
            FROM read_parquet('{DATA_GLOB}')
            WHERE dedup_primary = 1 AND content IS NOT NULL
            ORDER BY hash(file_sha || 'EXP-018')
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

            name = row["name"] if isinstance(row["name"], str) else ""
            description = row["description"] if isinstance(row["description"], str) else ""
            content = row["content"] if isinstance(row["content"], str) else ""

            prose = strip_non_prose((description or "") + "\n\n" + (content or ""))
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
                record["rejection_evidence"] = json.dumps(evidence, ensure_ascii=False)
                rejected_rows.append(record)

            if len(accepted_rows) >= N_TARGET:
                break

        if len(accepted_rows) < N_TARGET:
            print(
                f"Só {len(accepted_rows)} casos aprovados em {batch_size} candidatos; "
                f"expandindo o lote.",
                file=sys.stderr,
            )
            batch_size += BATCH_STEP

    if len(accepted_rows) < N_TARGET:
        raise RuntimeError(
            f"Não foi possível reunir {N_TARGET} casos 100% em inglês mesmo "
            f"com {batch_size} candidatos (MAX_BATCH={MAX_BATCH}). Revisar "
            f"limiares ou aumentar MAX_BATCH."
        )

    accepted_rows = accepted_rows[:N_TARGET]

    # case_id determinístico pela mesma ordem (não pelo sorteio do dict)
    for i, row in enumerate(accepted_rows, start=1):
        row["case_id"] = f"LLM{i:03d}"

    accepted_df = pd.DataFrame(accepted_rows)
    rejected_df = pd.DataFrame(rejected_rows)

    # --- Saídas ---
    # 1) Amostra final (metadados, sem conteúdo bruto — reprodutível a
    #    partir do file_sha) — versionável.
    accepted_out = accepted_df[["case_id", "file_sha", "name", "body_chars"]]
    accepted_out.to_csv(RESULTS_DIR / "EXP-018_llm_sample.csv", index=False)

    # 2) Log de rejeições — quantos candidatos foram descartados por
    #    conterem prosa não inglesa, e onde. Dado relevante para o TCC
    #    (mostra a seletividade real do filtro de D-025).
    if not rejected_df.empty:
        rejected_out = rejected_df[["file_sha", "name", "body_chars", "rejection_evidence"]]
        rejected_out.to_csv(RESULTS_DIR / "EXP-018_llm_sample_rejected.csv", index=False)

    # 3) Arquivos por caso, cegos (só name/description/body — nada de
    #    file_sha, repositório, tier ou motivo de seleção), para consumo
    #    direto por CLIs de agente com acesso ao diretório (ver
    #    Classification Prompt (D-026)). Um arquivo por modelo/rodada não
    #    é necessário — os três CLIs leem o mesmo diretório, cada um a
    #    partir de uma invocação separada e sem visibilidade da saída dos
    #    outros (blindagem por processo, não por conteúdo do arquivo).
    for row in accepted_rows:
        case_path = CASES_DIR / f"{row['case_id']}.md"
        case_path.write_text(
            f"case_id: {row['case_id']}\n"
            f"name: {row['name']}\n"
            f"description: {row['description']}\n"
            f"---\n\n"
            f"{content_by_sha[row['file_sha']]}\n",
            encoding="utf-8",
        )

    # 4) Sumário
    summary = {
        "n_target": N_TARGET,
        "n_accepted": len(accepted_rows),
        "n_rejected_for_language": len(rejected_rows),
        "final_batch_size": batch_size,
        "population_frame": "dedup_primary = 1 AND content IS NOT NULL (status quo, D-022 EM ABERTO)",
        "language_filter": "lingua, por paragrafo (>= "
        f"{MIN_PARAGRAPH_CHARS} caracteres, confianca >= {MIN_CONFIDENCE}), "
        "corrige a lacuna de escrita latina registrada em Decision Log D-025",
        "caveat": "amostra aleatória simples, NÃO estratificada por sinal "
        "preliminar (Decision Log D-026) — pode conter poucos casos na "
        "fronteira SECONDARY/MENTION",
    }
    (RESULTS_DIR / "EXP-018_llm_sample_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"OK: {len(accepted_rows)} casos aceitos, {len(rejected_rows)} rejeitados por idioma.", file=sys.stderr)
    print(f"Casos em: {CASES_DIR}", file=sys.stderr)


if __name__ == "__main__":
    main()
