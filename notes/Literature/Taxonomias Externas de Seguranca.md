---
tipo: literatura
leitura: resumo-de-busca
usado-em: QI-3 (crosswalk) — NAO usar antes disso
---

# Taxonomias externas de seguranca

- **Classification of Software Security Tools** (CEUR Vol-2933) —
  https://ceur-ws.org/Vol-2933/paper28.pdf
- **SAMATE Tool Taxonomy** (NIST) —
  https://www.nist.gov/itl/csd/secure-systems-and-applications/samate-tool-taxonomy
- **A Practical Approach to the Automatic Classification of Security-Relevant
  Commits** — https://arxiv.org/pdf/1807.02458
- **Improved Labeling of Security Defects in Code Review by Active Learning
  with LLMs** (EASE '25) — https://dl.acm.org/doi/10.1145/3756681.3756986

## O que sao

Taxonomias e classificadores que organizam seguranca **por funcao**: SAST,
DAST, scanner de vulnerabilidade — ou que classificam artefatos (commits,
defeitos) como relevantes ou nao para seguranca.

## No que nos ajudaram — e o principal e uma proibicao

**1. Delimitam o que NAO deve entrar agora.** Estas taxonomias correspondem ao
campo `security_functions`, nao a `security_relevance`. Foi ao reconhecer que
`PREVENT·DETECT·ASSESS·TEST·RESPOND·RECOVER` e derivado do **NIST CSF** que
removemos esse campo do instrumento em [[Decision Log#D-029]]: coleta-lo
durante a classificacao e depois alimentar o open coding seria a circularidade
que a regra inegociavel da QI-2 proibe.

**O lugar delas e a QI-3**, como crosswalk, **depois** da taxonomia empirica
estabilizada. Antes disso, encontrariamos o que fomos procurar.

**2. Documentam uma lacuna.** Nao foi localizado nenhum trabalho usando escala
ordinal graduada de **relevancia** de seguranca (primaria / secundaria /
incidental / nenhuma) para artefatos de software. As taxonomias existentes
classificam por funcao, nao por centralidade.

Leitura dupla, ambas necessarias: e **oportunidade** (o construto ordinal
parece novo) e e **aviso** (talvez ninguem tenha tentado porque e dificil — e o
[[EXP-013]] mediu o quanto).

## Ressalva

**Todas lidas apenas por resumo de busca.**

## Ligacoes

[[Decision Log#D-029]] · [[QI-3 Coverage Methodology]] · [[Taxonomy Coding Protocol]]
