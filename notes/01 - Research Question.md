---
tipo: questões
atualizado: 2026-08-22
status: QI-1 adotada como questão central
---

# Research Questions

> [!important] Questão central: **QI-1** (desde 2026-08-22)
> **Qual a prevalência de skills de segurança na população pública de Agent Skills?**
>
> Security Skill = **`SEC-PRIMARY` + `SEC-SECONDARY`** ([[Codebook]] v2.1), com as
> duas classes **sempre reportadas separadamente** além do agregado.
> População: **todos os idiomas** ([[Decision Log#D-012]]).
> Decisão: [[Decision Log#D-011]] · Metodologia: [[QI-1 Methodology]]
>
> **QI-2 e QI-3 permanecem documentadas como extensões futuras** — ver §Extensões.

> [!important] Procedência
> Separado por origem. **Nada abaixo de "Inferidas" ou "Propostas" foi definido
> pelo pesquisador** - são leituras minhas do material e precisam de confirmação,
> rejeição ou reescrita antes de virar objetivo do TCC.

---

## Explicitamente definido no projeto

Do README, única formulação existente:

> "Avaliar as skills agênticas (arquivos `SKILL.md`) que se relacionam com
> **segurança no desenvolvimento com IA**, buscando identificar falhas, lacunas ou
> padrões relevantes."

Não e uma questão de pesquisa: não define população, variável, comparação nem
critério de resposta. "Falhas, lacunas ou padrões" cobre três objetivos distintos.

O notebook adiciona uma intenção operacional implicita: **medir a prevalência** de
skills de segurança por keywords. Essa tentativa produziu resultado inválido
([[Decision Log#D-002]]) e o método tem validade insuficiente
(skill `security-analysis`).

---

## Inferidas do material existente

Leituras minhas do README, do notebook e do paper do GitSkills.

**QI-1. Qual a prevalência de skills de segurança na população pública de Agent
Skills?** ⭐ **Questão central adotada** ([[Decision Log#D-011]]).

Critério definido ([[Decision Log#D-004]], [[Codebook]] v2.1): Security Skill =
`SEC-PRIMARY` + `SEC-SECONDARY`. **A resposta ainda não é obtível** — exige
estimativa com incerteza estatística a partir de amostra anotada e classificador
validado contra padrão-ouro, não contagem de keyword. Desenho completo em
[[QI-1 Methodology]].

Reportada sempre com `PRIMARY` e `SECONDARY` desagregados (SECONDARY tende a
dominar), por conteúdo distinto e por ocorrência, e com a taxa de `AMBIGUOUS` à
parte.

**QI-2. Que tipos de preocupação de segurança as skills expressam, e como se
distribuem?** Implícita em "identificar padrões". **Metodologia definida em
[[QI-2 Methodology]]** — bottom-up, open coding, taxonomia emergente em
[[Security Taxonomy]]. Iniciada: candidate retrieval medido e amostra de descoberta
gerada ([[EXP-002]]). **Nenhuma distribuição calculada.**

**QI-3. Que lacunas existem - o que as skills de segurança *não* cobrem?**
Implícita em "identificar lacunas". Metodologicamente a mais difícil.
**Metodologia definida em [[QI-3 Coverage Methodology]]** — top-down, crosswalk com
referenciais externos escolhidos com justificativa, **denominador condicional por
aplicabilidade**, escala de seis níveis de cobertura, e tratamento obrigatório de
"ausência de evidência ≠ evidência de ausência". **Bloqueada por desenho** até a
taxonomia da QI-2 estabilizar.

---

## Propostas por mim

Não estão no material. Ofereco porque são mensuráveis com este dataset e atacam
lacunas que o paper do GitSkills declara mas não executa.

**QP-1. Que permissões as agent skills declaram, e há excesso de privilegio?**
`allowed-tools` aparece no front matter de ~10% de uma amostra de 2.000. Permite
medir escopo declarado e comparar com o que o corpo da skill de fato pede. Não
depende de classificar dominio.

**QP-2. Skills que empacotam scripts executáveis diferem em risco das de texto
puro?** 214.507 representantes (11,4%) tem `has_scripts = 1`, com o texto dos
scripts em `artifact_siblings`. Superficie de execução concreta e observável.

**QP-3. Cópias divergentes introduzem execução de comando ou acesso de rede ausentes
no ancestral?** E o analogo de ataque de supply chain que o paper sugere para um
ecossistema sem registro. 388.501 conteúdos tem cópias. **Ressalva seria:** a
direção temporal só e defensável para os 458.548 arquivos com histórico, e esse
subconjunto e enviesado (MNAR). Sem isso não se sabe qual cópia veio antes -
divergência sozinha não sustenta afirmação de ataque.

**QP-4. Skills de segurança são mantidas melhor que as demais?** `commit_count`,
`first_commit_at`, `last_commit_at` permitem medir churn e staleness. Mesma
ressalva MNAR de QP-3.

**QP-5. Parte do ecossistema já reconhece o risco?** Os campos `risk` (~2,8%) e
`disable-model-invocation` (~3,0%) aparecem no front matter sem estar na spec
original - sinal de convenção emergente de segurança. Questão pequena, mas barata e
possivelmente original.

---

## Extensões futuras

Preservadas, com dependências registradas. Nenhuma é caminho crítico da QI-1, e o
trabalho já feito nelas é reaproveitável.

| Questão | Estado | Depende de |
|---|---|---|
| **QI-2** — tipos de preocupação e distribuição | metodologia escrita; candidate retrieval medido; [[Security Taxonomy]] v0.1 não validada | classificação validada da QI-1 fornece a base; taxonomia precisa de open coding humano |
| **QI-3** — lacunas de cobertura | metodologia escrita; não iniciada | QI-2 estabilizada + [[Decision Log#D-009]] |
| **QP-1** — permissões declaradas (`allowed-tools`) | não iniciada | independente; instrumentação própria |
| **QP-2** — skills com scripts empacotados | não iniciada | independente |
| **QP-3** — divergência entre cópias | não iniciada | limitada por MNAR do histórico |
| **QP-4** — manutenção de skills de segurança | não iniciada | classificação da QI-1 + histórico (MNAR) |
| **QP-5** — convenções emergentes (`risk`, `disable-model-invocation`) | não iniciada | independente; barata |

QP-4 é a extensão mais natural depois da QI-1: reusa exatamente a mesma
classificação, só acrescenta as variáveis de histórico.

## Avaliação (registro histórico, anterior a D-011)

> [!note] Superada pela decisão do pesquisador
> Este parágrafo é mantido por rastreabilidade. Ele recomendava QP-1/QP-2 como eixo
> central, com QI-1 apenas como caracterização de contexto. O pesquisador decidiu
> pela **QI-1 como questão central** ([[Decision Log#D-011]]).

A objeção registrada na época era: *"QI-1 é a mais óbvia e a mais frágil: vira
exercício de definição, e a resposta é determinada pelo critério mais do que pelo
dado."*

**Como a objeção fica endereçada.** A fragilidade é real e não desaparece — mas é
mitigável, e o desenho de [[QI-1 Methodology]] a ataca de frente:

1. O critério está **fixado por escrito e antes da medição** ([[Codebook]] v2.1), o
   que impede ajustá-lo depois de ver o resultado.
2. `PRIMARY` e `SECONDARY` são reportados **separadamente**, então o leitor vê o
   efeito da escolha de agregação em vez de recebê-la embutida.
3. `AMBIGUOUS` é reportado com **limites inferior e superior**, tornando explícita a
   parcela da estimativa que depende de julgamento.
4. Sensibilidade a definições alternativas entra como **robustness check**.

Continua valendo o alerta: se a estimativa mudar muito sob critérios plausíveis
alternativos, **isso é o achado** e deve ser reportado como tal.

## Ligações

[[00 - Research Overview]] · [[02 - Hypotheses]] · [[Decision Log]] · [[EXP-001]]
