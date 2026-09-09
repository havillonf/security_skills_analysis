---
tipo: literatura
data: 2026-09-03
status: busca inicial — NÃO é revisão sistemática
questao: QI-1
decisoes: D-004, D-006, D-014, D-022, D-026
---

# Precedentes de classificação e amostragem

Fontes levantadas na sessão de 2026-09-03, motivadas por duas perguntas
concretas que apareceram ao consolidar o [[EXP-013]]:

1. alguém já classificou artefatos por **relevância de segurança graduada**
   (primária / secundária / incidental)?
2. como outros trabalhos lidaram com **unidades que não dá para classificar**
   (script ausente, texto insuficiente) ao construir o frame amostral?

> [!warning] Escopo e confiabilidade desta nota
> Busca exploratória em torno de ~6 eixos, **não** revisão sistemática: sem
> protocolo declarado, sem strings de busca versionadas, sem critério de
> inclusão/exclusão. Para ir ao TCC como "trabalhos relacionados" precisa ser
> refeita com protocolo.
>
> **Nível de leitura por fonte** — importa para poder citar:
> - **Lida** (conteúdo recuperado): Agent Skills in the Wild.
> - **Parcial** (metadados/estrutura, conteúdo não confirmado): Prompt Bank.
> - **Somente resumo de busca**: todas as demais. **Não citar sem ler.**

---

## 1. O trabalho mais próximo — e a convergência com nosso núcleo

**Agent Skills in the Wild: An Empirical Study of Security Vulnerabilities at
Scale** — https://arxiv.org/html/2601.10338v1

- 42.447 skills coletadas de dois marketplaces (skills.rest, skillsmp.com);
  31.132 únicas analisadas; **1.218 categorizadas manualmente**.
- Taxonomia de **8 categorias funcionais por propósito pretendido**, uma delas
  *Security/Red-team* (pentest, vulnerability scanning).
- **Security/Red-team = 89 de 1.218 = 7,3%.**
- Concordância: **κ=0,86** (categorização), κ=0,83 (presença binária de
  vulnerabilidade), κ=0,79 (categoria de vulnerabilidade).

**Convergência externa.** Nossa camada `PRIMARY` no [[EXP-013]] deu 6,6% / 6,6%
/ 7,7% nos três modelos. Estudo independente, outro dataset, outro método,
mesmo patamar. Corrobora que `security_focus` mede algo real e estável.

**Diferença metodológica decisiva.** A taxonomia deles é de **rótulo único e
mutuamente exclusivo** — uma skill é *Development Tools* **ou**
*Security/Red-team*, nunca as duas. **Não existe equivalente de `SECONDARY`.**
Um `code-review` com seção de OWASP cairia em *Development Tools*.

Consequência para nossa defesa: o κ=0,86 deles é de uma tarefa mais fácil
(propósito dominante em rótulo único), que corresponde ao nosso
`security_focus` — onde também temos κ=0,942. O κ=0,370 aparece porque medimos
o que essa literatura não mede. **O kappa alto deles vem de contornar a
fronteira difícil, não de resolvê-la.**

**Não há sobreposição de escopo:** eles estudam vulnerabilidades *nas* skills
(Eixo B de [[Decision Log#D-007]]); a QI-1 estuda skills que *fazem* segurança
(Eixo A).

Eles também reportam um problema análogo ao nosso: *"Security/Red-team
conflation — nossa detecção corretamente as identifica como perigosas mas não
consegue determinar intenção."*

### Adjacentes (mesma onda, não lidos)

- Agent Skill Security: Threat Models, Attacks, Defenses, and Evaluation — https://arxiv.org/html/2607.13987v1
- Prompt Injection Attacks on Agentic Coding Assistants — https://arxiv.org/pdf/2601.17548
- Agent Skills for LLMs: Architecture, Acquisition, Security — https://arxiv.org/html/2602.12430
- MCP-38: A Comprehensive Threat Taxonomy for Model Context Protocol Systems — https://arxiv.org/pdf/2603.18063

---

## 2. Precedente para o desenho de [[Decision Log#D-026]]

**A Validated Prompt Bank for Malicious Code Generation: Separating Executable
Weapons from Security Knowledge in 1.554 Consensus-Labeled Prompts** —
https://arxiv.org/pdf/2605.03179

Usa **rotulagem por consenso de LLMs com adjudicação humana**, reportando
Fleiss' κ e Krippendorff's α — mesma arquitetura de D-026. Serve para
justificar o desenho perante orientador/banca.

A distinção do título (*executable weapons* vs. *security knowledge*) é irmã
conceitual do nosso eixo **ativo/passivo** e do campo `operation_level`
(`executable` vs. `reasoning`).

⚠️ Leitura apenas parcial — confirmar números antes de citar.

---

## 3. Discordância como sinal, não ruído

Sustenta reportar a QI-1 **em camadas com confiabilidade declarada** em vez de
um número único, e tratar o κ=0,370 como achado sobre o construto.

- **Learning from Disagreement: A Survey** (JAIR) — https://www.jair.org/index.php/jair/article/download/12752/26751/29240
- **Beyond Consensus: Perspectivist Modeling and Evaluation of Annotator Disagreement in NLP** — https://arxiv.org/html/2601.09065v1
- **LeWiDi** (*Learning with Disagreement*), SemEval 2021 e 2023 — avalia
  sistemas pela capacidade de reproduzir a **distribuição** de anotadores, não
  o voto majoritário.

Tese central: quando anotadores especialistas discordam de forma persistente,
isso reflete **ambiguidade real do conceito**, não erro de medição.

---

## 4. Construção do frame e critérios de exclusão

Precedente para a **etapa 2** do pipeline (corte de skills sem evidência
classificável) e para fechar [[Decision Log#D-022]].

- **Sampling in Software Engineering Research: A Critical Review and
  Guidelines** (Baltes & Ralph, EMSE) — https://link.springer.com/article/10.1007/s10664-021-10072-8
  · preprint: https://arxiv.org/pdf/2002.07764

  Achados relevantes: amostragem aleatória é **rara** em ESE, estratégias
  sofisticadas são **muito raras**, e *"amostragem, representatividade e
  aleatoriedade frequentemente aparecem mal compreendidas"*. Tamanhos de frame
  reportados variam de 3 a 2.000.000, **mediana 395**.

  → Posiciona o Desenho C ([[Decision Log#D-014]]) como rigoroso em relação à
  prática dominante da área, e nosso frame (1,57M) como caso extremo de escala.

- **On the Creation of Representative Samples of Software Repositories** — https://arxiv.org/html/2410.00639

**Prática estabelecida:** declarar lista explícita de critérios de inclusão e
exclusão, e filtrar artefatos triviais é **padrão aceito** — exemplos reais na
literatura excluem repos com <5 contribuidores, <100 commits, <10 stars e
<10 forks, arquivados ou desabilitados. O que a área exige não é ausência de
corte, é **corte declarado e justificado**.

→ Nosso corte (`length(description) + body_chars < 200`, 25.284 = 1,35%) é
conservador frente a esses exemplos.

---

## 5. Unidades não codificáveis — precedente direto

O problema do **script ausente** tem nome na análise de conteúdo clássica.

A metodologia de content analysis distingue três problemas na seleção de
documentos: **documentos ausentes, documentos inapropriados e documentos não
codificáveis** — sendo que *"unidades podem ser não codificáveis porque contêm
passagens ausentes ou conteúdo ambíguo"*.

- Content Analysis: A Methodology for Structuring and Analyzing Written
  Material (GAO/PEMD-10.3.1) — https://www.govinfo.gov/content/pkg/GAOREPORTS-PEMD-10-3-1/html/GAOREPORTS-PEMD-10-3-1.htm
- Practical Resources for Assessing and Reporting Intercoder Reliability in
  Content Analysis Research Projects (Lombard et al.) — https://www.researchgate.net/publication/242785900_Practical_Resources_for_Assessing_and_Reporting_Intercoder_Reliability_in_Content_Analysis_Research_Projects

**Precedente que valida a decisão do pesquisador (2026-09-03):** "não
codificável" é tratado como **problema de seleção de documento**, resolvido no
estágio do frame — **não** como uma categoria do esquema de codificação. É
exatamente mover `AMBIGUOUS` de classe para exclusão de frame.

> [!danger] Alerta que essa literatura levanta contra nós
> *"A unidade de análise deve ser decidida e pilotada **antes** da codificação
> em escala começar, não ajustada no meio — uma mudança a meio caminho
> invalida os números de confiabilidade calculados sob a unidade antiga."*
>
> O [[EXP-013]] **é** o piloto, então mudar agora é legítimo. Mas os números
> de confiabilidade medidos (κ=0,370 etc.) pertencem ao **Codebook v2.3**.
> Qualquer esquema novo precisa de **medição própria de confiabilidade** —
> não se pode herdar nem assumir melhora.

---

## 6. Identificação parcial — como reportar o que foi excluído

Sustenta a recomendação de reportar a prevalência como **intervalo limitado**
(assumindo que todos os excluídos são segurança / que nenhum é), em vez de
assumir que a exclusão foi inofensiva.

- **Embracing Uncertainty: The Value of Partial Identification in Public Health
  and Clinical Research** — https://pmc.ncbi.nlm.nih.gov/articles/PMC10799552/
- **HIV Estimation Using Population-Based Surveys with Non-Response: A Partial
  Identification Approach** — https://www.medrxiv.org/content/10.1101/2023.06.03.23290936.full.pdf
- Partial identification with missing data: concepts and findings (Manski) — https://www.researchgate.net/publication/223625728_Partial_identification_with_missing_data_Concepts_and_findings

**Analogia direta:** estimar prevalência quando parte das unidades não pode ser
medida é o problema de prevalência de HIV com não resposta. A epidemiologia
resolve com **limites que não dependem de suposições não testáveis** sobre o
mecanismo de ausência, em vez de imputar ou ignorar.

Como o conjunto excluído aqui é fração de 0,75% (skills com
`composition_truncated = 1` **e** `has_scripts = 1`), o intervalo deve sair
**estreito** — o que transforma "a exclusão foi inofensiva" de suposição em
**demonstração**.

---

## 7. Lacuna encontrada

**Não foi localizado nenhum trabalho que use escala ordinal graduada de
relevância de segurança** (primária / secundária / incidental / nenhuma) para
artefatos de software. As taxonomias de segurança existentes classificam por
**função** — o que corresponde ao nosso `security_functions`, não a
`security_relevance`:

- Classification of Software Security Tools (CEUR Vol-2933) — https://ceur-ws.org/Vol-2933/paper28.pdf
- SAMATE Tool Taxonomy (NIST) — https://www.nist.gov/itl/csd/secure-systems-and-applications/samate-tool-taxonomy
- A Practical Approach to the Automatic Classification of Security-Relevant Commits — https://arxiv.org/pdf/1807.02458
- Improved Labeling of Security Defects in Code Review by Active Learning with LLMs (EASE '25) — https://dl.acm.org/doi/10.1145/3756681.3756986

**Leitura dupla, ambas necessárias:**

- **Oportunidade** — o construto ordinal parece genuinamente novo; ninguém
  mediu "segurança como capacidade secundária" em escala.
- **Aviso** — talvez ninguém tenha tentado porque é difícil, e o [[EXP-013]]
  acabou de medir o quanto. Sem precedente não há âncora externa de
  calibração, e a banca vai cobrar justificativa.

---

## Ligações

[[EXP-013]] · [[Decision Log]] · [[Codebook]] · [[QI-1 Methodology]] ·
[[03 - Methodology]] · [[Multilingual Methodology Review]]
