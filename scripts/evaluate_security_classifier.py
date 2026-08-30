#!/usr/bin/env python3
"""
EXP-012 - Relatorio de avaliacao do classificador definitivo v1.

Nao re-executa a validacao cruzada (isso e scripts/train_security_classifier.py).
Este script: (1) confere a integridade dos artefatos serializados - carrega
os modelos IMPLANTADOS e reproduz as predicoes no golden set completo, como
checagem de que o .joblib salvo corresponde ao que foi treinado; (2) formata
o relatorio final a partir de results/EXP-012_metrics.json e
results/EXP-012_classifier_comparison.csv, ja produzidos pelo treino.

Uso:
    uv run --with scikit-learn --with pandas --with pyarrow --with joblib \
        python scripts/evaluate_security_classifier.py
"""

import json
import sys
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score

ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = ROOT / "results"
MODELS_DIR = ROOT / "models"


def main() -> int:
    frame_path = RESULTS_DIR / "EXP-012_training_frame.parquet"
    meta_path = MODELS_DIR / "security_classifier_v1_metadata.json"
    metrics_path = RESULTS_DIR / "EXP-012_metrics.json"
    if not (frame_path.exists() and meta_path.exists() and metrics_path.exists()):
        print("ERRO: rode build_training_frame.py e train_security_classifier.py "
              "antes deste script", file=sys.stderr)
        return 1

    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    df = pd.read_parquet(frame_path)
    df = df[df["used_in_training"]].reset_index(drop=True)

    print("=== checagem de integridade dos artefatos serializados ===")
    for task, target_col in [("multiclass", "security_relevance"),
                              ("binary", "binary_label")]:
        path = ROOT / meta[f"{task}_model_path"]
        pipe = joblib.load(path)  # artefato local, gerado por este mesmo pipeline
        preds = pipe.predict(df["text"].to_numpy())
        y = df[target_col].to_numpy()
        acc = accuracy_score(y, preds)
        avg = "macro" if task == "multiclass" else "binary"
        kwargs = {} if task == "multiclass" else {"pos_label": "SECURITY"}
        f1 = f1_score(y, preds, average=avg, zero_division=0, **kwargs)
        print(f"  {path.name}: carregado OK, algoritmo={meta[f'{task}_algorithm']}")
        print(f"    treino-completo (nao e generalizacao): "
              f"accuracy={acc:.3f} f1({avg})={f1:.3f}")
        print(f"    ATENCAO: isto e desempenho no proprio conjunto de treino "
              f"(re-treinado com todo o golden set); a estimativa de "
              f"generalizacao valida e a CV em EXP-012_metrics.json.")

    print("\n=== resumo da comparacao (de EXP-012_classifier_comparison.csv) ===")
    comp = pd.read_csv(RESULTS_DIR / "EXP-012_classifier_comparison.csv")
    print(comp.to_string(index=False))

    print("\n=== decisao de implantacao ===")
    print(f"melhor performer em CV:  {meta['best_cv_performer']}")
    print(f"modelo implantado (populacao): {meta['deployed_algorithm']}")
    if meta.get("deployment_overrides_best_performer"):
        print(f"motivo do override: {meta['deployment_override_reason']}")

    print("\n=== confusao SECONDARY <-> MENTION (a que altera a prevalencia) ===")
    cm = pd.read_csv(RESULTS_DIR / "EXP-012_confusion_matrix.csv")
    mc_cm = cm[(cm.task == "multiclass") &
               (cm.true_label.isin(["SECONDARY", "MENTION"])) &
               (cm.pred_label.isin(["SECONDARY", "MENTION"]))]
    print(mc_cm.pivot_table(index=["model", "true_label"], columns="pred_label",
                             values="count_summed_over_repeats").to_string())

    print("\n=== confusao PRIMARY <-> SECONDARY (nao altera o agregado SECURITY) ===")
    ps_cm = cm[(cm.task == "multiclass") &
               (cm.true_label.isin(["PRIMARY", "SECONDARY"])) &
               (cm.pred_label.isin(["PRIMARY", "SECONDARY"]))]
    print(ps_cm.pivot_table(index=["model", "true_label"], columns="pred_label",
                             values="count_summed_over_repeats").to_string())

    return 0


if __name__ == "__main__":
    sys.exit(main())
