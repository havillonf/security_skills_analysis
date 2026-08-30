---
name: data-analysis
description: Como conduzir análise de dados no projeto security_skills_analysis - DuckDB sobre Parquet, denominadores corretos em GitSkills, amostragem reproduzível, validação de joins, e regras de reprodutibilidade. Use ao consultar, agregar, amostrar, cruzar tabelas ou gerar qualquer número/gráfico a partir do dataset.
---

# Análise de dados: GitSkills

Pre-requisito: skill `project-context`.

## Ambiente

A máquina primária e Windows, sem `.venv` e sem as dependências do
`requirements.txt` instaladas. O caminho que funciona hoje e `uv` com dependências
efemeras - não muta o ambiente e e reproduzível:

```bash
uv run --with duckdb python scripts/profile_dataset.py
uv run --with duckdb --with polars python scripts/<novo_script>.py
```

O `Makefile` e o `scripts/download_dataset.py` assumem POSIX e um layout de dados
que não é o que existe em disco. Não confie neles sem verificar.

## Regra 1 - DuckDB sobre os Parquet, nunca pandas sobre o dataset

`artifacts` tem 3,8M linhas e 6,1 GB. Carregar em pandas custa ~2,4 GB de RAM só
para os metadados, e o notebook legado faz exatamente isso. Não repita.

```python
import duckdb
con = duckdb.connect()
con.execute("SET enable_progress_bar=false")   # senao polui o output do agente

A = "read_parquet('data/raw/gitskills/data/artifacts/*.parquet')"
R = "read_parquet('data/raw/gitskills/data/repos/*.parquet')"
S = "read_parquet('data/raw/gitskills/data/artifact_siblings/*.parquet')"
```

O glob resolve os 31 shards de `artifacts`. DuckDB faz projection e predicate
pushdown: selecionar 3 colunas de 3,8M linhas custa segundos. Uma varredura de
`lower(content) LIKE ...` sobre todos os representantes leva ~1 min - aceitável,
mas rode uma vez e salve o resultado.

`content` e a coluna cara (mediana 5 KB, máximo 356 KB). Nunca a inclua num
`SELECT *` que retorne muitas linhas.

## Regra 2 - declare o denominador antes de calcular o percentual

`artifacts` mistura dois graos. Escolha um explicitamente e escreva qual foi no
resultado:

| Denominador | n | Quando usar |
|---|---|---|
| Ocorrências | 3.797.117 | "quantos arquivos existem no GitHub" (conta cópias) |
| Representantes (`dedup_primary = 1`) | 1.877.981 | **padrão**: qualquer análise de conteúdo |
| `frontmatter_valid = 1` | 1.627.753 | análise de conformidade com a spec |
| ... com `name` e `description` não nulos | 1.625.701 | análise de `name` / `description` |
| Com histórico de commits | 458.548 | qualquer análise temporal |
| Repositórios | 282.200 | análise por projeto |

`content`, `name`, `description`, `body_chars`, `has_scripts`, `has_references` e
o histórico **só existem para representantes**. Filtrar por `content IS NOT NULL`
sem entender isso equivale a filtrar por `dedup_primary = 1` - o que é valido, mas
precisa ser dito, porque muda a população.

Inconsistência conhecida a evitar: 2.367 linhas tem `dedup_primary = 0` com
`content_fetched = 1`, e 2.348 delas tem `content`. Use `dedup_primary = 1` como
critério canonico, não `content_fetched`.

## Regra 3 - amostragem tem que ser aleatória e reproduzível

**`LIMIT n` e `head(n)` sobre Parquet não são amostra.** As primeiras linhas de
`artifacts` são um bloco patológico (ver `project-context`). Foi o que invalidou o
resultado anterior.

Amostra determinística, mesma em qualquer máquina, sem seed externa:

```sql
SELECT ... FROM read_parquet(...)
WHERE dedup_primary = 1
ORDER BY hash(file_sha)
LIMIT 5000
```

`USING SAMPLE n ROWS` do DuckDB e reservoir e **não respeita o `n` pedido** quando
combinado com filtros - num teste pediu 5.000 e devolveu 2.455. Evite, ou valide
`count(*)` do resultado.

Para amostra estratificada (por `location_class`, por faixa de stars, por presença
de scripts), estratifique explicitamente com `QUALIFY row_number() OVER (PARTITION
BY ... ORDER BY hash(file_sha)) <= n`.

Qualquer amostra usada para anotação manual: salve os `file_sha` sorteados em
`results/`, para a anotação ser auditável e re-executável.

## Regra 4 - joins

Chaves verificadas (EXP-001, integridade confirmada):

- `artifacts.repo_full_name` -> `repos.full_name`: **N:1, zero órfãos**, 282.200
  repos distintos dos dois lados, `metadata_fetched = 0` em zero linhas. Join
  seguro; ainda assim, valide `count(*)` antes e depois.
- `artifact_siblings (repo_full_name, artifact_path)` -> `artifacts (repo_full_name,
  path)`: **N:1 apenas contra representantes**. Siblings só existem para
  representantes. Um join ingenuo aqui infla linhas - `sibling_count` tem máximo
  79.940 num único skill.

Não há fuzzy matching neste projeto. Se alguma análise parecer exigir matching
aproximado, isso é sinal de que a unidade de análise esta errada - pare e registre.

Toda vez que fizer join: compare a contagem antes e depois e explique a diferenca.
Diferenca inexplicada e bug, não resultado.

## Regra 5 - nulos significam coisas diferentes

Ausência aqui quase nunca e "dado faltando aleatoriamente":

- `content IS NULL` -> não é representante (por construção, não por falha).
- `first_commit_at IS NULL` -> histórico não coletado. `history_fetched = 1` para
  458.548 arquivos: locais padrão **mais** uma amostra estratificada por tamanho do
  resto. Isso é MNAR: skills em locais padrão estão sobre-representadas em qualquer
  análise temporal. Diga isso ao reportar.
- `frontmatter_valid = 0` -> o arquivo não tem front matter parseável. Pode ser um
  `SKILL.md` que não segue a spec, ou um falso positivo da busca por nome de
  arquivo. E um achado, não lixo a descartar.
- `repos.stars IS NULL` (515 repos) -> metadados não obtidos; repositório pode ter
  sido removido ou tornado privado entre a descoberta e o enriquecimento.

Nunca impute sem aprovação humana explícita.

## Regra 6 - distribuições são pesadas; use a estatística certa

`stars`: mediana 0, p75 = 2, p90 = 15, p99 = 1.278, máximo 383.040, média 122.
**59,3% dos repositórios tem zero stars.** Média de stars não descreve nada aqui.
Use mediana, quantis e escala log; ao comparar grupos use testes não paramétricos
(Mann-Whitney, Kruskal-Wallis) e reporte tamanho de efeito, não só p-valor.

`sibling_count`: mediana 0, máximo 79.940. `body_chars`: mediana 4.605, máximo
355.781. Sempre inspecione a cauda antes de resumir.

## Regra 7 - dependência entre observações

Observações **não são independentes**. 388.501 conteúdos distintos aparecem mais de
uma vez, cobrindo 2.307.637 das 3.797.117 ocorrências (60,8%). Repositórios
concentram muitas skills, e contas concentram muitos repositórios (195.841 contas
para 282.200 repos).

Consequência: qualquer teste que assuma independência entre ocorrências está errado.
Deduplique por `file_sha` **e** verifique se o resultado não é dominado por poucos
repositórios/donos. Reporte, junto de cada achado, quantos repos e quantos donos
distintos o sustentam.

## Regra 8 - reprodutibilidade

Número que vai para o TCC nasce de script versionado, nunca de conversa com o
agente nem de celula de notebook.

1. Script em `scripts/`, com argumentos explícitos e sem caminho absoluto de
   máquina.
2. Saída em `results/<EXP-ID>_<nome>.json|parquet|csv`. Parquet para tabela
   intermediaria, JSON para métricas escalares.
3. Nota `notes/Experiments/EXP-XXX.md` ligando questão -> script -> saída ->
   interpretação -> limitações.
4. Seed explícita quando houver aleatoriedade; preferir ordenação determinística
   (`ORDER BY hash(...)`) a seed.
5. Registrar versão de DuckDB na saída (o `profile_dataset.py` já faz).

Notebooks servem para explorar e para gerar figura final a partir de `results/`.
Não servem como fonte de verdade de nenhum número.

## Regra 9 - economia de output

- Nunca imprima mais de ~30 linhas de dados.
- Antes de uma query que possa retornar muito, rode `count(*)`.
- Nunca imprima `content` inteiro; use `substr(content, 1, 300)`.
- Prefira salvar em `results/` e reportar só o agregado.

## Regra final

**Nunca transforme uma observação exploratória em conclusão científica sem
validação adequada.** Antes de chamar qualquer coisa de achado, verifique: o
denominador esta declarado? a amostra e aleatória? o resultado sobrevive a
deduplicação? sobrevive a excluir os 10 maiores repositórios? uma pequena mudança
no critério muda a conclusão? Se qualquer resposta for "não sei", e observação.
