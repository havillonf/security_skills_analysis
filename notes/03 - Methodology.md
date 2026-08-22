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
> População: **todos os idiomas** ([[Decision Log#D-012]]).
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

| Etapa | Resultado | Uso na QI-1 |
|---|---|---|
| **E-0** ✅ Auditoria estrutural | [[EXP-001]] · integridade verificada, denominadores fixados, resultado anterior invalidado | define a população e as unidades |
| **E-1** ✅ Definição e instrumento | [[Codebook]] v2.3 · [[Decision Log#D-004]], [[Decision Log#D-006\|D-006]] | é o instrumento de anotação |
| **E-2b** ✅ Candidate retrieval (inglês) | [[EXP-002]] · pool de 78,69% | baseline a superar; mostra que keyword não filtra |

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
**Saída.** `scripts/detect_languages.py` · `results/EXP-003_languages.json` ·
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

### E-5 — Piloto de anotação  ← PRÓXIMA ETAPA

**Objetivo.** Testar o [[Codebook]] v2.3 antes de investir na anotação grande.
**Método.** ~50 casos, estratificados por **classe prevista × grupo linguístico**
(L1–L5), sobre-amostrando:

- a fronteira `SECONDARY`/`MENTION` — onde o instrumento falha;
- conteúdo **não inglês**, obrigatoriamente presente desde o piloto;
- casos **`mixed`** e de cauda;
- casos de **GRC** ([[Decision Log#D-016]]), com concordância reportada à parte;
- casos `code-review`.

Dois anotadores independentes quando viável. Registrar `used_translation`, o idioma
julgado por humano (fecha a lacuna de [[EXP-004]]) e o **tempo por item por idioma** —
se anotar em chinês custar três vezes mais, isso muda o dimensionamento do gold set.

**Saída.** [[Codebook]] v2.3 se revisado, com motivo datado; primeira medida real de
acurácia de detecção de idioma.
**Conclusão quando.** R-2 se mostrar aplicável; custo por item medido por idioma;
regras ambíguas identificadas; concordância preliminar em GRC conhecida.
**Risco.** Ajustar o codebook depois de ver resultado vira racionalização — revisão
só entre piloto e anotação definitiva, nunca durante.

### E-6 — Gold set e concordância

**Objetivo.** Padrão-ouro humano com confiabilidade conhecida.
**Método.** Amostra estratificada por idioma/grupo linguístico. Dois anotadores
quando viável; adjudicação registrada. Métricas do [[Codebook]] §9 — kappa ponderado
nos quatro ordinais (excluindo `AMBIGUOUS`), kappa/α na dicotomia.
**Conclusão quando.** Gold set versionado em `results/` e concordância reportada,
incluindo por idioma quando houver suporte.

### E-7 — Classificador validado

**Objetivo.** Classificador com desempenho medido, para formar estratos.
**Método.** Validação contra o gold set: precisão, recall, F1 **por classe** e para a
dicotomia, com IC e matriz de confusão completa; **desempenho por idioma**.
**Análise de erro exigida.** `SECONDARY` ↔ `MENTION` é a confusão que altera a
prevalência; `PRIMARY` ↔ `SECONDARY` não altera o agregado. Reportar separadamente
([[QI-1 Methodology]] §5).
**Conclusão quando.** Métricas por classe e por idioma reportadas com IC.
**Regra.** LLM não é ground truth ([[Decision Log#D-008]]).

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
E-5  piloto de anotação          <- PRÓXIMA ETAPA
   |
E-6  gold set + concordância
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

## Ligações

[[00 - Research Overview]] · [[01 - Research Question]] · [[QI-1 Methodology]] ·
[[Multilingual Strategy]] · [[Codebook]] · [[Decision Log]] · [[02 - Hypotheses]] ·
[[EXP-001]] · [[EXP-002]] · [[EXP-003]] · [[QI-2 Methodology]] ·
[[QI-3 Coverage Methodology]]
