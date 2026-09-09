---
tipo: literatura
leitura: conteudo-recuperado
usado-em: D-027, EXP-014, Codebook v2.5
---

# Agent Skills in the Wild

**arXiv 2601.10338** — https://arxiv.org/html/2601.10338v1

> *An Empirical Study of Security Vulnerabilities at Scale*

## O que e

Estudo empirico em escala sobre agent skills: 42.447 coletadas de dois
marketplaces (skills.rest, skillsmp.com), 31.132 unicas analisadas com
`SkillScan` (estatico + classificacao semantica por LLM), 1.218 categorizadas
manualmente.

## Intuito dos autores

Medir **vulnerabilidades dentro das skills** — prompt injection, exfiltracao
de dados, escalacao de privilegio, risco de cadeia de suprimentos. Encontram
26,1% com ao menos uma vulnerabilidade.

Como subproduto, criam uma **taxonomia funcional de 8 categorias por proposito
pretendido**, uma delas *Security/Red-team*.

## No que nos ajudou

**1. Corroboracao externa do nosso numero mais estavel.**
*Security/Red-team* = 89 de 1.218 = **7,3%**. Nossa camada `PRIMARY` deu
9/100 no [[EXP-014]] e 6-7/91 no [[EXP-013]] — quatro execucoes independentes,
dois esquemas diferentes, outro dataset, outro metodo, mesmo patamar.

**2. Explica por que o kappa deles e alto e o nosso nao era.**
A taxonomia deles e de **rotulo unico e mutuamente exclusivo**: uma skill e
*Development Tools* **ou** *Security/Red-team*, nunca as duas. **Nao existe
equivalente de `SECONDARY`.** Um `code-review` com secao de OWASP cairia em
*Development Tools*.

Isso da resposta pronta para a banca perguntar *"por que seu kappa e 0,67 se a
literatura reporta 0,86?"* — eles medem proposito dominante em rotulo unico,
que corresponde ao nosso `security_focus`, onde tambem temos kappa alto. O
kappa deles vem de **contornar** a fronteira dificil, nao de resolve-la.

**3. Delimita o escopo e mostra que nao ha sobreposicao.**
Eles estudam seguranca **das** skills (Eixo B de [[Decision Log#D-007]]); a
QI-1 estuda skills que **fazem** seguranca (Eixo A). Perguntas diferentes,
populacoes diferentes.

## Numeros citaveis

| | |
|---|---|
| Skills coletadas / analisadas / categorizadas | 42.447 / 31.132 / 1.218 |
| *Security/Red-team* | 89 (**7,3%**) |
| kappa categorizacao (automatico vs. manual) | 0,86 |
| kappa presenca binaria de vulnerabilidade | 0,83 |
| kappa categoria de vulnerabilidade | 0,79 |
| Skills com >=1 vulnerabilidade | 26,1% |

## Ressalvas

- Marketplaces (skills.rest, skillsmp.com), **nao GitHub** — populacao
  diferente do GitSkills. A convergencia em ~7% e mais forte por isso, nao
  menos, mas nao e replicacao.
- O kappa=0,86 e entre **classificacao automatica e rotulo manual**, nao entre
  dois anotadores independentes. Nao e diretamente comparavel ao nosso.
- Eles proprios declaram o problema de *"Security/Red-team conflation"*: a
  deteccao identifica corretamente como perigoso mas **nao consegue determinar
  intencao** — pentest legitimo e malware disfarcado ficam indistinguiveis.

## Ligacoes

[[EXP-014]] · [[Decision Log#D-027]] · [[Codebook]] · [[Classification and Sampling Precedents]]
