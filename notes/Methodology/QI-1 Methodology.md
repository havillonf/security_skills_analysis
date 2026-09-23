---
tipo: metodologia
questao: QI-1
data: 2026-08-22
atualizado: 2026-09-23
status: Amostra manual de 385 casos de SDLC adotada (D-036); amostragem com reposição e descarte (D-037); dois estágios binários (D-034/D-035); heurística como pré-filtro (D-038)
---

# QI-1 — Metodologia

> **QI-1 (Prevalência). Entre as Agent Skills voltadas ao ciclo de vida de desenvolvimento de software (SDLC), qual é a prevalência de considerações e salvaguardas de segurança?**

Questão central desde 2026-08-22 ([[Decision Log#D-011]]), reformulada em 2026-09-21 para foco em SDLC ([[Decision Log#D-034]], [[Decision Log#D-035]]).

A classificação opera em **dois estágios binários** ([[Codebook]] v3.1):
1. **Estágio 1 (SDLC):** A skill atua no ciclo de vida de software? (`is_software_development`: `true`/`false`)
2. **Estágio 2 (Segurança em SDLC):** A skill traz salvaguardas, verificações ou preocupações de segurança no contexto de software? (`has_security`: `true`/`false`)

> [!important] População restrita a inglês e elegibilidade — [[Decision Log#D-025]] e [[Codebook]] v3.1
> A população-alvo é estritamente de skills 100% em inglês, deduplicadas por hash (`dedup_primary = 1`) e com texto suficiente para classificação (`length(description) + body_chars >= 200`).

---

## 1. O que precisa ser produzido

Uma **estimativa estatisticamente sólida com intervalo de confiança de 95% e margem de erro de 5%**:

- Prevalência de segurança **dentro do universo de SDLC** ($\hat{p} \pm 5\%$);
- **Taxa de descarte** de skills não-SDLC no sorteio, permitindo inferir a prevalência geral de SDLC na população total elegível;
- Medição formal de confiabilidade humana (**Cohen's $\kappa \ge 0.8$**) sobre calibração independente de 20 a 40 casos;
- Análise de precisão, recall e F1-score da **heurística determinística** contra os 385 rótulos manuais (para avaliar viabilidade de extrapolação aos 1,5M).

---

## 2. População e unidades

| Unidade | n (Total Parquet) | Papel |
|---|---|---|
| Ocorrência de arquivo | 3.797.117 | difusão, difusão de mercado |
| **Conteúdo distinto** (`dedup_primary = 1`) | 1.877.981 | base bruta |
| **População Elegível** (Inglês + tamanho $\ge 200$) | ~1.550.550 | **universo amostral** ([[EXP-016]]) |
| **Subpopulação de SDLC** (Estágio 1 = `true`) | Desconhecida | população inferida via taxa de descarte |

> [!warning] Near-duplicates sobrevivem à deduplicação por hash
> Pacotes replicados entre proprietários geram hashes diferentes ([[EXP-002]]). O controle de concentração por repositório e proprietário continua sendo reportado como análise de robustez ([[Decision Log#D-017]]).

---

## 3. Desenho amostral: Amostragem com Reposição Condicional ($n=385$)

> [!done] Decidido: **Anotação 100% Manual de 385 casos de SDLC** ([[Decision Log#D-036]], [[Decision Log#D-037]])
> Substitui o antigo ensemble de LLMs da D-026 e o desenho estratificado dependente de LLM (Desenho C de D-014).

Para estimar uma proporção com nível de confiança de 95%, margem de erro de 5% e variância máxima ($p=0,5$), a fórmula de amostragem para populações grandes estabelece:

$$n = \frac{Z^2 \cdot p \cdot (1-p)}{E^2} = \frac{1,96^2 \cdot 0,5 \cdot 0,5}{0,05^2} \approx 384,16 \implies 385 \text{ casos}$$

### 3.1 Procedimento de Extração e Reposição

Como o objetivo de pesquisa restringe o escopo a skills de desenvolvimento de software, os 385 casos devem ser **100% de SDLC**:

1. **Sorteio:** Sorteia-se um lote amplo da População Elegível de forma pseudo-aleatória e determinística (`ORDER BY hash(file_sha || salt)`).
2. **Filtragem de Estágio 1 (SDLC):** Cada skill é avaliada. Se `is_software_development = true`, ela é aceita no "balde" dos 385.
3. **Descarte e Reposição (D-037):** Se `is_software_development = false`, a skill é **descartada** do balde e substituída pela próxima skill sorteada da fila.
4. **Rastreio:** A quantidade de skills não-SDLC descartadas ($N_{\text{descarte}}$) é estritamente contabilizada. A proporção $\frac{385}{385 + N_{\text{descarte}}}$ fornecerá a estimativa de prevalência de SDLC em todo o ecossistema.

---

## 4. Protocolo de Anotação e Calibração Humana

A anotação é integralmente humana, realizada pelos pesquisadores, garantindo validade de *ground truth*:

1. **Calibração Inicial (D-036):** Os primeiros **20 a 40 casos** são anotados de forma cega e independente por dois pesquisadores.
2. **Cálculo de Concordância:** Mede-se o **Cohen's $\kappa$** interavaliador para os dois estágios. O limiar mínimo aceitável é $\kappa \ge 0,80$.
3. **Reconciliação:** Divergências são discutidas e reconciliadas, documentando no Codebook eventuais esclarecimentos jurisprudenciais.
4. **Execução Final:** Após calibração satisfatória, a anotação prossegue (dividida entre pesquisadores ou mantida em consenso) até completar as **385 skills de SDLC**.

---

## 5. Papel da Heurística e das LLMs (D-038)

- **Heurística Determinística (Regex/Keywords):** Atua como ferramenta de triagem prévia. Pode ser usada para ordenar ou enriquecer o lote inicial de sorteio (reduzindo tempo gasto lendo itens descartáveis) e, se validada com alto F1 contra o ground truth humano, executada sobre o 1,5M para estatísticas descritivas complementares.
- **LLMs (Claude / Qwen local):** **Não atuam como classificadores da RQ1.** Seu papel é transferido integralmente para a RQ2 (assistência qualitativa na extração e proposta de códigos de segurança).

---

## 6. Exclusões de Quadro

Conforme [[Codebook]] v3.1:
- `length(description) + body_chars < 200`: Removido mecanicamente no pré-processamento.
- `not_an_instruction_artifact`: Arquivos que são logs, saídas geradas ou dumps são descartados.
- `truncated_undecidable`: Casos truncados cuja evidência seja insuficiente para julgar são reportados com limites de Manski.

---

## 7. Caminho Metodológico Atualizado

```text
População Elegível (~1.55M)
        │
        ▼ (Sorteio com hash + pré-filtro heurístico)
Lote Amplo de Candidatas
        │
        ├────────────────────────────────┐
        ▼ (Estágio 1 = não)              ▼ (Estágio 1 = sim)
Descarte Registrado (D-037)       Balde de SDLC (n=385)
                                         │
                        ┌────────────────┴────────────────┐
                        ▼                                 ▼
           Fase 1: Calibração (20-40)         Fase 2: Conclusão (até 385)
           κ de Cohen ≥ 0.8                   Anotação de Segurança (Estágio 2)
                        │                                 │
                        └────────────────►────────────────┘
                                         │
                                         ▼
                             Prevalência RQ1 (IC 95%)
                                         │
                                         ▼
                             Entrada para RQ2 (Open Coding)
```

## Ligações

[[01 - Research Question]] · [[Codebook]] · [[Decision Log]] · [[QI-2 Methodology]] · [[QI-3 Coverage Methodology]]
