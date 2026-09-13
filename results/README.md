# `results/` — índice das saídas

Toda saída citável do TCC vive aqui, com nome `EXP-XXX_<nome>.<ext>`, produzida
por um script de `scripts/` e explicada por uma nota de `notes/Experiments/`.
**Nada aqui é escrito à mão** — exceto os formulários de anotação, que existem
justamente para o humano preencher.

**A raiz só tem o caminho crítico** (EXP-013 → EXP-016). Tudo de etapa
concluída ou de esquema substituído está em [`_arquivo/`](_arquivo/README.md),
preservado e em boa parte ainda citável — mesma convenção de `notes/_arquivo/`.

> [!important] ⭐ Gold set pronto — `EXP-014_gold_set.csv` (99 casos)
> Adjudicação humana concluída em 2026-09-13 ([[Decision Log#D-031]]). Cada
> linha traz a origem do rótulo (`llm_consensus`, `human_agreement`,
> `human_agreement_after_marking_fix`, `human_reconciliation`) e as marcações de
> quadro. Contagens e estimativa **preliminar** em `EXP-014_gold_set_summary.json`.
>
> **Próxima etapa: E-7**, validar o LLM local do orientador contra este arquivo
> ([`notes/03 - Methodology.md`](../notes/03%20-%20Methodology.md)). **Congelar o
> gold set num commit antes** de qualquer modelo novo vê-lo.

---

## Como ler um nome de arquivo

`EXP-XXX` diz **qual experimento** produziu o arquivo, não em que ordem ele
deve ser lido. O sufixo diz o papel:

| Sufixo | Papel |
|---|---|
| `_summary.json`, `_profile.json`, `_metrics.json` | **agregado citável** — o número que vai para o texto |
| `_form.csv` | **formulário cego**, para o humano preencher |
| `_output.jsonl` | saída **bruta** de um avaliador (um objeto por caso) |
| `_report.jsonl`, `_labels.jsonl`, `_cases.jsonl` | **derivado**, regenerável a partir dos brutos |
| `_sample.parquet`, `_frame.parquet` | amostra/quadro congelado (grande, gitignored) |

Os CSVs da raiz, e a distinção entre eles:

| CSV na raiz | Papel |
|---|---|
| **`EXP-014_gold_set.csv`** | **o gold set** — 99 casos, rótulo final e origem |
| `EXP-014_adjudication_form.csv` | rótulo humano final dos 16 casos adjudicados |
| `EXP-014_adjudication_victor.csv` · `_havillon.csv` | anotação independente de cada pesquisador — **não editar** |
| `EXP-013_llm_sample.csv` | a amostra de 100 casos (metadados) |
| `EXP-013_llm_sample_rejected.csv` | rejeitados por idioma *(gitignored)* |
| `EXP-013_population_english_filter.csv` | filtro linha a linha, 95 MB *(gitignored)* |

Os demais formulários e matrizes em CSV são de etapas concluídas e estão em
`_arquivo/`.

---

## Índice — caminho crítico

### EXP-013 · amostra do ensemble de LLMs

| Arquivo | O que é |
|---|---|
| `EXP-013_llm_sample.csv` | **A amostra**: 100 casos (`case_id`, `file_sha`, `name`, `body_chars`) |
| `EXP-013_llm_sample_summary.json` | Composição da amostra e critério de aceitação |
| `EXP-013_llm_cases/` | 100 × `LLMxxx.md` com o SKILL.md inteiro *(gitignored)* |
| `EXP-013_llm_sample_rejected.csv` | Rejeitados por idioma, com trecho *(gitignored)* |
| `EXP-013_population_english_filter.csv` | Filtro linha a linha, 1,88M registros, **95 MB** *(gitignored)* |
| `EXP-013_population_english_filter_summary.json` | O agregado citável: 83,67% puramente inglês |

`scripts/build_llm_ensemble_sample.py`, `scripts/filter_population_english.py`.

> [!danger] `EXP-013_llm_cases/` é o diretório **cego**
> O prompt manda o avaliador ler *tudo* que estiver ali. **Nunca escrever saída
> dentro dele** — um arquivo de output nesse diretório fica visível para o
> avaliador seguinte. Já aconteceu uma vez (ver ressalva no EXP-014 abaixo).

### EXP-014 · re-teste do instrumento, adjudicação e gold set ✅

| Arquivo | O que é | n |
|---|---|---|
| `EXP-014_gpt_output.jsonl` | Saída bruta do GPT | 100 |
| `EXP-014_claude_output.jsonl` | Saída bruta do Claude (Opus) | 100 |
| `EXP-014_agreement.json` | Cohen's κ, Krippendorff's α, Gwet's AC1, Brennan-Prediger, PABAK, PI/BI, McNemar, IC bootstrap | — |
| `EXP-014_aggregation_summary.json` | 84 unânimes, 16 discordantes | — |
| `EXP-014_consensus_labels.jsonl` | Casos unânimes (derivado) | 84 |
| `EXP-014_discordant_cases.jsonl` | Casos para adjudicação (derivado) | 16 |
| `EXP-014_comparison_report.jsonl` | Trilha de auditoria, todo caso (derivado) | 100 |
| `EXP-014_adjudication_cases/` | Os 16 arquivos lidos na adjudicação + `PROVENANCE.csv` (repo de origem e licença) | 16 |
| `EXP-014_adjudication_victor.csv` · `_havillon.csv` | Anotação humana independente, um arquivo por pesquisador | 16 |
| `EXP-014_human_agreement_original.json` | Concordância humana na marcação original — **a que se reporta** | 16 |
| `EXP-014_human_agreement.json` | Idem, após corrigir 2 erros de marcação | 16 |
| `EXP-014_adjudication_form.csv` | Rótulo humano final (concordância ou reconciliação mútua) | 16 |
| **`EXP-014_gold_set.csv`** | **Gold set consolidado**, no quadro do EXP-016 | **99** |
| `EXP-014_gold_set_summary.json` | Contagens por classe e origem, marcações de quadro, estimativa preliminar | — |

`scripts/compute_agreement.py` (aceita `.jsonl` e `.csv`),
`scripts/aggregate_llm_classifications.py`, `scripts/build_adjudication_form.py`,
`scripts/build_adjudication_package.py`, `scripts/build_gold_set.py`.
Os derivados do agregador regeneram a partir dos dois brutos; o gold set
regenera a partir do formulário, dos arquivos individuais e do quadro.

> [!warning] Procedência quebrada em `EXP-014_agreement.json`
> O campo `rater_a.file` aponta para
> `results\EXP-013_llm_cases\classifications.jsonl` — caminho que **não existe
> mais**: era a saída do GPT escrita por engano dentro do diretório cego, hoje
> em `EXP-014_gpt_output.jsonl`. Os números do arquivo continuam válidos; só a
> trilha de procedência está desatualizada. Rodar `compute_agreement.py` de
> novo, apontando para o caminho atual, corrige.

### EXP-015 · artefatos gerados dentro do quadro amostral

| Arquivo | O que é |
|---|---|
| `EXP-015_frame_artifact_profile.json` | Quantos `SKILL.md` da população são **saída gerada** (relatório, log, dump) em vez de instrução: marcadores de procedência, estratos, regra testada e validação nos casos conhecidos (`LLM019`, `LLM067`) |

`scripts/profile_frame_artifacts.py` → [[EXP-015]], [[Decision Log#D-030]].
Mede o problema; **não** decide o quadro amostral.

### EXP-016 · quadro de análise — **o denominador da QI-1**

| Arquivo | O que é |
|---|---|
| `EXP-016_analysis_frame_summary.json` | A cascata das exclusões em sequência: 1.877.981 → 1.571.243 → **1.550.550** |
| `EXP-016_analysis_frame.parquet` | Rótulo por arquivo (motivo de exclusão + estrato de gênero), 45 MB *(gitignored)* |

`scripts/build_analysis_frame.py` → [[EXP-016]]. Consome
`EXP-013_population_english_filter.csv`; se ele sumir, o script **para com
mensagem explícita** em vez de calcular um quadro errado.

> [!important] É aqui que sai o número de baixo da porcentagem
> Os percentuais de cada exclusão **se sobrepõem** — o limiar do D-028 remove
> 25.284 isolado, mas só 20.693 a mais depois do filtro de idioma. Somar
> marginais superestima. Use sempre este arquivo, nunca a soma.

---

## `_arquivo/` — o que saiu da raiz

| Bloco | O que tem |
|---|---|
| Etapas concluídas | EXP-001 (perfil), EXP-002 (quadro de candidatos), EXP-003/EXP-004 (idioma), EXP-005 (piloto e gold set v1), EXP-012 (classificador de triagem) |
| Rodada substituída | EXP-013 sob o Codebook **v2.3** (classes `MENTION` e `AMBIGUOUS`, que deixaram de existir) |

Índice detalhado, com o que ainda é citável de cada um:
[`_arquivo/README.md`](_arquivo/README.md).

> Cuidado ao procurar arquivo por nome: `_arquivo/` contém
> `EXP-013_adjudication_form.csv`, `EXP-013_claude_output.jsonl` e
> `EXP-013_comparison_report.jsonl` — homônimos quase exatos dos do EXP-014.
> **O da etapa atual é sempre `EXP-014_`, na raiz de `results/`.**

---

## Política de versionamento

| Bucket | Regra |
|---|---|
| **Versionado** | Agregados pequenos (`*.json`), matrizes, formulários de anotação, gold set |
| **Gitignored** | Parquet, reading packs, `EXP-013_llm_cases/`, CSVs > 10 MB — tudo regenerável de forma determinística por script |
| **Motivo recorrente** | O arquivo reproduz `SKILL.md` de terceiros (licença do repo de origem) ou é grande demais para o git |

Os globs do `.gitignore` usam `results/**/` justamente para continuar valendo
dentro de `_arquivo/` — mover um parquet para lá não o expõe.

> [!note] Lacuna conhecida
> As saídas do **EXP-013 (amostra) e do EXP-014 inteiro** não estão nem
> versionadas nem ignoradas — caem entre as duas políticas. São a evidência do
> κ que vai para o TCC e **deveriam ser versionadas**: os `*_output.jsonl`
> trazem trechos literais de terceiros no campo `evidence`, então isso é uma
> decisão do pesquisador, não automática. Enquanto não for resolvido, esses
> arquivos existem só nesta máquina.

## Ligações

`notes/Experiments/` (uma nota por EXP) · `notes/Decisions/Decision Log.md` ·
`notes/Instruments/Guia do Anotador Humano.md` · `scripts/`
