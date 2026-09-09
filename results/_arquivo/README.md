# `results/_arquivo/` — saídas fora do caminho crítico

> [!important] Arquivado ≠ irrelevante ≠ falso
> Nada aqui foi descartado por estar errado. Estes arquivos saíram da raiz de
> `results/` porque a etapa que os produziu terminou, ou porque o esquema que
> os gerou foi substituído. **Vários continuam citáveis** — a coluna "o que
> ainda vale" diz o quê. Mesma convenção de `notes/_arquivo/`.

Os scripts que produzem estes arquivos apontam para cá pela constante
`ARCHIVE_DIR = RESULTS_DIR / "_arquivo"`: **reexecutar um deles reescreve o
arquivo no lugar**, não cria cópia órfã na raiz. Saída nova de etapa nova
recebe um `EXP-XXX` novo e vai para a raiz.

---

## 1. Etapas concluídas

### EXP-001 · perfil do dataset

| Arquivo | O que é |
|---|---|
| `EXP-001_profile.json` | Contagens canônicas da população (1.877.981 representantes), frequência de keywords, integridade das chaves |

`scripts/profile_dataset.py`. **O que ainda vale:** os denominadores canônicos
— são a fonte dos números declarados em `.claude/skills/data-analysis` e a base
de D-001/D-002.

### EXP-002 · quadro de candidatos

| Arquivo | O que é |
|---|---|
| `EXP-002_frame.json` | Tamanho do pool e dos estratos do retrieval por keyword |
| `EXP-002_sample.parquet` | Amostra estratificada determinística *(gitignored)* |
| `EXP-002_sample_preview.md` | Texto truncado para open coding *(gitignored)* |

`scripts/build_candidate_frame.py` → consumido por `build_pilot_sample.py`.
**O que ainda vale:** que recuperação ampla por keyword atinge 78,69% da
população — foi esse número que descartou o filtro por keyword.

### EXP-003 / EXP-004 · idioma

| Arquivo | O que é |
|---|---|
| `EXP-003_languages.json` | Distribuição de idiomas na população (14,21% ± 0,48 pp não inglês) |
| `EXP-004_langdetect_validation.json` | Concordância entre detectores (0,987 global) |
| `EXP-004_disagreements.json` | Os casos em que os detectores divergem, com trecho |

`scripts/detect_languages.py`, `scripts/validate_language_detection.py`.
**O que ainda vale:** a linhagem do denominador — 14,21% pela detecção de
idioma dominante contra 16,333% pela detecção por parágrafo do EXP-013; a
diferença **é** o efeito da correção.

### EXP-005 · piloto de anotação humana (gold set v1)

| Arquivo | O que é |
|---|---|
| `EXP-005_annotation_form.csv` | Formulário **cego** original, campos vazios |
| `EXP-005_annotation_form_filled_updated.csv` | **Gold set preenchido** — insumo do classificador |
| `EXP-005_strata_key.csv` | Chave de estratos — **não abrir antes de anotar** |
| `EXP-005_sample_composition.json` | Composição e tamanho dos tiers |
| `EXP-005_annotation_example.csv` | Exemplo preenchido, uma linha, para ilustrar formato |
| `EXP-005_pilot_sample.parquet` | Amostra congelada *(gitignored)* |
| `EXP-005_reading_pack.md` | Texto das skills para leitura *(gitignored)* |

`scripts/build_pilot_sample.py` → consumido por `build_training_frame.py` e
`train_security_classifier.py`, que continuam lendo o gold set **daqui**.

> [!warning] `EXP-005_annotation_example.csv` está no esquema **v2.3**
> Traz colunas que a v2.5 eliminou (`security_focus`, `operational_security`,
> `operation_level`, `rule_applied`, `secondary_mention_boundary`) e a classe
> `MENTION`. Continua válido como registro do que foi anotado então —
> **não** use como modelo de preenchimento hoje.

### EXP-012 · classificador de triagem

| Arquivo | O que é |
|---|---|
| `EXP-012_metrics.json` | Métricas por classe e para a dicotomia, com IC |
| `EXP-012_classifier_comparison.csv` | Comparação entre os modelos testados |
| `EXP-012_confusion_matrix.csv` | Matriz de confusão do modelo escolhido |
| `EXP-012_population_summary.json` | Agregado da aplicação à população inteira |
| `EXP-012_uncertain_cases_sample.csv` | Amostra de casos de baixa confiança |
| `EXP-012_training_frame.parquet` | Quadro de treino *(gitignored)* |
| `EXP-012_population_classification.parquet` | 1,88M linhas, **97 MB** *(gitignored)* |

`scripts/train_security_classifier.py`, `scripts/classify_population.py`,
`scripts/evaluate_security_classifier.py`.

> A contagem de positivos deste classificador **não é a prevalência** — ela
> forma os estratos do Desenho C (D-014).

---

## 2. EXP-013 sob o Codebook v2.3 — esquema substituído

Arquivado em 2026-09-03, quando o [[Codebook]] passou para a **v2.4**
([[Decision Log#D-027]]). **Não são saídas ativas de nenhum experimento em
curso** — o esquema de classificação que as produziu foi substituído.

### Por que não foram apagadas

1. **São a evidência empírica de D-027 e D-028.** Todos os números citados
   nessas decisões saem daqui: Fleiss' κ=0,370 na dicotomia da QI-1,
   κ=0,942 em `security_focus`, κ=0,298 em `operational_security`,
   κ=0,070 em `confidence`; as contagens `PRIMARY` 6/6/7 contra
   `SECONDARY` 25/7/8; os 32 casos que viram o bucket SECURITY/NOT; a
   decomposição por fronteira (20 em `NONE`↔`SECONDARY` contra 7 em
   `MENTION`↔`SECONDARY`). Sem os arquivos, viram afirmação não
   verificável.
2. **A saída do Gemini é irrecuperável** — 91 classificações produzidas
   com cota que foi esgotada. Não podem ser regeradas.
3. **São a linha de base do re-teste.** A comparação v2.3 → v2.4 exige o
   κ de duas vias entre Opus e GPT **sob a v2.3**, calculado a partir
   destes arquivos.

### Conteúdo

| Arquivo | O que é |
|---|---|
| `EXP-013_classifications_gpt.jsonl` | Saída bruta do GPT, 100/100 casos |
| `EXP-013_claude_output.jsonl` | Saída bruta do Claude, 100/100 casos |
| `EXP-013_llm_cases_output_gemini.jsonl` | Saída bruta do Gemini, **91/100** — faltam `LLM066`–`LLM074` (nunca gerados) e 26 casos têm schema truncado |
| `EXP-013_consensus_labels.jsonl` | Derivado: casos unânimes |
| `EXP-013_discordant_cases.jsonl` | Derivado: casos para adjudicação |
| `EXP-013_comparison_report.jsonl` | Derivado: trilha de auditoria, todo caso |
| `EXP-013_aggregation_summary.json` | Derivado: contagens |
| `EXP-013_adjudication_form.csv` | Formulário cego dos 78 casos (adjudicação **suspensa** — era sob a v2.3) |

Os cinco derivados são regeneráveis a partir dos três primeiros com
`scripts/aggregate_llm_classifications.py`. **Atenção:** o script hoje
implementa a regra da v2.4 (`confidence` e `rule_applied` fora da
comparação), então uma reexecução **não** reproduz exatamente os números
originais de D-026 — reproduz 31 unânimes, não 22.

### O que NÃO usar isto para

- Não usar como rótulo de treino nem como gold set: são de um esquema
  substituído.
- Não comparar diretamente com as saídas da v2.4 caso a caso sem
  explicitar que as classes mudaram (`MENTION` e `AMBIGUOUS` deixaram de
  existir; `SECONDARY` passou a ser inclusivo).

Ver [[EXP-013]], [[Decision Log#D-027]], [[Decision Log#D-028]] e
[[Classification Prompt]] (o prompt que os produziu).

---

Volta para o índice ativo: [`../README.md`](../README.md).
