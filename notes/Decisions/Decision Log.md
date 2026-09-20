---
tipo: decisões
atualizado: 2026-09-13
---

# Decision Log

Toda decisão metodológica relevante. Decisão já usada em experimento **não muda em
silêncio**: registra-se a revisão com data e motivo.

Status: `proposta` (aguarda pesquisador) · `aceita` · `revisada` · `rejeitada`.

> [!info] Este arquivo não é dividido, por desenho
> O valor dele é ser um registro **único e cronológico** onde se rastreia por que
> algo mudou (D-012→D-025, D-019→D-026, D-004/D-006→D-027, D-022→D-028). Separar
> "decisões antigas" quebraria exatamente a cadeia que dá defensabilidade ao
> trabalho. Use o índice abaixo para ver o estado sem perder o histórico.

## Índice de status (2026-09-13)

**Vigentes — sustentam o desenho atual**

| | Decisão | |
|---|---|---|
| D-001 | Unidade = conteúdo distinto (`dedup_primary=1`) | |
| D-005 | DuckDB sobre Parquet, via `uv` | |
| D-007 | Eixo B (segurança *da* skill) permanece separado | |
| D-008 | LLM não é ground truth | |
| D-011 | QI-1 (prevalência) é a questão central | |
| D-013 | Tradução é auxiliar, nunca substituição | |
| D-014 | **Desenho C** — estratificada com classificador de triagem | ⭐ |
| D-016 | Escopo de GRC (R-10) | |
| D-017 | Near-duplicates como análise de robustez | |
| D-018 | E-4 depois de E-6 (evita circularidade) | |
| D-021 | Cegamento da anotação | |
| D-024 | Sequência QI-1 → gate → QI-2 → QI-3 | |
| D-025 | **População restrita a inglês** (revisa D-012) | ⭐ |
| D-026 | Ensemble de LLMs + adjudicação humana na discordância | |
| D-027 | **Três classes; subclassificação posterior** (revisa D-004/D-006) | ⭐ |
| D-028 | Evidência insuficiente = exclusão de frame (fecha D-022) | ⭐ |
| D-029 | **Primeira classificação enxuta** (Codebook v2.5) | ⭐ |
| D-030 | Terceira exclusão de frame: não é instrução (Codebook v2.6) | ⭐ |
| D-031 | **Gold set**: dois anotadores independentes + reconciliação mútua | ⭐ |
| D-032 | Subclassificação depois do gate do E-7; **LLM propõe, humanos validam** | ⭐ |

**Revisadas ou encerradas — preservadas por rastreabilidade**

| | Decisão | Situação |
|---|---|---|
| D-002 | Resultado do notebook 01 inválido | histórico; a lição vale |
| D-003 | Contradições doc↔realidade: registrar | histórico |
| D-004 · D-006 | Definição operacional / esquema de classes | **revisadas por D-027** |
| D-009 | Escopo da QI-3 | **EM ABERTO** |
| D-010 | Dedup por similaridade | encerrada |
| D-012 | População inclui todos os idiomas | **revisada por D-025** |
| D-015 | Desenho multi-estágio se integral inviável | contingência não acionada |
| D-019 · D-020 | Anotador único / sinal preliminar no piloto | **substituídas por D-026** |
| D-022 | Elegibilidade da população | **fechada por D-028** |
| D-023 | Classificador v1 do EXP-012 | PoC, fora do caminho crítico |

**Em aberto:** D-009 (escopo da QI-3) e o limiar numérico de "validação
satisfatória" do gate de D-024.

---

## D-001 - Unidade de análise primária: conteúdo distinto

**Data:** 2026-08-22 · **Status:** `proposta` - requer decisão do pesquisador

**Contexto.** `artifacts` mistura dois graos: 3.797.117 ocorrências de arquivo e
1.877.981 conteúdos distintos. Apenas os representantes (`dedup_primary = 1`) tem
`content`, front matter e composição. 60,8% das ocorrências são cópias.

**Decisão proposta.** Usar **conteúdo distinto (`dedup_primary = 1`)** como unidade
primária, reportando contagem por ocorrência em paralelo como medida de *difusão*.

**Justificativa.** Contar ocorrências faz uma única skill popular copiada 5.000
vezes pesar 5.000 vezes mais que uma escrita a mao. Para perguntas sobre *o que as
pessoas escrevem*, isso é viés puro. Para perguntas sobre *o que os agentes
encontram no ecossistema*, ocorrência e a unidade certa - dai reportar as duas.

**Alternativas.**
- Ocorrência como primária: mede exposição real, mas dominada por poucos conteúdos.
- Repositório (282.200): útil para questões sobre projetos; perde a skill como
  artefato.
- Dono (195.841): controla concentração por autor; perde granularidade.

**Consequências.** Todo percentual precisa declarar o denominador. Análises de
conteúdo ficam limitadas aos 1.877.981 representantes.

**Limitações.** A escolha do representante **não é aleatória**: prefere arquivos em
`.claude/skills/`. O texto analisado tende a ser a variante mais convencional do
grupo de cópias - possível viés a favor de skills bem formadas.

> [!warning] Ressalva acrescentada em 2026-08-22 (não altera a decisão)
> [[EXP-002]] mostrou que **a deduplicação por `file_sha` não remove
> near-duplicates**. 13.187 conteúdos *distintos* com `domain: cybersecurity` vêm de
> apenas 82 repositórios, e os oito maiores donos respondem por cerca de metade, em
> contagens quase idênticas — o mesmo pacote replicado com variações mínimas,
> suficientes para mudar o hash e insuficientes para tornar as observações
> independentes.
>
> A premissa "1 voto por texto" é **mais fraca do que se supunha**. A decisão de usar
> conteúdo distinto como unidade primária **permanece** (é a melhor disponível), mas
> toda análise precisa reportar concentração por repositório **e por dono**.
> Deduplicação por similaridade é decisão em aberto — ver [[#D-010]].

---

## D-002 - Resultado do notebook 01 declarado inválido

**Data:** 2026-08-22 · **Status:** `aceita` (fato técnico verificado, não escolha)

**Contexto.** `notebooks/01_exploratory.ipynb` seção 6 reporta "1,1% das skills
mencionam ao menos um termo de segurança (53/5000)".

**Decisão.** O resultado e **inválido** e não pode ser citado, reutilizado nem
usado como baseline.

**Justificativa.** Amostragem por `pd.read_parquet(...).head(5000)`. O bloco
inicial do Parquet e um estrato, não uma amostra: um único `discovered_at`, 920
repos, e `content` com mediana de 42 caracteres - majoritariamente alvos de symlink
em vez de texto de skill. Apenas 67 de 5.000 linhas tinham front matter. Recomputado
sobre os 1.877.981 representantes com as mesmas keywords: **52,93%** - 48x maior.
Evidência completa em [[EXP-001]].

**Alternativas.** Corrigir o notebook in place foi rejeitado: apagaria o registro do
erro. O notebook permanece como legado, com aviso.

**Consequências.** O notebook e **exploratório e legado**. Nenhum número dele entra
no TCC sem recomputo por script versionado.

**Acao pendente.** Inserir celula de aviso no topo do notebook (requer aprovação,
pois altera artefato do pesquisador).

---

## D-003 - Contradições entre documentação e realidade: registrar, não corrigir

**Data:** 2026-08-22 · **Status:** `aceita`

**Contexto.** Divergências encontradas na FASE 1:

| Documentação | Realidade |
|---|---|
| `download_dataset.py` grava `data/<tabela>.parquet` | dados em `data/raw/gitskills/data/<tabela>/*.parquet`, 31 shards |
| notebook le `../data/artifacts.parquet` | caminho inexistente; notebook não roda |
| README: `requirements.txt` "com versões fixas" | nenhuma versão pinada |
| README: `artifacts` ~12 GB | 6,1 GB em disco |
| `Makefile` usa `.venv/bin/` (POSIX) | máquina primária e Windows; sem `.venv` |
| outputs do notebook com `/tmp/ipykernel_*` | executado em Linux/macOS/WSL, não onde os dados estão |

**Decisão.** Documentar todas; **não alterar** os arquivos do pesquisador nesta
rodada.

**Justificativa.** São pistas sobre o histórico do projeto (o dataset foi
re-baixado por outro caminho depois que o notebook rodou), e "consertar" apagaria
essa informação antes de o pesquisador confirmar a intenção.

**Consequências.** Até serem resolvidas, o notebook não é executável na máquina
atual e a reprodutibilidade declarada no README não se sustenta.

**Pendente de aprovação.** Atualizar `download_dataset.py`/notebook para o layout
real, e pinar `requirements.txt`.

---

## D-004 - Definição operacional de "skill de segurança"

**Data:** 2026-08-22 · **Status:** `aceita` (decidida pelo pesquisador, 2026-08-22)

### Decisão

Definição adotada, na formulação do pesquisador:

> **Security Skill:** uma Agent Skill cujo **propósito principal**, ou uma **parte
> substancial de seu comportamento operacional**, e prevenir, detectar, analisar,
> avaliar, explorar, mitigar ou responder a ameaças, vulnerabilidades, violações de
> propriedades de segurança ou controles de acesso em sistemas computacionais.

Com quatro classes ordinais e mutuamente exclusivas:

| Classe | Significado | Exemplo |
|---|---|---|
| `SEC-PRIMARY` | segurança e o objetivo central | vulnerability scanner |
| `SEC-SECONDARY` | capacidade relevante, não o propósito principal | deploy skill que tambem faz security scanning |
| `SEC-MENTION` | apenas menciona / recomenda | "store API keys securely" |
| `NON-SEC` | sem função relevante de segurança | formatter, gerador de UI |

**Security Skill = `SEC-PRIMARY` + `SEC-SECONDARY`.**

**Justificativa do pesquisador.** O critério e "propósito **ou** comportamento
substancial", o que impede classificar como segurança uma skill que apenas diz
"do not expose API keys".

**Alternativa (a) - keyword no corpo - fica rejeitada** como definição: continua
valendo apenas como **triagem** de recall, nunca como classificador.

**Operacionalização.** Regras de decisão R-1..R-7, campos de anotação, âncoras reais
e limites: [[Codebook]] v1.0.

### Consequências verificadas nos dados

- **`code-review` classifica como `SEC-SECONDARY`.** Casos reais inspecionados tem
  seção dedicada de segurança com OWASP Top 10, injection, XSS, CSRF e falhas de
  authz - conteúdo acionável, não mera menção. E o **nome mais frequente** entre as
  skills que declaram segurança no front matter (1.292 conteúdos distintos).
- Logo, **`SEC-SECONDARY` deve dominar** a população de Security Skills. Todo
  resultado precisa reportar PRIMARY e SECONDARY **separadamente**, além do total -
  caso contrário o número de "skills de segurança" e carregado por skills de review
  genérico.
- A fronteira que determina o número final e **SECONDARY vs MENTION**, não
  PRIMARY vs resto. E onde o piloto de anotação deve concentrar esforco.
- Triagem por keyword precisa considerar **onde** o termo casa: `category:
  testing-security` num skill de automação de browser e ruido (regra R-4).

### Limitações conhecidas

- "Substancial" segue sendo julgamento; R-2 (teste de acionabilidade) o
  operacionaliza mas não o elimina.
- A taxonomia classifica **função** da skill. Não mede a **segurança da própria
  skill** (permissões em `allowed-tools`, scripts empacotados) - esse e o eixo
  estrutural de [[01 - Research Question|QP-1/QP-2]], **ortogonal** a esta
  classificação. Não colapsar os dois.
- 1,9M conteúdos não são anotáveis a mao: esta definição produz o padrão-ouro, e a
  aplicação em escala exige classificador validado contra ele.

---

### Histórico

**v0 (`proposta`, 2026-08-22, substituida)** - registro do estado anterior a decisão,
mantido para rastreabilidade.

**Contexto.** O objetivo do README ("skills que se relacionam com segurança") admitia
leituras que diferem por mais de uma ordem de grandeza:

| Critério | n | % dos representantes |
|---|---|---|
| >= 1 keyword no corpo | 994.106 | 52,93% |
| "security"/"vulnerab" no front matter | 66.482 | 4,09% (dos 1.625.701 com FM) |

**Decisão.** Nenhuma tomada. Requer o pesquisador.

**Alternativas.**

- **(a) Ampla - keyword no corpo.** n≈994k. Recall alto, precisão muito baixa:
  `token` (20,69%) e majoritariamente token de LLM; `audit` (16,24%) e revisão
  genérica. Inviável de validar manualmente nessa escala.
- **(b) Estrita - propósito declarado no front matter.** n≈66k. Precisão muito
  maior, mas exclui os 252.280 representantes sem `name`+`description` e ainda
  captura `code-review` (o nome mais frequente do conjunto).
- **(c) Em duas fases - triagem ampla + classificação validada.** Triagem por (a),
  amostra aleatória anotada manualmente, codebook, métricas de precisão/recall, e só
  então aplicação em escala. Mais caro, única que produz número defensável.
- **(d) Mudar o objeto** - em vez de "quais skills são de segurança", perguntar
  "que propriedades de segurança as skills tem" (permissões declaradas em
  `allowed-tools`, scripts empacotados, divergência entre cópias). Não depende de
  classificar dominio; mensurável diretamente; mais alinhado a lacuna do paper.

**Recomendação.** **(c) para a questão de prevalência, e (d) como eixo principal do
TCC.** (d) e defensável com o que o dataset oferece e não depende de uma categoria
subjetiva; (c) sustenta a caracterização descritiva.

**Consequências.** Sem esta decisão, nenhum número de prevalência e apresentável.

---

## D-005 - Ferramental: DuckDB sobre Parquet, via `uv`

**Data:** 2026-08-22 · **Status:** `aceita`

**Contexto.** `artifacts` tem 3,8M linhas / 6,1 GB. O notebook carrega 29 colunas em
pandas (2,4 GB de RAM). A máquina Windows não tem `.venv` nem as dependências do
`requirements.txt`.

**Decisão.** Análises via **DuckDB sobre os Parquet**, executadas com
`uv run --with duckdb`. Amostragem determinística por `ORDER BY hash(file_sha)`.

**Justificativa.** Projection e predicate pushdown tornam agregações sobre 3,8M
linhas questão de segundos, sem carregar nada em memória. `uv` evita mutar o
ambiente. `hash()` da amostra reproduzível sem seed externa.

**Alternativas.** pandas (não escala); Polars lazy (viável, sem vantagem sobre
DuckDB aqui); SQLite original do Zenodo (44 GB, mais lento).

**Consequências.** `requirements.txt` e `Makefile` não refletem o ferramental real -
atualizar quando D-003 for resolvida.

**Nota técnica.** `USING SAMPLE n ROWS` do DuckDB não respeita `n` sob filtro
(pediu 5.000, devolveu 2.455). Não usar.

---

## D-006 — Revisão do esquema de classificação (revisa D-004)

**Data:** 2026-08-22 · **Status:** `aceita` · **Revisa:** [[#D-004]]

**Contexto.** [[#D-004]] fixou quatro classes ordinais. O pesquisador refinou a
especificação em 2026-08-22, acrescentando dimensões que a v1.0 do [[Codebook]]
colapsava numa classe única.

**Decisão.** [[Codebook]] passa a v2.0, com estas mudanças:

1. `NON-SEC` → **`NONE`** (renomeação).
2. Acrescentada a classe **`AMBIGUOUS`** — evidência insuficiente para classificação
   confiável. Nunca forçar uma das outras quatro.
3. `security_focus` e `operational_security` viram **dimensões booleanas
   independentes**, não graus da mesma escala.
4. Acrescentados `operation_level`, `security_functions` (multi-label),
   `security_concerns` (multi-label), `operational_capability` (multi-label),
   `evidence` e `confidence`.

**Justificativa.** Uma classe ordinal única não distinguia *falar sobre* segurança de
*fazer* segurança — a distinção central da pesquisa. Uma skill pode ter propósito de
segurança sem operacionalizá-la (educacional), e outra pode operacionalizar segurança
sem ter propósito de segurança (deploy com scan). A escala única forçava as duas ao
mesmo valor.

**Retrabalho.** **Nenhum.** Nenhuma anotação havia sido feita sob a v1.0 — a revisão
é gratuita. Registrada mesmo assim, por rastreabilidade.

**Consequências.**
- `AMBIGUOUS` fica fora do numerador e do denominador de qualquer prevalência, e sua
  contagem é reportada sempre.
- A estatística de concordância muda: `AMBIGUOUS` está **fora da ordem** e não pode
  entrar num kappa ponderado como quinto degrau. Ver [[Codebook]] §9.
- Dimensões multi-label exigem Krippendorff's α ou Jaccard, não kappa.

**Limitações.** O esquema é mais rico e, portanto, mais caro de anotar e mais sujeito
a discordância. O piloto deve medir o custo por item e a concordância por dimensão —
se alguma dimensão for irreprodutível, é candidata a corte.

---

## D-007 — Eixo B (segurança da própria skill) permanece separado

**Data:** 2026-08-22 · **Status:** `aceita`

**Contexto.** Duas perguntas distintas convivem no projeto:

| Eixo | Pergunta | Exemplo |
|---|---|---|
| **A** | O que a skill faz em segurança? | executar pentest |
| **B** | A própria skill opera de forma segura? | executa comandos remotos sem validação |

**Decisão.** Os eixos permanecem **independentes**. O eixo B **nunca** é usado para
decidir se uma skill pertence ao domínio de segurança.

**Justificativa.** São ortogonais: uma skill fortemente voltada a segurança pode ter
comportamento arriscado, e uma skill `NONE` (um formatter com `allowed-tools:
Bash(*)`) pode ser altamente relevante para segurança. Misturar os eixos tornaria
ambos ininterpretáveis.

**Consequências.** O eixo A responde QI-1/QI-2/QI-3 via [[Codebook]]. O eixo B é
material de [[01 - Research Question|QP-1/QP-2]] e tem instrumentação própria, ainda
não escrita.

---

## D-008 — LLM não é ground truth

**Data:** 2026-08-22 · **Status:** `aceita`

**Decisão.** Saída de LLM **nunca** é verdade de referência. Pode assistir triagem,
sugerir códigos e pré-classificar em escala; não pode fundamentar resultado sem
validação contra padrão-ouro humano.

**Consequências.**
- Todo uso de LLM em resultado registra modelo, versão, prompt e temperatura.
- Precisão/recall/F1 **por classe** contra o gold set, com IC e matriz de confusão.
- A semeadura da [[Security Taxonomy]] v0.1 foi feita por LLM e está marcada como
  **não validada**; serve como ponto de partida do open coding humano.

**Limitação.** Se a anotação humana for feita por um único anotador, o gold set
carrega o viés desse anotador — ameaça a declarar, não a esconder.

---

## D-009 — Escopo de aplicabilidade da QI-3 — EM ABERTO

**Data:** 2026-08-22 · **Status:** `proposta` — **requer aprovação humana**

**Contexto.** A [[QI-3 Coverage Methodology|QI-3]] mede cobertura sobre o
denominador **condicional** (skills às quais a preocupação é aplicável), não sobre
todas as Security Skills. Prompt injection não é esperado numa skill que não
interage com LLM.

**Decisão.** Nenhuma. O escopo de aplicabilidade de cada preocupação é subjetivo e
**determina o denominador de toda a QI-3** — logo, determina toda "lacuna" que a
pesquisa vier a reportar.

**Alternativas.**
- **(a)** Escopo derivado de atributos já anotados na QI-2 (concern, capability,
  artefato-alvo). Herda a validação da QI-2; menos flexível.
- **(b)** Escopo anotado à parte, por leitura dedicada. Mais preciso, custo alto,
  exige validação própria.
- **(c)** Sem condicionamento (denominador = todas as Security Skills).
  **Rejeitada:** produz lacuna artificial.

**Recomendação.** (a), com `uncertain` explícito e reportado à parte.

**Consequências.** Sem esta decisão, nenhum número de cobertura é calculável.

---

## D-010 — Deduplicação por similaridade — ENCERRADA

**Data:** 2026-08-22 · **Status:** `revisada` — **encerrada por [[#D-017]]**
(adotada a alternativa (a), com (b) como análise de robustez)

**Contexto.** [[EXP-002]] mostrou que near-duplicates sobrevivem à deduplicação por
hash: pacotes replicados entre donos com variações mínimas produzem `file_sha`
distintos. Isso afeta diretamente a distribuição de concerns da
[[QI-2 Methodology|QI-2]] — a frequência de uma preocupação pode refletir o que um
pacote popular cobre, não o que a comunidade se preocupa.

**Decisão.** Nenhuma.

**Alternativas.**
- **(a) Manter só dedup por hash**, reportando concentração por repo e por dono
  junto de cada resultado. Simples e transparente; não corrige o problema.
- **(b) Deduplicar por similaridade** (MinHash/SimHash sobre o corpo, ou clustering
  por `name` + estrutura). Corrige melhor; introduz um **limiar arbitrário** que
  precisa de sensitivity analysis, e pode fundir skills genuinamente distintas.
- **(c) Unidade de análise = dono**, não conteúdo. Elimina a replicação por
  construção; perde granularidade e muda a pergunta.

**Recomendação.** (a) agora, com concentração sempre reportada; avaliar (b) como
**robustness check** em [[03 - Methodology|E-10]], não como pipeline principal —
assim o limiar não contamina o resultado central. **Encerrada por [[#D-017]].**

**Consequências.** Se (b) vier a ser adotado depois de análises feitas sob (a), os
resultados precisam ser recomputados, não ajustados.

---

## D-011 — QI-1 como questão central da pesquisa

**Data:** 2026-08-22 · **Status:** `aceita` (decidida pelo pesquisador)

**Decisão.** A questão central passa a ser:

> **QI-1. Qual a prevalência de skills de segurança na população pública de
> Agent Skills?**

Definição vigente de Security Skill: **`SEC-PRIMARY` + `SEC-SECONDARY`**
([[Decision Log#D-004|D-004]], revisada por [[Decision Log#D-006|D-006]];
operacionalização no [[Codebook]] v2.3).

`SEC-PRIMARY` e `SEC-SECONDARY` são **sempre reportados separadamente**, além da
prevalência agregada. Motivo empírico: `code-review` classifica como `SECONDARY` e é
o nome mais frequente do conjunto (1.292 conteúdos distintos) — a agregação sozinha
seria carregada por revisão genérica de código.

**Contexto.** [[QI-2 Methodology|QI-2]] havia sido a candidata preferida. O
pesquisador optou pela QI-1 após [[2026-08-22 - Pauta para o Orientador|alinhamento]].

**Consequências.**
- QI-2 e QI-3 permanecem **documentadas como extensões futuras**, com dependências
  registradas. Nenhum trabalho já feito é descartado: o [[Codebook]], a definição, o
  candidate retrieval de [[EXP-002]] e a [[Security Taxonomy]] v0.1 são reutilizados.
- A QI-1 exige **estimativa com incerteza estatística**, não uma contagem. Isso muda
  o desenho: ver [[QI-1 Methodology]].
- A [[Security Taxonomy]] deixa de ser caminho crítico; a taxonomia de `concerns` não
  é necessária para responder à QI-1.

**Limitações.** A QI-1 é descritiva. Responde "quanto", não "por quê" nem "o quê".
O valor científico depende de a estimativa ser defensável — daí o rigor do desenho
amostral.

---

## D-012 — População-alvo inclui skills de todos os idiomas

**Data:** 2026-08-22 · **Status:** `aceita` (decidida pelo pesquisador)

**Decisão.** A população-alvo da QI-1 é **toda a população pública analisável**, sem
recorte por idioma. Regras vinculantes:

1. **Não descartar** registros por idioma.
2. **Não classificar** conteúdo não inglês automaticamente como `NONE`, `AMBIGUOUS`
   ou irrelevante.
3. **Não usar** candidate retrieval que dependa exclusivamente de keywords inglesas.
4. **Não tratar** inglês como idioma padrão para determinar relevância.
5. **Não interpretar** ausência de termos ingleses como ausência de preocupação de
   segurança.

**Contexto.** [[EXP-002]] observou francês, chinês, russo, coreano, italiano e
japonês numa amostra de 48 casos. A distribuição real de idiomas da população é
**desconhecida** — medi-la é pré-requisito ([[EXP-003]]).

**Consequências.**
- O candidate retrieval de [[EXP-002]] (60 termos, só inglês) fica **inadequado como
  desenho final**. Permanece válido como medição já feita, não como pipeline.
- O gold set precisa representar a diversidade linguística; estratificação por idioma
  ou grupo linguístico quando houver suporte amostral.
- Desempenho do classificador avaliado **por idioma**, não só global. F1 global bom
  não é evidência de desempenho uniforme.
- Queda relevante de desempenho num idioma é **ameaça à validade da estimativa de
  prevalência**, a declarar.

**Correção que esta decisão força.** O [[Codebook]] v2.3 listava "skill em idioma que
o anotador não domina" como caso típico de `AMBIGUOUS`. Isso **contraria a regra 2** e
foi corrigido na v2.1: barreira de idioma do anotador é problema de **processo**
(roteamento para anotador competente ou tradução auxiliar registrada), nunca
justificativa de classe.

**Limitações.** "Tecnicamente possível" tem limite: idiomas com pouquíssimos casos não
terão suporte amostral para avaliação separada. Isso se declara, não se resolve
descartando.

---

## D-013 — Tradução é representação auxiliar, nunca substituição

**Data:** 2026-08-22 · **Status:** `aceita`

**Decisão.** Quando tradução for necessária para apoiar anotação ou classificação:
o **texto original é preservado sempre**; a tradução é representação auxiliar e
**nunca sobrescreve** o dado original; registra-se quando uma decisão classificatória
dependeu de tradução (campo `used_translation`).

**Preferência técnica.** Quando viável, usar modelo capaz de raciocinar **diretamente
sobre o idioma original**, em vez de traduzir o corpus inteiro antecipadamente.

**Justificativa.** Terminologia técnica de segurança sofre perda semântica em
tradução automática — falsos amigos e termos ingleses embutidos em texto de outro
idioma são casos comuns. Traduzir antes de classificar introduz um erro que não é
possível separar do erro do classificador.

**Consequências.** A anotação registra se dependeu de tradução, permitindo medir se
esses casos têm concordância pior.

---

## D-014 — Desenho C: amostragem estratificada com classificador de triagem

**Data:** 2026-08-22 · **Status:** `aceita` (decidida pelo pesquisador) ·
**Branch:** `Q1`

### Decisão

O desenho principal para responder à [[QI-1 Methodology|QI-1]] é a **amostragem
estratificada com classificador de triagem**:

1. um classificador automático/LLM atribui uma **classe prevista** a toda a
   população;
2. essas previsões **não são resultado científico**;
3. servem exclusivamente para construir estratos;
4. os estratos combinam **classe prevista × grupo linguístico**, quando
   metodologicamente apropriado;
5. sorteia-se uma **amostra probabilística dentro de cada estrato**;
6. os itens amostrados são **anotados manualmente**;
7. a prevalência final é estimada por **ponderação estratificada**.

### Estimador

$$\hat{p} = \sum_h \frac{N_h}{N}\,\hat{p}_h$$

com variância

$$\widehat{\mathrm{Var}}(\hat{p}) = \sum_h \left(\frac{N_h}{N}\right)^{2}
\left(1 - \frac{n_h}{N_h}\right)\frac{\hat{p}_h(1-\hat{p}_h)}{n_h - 1}$$

onde `N_h` é o tamanho do estrato `h`, `N` o tamanho da população, `n_h` o tamanho da
amostra no estrato e `p̂_h` a proporção de Security Skills observada **na anotação
humana** daquele estrato.

O fator `(1 − n_h/N_h)` é a **correção para população finita**. Aqui ela é quase
sempre desprezível (`n_h/N_h` da ordem de 10⁻³ ou menor), mas passa a importar em
estratos pequenos com oversampling forte — por exemplo, um estrato raro de idioma
minoritário. Aplicar sempre; o custo é nulo e evita subestimar a precisão onde ela
de fato existe.

### Condições de validade

O desenho só sustenta a estimativa se **todas** valerem:

1. **Cobertura total** — toda unidade elegível pertence a algum estrato.
2. **Nada é descartado por previsão** — nenhuma skill sai da população só porque o
   classificador previu `NONE`. Estratos de baixa prevalência prevista continuam
   sendo amostrados.
3. **Seleção probabilística** dentro de cada estrato, com probabilidade conhecida.
4. **`N_h` conhecido corretamente** para todo estrato usado na estimação.
5. **Partição** — na etapa de estimação, cada unidade pertence a **exatamente um**
   estrato.
6. **O desfecho é a anotação humana**, não a previsão do modelo.

### Papel do classificador

Sob as condições acima, erro do classificador de triagem afeta **principalmente a
eficiência da estratificação** — estratos menos puros exigem amostras maiores para a
mesma precisão — e não constitui, por si só, a estimativa.

> [!warning] Isso não é uma garantia absoluta
> Erro do classificador **pode** afetar a validade se comprometer as condições acima:
> `N_h` calculado errado, unidade em mais de um estrato, estrato inteiro não
> amostrado, ou falha correlacionada com o desfecho **e** com a chance de seleção.
> A frase correta é "afeta principalmente a eficiência", nunca "nunca afeta a
> validade".

### Três números que não podem ser confundidos

| Número | O que é | Pode ser reportado como prevalência? |
|---|---|---|
| Contagem prevista pelo modelo | soma de previsões `PRIMARY`+`SECONDARY` | **não** |
| Proporção observada na amostra humana | `p̂_h` dentro de cada estrato | **não** (é por estrato) |
| Estimativa estratificada | `p̂` com IC | **sim** |

**Não reportar a proporção de previsões `PRIMARY + SECONDARY` como prevalência da
população.** Essa é a confusão que o desenho existe para evitar.

### Alternativas consideradas

- **Desenho A — aleatória simples.** Válido e mais simples, sem classificador. Menos
  eficiente: com prevalência baixa, quase todo o esforço de anotação cai em `NONE`.
- **Desenho B — classificar tudo e contar.** **Rejeitado.** Herda o viés do modelo
  sem quantificá-lo.
- **Desenho multi-estágio** — se classificar 1,88 M for inviável, ver [[#D-015]].

### Consequências

- Exige `N_h` para toda a população: o classificador roda em escala **ou** adota-se o
  desenho multi-estágio de [[#D-015]].
- Exige que idioma seja variável de estratificação confiável — daí a validação
  pendente do detector ([[EXP-003]] limitações).
- Permite **oversampling de estratos raros** (`PRIMARY` previsto, idiomas
  minoritários) sem enviesar o total, porque os pesos `N_h/N` corrigem.

### Limitações

- Estratos por idioma dependem de detecção ainda não validada.
- Ganho de eficiência é desconhecido até o classificador ter desempenho medido.
- Se o classificador for muito ruim, o desenho degenera para algo próximo do
  Desenho A — continua válido, só deixa de compensar o custo.

---

## D-015 — Desenho multi-estágio se a classificação integral for inviável

**Data:** 2026-08-22 · **Status:** `proposta` — decidir só com custo medido

**Contexto.** O Desenho C ([[#D-014]]) pressupõe `N_h` conhecido, o que exige
classificar os 1.877.981 conteúdos. Se isso for financeira ou computacionalmente
proibitivo, é preciso um plano alternativo.

**O erro a evitar.** Classificar uma subamostra de 100 mil e **tratá-la como se fosse
a população** — isso ignora a variância do primeiro estágio e produz IC otimista
demais.

**Alternativa correta — amostragem em dois estágios:**

```text
população completa (N = 1.877.981)
      ↓  estágio 1: amostra probabilística grande (n₁)
amostra-quadro
      ↓  classificador -> estratos
      ↓  estágio 2: subamostra por estrato (n₂ₕ)
anotação humana
```

O estágio 1 **entra na inferência e na variância**. `N_h` passa a ser estimado a
partir da amostra-quadro, não conhecido — e essa incerteza se propaga para
`Var(p̂)`.

**Comparar antes de adotar.** Custo de classificar 1,88 M contra a perda de precisão
do desenho em dois estágios. Um classificador barato sobre a população inteira pode
sair mais em conta que a variância extra.

**Recomendação.** Medir o custo real de classificar a população antes de decidir.
Preferir a classificação integral se for viável.

> [!important] Mantida PENDENTE por decisão do pesquisador (2026-08-22)
> A escolha entre classificação integral e dois estágios **só deve ser feita depois
> que [[EXP-005]] fornecer dados reais** sobre: tempo por item, dificuldade,
> custo, distribuição de casos, necessidade de tradução e frequência de casos
> fronteiriços. Decidir antes disso seria estimar custo sem medi-lo.

---

## D-016 — Escopo de GRC (governança, risco e conformidade)

**Data:** 2026-08-22 · **Status:** `aceita` (aprovada pelo pesquisador)
· **Branch:** `Q1`

**Contexto.** [[EXP-002]] encontrou `draft-vendor-onboarding-questionnaire` —
questionário de risco de fornecedor, com conformidade em saúde, áreas de controle e
exigência de evidência. É segurança como **governança**, não como técnica.

A definição vigente ([[#D-004]]) fala em *"ameaças, vulnerabilidades, violações de
propriedades de segurança ou controles de acesso em **sistemas computacionais**"*.
Risco de fornecedor é organizacional. A definição não resolve o caso sozinha.

**Por que importa.** GRC é um domínio grande. Incluir tudo pode inflar a prevalência
com skills de compliance contratual que ninguém chamaria de segurança; excluir tudo
descarta auditoria de IAM e gestão de risco técnico, que claramente são.

### Critério aprovado: o objeto da atividade

> GRC entra como Security Skill **apenas quando a atividade incide sobre
> propriedades de segurança de sistemas computacionais**. Governança puramente
> organizacional, contratual ou processual fica fora.

O teste é **sobre o que a skill atua**, não que vocabulário usa.

**Positivos (dentro):**
- auditoria de IAM, revisão de políticas de acesso, verificação de least privilege;
- mapeamento de controles técnicos contra um framework (CIS Benchmarks, hardening);
- avaliação de risco de dependência ou de componente de software;
- verificação de conformidade que **inspeciona configuração ou código**.

**Negativos (fora):**
- questionário de onboarding de fornecedor focado em contrato, seguro, sanções,
  continuidade de negócio organizacional;
- conformidade regulatória sem objeto computacional (retenção documental, LGPD/HIPAA
  em nível de política, sem inspecionar sistema);
- gestão de risco corporativo genérica;
- política de segurança da informação como documento, sem atividade sobre sistema.

**Casos fronteiriços — anotar e adjudicar, não decidir por regra:**
- questionário de fornecedor que inclui perguntas técnicas específicas (criptografia
  em repouso, MFA): **misto**; classificar pela parte dominante, `confidence: low`;
- checklist de conformidade que às vezes inspeciona configuração;
- threat modeling organizacional sem sistema concreto;
- skills de privacidade — LGPD/GDPR como propriedade de sistema (minimização, dados
  pessoais em log) entram; como processo jurídico, não.

### Impacto nas classes

| Situação | Classe |
|---|---|
| GRC técnico com procedimento acionável | `PRIMARY` ou `SECONDARY` conforme R-1/R-3 |
| GRC organizacional puro | `NONE` — não é MENTION, porque não é sequer preocupação de segurança computacional |
| Misto, parte técnica acionável | `SECONDARY`, `confidence: low` |
| Misto, parte técnica só mencionada | `MENTION` |
| Indeterminável | `AMBIGUOUS` |

Nota: GRC organizacional puro vai para `NONE`, não `MENTION`. `MENTION` pressupõe
preocupação de segurança computacional incidental; conformidade contratual não é
disso que trata.

### Alternativas

- **(a) Incluir todo GRC.** Simples e reprodutível; infla a prevalência com
  compliance não técnico e enfraquece o construto.
- **(b) Excluir todo GRC.** Também simples; descarta auditoria de IAM e gestão de
  risco técnico, que são segurança por qualquer definição razoável.
- **(c) Critério do objeto** (proposto). Alinhado à definição já aceita, ao custo de
  exigir julgamento na fronteira.

**Aprovada: (c).** Os casos fronteiriços são medidos no piloto. Se a concordância
nesses casos for ruim, reconsiderar (b) numa revisão datada — que é defensável desde
que declarada.

A lista de objetos que qualificam, na formulação do pesquisador: sistemas
computacionais, código, aplicação, infraestrutura, configuração, IAM, identidade,
dependências, agentes, modelos e artefatos computacionais equivalentes.

**Consequências.** Acrescenta uma dimensão de julgamento ao codebook. O piloto
([[03 - Methodology|E-5]]) deve incluir casos de GRC deliberadamente e reportar a
concordância **nesse subconjunto separadamente**.

**Limitações.** "Incide sobre sistemas computacionais" continua sendo julgamento.
O critério reduz, não elimina, a ambiguidade.

---

## D-017 — Near-duplicates ficam como análise de robustez

**Data:** 2026-08-22 · **Status:** `aceita` (decidida pelo pesquisador) ·
**Branch:** `Q1` · **Substitui:** [[#D-010]]

**Decisão.** A **deduplicação exata por `file_sha` permanece o desenho principal**.
Deduplicação semântica **não** entra no pipeline principal agora.

Near-duplicates viram **análise posterior de robustez**, respondendo:

> A estimativa de prevalência muda materialmente quando conteúdos quase idênticos
> são agrupados?

**Justificativa.** Deduplicação semântica exige um limiar arbitrário que
contaminaria a estimativa principal. Como robustez, o limiar é explorado por
sensitivity analysis sem contaminar o resultado central.

**Consequência.** Toda estimativa continua obrigada a reportar concentração por
repositório **e por dono** ([[#D-001]] ressalva, [[EXP-002]]). Se a análise de
robustez mostrar mudança material, isso é achado a reportar, não motivo para
substituir o resultado principal em silêncio.

**Encerra [[#D-010]]**, que ficava em aberto entre as alternativas (a), (b) e (c);
adotada a (a) com (b) como robustez.

---

## D-018 — E-4 depois de E-6 (reordenação definitiva)

**Data:** 2026-08-22 · **Status:** `aceita` (aprovada pelo pesquisador)
· **Branch:** `Q1`

**Decisão.** O candidate retrieval (**E-4**) ocorre **depois** do gold set (**E-6**).
Deixa de ser provisória: os documentos não devem mais apresentá-la como proposta.

**Justificativa.**
- Candidate retrieval **não determina elegibilidade** — nenhuma skill é descartada
  por não ser recuperada.
- Retrieval é apenas sinal, ou mecanismo de formação de estratos.
- A escolha entre retrieval lexical e semântico deve ser decidida por **recall contra
  um gold set humano independente**.
- Escolher o retrieval definitivo **antes** do gold set cria risco de circularidade:
  o instrumento de recuperação passaria a definir aquilo contra o que ele próprio
  seria avaliado.

**Consequências.** Ordem vigente: `E-5 → E-6 → E-4 → E-7 → E-8 → E-9 → E-10`.
O retrieval inglês de [[EXP-002]] permanece como **um sinal entre outros**, nunca
como filtro de população.

---

## D-019 — Anotador único não bloqueia E-5

**Data:** 2026-08-22 · **Status:** `aceita` (aprovada pelo pesquisador)
· **Branch:** `Q1`

**Decisão.** A ausência de um segundo anotador **não bloqueia** o piloto E-5.

- Se um segundo humano estiver disponível depois, define-se **previamente** uma
  subamostra de dupla anotação — nunca escolhida após ver os resultados.
- Se não houver, assume-se explicitamente a limitação de **single annotator** como
  ameaça à validade, declarada no texto final.

> [!danger] Restrição inegociável
> **LLM, ou consenso entre agentes, não pode ser usado como segundo anotador humano
> nem como ground truth.** Concordância entre modelos não substitui confiabilidade
> interavaliadores. Ver [[#D-008]].

**Consequências.** Sem segundo anotador, não há kappa interavaliadores; a
confiabilidade do instrumento passa a depender de consistência intra-anotador e da
qualidade das âncoras. Isso enfraquece a validação e precisa ser dito com todas as
letras — não compensado com números de concordância entre modelos.

---

## D-020 — Sinal preliminar de segurança substitui "classe prevista" no piloto

**Data:** 2026-08-22 · **Status:** `aceita` · **Branch:** `Q1`

**Contexto.** O [[Decision Log#D-014|Desenho C]] estratifica por *classe prevista ×
grupo linguístico*. Mas **não existe classificador validado**, então "classe
prevista" ainda não é uma quantidade definida.

**Decisão.** Enquanto não houver classificador validado, o eixo de estratificação do
piloto é o **sinal preliminar de segurança × grupo linguístico**.

O sinal é calculado **apenas** com informação já existente — léxico estrito de
[[EXP-002]], `name`, `description`, `domain:`/`category:`, `has_scripts` — e é
definido por um `CASE` ordenado em quatro níveis mutuamente exclusivos
(T3 forte, T2 médio, T1 fraco, T0 nulo), documentado em
`scripts/build_pilot_sample.py` e em [[EXP-005]].

**Restrições.**
1. O sinal serve **apenas para diversificar o piloto**.
2. **Não é rótulo** e **não é ground truth**.
3. **Não pode aparecer depois como evidência de validade do classificador** — usá-lo
   assim seria avaliar um instrumento contra outro instrumento, não contra
   julgamento humano.
4. Os tamanhos de tier medidos na população são **documentação**, não os `N_h` do
   estimador. Os `N_h` do Desenho C virão da classificação validada em E-8.

**Consequências.** Quando o classificador validado existir, os estratos serão
recalculados a partir dele. O sinal preliminar não é reaproveitado como estrato
definitivo.

---

## D-021 — Cegamento da anotação (achado C-3 da auditoria adversarial)

**Data:** 2026-08-22 · **Status:** `aceita` · **Branch:** `Q1`

**Contexto.** A primeira versão do formulário e do reading pack de [[EXP-005]]
exibia ao anotador, **antes do texto da skill**, o tier do sinal preliminar, a
densidade de keyword, as flags de GRC e code-review, o grupo linguístico e o motivo
da seleção (inclusive `"dirigido fronteira SECONDARY/MENTION"`).

**Problema.** O sinal de triagem — cuja premissa declarada em [[#D-020]] é "não é
rótulo, não é ground truth" — era entregue como **prior explícito** a quem produz o
rótulo. Sob o Desenho C o desfecho precisa ser anotação humana **independente do
estrato**. Se o sinal ancora o anotador, `p̂_h` sobe nos estratos altos e desce nos
baixos, e o viés fica **correlacionado com a probabilidade de seleção** — a única
falha que [[#D-014]] admite ser capaz de destruir a validade. Como o oversampling é
forte em T3, o efeito seria amplificado pelos pesos, não cancelado.

**Decisão.** A anotação é **cega ao sinal de triagem**:

1. `results/_arquivo/EXP-005_annotation_form.csv` traz apenas `case_id`, `name`, `body_chars`
   e os campos humanos vazios.
2. `results/_arquivo/EXP-005_reading_pack.md` traz apenas `case_id`, `name`, `description`,
   tamanho e o texto.
3. Tier, densidade, flags, grupo linguístico e motivo da seleção ficam em
   `results/_arquivo/EXP-005_strata_key.csv`, unido por `case_id` **somente depois** de a
   anotação estar fechada.
4. Registrada como **regra R-11** no [[Codebook]] v2.3 — não apenas no script.

**Apoio na literatura.** Herbold et al. (EMSE, aceito) é o único protocolo em MSR
que encontramos que (i) mitiga ancoragem por pré-rótulo instruindo ceticismo
explícito e (ii) **testa empiricamente** se a mitigação funcionou. Cegar é mais
forte que instruir ceticismo, e mais barato.

**Consequências.** O anotador não pode usar o tier como atalho — anotar fica mais
lento, e é esse o ponto. O tempo por item medido no piloto passa a ser o tempo real
de leitura, não o de confirmar um palpite.

**Limitação.** O cegamento não é perfeito: `name` e `description` continuam
visíveis, e para muitas skills eles já revelam o domínio. Isso é inevitável — são
parte do artefato a ser julgado.

---

## D-022 — Critério de elegibilidade da população — FECHADA por D-028

**Data:** 2026-08-22 · **Status:** `revisada` — **fechada em 2026-09-03 por
[[#D-028]]** · **Branch:** `Q1` · **Origem:** achado C-5 da auditoria adversarial

> [!important] Resolução (2026-09-03)
> "Elegível" passa a ser definido em [[#D-028]]: `dedup_primary = 1`,
> `content IS NOT NULL`, 100% em inglês ([[#D-025]]), **e**
> `length(description) + body_chars >= 200`. Os casos de symlink e conteúdo
> mínimo que motivaram esta entrada são capturados pelo corte de 200
> caracteres (3.447 ponteiros de symlink entre os excluídos). O texto abaixo
> permanece por rastreabilidade.

**Contexto.** A QI-1 pergunta pela prevalência na "população pública de Agent
Skills". O único filtro operacional em todos os scripts é
`dedup_primary = 1 AND content IS NOT NULL` — n = 1.877.981.

Mas [[GitSkills]] documenta que o frame **contém não-skills**: a descoberta foi por
nome de arquivo e inclui falsos positivos deliberados, arquivos anteriores ao
formato, 7.309 conteúdos com menos de 80 caracteres e 5.363 que parecem alvos de
symlink (`../.claude/SKILL.md`).

E [[#D-014]] condição 1 exige que "toda unidade **elegível** pertença a algum
estrato" — mas **"elegível" nunca foi definido**.

**Por que importa.** O denominador é o número pelo qual a QI-1 divide. Cada stub de
42 caracteres no frame é um `NONE` garantido que **deprime a prevalência**. É o mesmo
tipo de premissa que invalidou o notebook original ([[#D-002]]: keywords rodando
sobre alvos de symlink), voltando pela porta do denominador. Pelo menos ~12,7 mil
unidades (0,7%) são inelegíveis por inspeção óbvia; quantas mais existem é
desconhecido porque ninguém mediu.

**Alternativas.**

- **(a) Frame amplo (status quo).** `dedup_primary = 1 AND content IS NOT NULL`.
  Simples e sem julgamento; inclui não-skills e subestima a prevalência.
- **(b) Frame com piso de tamanho.** Acrescentar `body_chars >= X` e excluir
  symlink-like. Requer justificar `X` — qualquer valor é arbitrário sem análise de
  sensibilidade.
- **(c) Frame por conformidade com a spec.** Exigir front matter válido. Exclui
  252.280 representantes (13,4%) e muda a pergunta: passaria a medir prevalência
  entre skills bem formadas.
- **(d) Frame amplo + reporte estratificado.** Manter (a), mas reportar a prevalência
  também **excluindo** os inelegíveis óbvios, como análise de sensibilidade.

**Recomendação:** **(d)**, com o critério de inelegibilidade escrito antes do piloto
e testado nele. Preserva a comparabilidade com o dataset publicado e torna o efeito
do frame visível em vez de embutido.

**Ação no piloto.** Incluir deliberadamente 3–5 casos de fronteira (stubs curtos,
symlink-like, sem front matter) para que o anotador julgue **se são agent skills**,
não apenas que classe recebem. Acrescentar ao formulário o campo `is_agent_skill`.

**Consequência de não decidir.** Enquanto D-022 estiver aberta, o denominador da
QI-1 permanece indefinido e nenhuma estimativa é reportável.

---

## D-023 — Classificador definitivo da iteração v1 (EXP-012)

**Data:** 2026-08-23 · **Status:** `aceita` · **Branch:** `Q1`

**Contexto.** [[Decision Log#D-022|D-022]] segue em aberto e o gold set humano
de [[03 - Methodology|E-6]] ainda não existe. Para provar o pipeline
ponta-a-ponta desta primeira semana exploratória, o pesquisador decidiu
congelar `EXP-005_annotation_form_filled_updated.csv` (n=50, assistido por
LLM) como **golden set operacional da iteração v1** — não é gold standard
humano definitivo, tem as limitações declaradas em [[EXP-005]] (amostra
deliberadamente enviesada, anotador único/LLM). Commit de congelamento:
`a90ce044bc07e042467de74a844407e9e5717267`.

Excluindo `AMBIGUOUS` (n=1, suporte insuficiente para qualquer fold),
n=49: `NONE` 26 · `PRIMARY` 11 · `SECONDARY` 7 · `MENTION` 5. Binário:
`SECURITY` 18 · `NON_SECURITY` 31.

**Vazamento evitado.** O frame de treino (`scripts/build_training_frame.py`)
usa **apenas o texto bruto** (`content`) recuperado por `file_sha` — nenhum
campo de `EXP-005_strata_key.csv` (tier, `kw_density`, `domain_decl`,
`fm_signal`, flags de GRC/code-review, sinais de idioma, `selection_reason`)
entra como feature; o script aborta se algum aparecer. Três repositórios do
golden set contêm mais de um caso (`bpcakes/jig-skills`,
`pjt222/agent-almanac`, `GeorgeDoors888/GB-Power-Market-JJ`) — a validação
cruzada agrupa por `repo_full_name` (`StratifiedGroupKFold`) para não deixar
conteúdo do mesmo repositório em treino e validação simultaneamente.

### Protocolo de validação

`StratifiedGroupKFold(n_splits=5, shuffle=True)` repetido 5× com seeds
distintas (20260823–20260827), agrupado por `repo_full_name`. Cada repeat
produz uma predição out-of-fold para as 49 linhas; métricas calculadas por
repeat e agregadas (média ± desvio padrão) entre os 5 repeats. `AMBIGUOUS`
fora de qualquer fold, como o [[Codebook]] exige.

### Modelos comparados

| Modelo | Representação | Classificador |
|---|---|---|
| A | TF-IDF (char n-grams 2–5, robusto a CJK sem segmentação por espaço) | Logistic Regression |
| B | idem A | Linear SVM |
| C | Sentence embeddings multilíngues (`paraphrase-multilingual-MiniLM-L12-v2`) | Logistic Regression |

### Métricas — tarefa binária (`SECURITY` vs `NON_SECURITY`)

| Modelo | Precision | Recall | F1 | Especificidade | Bal.Acc | ROC-AUC | PR-AUC | F1 en | F1 não-en |
|---|---|---|---|---|---|---|---|---|---|
| A tfidf+logreg | 0,438 | 0,100 | 0,158±0,090 | 0,923 | 0,511 | 0,610 | 0,481 | 0,000 | 0,254 |
| B tfidf+linearsvc | 0,515 | 0,133 | 0,206±0,112 | 0,929 | 0,531 | 0,648 | 0,508 | 0,000 | 0,327 |
| **C embed+logreg** | **0,710** | **0,622** | **0,663±0,046** | 0,852 | **0,737** | **0,830** | **0,798** | **0,653** | **0,675** |

### Métricas — tarefa multiclasse (4 classes, excl. `AMBIGUOUS`)

| Modelo | macro-F1 | weighted-F1 | Bal.Acc | F1 `SECONDARY` | F1 `PRIMARY` | F1 `MENTION` | F1 `NONE` |
|---|---|---|---|---|---|---|---|
| A tfidf+logreg | 0,209±0,007 | 0,399 | 0,257 | **0,000** | 0,145 | 0,000 | 0,691 |
| B tfidf+linearsvc | 0,208±0,018 | 0,401 | 0,264 | **0,000** | 0,133 | 0,000 | 0,699 |
| **C embed+logreg** | **0,467±0,014** | **0,643** | **0,479** | 0,134 | 0,819 | 0,107 | 0,808 |

**Achado que decidiu contra A/B por si só:** nos dois modelos TF-IDF, `SECONDARY`
e `MENTION` têm F1 = 0,000 em **todos** os 5 repeats — o modelo nunca prevê
essas classes na validação cruzada (confusão agregada em
`results/_arquivo/EXP-012_confusion_matrix.csv` confirma zero previsões de
`SECONDARY`/`MENTION` nas duas direções). Isso é fatal justamente para a
fronteira que mais importa ([[Decision Log#D-011|D-011]]): a confusão
`SECONDARY` × `MENTION` é a que altera a prevalência estimada.

### Decisão — dois papéis distintos

**Melhor desempenho em validação cruzada: `C_embed_logreg`.** Vence em todos
os critérios 1–4 do enunciado (desempenho binário, macro-F1, recall de
`SECURITY`, desempenho em `SECONDARY`) por margem larga, inclusive no recorte
por idioma.

**Modelo implantado na classificação da população: `B_tfidf_linearsvc`.**
Medição empírica de custo computacional: o encoder de embeddings processou
1.500–3.000 documentos reais a **17–19 documentos/segundo em CPU** (sem GPU
disponível nesta máquina — `torch.cuda.is_available() == False`; variar
`batch_size`, threads (10→16) e truncar o texto antes de tokenizar não
mudou o throughput de forma relevante). Projeção para 1.877.981 conteúdos:
**≈ 27–30 horas**. O TF-IDF processou a população inteira
(`scripts/classify_population.py`) a **≈ 1.972 itens/segundo**, concluindo
em minutos.

Isso é exatamente o conflito que os critérios 6 (custo computacional) e 7
(escalabilidade) do enunciado antecipam: o candidato com melhor desempenho
não é viável de operacionalizar nesta iteração. A decisão foi **priorizar a
prova de conceito ponta-a-ponta reproduzível** (congelamento → treino →
validação → classificação da população inteira) em vez de rodar o melhor
modelo por trinta horas sem supervisão nesta primeira semana.

**Justificativa para não escolher B "de verdade":** B tem desempenho fraco e
documentado — não é apresentado como classificador válido, e sua saída sobre
a população é rotulada explicitamente como "resultado preliminar do
classificador", nunca como prevalência (ver
`results/_arquivo/EXP-012_population_summary.json`, campo `caveat`).

**Calibração.** `LinearSVC` não expõe `predict_proba`; `decision_function`
nunca é tratada como probabilidade. O modelo implantado (multiclasse e
binário) foi re-ajustado no golden set completo com
`CalibratedClassifierCV(method="sigmoid", cv=3)` antes de servir de base
para a `confidence` reportada na classificação da população.

### Alternativas consideradas

- **(a) Implantar C mesmo assim, aceitando ~27–30h de execução.** Rejeitada
  nesta iteração — inviável dentro do escopo de uma prova de conceito de
  uma semana, sem infraestrutura de GPU.
- **(b) Implantar B, aceitando o desempenho fraco, com o resultado
  rotulado como preliminar.** **Adotada.**
- **(c) Não classificar a população agora; esperar GPU ou um encoder mais
  leve.** Rejeitada — o pesquisador pediu explicitamente a execução
  ponta-a-ponta nesta iteração (regra 15 do enunciado desta tarefa: "não
  deixe a natureza exploratória... impedir a execução end-to-end").
- **(d) Reduzir a dimensão do embedding/usar um modelo menor para viabilizar
  C em escala.** Não testada nesta iteração — candidata para v2.

### Consequências

- `results/_arquivo/EXP-012_population_classification.parquet` e
  `results/_arquivo/EXP-012_population_summary.json` são saídas do modelo B, **não**
  do modelo C. Qualquer leitura desses números precisa citar essa decisão.
- Os artefatos do candidato C (`models/security_classifier_v1_*_cv_best_candidate.joblib`)
  ficam preservados para quando (i) um gold set maior (E-6) justificar
  retreinar, e (ii) houver GPU ou um encoder mais leve para viabilizar
  escala.
- `SECONDARY` previsto pelo modelo implantado é quase inexistente na
  população — qualquer estrato construído a partir dele para o Desenho C
  ([[Decision Log#D-014]]) teria eficiência degradada para essa classe.
  Isso **não é** os `N_h` definitivos do estimador (que exigem classificador
  validado contra gold set humano, [[Decision Log#D-020]] e
  [[Decision Log#D-014]] condição 6) — apenas uma prova de que o pipeline
  roda ponta a ponta.

### Estimativa inicial de tempo incorreta — causa e correção

A primeira estimativa de runtime da classificação da população (15–16 min)
estava **errada por mais de duas ordens de grandeza**. Registrado aqui
porque é, em si, uma instância do mesmo erro metodológico de D-002: medir
sobre uma amostra não representativa e generalizar.

**O que aconteceu.** O primeiro benchmark de throughput usou
`SELECT content FROM ... ORDER BY hash(file_sha) LIMIT n` — correto como
padrão de amostragem — mas um segundo benchmark de checagem rápida usou
`LIMIT n` **sem** `ORDER BY`, o que no Parquet devolve as primeiras linhas
em ordem física do arquivo. Essas linhas iniciais têm em média **138
caracteres** — a mesma faixa de stub/symlink que invalidou o notebook
original ([[#D-002]]). O comprimento médio real da população, medido por
amostra aleatória, é **7.247 caracteres** (máx. observado: 276.779). A
uma taxa de ~1.972 itens/s (medida sobre o texto curto), a extrapolação
para 1.877.981 itens dava ~16 min; a taxa real, medida depois sobre texto
representativo, era de **~56,5 itens/s** (isolando o custo: vetorização
TF-IDF ~40s/20.000 linhas, classificação calibrada ~0,2s/20.000 linhas —
o gargalo é a vetorização por n-gramas de caractere sobre texto longo, não
a classificação). Extrapolação correta: **~9,3 horas**.

**Consequência operacional.** A primeira tentativa de rodar a população
inteira foi autorizada para rodar em segundo plano até o fim, mas foi
**encerrada pelo ambiente de execução após ~2h11min**, sem aviso de erro,
sem concluir e sem escrever `EXP-012_population_summary.json`. O arquivo
parquet parcial ficou sem rodapé válido (`ArrowInvalid: Parquet magic
bytes not found in footer`) — descartado.

**Correção aplicada, sem retreinar o modelo:**
1. os dois pipelines (multiclasse, binário) foram ajustados no **mesmo
   corpus com os mesmos hiperparâmetros do vetorizador** — `vocabulary_` e
   `idf_` são **idênticos** (verificado por igualdade exata, não suposição)
   — logo a vetorização roda **uma vez** por lote e é reaproveitada pelos
   dois classificadores, em vez de duas vezes;
2. o texto é truncado a **1.500 caracteres** antes de vetorizar — reduz o
   custo por documento linearmente, sem alterar o modelo já treinado;
3. uma tentativa de paralelizar com `ProcessPoolExecutor` falhou nesta
   máquina (Windows + `uv`: erro ao importar `scipy`/`scikit-learn` nos
   processos-filho via spawn) — não investigada a fundo; o ganho das duas
   otimizações seriais acima já foi considerado suficiente.

**Resultado da correção, medido:** ~1.364 itens/s num teste de 100 mil
linhas: **449 itens/s reais** na execução completa (throughput cai à
medida que o processo avança, porque o início do arquivo tem conteúdo
mais curto que a média — o mesmo viés de ordenação física, na direção
oposta). Tempo total real: **4.184,5 s (≈ 69,7 min)** para os 1.877.981
conteúdos. Script: `scripts/classify_population.py` (docstring documenta a
v1 malsucedida e a v2 otimizada).

### Resultado da classificação da população (execução concluída)

`results/_arquivo/EXP-012_population_summary.json`, gerado em 2026-08-24T00:09:54Z:

| Classe prevista | n | % |
|---|---|---|
| `NONE` | 1.815.753 | 96,686 |
| `PRIMARY` | 58.066 | 3,092 |
| `MENTION` | 3.154 | 0,168 |
| `SECONDARY` | 1.008 | 0,054 |

`SECURITY` previsto (`PRIMARY`+`SECONDARY`): **30.281 (1,612%)**.
`SECONDARY` continua quase ausente em escala (0,054%), consistente com o
achado da CV — o modelo implantado essencialmente não reconhece essa
classe. `language_group` (proxy Unicode, não o detector validado):
L1 (ASCII/latino) 1.436.055 · L2 (zh) 159.525 · L4 (latino acentuado)
195.355 · L3 (ja) 38.550 · L3 (ko) 27.857 · L5 (cirílico) 13.889 · L5
(outro script) 6.750. Confiança: média 0,551, mediana 0,561, 24,09% abaixo
de 0,5. Amostra de 450 casos de baixa confiança/fronteira salva em
`results/_arquivo/EXP-012_uncertain_cases_sample.csv` (metadados apenas).

Todos os números acima carregam o `caveat` gravado no próprio JSON:
resultado preliminar do classificador v1, não estimativa de prevalência;
modelo com desempenho fraco em CV; texto truncado a 1.500 caracteres nesta
execução.

### Limitações

- n=49 é pequeno demais para qualquer conclusão sobre qual algoritmo é
  "melhor" de forma estável — `f1_std` do modelo C na tarefa binária
  (0,046) é a mais estável das três, mas ainda assim sobre 5 repeats de um
  golden set de 49 casos.
- O `language_group` usado no recorte multilíngue da CV vem de
  `human_language` **anotado**, não do detector; já na classificação da
  população (`scripts/classify_population.py`) o `language_group` é um
  **proxy barato por script Unicode** (SQL, população inteira), não o
  detector validado de [[EXP-003]]/[[EXP-004]] — rodar aquele detector a
  1,88M de documentos está fora do escopo desta iteração.
- Retreinar no golden set inteiro (sem held-out) para o modelo final produz
  `accuracy = 1.0` de forma trivial (memorização com features de alta
  dimensão) — não é evidência de desempenho; a estimativa de generalização
  válida é a validação cruzada acima, não o ajuste final.
- Este classificador **não deve ser citado como resultado da QI-1**. É
  prova de conceito de engenharia; a resposta à QI-1 exige gold set humano
  maior (E-6) e classificador validado contra ele (E-7), por [[Decision Log#D-014|D-014]].

---

## D-024 — Execução sequencial de QI-2 e QI-3, condicionada à validação do classificador de QI-1

**Data:** 2026-08-27 · **Status:** `aceita` (decidida pelo pesquisador) · **Branch:** `Q1`

**Contexto.** [[#D-011]] fixou QI-1 como questão central e manteve QI-2 e QI-3
como "extensões futuras", sem formalizar se, quando ou em que ordem seriam
executadas dentro deste projeto. [[01 - Research Question]] já registrava
informalmente que QI-2 depende da classificação validada de QI-1 e que QI-3
depende de QI-2 estabilizada, mas essa dependência nunca tinha virado decisão
registrada nem definia um critério de transição entre etapas.

**Decisão.** A execução de QI-2 e QI-3 passa a ser parte do plano deste
projeto, formalmente sequenciada:

> **QI-1 → validação satisfatória do classificador de triagem (E-7) → QI-2 → QI-3**

1. QI-1 continua sendo a questão do caminho crítico imediato, com o desenho já
   estabelecido (Desenho C, [[#D-014]]) — esta decisão **não altera nada** do
   método já definido para QI-1.
2. QI-2 e QI-3 só começam **depois** de o classificador de triagem treinado
   para QI-1 passar pela validação metodológica prevista em E-7
   (precisão/recall/F1 por classe e por idioma, matriz de confusão completa,
   contra o gold set humano de E-6) com desempenho considerado
   **satisfatório**.
3. O conjunto de skills analisado por QI-2 é a população classificada como
   `SEC-PRIMARY`/`SEC-SECONDARY` pelo classificador **validado**, produzida em
   E-8 — não o pool de candidate retrieval por palavra-chave usado como
   exploração inicial ([[EXP-002]]) nem qualquer classificação não validada
   (como a prova de conceito de [[#D-023]]).
4. QI-3 só começa depois de a taxonomia empírica de QI-2 estar razoavelmente
   estabilizada, como já previsto em [[QI-2 Methodology]] e
   [[QI-3 Coverage Methodology]] — esta decisão não muda esse requisito, só o
   integra a uma cadeia de decisão única e explícita em vez de duas
   dependências registradas separadamente.

**Papel do gate.** A validação do classificador funciona como **gate
metodológico**: se o desempenho medido em E-7 não for suficiente para
sustentar as análises seguintes, o método deve ser revisado **antes** de
avançar para QI-2 — não se prossegue com um conjunto de skills identificado
por um classificador conhecidamente fraco.

> [!warning] Critério de "satisfatório" ainda não definido — decisão pendente
> Este projeto ainda não define numericamente o que conta como validação
> satisfatória (ex.: F1 mínimo por classe, recall mínimo para `SECONDARY`,
> desempenho mínimo por idioma). E-7 já exige que essas métricas sejam
> medidas e reportadas com IC ([[03 - Methodology]]), mas não fixa um limiar
> de aprovação. Fixar esse limiar **antes** de ver o resultado de E-7 é
> trabalho pendente, não parte desta decisão — inventar um número aqui
> repetiria o erro que [[#D-014]] existe para evitar (ajustar critério depois
> de ver o dado). Enquanto não for definido, a decisão de prosseguir ou não
> para QI-2 é humana e caso a caso.

**Justificativa.**
- Evita circularidade: QI-2 constrói taxonomia emergente a partir dos dados
  (regra inegociável de [[QI-2 Methodology]] — nunca usar OWASP/MITRE para
  semear a taxonomia), mas a *base de skills* sobre a qual essa taxonomia é
  construída precisa ter confiabilidade conhecida; usar a saída de um
  classificador não validado (como em [[#D-023]]) contaminaria QI-2 com o
  mesmo viés não quantificado que [[#D-014]] rejeita para QI-1 (Desenho B).
- Formaliza uma dependência que já estava implícita em
  [[01 - Research Question]] e [[QI-2 Methodology]] §1, tornando-a
  rastreável como decisão datada, em vez de apenas uma frase solta em nota
  de metodologia.

**Alternativas consideradas.**
- **(a) Manter QI-2/QI-3 como extensões sem ordem nem gate definidos**
  (status anterior a esta decisão). Rejeitada: deixava em aberto se QI-2
  usaria a classificação validada ou uma classificação preliminar — risco já
  materializado uma vez neste projeto, quando a prova de conceito de
  [[#D-023]] chegou a produzir números de população antes de qualquer
  validação.
- **(b) Executar QI-2 em paralelo a QI-1**, usando o pool de candidate
  retrieval em vez da classificação validada. Rejeitada: reintroduziria o
  problema que [[#D-018]] já resolveu para o retrieval de QI-1 — decidir o
  conjunto analisado antes de ele ter sido validado contra padrão-ouro.
- **(c) Sequência formal QI-1 → validação → QI-2 → QI-3.** **Adotada.**

**Consequências.**
- [[QI-2 Methodology]] e [[QI-3 Coverage Methodology]] permanecem válidas
  como desenho metodológico; esta decisão acrescenta o gate e a origem do
  conjunto analisado, sem reescrever o que já estava certo nelas.
- Resultados já produzidos (candidate retrieval de [[EXP-002]], taxonomia
  semeada por LLM em [[Security Taxonomy]] v0.1) continuam registrados como
  histórico exploratório — não são o conjunto de entrada de QI-2 sob esta
  decisão, e não foram alterados por ela.
- Nenhum cronograma é fixado aqui: se o gate de E-7 não for satisfeito dentro
  do prazo do trabalho, QI-2 e QI-3 permanecem como trabalho futuro, não como
  entrega concluída — ver [[03 - Methodology]] e `ROTEIRO.md`.

**Limitações.**
- O critério numérico de "validação satisfatória" é, ele mesmo, uma decisão
  pendente (ver aviso acima).
- QI-3 herda qualquer viés não corrigido de QI-2 (deriva do codebook,
  dependência entre observações, concentração por repositório/dono) — já
  documentado em [[QI-2 Methodology]] §7.

---

## D-025 — População-alvo restrita a skills em inglês (revisa D-012)

**Data:** 2026-09-03 · **Status:** `aceita` (decidida em reunião com o
orientador) · **Branch:** `Q1` · **Revisa:** [[#D-012]]

**Contexto.** [[#D-012]] fixava a população-alvo da QI-1 como toda a
população pública analisável, sem recorte por idioma, com cinco regras
vinculantes contra descartar registros por idioma, classificar conteúdo não
inglês automaticamente como `NONE`/`AMBIGUOUS`, ou tratar inglês como padrão
de relevância. Essa decisão orientou [[Multilingual Strategy]], os estratos
L1–L5 de [[EXP-003]]/[[EXP-004]], e a composição deliberadamente multilíngue
da amostra de [[EXP-005]] (metade não inglesa, por desenho).

Na reunião com o orientador de 2026-09-03, foi decidido restringir a
população-alvo da pesquisa a skills em **inglês**.

**Decisão.** A população-alvo da QI-1 — e, por extensão, de QI-2/QI-3 via
[[#D-024]] — passa a ser **skills em inglês**. Conteúdo em outros idiomas
fica fora do escopo da estimativa de prevalência e da classificação
subsequente.

**O que isso muda:**

1. O denominador da QI-1 deixa de ser os 1.877.981 (ou 1.877.939 após a
   exclusão de [[EXP-002]]) representantes em todos os idiomas e passa a ser
   apenas o subconjunto de língua inglesa desse total. Esta decisão **não
   fixa** um número exato de denominador — precisa ser recomputado por
   script versionado, com um `EXP-XXX` próprio, antes de qualquer estimativa.
2. As cinco regras vinculantes de [[#D-012]] (não descartar por idioma, não
   tratar inglês como padrão etc.) deixam de valer para a **definição da
   população** — continuam corretas como proteção contra viés **dentro** de
   uma população multilíngue, mas essa deixou de ser a população estudada.
3. [[Multilingual Strategy]] deixa de orientar o desenho amostral principal
   da QI-1. As medições já feitas ([[EXP-003]]: 14,21% não inglês;
   [[EXP-004]]: concordância entre detectores) continuam válidas como
   caracterização histórica da população completa do dataset. A **camada de
   detecção de idioma que elas construíram é reaproveitada com papel
   diferente**: deixa de ser variável de estratificação (L1–L5) e passa a
   ser **critério de filtro** (inglês vs. não inglês).
4. Os estratos linguísticos L1–L5 de [[EXP-004]] deixam de ser eixo de
   estratificação da amostragem principal — a população-alvo passa a ser
   aproximadamente monolíngue por construção.
5. A amostra de [[EXP-005]] (50 casos, metade deliberadamente não inglesa)
   deixa de refletir a composição da população-alvo agora em vigor.
   Permanece um artefato histórico válido — testou o [[Codebook]] em casos
   difíceis, inclusive multilíngues —, mas não é reaproveitável como piloto
   representativo da população sob esta decisão. Ver [[#D-026]].

**O que esta decisão não muda:**

- [[Codebook]] R-9 continua vigente para decidir casos de fronteira dentro do
  subconjunto em inglês (skills `mixed`, termos técnicos embutidos em outro
  idioma) — ver a pendência de definição operacional abaixo.
- [[Decision Log#D-013|D-013]] (tradução como apoio, nunca substituição)
  permanece válida para os casos de fronteira que restarem no subconjunto de
  inglês.

> [!warning] Definição operacional de "skill em inglês" — pendente
> Esta decisão fixa a restrição de escopo, mas não define o critério
> operacional exato: idioma majoritário do corpo (`human_language`/detector
> = `en`)? Skills `mixed` com inglês dominante entram ou saem? Front matter
> em inglês com corpo em outro idioma ([[Multilingual Strategy]] documentou
> 4,17% de divergência) conta como quê? Essa definição precisa ser fixada
> **antes** de gerar a nova amostra de [[#D-026]], usando a camada de
> detecção já validada em [[EXP-003]]/[[EXP-004]], e registrada como parte
> da execução de [[#D-026]] — não decidida ad hoc dentro do script.

> [!success] Pendência resolvida em 2026-09-03 (mesma reunião)
> Critério fixado: a skill precisa estar **100% em inglês**. Operacionalização
> que reaproveita um limiar já existente no projeto, em vez de inventar um
> novo: uma skill é elegível apenas se **não** se qualificaria como `mixed`
> nem `und` sob os critérios já fixados na regra **R-9** do
> [[Codebook]] v2.3 (`mixed` = duas ou mais línguas com conteúdo
> substantivo — operacionalmente, ≥15% do texto na língua minoritária,
> ≥40 caracteres não latinos e ≥20 palavras latinas; `und` = prosa curta ou
> técnica demais para decidir). Termos técnicos isolados em inglês dentro
> de texto majoritariamente não inglês não tornam a skill elegível
> sozinhos — e, simetricamente, um termo técnico isolado em outro idioma
> dentro de texto majoritariamente inglês não caracteriza `mixed` sob esse
> limiar. Trechos não-prosa (nome de arquivo, código, mensagem de erro
> literal, comando) em outro idioma não contam para o critério — a mesma
> etapa de pré-processamento de [[Multilingual Strategy]] §2 (remover
> código, front matter, URLs antes de detectar) se aplica aqui.
>
> O detector/script exato que aplica esse critério na amostragem
> permanece detalhe de implementação (não decisão metodológica adicional)
> — a documentar no script quando escrito.

> [!success] Denominador real calculado em 2026-09-03 — [[EXP-013]]
> `scripts/filter_population_english.py` rodou contra a população inteira
> (1.877.981 conteúdos distintos elegíveis, frame status quo de D-022).
> **1.571.243 (83,667%) são 100% em inglês**; 306.738 (16,333%) contêm ao
> menos um parágrafo detectado em outro idioma e ficam fora da
> população-alvo da QI-1 sob esta decisão. Sem duplicatas (1.877.981
> `file_sha` únicos = 1.877.981 linhas). Consistente com a estimativa por
> amostra feita antes (82,0%, IC 95% 75,2–88,8%) e um pouco abaixo da
> medição antiga de [[EXP-003]] (85,79% inglês) — esperado, porque o
> critério por parágrafo é mais estrito que a detecção de idioma
> dominante do documento inteiro. **Este é o denominador oficial da
> população restrita a inglês** até que [[Decision Log#D-022]] (elegibilidade)
> seja resolvida, o que mudaria o frame de partida.

> [!danger] Lacuna real encontrada em 2026-09-03, ao construir [[Classification Prompt (D-026)]]
> O limiar de `mixed` emprestado de R-9 (≥15% do texto em língua
> minoritária, **≥40 caracteres não latinos**, ≥20 palavras latinas) foi
> desenhado para mistura com escrita não latina (CJK, cirílico etc.) — a
> condição de "caracteres não latinos" o torna estruturalmente incapaz de
> capturar mistura **dentro da mesma escrita latina** (uma frase em
> italiano, português ou espanhol embutida num texto majoritariamente em
> inglês). Isso não é hipotético: o caso real
> `cybersec-testing-ransomware-recovery-procedures` (`file_sha` prefixo
> `2c503744`, já citado como âncora `PRIMARY` em [[Codebook]] §8) contém a
> frase *"Nota per Kimi Code: questa skill è convertita dal pacchetto
> Anthropic Cybersecurity Skills..."* em italiano, e o limiar de R-9 não a
> detectaria como `mixed`.
>
> **Resolvido em [[EXP-013]] (2026-09-03), com uma correção de percurso
> registrada por transparência.** A primeira tentativa
> (`lingua.detect_multiple_languages_of()` sobre o texto inteiro) foi
> **abandonada**: só ~2% dos candidatos passavam em 2.400 testados, muito
> abaixo do ~86% esperado por [[EXP-003]] — o algoritmo de segmentação
> automática do `lingua` mostrou-se instável em texto técnico ruidoso
> (tabelas, listas, trechos curtos), produzindo falsos positivos em massa.
> **Adotado:** `lingua.compute_language_confidence_values()` **por
> parágrafo** (≥40 caracteres, confiança ≥0,60 para vencer como não
> inglês) — captura o caso real do italiano embutido, mantém taxa de
> rejeição (~18% no primeiro lote) coerente com [[EXP-003]], e roda em
> ordem de dezenas de milissegundos por candidato. O limiar de confiança
> (0,60) é engenharia, não decisão metodológica formal — ver limitações em
> [[EXP-013]].

**Justificativa.** Decisão tomada pelo orientador na reunião de 2026-09-03.
A motivação específica (viabilidade de prazo, redução de escopo para a
iteração atual, ou outra razão) não foi detalhada nesta sessão — registrar
aqui se/quando for comunicada.

**Consequências.**

- Toda alegação de prevalência do TCC passa a valer para a **subpopulação de
  skills em inglês**, não para a população multilíngue completa do dataset
  GitSkills. É uma redução de escopo/generalização que precisa ser declarada
  explicitamente em toda apresentação de resultado.
- O trabalho já feito sobre multilinguismo ([[EXP-003]], [[EXP-004]],
  [[Multilingual Strategy]]) não é descartado: continua sendo a única
  medição existente da composição linguística real do dataset, útil para
  caracterizar **o que ficou fora** do estudo e para uma eventual extensão
  futura que reverta este recorte.
- [[#D-024]] (sequência QI-1 → validação → QI-2 → QI-3) permanece válida; o
  "conjunto de skills analisado" que ela define para QI-2 agora herda
  implicitamente a restrição a inglês.

**Alternativas.** Não há alternativas registradas nesta entrada — a decisão
veio definida pelo orientador. A alternativa que estava em vigor era a
própria [[#D-012]] (população multilíngue), agora revisada.

**Limitações.**

- Reduz a validade externa dos resultados: não respondem sobre a população
  real e multilíngue de Agent Skills, apenas sobre seu subconjunto em
  inglês (~85,79% da população por [[EXP-003]] — número aproximado, não
  recomputado sob o critério operacional desta decisão).
- Skills `mixed` ficam numa zona operacionalmente indefinida até a pendência
  acima ser resolvida.

---

## D-026 — Novo desenho de E-5/E-6: ensemble de três LLMs sobre amostra aleatória, validação humana restrita à discordância (revisa D-019)

**Data:** 2026-09-03 · **Status:** `aceita` (decidida em reunião com o
orientador) · **Branch:** `Q1` · **Revisa:** [[#D-019]] · **Ver também:**
[[#D-008]], [[#D-020]], [[#D-021]], [[#D-025]]

**Instrumento operacional.** O prompt único usado pelos três modelos,
sintetizado a partir da documentação oficial de prompt engineering da
Anthropic, OpenAI e Google, está em
[[Classification Prompt (D-026)]] — não testado ainda contra casos reais.
O resumo em linguagem simples para o anotador humano que faz a
adjudicação está em [[Guia do Anotador Humano (D-026)]].

**Contexto.** O caminho crítico vigente definia **E-5** como piloto de
anotação humana cega, estratificado por sinal preliminar × grupo linguístico
([[#D-020]], [[#D-021]]), sobre os 50 casos de [[EXP-005]], seguido de
**E-6** — gold set com concordância entre um ou dois anotadores humanos
([[#D-019]]). [[#D-019]] registrava explicitamente como **restrição
inegociável** que "LLM, ou consenso entre agentes, não pode ser usado como
segundo anotador humano nem como ground truth."

Na reunião com o orientador de 2026-09-03, foi decidido um desenho diferente
para produzir o padrão-ouro que alimenta **E-7**.

**Decisão.** E-5/E-6 passam a ser executados assim:

1. Sortear uma **nova amostra aleatória de n = 100** skills, sobre a
   população restrita a inglês por [[#D-025]] — **não** reaproveitando os
   50 casos de [[EXP-005]]. Amostragem determinística
   (`ORDER BY hash(file_sha)`), como no resto do projeto.
2. Cada um dos **três modelos** — **GPT-5.6 Sol**, **Claude Opus** e
   **Gemini 3.1 Pro** — classifica os 100 casos **independentemente**,
   aplicando o [[Codebook]] v2.3.
3. Onde os três modelos **concordam**, o rótulo de consenso é aceito.
4. Onde os três **discordam** (não há unanimidade), um **anotador humano**
   adjudica o caso aplicando o [[Codebook]] — esse julgamento humano é o
   rótulo final para esses casos.

O conjunto resultante (rótulos de consenso entre LLMs + rótulos
humano-adjudicados nos casos de discordância) passa a ser o padrão-ouro
operacional que alimenta a validação do classificador em **E-7**.

> [!danger] Isto reverte a restrição inegociável de [[#D-019]]
> [[#D-019]] proibia explicitamente usar consenso entre modelos como
> substituto de confiabilidade interavaliadores humana, e [[#D-008]] afirma
> que saída de LLM nunca é verdade de referência sem validação humana. Sob
> este novo desenho, os casos em que os três LLMs concordam **nunca são
> vistos por um humano** — o consenso entre modelos passa a funcionar, na
> prática, como ground truth para a maior parte da amostra (a fração exata
> depende da taxa de discordância observada, ainda desconhecida). Esta
> decisão **revoga** essa restrição especificamente para o desenho de
> E-5/E-6, por instrução explícita do orientador — registrada aqui, não
> aplicada em silêncio.

**Riscos que este desenho introduz — declarados, não resolvidos:**

- **Viés sistemático compartilhado entre os três modelos fica invisível.**
  Se os três LLMs erram na mesma direção no mesmo tipo de caso — algo
  plausível se compartilharem dados de treino ou dificuldades semelhantes —
  esse erro nunca chega a um humano, porque só a discordância aciona
  validação. [[EXP-012]] já documentou, com dados de validação cruzada
  (não especulação), que um classificador barato treinado neste domínio
  falha sistematicamente na fronteira `SECONDARY`/`MENTION` (F1 = 0,000 em
  todos os 5 repeats) — é exatamente o tipo de erro correlacionado que este
  desenho não teria como capturar, se os três modelos compartilharem essa
  dificuldade.
- **Amostragem aleatória simples, não estratificada.** Diferente do piloto
  anterior ([[#D-020]], estratificado por sinal × idioma para garantir casos
  de fronteira), esta amostra de n=100 é sorteada aleatoriamente sobre a
  população. Como a prevalência esperada de Security Skill é baixa
  (ordem de poucos pontos percentuais), é provável que a amostra contenha
  **poucos casos `PRIMARY`/`SECONDARY`** e menos ainda na fronteira
  `SECONDARY`/`MENTION` — justamente o caso mais informativo para validar o
  classificador ([[QI-1 Methodology]] §5). Isso não é corrigido por esta
  decisão; é um risco a monitorar quando a amostra for gerada.
- **A estatística de confiabilidade muda de natureza.** O framework de
  kappa do [[Codebook]] §9 pressupõe dois anotadores humanos independentes.
  Aqui a métrica análoga é: taxa de concordância unânime entre os três LLMs,
  e taxa de casos que precisaram de adjudicação humana. Essas duas
  quantidades devem ser reportadas explicitamente e **não devem ser
  apresentadas como equivalentes** a um kappa interavaliadores humano.
- **Cobertura de validação humana é parcial, e precisa ser declarada como
  tal.** Todo relato deste gold set deve informar a fração de casos que
  recebeu julgamento humano (discordância) versus a fração aceita só por
  consenso de LLM.

**O que esta decisão não muda:**

- [[#D-008]] continua valendo para todo uso de LLM fora deste desenho
  específico — modelo, versão, prompt e temperatura de GPT-5.6 Sol, Claude
  Opus e Gemini 3.1 Pro devem ser registrados quando a classificação for
  executada.
- [[#D-021]] (cegamento) continua aplicável no que for possível: os três
  LLMs não devem receber o sinal preliminar de triagem, tier ou motivo de
  seleção como parte do prompt — apenas o conteúdo da skill, para evitar
  ancoragem, do mesmo modo que se exigiria de um anotador humano.
- [[#D-025]] define a população da qual a amostra de n=100 é sorteada.

**Consequências para o restante do plano:**

- [[EXP-005]] (50 casos, ainda não anotados por humano) deixa de ser a base
  de E-5/E-6. Permanece um artefato gerado e válido, reaproveitável no
  futuro (por exemplo, como amostra de comparação ou se a decisão for
  revista), mas não é mais parte do caminho crítico em execução.
- [[#D-015]] (desenho multi-estágio, pendente de custo por item medido em
  E-5) precisa de uma fonte de dado de custo diferente sob este desenho —
  o tempo por item de um humano lendo 100 casos não é mais medido da mesma
  forma que no piloto anterior (que cronometrava anotação completa, não
  apenas adjudicação de discordância). Registrado como pendência aberta,
  não resolvida aqui.
- Nenhum `EXP-XXX` é reservado por esta decisão — será atribuído quando o
  script que implementa este desenho for escrito e executado, seguindo a
  convenção do projeto ([[03 - Methodology]] §8).

**Alternativas consideradas.**

- **(a) Manter E-5/E-6 como piloto + gold set humano completo** (desenho
  anterior, [[#D-019]]/[[#D-020]]/[[#D-021]]). Era o desenho vigente até
  esta reunião; substituído por instrução do orientador.
- **(b) Dois anotadores humanos independentes**, fallback previsto em
  [[#D-019]] quando disponível. Não adotada nesta decisão — o orientador
  optou pelo ensemble de LLMs com adjudicação humana restrita à
  discordância.
- **(c) Ensemble de três LLMs, validação humana só na discordância.**
  **Adotada.**

**Limitações.**

- Esta decisão não define um critério numérico de quantos casos de
  discordância seriam "poucos demais" para validar o classificador com
  confiança — herda a mesma lacuna que [[#D-024]] já registra para o
  critério de "validação satisfatória" de E-7.

> [!success] Duas pendências resolvidas em 2026-09-03 (mesma reunião)
> **1. Cegamento entre os três modelos, explícito e não negociável.** Os
> três modelos classificam de forma estritamente independente: nenhum dos
> três recebe, em nenhum momento, a saída ou a classificação de outro
> modelo — nem durante a chamada, nem em qualquer etapa posterior de
> reclassificação. Isso já estava implícito em "classificam
> independentemente" no texto original desta decisão, mas fica registrado
> aqui como regra explícita, por analogia direta a R-11
> ([[#D-021]]): o sinal preliminar de outro julgador nunca é exposto antes
> do julgamento.
>
> **2. Escopo da adjudicação humana: todas as dimensões, não só
> `security_relevance`.** Sempre que os três modelos discordarem em
> **qualquer** dimensão do [[Codebook]] — classe principal
> (`security_relevance`), `security_focus`, `operational_security`,
> `operation_level`, `security_functions`, `security_concerns`,
> `operational_capability`, `evidence`, `confidence`, `rule_applied`,
> `grc_case` ou `secondary_mention_boundary` —, o caso vai para
> adjudicação humana. Isso resolve as duas lacunas anteriores (regra de
> desempate parcial; tratamento de discordância multi-label) com uma única
> regra mais ampla, em vez de regras separadas por campo.
>
> **Operacionalização adotada (não literalmente especificada na reunião,
> registrada aqui como interpretação razoável a confirmar):** quando
> qualquer dimensão diverge, o **caso inteiro** — não só o campo
> divergente — vai para adjudicação humana, que decide todos os campos
> daquele caso. Justificativa: as dimensões do Codebook são interdependentes
> (`security_functions`, por exemplo, só existe se `security_relevance`
> for `PRIMARY`/`SECONDARY`), e reconciliar campos vindos de fontes
> diferentes por caso — parte do consenso de LLM, parte de um humano —
> produziria um registro internamente inconsistente. Se essa leitura não
> for a intencionada, precisa de correção explícita antes da execução.

---

## D-027 — Esquema de três classes com subclassificação posterior (revisa D-004/D-006, Codebook v2.4)

**Data:** 2026-09-03 · **Status:** `aceita` (pesquisador) — requer aval do
orientador por revisar a definição operacional

**Contexto.** O [[EXP-013]] produziu a primeira medida de confiabilidade do
instrumento, com três LLMs sobre 100 casos. Fleiss' κ:

| Dimensão | κ | Leitura (Landis & Koch) |
|---|---|---|
| `security_focus` | **0,942** | quase perfeita |
| `security_relevance` (4 ordinais) | 0,448 | moderada |
| **Security Skill vs resto** | **0,370** | **sofrível** |
| `operational_security` | 0,298 | sofrível |
| `grc_case` | 0,234 | sofrível |
| `confidence` | 0,070 | praticamente ruído |

O desfecho que decide a QI-1 era o menos confiável do instrumento. Em contagem:
`PRIMARY` deu 6/6/7 entre os três modelos (amplitude de 1 caso), enquanto
`SECONDARY` deu 25/7/8 (amplitude de 18, 3,6×). Traduzido em prevalência sobre a
amostra: 6,6–7,7% usando só `PRIMARY`, contra 14,3–34,1% usando
`PRIMARY`+`SECONDARY` — **20 pontos percentuais de amplitude no número-título**.

Decompondo os 40 casos de classe divergente por fronteira em disputa: 20 (50%)
eram `NONE`↔`SECONDARY`, contra apenas 7 (17,5%) em `MENTION`↔`SECONDARY`. O
Codebook v2.3 §10 previa que o piloto estressaria a fronteira
`SECONDARY`/`MENTION`; **o piloto mostrou que a hipótese estava errada** — a
disputa dominante não era *"é acionável o bastante?"* e sim *"isso é segurança,
afinal?"*, com 35% do desacordo concentrado em restrições de comportamento de
agente, categoria onipresente num corpus de agent skills e para a qual o
codebook não tinha regra.

**Decisão.** Codebook **v2.4**:

1. **Três classes** — `PRIMARY`, `SECONDARY`, `NONE`. `MENTION` e `AMBIGUOUS`
   deixam de existir como classes.
2. **Decisão por analogia de papel profissional** — *se esta skill fosse uma
   pessoa, qual seria a profissão dela?* Profissional de cibersegurança →
   `PRIMARY`; outra profissão com consideração de segurança no texto →
   `SECONDARY`; sem consideração alguma → `NONE`.
3. **`PRIMARY` e `SECONDARY` são ambas Security Skill.** A classe distingue
   **se segurança é o foco**, não se conta.
4. **`SECONDARY` é deliberadamente inclusivo** — balde de coleta por
   **presença**, não julgamento de **grau**. Contam explicitamente: restrição de
   comportamento de agente (read-only, permissão, escopo de ferramenta),
   configuração protetiva (`chmod 600`, secrets), implementação de controle de
   acesso (login/JWT/RBAC), e defesa/teste contra ameaça nomeada.
5. **Subclassificação posterior por open coding** sobre `PRIMARY` ∪ `SECONDARY`,
   com categorias emergindo dos padrões observados — nunca importadas de
   referencial externo.
6. `confidence` e `rule_applied` saem de qualquer cálculo de concordância e de
   qualquer gatilho de adjudicação.

**Justificativa.** A pergunta de grau ("é substancial/acionável?") era a fonte
medida da baixa confiabilidade e foi removida do caminho crítico; a pergunta de
presença que a substitui é estruturalmente mais fácil. A granularidade não é
perdida — é adiada para um estágio onde erra-se de forma recuperável, porque
subclassificar um conjunto já coletado é revisável, enquanto excluir da coleta
não é. Por isso R-2 inverte a orientação da v2.3: na dúvida entre `SECONDARY` e
`NONE`, prefere-se `SECONDARY` com `confidence: low`.

**Alternativas descartadas.**
- *Manter as quatro classes e refinar R-2* — atacaria os 17,5% do desacordo, não
  os 50%.
- *Esquema novo com `protected_object` + `security_actionability` ordinal*
  (proposto pelo agente e descartado) — a analogia de papel profissional resolve
  os mesmos casos sem schema novo, preservando comparabilidade com [[EXP-005]] e
  [[EXP-012]].
- *Colapsar tudo em binário Security/não* — perderia a distinção de foco, que é
  justamente a medida confiável (κ=0,942).

**Consequências.**
- **O numerador cresce muito.** Âncoras medidas: 34% (leitura inclusiva do GPT no
  [[EXP-013]]) a 78,69% (alcance da recuperação ampla por keyword, [[EXP-002]]).
  O relato **tem de ser em dois níveis** — quantas contêm alguma consideração de
  segurança, e quantas existem para fazer segurança. Número único é indefensável.
- **A confiabilidade da v2.4 é desconhecida.** Os κ acima são da v2.3 e **não
  transferem** — mudança de esquema invalida confiabilidade calculada sob o
  esquema anterior. Re-teste obrigatório sobre os mesmos 100 casos antes de uso
  em escala.
- Instrumentos adaptados em 2026-09-03: [[Classification Prompt]] e
  [[Guia do Anotador Humano]] substituem as versões D-026 (que
  permanecem por rastreabilidade), e `aggregate_llm_classifications.py` passou
  a aceitar dois avaliadores.
- As âncoras da v2.3 foram revalidadas e **nenhuma quebra**; `zero-to-running` e
  `clawville` migram de `MENTION` para `SECONDARY` por efeito da fusão.

**Corroboração externa.** *Agent Skills in the Wild* (arXiv 2601.10338)
classificou 1.218 skills de outros marketplaces em 8 categorias funcionais e
encontrou **7,3%** em *Security/Red-team* — praticamente em cima da nossa camada
`PRIMARY` (6,6–7,7%). A taxonomia deles é de rótulo único e **não tem equivalente
de `SECONDARY`**, o que explica o κ=0,86 reportado: mede propósito dominante,
que corresponde ao nosso `security_focus` (κ=0,942). Ver
[[Classification and Sampling Precedents]].

---

## D-028 — Evidência insuficiente vira exclusão de frame, não classe (fecha D-022)

**Data:** 2026-09-03 · **Status:** `aceita` (pesquisador)

**Contexto.** [[Decision Log#D-022]] (elegibilidade da população) estava em
aberto desde 2026-08-22. Paralelamente, `AMBIGUOUS` acumulava três fenômenos
distintos: texto insuficiente, script não recuperado (`composition_truncated = 1`,
13,43% dos representantes) e fronteira conceitual real. Como `AMBIGUOUS` ficava
fora do numerador **e** do denominador, um problema de cobertura de dado
encolhia a população em silêncio.

**Decisão.** O que não pode ser classificado sai da **população**, não vira
classe. Duas exclusões, aplicadas antes da classificação:

| Exclusão | Critério | n | % |
|---|---|---|---|
| Sem evidência classificável | `length(description) + body_chars < 200` | 25.284 | 1,35% |
| Evidência truncada e indecidível | `composition_truncated = 1` **e** texto restante não permite decidir | ≤14.157 | ≤0,75% |

**Justificativa do limiar de 200.** Medido no dataset: `body_chars` cobre só o
corpo, e o Codebook aceita `evidence: description` — existem skills com
`body_chars = 1` e `description` completa, perfeitamente classificáveis. Logo o
critério tem de ser sobre **description + body**, não sobre tamanho do corpo.
Inspeção do conteúdo real por faixa mostrou que skills de 150–400 caracteres são
classificáveis sem dificuldade (a descrição declara o propósito), enquanto abaixo
de ~200 aparecem ponteiros de symlink (`../../../.claude/commands/...`, 3.447
casos), corpo vazio e front matter sem descrição (11.866 sem `description` e
corpo curto). 200 caracteres ≈ 30 palavras ≈ duas frases, e fica logo abaixo do
p02 da distribuição (274) — corta a cauda extrema, não uma fatia da população.
O corte é **mecânico** (contagem de caracteres), sem julgamento, logo
perfeitamente reprodutível.

**Script ausente não muda a classe** e **não força `SECONDARY`**: se a descrição
revela o comportamento, classifica-se normalmente com `confidence` mais baixa.
Só o caso genuinamente indecidível é excluído.

**Controle de viés obrigatório.** A segunda exclusão depende de dúvida **sobre a
própria variável estimada**, o que enviesa em direção desconhecida — e é um
*julgamento*, ao contrário do corte de tamanho. Mitigação: reportar a prevalência
como **intervalo de identificação parcial** (limites de Manski), calculado
assumindo que todos os excluídos são Security Skill e que nenhum é. Como o
universo possível é ≤0,75%, o intervalo deve sair estreito — o que **demonstra**
que a exclusão foi inofensiva em vez de assumir. Toda exclusão é registrada com
`file_sha` e motivo em `results/`, para ser auditável e re-executável.

**Alternativas descartadas.**
- *Manter `AMBIGUOUS` como classe* — mistura problema de dado com problema de
  construto e torna a contagem ininterpretável.
- *Forçar os indecidíveis para `NONE`* — subestima sistematicamente, e o viés é
  direcional: skills que executam coisas (mais prováveis de serem de segurança)
  são as que mais dependem de script.
- *Corte por percentil de `body_chars`* — mede a coisa errada; jogaria fora
  skills classificáveis pela descrição.

**Precedente.** A análise de conteúdo clássica já trata "unidade não
codificável" como problema de **seleção de documento**, resolvido no estágio do
frame, e não como categoria do esquema de codificação. Filtrar artefatos triviais
com critério declarado é prática aceita em MSR. Ver
[[Classification and Sampling Precedents]] §4 e §5.

**Consequências.** [[Decision Log#D-022]] passa de `EM ABERTO` para fechada. O
denominador da QI-1 precisa ser recomputado sobre o frame com os dois cortes,
partindo dos 1.571.243 conteúdos em inglês de [[EXP-013]]. Números para o TCC
exigem script versionado e `EXP-XXX` próprio — os desta entrada vieram de
consulta exploratória.

---

## D-029 — Primeira classificação enxuta; dimensões medidas e podadas (Codebook v2.5)

**Data:** 2026-09-04 · **Status:** `aceita` (pesquisador)

**Contexto.** O [[EXP-014]] mediu, pela primeira vez, **cada dimensão** do
instrumento sobre a mesma amostra (n=100, dois avaliadores, Codebook v2.4):

| Dimensão | κ / Jaccard | Concordância bruta |
|---|---|---|
| `security_relevance` | κ=0,724 | 84% |
| `security_focus` | κ=1,000 | 100% |
| `grc_case` | κ=0,852 | 99% |
| `evidence` | J=0,788 | — |
| `security_functions` | J=0,784 | — |
| `frame_exclusion` | κ=0,662 | 99% |
| `operational_security` | κ=0,511 | 77% |
| `operation_level` | κ=0,446 | **61%** |
| `security_concerns` | J=0,368 | — |
| `operational_capability` | J=0,348 | — |
| `rule_applied` | κ=0,307 | 50% |
| `confidence` | κ=0,177 | 46% |

Três achados decidiram a poda:

1. **`security_focus` é redundância pura.** Em **100/100 casos, nos dois
   avaliadores**, `security_focus` == (`security_relevance` == `PRIMARY`). Não
   é dimensão independente — é a classe medida duas vezes. Isso recontextualiza
   o κ=0,942 da v2.3, o número mais citado do projeto: **era a confiabilidade
   de `PRIMARY`**, não de uma dimensão separada.
2. **`security_functions` importa referencial externo para dentro do
   instrumento.** `PREVENT·DETECT·ASSESS·TEST·RESPOND·RECOVER` é derivado do
   NIST CSF. Coletá-lo na classificação e alimentar o open coding é exatamente
   a circularidade que a regra inegociável da QI-2 proíbe.
3. **Vocabulário livre normalizado cedo demais não funciona.** Em `LLM003` e
   `LLM001` a interseção de `security_concerns` entre os avaliadores é
   **vazia**, embora as `note` descrevam a mesma coisa de forma reconhecível.
   É sinonímia, não discordância — sintoma de fazer open coding um caso por
   vez, sem ver o conjunto.

**Decisão.** Codebook **v2.5**:

- **Primeira classificação reduzida a cinco campos**: `security_relevance`,
  `evidence`, `frame_exclusion`, `note`, `confidence` (este último explicitamente
  como metadado de triagem, não medida).
- **`note` promovida a campo estruturado em prosa**, com três elementos
  obrigatórios (papel profissional · qual é o conteúdo de segurança, ou por que
  não conta se `NONE` · o elemento concreto que sustenta). Passa a ser o
  **insumo primário do open coding**.
- **`security_focus` removida** — se necessária, derive da classe.
- **`security_functions` migra para a QI-3** (crosswalk), depois da taxonomia
  estabilizada.
- **`operational_security` e `operation_level` removidas**; se voltarem, voltam
  **fundidas numa dimensão só**, com definição nova e medição própria.
- **`grc_case`, `security_concerns`, `operational_capability` removidas** da
  primeira classificação.
- **A adjudicação da primeira classificação considera apenas
  `security_relevance`** — dimensões de apoio não disparam revisão humana.

**Justificativa.** A etapa 2 relê os casos de qualquer forma (é reclassificação,
não enriquecimento incremental), então coletar payload descritivo mal medido na
etapa 1 não compra nada e custa confiabilidade e tempo de anotação. Efeito
imediato: a adjudicação do EXP-014 cai de **50 para 16 casos**.

**Não altera a decisão de classe.** R-1…R-8 ficam intactas, portanto os
coeficientes do [[EXP-014]] (κ=0,724 na classe, κ=0,672 na dicotomia)
**transferem** para a v2.5. Esta é a diferença em relação a D-027, que alterou
as regras e por isso invalidou os números da v2.3.

**Alternativas descartadas.**
- *Manter tudo e só não usar na adjudicação* — não resolve: o campo continua
  sendo pedido ao anotador, custa tempo e degrada a atenção no que importa.
- *Normalizar o vocabulário de `security_concerns` com lista fechada* — seria
  impor taxonomia a priori, violando a regra da QI-2.

**Consequências.** [[Classification Prompt]], [[Guia do Anotador Humano]] e `aggregate_llm_classifications.py` precisam refletir o payload
reduzido. Métricas de concordância passam a ser calculadas por
`scripts/compute_agreement.py`, que reporta Cohen's κ, Krippendorff's α, Gwet's
AC1 e Brennan-Prediger com IC95 por bootstrap, mais os índices de prevalência e
viés (Byrt et al.) e o teste de McNemar.

**Limitação declarada.** Baseado em **uma** rodada de 100 casos com dois
avaliadores, um dos quais teve vazamento de contexto por memória de agente (ver
[[EXP-014]]). A redundância de `security_focus` (100/100 nos dois) é robusta o
bastante para decidir sozinha; os κ das dimensões fracas têm IC largo nesse n —
a direção é clara, o valor exato não.

---

## D-030 — Terceira exclusão de frame: o arquivo não é instrução (Codebook v2.6)

**Data:** 2026-09-05 · **Status:** `aceita` (pesquisador)

**Contexto.** Inspecionando a amostra do [[EXP-014]], o pesquisador observou que
`LLM019` não é uma skill: é um **despejo de resultados de pesquisa** (`Date
Range`, `Mode`, `OpenAI Model`, threads de Reddit com score e link) salvo com o
nome `SKILL.md`. Leitura dos demais casos encontrou um segundo, `LLM067`, um
documento *"Feature Context"* com bloco `Document Metadata / Generated / Input
Type / Source`. Nenhum dos dois é instrução para um agente.

O limiar do [[Decision Log#D-028]] não os alcança: têm 15.744 e 19.445
caracteres. Ele exclui **evidência de menos**, não **gênero errado**.

Importante separar dois achados, porque a leitura dos 14 casos de `name` nulo da
amostra mostrou que eles **não** são a mesma coisa:

- **12 de 14** são skills legítimas cujo front matter está fora da spec. O
  `name` chega vazio ao avaliador, mas o conteúdo é instrucional — em `LLM060` o
  front matter aparece intacto quatro linhas abaixo, com `name: pm-dogfood-add`.
  **`name` nulo não é critério de exclusão.**
- **2 de 14** são saídas geradas. Só esses saem.

**Decisão.** Terceiro valor de `frame_exclusion`:
**`not_an_instruction_artifact`** — o arquivo é registro ou saída produzida por
algum processo (relatório, log, dump, documento de contexto gerado), não um
conjunto de instruções dirigido a um executor.

O anotador marca; **a exclusão da população fica adiada** até que a taxa seja
estimada (ver "O que fica em aberto"). Marcar hoje custa uma coluna que já
existe no formulário; não marcar custa reler a amostra inteira depois.

**Por que não é a mesma coisa que o `truncated_undecidable` do D-028.** Aquela
exclusão depende do desfecho — exclui-se por não conseguir decidir *se há
segurança* —, e por isso exige limites de Manski. Esta não: decidir "isto é
instrução ou é saída?" é julgamento de **gênero do documento**, feito sem
consultar se há segurança. O estimador estratificado continua válido sem limites.

**Justificativa quantitativa** ([[EXP-015]], `results/EXP-015_frame_artifact_profile.json`).
Foi testada uma regra em escala populacional — marcador de procedência no topo
(`Generated:`, `Date Range:`, `Input Type:`, `Document Metadata`, …) **e**
`frontmatter_valid = 0`:

| | n | % da população |
|---|---:|---:|
| População (representantes) | 1.877.981 | 100% |
| Front matter válido | 1.625.701 | 86,57% |
| Qualquer marcador de procedência | 5.913 | 0,315% |
| **Regra completa** | **707** | **0,038%** |

Nos 14 casos conhecidos a regra acerta tudo (2 verdadeiros positivos, 0 falsos
positivos). **Mas o recall é baixo.** Os 2 não-skills apareceram dentro do
estrato `frontmatter_valid = 0`, que tem 252.280 arquivos; a regra marca 707
deles, 0,28% do estrato, contra os ~14% que a leitura sugere. Mesmo supondo que
a leitura superestime em uma ordem de grandeza, a regra encontraria menos de um
terço do que existe.

**Por isso a regra determinística foi rejeitada como filtro.** Ela removeria
0,04% da população e faria o quadro **parecer saneado**, com a distorção intacta
e agora sem sinalização. A regra permanece útil como **estratificador**, no
mesmo espírito do [[Decision Log#D-014]]: contagem de positivos não é taxa.

**Alternativas descartadas.**

- *Excluir todo `name` nulo* — descartaria 252.280 arquivos, dos quais a leitura
  indica que ~86% são skills legítimas. Erro muito maior que o corrigido.
- *Aplicar a regra determinística e seguir* — recall estimado em ~2%; ver acima.
- *Classificar como `NONE` sem marcar* — colapsa duas coisas distintas num
  rótulo só e torna a correção posterior impossível sem reanotar a amostra.

**Limitação declarada.** A direção do viés **não é garantidamente conservadora**.
Se os artefatos gerados fossem neutros quanto a segurança, deixá-los no
denominador subestimaria a prevalência — erro seguro. Medição em [[EXP-015]]:
o grupo marcado pela regra tem **29,14%** de vocabulário de segurança contra
**24,93%** da população com front matter válido. É plausível: relatório de scan
e saída de auditoria são exatamente o que se salva por engano como `SKILL.md`.
Ressalva sobre a ressalva: isso é **vocabulário**, não classificação — este
projeto já mediu que keyword não separa classe ([[EXP-001]], [[EXP-002]]). Serve
para proibir a hipótese de neutralidade, não para estimar o viés.

Ordem de grandeza do erro, se ignorado: com f ≈ 2% da amostra e prevalência real
de 5%, a estimativa cairia entre ~4,9% (artefatos neutros) e ~6,9% (todos
positivos) — até ~2 pontos numa estimativa de 5.

**O que fica em aberto — decisão futura, não tomada aqui.** Estimar a taxa de
não-instrução no estrato `frontmatter_valid = 0` **sem** marcador de procedência
(251.573 arquivos, 13,4% da população), que é onde o problema está escondido.
Rota proposta: amostra determinística de ~100 casos, uma pergunta por caso
("instrução ou saída?"), taxa com IC, denominador corrigido. Nada disso invalida
a anotação já feita, desde que a marcação exista — que é exatamente o que esta
decisão garante.

**Consequências.** [[Codebook]] passa a **v2.6** (§1.2 e §2.1);
[[Guia do Anotador Humano]] §6 e §7; [[Classification Prompt]] — no prompt a
mudança vale **a partir da próxima rodada**, e o [[EXP-014]] permanece registrado
sob o schema de dois valores. `scripts/build_adjudication_form.py` não muda: a
coluna `frame_exclusion` já existe e é texto livre.

---

## D-031 — Gold set da QI-1: dois anotadores humanos independentes e reconciliação mútua (estende D-026)

**Data:** 2026-09-13 · **Status:** `aceita` (pesquisadores)

**Contexto.** O [[Decision Log#D-026]] previa que **um** anotador humano
adjudicasse os casos em que os modelos discordassem. No [[EXP-014]] foram 16
casos. Eles foram anotados por **dois** pesquisadores, Victor e Havillon, de
forma independente, cada um no próprio arquivo, seguindo o
[[Guia do Anotador Humano]] (Codebook v2.6).

**Decisão.** O rótulo humano de um caso adjudicado sai deste procedimento:

1. **Anotação independente**, um arquivo por anotador, sem conversa prévia.
2. **Concordância medida antes de qualquer conversa**, e é essa que se reporta
   como independente.
3. **Erro de marcação** (rótulo que contradiz a própria nota do anotador) pode
   ser corrigido no arquivo individual, **registrado na nota** com data, valor
   anterior e motivo. Mudança de julgamento depois da conversa **não** é
   permitida nos arquivos individuais.
4. **Reconciliação mútua** dos casos ainda divergentes: os dois anotadores
   relêem o caso e decidem juntos. Se não houver acordo, **o orientador
   desempata**.
5. O rótulo final vai para o formulário principal
   (`EXP-014_adjudication_form.csv`), com etiqueta de origem no início da nota.

**Resultado.**

| Etapa | Concordância | Cohen's κ (IC95 bootstrap) | Gwet's AC1 |
|---|---|---|---|
| Marcação original, independente | 10/16 (0,625) | 0,186 [−0,23; 0,61] | 0,343 |
| Depois de corrigir 2 erros de marcação | 12/16 (0,750) | 0,458 [0,00; 0,86] | 0,562 |

- Erros de marcação corrigidos: LLM083 (NONE → SECONDARY) e LLM089
  (SECONDARY → NONE), os dois no arquivo do Victor. Nos dois a nota já dizia
  o contrário do rótulo.
- Reconciliados em conjunto: LLM029, LLM045, LLM052 e LLM091, **todos para
  `NONE`**. Motivos registrados nas notas:
  - LLM029/LLM052: linters, testes e confiabilidade são qualidade, e o Guia §3
    exige a consideração de segurança no conteúdo.
  - LLM045/LLM091: a restrição imposta ao agente foi lida como de fluxo de
    trabalho, não de proteção.
- Nenhum caso precisou de desempate do orientador.

**Por que a concordância baixa não invalida o gold set.**

- **n=16.** Os intervalos são largos: o de κ da marcação original inclui zero.
- **Seleção.** Os 16 são, por construção, os casos em que os modelos
  discordaram, ou seja, os mais difíceis da amostra. **Não** se comparam com o
  κ=0,672 dos modelos, medido em 100 casos sorteados.
- **A divergência se concentrou** em duas regras do Guia (restrição ao agente
  e "qualidade ≠ segurança"), não se espalhou. Isso aponta para onde o
  instrumento precisa de exemplo, não para um instrumento sem confiabilidade.

**Composição do gold set** (`results/EXP-014_gold_set.csv`,
`scripts/build_gold_set.py`):

| | n |
|---|---:|
| Casos da amostra | 100 |
| Fora do quadro do [[EXP-016]] (LLM078, 75 caracteres) | −1 |
| **Gold set no quadro** | **99** |
| … consenso entre modelos, sem verificação humana | 83 |
| … concordância humana independente | 10 |
| … concordância após corrigir marcação | 2 |
| … reconciliação mútua | 4 |

Classes: `PRIMARY` 9 · `SECONDARY` 46 · `NONE` 44.

**Marcações de quadro aplicadas ao gold set.**

- `truncated_undecidable` ([[Decision Log#D-028]]) em **LLM092**. Os dois
  modelos marcaram, mas o arquivo de consenso guardou só a classe. Sai da
  população na estimativa, com limites de Manski.
- `not_an_instruction_artifact` ([[Decision Log#D-030]]) em **LLM019** e
  **LLM067**. Marcados; exclusão adiada.

**Estimativa preliminar, não é a resposta da QI-1.** Tratando o gold set como
amostra aleatória simples do quadro (n=98, sem LLM092):

- Security Skill **56,1%**, IC95 de Wilson [46,2%; 65,5%]
- `PRIMARY` 9,2% · `SECONDARY` 46,9%
- Limites de Manski para LLM092: [55,6%; 56,6%]
- Sensibilidade sem os dois artefatos do D-030 (n=96): 57,3% [47,3%; 66,7%]

Três razões para não tratar isso como resultado:

- 83 rótulos são de consenso de LLM sem verificação humana (risco declarado do
  D-026);
- n=98 dá margem de ~±10 pp;
- o `SECONDARY` inclusivo do D-027 é deliberadamente amplo.

**Consequência para o desenho.** O Desenho C ([[Decision Log#D-014]]) e a tabela
de tamanhos da [[QI-1 Methodology]] §3 foram pensados para prevalência de ~5%,
com positivos raros. Com a prevalência perto de 50%, a vantagem da
estratificação precisa ser recalculada antes do E-8/E-9. Fica como decisão
aberta para o orientador (ver [[03 - Methodology]], E-7).

**Alternativas descartadas.**

- *Um só anotador, como no D-026*: impede medir a confiabilidade humana, que é o
  que sustenta o rótulo dos 16.
- *Conversar antes de anotar*: produziria um rótulo, mas inflaria a
  concordância e esconderia onde o Guia é ambíguo.
- *Reescrever os arquivos individuais depois da conversa*: apagaria a medida de
  concordância independente.

**Limitação declarada.** Os quatro casos reconciliados terminaram em `NONE`, o
rótulo inicial de um dos anotadores. A reconciliação foi mútua e o critério foi
o Guia §3, registrado caso a caso. O dado é declarado para que a direção possa
ser examinada.

**Consequências.** [[EXP-014]] (seção de adjudicação), [[Guia do Anotador Humano]]
(procedimento com dois anotadores), [[Codebook]] §8, [[03 - Methodology]] e
[[QI-1 Methodology]] (E-5/E-6 concluídos; próximo passo E-7).
`scripts/compute_agreement.py` passa a aceitar os CSVs humanos, e
`--original-marking` desfaz as correções de marcação registradas.

---

## D-032 — Subclassificação: mantida depois do gate do E-7; LLM propõe, humanos validam

**Data:** 2026-09-13 · **Status:** `aceita` (pesquisadores)

**Contexto.** Com o gold set pronto ([[Decision Log#D-031]]), surgiu a pergunta
de antecipar a subclassificação de `PRIMARY` ∪ `SECONDARY`
([[Codebook]] §5, [[Taxonomy Coding Protocol]]). Três argumentos a favor de
antecipar:

- o protocolo nunca foi testado;
- 46 das 55 skills de segurança do gold set são `SECONDARY`, o que torna a
  estimativa preliminar de 56% difícil de interpretar sem saber o que há
  dentro dela;
- as notas dos dois modelos já existem para 52 dos 55 casos.

Em aberto também estava **quem** faz a codificação aberta.

**Decisão.**

1. **A ordem do [[Decision Log#D-024]] fica mantida.** A subclassificação
   acontece **depois do gate do E-7**, sobre o conjunto classificado no E-8, e
   não como piloto no gold set agora.
2. **A codificação aberta é feita por LLM propondo e humanos validando.** Nas
   passagens do protocolo:

   | Passagem ([[Taxonomy Coding Protocol]] §3) | Quem faz |
   |---|---|
   | 1 — códigos abertos, com exemplo literal | **LLM propõe** |
   | 2 — agrupamento de códigos | **LLM propõe** |
   | 3 — poda, fusão e nomeação das categorias | **Humanos decidem** |
   | 4 — reaplicação da taxonomia a todos os casos | LLM aplica; **humanos revisam** |
   | §5.1 — conferência contra o `SKILL.md` original | **Humanos** |
   | §5.2 — confiabilidade (dupla codificação de subamostra) | **Dois humanos** |

**Salvaguardas obrigatórias**, porque o insumo já são notas de LLM
(protocolo §6) e o risco de circularidade aumenta:

- **Exemplo literal verificável.** Todo código proposto cita `case_id` e um
  trecho que precisa existir **literalmente** na nota de origem. A checagem é
  por script; código sem trecho confirmado é descartado. Isso impede categoria
  inventada pelo modelo.
- **Regra inegociável da QI-2 no prompt.** O prompt do propositor proíbe
  explicitamente OWASP, MITRE, NIST ou qualquer taxonomia externa; propostas que
  as usem como categoria são rejeitadas na passagem 3.
- **Registro completo** de modelo, versão, prompt e temperatura
  ([[Decision Log#D-008]]).
- **A decisão final sobre as categorias é humana.** A saída do LLM é proposta,
  nunca resultado.
- **A confiabilidade reportada é humana:** Krippendorff α para multi-valorados
  e Jaccard médio, calculados entre os dois pesquisadores aplicando a taxonomia
  final, e não entre LLM e humano.

**Recomendação, ainda não decidida:** o modelo propositor deve ser **diferente**
dos que escreveram as notas (GPT e Claude), para não reforçar a leitura deles.
O LLM local do orientador é o candidato natural, se passar pelo E-7.

**Alternativas descartadas.**

- *Piloto agora no gold set:* recusado para manter a sequência formal do D-024.
  O protocolo continua sem teste até o gate.
- *Dois pesquisadores codificando tudo à mão:* mais caro. O ganho sobre LLM
  propondo com salvaguardas foi julgado menor que o custo.

**Limitação declarada.** **Viés de ancoragem:** humanos que validam categorias
já propostas tendem a aceitá-las. A dupla codificação humana (§5.2) e a
conferência contra o texto original (§5.1) medem, mas não eliminam, esse
efeito. Declarar no texto.

**Consequências.** [[Taxonomy Coding Protocol]] → v1.1 (papéis por passagem e
salvaguardas); [[Codebook]] §5; [[03 - Methodology]] (subclassificação explícita
na ordem, depois do E-8); [[QI-2 Methodology]] §8.

---

## Ligações

[[00 - Research Overview]] · [[EXP-001]] · [[EXP-002]] · [[GitSkills]] ·
[[03 - Methodology]] · [[Codebook]] · [[QI-2 Methodology]] ·
[[QI-3 Coverage Methodology]] · [[Security Taxonomy]] ·
[[Classification and Sampling Precedents]]
