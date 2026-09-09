---
tipo: literatura
leitura: resumo-de-busca
usado-em: D-028, justificativa do Desenho C
---

# Sampling in Software Engineering Research

**Baltes & Ralph**, *Empirical Software Engineering* —
https://link.springer.com/article/10.1007/s10664-021-10072-8
· preprint: https://arxiv.org/pdf/2002.07764

> *A Critical Review and Guidelines*

## O que e

Revisao critica de como a pesquisa em engenharia de software faz amostragem,
com diretrizes. Analisa as estrategias efetivamente usadas em artigos
publicados na area.

## Intuito dos autores

Documentar que a area trata amostragem de forma frouxa, e oferecer vocabulario
e diretrizes para corrigir.

## No que nos ajudou

**1. Posiciona o rigor do nosso desenho.** Achados deles: amostragem aleatoria
e **rara** em ESE; estrategias sofisticadas sao **muito raras**; e
*"amostragem, representatividade e aleatoriedade frequentemente aparecem mal
compreendidas"*. Tamanhos de frame vao de 3 a 2.000.000, **mediana 395**.

Isso enquadra o Desenho C ([[Decision Log#D-014]]) como rigoroso frente a
pratica dominante, e nosso frame (1,57M) como caso extremo de escala.

**2. Sustenta o corte de elegibilidade.** Filtrar artefatos triviais com
criterio **declarado** e pratica aceita — exemplos na literatura excluem repos
com <5 contribuidores, <100 commits, <10 stars. A area nao exige ausencia de
corte, exige corte **declarado e justificado**. Nosso corte de
[[Decision Log#D-028]] (1,35%) e conservador frente a esses exemplos.

## Ressalva

**Lida apenas por resumo de busca.** Os numeros citados (mediana 395, faixa
3-2.000.000) vieram de resultado de busca, nao do texto. **Ler antes de citar
no TCC.**

## Ligacoes

[[Decision Log#D-028]] · [[Decision Log#D-014]] · [[Classification and Sampling Precedents]]
