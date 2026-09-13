"""EXP-014 — Estatisticas de concordancia entre avaliadores.

Calcula um conjunto de coeficientes complementares sobre a MESMA amostra,
porque nenhum deles sozinho e suficiente e cada um falha de um jeito
diferente:

  p_o           concordancia bruta. Nao corrige acaso; nunca reportar
                sozinho, mas obrigatorio ao lado dos demais (Feinstein &
                Cicchetti 1990: kappa e ininterpretavel sem ela).

  Cohen's k     padrao de facto para 2 avaliadores, categorias nominais.
                Corrige acaso pelas marginais de CADA avaliador.
                Fraqueza: o "paradoxo do kappa" -- com marginais
                desbalanceadas (nosso caso: PRIMARY ~9%), k despenca mesmo
                com p_o alto.

  Krippendorff  padrao-ouro da analise de conteudo (Krippendorff 2004;
  alpha         Hayes & Krippendorff 2007). Generaliza para qualquer
                numero de avaliadores, dados faltantes e niveis de
                medida. Krippendorff argumenta explicitamente que alpha
                deve substituir kappa.

  Gwet's AC1    projetado para corrigir o paradoxo do kappa (Gwet 2008).
                Usa uma probabilidade de acaso que nao colapsa sob
                prevalencia extrema. Quando k e AC1 divergem muito, a
                diferenca E o diagnostico.

  Brennan-      corrige acaso assumindo distribuicao uniforme entre
  Prediger      categorias (Brennan & Prediger 1981). Robusto a
                prevalencia, mas depende do numero de categorias.

  PI / BI       indice de prevalencia e indice de vies (Byrt, Bishop &
                Carlin 1993). Diagnosticam POR QUE k esta deprimido:
                PI alto = categorias desbalanceadas; BI alto = os
                avaliadores usam as categorias em proporcoes diferentes.

  PABAK         kappa ajustado por prevalencia e vies (= 2*p_o - 1).

  McNemar       testa se a discordancia e SISTEMATICA (um avaliador
                sobe consistentemente) ou simetrica. Relevante aqui
                porque o EXP-013 encontrou vies direcional por modelo.

Intervalos de confianca por bootstrap percentil sobre as unidades.

Uso (aceita .jsonl de modelo e .csv de formulario humano):
    python scripts/compute_agreement.py \
        --a results/EXP-014_adjudication_victor.csv \
        --b results/EXP-014_adjudication_havillon.csv \
        --label-a victor --label-b havillon --original-marking \
        --out results/EXP-014_human_agreement_original.json

    python scripts/compute_agreement.py \
        --a results/EXP-013_llm_cases/classifications.jsonl \
        --b results/EXP-014_claude_output.jsonl \
        --label-a gpt --label-b claude \
        --out results/EXP-014_agreement.json
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import re
from collections import Counter
from pathlib import Path

SECURITY_CLASSES = {"PRIMARY", "SECONDARY"}


MARKING_FIX = re.compile(r"rotulo corrigido de (PRIMARY|SECONDARY|NONE) para (PRIMARY|SECONDARY|NONE)")


def load_labels(path: Path, field: str = "security_relevance",
                original_marking: bool = False) -> dict[str, str]:
    """Le rotulos de .jsonl (saida dos modelos) ou .csv (formulario humano).

    `original_marking`: nos formularios humanos, um erro de marcacao
    corrigido depois da anotacao fica registrado na nota como
    "rotulo corrigido de X para Y". Com a flag ligada, devolve X - a
    marcacao original, antes de qualquer conversa entre anotadores. E a
    concordancia que deve ser reportada como independente (D-031).
    """
    out = {}
    if path.suffix.lower() == ".csv":
        with path.open(encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                cid = (row.get("case_id") or "").strip()
                val = (row.get(field) or "").strip().upper()
                if not cid or not val:
                    continue
                if original_marking:
                    m = MARKING_FIX.search(row.get("note") or "")
                    if m:
                        val = m.group(1)
                out[cid] = val
        return out
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            cid = obj.get("case_id")
            if cid and field in obj:
                out[cid] = str(obj[field])
    return out


def observed_agreement(a: list[str], b: list[str]) -> float:
    return sum(1 for x, y in zip(a, b) if x == y) / len(a)


def cohen_kappa(a: list[str], b: list[str]) -> float:
    n = len(a)
    cats = set(a) | set(b)
    po = observed_agreement(a, b)
    ca, cb = Counter(a), Counter(b)
    pe = sum((ca[c] / n) * (cb[c] / n) for c in cats)
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def krippendorff_alpha_nominal(a: list[str], b: list[str]) -> float:
    """Dois avaliadores, dados completos, metrica nominal.

    Matriz de coincidencia: cada unidade com valores (x, y) contribui
    com os pares ordenados (x,y) e (y,x), divididos por (m_u - 1) = 1.
    """
    cats = sorted(set(a) | set(b))
    o: dict[tuple[str, str], float] = {(c, k): 0.0 for c in cats for k in cats}
    for x, y in zip(a, b):
        o[(x, y)] += 1.0
        o[(y, x)] += 1.0
    n_c = {c: sum(o[(c, k)] for k in cats) for c in cats}
    n_total = sum(n_c.values())
    if n_total <= 1:
        return float("nan")
    disagree_o = sum(o[(c, k)] for c in cats for k in cats if c != k)
    disagree_e = sum(n_c[c] * n_c[k] for c in cats for k in cats if c != k)
    if disagree_e == 0:
        return 1.0
    return 1.0 - (n_total - 1) * disagree_o / disagree_e


def gwet_ac1(a: list[str], b: list[str]) -> float:
    n = len(a)
    cats = sorted(set(a) | set(b))
    K = len(cats)
    if K < 2:
        return 1.0
    po = observed_agreement(a, b)
    ca, cb = Counter(a), Counter(b)
    pi = {c: ((ca[c] / n) + (cb[c] / n)) / 2 for c in cats}
    pe = sum(pi[c] * (1 - pi[c]) for c in cats) / (K - 1)
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def brennan_prediger(a: list[str], b: list[str]) -> float:
    cats = set(a) | set(b)
    K = len(cats)
    if K < 2:
        return 1.0
    po = observed_agreement(a, b)
    return (po - 1 / K) / (1 - 1 / K)


def binary_indices(a: list[str], b: list[str], positive: str) -> dict:
    """PI, BI, PABAK e McNemar -- so fazem sentido em 2x2."""
    n = len(a)
    cell_a = sum(1 for x, y in zip(a, b) if x == positive and y == positive)
    cell_b = sum(1 for x, y in zip(a, b) if x == positive and y != positive)
    cell_c = sum(1 for x, y in zip(a, b) if x != positive and y == positive)
    cell_d = sum(1 for x, y in zip(a, b) if x != positive and y != positive)
    po = (cell_a + cell_d) / n
    pi = abs(cell_a - cell_d) / n
    bi = abs(cell_b - cell_c) / n
    pabak = 2 * po - 1
    # McNemar exato (binomial bicaudal sobre os discordantes)
    m = cell_b + cell_c
    if m == 0:
        p_mcnemar = 1.0
    else:
        k = min(cell_b, cell_c)
        tail = sum(math.comb(m, i) for i in range(0, k + 1)) / (2 ** m)
        p_mcnemar = min(1.0, 2 * tail)
    return {
        "table": {"a_pos_pos": cell_a, "b_pos_neg": cell_b, "c_neg_pos": cell_c, "d_neg_neg": cell_d},
        "prevalence_index": round(pi, 4),
        "bias_index": round(bi, 4),
        "pabak": round(pabak, 4),
        "mcnemar_exact_p": round(p_mcnemar, 5),
        "mcnemar_reading": (
            "discordancia SISTEMATICA (um avaliador sobe consistentemente)"
            if p_mcnemar < 0.05
            else "discordancia simetrica (sem vies direcional detectavel)"
        ),
    }


def bootstrap_ci(a: list[str], b: list[str], fn, iters: int = 5000, seed: int = 20260904) -> tuple:
    rng = random.Random(seed)
    n = len(a)
    vals = []
    for _ in range(iters):
        idx = [rng.randrange(n) for _ in range(n)]
        sa = [a[i] for i in idx]
        sb = [b[i] for i in idx]
        if len(set(sa) | set(sb)) < 2:
            continue
        try:
            vals.append(fn(sa, sb))
        except (ZeroDivisionError, ValueError):
            continue
    if not vals:
        return (float("nan"), float("nan"))
    vals.sort()
    lo = vals[int(0.025 * len(vals))]
    hi = vals[min(len(vals) - 1, int(0.975 * len(vals)))]
    return (round(lo, 4), round(hi, 4))


def landis_koch(k: float) -> str:
    if k < 0:
        return "pobre"
    if k <= 0.20:
        return "leve"
    if k <= 0.40:
        return "sofrivel"
    if k <= 0.60:
        return "moderada"
    if k <= 0.80:
        return "substancial"
    return "quase perfeita"


def analyse(a: list[str], b: list[str], name: str, positive: str | None = None) -> dict:
    res = {
        "n": len(a),
        "categories": sorted(set(a) | set(b)),
        "observed_agreement": round(observed_agreement(a, b), 4),
        "cohen_kappa": round(cohen_kappa(a, b), 4),
        "cohen_kappa_ci95": bootstrap_ci(a, b, cohen_kappa),
        "krippendorff_alpha": round(krippendorff_alpha_nominal(a, b), 4),
        "krippendorff_alpha_ci95": bootstrap_ci(a, b, krippendorff_alpha_nominal),
        "gwet_ac1": round(gwet_ac1(a, b), 4),
        "gwet_ac1_ci95": bootstrap_ci(a, b, gwet_ac1),
        "brennan_prediger": round(brennan_prediger(a, b), 4),
        "landis_koch_cohen": landis_koch(cohen_kappa(a, b)),
        "dist_a": dict(Counter(a)),
        "dist_b": dict(Counter(b)),
    }
    if positive is not None:
        res.update(binary_indices(a, b, positive))
    return {name: res}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--a", required=True, type=Path)
    p.add_argument("--b", required=True, type=Path)
    p.add_argument("--label-a", default="rater_a")
    p.add_argument("--label-b", default="rater_b")
    p.add_argument("--out", type=Path, default=None)
    p.add_argument("--original-marking", action="store_true",
                   help="em CSV humano, desfaz correcoes de marcacao registradas na nota")
    args = p.parse_args()

    la = load_labels(args.a, original_marking=args.original_marking)
    lb = load_labels(args.b, original_marking=args.original_marking)
    ids = sorted(set(la) & set(lb))
    if not ids:
        raise SystemExit("Nenhum case_id em comum.")

    a = [la[i] for i in ids]
    b = [lb[i] for i in ids]
    a_bin = ["SECURITY" if x in SECURITY_CLASSES else "NOT" for x in a]
    b_bin = ["SECURITY" if x in SECURITY_CLASSES else "NOT" for x in b]

    out = {
        "rater_a": {"label": args.label_a, "file": str(args.a)},
        "rater_b": {"label": args.label_b, "file": str(args.b)},
        "original_marking": args.original_marking,
        "n_paired": len(ids),
        "n_only_a": len(set(la) - set(lb)),
        "n_only_b": len(set(lb) - set(la)),
        "bootstrap_iterations": 5000,
        "bootstrap_seed": 20260904,
    }
    out.update(analyse(a, b, "class_security_relevance"))
    out.update(analyse(a_bin, b_bin, "binary_security_vs_not", positive="SECURITY"))

    disagree = [i for i in ids if la[i] != lb[i]]
    out["adjudication"] = {
        "n_class_disagreement": len(disagree),
        "case_ids": disagree,
        "rule": "Sob D-027 a adjudicacao da PRIMEIRA classificacao considera "
        "apenas security_relevance; as dimensoes de apoio nao disparam "
        "revisao humana (serao refeitas na reclassificacao taxonomica "
        "posterior, sobre PRIMARY+SECONDARY).",
    }

    txt = json.dumps(out, ensure_ascii=False, indent=2)
    if args.out:
        args.out.write_text(txt, encoding="utf-8")
        print(f"Escrito em {args.out}")
    print(txt)


if __name__ == "__main__":
    main()
