---
tipo: questões
atualizado: 2026-08-22
status: não operacionalizada
---

# Research Questions

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

**QI-1. Qual a prevalência de skills de segurança na população pública de agent
skills?** Objetivo direto do notebook. O critério já está definido
([[Decision Log#D-004]], [[Codebook]]): Security Skill = `SEC-PRIMARY` +
`SEC-SECONDARY`. **A resposta ainda não é obtível** - depende de classificador
validado contra padrão-ouro. E deve ser reportada com PRIMARY e SECONDARY
desagregados, já que SECONDARY tende a dominar.

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

## Avaliação

QI-1 e a mais óbvia e a mais fragil: vira exercicio de definição, e a resposta e
determinada pelo critério mais do que pelo dado.

QP-1, QP-2 e QP-5 medem **propriedades declaradas ou estruturais** das skills. Não
dependem de julgar se uma skill "e de segurança" - o ponto fraco de QI-1/QI-2/QI-3.
São mais defensáveis num TCC e mais originais.

QP-3 e a de maior impacto potencial e maior risco metodológico. Só vale a pena com
a restrição temporal explícita, e o resultado provável e descritivo ("cópias
divergem em X% dos casos; em Y% a divergência envolve execução"), não causal.

**Recomendação:** uma questão central de QP-1/QP-2 mais QI-1 como caracterização
descritiva de contexto. Decisão do pesquisador.

## Ligações

[[00 - Research Overview]] · [[02 - Hypotheses]] · [[Decision Log]] · [[EXP-001]]
