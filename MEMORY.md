# MEMORY.md — Estado acumulado do projeto

> Gerado em 2026-08-25 a partir do estado real do repositório (branch `Q1`),
> do `README.md`, de `notes/` (vault Obsidian) e das skills em `.claude/skills/`.
> Este arquivo é um **ponteiro de continuidade**, não a fonte da verdade.
> A fonte da verdade metodológica é `notes/Decisions/Decision Log.md`
> (uma entrada `D-XXX` por decisão, com data, alternativas e consequências) e
> o plano em `notes/03 - Methodology.md`. Não duplique o conteúdo deles aqui —
> atualize os pointers.

## 1. Objetivo e contexto

TCC (possível artigo) de Victor Brito. Estuda a população pública de **agent
skills** (arquivos `SKILL.md`) do dataset **GitSkills** (Destefanis et al.,
MSR '27) pela lente de segurança no desenvolvimento com IA.

Questão central adotada (não a única possível — ver `notes/01 - Research
Question.md`): **QI-1** — qual a prevalência de skills de segurança na
população pública de Agent Skills? Formalizada em `Decision Log#D-011`.
Detalhe: [[project-context]] skill e `notes/00 - Research Overview.md`.

## 2. Arquitetura e stack

- **Dados**: 4 tabelas Parquet (`artifacts`, `artifact_siblings`, `repos`,
  `mining_runs`) baixadas de um mirror HuggingFace, cacheadas em `data/`
  (gitignored — cada pesquisador baixa localmente, mesma fonte).
- **Consulta**: DuckDB direto sobre Parquet (nunca carregar `artifacts`
  inteiro em pandas — ver skill `data-analysis`).
- **Execução**: `uv run --with <libs> python scripts/...` — não há `.venv`
  nem dependências instaladas globalmente na máquina Windows primária. O
  `Makefile` e `requirements.txt` assumem um layout POSIX que não reflete o
  ambiente real (ver `Decision Log#D-003`).
- **Anotação**: caderno científico em Obsidian (`notes/`), formulários CSV
  cegos para anotação humana/LLM-assistida.
- **Classificação (EXP-012, prova de conceito)**: scikit-learn (TF-IDF +
  LogisticRegression/LinearSVC) e `sentence-transformers`
  (`paraphrase-multilingual-MiniLM-L12-v2`), `joblib` para serialização.

## 3. Convenções do projeto

- **Idioma**: notas e commits em português; identificadores de código em
  inglês.
- **Numeração `EXP-XXX`**: cada número que vai para o texto do TCC precisa
  vir de um script versionado em `scripts/` com saída em `results/`. EXP-006
  a EXP-011 estão **reservados** no plano (`03 - Methodology.md` §8) para o
  caminho crítico rigoroso (E-6 gold set → E-11 consolidação). **EXP-012**
  foi usado para a prova de conceito do classificador (ver §8) justamente
  para não colidir com essa reserva — se criar um novo experimento, cheque
  essa tabela antes de numerar.
- **Git**: nunca commitar sem o pesquisador pedir explicitamente. Preferir
  commits pequenos e descritivos; não fazer merge de `Q1` para `main` sem
  pedido explícito.
- **Dados versionados vs gitignored**: `data/` inteiro, `results/**/*.parquet`,
  `results/**/*_reading_pack.md`, `results/**/*_sample_preview.md` e
  `models/*.joblib` são gitignored (regeneráveis por script, ou reproduzem
  texto de terceiros). Agregados pequenos (`*.json`, `*.csv` de métricas) são
  versionados. `models/security_classifier_v1_metadata.json` é a exceção
  versionada dentro de `models/`.
- **Decisões de alto impacto** (definir "segurança", threshold, unidade de
  análise, descartar volume de dados, escolher modelo definitivo) exigem
  aprovação humana explícita e viram entrada no Decision Log.

## 4. Estrutura e responsabilidades

Reorganizado em 2026-09-05: o que está no caminho crítico fica na raiz de
`notes/`; o resto foi para `notes/_arquivo/`, **sem apagar nada**. Wikilinks
não quebram ao mover (o Obsidian resolve por nome). Ver
`notes/_arquivo/README.md` para o que ainda é citável de cada arquivado.

```
notes/                        caderno científico (Obsidian) — fonte da verdade
  00-03 - *.md                 overview, questão, hipóteses, plano de etapas
  Resumo do Trabalho.md        resumo em linguagem simples
  Datasets/GitSkills.md        o dataset
  Decisions/
    Decision Log.md            D-001..D-031 — ÍNDICE DE STATUS no topo. Não dividir
    Codebook.md                Security Skill, v2.6 (3 classes)
  Instruments/                 o que se usa para anotar
    Classification Prompt.md   etapa 1 — para colar na CLI de cada modelo
    Guia do Anotador Humano.md etapa 1 — adjudicação humana; §9 = dois anotadores
    Taxonomy Coding Protocol.md etapa 2 — open coding (NÃO TESTADO)
  Methodology/                 QI-1 · QI-2 · QI-3
  Experiments/                 EXP-013 (amostra) · EXP-014 (confiabilidade + gold set) ·
                               EXP-015 (validade do quadro) · EXP-016 (denominador)
  Literature/                  Classification and Sampling Precedents.md
  Results/Security Taxonomy.md saída da etapa 2 (ainda v0.1, não produzida)
  _arquivo/                    fora do caminho crítico — ver README.md de lá
scripts/
  compute_agreement.py         Cohen · Krippendorff · Gwet AC1 · Brennan-Prediger
                               · IC bootstrap · McNemar  (EXP-014)
  aggregate_llm_classifications.py  consenso vs discordância; 2 ou 3 avaliadores
  build_llm_ensemble_sample.py amostra determinística de n=100 (EXP-013)
  filter_population_english.py filtro de idioma na população (EXP-013)
  build_adjudication_form.py   formulário cego dos casos discordantes
  build_adjudication_package.py pasta versionada com os casos a ler + procedência
  build_gold_set.py            consolida o GOLD SET (99) + estimativa preliminar
  profile_frame_artifacts.py   artefatos gerados no quadro amostral (EXP-015)
  build_analysis_frame.py      exclusões em sequência -> DENOMINADOR (EXP-016)
  (demais scripts servem experimentos arquivados — ver _arquivo/README.md)
models/                        classificador v1 do EXP-012 (fora do caminho crítico)
results/                       raiz = caminho crítico (EXP-013..EXP-016);
                               EXP-014_gold_set.csv é o gold set;
                               README.md indexa tudo. _arquivo/ tem
                               as etapas concluídas (EXP-001..005, EXP-012) e a
                               rodada v2.3, com README próprio
.claude/skills/                project-context, data-analysis, security-analysis
```

## 5. Decisões que não devem ser revertidas sem razão explícita

Lista de título apenas — conteúdo completo em `Decision Log`:

- **D-001** — unidade de análise primária = conteúdo distinto (`dedup_primary=1`), não ocorrência.
- **D-002** — resultado do notebook legado ("1,1%") é inválido; não citar sem recomputar.
- **D-004/D-006** — definição operacional de Security Skill.
  **Revisada por D-027** (2026-09-03): Codebook **v2.4**, três classes
  (`PRIMARY`/`SECONDARY`/`NONE`), decisão por analogia de papel profissional,
  `SECONDARY` deliberadamente inclusivo (presença, não grau), subclassificação
  posterior por open coding. `MENTION` e `AMBIGUOUS` deixaram de ser classes.
  **`PRIMARY` + `SECONDARY` = Security Skill** — a classe diz se segurança é o
  foco, não se conta. Motivo: o EXP-013 mediu que a fronteira de grau era a
  fonte da baixa confiabilidade (κ=0,298) e que 50% do desacordo estava em
  `NONE`↔`SECONDARY`, não em `SECONDARY`↔`MENTION` como o v2.3 §10 previa.
- **D-008** — LLM não é ground truth.
- **D-011** — QI-1 (prevalência) é a questão central; QI-2/QI-3 são extensões, não descartadas.
- **D-012** — população-alvo inclui todos os idiomas, não só inglês.
  **Revisada por D-025** (2026-09-03): população-alvo passa a ser restrita a
  skills em inglês, por decisão do orientador. D-012 permanece registrada
  por rastreabilidade; suas cinco regras não valem mais para a definição da
  população.
- **D-014** — Desenho C (amostragem estratificada com classificador de triagem) é o desenho estatístico adotado; a classificação em escala nunca é o resultado científico por si, só define os estratos.
- **D-018** — E-4 (candidate retrieval) executa depois de E-6, não antes (evita circularidade).
- **D-020/D-021** — sinal de triagem e metadados de seleção nunca são mostrados ao anotador (blinding) nem usados como rótulo.
- **D-023** — o classificador definitivo v1 (EXP-012) usa um golden set **assistido por LLM** como base operacional exploratória, não gold standard humano — não tratar seus números como resultado da QI-1.
- **D-024** (2026-08-27) — QI-2 e QI-3 têm execução **sequenciada e formal**:
  QI-1 → validação satisfatória do classificador (gate em E-7) → QI-2
  (conjunto de entrada = população `PRIMARY`/`SECONDARY` de E-8, não o pool
  de candidate retrieval) → QI-3 (depende de QI-2 estabilizada). Critério
  numérico de "validação satisfatória" **ainda não definido** — não inventar
  threshold sem decisão humana.
- **D-025** (2026-09-03, reunião com o orientador) — população-alvo restrita
  a skills em **inglês** (revisa D-012). Denominador da QI-1 precisa ser
  recomputado para o subconjunto inglês; critério operacional de "skill em
  inglês" (tratamento de `mixed`, divergência front matter/corpo) ainda não
  definido.
- **D-026** (2026-09-03, reunião com o orientador) — novo desenho de E-5/E-6
  (revisa D-019): amostra aleatória **nova** de n=100 (população em inglês
  de D-025, não os 50 casos de EXP-005), classificada independentemente por
  três LLMs (GPT-5.6 Sol, Claude Opus, Gemini 3.1 Pro); onde os três
  concordam, aceita-se o consenso; onde discordam, um humano adjudica. Isso
  reverte a restrição inegociável de D-019 (LLM/consenso não pode ser ground
  truth) — feito de forma explícita, por instrução do orientador, com riscos
  declarados (viés compartilhado entre modelos fica invisível nos casos de
  consenso; amostra não estratificada pode ter poucos casos na fronteira
  SECONDARY/MENTION).
  **Atualização (D-027/D-029):** o desenho de ensemble + adjudicação
  permanece; o que mudou foi o **esquema de classes** (`MENTION` e
  `AMBIGUOUS` deixaram de existir) e o **número de avaliadores** — o
  EXP-014 rodou com 2 (cota do Gemini esgotada), o que significa **Cohen's
  κ**, não Fleiss', e nenhuma regra de maioria: toda divergência vai ao
  humano. O risco de "poucos casos na fronteira SECONDARY/MENTION" ficou
  sem objeto: a fronteira medida como problemática foi `NONE`↔`SECONDARY`.
- **D-028 / D-030** — o que não pode ser classificado sai da **população**,
  e não vira classe: limiar de 200 caracteres (mecânico), `truncated_undecidable`
  (na anotação, com limites de Manski) e `not_an_instruction_artifact`
  (marcado, exclusão adiada até estimar a taxa no estrato F3).
- **D-031** (2026-09-13) — gold set humano feito por **dois anotadores
  independentes + reconciliação mútua**; orientador desempata. Arquivos
  individuais **não se editam** depois da conversa (só erro de marcação,
  registrado na nota); a concordância reportada é a da marcação original.

## 6. Funcionalidades / etapas concluídas

- E-0 auditoria estrutural, E-1 definição/instrumento (Codebook), E-2b candidate retrieval em inglês, E-3 distribuição de idiomas, E-3b validação de concordância entre detectores — todas com `EXP-00X` correspondente.
- EXP-005: piloto de 50 casos anotado (assistido por LLM) — golden set **operacional v1**, não o E-5 humano rigoroso.
- EXP-012 (paralelo, fora do caminho crítico): pipeline completo treino → comparação de 3 modelos → seleção → classificação em lote dos 1.877.981 conteúdos. Resultado preliminar do classificador: 1,61% `SECURITY`. Explicitamente **não é a resposta da QI-1** (ver `Decision Log#D-023`).
- **EXP-013** (2026-09-03): amostra determinística de n=100 sobre a população
  em inglês; população em inglês 1.571.243 (83,667% de 1.877.981).
  **O denominador vigente é 1.550.550** ([[EXP-016]], depois do limiar do
  D-028). Classificação por 3 LLMs sob a v2.3 — mediu κ=0,370 na
  dicotomia, o que motivou D-027.
- **EXP-014** (2026-09-04): re-teste sob a v2.4, mesma amostra, 2 avaliadores.
  **κ=0,724 (classe) e 0,672 (dicotomia)**, faixa substancial. Mediu também
  **cada dimensão separadamente**, o que produziu D-029. Em 2026-09-13:
  adjudicação humana por dois anotadores e **gold set de 99 casos** (D-031).
- **Reorganização** (2026-09-05): `notes/` reestruturado (Instruments/,
  _arquivo/, Literature/), README reescrito como ponto de entrada, Decision
  Log com índice de status. Nada apagado.

## 7. Em andamento / pendências conhecidas

> [!important] ⭐ PRÓXIMO PASSO — E-7: validar o LLM local do orientador
> Plano completo em `notes/03 - Methodology.md`, seção E-7. Em ordem:
>
> 1. **Congelar o gold set num commit** (`results/EXP-014_gold_set.csv`) antes
>    de qualquer modelo novo vê-lo. Prompt = `Classification Prompt` v2.6 **sem
>    ajuste feito com o gold set**; calibrar, se precisar, em amostra separada.
> 2. **Obter do orientador:** modelo e versão, forma de chamada (API compatível
>    com OpenAI?), hardware e throughput, temperatura 0, janela de contexto.
> 3. **Harness** `scripts/run_local_llm_classification.py`: endpoint
>    configurável, registra modelo, versão, hash do prompt e temperatura
>    (D-008), saída `.jsonl` legível por `compute_agreement.py`, retomável,
>    `ThreadPoolExecutor`, lê `EXP-013_llm_cases/` sem escrever lá, `remember`
>    desligado.
> 4. **Throughput nos 99** → projeção para 1.550.550.
> 5. **Métricas** P/R/F1 por classe e na dicotomia, com IC, e
>    `NONE`↔`SECONDARY` à parte, **separadas entre os 83 de consenso e os 16
>    humanos**.
> 6. **Pré-registrar o critério de "satisfatório"** do gate (D-024) **antes**
>    de ver as métricas. Vira entrada no Decision Log.
> 7. **Decisão de desenho para o orientador:** a prevalência preliminar é
>    ~56%, e não os ~5% que motivaram o Desenho C. Escolher entre C, amostra
>    aleatória simples expandida (~384 casos para ±5 pp) e dois estágios
>    (D-015). Rever também se o E-4 (retrieval) ainda faz sentido.

- **Gold set concluído ([[EXP-014]], [[Decision Log#D-031]], 2026-09-13).**
  Os 16 casos discordantes foram anotados por **dois pesquisadores
  independentes**, Victor e Havillon, cada um no próprio arquivo
  (`EXP-014_adjudication_victor.csv`, `_havillon.csv`). Concordância
  **10/16 (κ=0,186) na marcação original** — é a que se reporta — e 12/16
  (κ=0,458) após corrigir 2 erros de marcação (LLM083, LLM089), registrados na
  nota. Os 4 restantes (LLM029, 045, 052, 091) foram **reconciliados em
  conjunto**, todos para `NONE`; a reconciliação foi **mútua**, e não partiu de
  um anotador. Rótulo final em `EXP-014_adjudication_form.csv`.
  `scripts/build_gold_set.py` → **`EXP-014_gold_set.csv`: 99 casos no quadro**
  (LLM078 fora), 83 consenso de LLM + 16 humanos; `PRIMARY` 9 · `SECONDARY` 46
  · `NONE` 44. Marcações: LLM092 `truncated_undecidable` (os dois modelos
  marcaram, mas o consenso tinha perdido o campo); LLM019/067
  `not_an_instruction_artifact`. **Estimativa preliminar: 56,1% [46,2%;
  65,5%]**, que não é a resposta: 83 rótulos sem verificação humana.
  `compute_agreement.py` agora lê CSV humano, e `--original-marking` desfaz as
  correções registradas.
- **Quadro de análise construído ([[EXP-016]], 2026-09-05).** As exclusões
  foram aplicadas **em sequência** pela primeira vez:
  1.877.981 → (só inglês, D-025) 1.571.243 → (evidência ≥ 200, D-028)
  **1.550.550 = o denominador da QI-1**, 82,565% da base. Os marginais se
  sobrepõem — o limiar remove 25.284 isolado mas só 20.693 a mais depois do
  idioma (4.591 já tinham saído); **não somar marginais**. Estratos de gênero
  marcados dentro do quadro (D-030, não excluem): F1 1.339.453 · **F3 205.928
  (13,3%, taxa desconhecida)** · F1b 4.543 · F2 626. Teste de ponta a ponta:
  os 100 casos do EXP-014 localizados, `LLM019`/`LLM067` em F2, os 14 de
  `name` vazio em 12 F3 + 2 F2. ⚠️ **`LLM078` sai do quadro** (75 caracteres):
  o gold set efetivo tem **99 casos, não 100**.
- **Validade do quadro amostral ([[EXP-015]], 2026-09-05).** Nem todo
  `SKILL.md` é uma skill: 2 dos 100 casos da amostra são **saída gerada**
  salva com esse nome (`LLM019`, um dump de pesquisa; `LLM067`, um
  *"Feature Context"*). O limiar do D-028 não os pega — têm 15.744 e 19.445
  caracteres, e ele exclui evidência de menos, não gênero errado.
  Regra determinística testada (marcador de procedência + front matter
  inválido) acerta 2/2 nos conhecidos mas marca só **707 arquivos (0,038%)**,
  contra os ~35 mil que a amostra sugere — **recall baixo demais para servir
  de filtro**, e usá-la faria o quadro *parecer* saneado. Decisão
  ([[Decision Log#D-030]]): marcar agora com `frame_exclusion:
  not_an_instruction_artifact`, **excluir depois**, quando a taxa em F3
  (251.573 arquivos sem marcador) for estimada. Instrumentos em **v2.6**.
  ⚠️ O viés **não é conservador**: o grupo marcado tem 29,14% de vocabulário
  de segurança contra 24,93% da população com front matter válido.
- **Re-teste CONCLUÍDO ([[EXP-014]], 2026-09-04).** O Codebook v2.4 melhorou a
  confiabilidade de forma mensurável, sobre os mesmos 100 casos e os mesmos
  dois avaliadores: classe **κ=0,531 → 0,724**; dicotomia que decide a QI-1
  **κ=0,540 → 0,672** (faixa substancial). Quatro coeficientes convergem
  (Cohen, Krippendorff, Gwet AC1, Brennan-Prediger) e κ≈AC1 mostra que o
  paradoxo do kappa não distorce os dados. `PRIMARY` = **9/100 em quatro
  execuções independentes**, sob dois esquemas — bate com os 7,3% do
  *Agent Skills in the Wild*.
  **Duas ressalvas declaradas:** discordância **sistemática** persiste
  (McNemar p=0,0042, 14 contra 2 — a escolha do modelo que forma os estratos
  desloca o resultado); e houve **vazamento de cegamento por memória de
  agente** (ver §9).
- **Instrumentos da v2.5 prontos** (2026-09-05): `Codebook.md` v2.5 (D-029 —
  primeira classificação enxuta, cinco campos), `Classification Prompt.md`,
  `Guia do Anotador Humano.md` e `Taxonomy Coding Protocol.md` (etapa 2,
  **escrito mas nunca executado**). `compute_agreement.py` reporta Cohen,
  Krippendorff, Gwet AC1, Brennan-Prediger, IC bootstrap, PI/BI e McNemar.
- **Literatura organizada** (2026-09-05): `notes/Literature/` com protocolo de
  busca declarado, resultado da busca (incluindo **exclusões com motivo**) e
  12 notas de referência. `referencias.bib` na raiz com **27 entradas, todas
  com metadados de fonte autoritativa** (14 Crossref, 10 arXiv, 3 manuais).
  **Mas só 2 das 12 referências foram efetivamente lidas** — ver o campo
  `leitura:` em cada nota. É a maior dívida da seção de trabalhos
  relacionados.
- A adjudicação dos 78 casos do EXP-013 sob a v2.3 fica **cancelada** —
  seria trabalho sob um esquema substituído.
  **As saídas do EXP-013 (v2.3) foram arquivadas em `results/_arquivo/`**
  (2026-09-03), não apagadas: são a evidência empírica de D-027/D-028, a
  saída do Gemini é irrecuperável (cota esgotada), e são a linha de base
  para a comparação v2.3 → v2.4. Ver o `README.md` de lá.
- Depois: E-4 reordenado (retrieval escolhido por recall) → E-7 (classificador
  validado contra o gold set misto de D-026) → E-8 (classificação da
  população para `N_h`) → E-9 (estimativa de prevalência com IC) → E-10
  (robustez) → E-11 (consolidação).
- **D-022 — FECHADA em 2026-09-03 por [[Decision Log#D-028]]**. "Elegível" =
  `dedup_primary=1`, `content IS NOT NULL`, 100% inglês (D-025) **e**
  `length(description) + body_chars >= 200`. O corte de 200 caracteres exclui
  25.284 conteúdos (1,35%), entre eles 3.447 ponteiros de symlink. Evidência
  truncada e indecidível (≤14.157, ≤0,75%) também sai do frame, **com limites
  de Manski obrigatórios** por ser exclusão condicionada ao desfecho.
  Números vieram de consulta exploratória — precisam de script + `EXP-XXX`
  antes de ir ao TCC.
- **D-024 (2026-08-27)**: QI-2 e QI-3 deixaram de ser "extensões futuras" soltas e passaram a ter ordem formal — QI-1 → validação do classificador (gate) → QI-2 → QI-3. Nada do caminho crítico da QI-1 muda por causa disso. O gate em si (E-7) ainda não foi executado, então QI-2/QI-3 continuam não iniciadas; o limiar numérico de "validação satisfatória" é uma decisão pendente separada.
- **D-025/D-026 (2026-09-03, reunião com o orientador)**: população restrita
  a inglês; E-5/E-6 passam a usar ensemble de três LLMs com adjudicação
  humana só na discordância, sobre uma amostra nova de n=100.
  **Atualização, mesmo dia:** critério de "inglês" fixado (100%); regra de
  desempate fixada (qualquer discordância entre os três modelos, em
  qualquer dimensão, leva o caso inteiro à adjudicação humana; cegamento
  entre os três modelos confirmado como regra explícita).
  **Execução (2026-09-03):** amostra de n=100 gerada
  ([[EXP-013]], `scripts/build_llm_ensemble_sample.py`) — o filtro de
  idioma inicial (limiar de R-9) tinha uma lacuna real (não pegava mistura
  de escrita latina), corrigida na prática com detecção por parágrafo.
  Prompt reformulado para invocação via CLI de cada modelo com acesso ao
  diretório (decisão do pesquisador, não API programática) —
  [[Classification Prompt]]. Script de agregação/discordância
  escrito e testado com dados sintéticos
  (`scripts/aggregate_llm_classifications.py`).
  **Execução real concluída (2026-09-03):** GPT e Claude 100/100; Gemini
  91/100 (9 casos nunca gerados — `LLM066`-`074` — e schema truncado em
  26 dos 91, ambos por operação manual em blocos colados via CLI; **não
  preenchidos por inferência**, decisão explícita do pesquisador, para não
  quebrar a independência entre os três modelos que sustenta D-026).
  Agregador corrigido para tratar campo ausente como dado insuficiente,
  não como divergência de valor (status novo `INCOMPLETE`), e para
  excluir `possible_non_english` da comparação (nenhum dos três modelos
  preencheu esse campo obrigatório do schema — falha de conformidade
  simétrica, sem sinal de discordância). Resultado: 22 `UNANIMOUS`, 59
  `DISCORDANT`, 10 `INCOMPLETE`, 9 `MISSING` → **78 casos vão para
  adjudicação humana** (hoje em `results/_arquivo/EXP-013_adjudication_form.csv`
  — essa adjudicação foi **suspensa**, era sob a v2.3; a atual é a do EXP-014).
  **Achado relevante para o Codebook** (não decidido, registrado para o
  orientador): a discordância não é ruído disperso — é viés sistemático
  por modelo (GPT liberal em SECONDARY, Claude em MENTION, Gemini
  puxando para NONE), e 32/91 casos (35%) divergem no bucket binário
  SECURITY/NOT que decide o numerador da QI-1. Decompondo por sub-campo,
  `security_focus` concorda 95,8% mas `operational_security` só 63,9% —
  o gargalo é o critério "acionável" de R-2/R-3, não a estrutura ordinal
  PRIMARY/SECONDARY/MENTION/NONE em si (ver [[EXP-013]] para a análise
  completa). **Superado:** essa leitura levou a D-027 (Codebook v2.4) — a
  adjudicação sob a v2.3 foi suspensa; o instrumento ativo agora é
  [[Guia do Anotador Humano]].
  **Denominador da QI-1 sob o novo recorte calculado (2026-09-03,
  [[EXP-013]]): 1.571.243 de 1.877.981 (83,667%) são 100% em inglês.**
  306.738 (16,333%) ficam fora da população-alvo. Sem duplicatas. Este é
  o denominador oficial enquanto [[Decision Log#D-022]] (elegibilidade)
  seguir em aberto — se D-022 mudar o frame de partida, recalcular.
- Branch `Q1` está significativamente à frente de `main` (todo o trabalho de metodologia e o EXP-012 não estão em `main` ainda) — ver §9.

## 8. Integrações externas

- Dataset via mirror HuggingFace (`mvaccargiu/gitskills`), citado no README.
- `sentence-transformers` baixa o modelo `paraphrase-multilingual-MiniLM-L12-v2` do Hub na primeira execução (cache local do HF, fora do repo).

## 9. Limitações, riscos e informações difíceis de reconstruir só pelo código

- **`main` vs `Q1` divergem muito.** `scripts/` em `main` tem só 4 arquivos
  (download/profile/candidate-frame/languages); todo o resto (piloto E-5,
  EXP-012, Codebook v2.3, Decision Log D-005 em diante) existe **só em
  `Q1`**, ainda não mergeado. Rode `git branch --show-current` no início da
  sessão — não assuma que `main` reflete o estado real do projeto.
- **Ambiente não sobrevive a jobs longos em background.** Um job de
  classificação em lote de ~9h foi encerrado pelo ambiente após ~2h11min
  sem aviso do usuário. Jobs de inferência/treino potencialmente longos
  devem ser otimizados para rodar em menos de ~1-2h, ou quebrados em lotes
  menores/checkpointáveis.
- **`ProcessPoolExecutor` falha no Windows nativo** (Windows + `uv run`) —
  confirmado **duas vezes** com bibliotecas diferentes (`scipy`/`sklearn`
  no EXP-012; `lingua` no EXP-013), sempre `BrokenProcessPool` na
  inicialização do processo-filho via spawn. Não é peculiaridade de uma
  biblioteca — é o par spawn+`uv run` nesta máquina. **No WSL/Linux
  funciona** (fork, não spawn) e dá paralelismo real (~5,2x medido) — mas
  o **WSL nesta máquina teve instabilidade própria** durante a execução
  em escala de [[EXP-013]] (o serviço quebrou duas vezes com
  `Wsl/Service/E_UNEXPECTED`, e um processo foi encerrado pelo ambiente
  com SIGKILL depois de ~40 min, mesmo padrão do incidente de EXP-012 mas
  bem mais cedo) — `wsl --shutdown` seguido de nova chamada recuperou o
  serviço nas duas vezes, sem perda de progresso graças ao desenho
  retomável. Nenhuma das duas plataformas é totalmente confiável sozinha
  para jobs longos aqui; **`ThreadPoolExecutor`** (Windows, ~1,8x com
  12–16 threads quando a biblioteca libera o GIL) é a opção mais estável,
  mesmo sendo mais lenta — bom fallback se o WSL travar de novo.
- **O plugin `remember` é um vetor de vazamento de cegamento.** No
  [[EXP-014]] ele injetou, no início da sessão de um dos avaliadores,
  achados da análise anterior — inclusive **a direção do viés do outro
  avaliador**. Não houve leitura de arquivo de output, mas os avaliadores
  ficaram em condições não equivalentes. A injeção **não deixa rastro na
  saída**, então isso se repete em silêncio em qualquer rodada cega futura
  (E-5, E-6, adjudicação, validação do classificador) a menos que o plugin
  seja **desativado explicitamente antes**. Registrar como limitação sempre
  que não for possível desativar.
- **Não escrever saída dentro de `results/EXP-013_llm_cases/`.** O prompt de
  classificação manda o modelo ler tudo daquele diretório; um arquivo de
  output ali dentro fica visível para o avaliador seguinte. Aconteceu no
  EXP-014 (`classifications.jsonl`), sem consequência verificada, mas é
  armadilha ativa.
- **`uv run` falha em silêncio nesta máquina** (exit 120, sem saída
  nenhuma). Os scripts do caminho crítico usam só stdlib — rodar
  `python script.py` direto. `uv run` só quando houver dependência real
  (duckdb, lingua).
- **Busca bibliográfica por título produz falso positivo.** Aconteceu aqui:
  *"Learning from Disagreement: A Survey"* casou com um artigo de economia
  no SSRN, só pela palavra "disagreement" — teria entrado no TCC como
  citação fabricada **com DOI real de outro artigo**. Resolvido com guarda
  de similaridade Jaccard ≥ 0,60 mais inspeção manual. **Nenhuma ferramenta
  é imune, nem MCP** — o que protege é conferir o título devolvido.
- **`models/security_classifier_v1_metadata.json`** tem o campo
  `golden_set_commit` como `null` — nunca foi preenchido com o hash do
  commit de freeze do golden set (`a90ce04...`). Gap de rastreabilidade
  conhecido, não corrigido.
- **A skill `.claude/skills/project-context/SKILL.md` está desatualizada**
  (datada de 2026-08-22, "Estado atual" não reflete D-011 em diante, Desenho
  C, EXP-003/004/005/012 nem a existência da branch `Q1`). Ela continua
  correta quanto às armadilhas estruturais do dataset (unidade de análise,
  `head(n)` enviesado, keyword ≠ classificador), mas não é o retrato mais
  recente do projeto — prefira `notes/00 - Research Overview.md` e este
  arquivo para o estado atual, e considere atualizar a skill quando o
  próximo marco fechar.
- **Armadilhas do dataset** (D-001, D-002) continuam válidas e são a causa
  raiz do resultado do notebook legado ter sido invalidado — não usar
  `head(n)`/`LIMIT` sem `ORDER BY` determinístico como amostra; já
  aconteceu duas vezes neste projeto (notebook legado e um benchmark do
  EXP-012) com o mesmo padrão de erro.

## Ligações

`README.md` · `notes/Decisions/Decision Log.md` · `notes/03 - Methodology.md` ·
`.claude/skills/project-context/SKILL.md` · `.claude/skills/security-analysis/SKILL.md` ·
`.claude/skills/data-analysis/SKILL.md`
