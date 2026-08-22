---
tipo: metodologia
questao: QI-2
data: 2026-08-22
status: proposta; open coding iniciado
---

# QI-2 — Metodologia

> **QI-2. Que tipos de preocupação de segurança as skills expressam, e como se
> distribuem?**

Abordagem **bottom-up**. A taxonomia emerge dos dados via análise temática, não de
framework externo.

> [!danger] Regra inegociável
> **Nunca use OWASP, MITRE ou qualquer referencial externo para construir a
> taxonomia empírica da QI-2.** Isso criaria circularidade — encontraríamos o que
> fomos procurar — e esconderia padrões próprios do ecossistema de Agent Skills.
> Frameworks externos entram **apenas depois** da taxonomia estabilizada, para
> crosswalk e [[QI-3 Coverage Methodology|QI-3]].

---

## 1. Pipeline

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

Cada iteração registra: códigos novos, códigos fundidos, códigos abandonados, casos
fronteiriços e sobreposições. O histórico de mudanças fica em [[Security Taxonomy]].

---

## 2. Candidate retrieval

Keyword matching serve **exclusivamente** para reduzir 1.877.981 representantes a um
pool revisável. Não classifica nada.

Implementado em `scripts/build_candidate_frame.py` (58 termos, recall-orientado).

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
a partir da precisão desejada, definido em E-3.

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
```

Mesmo concern, comportamentos completamente diferentes. Colapsar as três numa
categoria só destrói a distinção central da pesquisa.

Valores e definições: [[Codebook]] §5 e §6.

---

## 5. População e denominadores

> [!important] Não deixe `MENTION` dominar a distribuição
> Reportar uma distribuição única sobre "tudo que menciona segurança" faz a resposta
> ser carregada por menção incidental.

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

Nada da QI-2 é resultado científico antes disto.

1. Codebook escrito antes da anotação — [[Codebook]] v2.0 ✅
2. Amostra anotada manualmente.
3. **Dois anotadores independentes** quando viável.
4. Análise de discordâncias, com adjudicação registrada.
5. Refinamento das definições → nova versão do codebook, datada.
6. Concordância interavaliadores (métricas em [[Codebook]] §9; escolha final só
   depois de fechado o desenho).
7. **Gold set** versionado em `results/`.
8. Validação de qualquer classificação automática contra o gold set: precisão,
   recall, F1 **por classe** e para a dicotomia, com IC, mais matriz de confusão.

> [!danger] LLM não é ground truth
> Claude pode assistir triagem, sugerir códigos e pré-classificar em escala. Nada
> disso é verdade de referência. Todo output de LLM usado em resultado precisa de
> validação contra gold set humano, com registro de modelo, versão, prompt e
> temperatura. Ver [[Decision Log#D-008]].

---

## 7. Ameaças à validade específicas da QI-2

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

---

## 8. Estado atual

- ✅ Candidate retrieval implementado e medido ([[EXP-002]]).
- ✅ Amostra de descoberta gerada (48 itens, 4 estratos).
- 🟡 Open coding: **primeira passagem exploratória feita por LLM**, com códigos
  candidatos em [[Security Taxonomy]]. **Não é gold set nem resultado.**
- ⬜ Open coding humano, iteração, estabilização, validação.

**Nenhum número de distribuição foi calculado, e nenhum deve ser antes da validação.**

## Ligações

[[01 - Research Question]] · [[Codebook]] · [[Security Taxonomy]] ·
[[QI-3 Coverage Methodology]] · [[EXP-002]] · [[03 - Methodology]] ·
[[Decision Log]]
