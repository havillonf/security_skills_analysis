---
tipo: protocolo
questao: trabalhos relacionados (QI-1)
version: 1.0
data: 2026-09-05
status: declarado antes da execucao desta rodada
---

# Protocolo de busca — trabalhos relacionados

> [!important] O que este documento é, e o que não é
> Uma **revisão estruturada**: protocolo declarado antes da execução, strings
> versionadas, critérios explícitos, seleção registrada com motivo.
>
> **Não é uma revisão sistemática** no sentido estrito: não há dupla triagem
> por avaliadores independentes, não há busca em múltiplas bases indexadas
> (Scopus, WoS, ACM DL, IEEE Xplore) com strings adaptadas por base, e não há
> fluxo PRISMA completo com contagem de duplicatas. Descrever como
> "sistemática" no texto seria superdeclarar.
>
> É reprodutível e auditável — o que a rodada exploratória anterior não era.

## 1. Perguntas da revisão

| | Pergunta | Por que o projeto precisa |
|---|---|---|
| **RQ-A** | Existe trabalho que meça **prevalência** de conteúdo de segurança numa população de artefatos de software? | Saber se a QI-1 já foi respondida, e contra que número comparar |
| **RQ-B** | Que **esquemas de classificação** de relevância de segurança existem, e que **confiabilidade** reportam? | Posicionar o Codebook e calibrar o que é κ aceitável neste construto |
| **RQ-C** | Que precedentes existem para **anotação assistida por LLM com adjudicação humana**? | Justificar o desenho de [[Decision Log#D-026]] |

## 2. Fontes

- Busca web indexada (motor do agente), que alcança arXiv, ACM DL, IEEE,
  SpringerLink, ScienceDirect, PMC e repositórios abertos.
- **Limitação declarada:** sem acesso a bases com login (Scopus, Web of
  Science). Trabalho fechado que não apareça em índice aberto **não é
  alcançado** por esta busca.

## 3. Strings de busca

Versionadas. Executadas em 2026-09-05.

### RQ-A — prevalência

```
A1  prevalence security-related artifacts proportion corpus empirical study software
A2  "how many" OR "what fraction" repositories packages security-focused empirical measurement
A3  agent skills OR prompt library security purpose classification prevalence
```

### RQ-B — esquemas e confiabilidade

```
B1  security relevance classification scheme coding reliability kappa software artifacts
B2  taxonomy security concerns software documentation inter-rater agreement empirical
B3  classify commits OR issues OR documentation "security-related" annotation guidelines agreement
```

### RQ-C — anotação assistida por LLM

```
C1  LLM annotation agreement human adjudication content analysis reliability
C2  large language models as annotators inter-rater agreement human validation
C3  multi-model consensus labeling human adjudication dataset construction
```

## 4. Critérios

### Inclusão (todos)

- **I1** — trata de **classificação/anotação de artefatos** (código, commits,
  documentação, políticas, skills, prompts) quanto a segurança, **ou** de
  metodologia de anotação diretamente aplicável a isso.
- **I2** — reporta **método** (esquema, critérios, procedimento) ou **medida**
  (prevalência, concordância), não apenas resultado narrativo.
- **I3** — texto acessível o suficiente para extrair o método.

### Exclusão (qualquer uma)

- **E1** — trata de **detectar vulnerabilidades** em artefatos, sem
  classificar o artefato quanto ao seu **propósito** de segurança.
  *(Corta a maior parte da literatura de SAST/scanners — é o Eixo B de
  [[Decision Log#D-007]], não a nossa pergunta.)*
- **E2** — proposta de ferramenta sem avaliação de método.
- **E3** — não revisado por pares **e** sem método reproduzível descrito.
- **E4** — sobreposição total com item já incluído (mesma equipe, mesmo
  estudo).

> [!note] E1 é o critério que mais corta, e é deliberado
> "Segurança" na literatura de engenharia de software quase sempre significa
> *encontrar falhas*. A QI-1 pergunta outra coisa: *quantos artefatos existem
> para fazer segurança*. Sem E1 a revisão traria centenas de itens
> irrelevantes.

## 5. Processo de seleção

1. Executar cada string; registrar todos os títulos retornados.
2. Triagem por título/resumo contra I1–I3 e E1–E4.
3. Para os que passam: recuperar conteúdo e registrar `leitura:` real
   (`conteudo-recuperado` · `parcial` · `resumo-de-busca`).
4. Extrair para nota individual em `notes/Literature/`.
5. Registrar os **excluídos com motivo** — a exclusão é parte do resultado.

**Triagem por um único avaliador (o pesquisador, assistido).** É ameaça à
validade e está declarada; uma revisão sistemática exigiria dupla triagem com
concordância medida.

## 6. Extração

Cada nota incluída registra: o que é · intuito dos autores · **no que nos
ajudou**, com a decisão ou número concreto que sustenta · ressalvas · nível de
leitura.

## 7. Rodada anterior (exploratória) — como foi tratada

Antes deste protocolo houve uma busca exploratória (2026-09-03/04) que
produziu 9 notas. Elas **não foram descartadas**: foram reavaliadas contra
I1–I3/E1–E4 nesta rodada, e o resultado dessa reavaliação está em
[[Resultado da Busca]]. Referências que não passariam nos critérios estão
marcadas lá.

## Ligações

[[Resultado da Busca]] · [[Classification and Sampling Precedents]] ·
`notes/Literature/README.md`
