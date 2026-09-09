"""EXP-013 (parte 3) — Aplica o filtro de "100% inglês" (Decision Log
D-025) à população inteira, não só à amostra de n=100.

Motivo de existir: o classificador final (E-7/E-8) vai rodar só sobre a
população restrita a inglês — então o mapeamento completo file_sha ->
is_purely_english precisa existir de qualquer forma, mais cedo ou mais
tarde. Rodar agora produz, de brinde, o denominador real da população
restrita a inglês (pergunta que estava em aberto desde D-025).

Mesma lógica de scripts/build_llm_ensemble_sample.py (detecção por
parágrafo, lingua, corrige a lacuna de escrita latina), aplicada às
1.877.981 linhas, não a uma amostra.

> [!success] JÁ RODADO ATÉ O FIM em 2026-09-03 — resultado em
> results/EXP-013_population_english_filter_summary.json e
> notes/Experiments/EXP-013.md. Rodar de novo (nesta ou noutra máquina)
> deve reproduzir os mesmos números (determinístico, sem seed aleatória) —
> útil para conferência, não é passo obrigatório do pipeline de novo.
> Números da execução original: 1.571.243/1.877.981 (83,667%) 100% em
> inglês; 306.738 (16,333%) rejeitados; 0 duplicatas.

Desempenho medido (16 núcleos lógicos, mesma máquina física) — LIDO NA
PRÁTICA, não só estimado, porque o job real foi interrompido três vezes:

  - Windows nativo (`uv run`, multiprocessing = spawn): ProcessPoolExecutor
    QUEBRA (BrokenProcessPool) — mesma falha já documentada em EXP-012
    para scipy/sklearn, agora confirmada também para lingua; não é
    peculiaridade de biblioteca, é o par spawn+uv nesta máquina.
    ThreadPoolExecutor funciona, ~1,3-1,8x (lingua libera o GIL só em
    parte) -> ~2,8h estimadas para a população inteira. Mais lento, mas
    foi o que terminou de forma confiável o restante da população
    quando o WSL parou de cooperar (ver abaixo).
  - WSL/Linux (`uv run`, multiprocessing = fork): ProcessPoolExecutor
    FUNCIONA e é bem mais rápido — fork clona o processo já carregado,
    não precisa reimportar nada. ~5,2x de aceleração medida (8-16
    processos, mesmo resultado) -> throughput real em torno de
    1.000-2.500 linhas/s dependendo do trecho da população.
    **Porém, na execução real, isso NÃO ficou "bem abaixo" de nenhum
    limite seguro:** o processo foi encerrado pelo próprio ambiente
    (SIGKILL, código de saída 137) depois de só ~40 min — mais cedo que
    o incidente de ~2h11min já documentado em EXP-012, não depois. Em
    seguida, duas tentativas de retomar quebraram o **serviço do WSL**
    (`Wsl/Service/E_UNEXPECTED`), inclusive em comandos triviais como
    `wc -l` — `wsl --shutdown` seguido de nova chamada recuperou o
    serviço as duas vezes. NÃO tratar o WSL como estável para uma
    execução única e longa nesta máquina — planejar para interrupção.

Retomável por desenho, e a forma de retomar importa: usar SQL (anti-join
contra o CSV de saída já escrito) para descobrir o que falta, em vez de
carregar um `set` Python com milhões de `file_sha` — mais leve, e foi o
que efetivamente terminou a cauda da população depois que a abordagem
com `set` em memória parou de progredir de forma confiável perto do fim
da execução original.

Uso (dentro do WSL/Linux, com o repositório acessível — em WSL, via
/mnt/c/...; numa máquina Linux "de verdade", direto):
    uv run --with duckdb --with pandas --with pyarrow \
        --with lingua-language-detector \
        python3 scripts/filter_population_english.py

Em Windows nativo, funciona também (mais lento, sem paralelismo real via
processo) — trocar ProcessPoolExecutor por ThreadPoolExecutor abaixo se
for essa a plataforma; foi assim que a cauda desta execução terminou.
"""

from __future__ import annotations

import csv
import re
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import duckdb

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
from build_llm_ensemble_sample import DATA_GLOB, DETECTOR_LANGUAGES, strip_non_prose  # noqa: E402
from lingua import LanguageDetectorBuilder  # noqa: E402

RESULTS_DIR = REPO_ROOT / "results"
OUT_PATH = RESULTS_DIR / "EXP-013_population_english_filter.csv"
OUT_FIELDS = ["file_sha", "is_purely_english", "n_non_english_paragraphs", "reason"]
BATCH_SIZE = 8000
N_WORKERS = 8  # 8 e 16 deram o mesmo throughput no benchmark — 8 evita
# concorrência desnecessária por I/O/memória sem perder velocidade.
MIN_PARAGRAPH_CHARS = 40
MIN_CONFIDENCE = 0.60
TOTAL_POPULATION_ESTIMATE = 1_877_981  # so para o ETA impresso; nao afeta o resultado

_detector = None  # global por processo-filho, montado uma vez pelo initializer


def _init_worker() -> None:
    global _detector
    _detector = LanguageDetectorBuilder.from_languages(*DETECTOR_LANGUAGES).build()


def classify_one(args: tuple[str, str, str]) -> dict:
    file_sha, description, content = args
    description = description if isinstance(description, str) else ""
    content = content if isinstance(content, str) else ""
    prose = strip_non_prose(description + "\n\n" + content).strip()
    if not prose:
        return {
            "file_sha": file_sha,
            "is_purely_english": False,
            "n_non_english_paragraphs": 0,
            "reason": "no_prose_after_stripping",
        }

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", prose) if p.strip()]
    n_non_english = 0
    top_language = ""
    for para in paragraphs:
        if len(para) < MIN_PARAGRAPH_CHARS:
            continue
        values = _detector.compute_language_confidence_values(para)
        top = values[0]
        if str(top.language) != "Language.ENGLISH" and top.value >= MIN_CONFIDENCE:
            n_non_english += 1
            if not top_language:
                top_language = str(top.language)

    return {
        "file_sha": file_sha,
        "is_purely_english": n_non_english == 0,
        "n_non_english_paragraphs": n_non_english,
        "reason": top_language,
    }


def main() -> None:
    RESULTS_DIR.mkdir(exist_ok=True)
    con = duckdb.connect()

    write_header = not OUT_PATH.exists()
    if OUT_PATH.exists():
        con.execute(f"CREATE TABLE done AS SELECT file_sha FROM read_csv('{OUT_PATH}')")
        n_done_start = con.execute("SELECT COUNT(*) FROM done").fetchone()[0]
    else:
        con.execute("CREATE TABLE done (file_sha VARCHAR)")
        n_done_start = 0
    print(f"{n_done_start} linhas já processadas (retomando via anti-join SQL).", file=sys.stderr)

    out_f = OUT_PATH.open("a", newline="", encoding="utf-8")
    writer = csv.DictWriter(out_f, fieldnames=OUT_FIELDS)
    if write_header:
        writer.writeheader()
        out_f.flush()

    # Anti-join no próprio DuckDB: só o que falta entra no stream. Não
    # carrega os já-feitos em memória Python — é isso que evita repetir
    # o problema visto na execução original perto do fim da população.
    reader = con.execute(
        f"""
        SELECT a.file_sha, a.description, a.content
        FROM read_parquet('{DATA_GLOB}') a
        LEFT JOIN done d ON a.file_sha = d.file_sha
        WHERE a.dedup_primary = 1 AND a.content IS NOT NULL AND d.file_sha IS NULL
        """
    ).to_arrow_reader(batch_size=BATCH_SIZE)

    t_start = time.time()
    n_processed_this_run = 0
    n_done_total = n_done_start

    with ProcessPoolExecutor(max_workers=N_WORKERS, initializer=_init_worker) as ex:
        for batch in reader:
            todo = [(r["file_sha"], r["description"], r["content"]) for r in batch.to_pylist()]

            for result in ex.map(classify_one, todo, chunksize=50):
                writer.writerow(result)
                n_processed_this_run += 1
                n_done_total += 1
            out_f.flush()

            elapsed = time.time() - t_start
            rate = n_processed_this_run / elapsed if elapsed > 0 else 0
            remaining = max(0, TOTAL_POPULATION_ESTIMATE - n_done_total)
            eta_str = f"{round(remaining / rate / 60)}min" if rate > 0 else "n/d"
            print(
                f"concluídas_total={n_done_total} "
                f"processadas_nesta_rodada={n_processed_this_run} "
                f"taxa={round(rate, 1)}/s eta≈{eta_str}",
                file=sys.stderr,
            )

    out_f.close()
    print(f"OK. Total processado: {n_done_total}. Saída: {OUT_PATH}", file=sys.stderr)


if __name__ == "__main__":
    main()
