---
tipo: dataset
nome: GitSkills
version: snapshot julho/2026
licenca: CC-BY-4.0
atualizado: 2026-08-22
---

# GitSkills

Destefanis, G., Graziotin, D., Vaccargiu, M. & Ortu, M. (2027). *GitSkills: A
Dataset of Agent Skills on GitHub*. MSR '27. [arXiv:2608.10906](https://arxiv.org/abs/2608.10906).
Zenodo DOI 10.5281/zenodo.21875637 · mirror HF `mvaccargiu/gitskills`.

3.797.117 arquivos `SKILL.md` de 282.200 repositórios públicos (195.841 contas),
coletados em **julho de 2026**. Agrupados por hash de conteúdo em 1.877.981
conteúdos distintos.

> [!note] Não existem "Dataset A" e "Dataset B"
> O scaffolding inicial de `notes/` sugeria dois datasets com fuzzy matching.
> Há **um** dataset com quatro tabelas ligadas por chave exata. Sem fuzzy matching.

## Localização em disco

```
data/raw/gitskills/data/artifacts/*.parquet          31 shards, 6,1 GB
data/raw/gitskills/data/artifact_siblings/*.parquet   6,5 GB
data/raw/gitskills/data/repos/part-00000.parquet     18,7 MB
data/raw/gitskills/data/mining_runs/part-00000.parquet
```

`data/` e gitignored. `scripts/download_dataset.py` produz um layout **diferente**
(`data/<tabela>.parquet`) que não corresponde ao que existe - ver
[[Decision Log#D-003]].

## `artifacts` - 3.797.117 linhas, 30 colunas

**Grao duplo.** Uma linha = uma *ocorrência* de arquivo. Mas só as
**1.877.981 com `dedup_primary = 1`** (os representantes) foram enriquecidas.

| Grupo | Colunas | Preenchimento |
|---|---|---|
| Localização | `repo_full_name`, `path`, `filename`, `location_class`, `file_sha`, `discovered_at` | todas as linhas |
| Conteúdo | `content`, `content_fetched`, `content_sha_ok`, `body_chars` | só representantes |
| Front matter | `frontmatter_valid`, `name`, `description` | 1.627.753 validos |
| Composição | `sibling_count`, `sibling_bytes`, `has_scripts`, `has_references`, `composition_fetched`, `composition_truncated` | só representantes |
| Histórico | `first_commit_at`, `last_commit_at`, `commit_count`, `*_author`, `*_author_type`, `*_message` | 458.548 |

### Denominadores

| População | n |
|---|---|
| Ocorrências | 3.797.117 |
| Representantes (`dedup_primary = 1`) | 1.877.981 |
| `frontmatter_valid = 1` | 1.627.753 |
| ... e com `name` **e** `description` não nulos | 1.625.701 |
| Com histórico de commits | 458.548 |

Atenção aos dois ultimos: `frontmatter_valid = 1` não garante que `name` e
`description` estejam preenchidos - 2.052 linhas tem front matter valido sem um dos
dois. Análises sobre `name`/`description` usam 1.625.701; declare qual dos dois usou.

### `location_class`

| Valor | n | Leitura |
|---|---|---|
| `skills-dir` | 2.102.053 | dentro de um diretório de skills |
| `other` | 1.321.412 | fora de local convencional |
| `canonical` | 373.652 | local canonico da spec |

`filename` tem 20 variantes de capitalização: `SKILL.md` (3.742.828), `skill.md`
(49.314), `Skill.md` (3.530), `SKILL.MD` (1.426) e caudas como `SKIll.md`. A
descoberta foi por nome de arquivo, então **inclui falsos positivos deliberados**:
arquivos que apenas contém o termo, e arquivos minusculos anteriores ao formato.
Nem toda linha e uma agent skill no sentido da spec.

### Distribuições de `content` (representantes)

mediana 4.999 · média 7.334 · p05 707 · p95 20.905 · max 355.781 caracteres.
7.309 com menos de 80 caracteres; 5.363 parecem alvos de symlink
(`../.claude/SKILL.md`). Essas ultimas são a origem do erro em [[EXP-001]].

### Inconsistência conhecida

2.367 linhas com `dedup_primary = 0` e `content_fetched = 1` (2.348 com `content`).
Não explicado pela documentação do dataset. Use `dedup_primary = 1` como critério
canonico, nunca `content_fetched`.

## `artifact_siblings` - 7.264.865 linhas

Arquivos e diretórios ao lado de um **representante**. `entry_type`: `file`
(5.858.945, dos quais 3.497.752 com conteúdo sob um teto de tamanho) e `dir`
(1.405.920, nunca com conteúdo).

Junta em `artifacts` por `(repo_full_name, artifact_path)` -> `(repo_full_name,
path)`. N:1, e so contra representantes. `sibling_count` vai a 79.940 num único
skill - join ingenuo explode.

`composition_truncated = 1` em 252.250 representantes (13,4%): a listagem da pasta
esta **incompleta**. Limitação seria para qualquer análise de supply chain.

## `repos` - 282.200 linhas

`full_name` (chave), `owner`, `stars`, `forks`, `is_fork`, `language`, `license`,
`description`, `created_at`, `pushed_at`, `metadata_fetched`.

Integridade verificada: 282.200 repos distintos em `artifacts`, 282.200 em `repos`,
**zero órfãos**, `metadata_fetched = 0` em zero linhas. 515 repos tem `stars` nulo
(provavelmente removidos ou tornados privados entre descoberta e enriquecimento).

`stars`: mediana 0 · p75 2 · p90 15 · p99 1.278 · max 383.040 · média 122.
**59,3% com zero stars.** Cauda extrema - nunca resuma por média.

Top linguagens: Python 71.801 · TypeScript 67.104 · vazio 29.601 · JavaScript
23.938 · Shell 19.780. `description` nula em 113.141 repos.

## `mining_runs` - 7 linhas

Sete execuções entre 2026-07-09 e 2026-07-20, todas com query
`filename:SKILL.md`, `artifact_type = agent-skills`.

## Metodologia de coleta (do paper)

Read-only, via GitHub REST/GraphQL/code-search + CDN de conteúdo bruto:

1. **Descoberta** - busca por `filename:SKILL.md`, particionada por tamanho de
   arquivo para contornar o teto de 1.000 resultados da API. O `total_count`
   reportado pela API mostrou-se não confiável (~349.000 contra 3,8M reais).
2. **Deduplicação** - agrupamento por hash; um representante por grupo, preferindo
   arquivo em `.claude/skills/`.
3. **Enriquecimento** - conteúdo, front matter, composição da pasta, metadados do
   repo e histórico de commit para locais padrão mais amostra estratificada.

## Limitações e vieses

- **Limite inferior por construção.** O code search do GitHub indexa apenas branch
  default, arquivos < 384 KB, repos recentemente ativos com < 500.000 arquivos, e
  forks só quando tem mais stars que o pai.
- **Só repositórios públicos.** Práticas de segurança corporativa ficam de fora.
- **Snapshot único.** Sem série temporal; skills removidas não aparecem
  (survivorship bias).
- **Histórico MNAR.** Os 458.548 com commit history são locais padrão + amostra
  estratificada por tamanho: enviesado, não aleatório.
- **Preferência de representante não aleatória.** Prefere `.claude/skills/`, então
  o texto analisado tende a vir da variante mais convencional do grupo.
- **Dependência entre observações.** 388.501 conteúdos tem cópias, cobrindo
  2.307.637 ocorrências (60,8%).
- **Anonimização.** Autores substituidos por codigos unidirecionais com chave não
  distribuída; bots mantem login; e-mails e nomes pessoais redigidos. Autoria e
  rastreável entre linhas, mas não identificável - e não reversível.
- **Licenca do conteúdo.** Os campos `content` reproduzem texto de repos públicos e
  seguem a licenca de origem, não a CC-BY-4.0 do dataset. Consulte `repos.license`
  antes de reproduzir qualquer trecho no TCC.

## Ligações

[[00 - Research Overview]] · [[EXP-001]] · [[Decision Log]]
