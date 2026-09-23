---
tipo: metodologia
questao: QI-2
data: 2026-08-22
status: proposta; open coding iniciado
atualizado: 2026-09-23
status: Alinhada com D-036 e D-038: Open coding manual sobre os casos de segurança dos 385 de SDLC; LLMs (Claude/Qwen) como assistentes qualitativos
---

# QI-2 — Metodologia

> **QI-2. Que tipos de preocupação de segurança as skills expressam, e como se
> distribuem?**
> **QI-2 (Tipologia). Quais categorias e dimensões de segurança são contempladas nessas skills e como elas se distribuem?**

Abordagem **bottom-up**. A taxonomia emerge dos dados via análise temática, não de
framework externo.
Abordagem **bottom-up (indutiva)**. A taxonomia emerge dos dados via análise temática e *open coding*, e não a partir de frameworks externos pré-concebidos.

> [!danger] Regra inegociável
> **Nunca use OWASP, MITRE ou qualquer referencial externo para construir a
> taxonomia empírica da QI-2.** Isso criaria circularidade — encontraríamos o que
> fomos procurar — e esconderia padrões próprios do ecossistema de Agent Skills.
> Frameworks externos entram **apenas depois** da taxonomia estabilizada, para
> crosswalk e [[QI-3 Coverage Methodology|QI-3]].
> [!danger] Regra inegociável — Evitar Circularidade
> **Nunca use OWASP, MITRE ou qualquer referencial externo para construir a taxonomia empírica da QI-2.** 
> Isso criaria circularidade — encontraríamos apenas o que fomos buscar — e esconderia padrões próprios do ecossistema de Agent Skills. Frameworks externos entram **apenas depois** da taxonomia estabilizada, no âmbito da [[QI-3 Coverage Methodology|QI-3 (Gap Analysis)]].

> [!important] Gate — [[Decision Log#D-024]] (2026-08-27)
> QI-2 só é executada **depois** de o classificador de triagem de QI-1 passar
> pela validação de E-7 com desempenho satisfatório. O **conjunto de skills
> analisado** deixa de ser apenas o pool de candidate retrieval por
> palavra-chave (§2 abaixo, que permanece válido como medição histórica de
> [[EXP-002]]) e passa a ser a população classificada como
> `SEC-PRIMARY`/`SEC-SECONDARY` pelo classificador **validado**, produzida em
> E-8. Isso não é um erro de desenho anterior — E-8 simplesmente ainda não
> existia quando este documento foi escrito — mas é a atualização que esta
> nota registra. O critério numérico de "validação satisfatória" ainda não
> foi definido; ver o aviso em [[Decision Log#D-024]].

---

## 1. Pipeline
## 1. Conjunto de Entrada e Amostragem

```text
skills candidatas (candidate retrieval)
        ↓
amostra exploratória estratificada
        ↓
open coding
        ↓
códigos recorrentes
        ↓
agrupamento conceitual
        ↓
codebook preliminar
        ↓
nova amostra → refinamento → (iterar até estabilizar)
        ↓
taxonomia estabilizada
        ↓
validação (gold set, concordância)
        ↓
classificação em escala
```
O universo de análise da QI-2 deriva diretamente da anotação humana da QI-1:

Cada iteração registra: códigos novos, códigos fundidos, códigos abandonados, casos
fronteiriços e sobreposições. O histórico de mudanças fica em [[Security Taxonomy]].
1. **População Primária da QI-2:** Todas as skills classificadas com `has_security = true` no Estágio 2 da amostra de 385 casos de SDLC ([[Decision Log#D-036]]).
2. **Contingência para Baixa Incidência (Two-Phase Sampling):** Se a incidência de segurança dentro dos 385 casos for muito reduzida (ex: $< 50$ casos), uma amostra intencional complementar será extraída do pool filtrado pela heurística de segurança, assegurando volume empírico suficiente para saturação qualitativa.

---

## 2. Candidate retrieval
## 2. Processo de Open Coding e Saturação Teórica

Keyword matching serve **exclusivamente** para reduzir 1.877.981 representantes a um
pool revisável. Não classifica nada.
O procedimento analítico segue a grounded theory adaptada para engenharia de software empírica:

Implementado em `scripts/build_candidate_frame.py` (60 termos, recall-orientado).

> [!warning] Resultado que muda o desenho
> O pool resultante é de **1.477.763 conteúdos — 78,69% dos representantes**
> ([[EXP-002]]). A recuperação ampla **quase não filtra**.

Consequências:

1. Não existe atalho por keyword. A redução real da população só acontece na
   **classificação**, não na recuperação.
2. Anotação manual exaustiva está fora de questão em qualquer cenário.
3. O desenho tem de ser: amostra anotada → classificador validado → escala. Não há
   alternativa viável.
4. Um retrieval mais estrito pode ser testado, mas o critério para escolhê-lo é
   **recall contra o gold set**, nunca tamanho do pool. Perder Security Skills antes
   da anotação é erro irreversível; incluir ruído apenas custa trabalho.

---

## 3. Amostragem

Determinística (`ORDER BY hash(file_sha)`), sem seed externa, reproduzível em
qualquer máquina. `file_sha` sorteados sempre salvos em `results/`.

### 3.1 Amostra de descoberta (open coding)

**Estratificada para expor fronteiras, não para representar a população.** Não
produz estimativa de prevalência e não deve ser usada para isso.

| Estrato | Predicado | n no pool |
|---|---|---|
| `S1_frontmatter_signal` | termo no `name`/`description` | 332.547 |
| `S2_body_high_density` | só no corpo, ≥ 5 termos distintos | 124.773 |
| `S3_body_low_density` | só no corpo, 1–2 termos | 777.762 |
| `S4_with_scripts` | `has_scripts = 1` e ≥ 3 termos | 82.190 |

`S3` é o maior estrato e o mais provável reservatório de `MENTION`/`NONE`. `S4`
existe porque a capacidade real pode estar no script, não no `SKILL.md` (regra R-6).

### 3.2 Amostra de prevalência

**Aleatória simples sobre os representantes**, não estratificada, e separada da
amostra de descoberta. Só ela sustenta afirmação de distribuição. Tamanho calculado
a partir da precisão desejada. (A QI-2 é extensão futura; sob a QI-1 vigente, o
desenho amostral é o Desenho C de [[QI-1 Methodology]].)

Misturar as duas é erro grave: usar a amostra estratificada para estimar prevalência
inflaria artificialmente as classes sobre-amostradas.

---

## 4. Open coding

Regras:

- permanecer próximo ao conteúdo observado; não impor categorias externas;
- registrar exemplo textual literal para cada código;
- registrar casos fronteiriços e sobreposições;
- multi-label permitido e esperado;
- código novo é criado livremente na primeira passagem; fusão e poda vêm depois;
- toda mudança no codebook é datada e justificada.

Não buscar taxonomia perfeita na primeira iteração.

### 4.1 Três dimensões, nunca colapsadas

A QI-2 não pergunta só "qual vulnerabilidade aparece". Sempre que os dados
permitirem, separar:

| Dimensão | Pergunta |
|---|---|
| **Security concern** | Sobre qual preocupação a skill atua? |
| **Security function** | O que ela faz em relação à preocupação? |
| **Operational capability** | Como ela operacionaliza isso? |

```text
Concern: SQL Injection | Function: DETECT + TEST | Capability: dynamic_analysis + exploitation
Concern: SQL Injection | Function: PREVENT       | Capability: source_code_analysis
Skills de Segurança (Estágio 2 = true)
        │
        ▼
Leitura Detalhada e Identificação de Evidências
        │
        ▼ (Apoio de LLMs: Claude / Qwen propõem códigos)
Extração de Códigos Conceituais Iniciais
        │
        ▼ (Pesquisadores validam, fundem e agrupam)
Agrupamento em Categorias e Dimensões
        │
        ▼ (Iteração contínua ao longo dos 385 casos)
Busca por Saturação Teórica (Nenhuma nova categoria emerge)
        │
        ▼
Taxonomia de Segurança Estabilizada
```

Mesmo concern, comportamentos completamente diferentes. Colapsar as três numa
categoria só destrói a distinção central da pesquisa.
### 2.1 Critério de Saturação Teórica (D-036)
A análise deve atingir **saturação teórica** antes do término da leitura dos 385 casos: a leitura dos casos finais deve apenas instanciar códigos e categorias já mapeados anteriormente, sem o surgimento de conceitos novos.

Valores e definições: [[Codebook]] §5 e §6.

---

## 5. População e denominadores
## 3. Papel das Ferramentas de IA (LLMs como Assistentes)

> [!important] Não deixe `MENTION` dominar a distribuição
> Reportar uma distribuição única sobre "tudo que menciona segurança" faz a resposta
> ser carregada por menção incidental.
Conforme [[Decision Log#D-038]]:
- Modelos de linguagem (Claude e Qwen local) atuam exclusivamente como **assistentes de codificação aberta**.
- Podem ser instruídos a ler o texto e sugerir entidades (*e.g.*, *"menciona JWT"* ou *"protege contra command injection"*).
- **A decisão final é estritamente humana:** O agrupamento conceitual, a taxonomia, as regras de inclusão/exclusão de categorias e a verificação de coerência permanecem sob responsabilidade intelectual dos pesquisadores.

Toda distribuição da QI-2 é reportada em **camadas explícitas**:

| Camada | Denominador | Responde |
|---|---|---|
| A | todas as ocorrências relacionadas a segurança (inclui `MENTION`) | "o que é mencionado?" |
| B | `PRIMARY` + `SECONDARY` | "o que aparece como capacidade de segurança?" |
| C | `security_focus = true` | "o que é skill de segurança propriamente?" |
| D | `operational_security = true` | "o que efetivamente **faz** segurança?" |

`AMBIGUOUS` fora do numerador e do denominador, com contagem reportada sempre.

A distância entre A e D é, em si, um resultado potencial da pesquisa — a distância
entre **segurança mencionada** e **segurança operacionalizada**. Não assumir o
resultado antes de medir.

Unidade primária: conteúdo distinto ([[Decision Log#D-001]]). Contagem por
ocorrência reportada em paralelo como difusão.

---

## 6. Validação
## 4. Dimensões Analíticas de Segurança

Nada da QI-2 é resultado científico antes disto.
Para evitar o colapso de conceitos em rótulos genéricos, a análise qualitativa busca mapear, sempre que a evidência permitir:

1. Codebook escrito antes da anotação — [[Codebook]] v2.3 ✅
2. Amostra anotada manualmente.
3. **Dois anotadores independentes** quando viável.
4. Análise de discordâncias, com adjudicação registrada.
5. Refinamento das definições → nova versão do codebook, datada.
6. Concordância interavaliadores (métricas em [[Codebook]] §9; escolha final só
   depois de fechado o desenho).
7. **Gold set** versionado em `results/`.
8. Validação de qualquer classificação automática contra o gold set: precisão,
   recall, F1 **por classe** e para a dicotomia, com IC, mais matriz de confusão.
| Dimensão | Pergunta Norteada | Exemplo Empírico |
|---|---|---|
| **Security Concern** | Sobre qual preocupação, ameaça ou vulnerabilidade a skill atua? | Prompt Injection, Exposição de Segredos, SQLi, Abuso de Recursos |
| **Security Function** | O que a skill faz em relação à preocupação? | Prevenir, Detectar, Testar, Mitigar, Auditar |
| **Operational Capability** | Como essa segurança é operacionalizada no artefato? | Análise estática (SAST), Validação de regex, Uso de variáveis de ambiente, Rate limit |

> [!danger] LLM não é ground truth
> Claude pode assistir triagem, sugerir códigos e pré-classificar em escala. Nada
> disso é verdade de referência. Todo output de LLM usado em resultado precisa de
> validação contra gold set humano, com registro de modelo, versão, prompt e
> temperatura. Ver [[Decision Log#D-008]].

---

## 7. Ameaças à validade específicas da QI-2
## 5. Validação e Confiabilidade

- **Multilinguismo.** Confirmado empiricamente: a amostra de 48 trouxe francês,
  chinês, russo e coreano ([[EXP-002]]). Retrieval e codebook em inglês perdem essas
  skills e as empurram para `AMBIGUOUS`. Quantificar a fração não-inglesa do pool.
- **Dependência entre observações — pior do que se supunha.** 60,8% das ocorrências
  são cópias exatas, e [[EXP-002]] mostrou que **near-duplicates sobrevivem à
  deduplicação por hash**: 13.187 conteúdos *distintos* com `domain: cybersecurity`
  vêm de 82 repositórios, metade concentrada em oito donos. Deduplicar por `file_sha`
  **não basta**. Toda distribuição precisa reportar concentração por repositório
  **e por dono**, e nenhum código da taxonomia pode ser sustentado por poucos
  atores sem que isso seja dito. Ver [[Decision Log#D-010]].
- **Difusão ≠ preocupação.** Existem pacotes publicados por fornecedor. Se
  replicarem muito, a distribuição de concerns retrata o que alguns pacotes cobrem,
  não o que a comunidade se preocupa.
- **Deriva do codebook.** Refinar categorias depois de ver resultados vira
  racionalização. Refinamento só entre iterações, sempre datado.
- **Sobreposição de códigos.** Multi-label reduz o problema mas não elimina
  ambiguidade conceitual; registrar pares que coocorrem sistematicamente.
- **Frequência ≠ importância.** Uma skill copiada 5.000 vezes não representa
  preocupação mais importante, e sim mais difundida.
1. **Rastreabilidade de Evidências:** Cada código gerado deve conter o trecho textual literal (citação) que o originou no `SKILL.md`.
2. **Reconciliação:** Os códigos propostos são revisados conjuntamente entre os pesquisadores para consolidação da árvore taxonômica.
3. **Distribuição Empírica:** Uma vez fixadas as categorias, cada skill do conjunto de segurança recebe sua categorização final para reportar as frequências relativas na RQ2.

---

## 8. Estado atual

- ✅ Candidate retrieval implementado e medido ([[EXP-002]]) — histórico,
  reaproveitável como sinal, não é mais o conjunto de entrada planejado (ver
  gate acima).
- ✅ Amostra de descoberta gerada (48 itens, 4 estratos).
- 🟡 Open coding: **primeira passagem exploratória feita por LLM**, com códigos
  candidatos em [[Security Taxonomy]]. **Não é gold set nem resultado.**
- ⬜ Classificador de QI-1 ainda não validado (E-7) — **QI-2 não pode começar**
  enquanto essa etapa não passar pelo gate de [[Decision Log#D-024]].
- ⬜ Open coding, iteração, estabilização, validação — **LLM propõe, humanos
  validam**, com as salvaguardas do [[Taxonomy Coding Protocol]] v1.1
  ([[Decision Log#D-032]]). Ordem do D-024 reafirmada em 2026-09-13: só depois
  do gate do E-7.

**Nenhum número de distribuição foi calculado, e nenhum deve ser antes da
validação — nem da QI-2 propriamente, nem do classificador de QI-1 do qual
seu conjunto de entrada depende.**

## Ligações

[[01 - Research Question]] · [[Codebook]] · [[Security Taxonomy]] ·
[[QI-3 Coverage Methodology]] · [[EXP-002]] · [[03 - Methodology]] ·
[[Decision Log]]
[[01 - Research Question]] · [[Codebook]] · [[Security Taxonomy]] · [[QI-1 Methodology]] · [[QI-3 Coverage Methodology]] · [[Decision Log]]
