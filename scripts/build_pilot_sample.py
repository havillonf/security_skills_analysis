#!/usr/bin/env python3
"""
EXP-005 - Amostra do piloto de anotacao (~50 casos).

NATUREZA: piloto de VIABILIDADE e teste do instrumento. NAO estima prevalencia,
NAO mede desempenho definitivo. A amostra e deliberadamente informativa, com
sobre-amostragem de situacoes dificeis - nao reproduz a distribuicao da populacao.

SINAL PRELIMINAR DE SEGURANCA
Nao existe classificador validado. Por isso o eixo de estratificacao NAO e
"classe prevista", e sim um SINAL PRELIMINAR calculado apenas com informacao ja
existente (EXP-002, front matter, lexico, has_scripts). O sinal:
  - serve exclusivamente para diversificar o piloto;
  - NAO e rotulo, NAO e ground truth;
  - NAO pode aparecer depois como evidencia de validade do classificador.

Tiers, avaliados EM ORDEM (logo, mutuamente exclusivos - formam particao):
  T3 forte : declaracao explicita de dominio, OU front matter + densidade >= 3
  T2 medio : front matter de seguranca, OU densidade >= 6
  T1 fraco : densidade entre 1 e 5
  T0 nulo  : densidade 0, sem front matter de seguranca, sem declaracao

GRUPOS LINGUISTICOS (EXP-003, EXP-004)
  L1 en | L2 zh | L3 ja+ko | L4 de/es/pt/fr/it | L5 cauda+und+mixed
  Detector primario: lingua. Segundo detector: py3langid (so registrado).
  L5 nao e subdividido: a concordancia entre detectores ali e 0,667.

SAIDAS
  results/EXP-005_pilot_sample.parquet      amostra congelada (gitignored)
  results/EXP-005_annotation_form.csv       formulario CEGO, campos humanos VAZIOS
  results/EXP-005_strata_key.csv            chave de estratos - NAO abrir antes
  results/EXP-005_sample_composition.json   composicao e tamanhos dos tiers
  results/EXP-005_reading_pack.md           texto para leitura (gitignored)

Uso:
    uv run --with duckdb --with py3langid --with lingua-language-detector \
        python scripts/build_pilot_sample.py
"""

import argparse
import csv
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

SEED = 20260822          # seed unica desta amostra; mudar invalida a reproducao
NONLATIN_CHAR = ("[\u4e00-\u9fff\u3400-\u4dbf\u3040-\u309f\u30a0-\u30ff"
                 "\uac00-\ud7af\u0400-\u04ff\u0600-\u06ff\u0590-\u05ff"
                 "\u0900-\u097f\u0e00-\u0e7f]")
MIXED_MIN_SHARE = 0.15   # a lingua minoritaria precisa de >= 15% do texto
MIXED_MIN_CHARS = 40     # e de massa absoluta minima dos dois lados
MIXED_MIN_WORDS = 20
POOL_PER_TIER = 900      # pool deterministico por tier, antes da deteccao de idioma
TARGET_N = 50

# --- Lexico estrito ---------------------------------------------------------
# Deliberadamente SEM os termos de alto ruido medidos em EXP-001
# (token 20,69%, audit 16,24%, permission 10,07%, sandbox, safety, validate).
STRICT_TERMS = [
    "security", "secure", "vulnerab", "exploit", "malware", "ransomware",
    "pentest", "penetration test", "red team", "owasp", "cve-", "cwe-",
    "injection", "xss", "csrf", "ssrf", "sanitiz", "hardening",
    "threat model", "least privilege", "encrypt", "decrypt", "cryptograph",
    "secret scanning", "credential", "iam", "rbac", "authentication",
    "authorization", "prompt injection", "jailbreak", "guardrail",
    "supply chain", "sbom", "sast", "dast", "forensic", "incident response",
]

DOMAIN_DECL = [
    "domain: cybersecurity", "domain: security",
    "category: cybersecurity", "category: security",
]

# Sinalizadores de caso dificil - flags, NAO rotulos
GRC_TERMS = [
    "vendor", "compliance", "questionnaire", "governance", "regulatory",
    "iso 27001", "soc 2", "hipaa", "gdpr", "lgpd", "sox", "third-party risk",
    "risk register", "control framework",
]


def like_any(col, terms):
    return " OR ".join(f"{col} LIKE '%{t}%'" for t in terms)


def lang_group(lang):
    if lang == "en":
        return "L1"
    if lang == "zh":
        return "L2"
    if lang in ("ja", "ko"):
        return "L3"
    if lang in ("de", "es", "pt", "fr", "it"):
        return "L4"
    return "L5"          # cauda, und, mixed, e o artefato 'la'


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default=str(DEFAULT_DATA_DIR))
    ap.add_argument("--pool-per-tier", type=int, default=POOL_PER_TIER)
    ap.add_argument("--target-n", type=int, default=TARGET_N)
    ap.add_argument("--skip-tier-sizes", action="store_true",
                    help="pula a contagem dos tiers na populacao (etapa cara)")
    args = ap.parse_args()

    art = Path(args.data_dir) / "artifacts"
    if not list(art.glob("*.parquet")):
        print(f"ERRO: nenhum Parquet em {art}", file=sys.stderr)
        return 1

    try:
        from py3langid.langid import LanguageIdentifier, MODEL_FILE
        from lingua import LanguageDetectorBuilder
    except ImportError as e:
        print(f"ERRO: dependencia ausente ({e})", file=sys.stderr)
        return 1

    ident = LanguageIdentifier.from_pickled_model(MODEL_FILE, norm_probs=True)
    lingua = LanguageDetectorBuilder.from_all_languages().build()

    A = f"read_parquet('{(art / '*.parquet').as_posix()}')"
    con = duckdb.connect()
    con.execute("SET enable_progress_bar=false")
    con.execute("SET memory_limit='6GB'")
    con.execute("SET temp_directory='C:/Users/victo/AppData/Local/Temp/duckdb_tmp'")
    W = "dedup_primary = 1 AND content IS NOT NULL"

    # Anti-circularidade: as ancoras do Codebook foram escritas a partir da
    # amostra de descoberta de EXP-002. Reaproveitar aqueles mesmos casos no
    # piloto mediria a regra contra os exemplos que a originaram.
    exp002 = RESULTS_DIR / "EXP-002_sample.parquet"
    excluded = []
    if exp002.exists():
        excluded = [r[0] for r in con.execute(
            f"SELECT DISTINCT file_sha FROM read_parquet('{exp002.as_posix()}')"
        ).fetchall()]
        lst = ", ".join(f"'{s}'" for s in excluded)
        W += f" AND file_sha NOT IN ({lst})"
        print(f"excluindo {len(excluded)} file_sha ja usados em EXP-002")

    density = " + ".join(
        f"CASE WHEN lower(content) LIKE '%{t}%' THEN 1 ELSE 0 END"
        for t in STRICT_TERMS
    )
    fm = like_any("lower(coalesce(name,'') || ' ' || coalesce(description,''))",
                  STRICT_TERMS)
    dom = like_any("lower(content)", DOMAIN_DECL)
    grc = like_any("lower(content)", GRC_TERMS)

    # Sinais calculados UMA vez; o tier deriva deles.
    # Antes o CASE repetia a expressao de densidade 3x (38 LIKEs cada) e o
    # DuckDB estourava a memoria sobre 1,88M documentos.
    signals_sql = f"""
        SELECT file_sha, repo_full_name, path, name, description,
               body_chars, has_scripts, content,
               ({density}) AS kw_density,
               CASE WHEN ({dom}) THEN 1 ELSE 0 END AS domain_decl,
               CASE WHEN ({fm})  THEN 1 ELSE 0 END AS fm_signal,
               CASE WHEN ({grc}) THEN 1 ELSE 0 END AS grc_flag
        FROM {A} WHERE {W}
    """
    # CASE ordenado => particao garantida por construcao
    TIER_CASE = """
        CASE
          WHEN domain_decl = 1 OR (fm_signal = 1 AND kw_density >= 3) THEN 'T3'
          WHEN fm_signal = 1 OR kw_density >= 6                       THEN 'T2'
          WHEN kw_density BETWEEN 1 AND 5                             THEN 'T1'
          ELSE 'T0'
        END
    """

    out = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "seed": SEED,
        "duckdb_version": duckdb.__version__,
        "target_n": args.target_n,
        "pool_per_tier": args.pool_per_tier,
        "natureza": "piloto de viabilidade - NAO estima prevalencia",
        "sinal_preliminar": {
            "descricao": "tier T0..T3 calculado so com dados existentes; nao e rotulo",
            "strict_terms": STRICT_TERMS,
            "domain_decl": DOMAIN_DECL,
            "regra": "CASE ordenado T3>T2>T1>T0, mutuamente exclusivo",
        },
        "grupos_linguisticos": {
            "L1": "en", "L2": "zh", "L3": "ja+ko",
            "L4": "de/es/pt/fr/it", "L5": "cauda+und+mixed",
        },
    }

    # --- tamanhos dos tiers na populacao (documentacao; nao e N_h do estimador) ---
    if not args.skip_tier_sizes:
        print("contando tiers na populacao (pode levar alguns minutos)...")
        rows = con.execute(f"""
            WITH s AS (
              SELECT ({density}) AS kw_density,
                     CASE WHEN ({dom}) THEN 1 ELSE 0 END AS domain_decl,
                     CASE WHEN ({fm})  THEN 1 ELSE 0 END AS fm_signal
              FROM {A} WHERE {W}
            )
            SELECT {TIER_CASE} AS tier, count(*) AS n
            FROM s GROUP BY 1 ORDER BY 1
        """).fetchall()
        total = sum(r[1] for r in rows)
        out["tier_sizes_population"] = [
            {"tier": t, "n": n, "pct": round(100 * n / total, 3)} for t, n in rows
        ]
        out["n_population"] = total
        for t, n in rows:
            print(f"  {t}: {n:>9,}  {100*n/total:6.2f}%")

    # --- pool deterministico por tier -------------------------------------
    print(f"\nmontando pool de {args.pool_per_tier} por tier...")
    pool = con.execute(f"""
        WITH s AS ({signals_sql}),
             tiered AS (SELECT *, {TIER_CASE} AS tier FROM s)
        SELECT * FROM tiered
        QUALIFY row_number() OVER (PARTITION BY tier ORDER BY hash(file_sha))
                <= {args.pool_per_tier}
    """).fetchall()
    cols = [d[0] for d in con.description]
    print(f"  pool: {len(pool)} registros")

    # --- deteccao de idioma sobre o pool ----------------------------------
    print("detectando idioma no pool...")
    recs = []
    for r in pool:
        d = dict(zip(cols, r))
        _fmtxt, body = split_frontmatter(d["content"])
        prose = clean_prose(body)

        lg = lingua.detect_language_of(prose) if len(prose) >= 20 else None
        lang_primary = lg.iso_code_639_1.name.lower() if lg else "und"
        if len(prose) >= 40:
            la, prob = ident.classify(prose)
        else:
            la, prob = "und", 0.0
        if la == "la":            # artefato conhecido (EXP-004)
            la = "und"

        # `mixed` conforme Codebook R-9: exige prosa SUBSTANTIVA em >= 2 linguas.
        # Um termo tecnico ingles solto NAO basta - a versao anterior usava
        # `n_scripts >= 1 and has_ascii`, que marcava praticamente todo texto CJK
        # como mixed e o mandava para L5, esvaziando L2/L3 e corrompendo N_h.
        n_nonlatin = len(re.findall(NONLATIN_CHAR, prose))
        n_latin_words = len(re.findall(r"[A-Za-z]{3,}", prose))
        n_latin_chars = sum(len(w) for w in re.findall(r"[A-Za-z]{3,}", prose))
        tot = max(n_nonlatin + n_latin_chars, 1)
        minor = min(n_nonlatin, n_latin_chars) / tot
        # ambos os lados precisam de massa: >= 15% do texto e >= 20 palavras/chars
        is_mixed = bool(minor >= MIXED_MIN_SHARE
                        and n_nonlatin >= MIXED_MIN_CHARS
                        and n_latin_words >= MIXED_MIN_WORDS)

        d["prose"] = prose
        d["nonlatin_chars"] = n_nonlatin
        d["latin_words"] = n_latin_words
        d["minor_share"] = round(minor, 4)
        d["lang_primary"] = lang_primary
        d["lang_secondary"] = la
        d["lang_secondary_conf"] = round(float(prob), 4)
        d["detector_agreement"] = int(lang_primary == la)
        d["is_mixed"] = int(is_mixed)
        # is_mixed NAO sobrescreve o grupo: zh/ja/ko continuam em L2/L3.
        # `mixed` e um ATRIBUTO transversal, nao um grupo linguistico.
        d["lang_group"] = lang_group(lang_primary)
        d["code_review_flag"] = int(bool(re.search(
            r"review", (d["name"] or "") + " " + (d["path"] or ""), re.I)))
        recs.append(d)

    by_key = defaultdict(list)
    for d in recs:
        by_key[(d["tier"], d["lang_group"])].append(d)
    for v in by_key.values():
        v.sort(key=lambda x: x["file_sha"])

    # --- selecao por cotas -------------------------------------------------
    # Cotas escolhidas para COBRIR L1..L5 e sobre-amostrar dificuldade.
    # Nao reproduzem a distribuicao da populacao - e um piloto, nao uma estimativa.
    quotas = [
        ("T3", "L1", 4), ("T3", "L2", 2), ("T3", "L3", 1), ("T3", "L4", 1), ("T3", "L5", 2),
        ("T2", "L1", 5), ("T2", "L2", 2), ("T2", "L3", 1), ("T2", "L4", 2), ("T2", "L5", 2),
        ("T1", "L1", 5), ("T1", "L2", 2), ("T1", "L3", 1), ("T1", "L4", 2), ("T1", "L5", 2),
        ("T0", "L1", 4), ("T0", "L2", 2), ("T0", "L3", 1), ("T0", "L4", 1), ("T0", "L5", 2),
    ]
    rng = random.Random(SEED)
    chosen, seen = [], set()
    # I-5: os reforcos dirigidos sao inseridos PRIMEIRO. Na versao anterior eles
    # entravam por ultimo e o corte `chosen[:target_n]` descartava justamente os
    # casos de fronteira SECONDARY/MENTION - o alvo declarado do piloto.

    def take(cands, k, reason):
        got = 0
        for d in cands:
            if got >= k:
                break
            if d["file_sha"] in seen:
                continue
            seen.add(d["file_sha"])
            d = dict(d)
            d["selection_reason"] = reason
            chosen.append(d)
            got += 1
        return got

    def targeted(pred, k, reason):
        cands = [d for d in recs if pred(d) and d["file_sha"] not in seen]
        cands.sort(key=lambda x: x["file_sha"])
        return take(rng.sample(cands, len(cands)), k, reason)

    # 1) reforcos dirigidos - vagas reservadas
    targeted_specs = [
        (lambda d: d["tier"] == "T1" and d["kw_density"] <= 2, 3,
         "dirigido fronteira SECONDARY/MENTION"),
        (lambda d: d["grc_flag"] == 1 and d["tier"] in ("T1", "T2", "T3"), 4,
         "dirigido GRC"),
        (lambda d: d["code_review_flag"] == 1, 4, "dirigido code-review"),
        (lambda d: d["is_mixed"] == 1, 3, "dirigido mixed"),
        (lambda d: d["lang_group"] == "L5", 2, "dirigido cauda"),
    ]
    targeted_got = {}
    for pred, k, reason in targeted_specs:
        targeted_got[reason] = targeted(pred, k, reason)

    # 2) cotas por tier x grupo, no espaco restante
    budget = args.target_n - len(chosen)
    scale = budget / sum(k for _, _, k in quotas) if quotas else 0
    for tier, lg, k in quotas:
        if len(chosen) >= args.target_n:
            break
        kk = max(1, round(k * scale))
        cands = by_key.get((tier, lg), [])
        take(rng.sample(cands, len(cands)), min(kk, args.target_n - len(chosen)),
             f"cota {tier}x{lg}")

    # 3) completar se sobrou vaga, sem quebrar a exclusao de EXP-002
    if len(chosen) < args.target_n:
        rest = [d for d in recs if d["file_sha"] not in seen]
        rest.sort(key=lambda x: x["file_sha"])
        take(rng.sample(rest, len(rest)), args.target_n - len(chosen), "completar")

    out["targeted_obtidos"] = targeted_got
    if len(chosen) != args.target_n:
        print(f"AVISO: selecionados {len(chosen)} != alvo {args.target_n}")

    for i, d in enumerate(sorted(chosen, key=lambda x: x["file_sha"]), 1):
        d["case_id"] = f"P{i:03d}"
    chosen.sort(key=lambda x: x["case_id"])

    # --- composicao --------------------------------------------------------
    comp = {
        "n_selected": len(chosen),
        "por_tier": dict(Counter(d["tier"] for d in chosen)),
        "por_grupo_linguistico": dict(Counter(d["lang_group"] for d in chosen)),
        "por_tier_x_grupo": {f"{tt}x{gg}": c for (tt, gg), c in
                             Counter((x["tier"], x["lang_group"])
                                     for x in chosen).items()},
        "por_motivo_selecao": dict(Counter(d["selection_reason"] for d in chosen)),
        "idioma_detector_primario": dict(Counter(d["lang_primary"] for d in chosen)),
        "n_grc_flag": sum(d["grc_flag"] for d in chosen),
        "n_code_review_flag": sum(d["code_review_flag"] for d in chosen),
        "n_mixed": sum(d["is_mixed"] for d in chosen),
        "n_L5": sum(1 for d in chosen if d["lang_group"] == "L5"),
        "n_detector_disagreement": sum(1 for d in chosen
                                       if d["detector_agreement"] == 0),
        "n_has_scripts": sum(1 for d in chosen if d["has_scripts"] == 1),
    }
    out["composicao"] = comp
    out["excluded_exp002_shas"] = len(excluded)

    # --- artefatos ---------------------------------------------------------
    RESULTS_DIR.mkdir(exist_ok=True)

    # ---- CEGAMENTO (C-3) --------------------------------------------------
    # O formulario entregue ao anotador NAO pode conter o sinal de triagem.
    # Mostrar tier/kw_density/flags antes da leitura ancora o julgamento humano,
    # e o vies ficaria CORRELACIONADO com a probabilidade de selecao - a unica
    # falha que D-014 admite ser capaz de destruir a validade do estimador.
    # A chave de estratos fica em arquivo separado, unido por case_id SOMENTE
    # depois de a anotacao estar fechada.
    blind_cols = ["case_id", "name", "body_chars"]
    human_cols = ["human_language", "used_translation", "security_relevance",
                  "security_focus", "operational_security", "operation_level",
                  "security_functions", "security_concerns",
                  "operational_capability", "evidence", "confidence",
                  "rule_applied", "grc_case", "secondary_mention_boundary",
                  "annotation_seconds", "difficulty", "note"]
    key_cols = ["case_id", "file_sha", "repo_full_name", "path",
                "tier", "kw_density", "domain_decl", "fm_signal", "grc_flag",
                "code_review_flag", "lang_group", "lang_primary",
                "lang_secondary", "lang_secondary_conf", "detector_agreement",
                "is_mixed", "minor_share", "has_scripts", "selection_reason"]

    form = RESULTS_DIR / "EXP-005_annotation_form.csv"
    with open(form, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(blind_cols + human_cols)
        for d in chosen:
            # campos humanos VAZIOS por construcao - nunca preenchidos por LLM
            w.writerow([d.get(c, "") for c in blind_cols] + [""] * len(human_cols))

    key = RESULTS_DIR / "EXP-005_strata_key.csv"
    with open(key, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(key_cols)
        for d in chosen:
            w.writerow([d.get(c, "") for c in key_cols])

    con.execute("CREATE TEMP TABLE sel (case_id VARCHAR, file_sha VARCHAR)")
    con.executemany("INSERT INTO sel VALUES (?, ?)",
                    [(d["case_id"], d["file_sha"]) for d in chosen])
    sample_path = RESULTS_DIR / "EXP-005_pilot_sample.parquet"
    con.execute(f"COPY (SELECT * FROM sel) TO '{sample_path.as_posix()}' (FORMAT PARQUET)")

    pack = [
        "# EXP-005 — Reading pack do piloto (CEGO)",
        "",
        "Texto truncado em 2500 caracteres, para leitura durante a anotação.",
        "**Não versionado** (reproduz texto de terceiros; regenerável pelo script).",
        "",
        "> **Este pacote é deliberadamente cego.** Não traz tier, densidade de",
        "> keyword, grupo linguístico, flags de GRC/code-review nem o motivo da",
        "> seleção. Esses campos existem em `EXP-005_strata_key.csv` e só devem ser",
        "> unidos por `case_id` **depois** de a anotação estar fechada. Ver o achado",
        "> C-3 da auditoria adversarial e a decisão D-021.",
        "",
        "Preencha `results/EXP-005_annotation_form.csv`.",
        "",
    ]
    for d in chosen:
        pack += [
            f"## {d['case_id']}", "",
            f"- name: `{d['name'] or '(sem front matter)'}`",
            f"- description: {(d['description'] or '(nenhuma)')[:300]}",
            f"- tamanho do corpo: {d['body_chars']} caracteres",
            "", "```markdown", (d["content"] or "")[:2500].strip(), "```", "",
        ]
    (RESULTS_DIR / "EXP-005_reading_pack.md").write_text(
        "\n".join(pack), encoding="utf-8")

    (RESULTS_DIR / "EXP-005_sample_composition.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False, default=str), encoding="utf-8")

    print(f"\nselecionados: {len(chosen)}")
    print("  por tier:", comp["por_tier"])
    print("  por grupo:", comp["por_grupo_linguistico"])
    print("  GRC:", comp["n_grc_flag"], "| code-review:", comp["n_code_review_flag"],
          "| mixed:", comp["n_mixed"], "| L5:", comp["n_L5"],
          "| detectores discordam:", comp["n_detector_disagreement"])
    print(f"\nOK -> {form.name} (CEGO), EXP-005_strata_key.csv, "
          f"EXP-005_pilot_sample.parquet, EXP-005_reading_pack.md, "
          f"EXP-005_sample_composition.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
