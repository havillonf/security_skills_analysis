---
tipo: instrumento
questao: QI-2 (alimenta QI-1 e QI-3)
version: 1.1
data: 2026-09-13
decisoes: D-024, D-027, D-029, D-032
status: proposto — não testado
---

# Protocolo de codificação taxonômica — etapa 2

Instrumento da **segunda etapa**: depois que a classe está fechada (primeira
classificação + adjudicação humana), o conjunto `PRIMARY` ∪ `SECONDARY` é
codificado em categorias que **emergem dos dados**.

Implementa [[Codebook]] §5. Entra em execução **depois** do gate de
[[Decision Log#D-024]], confirmado em 2026-09-13 ([[Decision Log#D-032]]):
aplica-se ao conjunto classificado no E-8, e não ao gold set.

> [!important] Quem codifica — [[Decision Log#D-032]] (v1.1)
> **O LLM propõe, os humanos validam.** O LLM faz as passagens 1 e 2 (códigos
> e agrupamento) e aplica a taxonomia na passagem 4. **Os humanos decidem**
> poda, fusão e nomeação (passagem 3), revisam a reaplicação e fazem sozinhos
> a validação da §5. A saída do LLM é **proposta, nunca resultado**.

> [!danger] Regra inegociável
> **Nunca usar referencial externo — OWASP, MITRE, NIST CSF, ou a taxonomia de
> qualquer artigo — para construir as categorias.** Isso cria circularidade:
> encontra-se o que se foi procurar, e o padrão próprio do ecossistema de agent
> skills fica invisível.
>
> Referenciais externos entram **depois** da taxonomia estabilizada, como
> crosswalk na QI-3. É por isso que `security_functions`
> (`PREVENT·DETECT·ASSESS·TEST·RESPOND·RECOVER`, derivado do NIST CSF) foi
> **removido** do instrumento em [[Decision Log#D-029]].

---

## 1. Entrada

- **Universo:** todos os casos com classe final `PRIMARY` ou `SECONDARY`
  (consenso dos avaliadores + adjudicação humana). `NONE` fica fora.
- **Material primário:** o campo `note` de cada caso ([[Codebook]] §2.3), que
  já carrega o papel profissional, qual é o conteúdo de segurança e o elemento
  concreto que o sustenta.
- **Material de apoio:** o `SKILL.md` original, obrigatório na validação (§5).

**Ler em bloco, não caso a caso.** Foi exatamente a codificação um-a-um que
produziu sinonímia inútil no [[EXP-014]] — `agent_guardrails` contra
`agent_autonomy_constraints`, interseção vazia entre avaliadores que
concordavam. A categoria só aparece com o conjunto à vista.

---

## 2. As duas dimensões desta etapa

Fixadas em [[Decision Log#D-029]]. **Só estas duas** — não acrescentar
dimensão sem decisão registrada.

### 2.1 `security_category` — emergente, multi-label

A categoria de segurança da skill, derivada dos padrões observados. **Não tem
valores predefinidos**: eles são o produto desta etapa.

Multi-label: uma skill pode legitimamente pertencer a mais de uma categoria.
Não force categoria única.

### 2.2 `operationality` — fechada, valor único

Substitui `operational_security` + `operation_level`, que na v2.4 eram duas
perguntas sobrepostas (κ=0,511 e 0,446, coincidindo em 78%/71% dos casos).
Fundidas numa escala só:

| Valor | Significado |
|---|---|
| `descriptive` | Menciona ou recomenda, sem dizer o que fazer |
| `procedural` | Diz **o que fazer** — passo a passo, checklist, critério de decisão, classe de falha a procurar |
| `executable` | Invoca ferramenta, script ou comando concreto |

Na dúvida entre dois níveis, escolha o **mais baixo** — aqui a regra é oposta à
da primeira classificação, porque nesta etapa o conjunto já está fechado e
superestimar operacionalidade infla um resultado, em vez de apenas coletar.

> [!important] Este construto existe na literatura, e é difícil para todo mundo
> "Actionability" é dimensão estabelecida em pesquisa de segurança. O método de
> referência é o **SAcoding** (Chowdhury & van Oorschot, *Journal of
> Cybersecurity* 9(1), 2023), que classifica conselho de segurança em
> **practices · policies · principles · outcomes**, tratando como acionável
> apenas quatro tags de prática, por meio de uma **árvore de 10 perguntas
> sim/não** em vez de julgamento holístico.
>
> **Concordância que eles reportam:** 80% em acionabilidade (itens de tag
> única) e **apenas 46% na atribuição completa de tag**. Uma taxonomia de
> resposta a incidentes comparável reporta κ=0,39, subindo a 0,527 após
> refinamento.
>
> **Calibração para nós:** os 77% de `operational_security` e 61% de
> `operation_level` medidos no [[EXP-014]] **estão dentro da faixa publicada**,
> não abaixo dela. A dificuldade é do construto, não do nosso instrumento — o
> que muda a leitura: não se deve esperar κ alto aqui, e um valor em torno de
> 0,5 é resultado normal, citável contra benchmark, não fracasso.
>
> **Lição de desenho a considerar:** o SAcoding usa árvore de decisão
> sequencial, não escala holística. Se a medição de `operationality` sair
> fraca, converter para árvore de 3–4 perguntas é a correção indicada pela
> literatura antes de abandonar a dimensão.

> [!warning] Ainda assim, exige medição própria
> `operationality` é **nova** e não herda a confiabilidade de nada. Antes de
> qualquer número dela ir ao texto, medir com `scripts/compute_agreement.py`
> sobre subamostra dupla-codificada — e reportar **contra o benchmark do
> SAcoding**, não contra uma expectativa arbitrária.

---

## 3. Procedimento — quatro passagens

### Passagem 1 — codificação aberta, sem economia · **LLM propõe**

Leia todas as `note` em sequência. Para cada caso, escreva um ou mais **códigos
em linguagem próxima ao texto observado**. Não tente ser econômico, não tente
padronizar, não olhe para trás para reaproveitar código.

Registre, para **cada código criado**, um **exemplo literal** (o `case_id` e o
trecho da nota que o originou). Código sem exemplo literal não existe.

**Salvaguardas para a proposta do LLM** ([[Decision Log#D-032]]):

- o trecho citado precisa existir **literalmente** na nota de origem, conferido
  por script; código sem trecho confirmado é descartado;
- o prompt proíbe OWASP, MITRE, NIST ou qualquer taxonomia externa, e proposta
  que use alguma delas como categoria é rejeitada na passagem 3;
- registrar modelo, versão, prompt e temperatura ([[Decision Log#D-008]]);
- preferir um modelo **diferente** dos que escreveram as notas (GPT, Claude).
  Recomendação, não decisão.

### Passagem 2 — agrupamento · **LLM propõe**

Com todos os códigos à vista, agrupe por substância. É aqui que
`agent_guardrails` e `agent_autonomy_constraints` viram uma coisa só.

Ao fundir, **preserve os dois rótulos originais** no registro da categoria —
eles documentam a variação de vocabulário e servem de material para a QI-3.

### Passagem 3 — poda e nomeação · **humanos decidem**

- Categoria com **1 único caso**: mantenha como código, **não promova** a
  categoria. Registre à parte como cauda.
- Categoria que só existe porque duas outras se sobrepõem: funda ou separe,
  explicitando o critério.
- Nomeie em termos do **ecossistema observado**, não do vocabulário de
  segurança consagrado — se a categoria natural é "restrição de comportamento
  de agente", esse é o nome, ainda que não exista em nenhum framework.

### Passagem 4 — segunda volta · **LLM aplica, humanos revisam**

Reaplique a taxonomia estabilizada a **todos** os casos, do início. Casos que
não couberem em nenhuma categoria são sinal de que a passagem 3 podou demais —
volte, não force.

**Datar toda mudança de taxonomia.** Versionar em `notes/Results/Security
Taxonomy.md`.

---

## 4. Saída

`results/EXP-0XX_taxonomy_coding.jsonl`, um objeto por caso:

```json
{
  "case_id": "LLM008",
  "security_relevance": "PRIMARY",
  "security_category": ["threat_hunting", "incident_response"],
  "operationality": "executable",
  "codes_pass1": ["reconstrucao de timeline de endpoint", "caca a movimento lateral"],
  "evidence_span": "extract endpoint timelines to analyze file executions and lateral movement",
  "note_source": "gpt|claude|adjudicado"
}
```

E `notes/Results/Security Taxonomy.md` com, por categoria: nome, definição,
**exemplo literal com `case_id`**, códigos de origem fundidos, e contagem.

---

## 5. Validação — sem isto não é resultado

### 5.1 Contra o texto original (obrigatório)

Codificar sobre as notas produz uma taxonomia da **leitura do modelo**, não do
texto. Para **toda categoria que virar resultado**, sortear uma subamostra
(mínimo 5 casos ou 20% da categoria, o que for maior), abrir o `SKILL.md`
original e confirmar que a nota não distorceu.

Divergência aqui é achado, não erro de digitação: significa que os modelos leem
o ecossistema de um jeito que o ecossistema não confirma.

### 5.2 Confiabilidade da própria codificação

Dupla codificação de uma subamostra **por dois pesquisadores humanos**
aplicando a taxonomia final, com **Krippendorff's α para nominais
multi-valorados** (kappa não se aplica a multi-label) e Jaccard médio. A
confiabilidade reportada é **entre humanos**, e não entre LLM e humano
([[Decision Log#D-032]]).

> [!warning] Viés de ancoragem — limitação declarada
> Quem valida categorias já propostas tende a aceitá-las. A dupla codificação
> humana e a conferência da §5.1 medem esse efeito, mas não o eliminam.
`operationality` é nominal simples → Cohen's κ.

Reportar junto: quantas categorias, quantos casos na cauda, e quantos casos
receberam mais de uma categoria.

### 5.3 O que NÃO fazer

- Não comparar com OWASP/MITRE/NIST antes da §5.1 e §5.2 estarem fechadas.
- Não ajustar a taxonomia para "bater melhor" com um framework externo — se
  divergir, **a divergência é o resultado**, e é o insumo da QI-3.

---

## 6. Sobre codificar em cima de notas de LLM

A preocupação óbvia é que a taxonomia herde o viés dos avaliadores. **Medido no
[[EXP-014]], nas 200 notas produzidas (2 avaliadores × 100 casos):**

| Tipo de nota | n | % |
|---|---|---|
| Só contexto (papel + o que a skill faz + o que aparece de segurança) | 186 | **93%** |
| Invoca regra ou nome de classe para justificar | 14 | 7% |

Exemplo típico, que é o padrão dominante:

> *"Designer gráfico usando Adobe Express: o propósito é criar peças visuais,
> mas o texto manda remover PII das queries e refazer o OAuth em 401."*

Isso é **descrição de contexto**, não defesa de rótulo — e é codificável
independentemente da classe que o modelo atribuiu. **O conteúdo das notas não é
a fonte de viés.**

### O que resta, e é diferente

O viés que sobrevive não é de conteúdo, é de **seleção do conjunto**: a
taxonomia é codificada só sobre `PRIMARY` ∪ `SECONDARY`, e no EXP-014 esse
conjunto tinha 66 casos por um avaliador e 54 pelo outro. Nota descritivamente
perfeita não conserta um caso que nunca entrou.

**A adjudicação humana resolve a maior parte disso**: os casos em disputa são
decididos por pessoa, não por modelo. Sobra apenas o risco já declarado em
[[Decision Log#D-026]] desde o início — se os dois avaliadores compartilharem o
mesmo viés, o caso vira consenso e ninguém revisa.

É exatamente para esse resíduo que existe a validação de §5.1: ir ao `SKILL.md`
original numa subamostra de cada categoria. Ela não é formalidade — é a única
checagem que alcança os casos de consenso.

### Consequência para o prompt

Como as notas descritivas funcionam, o prompt **deve pedir contexto, não
argumentação**: o papel da skill, o que ela faz, e o que aparece de segurança.
Justificar a classe é subproduto, não objetivo. Ver [[Classification Prompt]]
§`<fields>`.

## Ligações

[[Codebook]] §5 · [[Classification Prompt]] · [[Guia do Anotador Humano]] ·
[[QI-2 Methodology]] · [[QI-3 Coverage Methodology]] · [[Security Taxonomy]] ·
[[Decision Log#D-029]] · [[Decision Log#D-032]] · [[EXP-014]]
