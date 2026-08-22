---
tipo: metodologia
questao: QI-1
data: 2026-08-22
status: proposta - desenho amostral aguarda aprovacao
---

# QI-1 — Metodologia

> **QI-1. Qual a prevalência de skills de segurança na população pública de
> Agent Skills?**

Questão central desde 2026-08-22 ([[Decision Log#D-011]]).

Security Skill = **`SEC-PRIMARY` + `SEC-SECONDARY`** ([[Codebook]] v2.1).
`PRIMARY` e `SECONDARY` **sempre reportados separadamente**, além do agregado.

---

## 1. O que precisa ser produzido

Uma **estimativa com incerteza**, não uma contagem:

- prevalência de Security Skill com intervalo de confiança de 95%;
- desagregada em `PRIMARY` e `SECONDARY`;
- por conteúdo distinto (primária) e por ocorrência (difusão);
- com taxa de `AMBIGUOUS` reportada à parte;
- com desempenho do classificador medido **por idioma**.

Nada disso é obtenível por contagem de keyword. Ver §7.

---

## 2. População e unidades

| Unidade | n | Papel |
|---|---|---|
| **Conteúdo distinto** (`dedup_primary = 1`) | 1.877.981 | **primária** |
| Ocorrência de arquivo | 3.797.117 | difusão, reportada em paralelo |
| Repositório | 282.200 | controle de concentração |
| Dono | 195.841 | controle de concentração |

Inclui **todos os idiomas** ([[Decision Log#D-012]]).

> [!warning] A unidade primária tem uma fragilidade conhecida
> Near-duplicates sobrevivem à deduplicação por hash ([[EXP-002]]). Um pacote
> replicado entre donos com variações mínimas gera `file_sha` distintos e infla
> qualquer contagem. Toda estimativa reporta concentração por repositório **e por
> dono**; deduplicação por similaridade é [[Decision Log#D-010|D-010]], em aberto.

---

## 3. Desenho amostral proposto

> [!important] Requer aprovação — muda materialmente a estimativa

### Desenho A — Amostragem aleatória simples

Sortear *n* representantes ao acaso, anotar tudo à mão, estimar por proporção
binomial.

*Prós:* simples, sem classificador, sem premissa nenhuma.
*Contras:* caro. Se a prevalência real for baixa (digamos 5%), a maior parte do
esforço cai em `NONE`, e o número de Security Skills observadas — que é o que
determina a precisão — fica pequeno.

Tamanhos, para prevalência assumida de 5%:

| Margem (95%) | n aproximado |
|---|---|
| ± 2,0 p.p. | ~456 |
| ± 1,5 p.p. | ~811 |
| ± 1,0 p.p. | ~1.825 |

### Desenho B — Classificador em escala, sem correção

Classificar tudo com LLM e contar os positivos.

**Rejeitado.** A contagem herda o viés do classificador sem quantificá-lo. Não é
estimativa, é output de modelo.

### Desenho C — Amostragem estratificada com classificador de triagem ✅ recomendado

1. Classificador (LLM) roda sobre a população e atribui uma classe *prevista*.
   Isso **não é o resultado** — serve para formar estratos.
2. Estratos = classe prevista × grupo linguístico.
3. Amostra aleatória **dentro de cada estrato**, anotada à mão.
4. Estimador estratificado:

```text
p̂   = Σ_h (N_h / N) · p̂_h

Var = Σ_h (N_h / N)² · p̂_h · (1 − p̂_h) / n_h
```

onde `N_h` é o tamanho do estrato na população e `p̂_h` a proporção de Security
Skill observada na amostra daquele estrato.

**A propriedade que torna este desenho defensável:** o estimador é **não enviesado
por construção, mesmo que o classificador seja ruim**. Um classificador fraco só
alarga o intervalo de confiança — não desloca a estimativa. O classificador afeta a
**eficiência**, nunca a **validade**.

*Prós:* muito mais preciso por hora de anotação; permite sobre-amostrar estratos
raros (`PRIMARY`) e idiomas minoritários sem enviesar o total.
*Contras:* exige `N_h` exato (classificar a população inteira) e disciplina para não
confundir contagem prevista com estimativa.

**Recomendação: Desenho C.** Se rodar o classificador em 1,88M for proibitivo, a
alternativa é aplicá-lo a uma sub-amostra aleatória grande (ex. 100k) e tratar essa
sub-amostra como a população do estimador — continua válido, com `N` menor.

---

## 4. Tratamento de `AMBIGUOUS`

Fica fora do numerador **e** do denominador. Isso muda a estimativa e precisa ser
reportado de forma honesta:

1. **Estimativa pontual** entre os classificáveis:
   `p̂ = SS / (total − AMB)`
2. **Limites**, tratando todos os `AMBIGUOUS` como pior e melhor caso:
   `p_min = SS / total` e `p_max = (SS + AMB) / total`
3. **Taxa de `AMBIGUOUS`** sempre reportada.

Se os limites forem largos demais para sustentar a conclusão, isso **é** o achado —
não se resolve escolhendo o número mais conveniente.

---

## 5. Validação do classificador

Contra o gold set humano, **por classe e por idioma**:

- precisão, recall, F1 por classe (`PRIMARY`, `SECONDARY`, `MENTION`, `NONE`);
- precisão/recall/F1 para a dicotomia Security Skill vs resto;
- **matriz de confusão completa**;
- intervalos de confiança em toda métrica.

### Análise de erro exigida

A fronteira que decide o resultado é **`SECONDARY` ↔ `MENTION`**. Confundir
`PRIMARY` com `SECONDARY` não muda a prevalência agregada — ambos são Security
Skill. Confundir `SECONDARY` com `MENTION` muda.

| Confusão | Impacto na prevalência agregada |
|---|---|
| PRIMARY ↔ SECONDARY | nenhum; muda só a desagregação |
| **SECONDARY ↔ MENTION** | **direto — é o erro que importa** |
| MENTION ↔ NONE | nenhum |
| qualquer ↔ AMBIGUOUS | muda o denominador |

Reportar essas taxas separadamente, não só o F1 global.

> [!danger] LLM não é ground truth ([[Decision Log#D-008]])
> Registrar modelo, versão, prompt e temperatura. O gold set é humano.

---

## 6. Idioma

Detalhes em [[Multilingual Strategy]]. O que a QI-1 exige:

- distribuição de idiomas medida **antes** de desenhar a amostra ([[EXP-003]]);
- gold set estratificado por idioma / grupo linguístico;
- desempenho avaliado por idioma — F1 global bom **não** é evidência de
  uniformidade;
- queda relevante num idioma = **ameaça à validade da estimativa**, declarada;
- prevalência principal = população inteira. Desagregação por idioma é
  **secundária**, só com suporte amostral, e nunca comparada sem considerar tamanho
  de população, incerteza, qualidade do classificador naquele idioma e viés do
  retrieval.

---

## 7. Números que **não** são a resposta

| Tipo | Exemplo já produzido | Status |
|---|---|---|
| Exploratório | 52,93% citam keyword ([[EXP-001]]) | **não é prevalência** |
| Candidate retrieval | pool de 78,69% ([[EXP-002]]) | **não é prevalência** |
| Amostra anotada | — | insumo |
| Desempenho do classificador | — | insumo |
| **Estimativa de prevalência** | — | **a produzir** |

Nenhum número das duas primeiras linhas pode ser apresentado como resposta à QI-1,
nem como aproximação dela.

---

## 8. Caminho

```text
EXP-003  distribuição de idiomas da população        <- etapa atual
   |
EXP-004  candidate retrieval multilíngue + recall por idioma
   |
EXP-005  piloto de anotação (~50), fronteira SECONDARY/MENTION, multilíngue
   |
EXP-006  gold set estratificado + concordância
   |
EXP-007  classificador validado (métricas por classe e por idioma)
   |
EXP-008  classificação da população -> estratos
   |
EXP-009  estimativa de prevalência com IC, desagregada
```

## 9. Estado atual

⬜ Nenhuma etapa concluída. `EXP-003` em execução.

Reaproveitado da fase anterior: [[Codebook]] (instrumento), a definição
([[Decision Log#D-004]]), o candidate retrieval de [[EXP-002]] (baseline inglês a
ser superado) e [[EXP-001]] (estrutura e denominadores).

## Ligações

[[01 - Research Question]] · [[Codebook]] · [[Multilingual Strategy]] ·
[[03 - Methodology]] · [[Decision Log]] · [[EXP-001]] · [[EXP-002]] ·
[[QI-2 Methodology]] · [[QI-3 Coverage Methodology]] · [[GitSkills]]
