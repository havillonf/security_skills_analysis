---
tipo: codebook
version: 2.6
data: 2026-09-05
substitui: v2.5 (2026-09-04)
decisoes: D-004, D-006, D-013, D-014, D-016, D-022, D-025, D-027, D-028, D-029, D-030, D-031
status: classe validada no EXP-014; concordância humana medida (§8.4); etapa 2 (§5) ainda não testada
---

# Codebook — Classificação de Security Skills

Instrumento canônico de anotação. Definição, classes e dimensões fornecidas pelo
pesquisador; operacionalização e âncoras derivadas dos dados.

> [!success] Confiabilidade medida — [[EXP-014]], 2 avaliadores, n=100
> A decisão de classe (§3–§4) foi testada e **melhorou de forma mensurável**
> em relação à v2.3, sobre os mesmos 100 casos e os mesmos dois avaliadores:
>
> | | v2.3 | **v2.4/v2.5** |
> |---|---|---|
> | Classe | κ=0,531 | **κ=0,724** · α=0,722 · AC1=0,776 |
> | Dicotomia Security/não (decide a QI-1) | κ=0,540 | **κ=0,672** · α=0,668 · AC1=0,692 |
>
> Faixa **substancial** (Landis & Koch), com os quatro coeficientes
> convergindo — κ e AC1 quase colados indicam que o paradoxo do kappa não
> distorce estes dados.
>
> **Nem a v2.5 nem a v2.6 alteram a decisão de classe** (R-1…R-8 intactas) —
> a v2.5 mexe no payload descritivo, a v2.6 acrescenta uma exclusão de frame.
> Por isso estes números **transferem** da v2.4 para a v2.6.
> O que ainda **não** foi medido é a etapa 2 (§5).

> [!warning] Duas ressalvas do EXP-014, declaradas
> 1. **Discordância sistemática persiste.** McNemar p=0,0042 (14 casos contra
>    2): um avaliador é consistentemente mais inclusivo. A mudança de esquema
>    melhorou a concordância mas **não eliminou o viés direcional**.
> 2. **Vazamento de cegamento por memória de agente.** A sessão de um dos
>    avaliadores recebeu, via plugin de memória, achados da análise da v2.3 —
>    incluindo a direção do viés do outro avaliador. Não houve leitura de
>    output, mas os avaliadores **não estavam em condições equivalentes**. Ver
>    [[EXP-014]] para a avaliação de magnitude.

> [!warning] Histórico de versões
> **v2.0** ([[Decision Log#D-006]]): renomeou `NON-SEC` → `NONE`, acrescentou
> `AMBIGUOUS`, separou dimensões colapsadas na v1.0.
> **v2.1** ([[Decision Log#D-012]]): idioma deixa de ser caso de `AMBIGUOUS`;
> acrescenta R-9, `language`, `used_translation`.
> **v2.2** ([[Decision Log#D-016]], [[Decision Log#D-014]]): operacionaliza
> `mixed`, acrescenta R-10 (escopo de GRC).
> **v2.3** ([[Decision Log#D-021]]): remove âncoras de `AMBIGUOUS` justificadas
> por barreira de idioma; acrescenta regra de cegamento.
> **v2.4** ([[Decision Log#D-027]], [[Decision Log#D-028]]): **remove `MENTION`
> e `AMBIGUOUS` como classes.** Três classes: `PRIMARY`, `SECONDARY`, `NONE`.
> Reformula a decisão de classe na linguagem de papel profissional. `SECONDARY`
> passa a ser deliberadamente inclusivo, com subclassificação **posterior** por
> open coding. Evidência insuficiente vira **exclusão de frame**, não classe.
> **v2.5** ([[Decision Log#D-029]]): **enxuga a primeira classificação para
> cinco campos** (§2.1) com base na medição do [[EXP-014]]. Remove
> `security_focus` (redundância pura: 100/100 igual a `classe == PRIMARY`),
> `security_functions` (derivada do NIST CSF — circularidade com a QI-2; migra
> para a QI-3), `operational_security` e `operation_level` (κ=0,511 e 0,446,
> sobrepostas), `grc_case`, `security_concerns` e `operational_capability`
> (vocabulário livre normalizado cedo demais). Promove a `note` a campo
> estruturado em prosa (§2.3), insumo primário do open coding. **Não altera a
> decisão de classe.**
>
> **v2.6** ([[Decision Log#D-030]]): terceiro valor de `frame_exclusion`,
> `not_an_instruction_artifact` — o arquivo é saída gerada, não instrução.
> Marcado agora, **excluído depois**, quando a taxa for estimada ([[EXP-015]]).
> Não toca na decisão de classe.

---

## 1. Definição

> **Security Skill:** uma Agent Skill cujo **propósito principal**, ou **parte de
> seu comportamento descrito**, envolve prevenir, detectar, analisar, avaliar,
> explorar, mitigar ou responder a ameaças, vulnerabilidades, violações de
> propriedades de segurança ou controles de acesso em sistemas computacionais.

Presença de vocabulário de segurança **nunca** basta. A classificação considera
propósito declarado, comportamento, atividade orientada ou executada, resultado
esperado, contexto e artefatos associados.

A inclusão de "explorar" torna a definição neutra quanto à postura: pentest,
exploit dev e CTF são Security Skills tanto quanto um scanner defensivo. Postura
é dimensão descritiva, **nunca** critério de inclusão nem juízo de malícia.

**`PRIMARY` + `SECONDARY` = Security Skill.** A classe distingue **se segurança é
o foco**, não *se conta*.

### 1.1 Unidade de análise

Um **conteúdo distinto** (`dedup_primary = 1`). Ver [[Decision Log#D-001]].
Anota-se o `SKILL.md`; artefatos associados (`artifact_siblings`) entram quando
necessários para determinar a capacidade real (R-6).

### 1.2 População e exclusões de frame

Sob [[Decision Log#D-025]] a população-alvo é restrita a skills **100% em
inglês** — 1.571.243 de 1.877.981 (83,667%), medido em [[EXP-013]].

**Três** exclusões acontecem **antes** da classificação, no frame, nunca como
classe ([[Decision Log#D-028]], [[Decision Log#D-030]]):

| Exclusão | Critério | Natureza |
|---|---|---|
| **Sem evidência classificável** | `length(description) + body_chars < 200` | Mecânica — contagem de caracteres, sem julgamento |
| **Evidência truncada com dúvida** | Script referenciado e não recuperado (`composition_truncated = 1`), **e** o texto restante não permite decidir se há consideração de segurança | Julgamento — registrar `file_sha` e motivo |
| **Não é arquivo de instrução** | O arquivo é registro ou saída produzida por algum processo — relatório, log, dump, documento de contexto gerado — e não instruções dirigidas a um executor | Julgamento — marcar `not_an_instruction_artifact` |

> [!note] A terceira exclusão é marcada agora e **aplicada depois**
> O anotador marca; a remoção da população aguarda a estimativa da taxa
> ([[Decision Log#D-030]], [[EXP-015]]). Marcar custa uma coluna que já existe;
> não marcar custa reler a amostra quando a decisão vier.
>
> **`name` nulo não é critério.** Dos 14 casos de `name` nulo na amostra do
> [[EXP-014]], **12 são skills legítimas** com front matter fora da spec — em
> `LLM060` o front matter está intacto quatro linhas abaixo do cabeçalho vazio.
> Julgue o **conteúdo**, nunca o metadado ausente.
>
> Diferente da exclusão por truncamento, esta **não depende do desfecho**:
> decidir "instrução ou saída?" não exige decidir se há segurança, então não
> requer limites de Manski.

> [!important] A segunda exclusão depende do desfecho — precisa de limites
> Excluir unidades com base em dúvida **sobre a própria variável que se está
> estimando** enviesa a estimativa em direção desconhecida. Obrigatório:
> reportar a prevalência como **intervalo**, calculado assumindo que todos os
> excluídos são Security Skill e que nenhum é (limites de Manski). O universo
> possível é pequeno — 14.157 conteúdos (0,75%) têm script **e** composição
> truncada — então o intervalo deve sair estreito, o que **demonstra** que a
> exclusão foi inofensiva em vez de assumir.

Script ausente **não muda a classe** e **não força `SECONDARY`**: se a descrição
já revela o comportamento, classifique normalmente com `confidence` mais baixa.

---

## 2. Dimensões

O instrumento tem **duas etapas**, e cada dimensão pertence a uma delas. A
primeira classificação é deliberadamente enxuta; a riqueza descritiva fica na
reclassificação taxonômica (§5), que relê os casos de qualquer forma.

### 2.1 Primeira classificação — cinco campos

| Campo | Valores | Papel |
|---|---|---|
| `security_relevance` | PRIMARY · SECONDARY · NONE | **O desfecho.** κ=0,724 no [[EXP-014]] |
| `evidence` | description · body · bundled_artifacts (multi) | Torna executável "nunca classifique sem citar evidência". Jaccard 0,788 |
| `frame_exclusion` | "" · truncated_undecidable · not_an_instruction_artifact | Exigido por [[Decision Log#D-028]] e [[Decision Log#D-030]] |
| `note` | texto | **Insumo do open coding (§5).** Ver §2.3 |
| `confidence` | high · medium · low | **Metadado de triagem, não medida.** κ=0,177 |

### 2.2 Dimensões removidas da primeira classificação (D-029)

Medidas no [[EXP-014]] e retiradas por redundância, sobreposição ou risco de
circularidade — **não** por serem desinteressantes:

| Removida | κ / Jaccard | Motivo |
|---|---|---|
| `security_focus` | κ=1,000 | **Redundância pura.** Em 100/100 casos, nos dois avaliadores, `security_focus` == (`security_relevance` == `PRIMARY`). Não é dimensão independente, é a classe reescrita. Se necessária, **derive**, não anote |
| `security_functions` | Jaccard 0,784 | `PREVENT·DETECT·ASSESS·TEST·RESPOND·RECOVER` é derivado do **NIST CSF**. Coletá-lo aqui e alimentar o open coding é a circularidade que a regra inegociável da QI-2 proíbe. **Migra para a QI-3 (crosswalk)**, depois da taxonomia estabilizada |
| `operational_security` | κ=0,511 | Sobrepõe `operation_level` (coincide em 78%/71% dos casos). Se voltar, volta **fundida numa dimensão só** |
| `operation_level` | κ=0,446 · p_o=61% | A pior medida do instrumento. 61% de concordância bruta não sustenta afirmação de tese |
| `grc_case` | κ=0,852 | Confiável, mas 3–4 positivos em 100 e duplica o R-10, que já é regra de decisão |
| `security_concerns` | Jaccard 0,368 | Vocabulário livre normalizado **cedo demais**: nos casos LLM001 e LLM003 a interseção entre avaliadores é **vazia** embora as notas descrevam a mesma coisa. É sinonímia, não discordância. Vai para §5 |
| `operational_capability` | Jaccard 0,348 | Mesma razão |
| `rule_applied` | κ=0,307 | Trilha de auditoria útil, mas não é medida. Opcional |

### 2.3 O que a `note` precisa conter

A `note` deixa de ser justificativa livre e passa a ser **campo estruturado em
prosa**, porque é ela que sustenta o open coding da §5. Três elementos
obrigatórios:

1. **O papel profissional** — *"seria um analista de malware"*, *"seria um
   designer gráfico"*.
2. **Qual é o conteúdo de segurança**, em termos próximos ao texto observado —
   ou, se `NONE`, **por que não conta** (homônimo de palavra? de conceito?
   objeto não computacional? só etiqueta?).
3. **O elemento concreto** que sustenta isso — o trecho, o comando, a seção.

> [!example] Nota que cumpre os três, do [[EXP-014]]
> `LLM001` → *"Designer gráfico usando Adobe Express: o propósito é criar
> peças visuais, mas o texto manda remover PII das queries e refazer o OAuth
> em 401."*
>
> `LLM004` → *"Neurocientista fazendo medição: validar entradas aqui protege
> validade científica, não um sistema computacional."* — o motivo da exclusão
> fica auditável contra R-5.

> [!warning] `confidence` não é medida
> κ=0,177 no [[EXP-014]] (κ=0,070 na v2.3). Serve para você **priorizar a
> adjudicação**, nunca para decidir discordância nem entrar em cálculo de
> concordância.

---

## 3. `security_relevance` — as três classes

A decisão de classe é feita por **analogia de papel profissional**: *se esta
skill fosse uma pessoa, qual seria a profissão dela, e o que ela faria a respeito
de segurança?*

| Classe | Analogia | Significado |
|---|---|---|
| `PRIMARY` | Um profissional de cibersegurança | Segurança é o propósito da skill. Ela existe para isso. |
| `SECONDARY` | Um dev de outra especialidade cujo texto traz consideração de segurança | Há consideração de segurança, mas o propósito da skill é outro. |
| `NONE` | Alguém cujo trabalho não toca segurança em ponto algum | Nenhuma consideração de segurança. |

**`PRIMARY` e `SECONDARY` são ambas Security Skill.** A distinção entre elas é
sobre **foco**, não sobre pertencimento.

> [!important] `SECONDARY` é deliberadamente inclusivo
> `SECONDARY` é um **balde de coleta**, não um juízo de substancialidade. A
> pergunta é de **presença** ("há alguma consideração de segurança?"), não de
> **grau** ("é substancial o bastante?"). A pergunta de grau foi a que mediu
> κ=0,298 na v2.3 e foi deliberadamente removida do caminho crítico.
>
> A granularidade vem depois, por **subclassificação via open coding sobre
> `PRIMARY` e `SECONDARY`** (§5) — não por julgamento na hora da anotação.

### 3.1 O que conta como consideração de segurança

**Conta** (→ no mínimo `SECONDARY`):

- restrição de comportamento de agente — read-only, "não altere sem permissão",
  "não commite", escopo de ferramenta, sandbox, least privilege;
- configuração protetiva — `chmod` em arquivo de chave, permissões de arquivo,
  gestão de secrets, `.gitignore` de credencial;
- implementação de controle de acesso — login, JWT, RBAC, OAuth, sessão;
- teste, análise ou defesa contra ameaça nomeada — SQL injection, XSS, CSRF,
  prompt injection, CVE, malware;
- qualquer menção a ameaça, vulnerabilidade, ataque ou incidente.

**Não conta** (→ `NONE`):

- casamento apenas em `tags`/`category`/nome de arquivo (R-4);
- homônimo de palavra ou de conceito (R-5);
- GRC puramente organizacional, sem objeto computacional (R-10);
- restrição de comportamento cujo objeto não é computacional — limite de gasto,
  segurança clínica, política de conteúdo.

### 3.2 Nota histórica sobre `security_focus`

Até a v2.4 o instrumento registrava `security_focus` como dimensão
independente, e a v2.3 reportou **κ=0,942** para ela — o número mais citado do
projeto, tratado como "a medida mais confiável do instrumento".

O [[EXP-014]] mostrou que essa leitura estava errada: em **100/100 casos, nos
dois avaliadores**, `security_focus` é exatamente `security_relevance ==
PRIMARY`. Não era uma dimensão medindo bem — era **a classe medida duas vezes**.

Isso não invalida nada do que foi concluído (a estabilidade de `PRIMARY` é real
e se confirmou em quatro execuções independentes, sempre 9/100 no EXP-014), mas
corrige o que o número significa: **é a confiabilidade de `PRIMARY`, não de uma
dimensão separada.** Onde `security_focus` for necessário para análise, derive
da classe — não peça ao anotador.

---

## 4. Regras de decisão

Aplicar em ordem; parar na primeira que decidir.

**R-1 — Teste do papel profissional.** *Se esta skill fosse uma pessoa, qual
seria a profissão dela?*
Profissional de cibersegurança → `PRIMARY`.
Outra profissão, mas o texto traz consideração de segurança (§3.1) → `SECONDARY`.
Outra profissão, sem nenhuma consideração de segurança → `NONE`.

**R-2 — Teste de presença.** Para separar `SECONDARY` de `NONE`, a pergunta é
**existe consideração de segurança?**, não *é substancial?*. Use a lista de §3.1.
Na dúvida entre `SECONDARY` e `NONE`, prefira `SECONDARY` com `confidence: low` —
o open coding posterior separa o que for marginal. *(Inverte a orientação da
v2.3, que mandava preferir a classe mais baixa: sob o desenho de dois estágios, o
custo de incluir demais é recuperável, o de excluir demais não.)*

**R-3 — Teste de foco.** Para separar `PRIMARY` de `SECONDARY`: segurança
organiza a skill e as demais dimensões são subordinadas → `PRIMARY`. Segurança é
uma entre várias dimensões, ou aparece dentro de um objetivo maior → `SECONDARY`.
Proporção textual isolada não decide: scanner curto é `PRIMARY`; skill longa com
um parágrafo de segurança é `SECONDARY`.

**R-4 — Locus da evidência.** Casamento apenas em `tags`, `category`, nome de
arquivo ou lista de "related skills" **não** conta como conteúdo de segurança.
*Caso real:* `go-playwright-v2` traz `category: testing-security` e é automação
de browser → `NONE`.

**R-5 — Homônimos.** Termo de segurança em sentido não-securitário não conta.
- **De palavra:** `meta-ads-audit` ("audit" = auditoria de anúncios) → `NONE`;
  `token` como token de LLM; `permission` como permissão de UX.
- **De conceito:** *safety* ≠ *security*; guardrail de qualidade ≠ guardrail de
  segurança; limite de gasto ≠ controle de acesso. Decide-se pelo **objeto
  protegido**: precisa ser sistema computacional.

**R-6 — Artefatos associados.** Se `has_scripts = 1` e o script executa função de
segurança que o `SKILL.md` mal menciona, classifique pelo **comportamento
operacional conjunto**; marque `evidence: bundled_artifacts`. Se o script for
necessário e não estiver disponível (`composition_truncated = 1`): classifique
pela evidência restante com `confidence: low`; **só se o texto restante não
permitir decidir**, exclua do frame (§1.2) registrando `file_sha` e motivo.

**R-7 — Objeto protegido não restringe a classe.** Vale para código produzido,
infraestrutura, agente/harness ou a própria skill — desde que **computacional**.
Registrar como `security_concern`, não na classe.

**R-9 — Idioma.** Sob [[Decision Log#D-025]] a população é restrita a inglês, mas
a regra permanece para casos `mixed` e termos técnicos embutidos: idioma **nunca**
decide a classe, e nunca é motivo de exclusão na anotação (é critério de frame,
aplicado antes). Termos técnicos de segurança em inglês dentro de texto em outro
idioma são evidência válida.

**R-10 — Escopo de GRC.** Governança, risco e conformidade entram **apenas quando
a atividade incide sobre propriedades de segurança de sistemas computacionais**
([[Decision Log#D-016]]).
*Dentro:* auditoria de IAM, revisão de política de acesso, least privilege,
mapeamento de controles técnicos, avaliação de risco de dependência,
conformidade que **inspeciona configuração ou código**.
*Fora:* questionário de fornecedor contratual, conformidade regulatória sem
objeto computacional, gestão de risco corporativo, política como documento —
`NONE`, não `SECONDARY`.

**R-11 — Cegamento.** O anotador **não vê** o sinal preliminar de triagem (tier,
densidade de keyword, flags, grupo linguístico, motivo da seleção) antes ou
durante a anotação, nem a resposta de qualquer modelo. Ver [[Decision Log#D-021]].

**R-8 — Fechamento (aplicar por último).** Não existe mais classe de dúvida.
- Evidência suficiente, limite discutível → `SECONDARY`, `confidence: low` (R-2).
- Evidência insuficiente para decidir → **exclusão de frame** (§1.2), nunca uma
  classe.

> Ordem: **R-11** (antes de começar) → **R-1 … R-3** (classe) → **R-4 … R-7**
> (evidência e escopo) → **R-9, R-10** (idioma e GRC) → **R-8** (fechamento).

---

## 5. Subclassificação — posterior, por open coding

`PRIMARY` e `SECONDARY` **não têm subclasses definidas a priori**. Depois de
classificado, todo o conjunto `PRIMARY` ∪ `SECONDARY` passa por **open coding**
sobre o contexto e as justificativas, e as categorias emergem dos padrões
observados.

> [!danger] Regra inegociável da QI-2
> **Nunca usar referencial externo (OWASP, MITRE, NIST, ou a taxonomia de
> qualquer artigo) para construir as subclasses.** Isso cria circularidade —
> encontra-se o que se foi procurar. Referenciais externos entram **depois** da
> taxonomia estabilizada, para crosswalk e QI-3.

### 5.1 Insumo: a `note`, não campos de vocabulário livre

O insumo primário do open coding é o **conjunto das `note`** dos casos
`PRIMARY` ∪ `SECONDARY` (§2.3), lido **em bloco**, não caso a caso.

Motivo, medido no [[EXP-014]]: pedir ao anotador que normalize o vocabulário
na hora da anotação **não funciona**. Em `LLM003` os dois avaliadores
produziram `security_concerns` com **interseção vazia**
(`agent_guardrails`/`agent_least_privilege`/`bounded_autonomy` contra
`agent_autonomy_constraints`/`least_privilege`/`untrusted_agent_output`),
enquanto as notas descreviam a mesma coisa de forma reconhecível. Jaccard
médio: 0,368. **Isso é sinonímia, não discordância** — e é o sintoma de fazer
open coding cedo demais, um caso por vez, sem ver o conjunto.

A categoria emergente já está na nota, em linguagem natural, só não
normalizada. Normalizar é trabalho da §5, com o corpus inteiro à vista.

### 5.2 Dimensões descritivas: só depois, e retrabalhadas

`operational_security` e `operation_level` **não voltam como estavam**
(κ=0,511 e 0,446, com 78%/71% de sobreposição entre si). Se forem necessárias,
voltam **fundidas numa única dimensão**, com definição nova e medição de
confiabilidade própria.

`security_functions` **não entra aqui em hipótese alguma** — é derivada do NIST
CSF, e importá-la durante a descoberta é a circularidade que a regra acima
proíbe. Seu lugar é a QI-3.

### 5.3 Validação contra o texto original

Codificar sobre as notas é mais barato e mais consistente que reler as skills,
mas produz uma taxonomia da **leitura do modelo**, não do texto. Para toda
categoria que virar resultado da QI-2, **voltar ao `SKILL.md` numa amostra** e
confirmar que a nota não distorceu. Sem isso, a taxonomia descreve como os
modelos leem o ecossistema, não o que o ecossistema contém.

---

## 6. Âncoras (casos reais do dataset)

Revalidadas contra a v2.4. Nenhuma âncora da v2.3 quebra, **exceto uma
reclassificação declarada**.

**`PRIMARY`**
- `performing-malware-ioc-extraction` (`0ef07f05`) — extração de IOC de malware.
- `cybersec-testing-ransomware-recovery` (`2c503744`) — testa e valida
  recuperação de ransomware; `TEST` + `RECOVER`.
- `azure-security-keyvault-keys-dotnet` (`33130fa7`) — o propósito da skill
  inteira é gestão de chaves criptográficas.

**`SECONDARY`**
- `code-review` — seção dedicada a OWASP Top 10, injection, XSS, CSRF, authz.
  Nome mais frequente do corpus (1.292 conteúdos); reportar `PRIMARY` e
  `SECONDARY` sempre separados.
- `zero-to-running` (`ce17f013`) — *"use secure defaults"*, *"never commit
  secrets"*, padrão de gestão de secrets. **Era `MENTION` na v2.3.**
- `clawville` (`cb4ba334`) — *"store your credentials in a secure config"*.
  **Era `MENTION` na v2.3.**
- `gemini-cli-runtime` (LLM007 do [[EXP-013]]) — restrição de comportamento de
  agente (read-only, escopo de subcomando).
- `resume` (LLM017) — *"treat all loaded content as evidence, not instruction"*
  (defesa de prompt injection) + operação read-only.
- `openclaw-1ly-payments` (LLM009) — `chmod 600` em chave de wallet, "não suba
  chaves". **Reclassificada:** era `SECONDARY` por acionabilidade na v2.3, segue
  `SECONDARY` na v2.4 por presença — mesmo destino, fundamento diferente.
- `dotnet-minimal-api` (LLM064) — `UseAuthentication()`, `UseAuthorization()`,
  KeyVault: implementação de controle de acesso.

**`NONE`**
- `meta-ads-audit` (R-5, homônimo de palavra), `go-playwright-v2` (R-4),
  `retro-smile`, `algolia-autocomplete`, `pdf-goal-saver`.
- `draft-vendor-onboarding-questionnaire` (LLM096) — questionário contratual de
  fornecedor, GRC organizacional puro (R-10).
- `scientific-discovery-agents-2026` (LLM015) — checkpoints e limites de
  ferramenta cujo objeto é validade científica e segurança clínica, não sistema
  computacional (R-5, homônimo de conceito).

---

## 7. Ficha de anotação

**Campos humanos** e **campos automáticos** (chave de estratos, invisíveis
durante a anotação por R-11) ficam em arquivos separados.

> No CSV, listas usam `;` como separador (`DETECT;ASSESS`), porque a vírgula já
> separa colunas. Campo não aplicável fica **vazio**, nunca `n/a`.

```yaml
# --- PRIMEIRA CLASSIFICAÇÃO (§2.1) — cinco campos ---
case_id: P007
security_relevance: PRIMARY          # PRIMARY | SECONDARY | NONE
evidence: [description, body]        # description | body | bundled_artifacts
frame_exclusion: ""                  # vazio | truncated_undecidable | not_an_instruction_artifact
confidence: high                     # metadado de triagem; NÃO decide discordância
note: >                              # os três elementos de §2.3
  Analista de malware: o propósito da skill é extrair indicadores de
  comprometimento; a seção "IOC extraction" prescreve YARA e saída em STIX 2.1.

# opcionais, para instrumentação do piloto (não são medidas)
rule_applied: R-1
annotation_seconds: 145
difficulty: medium
```

Campos removidos em v2.5 e **por que** estão em §2.2. Se algum for necessário
para análise, derive (caso de `security_focus`) ou colete na §5 — não
reintroduza na primeira classificação sem medir a confiabilidade de novo.

---

## 8. Confiabilidade

`security_relevance` tem três níveis, dois dos quais (`PRIMARY`, `SECONDARY`)
compõem o mesmo desfecho binário.

### 8.1 Coeficientes a reportar — todos, não um

Nenhum coeficiente é suficiente sozinho, e cada um falha de um jeito diferente.
**Reportar os quatro e mostrar que convergem** é argumento mais forte que
qualquer um isolado, e blinda contra "por que você escolheu justo esse?".
Implementado em `scripts/compute_agreement.py`.

| Coeficiente | Por que entra |
|---|---|
| Concordância bruta `p_o` | Kappa é ininterpretável sem ela (Feinstein & Cicchetti 1990). Nunca sozinha |
| **Cohen's κ** | Padrão de facto para dois avaliadores nominais |
| **Krippendorff's α** | Padrão-ouro da análise de conteúdo; generaliza para n avaliadores, dados faltantes e níveis de medida |
| **Gwet's AC1** | Robusto ao *paradoxo do kappa*. Quando κ e AC1 divergem muito, a diferença **é** o diagnóstico |
| Brennan-Prediger | Correção por acaso uniforme; robusta a prevalência |

Sempre com **IC95 por bootstrap** sobre as unidades (Zapf et al. 2016).

Diagnóstico obrigatório junto: **índice de prevalência e índice de viés**
(Byrt, Bishop & Carlin 1993), que explicam *por que* κ está deprimido quando
estiver.

### 8.2 Teste de discordância sistemática

Coeficientes de concordância não distinguem discordância **simétrica** de
**direcional**. Rodar **McNemar** sobre a dicotomia: se p < 0,05, um avaliador
sobe consistentemente, e isso precisa entrar na análise de sensibilidade —
a escolha do modelo que forma os estratos desloca o resultado de forma
sistemática, não aleatória.

Medido no [[EXP-014]]: **p = 0,0042**, 14 casos contra 2. O viés direcional
sobreviveu à mudança de esquema.

### 8.3 Regras fixas

- Com **dois** avaliadores, Cohen's κ; com três ou mais, Fleiss'.
- Multi-label → Krippendorff's α para nominais multi-valorados ou Jaccard
  médio; kappa não se aplica.
- **`confidence` e `rule_applied` ficam fora** de qualquer cálculo de
  concordância e de qualquer gatilho de adjudicação (κ=0,177 e 0,307 no
  [[EXP-014]] — metadados, não classificação).
- **A adjudicação da primeira classificação considera apenas
  `security_relevance`.** As dimensões de apoio não disparam revisão humana.
- Anotador único é ameaça à validade que **deve** ser declarada. LLM **não** é
  ground truth ([[Decision Log#D-008]]).

### 8.4 Concordância humana medida — [[EXP-014]], [[Decision Log#D-031]]

Dois anotadores humanos independentes nos 16 casos em que os modelos
discordaram:

| | Concordância | Cohen's κ (IC95) | Gwet AC1 |
|---|---|---|---|
| Marcação original | 10/16 | 0,186 [−0,23; 0,61] | 0,343 |
| Após corrigir 2 erros de marcação | 12/16 | 0,458 [0,00; 0,86] | 0,562 |

Não se compara com o κ dos modelos: n=16 e **só os casos difíceis**. As
divergências caíram em duas regras: restrição imposta ao agente, e
"qualidade ≠ segurança" (§3). Na reconciliação, a pergunta que decidiu foi se a
restrição ou a verificação **existe para proteger alguma coisa ou só para o
trabalho sair certo**. Exemplos no [[Guia do Anotador Humano]] §9.

O rótulo final alimenta o **gold set de 99 casos**
(`results/EXP-014_gold_set.csv`): 83 de consenso entre modelos e 16 decididos
por humanos.

---

## 9. Limites conhecidos

- **A confiabilidade desta versão é desconhecida.** Ver o aviso do topo. Os
  números que existem são da v2.3 e não transferem.
- **`SECONDARY` inclusivo infla o numerador.** Aceitar qualquer consideração de
  segurança faz a prevalência subir muito — os anchors medidos vão de 34% (leitura
  inclusiva do GPT no [[EXP-013]]) a 78,69% (alcance da recuperação ampla por
  keyword, [[EXP-002]]). O relato **deve** ser em dois níveis: quantas contêm
  alguma consideração de segurança, e quantas existem para fazer segurança. Um
  número único aqui é indefensável.
- **A fronteira `NONE`/`SECONDARY` é agora a crítica.** Deixou de ser sobre grau
  e passou a ser sobre presença, o que deve ajudar — mas não foi medido.
- **Excluir por evidência truncada depende do desfecho.** Mitigado por limites de
  Manski (§1.2), não eliminado.
- **Não mede a segurança *da* skill.** Uma skill `NONE` que declara
  `allowed-tools: Bash(*)` é altamente relevante para segurança e continua
  `NONE`. Eixo ortogonal — [[Decision Log#D-007]]. **Nunca use o eixo B para
  decidir a classe.**
- **Escala:** 1,9M conteúdos não são anotáveis à mão. Este codebook produz o
  padrão-ouro; aplicação em escala exige classificador validado contra ele, e
  **a contagem do classificador nunca é a prevalência** ([[Decision Log#D-014]]).

## Ligações

[[Decision Log]] · [[QI-1 Methodology]] · [[QI-2 Methodology]] ·
[[QI-3 Coverage Methodology]] · [[EXP-013]] ·
[[Classification and Sampling Precedents]] · [[01 - Research Question]]
