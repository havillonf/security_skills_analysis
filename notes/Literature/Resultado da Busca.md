---
tipo: resultado-de-busca
data: 2026-09-05
protocolo: Protocolo de Busca v1.0
---

# Resultado da busca estruturada

Execucao do [[Protocolo de Busca]] v1.0 em 2026-09-05.

## Sumario

| | RQ-A prevalencia | RQ-B esquemas | RQ-C anotacao por LLM |
|---|---|---|---|
| Titulos retornados | 17 | 10 | 10 |
| Incluidos | 1 novo | 1 novo | 1 familia (5 itens) |
| Excluidos por **E1** | 13 | 6 | 0 |
| Ja no acervo | 2 | 2 | 1 |

**Total no acervo apos esta rodada: 12 notas.**

## Inclusoes novas

| Referencia | RQ | Por que entrou | Leitura |
|---|---|---|---|
| [[SeRe - Security-Related Code Review Dataset]] | B | Fleiss kappa=0,88 com definicao intensional+extensional (CWE). O benchmark mais alto encontrado, e explica a diferenca | conteudo-recuperado |
| [[LLMs como Anotadores - Confiabilidade]] | C | kappa LLM-LLM=0,233 vs humano-humano=0,573 em tarefa interpretativa; e a tese "assistentes bons, anotadores independentes ruins" | resumo-de-busca |
| *Security in the Age of AI Teammates: Agentic Pull Requests* (arXiv 2601.00477) | A | 33.596 PRs de agentes autonomos, identificacao de PRs de seguranca por filtro baseado em regra + verificacao manual — desenho proximo ao nosso | **nao recuperado** |

> [!note] O terceiro nao virou nota ainda
> *Agentic Pull Requests* passa nos criterios e e o unico achado de RQ-A que
> mede algo proximo de prevalencia por proposito. **Nao foi recuperado nesta
> rodada** — fica registrado como pendencia de leitura, nao como referencia
> disponivel.

## Exclusoes — e por que a maioria caiu no mesmo criterio

**13 dos 17 resultados de RQ-A foram excluidos por E1**: tratam de *detectar
vulnerabilidades* em artefatos, nao de classificar o artefato quanto ao seu
**proposito** de seguranca.

Exemplos: *Empirical analysis of security vulnerabilities in Python packages*,
*An Empirical Study on Virtual Reality Software Security Weaknesses*,
*Towards Measuring Vulnerabilities and Exposures in Open-Source Packages*,
*Detecting Misuse of Security APIs*, *On the prevalence of software supply
chain attacks*, *The Hidden Dangers of Public Serverless Repositories*.

**Isto e resultado, nao ruido.** A concentracao esmagadora da literatura em
"encontrar falhas" confirma empiricamente a lacuna que ja haviamos observado:
quase ninguem pergunta *quantos artefatos existem para fazer seguranca*.
Perguntam *quantos artefatos estao inseguros*.

E a distincao exata do Eixo A vs Eixo B de [[Decision Log#D-007]] — que deixa
de ser uma escolha nossa de escopo e passa a ser um **posicionamento
defensavel contra o estado da literatura**.

## O que esta rodada mudou

**1. Temos benchmark de confiabilidade dos dois lados.**

| Estudo | Concordancia | Unidade | Anotadores |
|---|---|---|---|
| [[SeRe - Security-Related Code Review Dataset]] | kappa=0,88 | comentario de revisao | 6 humanos |
| [[Agent Skills in the Wild]] | kappa=0,86 | skill (rotulo unico) | automatico vs. manual |
| **Nosso [[EXP-014]]** | **kappa=0,672** | **`SKILL.md` inteiro, 3 classes** | **2 LLMs** |
| [[SAcoding - Actionability de Conselho de Seguranca]] | 46%-80% | item de conselho | 2 humanos |
| [[LLMs como Anotadores - Confiabilidade]] | kappa=0,233 (LLM-LLM) | texto etnografico | multiplos LLMs |

Nosso numero fica **acima** do que a literatura observa para concordancia
LLM-LLM, e **abaixo** dos estudos com anotador humano especialista, unidade
menor e ancoragem externa. Ambas as comparacoes sao explicaveis e nenhuma e
desfavoravel — desde que reportadas com as diferencas de desenho.

**2. Um trade-off ficou explicito.** O SeRe atinge kappa=0,88 ancorando a
definicao no **CWE**. Poderiamos fazer o mesmo e subir nossa confiabilidade —
ao custo de so encontrar o que CWE ja cataloga, perdendo justamente a categoria
mais caracteristica deste corpus (restricao de comportamento de agente).
**Confiabilidade e cobertura do fenomeno novo estao em tensao direta.** Isso
merece paragrafo proprio no TCC.

## Limitacoes desta rodada

- **Triagem por avaliador unico** (assistida). Sem dupla triagem independente,
  sem concordancia medida na propria selecao.
- **Sem bases indexadas com login** (Scopus, WoS). Trabalho fechado fora de
  indice aberto nao foi alcancado.
- **3 strings por RQ**, nao exaustivas. Sem busca por citacao (backward/forward
  snowballing), que seria o proximo passo natural e provavelmente o de maior
  retorno — especialmente a partir de [[Agent Skills in the Wild]] e do
  [[SAcoding - Actionability de Conselho de Seguranca]].
- **Metade do acervo continua em `resumo-de-busca`.** Esta rodada nao resolveu
  isso; melhorou a rastreabilidade da selecao, nao a profundidade da leitura.

## Proximo passo recomendado

Snowballing a partir das duas referencias com conteudo recuperado, e leitura
direta das que estao marcadas `resumo-de-busca` e que sustentam afirmacao
central — em ordem de prioridade: [[Learning from Disagreement]] (sustenta o
relato em camadas), [[Sampling in Software Engineering Research]] (sustenta o
corte de frame) e [[Identificacao Parcial - Limites de Manski]] (sustenta o
controle de vies).

## Ligacoes

[[Protocolo de Busca]] · `notes/Literature/README.md` · [[Classification and Sampling Precedents]]
