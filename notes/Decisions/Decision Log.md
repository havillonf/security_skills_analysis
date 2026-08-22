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

## D-010 — Deduplicação por similaridade — EM ABERTO

**Data:** 2026-08-22 · **Status:** `proposta` — **requer aprovação humana**

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
**robustness check** em [[03 - Methodology|E-7]], não como pipeline principal —
assim o limiar não contamina o resultado central.

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
operacionalização no [[Codebook]] v2.0).

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
- O candidate retrieval de [[EXP-002]] (58 termos, só inglês) fica **inadequado como
  desenho final**. Permanece válido como medição já feita, não como pipeline.
- O gold set precisa representar a diversidade linguística; estratificação por idioma
  ou grupo linguístico quando houver suporte amostral.
- Desempenho do classificador avaliado **por idioma**, não só global. F1 global bom
  não é evidência de desempenho uniforme.
- Queda relevante de desempenho num idioma é **ameaça à validade da estimativa de
  prevalência**, a declarar.

**Correção que esta decisão força.** O [[Codebook]] v2.0 listava "skill em idioma que
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

## Ligações

[[00 - Research Overview]] · [[EXP-001]] · [[EXP-002]] · [[GitSkills]] ·
[[03 - Methodology]] · [[Codebook]] · [[QI-2 Methodology]] ·
[[QI-3 Coverage Methodology]] · [[Security Taxonomy]]
