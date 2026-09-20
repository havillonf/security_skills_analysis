---
tipo: metodologia
atualizado: 2026-09-13
status: E-5/E-6 e quadro concluídos; próxima etapa E-7
---

# Plano de pesquisa — QI-1

> **Questão central: QI-1.** Qual a prevalência de skills de segurança na população
> pública de Agent Skills? ([[Decision Log#D-011]])
>
> Security Skill = `PRIMARY` + `SECONDARY`, sempre desagregados. Três classes
> (`PRIMARY`/`SECONDARY`/`NONE`, [[Decision Log#D-027]]).
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
| **E-1** ✅ Definição e instrumento       | [[Codebook]] v2.6 (três classes) · [[Decision Log#D-027]], [[Decision Log#D-029\|D-029]], [[Decision Log#D-030\|D-030]] | é o instrumento de anotação                       |
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

### E-5/E-6 — Amostra + gold set via ensemble de LLMs ✅ (2026-09-13)

> [!success] Concluído — gold set de **99 casos** em `results/EXP-014_gold_set.csv`
> [[EXP-013]] (amostra) · [[EXP-014]] (classificação, concordância e
> adjudicação) · [[Decision Log#D-026]] · [[Decision Log#D-031]]

O desenho foi revisado três vezes ao longo da execução, sempre registrado:

| Previsto no D-026 (2026-09-03) | Executado |
|---|---|
| 3 modelos (GPT, Claude, Gemini) | **2 modelos**. A cota do Gemini acabou; 91/100 casos, arquivados em `results/_arquivo/` |
| Codebook v2.3, cinco classes | **v2.4 → v2.6, três classes** (D-027, D-029, D-030) |
| Qualquer dimensão divergente vai para humano | **Só a classe** decide (D-029): 16 casos em vez de 50 |
| Um anotador humano adjudica | **Dois anotadores independentes + reconciliação mútua** (D-031) |

**Resultados**

- Concordância entre modelos na dicotomia da QI-1: κ = 0,672 (substancial).
  Classe: κ = 0,724.
- Concordância humana nos 16 casos difíceis: 10/16 na marcação original
  (κ = 0,186), 12/16 após corrigir dois erros de marcação (κ = 0,458).
- Gold set: 83 de consenso entre modelos, 16 humanos. LLM078 ficou fora do
  quadro. `PRIMARY` 9 · `SECONDARY` 46 · `NONE` 44.
- Marcações de quadro: LLM092 `truncated_undecidable`; LLM019 e LLM067
  `not_an_instruction_artifact`.

**Estimativa preliminar** (tratando o gold set como amostra aleatória simples,
n=98): Security Skill **56,1% [46,2%; 65,5%]**. **Não é a resposta**: 83
rótulos não passaram por humano, e a margem é de ~±10 pp.

**Riscos que continuam declarados:** consenso entre modelos nunca verificado
por humano; McNemar p = 0,0042 entre os modelos (viés direcional); vazamento de
cegamento pelo plugin `remember` num dos avaliadores ([[EXP-014]] §Limitações).

### E-Q — Quadro de análise ✅ (2026-09-05)

**Objetivo.** O denominador da QI-1, com as exclusões de quadro aplicadas em
sequência.
**Resultado.** 1.877.981 → só inglês (D-025) 1.571.243 → evidência ≥ 200
caracteres (D-028) **1.550.550**. As exclusões medidas isoladamente se
sobrepõem (4.591 arquivos são não ingleses e pequenos), então **não se somam
marginais**. Os estratos de gênero do D-030 são **marcados, não excluídos**:
F1 1.339.453 · F3 205.928 (taxa de não-instrução desconhecida) · F1b 4.543 ·
F2 626.
**Saída.** [[EXP-015]] (regra de não-instrução, recall baixo demais para
filtrar) · [[EXP-016]] · `scripts/build_analysis_frame.py`.
**Pendência.** Estimar a taxa de não-instrução em F3 antes de fechar o
denominador final.

### E-7 — Validar o LLM local do orientador ⭐ PRÓXIMA ETAPA

**Objetivo.** Saber se o LLM local do orientador classifica bem o bastante para
formar estratos (E-8) e para abrir o gate da QI-2 ([[Decision Log#D-024]]).

**Pré-requisitos** (informação do orientador, ainda não disponível):

- modelo e versão exata;
- forma de chamada: API compatível com OpenAI (Ollama, vLLM, LM Studio) ou
  outra;
- hardware e throughput esperado;
- se aceita temperatura 0;
- janela de contexto. O `SKILL.md` mediano tem ~5 mil caracteres, e o prompt de
  classificação é longo.

**Passos**

1. **Congelar o gold set** num commit antes de qualquer modelo novo vê-lo. O
   prompt é o [[Classification Prompt]] v2.6 **sem ajuste feito com o gold set**.
   Se precisar calibrar, usar uma amostra de desenvolvimento separada. Ajustar o
   prompt olhando o gold set e depois medir contra ele é circular.
2. **Harness** `scripts/run_local_llm_classification.py`:
   - endpoint configurável;
   - registra modelo, versão, hash do prompt e temperatura (D-008);
   - saída `.jsonl` no formato que `compute_agreement.py` já lê;
   - retomável: o que já foi classificado sai por anti-join;
   - `ThreadPoolExecutor`, não `ProcessPoolExecutor` (armadilha do Windows);
   - lê `EXP-013_llm_cases/` **sem escrever lá** (diretório cego);
   - plugin `remember` desativado na sessão.
3. **Medir o throughput nos 99** e projetar para 1.550.550. É isso que decide
   entre classificar a população inteira e o desenho em dois estágios
   ([[Decision Log#D-015]]).
4. **Métricas contra o gold set:**
   - P/R/F1 por classe e na dicotomia, com IC por bootstrap;
   - matriz de confusão;
   - erros `NONE`↔`SECONDARY` reportados à parte, porque são os que mudam a
     prevalência;
   - **resultados separados para os 83 casos de consenso e os 16 humanos.**
     Concordar com rótulos que vieram do GPT e do Claude pode ser só herdar um
     viés compartilhado; os 16 humanos são os casos difíceis e o teste mais
     honesto.
5. **Pré-registrar o critério de "satisfatório"** **antes** de ver as métricas.
   Está em aberto desde o D-024. É decisão humana e vira entrada no Decision
   Log. Sem isso, qualquer resultado pode ser declarado bom depois.
6. **Levar ao orientador a decisão de desenho**, com números. A prevalência
   preliminar perto de 50% muda a conta do Desenho C, que foi dimensionado para
   ~5%:

   | Opção | O que exige | Quando compensa |
   |---|---|---|
   | **Desenho C** (D-014) | classificar a população inteira + amostra humana por estrato | se o classificador separa bem, os estratos ficam puros e a margem cai muito por caso lido |
   | **Amostra aleatória simples expandida** | ~384 casos para ±5 pp com p≈0,5, pelo mesmo pipeline ensemble + humano | se o throughput local inviabiliza os 1,55M, ou se o classificador separa mal |
   | **Dois estágios** (D-015) | classificar uma subamostra grande, com `N_h` estimado | meio-termo de custo |

   E propor rever o **E-4**: busca por keyword não filtra (78,69%, [[EXP-002]]),
   e com um LLM fazendo a triagem o papel do E-4 talvez desapareça.

**Conclusão quando.** Métricas por classe com IC, critério de gate
pré-registrado e decidido, e desenho do E-8/E-9 escolhido pelo orientador.
**Passar no gate libera também a subclassificação** (QI-2, abaixo).

> [!note] Se o LLM local passar no gate, ele tem um segundo papel
> Pelo [[Decision Log#D-032]], a codificação taxonômica usa um LLM para
> **propor** códigos, de preferência um modelo diferente dos que escreveram as
> notas (GPT e Claude). O LLM do orientador é o candidato natural.
**Regra.** LLM não é ground truth ([[Decision Log#D-008]]).

### E-8 — Classificação da população

**Objetivo.** Atribuir classe prevista a cada conteúdo do quadro, formando os
estratos.
**Atenção.** A contagem de positivos **não é a resposta**. Serve só para `N_h`.
**Conclusão quando.** Tamanhos de estrato conhecidos, ou estimados, no desenho
em dois estágios.

### E-9 — Estimativa de prevalência

**Objetivo.** Responder à QI-1.
**Método.** Estimador do desenho escolhido no E-7 ([[QI-1 Methodology]] §3), com
IC.
**Saídas obrigatórias:**
- prevalência agregada com IC95%;
- `PRIMARY` e `SECONDARY` desagregados;
- por conteúdo distinto **e** por ocorrência (difusão);
- exclusões de quadro reportadas: contagem de `truncated_undecidable` com
  **limites de Manski** (D-028); taxa de `not_an_instruction_artifact` e
  sensibilidade com e sem eles (D-030);
- concentração por repositório **e** por dono.

**Conclusão quando.** Todos os itens acima produzidos por script versionado.

### E-10 — Robustez e revisão adversarial

**Método.** Repetir o E-9 sob:
- denominador alternativo (ocorrência vs. conteúdo);
- exclusão dos 10 maiores repositórios e donos;
- deduplicação por similaridade ([[Decision Log#D-017]]);
- definição alternativa de Security Skill (por exemplo, só `PRIMARY`);
- exclusões de quadro nos dois extremos.

Depois, revisão adversarial: existe explicação alternativa? viés de seleção ou
de sobrevivência? a conclusão depende de uma decisão só? frequência foi lida
como importância? outro pesquisador reproduz?
**Conclusão quando.** Cada conclusão tiver intervalo de variação reportado. Se
uma conclusão só vale sob uma configuração, **isso é o achado**.

### E-11 — Literatura e consolidação

Fontes primárias em `notes/Literature/`; ameaças à validade (construto,
interna, externa, conclusão); rastro dado → transformação → código → saída →
análise → conclusão verificado ponta a ponta. Todo número com um `EXP-XXX` e um
script. A literatura pode correr em paralelo desde já.

---

## Ordem

```text
E-0 ✅  E-1 ✅  E-2b ✅
   |
E-3 / E-3b  idiomas ✅ ──> D-025: população restrita a inglês
   |
E-5/E-6  amostra n=100 + ensemble de 2 LLMs +              ✅ 2026-09-13
         2 anotadores humanos na discordância   -> gold set 99
   |
E-Q      quadro de análise (EXP-015, EXP-016)               ✅ 1.550.550
   |
E-7      validar o LLM local do orientador + escolher o desenho  <- PRÓXIMA ETAPA
   |
E-4      retrieval — rever se ainda faz sentido (decisão no E-7)
   |
E-8      classificação da população -> N_h
   |                                    \
E-9      estimativa de prevalência com IC   QI-2  subclassificação de PRIMARY ∪ SECONDARY
   |                                              (depois do gate do E-7; LLM propõe,
   |                                               humanos validam — D-032)
   |
E-10     robustez (near-duplicates, D-017) + adversarial
   |
E-11     consolidação          (literatura em paralelo desde já)
```

**Reordenação** ([[Decision Log#D-018]]): o E-4 saiu de antes do E-5 para depois
do E-6. Desde 2026-09-13 ele fica **condicionado** à decisão de desenho do E-7.

---

## Depois da QI-1 — QI-2 e QI-3 ([[Decision Log#D-024]])

Este plano cobre o caminho crítico da QI-1 (E-0 a E-11). QI-2 e QI-3 não são
etapas desse caminho, mas têm execução planejada e formalmente sequenciada
desde 2026-08-27:

```text
E-7  classificador validado  ── gate ──▶  E-8  classificação da população
                                                  │
                                                  ▼
                                    conjunto PRIMARY ∪ SECONDARY
                                                  │
                                                  ▼
                                  QI-2  subclassificação / taxonomia emergente
                                        ([[Taxonomy Coding Protocol]] v1.1:
                                         LLM propõe, humanos validam — D-032)
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

**Ordem reafirmada em 2026-09-13** ([[Decision Log#D-032]]): a subclassificação
não é antecipada como piloto no gold set, apesar de o protocolo seguir sem
teste até lá. Consequência a ter em mente: a estimativa preliminar de 56%
continua sem decomposição do `SECONDARY` até o E-8.

## Ligações

[[00 - Research Overview]] · [[01 - Research Question]] · [[QI-1 Methodology]] ·
[[Multilingual Strategy]] · [[Codebook]] · [[Decision Log]] · [[02 - Hypotheses]] ·
[[EXP-001]] · [[EXP-002]] · [[EXP-003]] · [[QI-2 Methodology]] ·
[[QI-3 Coverage Methodology]] · [[EXP-014]] · [[EXP-016]] · [[Decision Log#D-031]]
