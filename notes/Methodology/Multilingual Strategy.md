---
tipo: metodologia
data: 2026-08-22
status: proposta - distribuicao medida (EXP-003)
decisoes: D-012, D-013
---

# Estratégia multilíngue

Decorre de [[Decision Log#D-012]] (população inclui todos os idiomas) e
[[Decision Log#D-013]] (tradução é auxiliar, nunca substituição).

> [!danger] Regra da população
> A língua em que uma skill foi escrita **não determina** se ela entra na pesquisa.
> Não descartar por idioma. Não classificar não inglês como `NONE`/`AMBIGUOUS`.
> Não tratar inglês como padrão de relevância. Ausência de termos ingleses **não é**
> ausência de preocupação de segurança.

---

## 1. Por que isso é difícil neste corpus

Agent skills são um caso ruim para detecção de idioma:

- **Código e prosa misturados.** Blocos de código, caminhos e nomes de ferramentas
  são "ingleses" mesmo em skill escrita em outro idioma.
- **Termos técnicos ingleses embutidos.** Uma skill em português diz "SQL injection",
  "prompt injection", "secrets". Isso é **evidência válida de segurança**, não ruído.
- **Front matter em inglês, corpo em outro idioma.** Observado em [[EXP-002]]:
  `ywc-iac-author` tem `description` em inglês com triggers em coreano e japonês.
- **Textos genuinamente multilíngues.** Não é um erro a corrigir: é uma categoria.
- **Textos curtos ou quase só código.** Idioma pode ser indeterminável.

Consequência: "o idioma da skill" nem sempre é uma pergunta bem posta. O desenho
tem de admitir `mixed` e `und` (indeterminado) como valores legítimos.

---

## 2. Detecção — desenho em duas camadas ([[EXP-003]])

**Camada 1 — script Unicode, sobre a população inteira.** Barato, exato e sem
modelo: detecta presença de Han, Hiragana/Katakana, Hangul, Cirílico, Árabe,
Hebraico, Devanágari, Grego, Tailandês. Dá o piso de conteúdo não latino sem
nenhuma suposição.

**Camada 2 — identificação de idioma, sobre amostra aleatória.** Necessária porque
a camada 1 não separa idiomas de escrita latina (inglês, português, espanhol,
francês, alemão, italiano...). Aplicada a uma amostra grande o suficiente para
estimar proporções com precisão útil.

**Pré-processamento antes de detectar** (o texto cru enganaria o detector):

1. remover blocos de código cercados e código inline;
2. remover front matter YAML — analisado à parte, pode divergir do corpo;
3. remover URLs, caminhos e nomes de arquivo;
4. só então identificar o idioma da prosa restante.

**Registrar sempre:** idioma do corpo, idioma do front matter, se divergem, e a
confiança do detector. Baixa confiança → `und`, nunca um palpite.

---

## 3. Candidate retrieval multilíngue

O retrieval de [[EXP-002]] (58 termos, só inglês, pool de 78,69%) **não serve como
desenho final** — permanece só como medição já feita e baseline a superar.

Requisitos para o substituto:

- não usar apenas termos ingleses;
- investigar terminologia de segurança **nos idiomas efetivamente presentes**, o que
  só é possível depois de [[EXP-003]];
- considerar variantes morfológicas (flexão, composição — relevante em alemão, russo,
  português);
- considerar **termos ingleses embutidos** em texto de outro idioma;
- considerar textos multilíngues;
- avaliar **recall por idioma** quando houver dados suficientes.

> [!warning] Traduzir a lista de keywords não basta
> Traduzir 58 termos ingleses para N idiomas produz um léxico que ignora como cada
> idioma realmente fala de segurança, perde termos sem equivalente direto e erra a
> morfologia. É ponto de partida, não solução.

**Se a via lexical se mostrar inadequada** — o critério é recall por idioma medido
contra o gold set — as alternativas são embeddings multilíngues (recuperação
semântica) ou um classificador multilíngue direto, dispensando retrieval lexical.
Decisão a tomar com dados de [[EXP-003]] e [[EXP-004]] em mãos.

Lembrando que, dado o pool de 78,69%, **o retrieval provavelmente não é o gargalo**:
com o Desenho C de [[QI-1 Methodology]], a triagem serve para estratificar, e
estratificação imperfeita custa precisão, não validade.

---

## 4. Gold set e validação

- Amostra de anotação **estratificada por idioma ou grupo linguístico**, quando
  metodologicamente apropriado.
- **Evitar gold set quase só em inglês** se a população não for.
- Sobre-amostrar idiomas minoritários é legítimo no Desenho C: a estratificação é
  corrigida pelos pesos `N_h / N` no estimador.
- Desempenho avaliado separadamente por idioma sempre que houver suporte amostral.

```text
desempenho global
   + desempenho em inglês
   + desempenho em português
   + desempenho em espanhol
   + demais idiomas com suporte suficiente
```

> **F1 global bom não é evidência de desempenho uniforme.** Se o inglês domina a
> população, um classificador que falha em chinês ainda mostra F1 global alto.

Queda relevante de desempenho num idioma → **ameaça à validade da estimativa de
prevalência**, registrada em [[QI-1 Methodology]] §6, não escondida no agregado.

---

## 5. Tradução ([[Decision Log#D-013]])

Quando necessária para apoiar anotação ou classificação:

- **preservar sempre o original**; a tradução é coluna adicional, nunca substituição;
- **nunca sobrescrever** o conteúdo original;
- registrar `used_translation: true` quando a decisão classificatória dependeu dela;
- considerar perda semântica, sobretudo em terminologia técnica de segurança.

**Preferência:** classificador capaz de raciocinar **diretamente sobre o idioma
original**, em vez de traduzir o corpus antecipadamente. Traduzir antes de
classificar introduz um erro que depois não se separa do erro do classificador.

Na anotação humana, a ordem preferida é: (1) anotador que domina o idioma;
(2) tradução como apoio, marcada; (3) `AMBIGUOUS` **nunca** por motivo de idioma —
ver [[Codebook]] R-9.

---

## 6. Prevalência por idioma

A estimativa principal da QI-1 cobre **toda a população analisável**.

Desagregação por idioma é **secundária**, salvo se os dados indicarem diferenças
relevantes. Nunca comparar idiomas sem considerar:

- tamanho das populações;
- incerteza estatística de cada estimativa;
- qualidade do classificador **naquele** idioma;
- diferenças de composição dos ecossistemas (um idioma pode concentrar um tipo de
  projeto);
- possíveis vieses do candidate retrieval por idioma.

---

## 7. Riscos metodológicos

| Risco | Consequência | Mitigação |
|---|---|---|
| Detector de idioma erra em texto com muito código | estratos por idioma contaminados | pré-processamento §2; `und` explícito |
| Léxico enviesado para inglês | recall menor em outros idiomas → **prevalência subestimada** neles | recall por idioma; alternativa semântica |
| Classificador pior em idiomas minoritários | erro heterogêneo, não visível no agregado | métricas por idioma |
| Gold set predominantemente inglês | validação não representa a população | estratificação por idioma |
| Perda semântica na tradução | erro que se confunde com erro do classificador | preferir modelo multilíngue direto; marcar `used_translation` |
| Idioma correlacionado com tipo de skill | diferença de prevalência confundida com diferença de ecossistema | não comparar sem os cinco fatores da §6 |
| Idiomas com pouquíssimos casos | sem suporte amostral para avaliação separada | declarar, **não** descartar da população |

---

## 8. Distribuição medida ([[EXP-003]], 2026-08-22)

**Não inglês: 14,21% ± 0,48 pp → ≈ 266.955 conteúdos** de 1.877.981.
Camada 1 (exata, população inteira): 14,06% contêm script não latino.

| Grupo | Idiomas | Share | Suporte para avaliação separada |
|---|---|---|---|
| Dominante | en 84,61% | ~1,59 M | sim |
| Massa relevante | **zh 5,99%** · ja 1,73% · de 1,61% · ko 1,25% · es 0,97% · pt 0,95% | ~215 k | sim |
| Cauda | fr 0,41% · ru 0,26% · vi 0,25% · tr 0,17% · ar 0,10% · it 0,09% | ~24 k | só com amostra dedicada |
| Indeterminado | und 0,82% | ~15 k | — |

Dois fatos que mudam o desenho:

- **Front matter diverge do corpo em 4,17%** — tipicamente `name`/`description` em
  inglês com corpo em outro idioma. Detectar idioma só pelo front matter erraria
  essas skills. Hipótese ainda não testada: um retrieval sobre `name`/`description`
  pode ter **melhor** recall em skills não inglesas justamente por isso.
- **11,71% do conteúdo é multi-script** — termos técnicos ingleses embutidos em texto
  de outro idioma. Favorece um léxico que **inclua** termos ingleses; desfavorece
  tratar idioma como partição limpa. O rótulo `mixed` do [[Codebook]] R-9 é
  necessário, não decorativo.

### Estratos linguísticos — versão pós-validação ([[EXP-004]])

Para o gold set e para o estimador do Desenho C ([[QI-1 Methodology]] §3):

```text
L1  en                       ~84,6%   concordância entre detectores 1,00
L2  zh                        ~6,0%   1,00
L3  ja + ko                   ~3,0%   1,00
L4  de + es + pt + fr + it    ~4,0%   1,00
L5  cauda + und + mixed       ~2,4%   0,667  -> NÃO estratificar internamente
```

Mudança em relação à proposta inicial: **L5 absorve `mixed` e a cauda inteira**. A
concordância de 0,667 naquele estrato não sustenta separação por idioma. `la` entra
em L5 como artefato, nunca como idioma.

Sobre-amostrar L2–L5 é legítimo — os pesos `N_h / N` corrigem no estimador.

### Detector: o que a validação mostrou

[[EXP-004]] mediu concordância entre `py3langid` e `lingua` em 118 casos:

- **A confiança do `langid` é inútil como filtro.** Quando os dois detectores
  discordam, a confiança do langid tem média **0,969** e chega a **1,000**. A
  superconfiança deixou de ser suspeita e passou a ser medida.
- **`lingua` passa a detector primário**, `py3langid` como segunda opinião. Onde
  discordam, o registro fica marcado — não se escolhe em silêncio.
- **Direção do viés é conhecida:** o langid inventa idiomas raros (`la`, `km`, `vi`)
  para texto inglês, então o não inglês de [[EXP-003]] está provavelmente
  **superestimado** (14,21% → perto de 13,5% se `la` e `vi` forem inglês).

> [!warning] Ainda não há acurácia real
> Concordância entre detectores **não é acurácia**, e a inspeção das discordâncias em
> [[EXP-004]] foi feita por LLM, não por anotador humano. A primeira medida de
> acurácia verdadeira deve sair do piloto [[03 - Methodology|E-5]], aproveitando o
> julgamento humano que já estará ocorrendo.

## Ligações

[[QI-1 Methodology]] · [[Codebook]] · [[Decision Log]] · [[EXP-002]] ·
[[EXP-003]] · [[GitSkills]] · [[03 - Methodology]]
