# Security Skills Analysis

Estudo empírico sobre a **prevalência de skills de segurança** na população pública de Agent Skills (`SKILL.md`) no GitHub, utilizando o dataset [GitSkills](https://zenodo.org/records/21875637).

> **Paper:** Destefanis, G., Graziotin, D., Vaccargiu, M., & Ortu, M. (2027). *GitSkills: A Dataset of Agent Skills on GitHub*. In MSR '27. [arXiv:2608.10906](https://arxiv.org/abs/2608.10906)

## Questão Central

> **QI-1:** Qual a prevalência de skills de segurança na população pública de Agent Skills?

Uma *agent skill* é um arquivo `SKILL.md` contendo instruções em linguagem natural para um agente LLM. O agente carrega a skill quando julga que a tarefa corresponde à descrição. Formato publicado pela Anthropic em outubro de 2025.

**Security Skill = `SEC-PRIMARY` + `SEC-SECONDARY`**, definida no [Codebook v2.3](notes/Decisions/Codebook.md), sempre reportadas separadamente. A classificação considera propósito, comportamento e artefatos — presença de vocabulário de segurança **nunca** basta.

## Estado Atual

O projeto está na etapa **E-5 (Piloto de anotação humana)**. Uma prova de conceito ponta a ponta (EXP-012) já foi executada: o pipeline completo de anotar → treinar → validar → classificar funciona. O número preliminar (**1,61%**) **não é a resposta** — é apenas a confirmação de que a infraestrutura está operacional.

| Etapa | Status | Descrição |
|---|---|---|
| E-0 Auditoria estrutural | ✅ | Integridade do dataset verificada; resultado anterior invalidado |
| E-1 Codebook | ✅ | Instrumento de anotação v2.3 definido |
| E-3 Idiomas | ✅ | ~14% da população não é em inglês (~267 mil conteúdos) |
| E-3b Validação detectores | ✅ | Concordância 0,987 entre `lingua` e `py3langid` |
| **E-5 Piloto** | ⬅ **AQUI** | Amostra de 50 casos gerada e preenchida (com ajuda de IA) |
| E-6 Gold set | ⬜ | Padrão-ouro humano com concordância |
| E-7 Classificador validado | ⬜ | Validação contra gold set por classe e por idioma |
| E-8–E-10 | ⬜ | Classificação da população → estimativa com IC → robustez |

## Estrutura do Projeto

```
security_skills_analysis/
├── data/                              # Cache local do dataset (gitignored)
├── models/                            # Classificadores treinados (gitignored, regeneráveis)
│   └── security_classifier_v1_metadata.json
├── notebooks/
│   ├── 01_exploratory.ipynb           # Exploração inicial (legado — resultado invalidado)
│   └── 02_research_questions_full_dataset.ipynb
├── notes/                             # Caderno científico (Obsidian vault)
│   ├── 00 - Research Overview.md      # Panorama técnico
│   ├── 01 - Research Question.md      # QI-1 (central) + extensões QI-2, QI-3, QP-*
│   ├── 02 - Hypotheses.md            # Hipóteses candidatas (nenhuma testada)
│   ├── 03 - Methodology.md           # Plano de pesquisa por etapas
│   ├── Resumo do Trabalho.md         # Resumo narrativo completo
│   ├── Datasets/
│   │   └── GitSkills.md              # Documentação do dataset (colunas, limitações)
│   ├── Decisions/
│   │   ├── Codebook.md               # Instrumento de anotação (v2.3)
│   │   └── Decision Log.md           # Todas as decisões metodológicas, datadas
│   ├── Experiments/
│   │   ├── EXP-001.md … EXP-005.md   # Experimentos do caminho crítico
│   │   └── EXP-012.md                # Prova de conceito do pipeline
│   ├── Literature/
│   │   └── Multilingual Methodology Review.md
│   ├── Methodology/
│   │   ├── QI-1 Methodology.md       # Desenho estatístico (Desenho C)
│   │   ├── QI-2 Methodology.md       # Open coding (extensão)
│   │   ├── QI-3 Coverage Methodology.md  # Crosswalk (extensão)
│   │   └── Multilingual Strategy.md  # Estratégia multilíngue
│   └── Results/
│       └── Security Taxonomy.md      # Taxonomia emergente (v0.1)
├── results/                           # Saídas reproduzíveis dos experimentos
│   ├── EXP-001_profile.json          # Profiling estrutural
│   ├── EXP-002_frame.json            # Candidate retrieval
│   ├── EXP-003_languages.json        # Distribuição de idiomas
│   ├── EXP-004_*.json                # Validação de detectores
│   ├── EXP-005_*.csv/json            # Amostra piloto e formulário
│   └── EXP-012_*.csv/json            # Métricas de classificação e população
├── scripts/                           # Programas que geram todos os resultados
│   ├── profile_dataset.py            # EXP-001: profiling reproduzível
│   ├── build_candidate_frame.py      # EXP-002: frame de candidatos
│   ├── detect_languages.py           # EXP-003: detecção de idiomas
│   ├── validate_language_detection.py # EXP-004: concordância entre detectores
│   ├── build_pilot_sample.py         # EXP-005: amostra piloto determinística
│   ├── build_training_frame.py       # EXP-012: frame de treino
│   ├── train_security_classifier.py  # EXP-012: comparação e treino
│   ├── evaluate_security_classifier.py # EXP-012: avaliação
│   ├── classify_population.py        # EXP-012: classificação em lote
│   ├── download_dataset.py           # Download via HuggingFace
│   ├── analyze_full.py               # Análise exploratória
│   └── create_notebook.py            # Geração de notebook
├── .claude/skills/                    # Skills para o agente de IA assistente
├── .gitignore
├── Makefile
├── requirements.txt
└── README.md
```

## Experimentos Realizados

| Exp | Script | Achado Principal |
|---|---|---|
| **EXP-001** | `profile_dataset.py` | Resultado anterior (1,1%) **invalidado** — valor correto: 52,93%. Dataset íntegro, zero órfãos |
| **EXP-002** | `build_candidate_frame.py` | 78,69% dos representantes citam algum termo de segurança → keyword **não filtra** |
| **EXP-003** | `detect_languages.py` | **14,21% ± 0,48 pp** não é inglês (~267 mil conteúdos); zh 6,0%, ja 1,7%, de 1,6% |
| **EXP-004** | `validate_language_detection.py` | Concordância 0,987 entre detectores; não inglês provavelmente **superestimado** |
| **EXP-005** | `build_pilot_sample.py` | 50 casos estratificados (metade não inglesa), formulário cego, golden set operacional v1 |
| **EXP-012** | `train_security_classifier.py` | TF-IDF nunca reconhece `SECONDARY`/`MENTION`; embeddings multilíngues 3× melhores mas inviáveis sem GPU; 1,61% previsto como SECURITY (**preliminar**) |

## Números que Existem — e o que Não São

> ⚠️ **Nenhum destes é a resposta da pesquisa.**

| Número | Significado |
|---|---|
| **52,93%** | Citam alguma keyword de segurança (inclui `token` como token de LLM) |
| **78,69%** | Recuperados pela busca ampla — mostra que keyword não filtra |
| **~14%** | Não escritos em inglês |
| **11,4%** | Empacotam scripts executáveis |
| **1,61%** | Previsão preliminar do classificador v1 (TF-IDF fraco, golden set de n=49) |

## Dataset

O dataset GitSkills é obtido via [mirror Parquet no HuggingFace](https://huggingface.co/datasets/mvaccargiu/gitskills) (~6 GB comprimido). O download é feito automaticamente e cacheado em `data/`.

| Tabela | Registros | Conteúdo |
|---|---|---|
| `artifacts` | 3.797.117 | Um registro por `SKILL.md`: repositório, path, hash, texto, front matter |
| `artifact_siblings` | 7.264.865 | Scripts e arquivos de referência junto às skills |
| `repos` | 282.200 | Metadados dos repositórios: stars, linguagem, fork, licença |
| `mining_runs` | 7 | Log de proveniência das coletas |

> **Nota:** `data/` está no `.gitignore`. Cada pesquisador executa o download localmente.

## Quick Start

> **Pré-requisitos:** Python 3.11+ e [`uv`](https://docs.astral.sh/uv/) instalados.

Os scripts utilizam `uv run` com dependências efêmeras — não é necessário instalar nada globalmente:

```bash
# Profiling do dataset (EXP-001)
uv run --with duckdb python scripts/profile_dataset.py

# Detecção de idiomas (EXP-003)
uv run --with duckdb --with py3langid --with lingua-language-detector \
  python scripts/detect_languages.py

# Amostra piloto (EXP-005)
uv run --with duckdb --with py3langid --with lingua-language-detector \
  python scripts/build_pilot_sample.py

# Treino do classificador (EXP-012)
uv run --with scikit-learn --with pandas --with pyarrow \
  --with sentence-transformers --with joblib \
  python scripts/train_security_classifier.py

# Classificação da população (EXP-012)
uv run --with duckdb --with pyarrow --with pandas \
  --with scikit-learn --with joblib \
  python scripts/classify_population.py
```

### Setup alternativo (venv tradicional)

```bash
make setup        # Cria venv, instala dependências e registra kernel Jupyter
make download     # Baixa o dataset do HuggingFace para data/
make notebook     # Abre o Jupyter Notebook
make clean        # Remove o ambiente virtual
make clean-data   # Remove os dados locais
```

## Caderno Científico

O diretório `notes/` é um vault [Obsidian](https://obsidian.md/) que funciona como caderno científico do projeto. Toda decisão metodológica está registrada com data, alternativas e consequências. Todo número citável vem de um script em `scripts/` com saída em `results/`.

Duas regras inegociáveis:

1. **IA não é gabarito** — LLM pode assistir triagem e pré-classificar, mas não é ground truth. Todo uso em resultado registra modelo, versão e prompt.
2. **Todo número precisa de script** — Se não dá para apontar o programa que gerou e o arquivo onde foi salvo, o número sai do texto.

## Citação

```bibtex
@inproceedings{gitskills2027,
  author    = {Destefanis, Giuseppe and Graziotin, Daniel and Vaccargiu, Matteo and Ortu, Marco},
  title     = {GitSkills: A Dataset of Agent Skills on GitHub},
  year      = {2027},
  publisher = {Association for Computing Machinery},
  address   = {New York, NY, USA},
  url       = {https://arxiv.org/abs/2608.10906},
  doi       = {https://doi.org/10.48550/arXiv.2608.10906},
  booktitle = {Proceedings of the 24th International Conference on Mining Software Repositories},
  pages     = {To Appear},
  numpages  = {3},
  location  = {Dublin, Ireland},
  series    = {MSR '27}
}
```
