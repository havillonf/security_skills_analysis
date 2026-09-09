---
tipo: metodologia
atualizado: 2026-08-22
status: reorganizado em torno da QI-1
---

# Plano de pesquisa — QI-1

> **Questão central: QI-1.** Qual a prevalência de skills de segurança na população
> pública de Agent Skills? ([[Decision Log#D-011]])
>
> Security Skill = `SEC-PRIMARY` + `SEC-SECONDARY`, sempre desagregados.
> População: **skills em inglês** ([[Decision Log#D-025]], 2026-09-03,
> decisão do orientador — revisa [[Decision Log#D-012]], que incluía todos
> os idiomas).
> **Desenho C** — amostragem estratificada com classificador de triagem
> ([[Decision Log#D-014]]).
> Desenho estatístico: [[QI-1 Methodology]] · Idiomas: [[Multilingual Strategy]] ·
> Literatura: [[Multilingual Methodology Review]]
>
> Trabalho isolado na branch `Q1`.

Reorganizado em 2026-08-22. O plano anterior servia a três questões em paralelo;
agora só as etapas necessárias à QI-1 são caminho crítico. Nada foi descartado —
QI-2, QI-3 e QP-* estão preservadas em [[01 - Research Question]]§Extensões.

Não avance uma etapa cujo critério de conclusão não tenha sido atingido.

---

## Concluído e reaproveitado

| Etapa                                   | Resultado                                                                                  | Uso na QI-1                                       |
| --------------------------------------- | ------------------------------------------------------------------------------------------ | ------------------------------------------------- |
| **E-0** ✅ Auditoria estrutural          | [[EXP-001]] · integridade verificada, denominadores fixados, resultado anterior invalidado | define a população e as unidades                  |
| **E-1** ✅ Definição e instrumento       | [[Codebook]] v2.3 · [[Decision Log#D-004]], [[Decision Log#D-006\|D-006]]                  | é o instrumento de anotação                       |
| **E-2b** ✅ Candidate retrieval (inglês) | [[EXP-002]] · pool de 78,69%                                                               | baseline a superar; mostra que keyword não filtra |

Produzido para a QI-2 e **preservado sem estar no caminho crítico**:
[[QI-2 Methodology]], [[QI-3 Coverage Methodology]], [[Security Taxonomy]] v0.1.

---

## Caminho crítico da QI-1

### E-3 — Distribuição de idiomas ✅

**Objetivo.** Saber quais idiomas existem na população e em que proporção.
**Por que primeiro.** Sem isso não é possível desenhar léxico multilíngue, estratos
de amostragem nem gold set representativo ([[Decision Log#D-012]]).
**Método.** Duas camadas — script Unicode sobre a população inteira; identificação de
idioma sobre amostra aleatória determinística, com remoção de código, front matter,
URLs e caminhos antes de detectar. Ver [[Multilingual Strategy]] §2.
**Saída.** `scripts/detect_languages.py` · `results/_arquivo/EXP-003_languages.json` ·
[[EXP-003]].
**Resultado.** ✅ **Não inglês = 14,21% ± 0,48 pp (≈ 267 mil conteúdos)**; zh 5,99%,
ja 1,73%, de 1,61%, ko 1,25%, es 0,97%, pt 0,95%. Front matter diverge do corpo em
4,17%; 11,71% do conteúdo é multi-script. Estratos linguísticos propostos em
[[Multilingual Strategy]] §8.
**Pendência.** O detector **não foi validado** contra rótulos humanos — fazer antes
de usar idioma como variável de estratificação.

### E-3b — Concordância entre detectores de idioma 🟡 (acurácia pendente)

**Objetivo.** Saber se o rótulo de idioma sustenta estratificação.
**Atenção.** Mede **concordância**, não acurácia. Não há ground truth humano; a
primeira medida de acurácia sai de E-5 (campo `human_language`).
**Método (v2).** Dois detectores independentes (`lingua` primário, `py3langid`
segunda opinião) sobre **150 casos, 30 por grupo L1-L5**, pool de 12.000.
**Resultado.** Concordância global **0,987** — L1 0,967 · L2 1,000 · L3 1,000 ·
L4 1,000 · L5 0,967. Confiança do `langid` quando erra: 1,000 — inútil como filtro.
**Correção.** A **v1 estava errada**: estratificava por uma partição auxiliar em que
a checagem de script vinha antes da de idioma, o CJK inteiro caiu em `S_multilingue`
e `S_cjk` ficou com 10 casos de 6.000. Os "1,00" de L2/L3 e o "0,667" da cauda eram
transplantados de outra partição. Achado C-1 da auditoria adversarial.
**Consequência.** L5 permanece colapsado — mas por **falta de suporte amostral**
(~2% da população em mais de dez idiomas), não por falha de detecção. O viés de
[[EXP-003]] tem direção conhecida: não inglês provavelmente superestimado.
**Saída.** `scripts/validate_language_detection.py` · [[EXP-004]].
**Pendência.** Não há acurácia real — a primeira sai do piloto E-5.

### E-4 — Candidate retrieval (executado **depois de E-6**)

**Ordem definitiva** — [[Decision Log#D-018]], aprovada em 2026-08-22. Não é mais
provisória. Sob o Desenho C o retrieval **estratifica** e não determina
elegibilidade: nenhuma skill é descartada por não ser recuperada. O critério para
escolher entre retrieval lexical e semântico é **recall contra um gold set humano
independente**, que não existe antes do piloto. Fixar o retrieval antes do gold set
criaria circularidade — o instrumento de recuperação passaria a definir aquilo contra
o que ele próprio seria avaliado.

E-4 passa a ser executado **depois de E-6** e muda de escopo:

1. manter o retrieval inglês de [[EXP-002]] como **um sinal entre outros**;
2. acrescentar sinais independentes de léxico: `domain:`/`category:` no front matter,
   presença de script, `has_scripts`;
3. testar a hipótese de que `name`/`description` dá recall melhor em skills não
   inglesas (4,17% divergem, [[EXP-003]]);
4. medir **recall por idioma** contra o gold set; só então decidir entre lexical e
   semântico.

### EXP-012 — Prova de conceito do classificador (paralela, fora do caminho crítico)

> [!warning] Não é E-6/E-7/E-8
> [[EXP-012]] usa `EXP-005_annotation_form_filled_updated.csv` como
> **golden set operacional v1** (assistido por LLM) para provar o pipeline
> completo — congelar → treinar → comparar 3 modelos em 2 tarefas via CV
> agrupada/repetida → selecionar → classificar os 1.877.981 conteúdos em
> lote. **Não substitui** E-6 (gold set humano) nem produz os `N_h`
> definitivos do Desenho C. Decisão completa, métricas e a divergência entre
> "melhor em CV" (embeddings) e "implantado na população" (TF-IDF, por
> custo computacional) em [[Decision Log#D-023]].

### E-5/E-6 — Amostra + gold set via ensemble de LLMs  ← PRÓXIMA ETAPA (do caminho crítico rigoroso)

> [!important] Desenho substituído em 2026-09-03 — [[Decision Log#D-026]]
> O desenho anterior (piloto humano cego de ~50 casos estratificados por
> sinal × idioma, seguido de gold set com um ou dois anotadores humanos)
> foi **substituído** por decisão do orientador. Os parágrafos abaixo
> descrevem o desenho **vigente**; o desenho anterior fica preservado só
> como histórico em [[Decision Log#D-019]], [[Decision Log#D-020]] e
> [[Decision Log#D-021]], que continuam valendo como princípios (cegamento,
> LLM não é ground truth **fora** deste desenho específico) mas não como
> procedimento em execução.

**Objetivo.** Produzir, numa única etapa, uma amostra anotada e o padrão-ouro
operacional que alimenta a validação do classificador em **E-7**.
**Método** ([[Decision Log#D-026]]):

1. Sortear uma **amostra aleatória nova de n = 100**, sobre a população
   restrita a inglês de [[Decision Log#D-025]] — não reaproveita os 50 casos
   de [[EXP-005]]. Amostragem determinística (`ORDER BY hash(file_sha)`).
2. Três modelos — **GPT-5.6 Sol**, **Claude Opus**, **Gemini 3.1 Pro** —
   classificam os 100 casos **independentemente**, aplicando o [[Codebook]]
   v2.3, sem ver o sinal preliminar de triagem (cegamento por analogia a
   [[Decision Log#D-021]]).
3. Onde os três **concordam**, o rótulo de consenso é aceito sem revisão
   humana adicional.
4. Onde **discordam**, um anotador humano adjudica aplicando o [[Codebook]].

**Riscos declarados, não resolvidos por este desenho** (detalhe completo em
[[Decision Log#D-026]]):

- amostra **não estratificada** — pode conter poucos casos `PRIMARY`/
  `SECONDARY` e menos ainda na fronteira `SECONDARY`/`MENTION`;
- consenso entre os três LLMs **nunca é verificado por um humano** — viés
  sistemático compartilhado entre modelos fica invisível;
- a estatística de confiabilidade (concordância entre LLMs + taxa de
  adjudicação humana) não é equivalente a um kappa interavaliadores humano
  do [[Codebook]] §9, e deve ser reportada como tal.

**Saída.** Gold set de n=100 com origem de rótulo declarada por caso (consenso
de LLM vs. adjudicação humana); registro de modelo/versão/prompt/temperatura
para os três LLMs ([[Decision Log#D-008]]); taxa de discordância; taxa de
`AMBIGUOUS`.
**Conclusão quando.** Gold set versionado em `results/`, com a fração
consenso-vs-adjudicado reportada, e regras ambíguas identificadas.
**Pendências resolvidas em 2026-09-03** (reunião com o orientador, mesmo
dia de D-025/D-026): critério operacional de "skill em inglês" — 100%
inglês; regra de desempate — qualquer discordância entre os três modelos,
em qualquer dimensão, leva o caso à adjudicação humana; cegamento entre
modelos confirmado como regra explícita.

**Progresso concreto (2026-09-03):**

1. ✅ **Amostra gerada** — [[EXP-013]], `scripts/build_llm_ensemble_sample.py`.
   100 casos aceitos, filtro de idioma corrigido na prática (ver
   [[Decision Log#D-025]] — a primeira operacionalização do limiar tinha
   uma lacuna real, corrigida).
2. ✅ **Prompt reformulado** para o modo de invocação escolhido pelo
   pesquisador — CLI de cada modelo com acesso ao diretório de casos, não
   API programática. [[Classification Prompt]] §2–§5.
3. ✅ **Script de agregação/discordância** escrito e testado com dados
   sintéticos — `scripts/aggregate_llm_classifications.py`.
4. ⬜ **Rodar as três CLIs** contra `results/EXP-013_llm_cases/` — não
   feito ainda. Validar o prompt (aviso no topo do documento) antes de
   rodar para valer.
5. ⬜ **Adjudicação humana** dos casos discordantes, usando
   [[Guia do Anotador Humano]] (v2.4). A execução de 2026-09-03 sob
   a v2.3 está arquivada em `results/_arquivo/` e sua adjudicação foi
   **suspensa** — o esquema que ela media foi substituído por
   [[Decision Log#D-027]].

### E-7 — Classificador validado

**Objetivo.** Classificador com desempenho medido, para formar estratos.
**Método.** Validação contra o gold set: precisão, recall, F1 **por classe** e para a
dicotomia, com IC e matriz de confusão completa; **desempenho por idioma**.
**Análise de erro exigida.** `SECONDARY` ↔ `MENTION` é a confusão que altera a
prevalência; `PRIMARY` ↔ `SECONDARY` não altera o agregado. Reportar separadamente
([[QI-1 Methodology]] §5).
**Conclusão quando.** Métricas por classe e por idioma reportadas com IC.
**Regra.** LLM não é ground truth ([[Decision Log#D-008]]).
**Papel adicional (desde [[Decision Log#D-024]], 2026-08-27).** O resultado
desta etapa funciona como **gate metodológico** para QI-2 e QI-3: só depois
de o desempenho medido aqui ser considerado satisfatório é que a população
classificada em E-8 pode servir de base para QI-2. O critério numérico de
"satisfatório" ainda não foi definido — ver aviso em
[[Decision Log#D-024]].

### E-8 — Classificação da população

**Objetivo.** Atribuir classe prevista a cada conteúdo, formando os estratos.
**Atenção.** A contagem de positivos **não é a resposta**. Serve só para `N_h`.
**Conclusão quando.** Tamanhos de estrato (classe prevista × grupo linguístico)
conhecidos.

### E-9 — Estimativa de prevalência

**Objetivo.** Responder à QI-1.
**Método.** Estimador estratificado do Desenho C ([[QI-1 Methodology]] §3), com IC.
**Saídas obrigatórias:**
- prevalência agregada com IC95%;
- `PRIMARY` e `SECONDARY` desagregados;
- por conteúdo distinto **e** por ocorrência (difusão);
- taxa de `AMBIGUOUS` e limites inferior/superior;
- concentração por repositório **e** por dono;
- prevalência por idioma quando houver suporte amostral (secundária).
**Conclusão quando.** Todos os itens acima produzidos por script versionado.

### E-10 — Robustez e revisão adversarial

**Método.** Repetir E-9 sob: denominador alternativo (ocorrência vs conteúdo);
exclusão dos 10 maiores repos e donos; deduplicação por similaridade
([[Decision Log#D-010]]); definição alternativa de Security Skill; `AMBIGUOUS` nos
dois extremos.
Depois, revisão adversarial: explicação alternativa? viés de seleção ou
sobrevivência? a conclusão depende de uma decisão só? frequência lida como
importância? outro pesquisador reproduz?
**Conclusão quando.** Cada conclusão tiver intervalo de variação reportado. Se uma
conclusão só vale sob uma configuração, **isso é o achado**.

### E-11 — Literatura e consolidação

Fontes primárias em `notes/Literature/`; ameaças à validade (construto, interna,
externa, conclusão); rastro dado → transformação → código → output → análise →
conclusão verificado ponta a ponta. Todo número com um `EXP-XXX` e um script.
Literatura pode correr em paralelo desde já.

---

## Ordem

```text
E-0 ✅  E-1 ✅  E-2b ✅
   |
E-3  idiomas ✅                 14,21% não inglês
E-3b validação do detector ✅   lingua primário; cauda colapsada
   |
E-5/E-6  amostra n=100 (inglês) + ensemble de 3 LLMs +   <- PRÓXIMA ETAPA
         adjudicação humana na discordância (D-026)
   |
E-4  retrieval, escolhido por recall medido   (rebaixado e reordenado)
   |
E-7  classificador validado (por classe e por idioma)
   |
E-8  classificação da população -> N_h
   |
E-9  estimativa de prevalência com IC
   |
E-10 robustez (near-duplicates, D-017) + adversarial
   |
E-11 consolidação          (literatura em paralelo desde já)
```

**Reordenação definitiva** ([[Decision Log#D-018]]): E-4 saiu de antes de E-5 para
depois de E-6. Fundamentação em [[Multilingual Methodology Review]].

---

## Depois da QI-1 — QI-2 e QI-3 ([[Decision Log#D-024]])

Este plano cobre o caminho crítico da QI-1 (E-0 a E-11). QI-2 e QI-3 não são
etapas desse caminho, mas têm execução planejada e formalmente sequenciada
desde 2026-08-27:

```text
E-7  classificador validado  ── gate ──▶  E-8  classificação da população
                                                  │
                                                  ▼
                                    conjunto SEC-PRIMARY/SEC-SECONDARY
                                                  │
                                                  ▼
                                  QI-2  taxonomia emergente ([[QI-2 Methodology]])
                                                  │
                                                  ▼
                                  QI-3  crosswalk com referenciais externos
                                        ([[QI-3 Coverage Methodology]])
```

O gate é o desempenho de E-7, não a conclusão de E-9/E-10/E-11: QI-2 usa o
conjunto de skills classificado em E-8, não a estimativa final de prevalência
com IC. E-9 (estimativa), E-10 (robustez) e E-11 (consolidação) continuam a
responder QI-1 e podem correr em paralelo a QI-2/QI-3, não como pré-requisito
delas. Detalhe completo, justificativa e o aviso sobre o critério de
"validação satisfatória" ainda não definido: [[Decision Log#D-024]].

## Ligações

[[00 - Research Overview]] · [[01 - Research Question]] · [[QI-1 Methodology]] ·
[[Multilingual Strategy]] · [[Codebook]] · [[Decision Log]] · [[02 - Hypotheses]] ·
[[EXP-001]] · [[EXP-002]] · [[EXP-003]] · [[QI-2 Methodology]] ·
[[QI-3 Coverage Methodology]]
