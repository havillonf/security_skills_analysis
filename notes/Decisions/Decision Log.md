---
tipo: decisões
atualizado: 2026-08-22
---

# Decision Log

Toda decisão metodológica relevante. Decisão já usada em experimento **não muda em
silêncio**: registra-se a revisão com data e motivo.

Status: `proposta` (aguarda pesquisador) · `aceita` · `revisada` · `rejeitada`.

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

1. `results/EXP-005_annotation_form.csv` traz apenas `case_id`, `name`, `body_chars`
   e os campos humanos vazios.
2. `results/EXP-005_reading_pack.md` traz apenas `case_id`, `name`, `description`,
   tamanho e o texto.
3. Tier, densidade, flags, grupo linguístico e motivo da seleção ficam em
   `results/EXP-005_strata_key.csv`, unido por `case_id` **somente depois** de a
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

## D-022 — Critério de elegibilidade da população — EM ABERTO

**Data:** 2026-08-22 · **Status:** `proposta` — **requer aprovação humana**
· **Branch:** `Q1` · **Origem:** achado C-5 da auditoria adversarial

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
`results/EXP-012_confusion_matrix.csv` confirma zero previsões de
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
`results/EXP-012_population_summary.json`, campo `caveat`).

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

- `results/EXP-012_population_classification.parquet` e
  `results/EXP-012_population_summary.json` são saídas do modelo B, **não**
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

`results/EXP-012_population_summary.json`, gerado em 2026-08-24T00:09:54Z:

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
`results/EXP-012_uncertain_cases_sample.csv` (metadados apenas).

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

## Ligações

[[00 - Research Overview]] · [[EXP-001]] · [[EXP-002]] · [[GitSkills]] ·
[[03 - Methodology]] · [[Codebook]] · [[QI-2 Methodology]] ·
[[QI-3 Coverage Methodology]] · [[Security Taxonomy]]
