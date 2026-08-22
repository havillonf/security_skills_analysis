---
tipo: overview
atualizado: 2026-08-22
status: exploração inicial concluída
---

# Research Overview

> [!warning] Estado
> **[[Decision Log#D-004|D-004]]** decidida e **[[Decision Log#D-006|revisada por
> D-006]]** (2026-08-22): existe definição de Security Skill, cinco classes
> (`PRIMARY`/`SECONDARY`/`MENTION`/`NONE`/`AMBIGUOUS`) e dimensões independentes,
> operacionalizadas no [[Codebook]] v2.0.
> A **questão central ainda não está escolhida** — [[QI-2 Methodology|QI-2]] é a
> candidata preferida do pesquisador, a alinhar com o orientador
> ([[2026-08-22 - Pauta para o Orientador]]). O codebook ainda **não passou pelo
> piloto**. Nenhum número deve ser apresentado como achado enquanto não houver
> métricas contra padrão-ouro anotado.

## Tema

Skills agênticas (`SKILL.md`) públicas no GitHub, analisadas pela lente da
segurança no desenvolvimento com IA. Fonte única: dataset [[GitSkills]].

Uma *agent skill* e uma pasta com um `SKILL.md` contendo instruções em linguagem
natural para um agente LLM, opcionalmente com scripts e arquivos de referência. O
agente carrega a skill quando julga que a tarefa corresponde a descrição. Formato
publicado pela Anthropic em outubro de 2025 como especificação aberta.

O que torna o artefato interessante para engenharia de software empírica: e
**linguagem natural**, **selecionado probabilisticamente em tempo de execução**,
distribuído **sem package manager, sem assinatura e sem registro**, e **não
verificado por compilador algum**.

## Objetivo declarado

Do README: *"avaliar as skills agênticas que se relacionam com segurança no
desenvolvimento com IA, buscando identificar falhas, lacunas ou padrões
relevantes"*.

Amplo demais para ser executável como esta. O refinamento está em
[[01 - Research Question]].

## Unidade de análise - ainda em aberto

Candidatas, com consequências diferentes:

| Unidade | n | Implicação |
|---|---|---|
| Ocorrência de arquivo | 3.797.117 | conta cópias; poucas skills populares dominam |
| **Conteúdo distinto** (representante) | 1.877.981 | 1 voto por texto; padrão recomendado |
| Repositório | 282.200 | ecossistema de projetos |
| Conta/dono | 195.841 | ecossistema de autores |

Recomendação atual: **conteúdo distinto** como unidade primária, com contagem por
ocorrência reportada em paralelo como medida de difusão. Ver [[Decision Log#D-001]].

## O que já se sabe (verificado)

Tudo abaixo vem de [[EXP-001]] / `results/EXP-001_profile.json`. Nada vem do
notebook legado.

- Estrutura do dataset e integridade referencial: intactas, zero órfãos.
- 52,93% dos representantes citam ao menos uma keyword de segurança no corpo.
- 4,09% dos que tem `name`/`description` preenchidos (n=1.625.701) declaram
  segurança nesses campos.
- 11,4% dos representantes empacotam scripts executáveis.
- 60,8% das ocorrências são cópias de um conteúdo que aparece mais de uma vez —
  e **near-duplicates sobrevivem à deduplicação por hash** ([[EXP-002]]).
- 78,69% dos representantes citam algum termo de segurança: recuperação por keyword
  não é filtro útil.
- 59,3% dos repositórios tem zero stars.

## O que foi invalidado

O notebook `01_exploratory.ipynb` conclui "1,1% das skills mencionam segurança".
**Inválido** - erro de amostragem, ver [[EXP-001]] e [[Decision Log#D-002]].
Valor correto com as mesmas keywords: 52,93%.

## Contribuição potencial

Ainda não é reivindicação, e hipótese de contribuição: o paper do GitSkills lista
usos pretendidos mas não os executa. A lacuna mais promissora é **segurança da
própria skill como artefato** - permissões declaradas (`allowed-tools`), scripts
empacotados, e divergência entre cópias num ecossistema sem registro. Ver a skill
`security-analysis`.

## Mapa

- [[Codebook]] - definição de Security Skill, classes, dimensões, regras R-1..R-8
- [[QI-2 Methodology]] - open coding bottom-up, amostragem, denominadores
- [[QI-3 Coverage Methodology]] - crosswalk, aplicabilidade, níveis de cobertura
- [[Security Taxonomy]] - taxonomia emergente (v0.1, preliminar)
- [[EXP-002]] - candidate retrieval, amostra de descoberta, near-duplicates
- [[01 - Research Question]] - questões, separadas por procedência
- [[02 - Hypotheses]] - hipóteses candidatas, nenhuma testada
- [[03 - Methodology]] - plano de pesquisa em etapas
- [[GitSkills]] - dataset, colunas, limitações
- [[Decision Log]] - decisões metodológicas
- [[EXP-001]] - profiling estrutural e invalidação do resultado anterior
