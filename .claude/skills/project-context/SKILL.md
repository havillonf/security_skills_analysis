---
name: project-context
description: Contexto científico e técnico do projeto security_skills_analysis (TCC sobre skills agênticas de segurança no dataset GitSkills). Use SEMPRE antes de analisar dados, escrever código, interpretar resultados ou responder perguntas sobre este repositório - inclui armadilhas conhecidas do dataset e resultados já invalidados.
---

# Contexto do projeto: security_skills_analysis

TCC / possível artigo. Pesquisador: Victor Brito. Idioma dos artefatos: **português**.
Código, nomes de variáveis e identificadores: inglês.

## O que se pesquisa

População de **agent skills** (`SKILL.md`) públicas no GitHub, olhadas pela lente de
**segurança**. O objetivo declarado no README e "avaliar as skills agênticas que se
relacionam com segurança no desenvolvimento com IA, buscando identificar falhas,
lacunas ou padrões relevantes".

Isso ainda e um objetivo amplo, não uma questão de pesquisa operacionalizada.
As questões candidatas estão em `notes/01 - Research Question.md`, marcadas por
procedência (explícita no projeto / inferida / proposta). **Não trate questão
inferida como se fosse definida pelo pesquisador.**

## Dataset: um só, com quatro tabelas

Atenção: o scaffolding inicial de `notes/` falava em "Dataset A" e "Dataset B" com
matching entre eles. **Isso não se aplica.** Existe **um** dataset (GitSkills) com
quatro tabelas relacionadas por chave exata. Não há fuzzy matching neste projeto.

GitSkills (Destefanis, Graziotin, Vaccargiu & Ortu, MSR '27, arXiv:2608.10906),
coletado em julho de 2026, CC-BY-4.0.

| Tabela | Linhas | Grao |
|---|---|---|
| `artifacts` | 3.797.117 | uma **ocorrência** de arquivo SKILL.md |
| `artifact_siblings` | 7.264.865 | um arquivo/dir vizinho de um representante |
| `repos` | 282.200 | um repositório |
| `mining_runs` | 7 | uma execução de coleta |

Detalhe por tabela, semântica de cada coluna e limitações:
`notes/Datasets/GitSkills.md`.

## As três armadilhas que mais importam

1. **`artifacts` tem dois graos misturados.** Cada linha e uma *ocorrência*, mas
   apenas as 1.877.981 linhas com `dedup_primary = 1` tem `content`, front matter e
   composição. As outras 1.919.136 tem só metadados de localização. Escolher o
   denominador errado muda qualquer percentual. Ver `notes/Decisions/D-001`.

2. **`head(n)` sobre o Parquet não é amostra.** As primeiras linhas são um bloco
   patológico: mediana de `content` = 42 caracteres (majoritariamente symlinks),
   67 de 5.000 com front matter, um único `discovered_at`. Numa amostra aleatória
   de representantes a mediana e 5.006 caracteres. Ver `notes/Decisions/D-002`.

3. **Keyword em `content` mede menção, não propósito.** 52,93% dos representantes
   citam ao menos uma keyword de segurança; 4,09% declaram segurança no front
   matter. Fator ~13x. Keyword serve como **triagem**, nunca como classificador -
   a classificação valida e a de D-004 (`SEC-PRIMARY`/`SEC-SECONDARY`/`SEC-MENTION`/
   `NON-SEC`). Ver a skill `security-analysis` e `notes/Decisions/Codebook.md`.

## Resultado já invalidado - não reutilizar

`notebooks/01_exploratory.ipynb`, seção 6, conclui **"1,1% das skills mencionam
segurança"**. Esse número e inválido: foi calculado sobre `head(5000)` (armadilha 2)
e sobre um campo `content` que naquele bloco continha alvos de symlink, não texto de
skill. O valor correto, sobre todos os representantes e com as mesmas keywords, e
**52,93%** - 48x maior. Registrado em `notes/Experiments/EXP-001.md`.

O notebook e **exploratório e legado**. Não cite nenhum número dele sem recomputar.

## Estado atual (2026-08-22)

Feito: dataset baixado e perfilado; integridade estrutural verificada; resultado
anterior invalidado; skills e caderno criados. **D-004 decidida**: existe definição
de Security Skill e taxonomia de 4 classes, com codebook v1.0
(`notes/Decisions/Codebook.md`).

Próximo: piloto de anotação (~50 casos) na fronteira **SEC-SECONDARY vs
SEC-MENTION**, que é onde o número final se decide. Até o codebook passar no piloto e
haver métricas contra padrão-ouro, **não produza prevalência nem número apresentável
como achado** - qualquer classificação em escala ainda não tem validade conhecida.

## Layout do repositório

```
data/raw/gitskills/data/{artifacts,artifact_siblings,repos,mining_runs}/*.parquet
notebooks/01_exploratory.ipynb    exploratorio, legado, contem resultado invalido
scripts/download_dataset.py       desatualizado: gera layout que ninguem usa
scripts/profile_dataset.py        profiling reproduzivel (EXP-001)
results/EXP-001_profile.json      numeros citados nas notas
notes/                            Obsidian vault = caderno cientifico
.claude/skills/                   project-context, data-analysis, security-analysis
```

## Contradições conhecidas entre documentação e realidade

Não "corrija" silenciosamente; estão registradas em `notes/Decisions/D-003`.

- `scripts/download_dataset.py` grava `data/<tabela>.parquet` (arquivo único);
  os dados presentes estão em `data/raw/gitskills/data/<tabela>/*.parquet`
  (31 shards só em `artifacts`). O notebook aponta para o caminho antigo e não roda.
- README diz que `requirements.txt` tem "versões fixas"; não tem nenhuma pinada.
- README informa ~12 GB para `artifacts`; em disco são 6,1 GB.
- `Makefile` assume `.venv/bin/` (POSIX). O ambiente primário e Windows. Os outputs
  do notebook trazem caminhos `/tmp/ipykernel_*`, então ele foi executado em
  Linux/macOS ou WSL, não na máquina onde os dados estão.
- Não existe `.venv` na máquina Windows, e nenhuma dependência do
  `requirements.txt` está instalada globalmente. `uv` está disponível e e o caminho
  usado hoje (ver skill `data-analysis`).

## Regras de trabalho neste repositório

- Toda decisão metodológica vai para `notes/Decisions/` com data, alternativas e
  consequências. Decisão já usada em experimento não muda em silêncio: registra-se
  a revisão.
- Todo número que vá para o texto do TCC precisa vir de script versionado em
  `scripts/`, com saída em `results/`, referenciado por um `EXP-XXX`.
- Separe sempre **observação** (o que os dados mostram), **interpretação** (uma
  explicação possível) e **conclusão** (sustentada por método e evidência).
- Não commite sem o pesquisador pedir. `data/` e gitignored; nunca versione Parquet.
- Escolhas que mudam materialmente as conclusões (definir "segurança", escolher
  threshold, trocar unidade de análise, descartar grande volume de dados) exigem
  aprovação humana explícita.
