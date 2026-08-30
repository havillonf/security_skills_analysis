#!/usr/bin/env python3
"""
EXP-003 - Distribuicao de idiomas da populacao de Agent Skills.

Desenho em duas camadas (notes/Methodology/Multilingual Strategy.md secao 2):

  Camada 1 - script Unicode sobre a POPULACAO INTEIRA (1.877.981 representantes).
             Barato, exato, sem modelo. Da o piso de conteudo nao latino.
  Camada 2 - identificacao de idioma sobre AMOSTRA ALEATORIA deterministica.
             Necessaria porque a camada 1 nao separa idiomas de escrita latina.

Pre-processamento antes de detectar (o texto cru enganaria o detector):
  1. remove front matter YAML (analisado a parte)
  2. remove blocos de codigo cercados e codigo inline
  3. remove URLs, caminhos e nomes de arquivo
  4. so entao identifica o idioma da prosa restante

Nada e descartado por idioma. Baixa confianca -> "und", nunca um palpite.

Uso:
    uv run --with duckdb --with py3langid python scripts/detect_languages.py
    uv run --with duckdb --with py3langid python scripts/detect_languages.py --sample 30000
"""

import argparse
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_DIR = ROOT / "data" / "raw" / "gitskills" / "data"
RESULTS_DIR = ROOT / "results"

# --- Camada 1: blocos Unicode -----------------------------------------------
# Presenca de caractere do bloco => o texto contem aquele script.
SCRIPTS = {
    "han":        r"[一-鿿㐀-䶿]",       # chines / kanji
    "hiragana":   r"[぀-ゟ]",                     # japones
    "katakana":   r"[゠-ヿ]",                     # japones
    "hangul":     r"[가-힯ᄀ-ᇿ]",        # coreano
    "cyrillic":   r"[Ѐ-ӿ]",                     # russo, ucraniano...
    "arabic":     r"[؀-ۿݐ-ݿ]",
    "hebrew":     r"[֐-׿]",
    "devanagari": r"[ऀ-ॿ]",                     # hindi, marathi...
    "greek":      r"[Ͱ-Ͽ]",
    "thai":       r"[฀-๿]",
    "latin_ext":  r"[À-ɏ]",                     # acentos: pt, es, fr, de...
}

# --- Pre-processamento -------------------------------------------------------
RE_FRONTMATTER = re.compile(r"\A---\r?\n.*?\r?\n---\r?\n", re.S)
RE_FENCE = re.compile(r"```.*?```|~~~.*?~~~", re.S)
RE_INLINE_CODE = re.compile(r"`[^`\n]*`")
RE_URL = re.compile(r"https?://\S+|www\.\S+")
RE_PATH = re.compile(r"[\w./~-]*/[\w./-]+|\b[\w-]+\.(?:md|py|js|ts|json|yaml|yml|sh|toml)\b")
RE_HTML = re.compile(r"<[^>]+>")
RE_MDLINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
RE_WS = re.compile(r"\s+")


def split_frontmatter(text: str) -> tuple[str, str]:
    """Devolve (front matter, corpo). Front matter pode divergir do corpo."""
    m = RE_FRONTMATTER.match(text)
    if not m:
        return "", text
    return m.group(0), text[m.end():]


def clean_prose(text: str) -> str:
    """Remove tudo que nao e prosa antes de identificar o idioma."""
    text = RE_FENCE.sub(" ", text)
    text = RE_INLINE_CODE.sub(" ", text)
    text = RE_MDLINK.sub(r"\1", text)
    text = RE_URL.sub(" ", text)
    text = RE_PATH.sub(" ", text)
    text = RE_HTML.sub(" ", text)
    return RE_WS.sub(" ", text).strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default=str(DEFAULT_DATA_DIR))
    ap.add_argument("--sample", type=int, default=20000,
                    help="tamanho da amostra da camada 2 (default 20000)")
    ap.add_argument("--min-chars", type=int, default=40,
                    help="prosa menor que isso -> 'und' (default 40)")
    ap.add_argument("--min-prob", type=float, default=0.90,
                    help="confianca minima do detector, 0-1 (default 0.90)")
    ap.add_argument("--skip-layer1", action="store_true",
                    help="reaproveita a camada 1 do JSON existente (ela e cara)")
    args = ap.parse_args()

    art = Path(args.data_dir) / "artifacts"
    if not list(art.glob("*.parquet")):
        print(f"ERRO: nenhum Parquet em {art}", file=sys.stderr)
        return 1

    A = f"read_parquet('{(art / '*.parquet').as_posix()}')"
    con = duckdb.connect()
    con.execute("SET enable_progress_bar=false")
    W = "dedup_primary = 1 AND content IS NOT NULL"

    out = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "duckdb_version": duckdb.__version__,
        "params": {"sample": args.sample, "min_chars": args.min_chars,
                   "min_prob": args.min_prob},
    }

    n_pop = con.execute(f"SELECT count(*) FROM {A} WHERE {W}").fetchone()[0]
    out["n_population"] = n_pop
    print(f"populacao: {n_pop:,} representantes\n")

    # === Camada 1: scripts Unicode sobre a populacao inteira =================
    prev_path = RESULTS_DIR / "EXP-003_languages.json"
    if args.skip_layer1 and prev_path.exists():
        prev = json.loads(prev_path.read_text(encoding="utf-8"))
        out["layer1_scripts"] = prev["layer1_scripts"]
        out["layer1_reused_from"] = prev.get("generated_at")
        print("=== Camada 1: reaproveitada do JSON anterior ===")
        for name, d in out["layer1_scripts"].items():
            print(f"  {name:22s} {d['n']:>9,}  {d['pct']:6.2f}%")
        _skip1 = True
    else:
        _skip1 = False
    if not _skip1:
      print("=== Camada 1: scripts Unicode (populacao inteira) ===")
      parts = ", ".join(
          f"sum(CASE WHEN regexp_matches(content, '{pat}') THEN 1 ELSE 0 END) AS s_{name}"
          for name, pat in SCRIPTS.items()
      )
      nonlatin = " OR ".join(
          f"regexp_matches(content, '{pat}')"
          for name, pat in SCRIPTS.items() if name != "latin_ext"
      )
      row = con.execute(f"""
          SELECT {parts},
                 sum(CASE WHEN {nonlatin} THEN 1 ELSE 0 END) AS any_nonlatin
          FROM {A} WHERE {W}
      """).fetchone()

      layer1 = {}
      for name, n in zip(list(SCRIPTS) + ["any_nonlatin_script"], row):
          layer1[name] = {"n": int(n), "pct": round(100 * n / n_pop, 3)}
          print(f"  {name:22s} {n:>9,}  {100*n/n_pop:6.2f}%")
      out["layer1_scripts"] = layer1

    # === Camada 2: identificacao de idioma sobre amostra aleatoria ==========
    print(f"\n=== Camada 2: idioma em amostra aleatoria (n={args.sample:,}) ===")
    try:
        from py3langid.langid import LanguageIdentifier, MODEL_FILE
    except ImportError:
        print("ERRO: py3langid ausente. Rode com --with py3langid", file=sys.stderr)
        return 1

    # norm_probs=True e OBRIGATORIO: sem isso classify() devolve log-probabilidade
    # (valores fora de [0,1]) e qualquer limiar de confianca vira lixo.
    identifier = LanguageIdentifier.from_pickled_model(MODEL_FILE, norm_probs=True)
    out["params"]["detector"] = "py3langid LanguageIdentifier(norm_probs=True)"

    rows = con.execute(f"""
        SELECT file_sha, content FROM {A}
        WHERE {W} ORDER BY hash(file_sha) LIMIT {args.sample}
    """).fetchall()

    body_lang, fm_lang, divergent, und_reason = Counter(), Counter(), 0, Counter()
    mixed_script = 0
    per_lang_conf = {}

    for sha, content in rows:
        fm, body = split_frontmatter(content)
        prose = clean_prose(body)

        # texto multilingue: mais de um script nao latino, ou nao latino + latino
        scripts_present = [n for n, p in SCRIPTS.items()
                           if n != "latin_ext" and re.search(p, prose)]
        has_ascii_words = bool(re.search(r"[A-Za-z]{4,}", prose))
        if len(scripts_present) > 1 or (scripts_present and has_ascii_words):
            mixed_script += 1

        if len(prose) < args.min_chars:
            body_lang["und"] += 1
            und_reason["prosa_curta"] += 1
        else:
            lang, prob = identifier.classify(prose)
            if prob < args.min_prob:
                body_lang["und"] += 1
                und_reason["baixa_confianca"] += 1
            else:
                body_lang[lang] += 1
                per_lang_conf.setdefault(lang, []).append(prob)

        fm_prose = clean_prose(fm)
        if len(fm_prose) >= args.min_chars:
            fl, fp = identifier.classify(fm_prose)
            fl = fl if fp >= args.min_prob else "und"
        else:
            fl = "und"
        fm_lang[fl] += 1

        bl = identifier.classify(prose)[0] if len(prose) >= args.min_chars else "und"
        if fl != "und" and bl != "und" and fl != bl:
            divergent += 1

    n = len(rows)
    out["layer2_sample_n"] = n
    out["layer2_body_language"] = [
        {"lang": l, "n": c, "pct": round(100 * c / n, 3),
         "mean_conf": round(sum(per_lang_conf[l]) / len(per_lang_conf[l]), 3)
         if l in per_lang_conf else None}
        for l, c in body_lang.most_common()
    ]
    out["layer2_frontmatter_language"] = [
        {"lang": l, "n": c, "pct": round(100 * c / n, 3)}
        for l, c in fm_lang.most_common(15)
    ]
    out["layer2_frontmatter_body_divergent"] = {
        "n": divergent, "pct": round(100 * divergent / n, 3)}
    out["layer2_mixed_script"] = {
        "n": mixed_script, "pct": round(100 * mixed_script / n, 3)}
    out["layer2_und_reasons"] = dict(und_reason)

    print(f"  {'idioma':10s} {'n':>7s} {'%':>7s}  conf.media")
    for d in out["layer2_body_language"][:15]:
        mc = f"{d['mean_conf']:.3f}" if d["mean_conf"] is not None else "-"
        print(f"  {d['lang']:10s} {d['n']:>7,} {d['pct']:>6.2f}%  {mc}")
    print(f"\n  front matter divergente do corpo: {divergent:,} ({100*divergent/n:.2f}%)")
    print(f"  texto com mistura de scripts:     {mixed_script:,} ({100*mixed_script/n:.2f}%)")
    print(f"  motivos de 'und': {dict(und_reason)}")

    RESULTS_DIR.mkdir(exist_ok=True)
    p = RESULTS_DIR / "EXP-003_languages.json"
    p.write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    print(f"\nOK -> {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
