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
> Desenho estatístico: [[QI-1 Methodology]] · Idiomas: [[Multilingual Strategy]]

Reorganizado em 2026-08-22. O plano anterior servia a três questões em paralelo;
agora só as etapas necessárias à QI-1 são caminho crítico. Nada foi descartado —
QI-2, QI-3 e QP-* estão preservadas em [[01 - Research Question]]§Extensões.

Não avance uma etapa cujo critério de conclusão não tenha sido atingido.

---

## Concluído e reaproveitado

| Etapa | Resultado | Uso na QI-1 |
|---|---|---|
| **E-0** ✅ Auditoria estrutural | [[EXP-001]] · integridade verificada, denominadores fixados, resultado anterior invalidado | define a população e as unidades |
| **E-1** ✅ Definição e instrumento | [[Codebook]] v2.1 · [[Decision Log#D-004]], [[Decision Log#D-006\|D-006]] | é o instrumento de anotação |
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

### E-4 — Candidate retrieval multilíngue

**Objetivo.** Triagem que não penalize idiomas.
**Entradas.** E-3.
**Método.** Terminologia de segurança nos idiomas efetivamente presentes; variantes
morfológicas; termos ingleses embutidos; textos multilíngues.
**Critério de escolha.** **Recall por idioma** contra o gold set — nunca tamanho do
pool. Se a via lexical falhar, avaliar embeddings multilíngues ou classificador
multilíngue direto. Ver [[Multilingual Strategy]] §3.
**Risco.** Traduzir a lista inglesa e achar que resolveu.
**Nota.** Dado o pool de 78,69% e o Desenho C, o retrieval provavelmente **não é o
gargalo**: serve para estratificar, e estratificação imperfeita custa precisão, não
validade.

### E-5 — Piloto de anotação

**Objetivo.** Testar o [[Codebook]] v2.1 antes de investir na anotação grande.
**Método.** ~50 casos, sobre-amostrando a fronteira `SECONDARY`/`MENTION` (é onde o
instrumento falha, não nos extremos) **e** conteúdo não inglês. Incluir casos
`code-review`.
**Saída.** [[Codebook]] v2.2 se revisado, com motivo datado.
**Conclusão quando.** R-2 se mostrar aplicável na prática; custo por item medido;
regras ambíguas identificadas.
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
E-3  idiomas ✅         14,21% não inglês
   |
E-4  retrieval multilíngue   <- próxima etapa
   |
E-5  piloto de anotação
   |
E-6  gold set + concordância
   |
E-7  classificador validado
   |
E-8  classificação da população (estratos)
   |
E-9  estimativa de prevalência com IC
   |
E-10 robustez + adversarial
   |
E-11 consolidação          (literatura em paralelo desde já)
```

## Ligações

[[00 - Research Overview]] · [[01 - Research Question]] · [[QI-1 Methodology]] ·
[[Multilingual Strategy]] · [[Codebook]] · [[Decision Log]] · [[02 - Hypotheses]] ·
[[EXP-001]] · [[EXP-002]] · [[EXP-003]] · [[QI-2 Methodology]] ·
[[QI-3 Coverage Methodology]]
