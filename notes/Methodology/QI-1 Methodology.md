---
tipo: metodologia
questao: QI-1
data: 2026-08-22
status: Desenho C adotado (D-014); estratos linguisticos definidos
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
> dono**. A deduplicação exata permanece o desenho principal; a semântica fica como
> **análise de robustez** ([[Decision Log#D-017]]).

---

## 3. Desenho amostral proposto

> [!done] Decidido: **Desenho C** ([[Decision Log#D-014]], 2026-08-22)
> As alternativas ficam registradas abaixo por rastreabilidade. Detalhes formais —
> estimador com correção para população finita, seis condições de validade, papel
> limitado do classificador — estão em [[Decision Log#D-014]].

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

Var = Σ_h (N_h / N)² · (1 − n_h/N_h) · p̂_h · (1 − p̂_h) / (n_h − 1)
```

onde `N_h` é o tamanho do estrato na população, `n_h` o tamanho da amostra no estrato
e `p̂_h` a proporção de Security Skill observada **na anotação humana** daquele
estrato. O fator `(1 − n_h/N_h)` é a **correção para população finita** — desprezível
na maioria dos estratos, relevante nos pequenos com oversampling forte. Forma
completa e justificativa em [[Decision Log#D-014]].

**A propriedade que torna este desenho defensável:** desde que as seis condições de
[[Decision Log#D-014]] valham, o desfecho usado na estimação é a **anotação humana**
sobre uma amostra probabilística. Erro do classificador afeta **principalmente a
eficiência da estratificação** — estratos menos puros exigem amostras maiores para a
mesma precisão.

Isso **não é** garantia absoluta: erro do classificador pode comprometer a validade
se quebrar alguma condição — `N_h` errado, unidade em mais de um estrato, estrato
não amostrado, ou falha correlacionada com o desfecho **e** com a chance de seleção.

**Apoio na literatura.** Egami et al. (NeurIPS 2023, *Design-based Supervised
Learning*) mostram que o uso direto de rótulos de surrogate em análise posterior
produz **viés substancial e intervalos de confiança inválidos, mesmo com acurácia de
80–90%** do surrogate, e que a correção depende de **amostragem probabilística** dos
rótulos gold. É a justificativa publicada mais forte para rejeitar o Desenho B. Ver
[[Multilingual Methodology Review]].

*Prós:* muito mais preciso por hora de anotação; permite sobre-amostrar estratos
raros (`PRIMARY`) e idiomas minoritários sem enviesar o total.
*Contras:* exige `N_h` exato (classificar a população inteira) e disciplina para não
confundir contagem prevista com estimativa.

**Adotado: Desenho C.** Se rodar o classificador em 1,88 M for proibitivo, **não**
basta tratar uma sub-amostra como se fosse a população — isso ignora a variância do
primeiro estágio. A alternativa correta é o desenho em **dois estágios** de
[[Decision Log#D-015]], em que `N_h` passa a ser *estimado* e essa incerteza se
propaga para `Var(p̂)`. Comparar custo antes de adotar.

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

- distribuição de idiomas medida **antes** de desenhar a amostra ([[EXP-003]]) e
  detector validado por concordância ([[EXP-004]]);
- estratos linguísticos **L1–L5** de [[Multilingual Strategy]] §8, com a cauda
  colapsada porque a detecção ali não sustenta separação;
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
EXP-003  distribuição de idiomas                    ✅ 14,21% não inglês
   |
EXP-004  validação do detector de idioma            ✅ lingua primário; cauda colapsada
   |
EXP-005  piloto de anotação  <- PRÓXIMA ETAPA
         estratificado por classe prevista × grupo linguístico;
         fronteira SECONDARY/MENTION; casos GRC; casos mixed
   |
EXP-006  gold set estratificado + concordância
   |
EXP-007  candidate retrieval, escolhido por recall medido contra o gold set
   |
EXP-008  classificador validado (métricas por classe e por idioma)
   |
EXP-009  classificação da população -> estratos (N_h)
   |
EXP-010  estimativa de prevalência com IC, desagregada
   |
EXP-011  robustez: near-duplicates ([[Decision Log#D-017]]), denominadores,
         concentração por dono, definições alternativas
```

**Mudança de ordem** proposta em [[Multilingual Methodology Review]] e adotada aqui:
o piloto vem **antes** do retrieval multilíngue. Sob o Desenho C o retrieval
estratifica e não determina elegibilidade, e o critério para escolhê-lo é recall
contra o gold set — que não existe antes do piloto.

## 9. Estado atual

✅ `EXP-003` e `EXP-004` concluídos. Desenho C adotado. Estratos linguísticos
definidos. ⬜ `EXP-005` (piloto) é a próxima etapa.

Reaproveitado da fase anterior: [[Codebook]] (instrumento), a definição
([[Decision Log#D-004]]), o candidate retrieval de [[EXP-002]] (baseline inglês a
ser superado) e [[EXP-001]] (estrutura e denominadores).

## Ligações

[[01 - Research Question]] · [[Codebook]] · [[Multilingual Strategy]] ·
[[03 - Methodology]] · [[Decision Log]] · [[EXP-001]] · [[EXP-002]] ·
[[QI-2 Methodology]] · [[QI-3 Coverage Methodology]] · [[GitSkills]]
