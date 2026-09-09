---
tipo: literatura
leitura: resumo-de-busca
usado-em: relato da QI-1 em camadas, interpretacao do kappa
---

# Discordancia como sinal, nao ruido

Conjunto de referencias em NLP que trata desacordo entre anotadores como
**informacao**, nao erro de medicao.

- **Learning from Disagreement: A Survey** (JAIR) —
  https://www.jair.org/index.php/jair/article/download/12752/26751/29240
- **Beyond Consensus: Perspectivist Modeling and Evaluation of Annotator
  Disagreement in NLP** — https://arxiv.org/html/2601.09065v1
- **LeWiDi** (*Learning with Disagreement*), tarefa compartilhada no
  SemEval 2021 e 2023

## Intuito

Contestar a pratica dominante de agregar anotacoes num rotulo unico por voto
majoritario. Propoem preservar a **distribuicao** de anotadores (soft labels),
e avaliar sistemas pela capacidade de reproduzi-la.

## Tese central

> Quando anotadores especialistas discordam de forma **persistente**, isso
> reflete **ambiguidade real do conceito**, nao incompetencia nem erro de
> medicao.

## No que nos ajudou

Da respaldo teorico para reportar a QI-1 **em camadas com a confiabilidade de
cada uma declarada**, em vez de um numero unico — e para tratar o kappa do
[[EXP-013]] como **achado sobre os limites do construto** em vez de fracasso a
esconder.

Sem essa literatura, "nosso instrumento teve kappa=0,37" e confissao de
fraqueza. Com ela, e observacao sobre a natureza da categoria "skill de
seguranca" — que e resultado, e possivelmente contribuicao.

## Ressalvas

**Lidas apenas por resumo de busca.** Ler ao menos a survey da JAIR antes de
citar, ja que seria a citacao de sustentacao do argumento central.

Vem de NLP, sobre tarefas subjetivas (toxicidade, sarcasmo, postura). A
transferencia para classificacao de artefato tecnico e plausivel mas precisa
ser argumentada, nao assumida.

## Ligacoes

[[EXP-013]] · [[EXP-014]] · [[QI-1 Methodology]]
