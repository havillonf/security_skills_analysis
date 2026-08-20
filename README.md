# Security Skills Analysis

Estudo exploratório sobre skills agênticas relacionadas à segurança no dataset [GitSkills](https://zenodo.org/records/21875637).

> **Paper:** Destefanis, G., Graziotin, D., Vaccargiu, M., & Ortu, M. (2027). *GitSkills: A Dataset of Agent Skills on GitHub*. In MSR '27. [arXiv:2608.10906](https://arxiv.org/abs/2608.10906)

## Objetivo

Avaliar as skills agênticas (arquivos `SKILL.md`) que se relacionam com **segurança no desenvolvimento com IA**, buscando identificar falhas, lacunas ou padrões relevantes.

## Estrutura do Projeto

```
security_skills_analysis/
├── data/                        # Cache local do dataset (gitignored)
├── notebooks/                   # Jupyter Notebooks de análise
│   └── 01_exploratory.ipynb     # Exploração inicial do dataset
├── scripts/
│   └── download_dataset.py      # Script de download do dataset via HuggingFace
├── .gitignore
├── Makefile                     # Automação de setup e tarefas comuns
├── requirements.txt             # Dependências Python (com versões fixas)
└── README.md
```

## Quick Start (Setup do Ambiente)

> **Pré-requisito:** Python 3.12+ instalado.

```bash
# Setup completo com um comando:
make setup

# Ou manualmente:
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m ipykernel install --user --name security-skills --display-name "Security Skills Analysis"
```

## Download do Dataset

O dataset GitSkills é obtido via [mirror Parquet no HuggingFace](https://huggingface.co/datasets/mvaccargiu/gitskills) (~13 GB comprimido, vs 44 GB do SQLite original no Zenodo). O download é feito automaticamente e cacheado em `data/`.

```bash
# Download completo (todas as tabelas → Parquet local em data/)
make download

# Ou diretamente:
source .venv/bin/activate
python scripts/download_dataset.py
```

> **Nota:** O `data/` está no `.gitignore`. Cada pesquisador executa o download localmente.
> Todos obtêm exatamente os mesmos dados da mesma fonte (HuggingFace), garantindo reprodutibilidade.

### Tabelas do Dataset

| Tabela                | Registros | Tamanho (Parquet) | Conteúdo                                                                  |
| --------------------- | --------- | ----------------- | -------------------------------------------------------------------------- |
| `artifacts`         | 3.797.117 | ~12 GB            | Um registro por`SKILL.md`: repositório, path, hash, texto, front matter |
| `artifact_siblings` | 7.264.865 | ~1 GB             | Scripts e arquivos de referência junto às skills                         |
| `repos`             | 282.200   | ~30 MB            | Metadados dos repositórios: stars, linguagem, fork, licença              |
| `mining_runs`       | 7         | ~5 KB             | Log de proveniência das coletas                                           |

## Uso dos Notebooks

```bash
# Ativar ambiente e abrir Jupyter
source .venv/bin/activate
jupyter notebook notebooks/

# Ou via Makefile:
make notebook
```

> **Importante:** Selecione o kernel **"Security Skills Analysis"** ao abrir os notebooks.

## Comandos Disponíveis

| Comando             | Descrição                                                  |
| ------------------- | ------------------------------------------------------------ |
| `make setup`      | Cria venv, instala dependências e registra o kernel Jupyter |
| `make download`   | Baixa o dataset do HuggingFace para`data/`                 |
| `make notebook`   | Abre o Jupyter Notebook                                      |
| `make clean`      | Remove o ambiente virtual                                    |
| `make clean-data` | Remove os dados locais                                       |

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
