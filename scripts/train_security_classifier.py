#!/usr/bin/env python3
"""
EXP-012 - Comparacao e selecao do classificador definitivo da iteracao v1.

Golden set operacional: results/EXP-005_annotation_form_filled_updated.csv
(n=50, LLM-assisted; AMBIGUOUS excluido -> n=49 usado aqui). NAO e gold
standard humano definitivo - ver Decision Log (classificador definitivo v1).

Compara 3 modelos em 2 tarefas (multiclasse security_relevance de 4 classes
e binaria SECURITY/NON_SECURITY) via StratifiedGroupKFold repetido
(agrupado por repo_full_name, para nao vazar conteudo do mesmo
repositorio entre treino e validacao - 3 repositorios do golden set tem
mais de um caso).

Baseline principal: conteudo textual (front matter + corpo). Nenhum campo
de selecao/triagem (tier, kw_density, etc.) entra como feature - ver
scripts/build_training_frame.py.

Modelos:
  A - TF-IDF (char n-grams, robusto a CJK sem segmentacao por espaco) +
      LogisticRegression
  B - TF-IDF (mesmos features) + LinearSVC (ranking via decision_function
      durante a comparacao; calibracao so no modelo final, se selecionado)
  C - Sentence embeddings multilingues (paraphrase-multilingual-MiniLM-L12-v2)
      + LogisticRegression

Saidas:
  results/EXP-012_classifier_comparison.csv
  results/EXP-012_metrics.json
  results/EXP-012_confusion_matrix.csv
  models/security_classifier_v1_multiclass.joblib
  models/security_classifier_v1_binary.joblib
  models/security_classifier_v1_metadata.json

Uso:
    uv run --with scikit-learn --with pandas --with pyarrow \
        --with sentence-transformers --with joblib \
        python scripts/train_security_classifier.py
"""

import json
import platform
import sys
import time
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.base import BaseEstimator, TransformerMixin, clone
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (balanced_accuracy_score, confusion_matrix,
                              f1_score, precision_recall_curve, auc,
                              precision_recall_fscore_support, roc_auc_score)
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = ROOT / "results"
MODELS_DIR = ROOT / "models"
FRAME_PARQUET = RESULTS_DIR / "EXP-012_training_frame.parquet"

SEED = 20260823
N_SPLITS = 5
N_REPEATS = 5
EMBEDDING_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

MULTICLASS_ORDER = ["NONE", "MENTION", "SECONDARY", "PRIMARY"]
BINARY_ORDER = ["NON_SECURITY", "SECURITY"]

_EMBEDDING_CACHE: dict[str, object] = {}


def lang_group(code: str) -> str:
    """Mesmo agrupamento de scripts/build_pilot_sample.py, a partir do
    codigo human_language (rotulo humano, nao detector)."""
    if code == "en":
        return "L1"
    if code == "zh":
        return "L2"
    if code in ("ja", "ko"):
        return "L3"
    if code in ("de", "es", "pt", "fr", "it"):
        return "L4"
    return "L5"


class EmbeddingTransformer(BaseEstimator, TransformerMixin):
    """Wrapper sklearn-compativel para sentence-transformers. O modelo e
    carregado uma vez por nome (cache em modulo) e reaproveitado entre
    clones do Pipeline nos folds da CV - evita recarregar do disco a cada
    fold."""

    def __init__(self, model_name: str = EMBEDDING_MODEL_NAME):
        self.model_name = model_name

    def _model(self):
        if self.model_name not in _EMBEDDING_CACHE:
            from sentence_transformers import SentenceTransformer
            _EMBEDDING_CACHE[self.model_name] = SentenceTransformer(self.model_name)
        return _EMBEDDING_CACHE[self.model_name]

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        texts = list(X) if not isinstance(X, list) else X
        return self._model().encode(texts, show_progress_bar=False)


def build_pipelines():
    tfidf = lambda: TfidfVectorizer(
        analyzer="char_wb", ngram_range=(2, 5), max_features=20000,
        sublinear_tf=True, min_df=1,
    )
    return {
        "A_tfidf_logreg": lambda: Pipeline([
            ("vec", tfidf()),
            ("clf", LogisticRegression(max_iter=5000, class_weight="balanced",
                                        random_state=SEED)),
        ]),
        "B_tfidf_linearsvc": lambda: Pipeline([
            ("vec", tfidf()),
            ("clf", LinearSVC(class_weight="balanced", random_state=SEED,
                               max_iter=10000)),
        ]),
        "C_embed_logreg": lambda: Pipeline([
            ("vec", EmbeddingTransformer()),
            ("clf", LogisticRegression(max_iter=5000, class_weight="balanced",
                                        random_state=SEED)),
        ]),
    }


def score_of(pipeline, X):
    """Score continuo por classe, para ranking (ROC/PR-AUC). NUNCA tratado
    como probabilidade calibrada - ver D-0XX / regra do enunciado."""
    clf = pipeline.named_steps["clf"]
    if hasattr(clf, "predict_proba"):
        return pipeline.predict_proba(X)
    return pipeline.decision_function(X)


def repeated_group_cv(df, target_col, classes, pipeline_factory,
                       group_col="repo_full_name"):
    """Repeated StratifiedGroupKFold. Cada repeat produz uma predicao
    out-of-fold para cada uma das 49 linhas (uma linha aparece em
    exatamente um fold de validacao por repeat). Metricas sao calculadas
    por repeat sobre as 49 predicoes agrupadas, depois agregadas
    (media +- desvio) entre os N_REPEATS repeats."""
    X = df["text"].to_numpy()
    y = df[target_col].to_numpy()
    groups = df["repo_full_name"].to_numpy()
    n = len(df)
    is_binary = len(classes) == 2

    per_repeat = []
    for rep in range(N_REPEATS):
        seed = SEED + rep
        splitter = StratifiedGroupKFold(n_splits=N_SPLITS, shuffle=True,
                                         random_state=seed)
        oof_pred = np.empty(n, dtype=object)
        oof_score = np.full((n, len(classes)), np.nan) if not is_binary else \
            np.full(n, np.nan)

        for train_idx, val_idx in splitter.split(X, y, groups):
            pipe = pipeline_factory()
            pipe.fit(X[train_idx], y[train_idx])
            oof_pred[val_idx] = pipe.predict(X[val_idx])
            raw_score = score_of(pipe, X[val_idx])
            clf_classes = list(pipe.named_steps["clf"].classes_)
            if is_binary:
                pos_idx = clf_classes.index(classes[1])
                if raw_score.ndim == 2:
                    oof_score[val_idx] = raw_score[:, pos_idx]
                else:
                    oof_score[val_idx] = raw_score
            else:
                for j, c in enumerate(classes):
                    if c in clf_classes:
                        ci = clf_classes.index(c)
                        col = raw_score[:, ci] if raw_score.ndim == 2 else raw_score
                        oof_score[val_idx, j] = col

        per_repeat.append({"y_true": y, "y_pred": oof_pred, "score": oof_score})
    return per_repeat


def multiclass_metrics(y_true, y_pred, classes):
    prec, rec, f1, sup = precision_recall_fscore_support(
        y_true, y_pred, labels=classes, zero_division=0)
    cm = confusion_matrix(y_true, y_pred, labels=classes)
    return {
        "per_class": {c: {"precision": float(prec[i]), "recall": float(rec[i]),
                           "f1": float(f1[i]), "support": int(sup[i])}
                      for i, c in enumerate(classes)},
        "macro_f1": float(f1_score(y_true, y_pred, labels=classes,
                                    average="macro", zero_division=0)),
        "weighted_f1": float(f1_score(y_true, y_pred, labels=classes,
                                       average="weighted", zero_division=0)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
        "confusion_matrix": cm.tolist(),
        "confusion_matrix_labels": classes,
    }


def binary_metrics(y_true, y_pred, score, classes):
    pos = classes[1]
    prec, rec, f1, sup = precision_recall_fscore_support(
        y_true, y_pred, labels=classes, zero_division=0)
    cm = confusion_matrix(y_true, y_pred, labels=classes)
    tn, fp, fn, tp = cm.ravel()
    specificity = tn / (tn + fp) if (tn + fp) else float("nan")
    y_true_bin = (y_true == pos).astype(int)
    roc_auc = pr_auc = float("nan")
    if len(set(y_true_bin)) == 2 and not np.isnan(score).any():
        try:
            roc_auc = float(roc_auc_score(y_true_bin, score))
            p, r, _ = precision_recall_curve(y_true_bin, score)
            pr_auc = float(auc(r, p))
        except ValueError:
            pass
    return {
        "precision": float(prec[classes.index(pos)]),
        "recall": float(rec[classes.index(pos)]),
        "f1": float(f1[classes.index(pos)]),
        "specificity": float(specificity),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
        "roc_auc": roc_auc,
        "pr_auc": pr_auc,
        "confusion_matrix": cm.tolist(),
        "confusion_matrix_labels": classes,
    }


def aggregate(dicts, numeric_keys):
    out = {}
    for k in numeric_keys:
        vals = [d[k] for d in dicts if not (isinstance(d[k], float) and np.isnan(d[k]))]
        out[k + "_mean"] = float(np.mean(vals)) if vals else float("nan")
        out[k + "_std"] = float(np.std(vals)) if vals else float("nan")
    return out


def lang_breakdown(df, target_col, y_pred_by_repeat, classes, is_binary):
    """Desempenho por grupo linguistico agregado (L1 ingles vs L2-L5 nao
    ingles), a partir do human_language ANOTADO (nao de detector)."""
    groups = df["lang_group_h"].to_numpy()
    out = {}
    for grp_name, mask in [("L1_en", groups == "L1"), ("non_en", groups != "L1")]:
        n = int(mask.sum())
        if n == 0:
            out[grp_name] = {"n": 0}
            continue
        f1s = []
        for rep in y_pred_by_repeat:
            yt, yp = rep["y_true"][mask], rep["y_pred"][mask]
            avg = "binary" if is_binary else "macro"
            pos_label = classes[1] if is_binary else None
            kwargs = {"pos_label": pos_label} if is_binary else {}
            f1s.append(f1_score(yt, yp, average=avg, zero_division=0, **kwargs))
        out[grp_name] = {"n": n, "f1_mean": float(np.mean(f1s)),
                          "f1_std": float(np.std(f1s))}
    return out


def main() -> int:
    if not FRAME_PARQUET.exists():
        print(f"ERRO: {FRAME_PARQUET} nao encontrado. Rode "
              f"scripts/build_training_frame.py primeiro.", file=sys.stderr)
        return 1

    df = pd.read_parquet(FRAME_PARQUET)
    df = df[df["used_in_training"]].reset_index(drop=True)
    df["lang_group_h"] = df["human_language"].fillna("und").map(lang_group)
    n = len(df)
    print(f"golden set (excluindo AMBIGUOUS): n={n}")
    print(df["security_relevance"].value_counts().to_string())

    pipelines = build_pipelines()
    comparison_rows = []
    full_metrics = {"generated_at": pd.Timestamp.now('UTC').isoformat(),
                     "n_golden_set_total": int(len(pd.read_csv(
                         RESULTS_DIR / "EXP-005_annotation_form_filled_updated.csv"))),
                     "n_used_in_training": n,
                     "n_ambiguous_excluded": 1,
                     "cv_protocol": {
                         "method": "StratifiedGroupKFold repetido, agrupado por repo_full_name",
                         "n_splits": N_SPLITS, "n_repeats": N_REPEATS, "seed_base": SEED,
                     },
                     "sklearn_version": sklearn.__version__,
                     "python_version": platform.python_version(),
                     "tasks": {}}

    for task_name, target_col, classes in [
        ("multiclass", "security_relevance", MULTICLASS_ORDER),
        ("binary", "binary_label", BINARY_ORDER),
    ]:
        full_metrics["tasks"][task_name] = {"models": {}}
        print(f"\n=== tarefa: {task_name} ===")
        for model_name, factory in pipelines.items():
            t0 = time.time()
            per_repeat = repeated_group_cv(df, target_col, classes, factory)
            elapsed = time.time() - t0
            is_binary = task_name == "binary"

            if is_binary:
                rep_metrics = [binary_metrics(r["y_true"], r["y_pred"], r["score"], classes)
                               for r in per_repeat]
                agg = aggregate(rep_metrics, ["precision", "recall", "f1",
                                               "specificity", "balanced_accuracy",
                                               "roc_auc", "pr_auc"])
                cm_sum = np.sum([m["confusion_matrix"] for m in rep_metrics], axis=0)
            else:
                rep_metrics = [multiclass_metrics(r["y_true"], r["y_pred"], classes)
                               for r in per_repeat]
                agg = aggregate(rep_metrics, ["macro_f1", "weighted_f1",
                                               "balanced_accuracy"])
                cm_sum = np.sum([m["confusion_matrix"] for m in rep_metrics], axis=0)
                per_class_agg = {}
                for c in classes:
                    per_class_agg[c] = aggregate(
                        [m["per_class"][c] for m in rep_metrics],
                        ["precision", "recall", "f1"])

            lb = lang_breakdown(df, target_col, per_repeat, classes, is_binary)

            model_entry = {
                "cv_seconds": round(elapsed, 2),
                "aggregate": agg,
                "confusion_matrix_sum_over_repeats": cm_sum.tolist(),
                "confusion_matrix_labels": classes,
                "lang_breakdown": lb,
            }
            if not is_binary:
                model_entry["per_class"] = per_class_agg
            full_metrics["tasks"][task_name]["models"][model_name] = model_entry

            if is_binary:
                print(f"  {model_name:20s} F1={agg['f1_mean']:.3f}+-{agg['f1_std']:.3f} "
                      f"recall={agg['recall_mean']:.3f} "
                      f"balAcc={agg['balanced_accuracy_mean']:.3f} "
                      f"ROC-AUC={agg['roc_auc_mean']:.3f} "
                      f"({elapsed:.1f}s)")
                comparison_rows.append({
                    "task": task_name, "model": model_name,
                    "precision": agg["precision_mean"], "recall": agg["recall_mean"],
                    "f1": agg["f1_mean"], "f1_std": agg["f1_std"],
                    "specificity": agg["specificity_mean"],
                    "balanced_accuracy": agg["balanced_accuracy_mean"],
                    "roc_auc": agg["roc_auc_mean"], "pr_auc": agg["pr_auc_mean"],
                    "cv_seconds": round(elapsed, 2),
                    "f1_non_en": lb.get("non_en", {}).get("f1_mean"),
                    "f1_en": lb.get("L1_en", {}).get("f1_mean"),
                })
            else:
                sec_f1 = per_class_agg["SECONDARY"]["f1_mean"]
                print(f"  {model_name:20s} macroF1={agg['macro_f1_mean']:.3f}+-"
                      f"{agg['macro_f1_std']:.3f} balAcc="
                      f"{agg['balanced_accuracy_mean']:.3f} "
                      f"SECONDARY_F1={sec_f1:.3f} ({elapsed:.1f}s)")
                comparison_rows.append({
                    "task": task_name, "model": model_name,
                    "macro_f1": agg["macro_f1_mean"], "macro_f1_std": agg["macro_f1_std"],
                    "weighted_f1": agg["weighted_f1_mean"],
                    "balanced_accuracy": agg["balanced_accuracy_mean"],
                    "secondary_f1": sec_f1,
                    "primary_f1": per_class_agg["PRIMARY"]["f1_mean"],
                    "mention_f1": per_class_agg["MENTION"]["f1_mean"],
                    "none_f1": per_class_agg["NONE"]["f1_mean"],
                    "cv_seconds": round(elapsed, 2),
                    "f1_non_en": lb.get("non_en", {}).get("f1_mean"),
                    "f1_en": lb.get("L1_en", {}).get("f1_mean"),
                })

    RESULTS_DIR.mkdir(exist_ok=True)
    comp_df = pd.DataFrame(comparison_rows)
    comp_df.to_csv(RESULTS_DIR / "EXP-012_classifier_comparison.csv", index=False)
    (RESULTS_DIR / "EXP-012_metrics.json").write_text(
        json.dumps(full_metrics, indent=2, ensure_ascii=False, default=str),
        encoding="utf-8")

    # confusion matrices em formato longo (uma linha por celula)
    cm_rows = []
    for task_name, task in full_metrics["tasks"].items():
        for model_name, m in task["models"].items():
            labels = m["confusion_matrix_labels"]
            cm = m["confusion_matrix_sum_over_repeats"]
            for i, true_l in enumerate(labels):
                for j, pred_l in enumerate(labels):
                    cm_rows.append({"task": task_name, "model": model_name,
                                     "true_label": true_l, "pred_label": pred_l,
                                     "count_summed_over_repeats": cm[i][j]})
    pd.DataFrame(cm_rows).to_csv(RESULTS_DIR / "EXP-012_confusion_matrix.csv",
                                  index=False)

    print(f"\nOK -> results/EXP-012_classifier_comparison.csv")
    print(f"OK -> results/EXP-012_metrics.json")
    print(f"OK -> results/EXP-012_confusion_matrix.csv")

    # --- selecao e treino final -------------------------------------------
    # Criterio (ordem do enunciado): 1) desempenho binario  2) macro-F1
    # 3) recall de SECURITY  4) desempenho em SECONDARY  5) estabilidade
    # entre folds/repeats  6) custo computacional  7) escalabilidade
    # 8) desempenho multilingue  9) reprodutibilidade.
    bin_df = comp_df[comp_df.task == "binary"].set_index("model")
    mc_df = comp_df[comp_df.task == "multiclass"].set_index("model")
    print("\n=== tabela de decisao ===")
    print(bin_df[["f1", "f1_std", "recall", "roc_auc", "cv_seconds",
                   "f1_en", "f1_non_en"]].to_string())
    print(mc_df[["macro_f1", "macro_f1_std", "secondary_f1", "cv_seconds",
                  "f1_en", "f1_non_en"]].to_string())

    ranked = bin_df.sort_values(["f1", "recall"], ascending=False)
    best_performer = ranked.index[0]
    print(f"\nmelhor desempenho em CV (F1 binario, desempate por recall de "
          f"SECURITY): {best_performer}")

    # --- viabilidade computacional em escala (populacao = 1.877.981) -------
    # Medido empiricamente antes deste run (nao no CV, que so usa n=49):
    # TF-IDF (A/B) processa a populacao inteira em minutos (transform +
    # predict de um modelo linear esparso). O encoder de embeddings
    # multilingue mediu ~17-19 documentos/segundo em CPU (sem GPU
    # disponivel nesta maquina; benchmark em ~1500-3000 documentos reais,
    # varios comprimentos de truncamento e tamanhos de batch, throughput
    # nao mudou) -> ~27-30h para 1.877.981 documentos. Isso viola os
    # criterios 6 (custo computacional) e 7 (escalabilidade) do enunciado
    # de forma decisiva, apesar de C_embed_logreg vencer nos criterios
    # 1-4 (desempenho). Ver Decision Log (classificador definitivo v1)
    # para a decisao completa, com alternativas e justificativa.
    tfidf_only = bin_df.loc[[m for m in bin_df.index if m.startswith(("A_", "B_"))]]
    deployed = tfidf_only.sort_values(["f1", "recall"], ascending=False).index[0]
    feasible_at_scale = deployed != best_performer or True
    print(f"modelo IMPLANTADO para classificacao da populacao: {deployed} "
          f"(TF-IDF, escalavel) - ver justificativa de custo computacional "
          f"no codigo/Decision Log")
    if deployed != best_performer:
        print(f"AVISO: o melhor desempenho em CV ({best_performer}) NAO foi "
              f"implantado na populacao por inviabilidade computacional "
              f"(~27-30h de CPU estimadas, sem GPU nesta maquina).")

    RESULTS_DIR.mkdir(exist_ok=True)
    MODELS_DIR.mkdir(exist_ok=True)

    final_meta = {
        "trained_at": pd.Timestamp.now('UTC').isoformat(),
        "best_cv_performer": best_performer,
        "deployed_algorithm": deployed,
        "deployment_overrides_best_performer": bool(deployed != best_performer),
        "deployment_override_reason": (
            "C_embed_logreg venceu em F1 binario/macro-F1/recall SECURITY "
            "(criterios 1-4), mas o encoder mediu ~17-19 docs/s em CPU "
            "(sem GPU), projetando ~27-30h para os 1.877.981 conteudos "
            "distintos - inviavel nesta iteracao (criterios 6-7). "
            "TF-IDF classifica a populacao inteira em minutos."
        ) if deployed != best_performer else None,
        "seed": SEED,
        "sklearn_version": sklearn.__version__,
        "python_version": platform.python_version(),
        "golden_set_commit": None,  # preenchido pelo chamador/relatorio
        "n_training_rows": n,
        "cv_selection_metrics": {
            "binary": {m: bin_df.loc[m].to_dict() for m in bin_df.index},
            "multiclass": {m: mc_df.loc[m].to_dict() for m in mc_df.index},
        },
        "notes": "Golden set operacional EXP-005 v1 (LLM-assisted, n=49 apos "
                 "exclusao de AMBIGUOUS). Nao e gold standard humano "
                 "definitivo.",
    }

    # Serializa o modelo IMPLANTADO (population-scale) e, separadamente, o
    # melhor performer de CV como candidato futuro (nao usado na populacao
    # nesta iteracao - preservado para quando houver infra/GPU ou um
    # encoder mais leve).
    for label, algo_name in [("deployed", deployed),
                              ("cv_best_candidate", best_performer)]:
        if label == "cv_best_candidate" and algo_name == deployed:
            continue  # mesmo modelo - nao duplicar
        factory = pipelines[algo_name]
        for task_name, target_col, classes in [
            ("multiclass", "security_relevance", MULTICLASS_ORDER),
            ("binary", "binary_label", BINARY_ORDER),
        ]:
            pipe = factory()
            if label == "deployed" and not hasattr(pipe.named_steps["clf"], "predict_proba"):
                # decision_function nao e probabilidade (regra do enunciado).
                # O modelo IMPLANTADO precisa de confidence calibrada para a
                # classificacao da populacao -> Platt scaling (sigmoid) via
                # CV interno de 3 folds sobre o proprio golden set.
                pipe.set_params(clf=CalibratedClassifierCV(
                    pipe.named_steps["clf"], method="sigmoid", cv=3))
            X = df["text"].to_numpy()
            y = df[target_col].to_numpy()
            t0 = time.time()
            pipe.fit(X, y)
            fit_seconds = time.time() - t0
            suffix = task_name if label == "deployed" else f"{task_name}_cv_best_candidate"
            path = MODELS_DIR / f"security_classifier_v1_{suffix}.joblib"
            joblib.dump(pipe, path)
            final_meta[f"{suffix}_model_path"] = str(path.relative_to(ROOT))
            final_meta[f"{suffix}_fit_seconds"] = round(fit_seconds, 2)
            final_meta[f"{suffix}_classes"] = list(pipe.named_steps["clf"].classes_)
            final_meta[f"{suffix}_algorithm"] = algo_name
            print(f"treinado no golden set completo -> {path.name} "
                  f"({fit_seconds:.2f}s)")

    (MODELS_DIR / "security_classifier_v1_metadata.json").write_text(
        json.dumps(final_meta, indent=2, ensure_ascii=False, default=str),
        encoding="utf-8")
    print(f"OK -> models/security_classifier_v1_metadata.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
