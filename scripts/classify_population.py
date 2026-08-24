#!/usr/bin/env python3
"""
EXP-012 - Classificacao em escala dos 1.877.981 conteudos distintos com o
classificador v1 IMPLANTADO (models/security_classifier_v1_{multiclass,binary}.joblib).

RESULTADO PRELIMINAR DO CLASSIFICADOR, NAO ESTIMATIVA ESTATISTICA FINAL.
O modelo foi treinado/validado num golden set de n=49 (EXP-005, LLM-assisted).
Os N_h corretos para o estimador do Desenho C ([[Decision Log#D-014]]) so
existem depois de um gold set humano maior (E-6). Este script produz o
"N_h de proxy" da iteracao v1 - insumo de engenharia para provar o pipeline
end-to-end, nao um resultado cientifico.

`language_group` aqui e um PROXY BARATO por script Unicode (heuristica SQL
sobre a populacao inteira), NAO o detector validado de EXP-003/EXP-004
(lingua/py3langid) - esse rodaria a horas de distancia em 1,88M documentos
sem trazer beneficio para a inferencia do classificador (que nao usa idioma
como feature). Serve so para o corte descritivo do resultado por idioma.

VERSAO 2 - OTIMIZADA (ver Decision Log D-023, secao "estimativa inicial
incorreta"). A v1 deste script rodou ~2h11min antes de ser encerrada pelo
ambiente sem concluir; a extrapolacao correta a partir do throughput medido
era ~9,3h. Causa identificada por profiling isolado (nao especulacao): a
classificacao em si e rapida (calibrated predict_proba leva ~0,2s para
20.000 linhas); o gargalo e a VETORIZACAO TF-IDF por n-gramas de caractere
sobre o comprimento medio real da populacao (~7.247 caracteres, MUITO maior
que os textos curtos usados no benchmark inicial que gerou a estimativa
errada de 15-16 min) - e essa vetorizacao rodava DUAS VEZES (uma por
pipeline, multiclasse e binario).

Uma tentativa de paralelizar com ProcessPoolExecutor falhou nesta maquina
(Windows + uv: falha ao importar scipy/sklearn nos processos-filho via
spawn - nao investigada a fundo, custo/beneficio nao compensou dado o ganho
ja obtido pela otimizacao abaixo). Este script permanece single-process.

Duas otimizacoes aplicadas, nenhuma exige retreino do modelo:
  1. os dois pipelines foram fit no MESMO corpus com os MESMOS hiperparametros
     -> `vocabulary_` e `idf_` sao identicos (verificado por igualdade exata,
     nao suposicao) -> vetoriza-se UMA vez por lote e reaproveita-se a matriz
     esparsa para os dois classificadores, cortando o custo de vetorizacao
     pela metade;
  2. o texto e truncado a TRUNC_CHARS caracteres ANTES de vetorizar - reduz
     linearmente o custo por documento sem alterar o modelo treinado (so
     limita o que a inferencia em escala "le", como um truncamento de
     contexto) - efeito medido, nao estimado: ver benchmark no Decision Log.

Inferencia em lote (sem chamada de LLM por item). Modelo implantado e
TF-IDF + LinearSVC calibrado (Platt scaling) - ver Decision Log
(classificador definitivo v1) para a justificativa da escolha por
viabilidade computacional sobre o candidato de melhor CV (embeddings).

Saidas:
  results/EXP-012_population_classification.parquet (gitignored - grande,
      mas contem so file_sha/predicoes, nao texto de terceiros; regeneravel)
  results/EXP-012_population_summary.json (agregados, versionado)
  results/EXP-012_uncertain_cases_sample.csv (amostra de casos de baixa
      confianca na fronteira SECONDARY<->MENTION e SECURITY<->NON_SECURITY;
      so metadados, sem corpo do texto - versionado)

Uso:
    uv run --with duckdb --with pyarrow --with pandas --with scikit-learn \
        --with joblib python scripts/classify_population.py
"""

import argparse
import json
import sys
import time
from pathlib import Path

import duckdb
import joblib
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "raw" / "gitskills" / "data"
RESULTS_DIR = ROOT / "results"
MODELS_DIR = ROOT / "models"
BATCH_SIZE = 20000
TRUNC_CHARS = 1500  # ver nota "VERSAO 2 - OTIMIZADA" acima; efeito medido no D-023

# Mesmos blocos Unicode de scripts/detect_languages.py (subconjunto
# suficiente para o proxy). CASE ordenado -> particao garantida.
LANG_PROXY_CASE = """
    CASE
      WHEN regexp_matches(content, '[぀-ゟ]') OR regexp_matches(content, '[゠-ヿ]')
        THEN 'L3_proxy_ja'
      WHEN regexp_matches(content, '[가-힯]') THEN 'L3_proxy_ko'
      WHEN regexp_matches(content, '[一-鿿]') THEN 'L2_proxy_zh'
      WHEN regexp_matches(content, '[Ѐ-ӿ]') THEN 'L5_proxy_cyrillic'
      WHEN regexp_matches(content, '[؀-ۿ]') OR regexp_matches(content, '[֐-׿]')
           OR regexp_matches(content, '[ऀ-ॿ]') OR regexp_matches(content, '[฀-๿]')
        THEN 'L5_proxy_other_script'
      WHEN regexp_matches(content, '[À-ɏ]') THEN 'L4_proxy_latin_accented'
      ELSE 'L1_proxy_ascii_latin'
    END
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None,
                    help="limita a populacao processada (teste/depuracao)")
    args = ap.parse_args()

    art_glob = (DATA_DIR / "artifacts" / "*.parquet").as_posix()
    mc_path = MODELS_DIR / "security_classifier_v1_multiclass.joblib"
    bin_path = MODELS_DIR / "security_classifier_v1_binary.joblib"
    meta_path = MODELS_DIR / "security_classifier_v1_metadata.json"
    if not (mc_path.exists() and bin_path.exists()):
        print("ERRO: rode train_security_classifier.py primeiro", file=sys.stderr)
        return 1

    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    # artefatos locais, gerados por scripts/train_security_classifier.py
    # nesta mesma maquina - carregamento de pickle seguro neste contexto.
    mc_pipe = joblib.load(mc_path)
    bin_pipe = joblib.load(bin_path)
    mc_classes = list(mc_pipe.classes_)
    bin_classes = list(bin_pipe.classes_)
    sec_idx = bin_classes.index("SECURITY")

    vec = mc_pipe.named_steps["vec"]
    assert vec.vocabulary_ == bin_pipe.named_steps["vec"].vocabulary_, (
        "vetorizadores divergentes - nao e seguro reaproveitar a matriz")
    mc_clf = mc_pipe.named_steps["clf"]
    bin_clf = bin_pipe.named_steps["clf"]

    con = duckdb.connect()
    con.execute("SET enable_progress_bar=false")
    con.execute("SET memory_limit='8GB'")
    W = "dedup_primary = 1 AND content IS NOT NULL"

    n_pop = con.execute(
        f"SELECT count(*) FROM read_parquet('{art_glob}') WHERE {W}"
    ).fetchone()[0]
    if args.limit:
        n_pop = min(n_pop, args.limit)
    print(f"populacao: {n_pop:,} conteudos distintos"
          + (f" (limitado a {args.limit:,})" if args.limit else ""))
    print(f"modelo implantado: {meta['deployed_algorithm']} "
          f"(melhor performer em CV: {meta['best_cv_performer']}, "
          f"nao implantado por custo computacional)")
    print(f"truncamento: {TRUNC_CHARS} caracteres | vetorizacao compartilhada "
          f"entre os 2 modelos | batch: {BATCH_SIZE}", flush=True)

    limit_sql = f" LIMIT {args.limit}" if args.limit else ""
    rel = con.sql(f"""
        SELECT file_sha, content, {LANG_PROXY_CASE} AS language_group
        FROM read_parquet('{art_glob}') WHERE {W}{limit_sql}
    """)

    RESULTS_DIR.mkdir(exist_ok=True)
    out_path = RESULTS_DIR / "EXP-012_population_classification.parquet"
    schema = pa.schema([
        ("file_sha", pa.string()),
        ("predicted_class", pa.string()),
        ("predicted_class_confidence", pa.float32()),
        ("predicted_security", pa.bool_()),
        ("predicted_security_confidence", pa.float32()),
        ("language_group", pa.string()),
    ])
    writer = pq.ParquetWriter(out_path, schema)

    n_done = 0
    class_counts = {c: 0 for c in mc_classes}
    security_count = 0
    lang_counts: dict[str, int] = {}
    conf_values = []
    uncertain_rows = []
    t0 = time.time()

    reader = rel.to_arrow_reader(BATCH_SIZE)
    while True:
        try:
            batch = reader.read_next_batch()
        except StopIteration:
            break
        bdf = batch.to_pandas()
        texts = [(t or "")[:TRUNC_CHARS] for t in bdf["content"]]

        X = vec.transform(texts)  # UMA vetorizacao, reaproveitada abaixo
        mc_proba = mc_clf.predict_proba(X)
        mc_argmax = mc_proba.argmax(axis=1)
        predicted_class = np.array(mc_classes)[mc_argmax]
        predicted_class_conf = mc_proba[np.arange(len(bdf)), mc_argmax]

        bin_proba = bin_clf.predict_proba(X)
        sec_conf = bin_proba[:, sec_idx]
        predicted_security = sec_conf >= 0.5

        out_tbl = pa.table({
            "file_sha": bdf["file_sha"].astype(str),
            "predicted_class": predicted_class,
            "predicted_class_confidence": predicted_class_conf.astype("float32"),
            "predicted_security": predicted_security,
            "predicted_security_confidence": sec_conf.astype("float32"),
            "language_group": bdf["language_group"].astype(str),
        }, schema=schema)
        writer.write_table(out_tbl)

        for c in mc_classes:
            class_counts[c] += int((predicted_class == c).sum())
        security_count += int(predicted_security.sum())
        for lg, cnt in bdf["language_group"].value_counts().items():
            lang_counts[lg] = lang_counts.get(lg, 0) + int(cnt)
        conf_values.append(predicted_class_conf)

        boundary_mask = ((sec_conf >= 0.35) & (sec_conf <= 0.65)) | \
            (np.isin(predicted_class, ["SECONDARY", "MENTION"]) &
             (predicted_class_conf <= 0.5))
        if boundary_mask.any():
            bsel = bdf.loc[boundary_mask, ["file_sha"]].copy()
            bsel["predicted_class"] = predicted_class[boundary_mask]
            bsel["predicted_class_confidence"] = predicted_class_conf[boundary_mask]
            bsel["predicted_security_confidence"] = sec_conf[boundary_mask]
            uncertain_rows.append(bsel)

        n_done += len(bdf)
        rate = n_done / (time.time() - t0)
        eta_min = (n_pop - n_done) / rate / 60 if rate else float("inf")
        print(f"  {n_done:>9,}/{n_pop:,}  ({rate:,.0f} itens/s, "
              f"ETA {eta_min:.1f} min)", flush=True)

    writer.close()
    elapsed = time.time() - t0
    conf_all = np.concatenate(conf_values) if conf_values else np.array([])

    summary = {
        "generated_at": pd.Timestamp.now("UTC").isoformat(),
        "deployed_algorithm": meta["deployed_algorithm"],
        "best_cv_performer_not_deployed": meta["best_cv_performer"],
        "n_population": n_pop,
        "n_classified": n_done,
        "performance": {
            "total_seconds": round(elapsed, 2),
            "items_per_second": round(n_done / elapsed, 1),
            "truncation_chars": TRUNC_CHARS,
            "shared_vectorization": True,
            "model_file_sizes_bytes": {
                "multiclass": mc_path.stat().st_size,
                "binary": bin_path.stat().st_size,
            },
        },
        "predicted_class_counts": class_counts,
        "predicted_class_pct": {c: round(100 * n / n_done, 3)
                                 for c, n in class_counts.items()} if n_done else {},
        "predicted_security_count": security_count,
        "predicted_non_security_count": n_done - security_count,
        "predicted_security_pct": round(100 * security_count / n_done, 3) if n_done else None,
        "language_group_proxy_counts": lang_counts,
        "language_group_proxy_note": (
            "Proxy barato por script Unicode calculado em SQL sobre toda a "
            "populacao - NAO e o detector validado lingua/py3langid de "
            "EXP-003/EXP-004. Nao distingue com precisao pt/es/fr/de/it "
            "(todos caem em L4_proxy_latin_accented) nem confirma ingles vs "
            "outras linguas latinas sem acento (todas caem em "
            "L1_proxy_ascii_latin)."
        ),
        "confidence_distribution": {
            "mean": float(np.mean(conf_all)) if len(conf_all) else None,
            "median": float(np.median(conf_all)) if len(conf_all) else None,
            "p10": float(np.percentile(conf_all, 10)) if len(conf_all) else None,
            "p90": float(np.percentile(conf_all, 90)) if len(conf_all) else None,
            "pct_below_0_5": round(100 * float((conf_all < 0.5).mean()), 3)
                              if len(conf_all) else None,
        },
        "inference_optimization_note": (
            "v1 deste script (sem truncamento, vetorizacao duplicada) foi "
            "encerrada pelo ambiente apos ~2h11min sem concluir; "
            "extrapolacao correta a partir do throughput medido era ~9,3h. "
            "Causa medida por profiling isolado: a vetorizacao TF-IDF char "
            "n-gram e o gargalo (nao a classificacao, ~0,2s/20k linhas), "
            "porque o comprimento medio real da populacao (~7.247 "
            "caracteres) e muito maior que o da amostra usada no benchmark "
            "inicial que gerou a estimativa errada de 15-16 min. v2 (esta "
            f"execucao): texto truncado a {TRUNC_CHARS} caracteres antes de "
            "vetorizar, vetorizacao compartilhada entre os dois "
            "classificadores (vocabularios identicos, verificado por "
            "igualdade exata). Uma tentativa de paralelizar com "
            "ProcessPoolExecutor falhou nesta maquina (Windows + uv, erro "
            "de import de scipy/sklearn nos processos-filho) - nao "
            "resolvida, o ganho da otimizacao serial ja foi considerado "
            "suficiente. Ver Decision Log D-023."
        ),
        "caveat": (
            "RESULTADO PRELIMINAR DO CLASSIFICADOR v1, nao estimativa "
            "estatistica de prevalencia. O classificador foi treinado num "
            "golden set operacional de n=49 (EXP-005, assistido por LLM, "
            "nao gold standard humano). O modelo IMPLANTADO (TF-IDF+"
            "LinearSVC) teve desempenho fraco na validacao cruzada "
            "(F1 binario ~0.21, nunca previu SECONDARY nem MENTION em "
            "nenhum repeat da CV) - ver EXP-012_metrics.json. Os numeros "
            "abaixo medem o que o pipeline produz em escala, nao a "
            "prevalencia real de Security Skills. Alem disso, esta rodada "
            f"classifica o TEXTO TRUNCADO a {TRUNC_CHARS} caracteres, nao o "
            "conteudo integral."
        ),
    }
    (RESULTS_DIR / "EXP-012_population_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False, default=str),
        encoding="utf-8")

    if uncertain_rows:
        unc = pd.concat(uncertain_rows, ignore_index=True)
        unc = unc.sort_values("predicted_class_confidence").head(300)
        meta_cols = con.execute(f"""
            SELECT file_sha, repo_full_name, path
            FROM read_parquet('{art_glob}')
            WHERE file_sha IN ({', '.join("'" + s + "'" for s in unc['file_sha'])})
        """).fetchdf()
        unc = unc.merge(meta_cols, on="file_sha", how="left")
        unc.to_csv(RESULTS_DIR / "EXP-012_uncertain_cases_sample.csv", index=False)
        print(f"OK -> results/EXP-012_uncertain_cases_sample.csv "
              f"(n={len(unc)})")

    print(f"\nconcluido: {n_done:,} itens em {elapsed:.1f}s "
          f"({n_done/elapsed:,.0f} itens/s)")
    print(f"predicted_class: {class_counts}")
    if n_done:
        print(f"SECURITY previsto: {security_count:,} "
              f"({100*security_count/n_done:.2f}%)")
    print(f"OK -> {out_path.relative_to(ROOT)}")
    print(f"OK -> results/EXP-012_population_summary.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
