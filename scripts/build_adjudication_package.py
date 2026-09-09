"""EXP-014 - Monta o PACOTE de adjudicacao humana: uma pasta autocontida com
os arquivos de caso que o pesquisador precisa ler, mais a procedencia de cada
um.

Motivo de existir: os 100 casos do ensemble ficam em
results/EXP-013_llm_cases/, que e gitignored (reproduz o SKILL.md inteiro de
100 repositorios de terceiros) e serve de DIRETORIO CEGO - o prompt manda o
avaliador ler tudo que estiver la. Nenhum dos dois papeis serve para a
auditoria humana, que precisa de:

  1. so os casos que exigem adjudicacao (nao os 100);
  2. versionados, para a auditoria ser reproduzivel e portavel entre maquinas;
  3. com procedencia explicita (repositorio de origem e licenca), ja que o
     conteudo e de terceiros.

Este script NAO toca no formulario. O formulario (EXP-014_adjudication_form.csv)
e preenchido a mao e regenera-lo apagaria o trabalho humano - por isso a
montagem do pacote vive aqui, e nao em build_adjudication_form.py.

Idempotente: rodar de novo sobrescreve as copias e a procedencia, nunca o
formulario.

Uso:
    uv run --with duckdb python scripts/build_adjudication_package.py
    uv run --with duckdb python scripts/build_adjudication_package.py --prefix EXP-014

Saidas:
    results/EXP-014_adjudication_cases/<case_id>.md   copias dos casos
    results/EXP-014_adjudication_cases/PROVENANCE.csv procedencia + licenca
    results/EXP-014_adjudication_cases/README.md      o que e e como usar
"""
from __future__ import annotations

import argparse
import csv
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = REPO_ROOT / "results"
SOURCE_CASES = RESULTS_DIR / "EXP-013_llm_cases"
ARTIFACTS = "read_parquet('data/raw/gitskills/data/artifacts/*.parquet')"
REPOS = "read_parquet('data/raw/gitskills/data/repos/*.parquet')"


def read_case_ids(form_path: Path) -> list[str]:
    with form_path.open(encoding="utf-8") as f:
        return [r["case_id"] for r in csv.DictReader(f) if r.get("case_id")]


def read_shas(sample_csv: Path, case_ids: set[str]) -> dict[str, str]:
    with sample_csv.open(encoding="utf-8") as f:
        return {r["case_id"]: r["file_sha"]
                for r in csv.DictReader(f) if r["case_id"] in case_ids}


def fetch_provenance(shas: dict[str, str]) -> list[dict]:
    """Junta cada caso ao repositorio de origem e a licenca declarada.

    A licenca importa: o conteudo copiado e de terceiros, e versiona-lo sem
    dizer de onde veio seria irresponsavel num trabalho academico.
    """
    import duckdb

    con = duckdb.connect()
    con.execute("SET enable_progress_bar=false")
    quoted = ", ".join(f"'{s}'" for s in shas.values())
    rows = con.execute(f"""
        SELECT a.file_sha, a.repo_full_name, a.path, r.license, r.stars
        FROM {ARTIFACTS} a
        LEFT JOIN {REPOS} r ON a.repo_full_name = r.full_name
        WHERE a.dedup_primary = 1 AND a.file_sha IN ({quoted})
    """).fetchall()
    by_sha = {r[0]: r for r in rows}
    by_case = {}
    for case_id, sha in shas.items():
        r = by_sha.get(sha)
        by_case[case_id] = {
            "case_id": case_id,
            "file_sha": sha,
            "repo_full_name": r[1] if r else "",
            "path": r[2] if r else "",
            "license": (r[3] if r and r[3] else "NAO DECLARADA") if r else "",
            "stars": r[4] if r else "",
        }
    return [by_case[c] for c in sorted(by_case)]


README = """# Casos para auditoria humana — {prefix}

Os **{n} casos** em que os avaliadores divergiram e que exigem decisão humana
([[Decision Log#D-026]]). Cada `<case_id>.md` traz o `SKILL.md` completo.

## Como usar

1. Abra `results/{prefix}_adjudication_form.csv`.
2. Para cada `case_id`, leia o arquivo correspondente **desta pasta**, do zero.
3. Classifique seguindo `notes/Instruments/Guia do Anotador Humano.md`
   (Codebook **v2.6**).

> [!danger] Não abra antes de decidir
> `{prefix}_gpt_output.jsonl`, `{prefix}_claude_output.jsonl` e
> `{prefix}_comparison_report.jsonl` contêm o rótulo dos modelos. Ver a
> saída deles antes de decidir contamina a adjudicação e invalida a
> independência que sustenta o D-026.

## Por que esta pasta existe, separada de `EXP-013_llm_cases/`

| | `EXP-013_llm_cases/` | esta pasta |
|---|---|---|
| Conteúdo | os 100 casos do ensemble | só os {n} que precisam de decisão humana |
| Git | gitignored | **versionada** |
| Papel | **diretório cego** — o prompt manda o modelo ler tudo dali | material de leitura do humano |

Nunca escreva saída dentro de `EXP-013_llm_cases/`. Esta pasta não tem esse
problema: nada aqui é lido por modelo nenhum de forma automática.

## Procedência

`PROVENANCE.csv` traz, por caso, o repositório de origem, o caminho do arquivo
e a **licença declarada** do repositório. O conteúdo é de terceiros, público no
GitHub, reproduzido aqui para tornar a auditoria verificável. Ao citar um caso
no texto do TCC, use essa tabela para atribuir corretamente.

Distribuição de licenças nesta pasta:

{license_table}

## Reprodutibilidade

Gerado por `scripts/build_adjudication_package.py`, a partir de
`{prefix}_adjudication_form.csv` e `EXP-013_llm_sample.csv`. O script é
idempotente e **nunca sobrescreve o formulário**.
"""


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--prefix", default="EXP-014")
    p.add_argument("--sample", default="EXP-013_llm_sample.csv")
    args = p.parse_args()

    form_path = RESULTS_DIR / f"{args.prefix}_adjudication_form.csv"
    if not form_path.exists():
        raise SystemExit(f"ERRO: {form_path.name} nao existe. "
                         "Rode antes scripts/build_adjudication_form.py")
    if not SOURCE_CASES.is_dir():
        raise SystemExit(
            f"ERRO: {SOURCE_CASES} nao existe. E gitignored e regeneravel por "
            "scripts/build_llm_ensemble_sample.py")

    case_ids = read_case_ids(form_path)
    out_dir = RESULTS_DIR / f"{args.prefix}_adjudication_cases"
    out_dir.mkdir(exist_ok=True)

    copiados, faltando = [], []
    for case_id in case_ids:
        src = SOURCE_CASES / f"{case_id}.md"
        if src.exists():
            shutil.copy2(src, out_dir / f"{case_id}.md")
            copiados.append(case_id)
        else:
            faltando.append(case_id)

    shas = read_shas(RESULTS_DIR / args.sample, set(case_ids))
    prov = fetch_provenance(shas)
    with (out_dir / "PROVENANCE.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["case_id", "file_sha", "repo_full_name",
                                          "path", "license", "stars"])
        w.writeheader()
        w.writerows(prov)

    counts: dict[str, int] = {}
    for r in prov:
        counts[r["license"] or "NAO DECLARADA"] = counts.get(r["license"] or "NAO DECLARADA", 0) + 1
    table = "\n".join(f"| `{k}` | {v} |" for k, v in sorted(counts.items(), key=lambda x: -x[1]))
    table = "| Licença | Casos |\n|---|---:|\n" + table

    (out_dir / "README.md").write_text(
        README.format(prefix=args.prefix, n=len(copiados), license_table=table),
        encoding="utf-8")

    print(f"{len(copiados)} casos copiados para results/{out_dir.name}/")
    if faltando:
        print(f"AVISO: sem arquivo de caso: {', '.join(faltando)}")
    print(f"procedencia: {len(prov)} linhas -> PROVENANCE.csv")
    print("licencas:", counts)


if __name__ == "__main__":
    main()
