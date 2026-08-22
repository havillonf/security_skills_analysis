---
tipo: metodologia
atualizado: 2026-08-22
status: proposta
---

# Plano de pesquisa

Incremental. Cada etapa tem critério de conclusão verificável. **E-0 está concluída;
E-1 está parcialmente concluída** - [[Decision Log#D-004]] foi decidida em
2026-08-22; falta escolher a questão central. **Próximo passo: E-3 (piloto do
[[Codebook]]).**

Não avance uma etapa cujo critério de conclusão não tenha sido atingido.

---

## E-0 - Reconhecimento e auditoria ✅

**Objetivo.** Verdade estrutural do dataset; auditar o que já existia.
**Saídas.** `scripts/profile_dataset.py`, `results/EXP-001_profile.json`,
[[EXP-001]], [[GitSkills]], [[Decision Log]], 3 skills em `.claude/skills/`.
**Concluída.** Integridade verificada; resultado anterior invalidado.

---

## E-1 - Definir a questão e o critério de segurança 🟡 parcial

**Objetivo.** Fechar [[Decision Log#D-004]] e escolher a questão central de
[[01 - Research Question]].
**Feito.** ✅ D-004 `aceita` em 2026-08-22: definição de Security Skill e as classes
`SEC-PRIMARY`/`SEC-SECONDARY`/`SEC-MENTION`/`NON-SEC`, operacionalizadas no
[[Codebook]] v1.0.
**Pendente.** ⬜ A **questão central ainda não foi escolhida** entre QI-1..QI-3 e
QP-1..QP-5. A definição diz *o que conta como Security Skill*; não diz *o que se
pergunta sobre elas*.
**Conclusão quando.** A questão tiver população, variável e critério de resposta
definidos por escrito.

---

## E-2 - Testar a validade de keywords (H-2)

**Objetivo.** Descobrir se keyword matching serve sequer como triagem.
**Entradas.** representantes; keywords de [[EXP-001]].
**Método.** Amostra aleatória determinística de ~100 ocorrências por keyword de alta
frequência (`token`, `audit`, `permission`, `security`); anotação manual do sentido;
precisão por keyword.
**Saídas.** `results/EXP-002_*`, [[02 - Hypotheses|H-2]] testada, lista de keywords
com precisão conhecida.
**Risco.** Anotador único = viés. Declarar como ameaça a validade.
**Conclusão quando.** Cada keyword tiver precisão estimada com intervalo de
confiança.
**Nota (revisada em 2026-08-22).** Com D-004 decidida, esta etapa **deixa de ser
prioritária** e muda de propósito: não serve mais para escolher a definição, e sim
para calibrar a **triagem** que alimenta a anotação. O critério que importa agora e
**recall** (não perder Security Skills antes da anotação), não precisão. Roda depois
do piloto E-3. Calibração já medida: o conjunto restrito de 17 keywords cobre 32,59%
dos representantes contra 52,93% do conjunto com keywords ruidosas.

---

## E-3 - Piloto do codebook e padrão-ouro

**Objetivo.** Levar o [[Codebook]] de v1.0 a instrumento com validade conhecida.
**Feito.** ✅ [[Codebook]] v1.0 escrito **antes** da anotação, com regras R-1..R-7 e
âncoras reais do dataset.
**Método.**
1. **Piloto (~50 casos)** amostrados deterministicamente, **estratificado para
   sobre-amostrar a fronteira SEC-SECONDARY / SEC-MENTION** - e ali que o
   instrumento falha, não nos extremos. Incluir casos `code-review`.
2. Revisar para v1.1 se necessário, com motivo registrado.
3. Padrão-ouro sobre amostra maior; **kappa ponderado** (classes são ordinais) e
   concordância na dicotomia PRIMARY+SECONDARY vs resto.
**Saídas.** `results/EXP-003_goldset.parquet`; [[Codebook]] v1.1 se revisado.
**Riscos.** Codebook ajustado depois de ver o resultado vira racionalização -
revisão só entre piloto e anotação definitiva, nunca durante. Anotador único e
ameaça a validade a declarar.
**Conclusão quando.** Existir padrão-ouro anotado, codebook estável e concordância
reportada.

---

## E-4 - Dataset analítico

**Objetivo.** Tabela por representante com as variáveis operacionalizadas.
**Entradas.** `artifacts` + `artifact_siblings` + `repos`; codebook.
**Método.** Script versionado; join validado por contagem antes/depois; variáveis de
[[01 - Research Question|QP-1/QP-2]] (`allowed-tools` parseado, presença de script,
padrões de execução/rede, métricas de tamanho e histórico).
**Saídas.** `results/analytic_dataset.parquet` + dicionário de dados.
**Risco.** Join com `artifact_siblings` infla linhas (`sibling_count` max 79.940).
Agregar antes de juntar.
**Conclusão quando.** Contagem de linhas bater com o denominador declarado em D-001
e o dicionário estiver escrito.

---

## E-5 - Análise exploratória

**Objetivo.** Distribuições, cauda, concentração.
**Método.** Mediana/quantis (nunca média em `stars` ou `sibling_count`);
concentração por repo e por dono; detecção de dominância por poucos atores.
**Saídas.** `results/EXP-005_*`, nota em `notes/Results/`.
**Risco.** **P-hacking.** Rotular tudo aqui como exploratório; nenhum p-valor desta
etapa vira evidência confirmatória.
**Conclusão quando.** Toda variável do dataset analítico tiver distribuição descrita.

---

## E-6 - Análise confirmatória

**Objetivo.** Testar as hipóteses declaradas a priori em [[02 - Hypotheses]].
**Método.** Escolher **antes** quais são confirmatórias; testes não paramétricos
(distribuições pesadas); tamanho de efeito sempre; correção para múltiplas
comparações; deduplicar por `file_sha` e verificar que não há dominância por poucos
repos.
**Saídas.** `results/EXP-006_*`, `notes/Results/`.
**Risco.** Dependência entre observações (60,8% de cópias) inválida testes que
assumam independência.
**Conclusão quando.** Cada hipótese confirmatória tiver resultado com efeito e IC.

---

## E-7 - Robustez e sensibilidade

**Objetivo.** Descobrir se as conclusões dependem de uma única escolha.
**Método.** Repetir E-6 sob: (a) denominador alternativo (ocorrência vs conteúdo);
(b) critério alternativo de segurança; (c) exclusão dos 10 maiores repos e dos 10
maiores donos; (d) só repos com >= 1 star; (e) thresholds deslocados.
**Saídas.** tabela de sensibilidade.
**Conclusão quando.** Cada conclusão principal tiver o intervalo de variação
reportado sob as alternativas.
**Nota.** Se uma conclusão só vale sob uma configuração, **isso é o achado** - e
deve ser reportado como tal, não escondido.

---

## E-8 - Revisão adversarial

**Objetivo.** Tentar derrubar as próprias conclusões.
**Método.** Para cada achado: explicação alternativa? viés de seleção ou
sobrevivência? leakage? depende de uma decisão? o resultado e frequência sendo lida
como importância? ausência de evidência lida como evidência de ausência? a
interpretação vai além do dado? outro pesquisador reproduz?
**Saídas.** `notes/Results/Adversarial Review.md`.
**Conclusão quando.** Cada achado tiver sobrevivido ou sido rebaixado a observação.

---

## E-9 - Literatura

**Objetivo.** Situar contra trabalho existente.
**Método.** Fontes primárias (papers, spec oficial da Anthropic, OWASP Top 10 for
LLM Applications). Blog não sustenta afirmação científica quando há literatura
primária. Não inventar referência.
**Saídas.** `notes/Literature/`.
**Nota.** Pode correr em paralelo desde E-1. **Começar cedo** - a literatura pode
mudar a taxonomia de E-3.

---

## E-10 - Consolidação

**Objetivo.** Material pronto para escrita.
**Saídas.** `notes/Results/` consolidado; ameaças a validade (construto, interna,
externa, conclusão); figuras geradas a partir de `results/`; rastro
dado → transformação → código → output → análise → conclusão verificado ponta a
ponta.
**Conclusão quando.** Todo número do texto tiver um `EXP-XXX` e um script.

---

## Ordem recomendada

```
E-0 ✅ → E-1 🟡 (D-004 + D-006 ✅ / questão central pendente)
      → E-2b ✅ candidate retrieval e amostra de descoberta (EXP-002)
      → E-3  piloto de anotação humana   ← PRÓXIMO PASSO
      → E-3b open coding humano iterativo → taxonomia estabilizada
      → E-3c gold set + concordância + classificador validado
      → E-11 QI-2 em escala
      → E-12 QI-3 (crosswalk, aplicabilidade, cobertura)
      → E-4 → E-5 → E-6 → E-7 → E-8 → E-10
E-9 em paralelo desde já
```

**Mudança de ordem em 2026-08-22.** E-2 vinha antes de E-3 para informar a decisão
D-004. Com D-004 decidida, a prioridade inverte: o piloto (E-3) passa a ser o próximo
passo, e E-2 vira pergunta subordinada — "que triagem alimenta a anotação com bom
recall", não mais "keyword serve como definição".

---

## Etapas acrescentadas em 2026-08-22

### E-2b — Candidate retrieval ✅

Feito em [[EXP-002]]. Pool = **78,69%** dos representantes; amostra de descoberta de
48 casos em 4 estratos. Conclusão: keyword não é filtro útil; o desenho tem de ser
amostra anotada → classificador validado → escala.

### E-3b — Open coding humano iterativo

**Objetivo.** Levar [[Security Taxonomy]] de v0.1 (semeada por LLM, **não validada**)
a taxonomia estabilizada.
**Método.** [[QI-2 Methodology]] §4. Iterar amostra → códigos → agrupamento →
refinamento, datando cada mudança.
**Conclusão quando.** Uma iteração completa não produzir código novo relevante.

### E-3c — Gold set, concordância e classificador

**Objetivo.** Instrumento com validade conhecida.
**Método.** [[Codebook]] §9 — kappa ponderado nos quatro ordinais (excluindo
`AMBIGUOUS`), kappa/α na dicotomia, Krippendorff's α nas dimensões multi-label.
Classificador validado contra o gold set.
**Conclusão quando.** Precisão/recall/F1 com IC reportados **por classe** e para a
dicotomia, com matriz de confusão.

### E-11 — QI-2 em escala

**Objetivo.** Responder QI-2 com evidência.
**Método.** Distribuições nas quatro camadas de denominador (A/B/C/D,
[[QI-2 Methodology]] §5), sempre com concentração por repositório **e por dono**
([[Decision Log#D-001]], [[Decision Log#D-010]]).
**Conclusão quando.** As oito perguntas de saída da QI-2 tiverem resposta sustentada
por classificação validada.

### E-12 — QI-3

**Objetivo.** Responder QI-3.
**Dependências.** E-11 concluída **e** [[Decision Log#D-009]] aprovada.
**Método.** [[QI-3 Coverage Methodology]] — escolha justificada de frameworks,
aplicabilidade antes de cobertura, crosswalk com relações 1:1/1:N/N:1/sem
correspondência, seis níveis de cobertura, sensitivity analysis em todo limiar.
**Conclusão quando.** Toda ausência observada tiver as cinco explicações
concorrentes examinadas e registradas.

## Ligações

[[00 - Research Overview]] · [[01 - Research Question]] · [[02 - Hypotheses]] ·
[[Decision Log]] · [[Codebook]] · [[QI-2 Methodology]] ·
[[QI-3 Coverage Methodology]] · [[Security Taxonomy]] · [[EXP-001]] · [[EXP-002]]
