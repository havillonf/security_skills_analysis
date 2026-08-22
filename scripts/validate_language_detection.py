#!/usr/bin/env python3
"""
EXP-004 - Validacao do detector de idioma por concordancia entre detectores.

Motivacao: em EXP-003 o py3langid reportou confianca media de 1,000, o que e
implausivel. Antes de usar idioma como variavel de estratificacao do Desenho C
(D-014), e preciso ter alguma medida da confiabilidade do rotulo.

Desenho: dois detectores INDEPENDENTES sobre a mesma amostra estratificada.
  - lingua-language-detector, high accuracy mode  -> detector PRIMARIO
  - py3langid (Lui & Baldwin 2012), norm_probs=True -> segunda opiniao

v2 (2026-08-22) - CORRECAO. A v1 estratificava por 7 categorias auxiliares
(S_en, S_cjk, S_multilingue, ...) numa cadeia if/elif em que a checagem de
script vinha ANTES da de idioma. Como praticamente todo texto CJK contem alguma
palavra ASCII, o CJK inteiro caiu em S_multilingue e S_cjk ficou com 10 casos de
6.000 - um residuo atipico. As concordancias daquela particao foram entao
transplantadas para L1-L5, e "1,00" foi atribuido a L2 e L3 SEM QUE TIVESSEM
SIDO MEDIDOS.

v2 estratifica pelos grupos L1-L5 REAIS, definidos pelo detector primario, e
trata texto curto / muito codigo / multi-script como ATRIBUTOS transversais,
nao como estratos concorrentes.

Concordancia entre detectores NAO e acuracia. E um limite superior grosseiro da
confiabilidade: onde discordam, ao menos um esta errado. Os casos de discordancia
sao exportados para inspecao manual.

Pratica seguida do GitHub Multilingual Repositories Dataset: manter a saida de
multiplos classificadores em vez de colapsar num rotulo unico.

Uso:
    uv run --with duckdb --with py3langid --with lingua-language-detector \
        python scripts/validate_language_detection.py --per-stratum 15
"""

import argparse
import json
import random
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_DIR = ROOT / "data" / "raw" / "gitskills" / "data"
RESULTS_DIR = ROOT / "results"

sys.path.insert(0, str(ROOT / "scripts"))
from detect_languages import clean_prose, split_frontmatter, SCRIPTS  # noqa: E402

SEED = 20260822


def lang_group(lang):
    """Grupos L1-L5 conforme notes/Methodology/Multilingual Strategy.md."""
    if lang == "en":
        return "L1"
    if lang == "zh":
        return "L2"
    if lang in ("ja", "ko"):
        return "L3"
    if lang in ("de", "es", "pt", "fr", "it"):
        return "L4"
    return "L5"


def build_strata(rows, label_primary, label_secondary):
    """Estratos = L1..L5 pelo detector PRIMARIO. Atributos sao transversais."""
    strata = defaultdict(list)
    for sha, content in rows:
        _fm, body = split_frontmatter(content)
        prose = clean_prose(body)

        la = label_primary(prose)      # lingua  -> define o grupo
        lb, prob = label_secondary(prose)  # py3langid -> segunda opiniao

        code_ratio = 1 - (len(prose) / max(len(content), 1))
        n_scripts = sum(1 for n, p in SCRIPTS.items()
                        if n != "latin_ext" and re.search(p, prose))
        has_ascii = bool(re.search(r"[A-Za-z]{4,}", prose))

        item = {
            "sha": sha, "prose": prose,
            "primary": la, "secondary": lb, "secondary_conf": prob,
            "short": len(prose) < 200,
            "code_heavy": code_ratio > 0.7,
            "multi_script": bool(n_scripts >= 1 and has_ascii),
        }
        strata[lang_group(la)].append(item)
    return strata


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default=str(DEFAULT_DATA_DIR))
    ap.add_argument("--pool", type=int, default=6000,
                    help="pool inicial de onde os estratos sao formados")
    ap.add_argument("--per-stratum", type=int, default=15)
    args = ap.parse_args()

    art = Path(args.data_dir) / "artifacts"
    if not list(art.glob("*.parquet")):
        print(f"ERRO: nenhum Parquet em {art}", file=sys.stderr)
        return 1

    try:
        from py3langid.langid import LanguageIdentifier, MODEL_FILE
        from lingua import LanguageDetectorBuilder
    except ImportError as e:
        print(f"ERRO: dependencia ausente ({e}). Rode com --with py3langid "
              f"--with lingua-language-detector", file=sys.stderr)
        return 1

    ident = LanguageIdentifier.from_pickled_model(MODEL_FILE, norm_probs=True)
    lingua = LanguageDetectorBuilder.from_all_languages().build()

    def label_primary(prose):
        if len(prose) < 20:
            return "und"
        lg = lingua.detect_language_of(prose)
        return lg.iso_code_639_1.name.lower() if lg else "und"

    def label_secondary(prose):
        if len(prose) < 40:
            return "und", 0.0
        lang, prob = ident.classify(prose)
        return (lang, float(prob)) if prob >= 0.90 else ("und", float(prob))

    A = f"read_parquet('{(art / '*.parquet').as_posix()}')"
    con = duckdb.connect()
    con.execute("SET enable_progress_bar=false")
    rows = con.execute(f"""
        SELECT file_sha, content FROM {A}
        WHERE dedup_primary = 1 AND content IS NOT NULL
        ORDER BY hash(file_sha) LIMIT {args.pool}
    """).fetchall()

    strata = build_strata(rows, label_primary, label_secondary)
    rng = random.Random(SEED)

    out = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "version": 2,
        "seed": SEED,
        "pool": args.pool,
        "per_stratum": args.per_stratum,
        "detectors": {
            "primary": "lingua-language-detector, high accuracy mode",
            "secondary": "py3langid LanguageIdentifier(norm_probs=True), limiar 0.90",
        },
        "nota": ("estratos = grupos L1-L5 definidos pelo detector PRIMARIO; "
                 "curto/codigo/multi-script sao atributos transversais, nao estratos"),
        "stratum_pool_sizes": {k: len(v) for k, v in strata.items()},
    }

    per_stratum, disagreements, conf_when_wrong = {}, [], []
    confusion = Counter()
    attr_stats = defaultdict(lambda: {"n": 0, "agree": 0})

    for name in ["L1", "L2", "L3", "L4", "L5"]:
        items = strata.get(name, [])
        if not items:
            per_stratum[name] = {"n": 0, "agree": 0, "agreement": None,
                                 "pool": 0}
            print(f"  {name:4s} POOL VAZIO - sem suporte amostral")
            continue
        picked = rng.sample(items, min(args.per_stratum, len(items)))
        agree = 0
        for it in picked:
            ok = (it["primary"] == it["secondary"])
            agree += ok
            for a in ("short", "code_heavy", "multi_script"):
                if it[a]:
                    attr_stats[a]["n"] += 1
                    attr_stats[a]["agree"] += ok
            if not ok:
                confusion[(it["primary"], it["secondary"])] += 1
                conf_when_wrong.append(it["secondary_conf"])
                disagreements.append({
                    "stratum": name, "file_sha": it["sha"],
                    "lingua": it["primary"], "langid": it["secondary"],
                    "langid_conf": round(it["secondary_conf"], 4),
                    "short": it["short"], "code_heavy": it["code_heavy"],
                    "multi_script": it["multi_script"],
                    "prose_len": len(it["prose"]),
                    "excerpt": it["prose"][:200],
                })
        per_stratum[name] = {
            "n": len(picked), "agree": agree, "pool": len(items),
            "agreement": round(agree / len(picked), 3),
        }
        print(f"  {name:4s} pool={len(items):>5} n={len(picked):>3}  "
              f"concordancia={per_stratum[name]['agreement']}")

    out["per_stratum"] = per_stratum
    out["por_atributo"] = {
        a: {"n": v["n"], "agree": v["agree"],
            "agreement": round(v["agree"] / v["n"], 3) if v["n"] else None}
        for a, v in attr_stats.items()
    }

    tot_n = sum(v["n"] for v in per_stratum.values())
    tot_a = sum(v["agree"] for v in per_stratum.values())
    out["overall"] = {"n": tot_n, "agree": tot_a,
                      "agreement": round(tot_a / tot_n, 4) if tot_n else None}
    out["top_confusions"] = [
        {"lingua": a, "langid": b, "n": n} for (a, b), n in confusion.most_common(15)
    ]
    out["langid_confidence_when_disagreeing"] = {
        "n": len(conf_when_wrong),
        "mean": round(sum(conf_when_wrong) / len(conf_when_wrong), 4)
        if conf_when_wrong else None,
        "min": round(min(conf_when_wrong), 4) if conf_when_wrong else None,
        "max": round(max(conf_when_wrong), 4) if conf_when_wrong else None,
    }

    RESULTS_DIR.mkdir(exist_ok=True)
    (RESULTS_DIR / "EXP-004_langdetect_validation.json").write_text(
        json.dumps(out, indent=2, default=str), encoding="utf-8")
    (RESULTS_DIR / "EXP-004_disagreements.json").write_text(
        json.dumps(disagreements, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\nconcordancia global: {tot_a}/{tot_n} = {out['overall']['agreement']}")
    print(f"discordancias: {len(disagreements)}")
    print("confianca do langid QUANDO discorda:",
          out["langid_confidence_when_disagreeing"])
    print("top confusoes:", out["top_confusions"][:8])
    print(f"\nOK -> results/EXP-004_langdetect_validation.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
