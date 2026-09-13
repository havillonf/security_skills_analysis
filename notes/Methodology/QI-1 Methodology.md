---
tipo: metodologia
questao: QI-1
data: 2026-08-22
atualizado: 2026-09-13
status: Desenho C adotado (D-014); gold set de 99 casos pronto; desenho do E-8/E-9 a reavaliar no E-7
---

# QI-1 — Metodologia

> **QI-1. Qual a prevalência de skills de segurança na população pública de
> Agent Skills?**

Questão central desde 2026-08-22 ([[Decision Log#D-011]]).

Security Skill = **`PRIMARY` + `SECONDARY`** ([[Codebook]] v2.6, três classes:
`PRIMARY` / `SECONDARY` / `NONE`, [[Decision Log#D-027]]).
`PRIMARY` e `SECONDARY` **sempre reportados separadamente**, além do agregado.

> [!important] População restrita a inglês — [[Decision Log#D-025]] (2026-09-03)
> §2 e §6 abaixo descrevem o desenho multilíngue anterior — histórico; a
> detecção de idioma virou filtro (inglês/não inglês), não mais eixo de
> estratificação.

---

## 1. O que precisa ser produzido

Uma **estimativa com incerteza**, não uma contagem:

- prevalência de Security Skill com intervalo de confiança de 95%;
- desagregada em `PRIMARY` e `SECONDARY`;
- por conteúdo distinto (primária) e por ocorrência (difusão);
- com as exclusões de quadro reportadas à parte: `truncated_undecidable` com
  limites de Manski (D-028), `not_an_instruction_artifact` com análise de
  sensibilidade (D-030);
- com desempenho do classificador medido contra o gold set.

Nada disso é obtenível por contagem de keyword. Ver §7.

---

## 2. População e unidades

| Unidade | n | Papel |
|---|---|---|
| **Conteúdo distinto** (`dedup_primary = 1`) | 1.877.981 | **primária** |
| Ocorrência de arquivo | 3.797.117 | difusão, reportada em paralelo |
| Repositório | 282.200 | controle de concentração |
| Dono | 195.841 | controle de concentração |

Inclui todos os idiomas na medição histórica abaixo ([[Decision Log#D-012]]);
**desde 2026-09-03 a população-alvo é restrita a inglês**
([[Decision Log#D-025]]) — os `n` desta tabela precisam ser recomputados
para o subconjunto em inglês antes de qualquer uso em estimativa.

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

> [!warning] A premissa de prevalência baixa não se confirmou (2026-09-13)
> A tabela do Desenho A e a motivação do Desenho C supunham prevalência de ~5%,
> com positivos raros. O gold set de 99 casos ([[EXP-014]]) dá uma estimativa
> **preliminar** de **56,1% [46,2%; 65,5%]**, inflada pelo `SECONDARY` inclusivo
> do D-027. Com p≈0,5, amostra aleatória simples precisa de ~384 casos para
> ±5 pp e ~1.067 para ±3 pp. O ganho do Desenho C depende de o classificador
> produzir estratos puros. A escolha entre C, amostra aleatória simples
> expandida e dois estágios (D-015) é **decisão do orientador no E-7**, com o
> throughput e as métricas do LLM local na mão. Ver [[03 - Methodology]].

**Adotado: Desenho C.** Se rodar o classificador em 1,88 M for proibitivo, **não**
basta tratar uma sub-amostra como se fosse a população — isso ignora a variância do
primeiro estágio. A alternativa correta é o desenho em **dois estágios** de
[[Decision Log#D-015]], em que `N_h` passa a ser *estimado* e essa incerteza se
propaga para `Var(p̂)`. Comparar custo antes de adotar.

---

## 4. Exclusões de quadro (antes: tratamento de `AMBIGUOUS`)

> [!important] Regra vigente — [[Decision Log#D-028]] e [[Decision Log#D-030]]
> `AMBIGUOUS` **deixou de ser classe** em 2026-09-03 (D-027/D-028). O que não
> pode ser classificado sai da **população**, e não vira categoria:
>
> | Exclusão | Onde é aplicada | Tratamento na estimativa |
> |---|---|---|
> | `description + corpo < 200` caracteres | no quadro, mecânica ([[EXP-016]]) | fora de numerador e denominador |
> | `truncated_undecidable` | na anotação, caso a caso | **depende do desfecho** → limites de Manski |
> | `not_an_instruction_artifact` | marcada na anotação; estratos F1–F3 no quadro | exclusão adiada; reportar com e sem |
>
> No gold set: LLM092 `truncated_undecidable` (Manski [55,6%; 56,6%]);
> LLM019 e LLM067 `not_an_instruction_artifact`.
>
> A matemática abaixo continua valendo, trocando "`AMBIGUOUS`" por
> "`truncated_undecidable`": sob amostragem estratificada os limites se calculam
> **por estrato antes de ponderar**, e não sobre a amostra bruta.

Histórico: o texto original desta seção, escrito para `AMBIGUOUS` como classe.

Fica fora do numerador **e** do denominador. Sob o Desenho C isso **não** é uma
razão simples sobre a amostra: a taxa de `AMBIGUOUS` varia por estrato, então o
denominador de classificáveis é ele próprio uma **quantidade estimada**, com
variância que precisa se propagar.

Estimador correto — **razão de dois estimadores estratificados**, com `w_h = N_h/N`:

```text
             Σ_h w_h · p̂_h^SS
p̂  =  ───────────────────────────────
        Σ_h w_h · (1 − p̂_h^AMB)
```

onde `p̂_h^SS` é a proporção de Security Skill e `p̂_h^AMB` a de `AMBIGUOUS`
(hoje: `truncated_undecidable`), ambas observadas na anotação humana do estrato
`h`. A variância sai por **método delta** ou **bootstrap estratificado**, e não
pela fórmula de proporção simples.

**Limites**, também por estrato **antes** de ponderar:

```text
p_min = Σ_h w_h · p̂_h^SS                          (todo excluído = não-Security)
p_max = Σ_h w_h · (p̂_h^SS + p̂_h^AMB)              (todo excluído = Security)
```

Se os limites forem largos demais para sustentar a conclusão, isso **é** o
achado. Não se resolve escolhendo o número mais conveniente.

---

## 5. Validação do classificador

> [!important] Gold set pronto — [[EXP-014]], [[Decision Log#D-031]] (2026-09-13)
> 99 casos no quadro: **83 de consenso entre 2 modelos** (GPT, Claude), sem
> verificação humana, e **16 decididos por 2 anotadores humanos**
> independentes com reconciliação mútua. `results/EXP-014_gold_set.csv`, com a
> origem de cada rótulo. **Reportar as métricas separadas por origem**:
> concordar com rótulos do GPT e do Claude pode ser só herdar o viés deles.

Contra o gold set:

- precisão, recall, F1 por classe (`PRIMARY`, `SECONDARY`, `NONE`);
- precisão/recall/F1 para a dicotomia Security Skill vs. resto;
- **matriz de confusão completa**;
- intervalos de confiança em toda métrica.

### Análise de erro exigida

| Confusão | Impacto na prevalência agregada |
|---|---|
| `PRIMARY` ↔ `SECONDARY` | nenhum; muda só a desagregação |
| **`SECONDARY` ↔ `NONE`** | **direto — é o erro que importa** |
| `PRIMARY` ↔ `NONE` | direto, mas raro |
| qualquer ↔ exclusão de quadro | muda o denominador |

Até a v2.3 a fronteira decisiva era `SECONDARY` ↔ `MENTION`. Com três classes ela
virou `SECONDARY` ↔ `NONE`, que é também onde se concentraram as discordâncias
dos modelos no [[EXP-013]]/[[EXP-014]] e as dos anotadores humanos.

> [!danger] LLM não é ground truth ([[Decision Log#D-008]])
> Registrar modelo, versão, prompt e temperatura.

---

## 6. Idioma

> [!important] De estratificação para filtro — [[Decision Log#D-025]] (2026-09-03)
> Medições abaixo continuam válidas; idioma virou critério de filtro, não
> eixo de estratificação (população restrita a inglês).

Detalhes em [[Multilingual Strategy]]. O que a QI-1 exigia sob o desenho
multilíngue anterior (histórico):

- distribuição de idiomas medida **antes** de desenhar a amostra ([[EXP-003]]) e
  **concordância entre detectores** medida ([[EXP-004]] v2: 0,987 global, 0,967–1,000
  por grupo). **Acurácia não medida** — não há ground truth humano; a primeira sai de
  [[EXP-005]] (campo `human_language`);
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
| Classificador v1 (TF-IDF) | 1,61% ([[EXP-012]]) | **não é prevalência** — prova de conceito |
| Amostra anotada | gold set, 56,1% [46,2%; 65,5%] ([[EXP-014]]) | **preliminar** — insumo |
| Desempenho do classificador | — | insumo (E-7) |
| **Estimativa de prevalência** | — | **a produzir** |

Nenhum número das duas primeiras linhas pode ser apresentado como resposta à QI-1,
nem como aproximação dela.

---

## 8. Caminho

```text
EXP-003/004  idiomas                                  ✅ -> D-025: só inglês
   |
EXP-013      amostra n=100 (inglês)                   ✅
EXP-014      ensemble de 2 LLMs + 2 humanos na        ✅ gold set 99 casos
             discordância (D-026, D-031)
   |
EXP-015/016  quadro de análise                        ✅ 1.550.550
   |
E-7          validar o LLM local do orientador;       <- PRÓXIMA ETAPA
             critério de gate pré-registrado;
             escolher desenho (C / AAS expandida / dois estágios)
   |
E-8          classificação da população -> N_h
   |
E-9          estimativa de prevalência com IC, desagregada, com exclusões de quadro
   |
E-10         robustez: near-duplicates (D-017), denominadores, concentração, definições
```

**Numeração.** Os `EXP-007` a `EXP-011` do plano original nunca foram usados, e
os experimentos seguiram a ordem de execução (EXP-012 a EXP-016). Os próximos
recebem número quando o script existir.

## 9. Estado atual (2026-09-13)

- ✅ População restrita a inglês (D-025) e quadro de análise de **1.550.550**
  conteúdos ([[EXP-016]]).
- ✅ Instrumento: [[Codebook]] v2.6, três classes, κ = 0,672 na dicotomia entre
  modelos.
- ✅ Gold set de **99 casos** ([[EXP-014]], [[Decision Log#D-031]]).
- ⬜ **E-7**: validar o LLM local do orientador, pré-registrar o critério de
  gate e decidir o desenho do E-8/E-9 à luz da prevalência preliminar perto de
  50%.
- ⬜ Taxa de não-instrução no estrato F3 (205.928 arquivos), D-030.

## Ligações

[[01 - Research Question]] · [[Codebook]] · [[Multilingual Strategy]] ·
[[03 - Methodology]] · [[Decision Log]] · [[EXP-001]] · [[EXP-002]] ·
[[QI-2 Methodology]] · [[QI-3 Coverage Methodology]] · [[GitSkills]]
