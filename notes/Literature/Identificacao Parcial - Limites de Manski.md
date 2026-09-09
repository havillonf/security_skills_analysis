---
tipo: literatura
leitura: resumo-de-busca
usado-em: D-028 (controle de vies da exclusao de frame)
---

# Identificacao parcial — limites de Manski

- **Embracing Uncertainty: The Value of Partial Identification in Public Health
  and Clinical Research** — https://pmc.ncbi.nlm.nih.gov/articles/PMC10799552/
- **HIV Estimation Using Population-Based Surveys with Non-Response: A Partial
  Identification Approach** —
  https://www.medrxiv.org/content/10.1101/2023.06.03.23290936.full.pdf
- **Manski, C. F. (1989).** *Anatomy of the Selection Problem.* *The Journal of
  Human Resources* 24(3). DOI 10.2307/145818 — **referencia adotada**
  (decisao do pesquisador, 2026-09-05), chave `manski1989anatomy`

## O que e

Abordagem para estimar um parametro quando parte das unidades **nao pode ser
medida**: em vez de imputar (que exige supor MAR) ou ignorar (que enviesa),
deriva-se **limites** que nao dependem de suposicoes nao testaveis sobre o
mecanismo de ausencia.

## No que nos ajudou

Sustenta o controle de vies obrigatorio de [[Decision Log#D-028]]. Nossa
segunda exclusao de frame — evidencia truncada e indecidivel — depende de
duvida **sobre a propria variavel estimada**, o que enviesa em direcao
desconhecida.

Solucao adotada: reportar a prevalencia como **intervalo**, calculado
assumindo que todos os excluidos sao Security Skill e que nenhum e. Como o
universo possivel e <=0,75% da populacao, o intervalo deve sair estreito — o
que **demonstra** que a exclusao foi inofensiva em vez de pedir que se
acredite.

**Analogia direta e citavel:** estimar prevalencia com unidades nao
mensuraveis e o problema de prevalencia de HIV com nao resposta em survey. A
epidemiologia resolveu com limites; nao e invencao nossa.

## Ressalva

**Lidas apenas por resumo de busca.** Metadados do Manski verificados via
Crossref; o **texto nao foi lido**. O tratamento formal precisa ser lido antes
de aparecer no TCC — e o tipo de citacao em que errar a formulacao e visivel.

Nota sobre a escolha: a busca tambem apontava *Partial identification with
missing data: concepts and findings*. Optou-se por *Anatomy of the Selection
Problem* por sustentar melhor o argumento de D-028.

## Ligacoes

[[Decision Log#D-028]] · [[QI-1 Methodology]]
