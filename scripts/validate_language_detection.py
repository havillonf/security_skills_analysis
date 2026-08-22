#!/usr/bin/env python3
"""
EXP-004 - Validacao do detector de idioma por concordancia entre detectores.

Motivacao: em EXP-003 o py3langid reportou confianca media de 1,000, o que e
implausivel. Antes de usar idioma como variavel de estratificacao do Desenho C
(D-014), e preciso ter alguma medida da confiabilidade do rotulo.

Desenho: dois detectores INDEPENDENTES sobre a mesma amostra estratificada.
  - py3langid (Lui & Baldwin 2012; fork py3langid), norm_probs=True
  - lingua-language-detector, high accuracy mode

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


def build_strata(rows, langid_label):
    """Estratos desenhados para expor onde a deteccao falha, nao para representar."""
    strata = defaultdict(list)
    for sha, content in rows:
        _fm, body = split_frontmatter(content)
        prose = clean_prose(body)
        lang, prob = langid_label(prose)

        # sinais estruturais independentes do idioma previsto
        code_ratio = 1 - (len(prose) / max(len(content), 1))
        n_scripts = sum(1 for n, p in SCRIPTS.items()
                        if n != "latin_ext" and re.search(p, prose))
        has_ascii = bool(re.search(r"[A-Za-z]{4,}", prose))

        if len(prose) < 200:
            strata["S_texto_curto"].append((sha, prose, lang, prob))
        elif code_ratio > 0.7:
            strata["S_muito_codigo"].append((sha, prose, lang, prob))
        elif n_scripts >= 1 and has_ascii:
            strata["S_multilingue"].append((sha, prose, lang, prob))
        elif lang in ("en",):
            strata["S_en"].append((sha, prose, lang, prob))
        elif lang in ("zh", "ja", "ko"):
            strata["S_cjk"].append((sha, prose, lang, prob))
        elif lang in ("de", "es", "pt", "fr", "it"):
            strata["S_latino"].append((sha, prose, lang, prob))
        else:
            strata["S_cauda"].append((sha, prose, lang, prob))
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

    def langid_label(prose):
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

    strata = build_strata(rows, langid_label)
    rng = random.Random(SEED)

    out = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "seed": SEED,
        "pool": args.pool,
        "per_stratum": args.per_stratum,
        "detectors": {
            "a": "py3langid LanguageIdentifier(norm_probs=True), limiar 0.90",
            "b": "lingua-language-detector, high accuracy mode",
        },
        "stratum_pool_sizes": {k: len(v) for k, v in strata.items()},
    }

    per_stratum, disagreements, conf_when_wrong = {}, [], []
    confusion = Counter()

    for name, items in sorted(strata.items()):
        picked = rng.sample(items, min(args.per_stratum, len(items)))
        agree = 0
        for sha, prose, la, prob in picked:
            lb_obj = lingua.detect_language_of(prose) if prose else None
            lb = lb_obj.iso_code_639_1.name.lower() if lb_obj else "und"
            ok = (la == lb)
            agree += ok
            if not ok:
                confusion[(la, lb)] += 1
                conf_when_wrong.append(prob)
                disagreements.append({
                    "stratum": name, "file_sha": sha,
                    "langid": la, "langid_conf": round(prob, 4), "lingua": lb,
                    "prose_len": len(prose),
                    "excerpt": prose[:200],
                })
        per_stratum[name] = {
            "n": len(picked), "agree": agree,
            "agreement": round(agree / len(picked), 3) if picked else None,
        }
        print(f"  {name:18s} n={len(picked):>3}  concordancia={per_stratum[name]['agreement']}")

    tot_n = sum(v["n"] for v in per_stratum.values())
    tot_a = sum(v["agree"] for v in per_stratum.values())
    out["per_stratum"] = per_stratum
    out["overall"] = {"n": tot_n, "agree": tot_a,
                      "agreement": round(tot_a / tot_n, 4) if tot_n else None}
    out["top_confusions"] = [
        {"langid": a, "lingua": b, "n": n} for (a, b), n in confusion.most_common(15)
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
