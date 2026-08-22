---
tipo: overview
atualizado: 2026-08-22
status: exploração inicial concluída
---

# Research Overview

> [!important] Questão central: **QI-1** ([[Decision Log#D-011]], 2026-08-22)
> **Qual a prevalência de skills de segurança na população pública de Agent Skills?**
>
> Security Skill = `SEC-PRIMARY` + `SEC-SECONDARY` ([[Codebook]] v2.1), sempre
> desagregados. População: **todos os idiomas** ([[Decision Log#D-012]]).
> Desenho: [[QI-1 Methodology]] · Idiomas: [[Multilingual Strategy]] ·
> Plano: [[03 - Methodology]]
>
> QI-2 e QI-3 preservadas como extensões futuras
> ([[01 - Research Question]]§Extensões).

> [!warning] Nenhum resultado ainda
> O codebook **não passou pelo piloto** e não existe padrão-ouro. Nenhum número deste
> projeto é resposta à QI-1. Em particular, **52,93%** (keyword) e **78,69%**
> (candidate retrieval) são números exploratórios — **não são prevalência**
> ([[QI-1 Methodology]] §7).

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

Recomendação vigente: **conteúdo distinto** como unidade primária, com contagem por
ocorrência reportada em paralelo como medida de difusão. Ver [[Decision Log#D-001]] —
inclusive a ressalva sobre near-duplicates, que enfraquece a premissa "1 voto por
texto" sem invalidar a escolha.

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
- **14,21% ± 0,48 pp da população não é escrita em inglês** (≈ 267 mil conteúdos);
  chinês sozinho é 5,99%. Ver [[EXP-003]].

## O que foi invalidado

O notebook `01_exploratory.ipynb` conclui "1,1% das skills mencionam segurança".
**Inválido** - erro de amostragem, ver [[EXP-001]] e [[Decision Log#D-002]].
Valor correto com as mesmas keywords: 52,93%.

## Contribuição potencial

Ainda hipótese, não reivindicação. O paper do GitSkills lista usos pretendidos e não
executa nenhum.

Sob a QI-1, a contribuição plausível é **uma estimativa de prevalência defensável e
reproduzível** onde hoje só existem contagens de keyword — com critério fixado antes
da medição, incerteza quantificada, e cobertura multilíngue explícita. O contraste
com os números exploratórios é o próprio ponto: 52,93% por keyword contra uma
estimativa validada mostram o tamanho do erro que a abordagem ingênua comete.

Preservadas como extensões: segurança **da própria skill** como artefato
(`allowed-tools`, scripts empacotados, divergência entre cópias) — ver
[[01 - Research Question]]§Extensões e a skill `security-analysis`.

## Mapa

- [[QI-1 Methodology]] - **questão central**: desenho amostral e estimador
- [[Multilingual Strategy]] - população multilíngue, detecção, gold set, riscos
- [[Codebook]] - definição de Security Skill, classes, dimensões, regras R-1..R-9
- [[QI-2 Methodology]] - open coding bottom-up, amostragem, denominadores
- [[QI-3 Coverage Methodology]] - crosswalk, aplicabilidade, níveis de cobertura
- [[Security Taxonomy]] - taxonomia emergente (v0.1, preliminar)
- [[EXP-002]] - candidate retrieval, amostra de descoberta, near-duplicates
- [[EXP-003]] - distribuição de idiomas da população
- [[01 - Research Question]] - questões, separadas por procedência
- [[02 - Hypotheses]] - hipóteses candidatas, nenhuma testada
- [[03 - Methodology]] - plano de pesquisa em etapas
- [[GitSkills]] - dataset, colunas, limitações
- [[Decision Log]] - decisões metodológicas
- [[EXP-001]] - profiling estrutural e invalidação do resultado anterior
