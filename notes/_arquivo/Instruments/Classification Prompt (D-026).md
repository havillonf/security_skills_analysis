---
tipo: instrumento
questao: QI-1
data: 2026-09-03
decisoes: D-025, D-026, D-021, D-008
status: proposto — não testado contra nenhum caso real
---

# Prompt de classificação por ensemble de LLMs (D-026)

Instrumento operacional que implementa, para os três classificadores de
[[Decision Log#D-026]] (GPT-5.6 Sol, Claude Opus, Gemini 3.1 Pro), a mesma
tarefa que um anotador humano executaria sob o [[Codebook]] v2.3. **Um único
texto de instrução**, enviado da mesma forma aos três modelos — a
comparação entre eles só faz sentido metodológico se a tarefa apresentada
for idêntica.

> [!warning] Não testado
> Este prompt não foi executado contra nenhum caso real ainda. Antes de
> rodar os 100 casos de [[EXP-013]], validar contra os exemplos few-shot
> abaixo e contra alguns casos reais adicionais, comparando a saída com o
> julgamento esperado.

> [!important] Modo de invocação: CLI com acesso ao diretório (revisado em 2026-09-03)
> Decisão operacional do pesquisador: os três modelos serão chamados
> **via CLI própria de cada um** (não via API programática), com acesso de
> leitura ao diretório `results/EXP-013_llm_cases/` — não via chamadas de
> API repetidas com `{{case_id}}` substituído por vez. Isso muda duas
> coisas em relação à primeira versão deste documento: (1) a tarefa passa
> a ser "processe todo o diretório", não "classifique este caso único";
> (2) o mecanismo nativo de Structured Outputs de cada API (que as três
> documentações recomendavam — §1) **não está disponível** por esse
> caminho, então o formato de saída depende inteiramente de instrução de
> texto, compensada por regras de formato explícitas e autovalidação
> (§4). Isso é uma troca deliberada (praticidade de não gerenciar chave de
> API por precisão de um schema aplicado no servidor) — declarada aqui,
> não escondida.

---

## 1. Fontes consultadas e o que cada uma sustenta nesta síntese

Documentação oficial lida em 2026-09-03, com o que efetivamente motivou
cada escolha de desenho abaixo (sem inventar prática não documentada):

| Fonte | O que sustenta |
|---|---|
| Anthropic, [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) | Papel no `system` vs. `user`; tags XML para separar instrução/exemplos/contexto (`<example>`/`<examples>`, nomes consistentes, aninhamento); "golden rule" de clareza; usar o recurso nativo de **Structured Outputs** (ou tool com campo `enum`) em vez de prefill para forçar formato — prefill não é mais suportado nos modelos atuais; `<thinking>` em few-shot para modelar o padrão de raciocínio quando o "thinking" está desligado. |
| OpenAI, [Prompt engineering guide](https://developers.openai.com/api/docs/guides/prompt-engineering) e [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs) | Ordem recomendada Identidade → Instruções → Exemplos → Contexto; combinar Markdown + tags para hierarquia; exemplos diversos cobrindo casos de fronteira; GPT se beneficia de instruções **precisas**, não de CoT verboso; `strict: true` com JSON Schema é o mecanismo correto para forçar formato (enum para classe única, array para multi-label), com todos os campos em `required`. |
| Google, [Prompting strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies) | Estrutura papel → restrições → codebook → tarefa → formato; exemplos diversos (2–4 por classe); Gemini 3 já gera raciocínio interno automaticamente — pedir passo a passo explícito (analisar → casar com regra → classificar → justificar) ainda ajuda; usar a **Structured Output API** (schema), não só formatação por prompt, para JSON complexo; fundamentar a resposta apenas no contexto fornecido, sem assumir informação externa. |

**Convergência entre as três fontes** — é isso que torna defensável usar
"um único prompt" para os três modelos, em vez de três prompts
customizados:

1. Todas recomendam **tags estruturais** (XML e/ou Markdown) para separar
   papel, instruções, exemplos e entrada — nenhuma depende de sintaxe
   proprietária de um único fornecedor.
2. Todas recomendam **exemplos diversos e no mesmo formato da saída
   esperada** — os 7 casos de [[EXP-005]] já cumprem isso.
3. Todas recomendam usar o **recurso nativo de saída estruturada** do
   fornecedor (Structured Outputs / tool com `enum` / response schema) em
   vez de confiar só em instrução textual para o formato. **Isso não é
   possível no modo de invocação adotado** (CLI com acesso ao diretório,
   ver aviso acima) — o schema da §3 vira só instrução textual, compensada
   por regras de formato explícitas e um passo de autovalidação (§4). É a
   única recomendação das três fontes que este desenho **não** consegue
   seguir à risca, e fica registrado como tal, não escondido.
4. Nenhuma recomenda expor ao modelo informação de contexto que não seja
   estritamente necessária à tarefa — o que aqui coincide diretamente com
   a regra de cegamento já em vigor no projeto ([[Decision Log#D-021]],
   por analogia estendida a [[Decision Log#D-026]]).

---

## 2. Instrução única (para colar na CLI de cada modelo)

Um único bloco de texto, sem separação formal entre `system` e `user` —
a maioria das CLIs de agente não expõe essa distinção da mesma forma que a
API bruta. Onde a CLI aceitar um prompt de sistema à parte (ex.:
`--append-system-prompt` no Claude Code), o parágrafo de papel/restrições
logo abaixo do `<task>` pode ir lá; caso contrário, o bloco inteiro
funciona como uma única instrução.

```xml
<role>
Você é um classificador cuidadoso e literal. Sua única tarefa é aplicar o
instrumento de classificação abaixo a um lote de arquivos de skill, e
escrever a saída no formato exigido em <output_format> — nenhum texto
fora do formato pedido, nenhum preâmbulo, nenhuma explicação adicional
fora dos campos do próprio schema.

Você não deve usar nenhum conhecimento externo sobre o repositório, autor
ou popularidade da skill — julgue apenas o texto de cada arquivo. Se a
evidência for insuficiente, use a classe prevista para isso (AMBIGUOUS)
em vez de adivinhar.
</role>

<task>
No diretório <cases_dir>results/EXP-013_llm_cases/</cases_dir> há um
arquivo `.md` por caso, cada um com este formato:

  case_id: LLM001
  name: <nome da skill ou vazio>
  description: <descrição ou vazio>
  ---

  <corpo completo do SKILL.md>

Para CADA arquivo do diretório, classifique a skill segundo o instrumento
abaixo (definição, classes, dimensões e regras de decisão), aplicando as
regras na ordem indicada. Processe TODOS os arquivos, um a um, na ordem
alfabética do nome do arquivo (LLM001, LLM002, ...) — não pule nenhum,
não amostre, não resuma vários casos juntos. Trate cada caso como
totalmente independente: a classificação de um caso não deve influenciar
a de outro (não procure padrões entre casos, não ajuste critério ao longo
do lote).

**Restrição de acesso:** leia apenas os arquivos dentro de
`results/EXP-013_llm_cases/`. Não leia, liste nem acesse nenhum outro
arquivo ou diretório deste repositório — isso preservaria informação que
não deveria influenciar o julgamento (cegamento, ver <constraints>).

Ao final de cada caso, responda apenas com o objeto JSON especificado em
<output_format>.
</task>

<definition>
Security Skill: uma Agent Skill cujo propósito principal, ou uma parte
substancial de seu comportamento operacional, é prevenir, detectar,
analisar, avaliar, explorar, mitigar ou responder a ameaças,
vulnerabilidades, violações de propriedades de segurança ou controles de
acesso em sistemas computacionais. Presença de vocabulário de segurança
nunca basta por si só — considere propósito declarado, comportamento,
atividade orientada ou executada, resultado esperado, contexto e
artefatos associados.
</definition>

<classes>
PRIMARY — segurança é o propósito principal da skill.
SECONDARY — segurança é capacidade ou etapa substancial de um objetivo maior.
MENTION — recomendação, observação ou preocupação incidental, não acionável.
NONE — sem preocupação de segurança relevante.
AMBIGUOUS — evidência insuficiente para classificar com confiança. Não é
descarte: é um resultado válido. Nunca force uma das outras quatro classes
quando a evidência não sustenta.
</classes>

<dimensions>
security_focus (true/false) — segurança é o propósito predominante?
operational_security (true/false) — a skill executa, automatiza, orienta
ou avalia uma atividade concreta de segurança sobre código, aplicação,
infraestrutura, rede, agente, modelo ou outro artefato computacional?
("Analise este código e encontre SQL Injection" É operacional, mesmo sendo
só raciocínio.)
operation_level — reasoning (só raciocínio/orientação) | executable
(invoca ferramenta/script/comando) | mixed | n/a (quando security_focus e
operational_security não se aplicam).
security_functions — multi-label, entre PREVENT, DETECT, ASSESS, TEST,
RESPOND, RECOVER. Só preencha se security_relevance for PRIMARY ou
SECONDARY.
security_concerns — multi-label, vocabulário livre (nomeie a preocupação
de segurança em termos curtos, ex.: "sql_injection", "secrets_in_code",
"dependency_security"). Só preencha se PRIMARY ou SECONDARY.
operational_capability — multi-label. Vocabulário sugerido (use "other" se
nenhum se aplicar bem): reasoning_or_guidance, source_code_analysis,
static_analysis, dynamic_analysis, configuration_analysis,
dependency_analysis, command_execution, network_scanning,
vulnerability_scanning, exploitation, secret_scanning, remediation, other.
Só preencha se PRIMARY ou SECONDARY.
evidence — multi-label, entre description, body, bundled_artifacts (onde
a evidência decisiva aparece).
confidence — high | medium | low.
</dimensions>

<rules>
Aplique nesta ordem; pare na primeira que decidir a classe.

R-1 (teste de remoção). Removido todo o conteúdo de segurança, a skill
ainda cumpre seu propósito? Não → PRIMARY. Sim, mas perde capacidade
operacional descrita → SECONDARY. Sim, praticamente inalterada → MENTION
ou NONE.

R-2 (teste de acionabilidade). Conteúdo de segurança é acionável quando
diz o que fazer (procedimento, checklist, critério, ferramenta a
executar), não apenas o que evitar. Advertência de uma linha não é
acionável. SECONDARY exige conteúdo acionável; sem isso, MENTION.

R-3 (teste de proporção). Segurança como uma entre várias dimensões
coordenadas → SECONDARY. Segurança organizando a skill inteira, demais
dimensões subordinadas → PRIMARY.

R-4 (locus da evidência). Casamento apenas em tags, categoria, nome de
arquivo ou lista de "related skills" não conta como conteúdo de
segurança.

R-5 (homônimos). Termo de segurança em sentido não relacionado a
segurança não conta (ex.: "audit" de anúncios, "token" de LLM,
"permission" de arquivo).

R-6 (artefatos associados). Se a skill inclui scripts que executam função
de segurança pouco mencionada no texto principal, classifique pelo
comportamento operacional conjunto (marque evidence: bundled_artifacts).
Se um artefato necessário não estiver disponível no texto fornecido, use
AMBIGUOUS.

R-7 (objeto protegido não restringe). Vale tanto para código produzido
quanto para o agente/harness ou a própria skill — registre isso em
security_concerns, não na classe.

R-9 (idioma). A classe nunca é decidida pelo idioma do texto. Termos
técnicos de segurança em inglês embutidos em texto de outro idioma são
evidência válida, não ruído. Para efeito do campo possible_non_english
(ver <constraints>): considere o texto "mixed" (não 100% inglês) quando
duas ou mais línguas carregam conteúdo substantivo — como referência
operacional, quando pelo menos 15% do texto está numa língua minoritária,
com pelo menos 40 caracteres não latinos e pelo menos 20 palavras latinas
presentes; e considere "und" (indeterminado) quando a prosa é curta ou
técnica demais para decidir o idioma. Um termo técnico isolado não basta
para caracterizar mixed em nenhuma direção.

R-10 (escopo de governança/risco/conformidade). GRC entra como Security
Skill apenas quando a atividade incide sobre propriedades de segurança de
sistemas computacionais (auditoria de IAM, least privilege, controles
técnicos, conformidade que inspeciona configuração/código). GRC
puramente contratual, organizacional ou documental (onboarding de
fornecedor, seguro, sanções, política como documento) → NONE, não
MENTION. Misto com parte técnica acionável → SECONDARY, confidence: low.
Misto com parte técnica só mencionada → MENTION.

R-8 (fechamento — aplicar por último, só se ainda houver dúvida).
Evidência insuficiente → AMBIGUOUS, confidence: low. Evidência presente
mas limite entre duas classes é discutível → classe mais baixa,
confidence: low.
</rules>

<constraints>
- Julgue apenas o texto fornecido abaixo (name, description, body). Não
  suponha nada sobre o repositório, popularidade, autor ou propósito além
  do que está escrito.
- Não force PRIMARY/SECONDARY/MENTION/NONE quando a evidência não
  sustentar — AMBIGUOUS é uma resposta válida e esperada em alguns casos.
- A população elegível para esta tarefa é restrita a skills **100% em
  inglês** ([[Decision Log#D-025]]): nenhum trecho substantivo de
  `description` ou `body` em outro idioma. Se você perceber QUALQUER
  trecho substantivo em outro idioma — mesmo que o restante do texto seja
  inglês, mesmo que seja só um parágrafo — classifique normalmente da
  melhor forma possível (R-9 continua valendo: idioma nunca decide a
  classe) e marque possible_non_english: true. Um termo técnico isolado em
  inglês dentro de texto majoritariamente não inglês NÃO torna a skill
  elegível sozinho; simetricamente, um termo técnico isolado em outro
  idioma dentro de texto majoritariamente inglês NÃO caracteriza a skill
  como não elegível. Trechos que não são prosa (nome de arquivo, código,
  mensagem de erro literal, comando) em outro idioma não contam para este
  critério. Esta flag sinaliza um possível erro do filtro de amostragem —
  nunca deve mudar sua classificação de security_relevance nem das demais
  dimensões.
- rule_applied deve ser a regra que efetivamente decidiu o caso (a última
  aplicada antes de você chegar à classe final), não todas as regras
  consideradas.
- note deve ter uma frase apenas, explicando o porquê da decisão.
</constraints>

<examples>
<example id="EX01">
  <input>
    name: performing-malware-ioc-extraction
    description: Malware IOC extraction is the process of analyzing malicious software to identify actionable indicators of compromise including file hashes, network indicators (C2 domains, IP addresses, URLs), registry modifications, mutex names, embedded strings, and behavioral artifacts.
    body: |
      # Performing Malware IOC Extraction
      ## Overview
      Malware IOC extraction is the process of analyzing malicious software to identify
      actionable indicators of compromise including file hashes, network indicators (C2
      domains, IP addresses, URLs), registry modifications, mutex names, embedded strings,
      and behavioral artifacts. This skill covers static analysis with PE parsing and
      string extraction, dynamic analysis with sandbox detonation, automated IOC
      extraction using tools like YARA, and formatting results as STIX 2.1 indicators.
      ## When to Use
      - When conducting security assessments that involve performing malware IOC extraction
      - When following incident response procedures for related security events
      ## Prerequisites
      - Python 3.9+ with pefile, yara-python, oletools, stix2 libraries
      [... trecho real truncado; caso completo tem 13.275 caracteres]
  </input>
  <output>
    {"case_id":"EX01","security_relevance":"PRIMARY","security_focus":true,
    "operational_security":true,"operation_level":"executable",
    "security_functions":["DETECT","ASSESS"],
    "security_concerns":["malware_analysis","threat_intelligence"],
    "operational_capability":["static_analysis","dynamic_analysis"],
    "evidence":["description","body"],"confidence":"high","rule_applied":"R-1",
    "grc_case":false,"secondary_mention_boundary":false,
    "possible_non_english":false,
    "note":"Skill dedicada à extração de indicadores de comprometimento de malware; sem o conteúdo de segurança ela deixa de existir."}
  </output>
</example>
<example id="EX02">
  <input>
    name: code-review
    description: Review code across every judgment lens this harness cares about, in one pass, by running the dedicated lenses in order: code-think-twice, code-kiss, code-yagni, code-dry, code-early-return, code-no-nested-loop, code-bounded-loops, code-composition, code-solid, code-smells, code-nitpick, code-magic-strings, code-magic-numbers, code-no-keys (no hardcoded secrets), code-no-credentials (no embedded logins / plaintext passwords), and code-traceability. Every lens ALWAYS runs.
    body: |
      # Review code across every judgment lens this harness cares about
      Runs a fixed sequence of ~20 review lenses on every pass. Two of them are
      security-specific (code-no-keys: no hardcoded meaningful literals used as
      secrets; code-no-credentials: no embedded logins / plaintext passwords),
      alongside lenses for simplicity, duplication, SOLID design, magic numbers,
      and traceability. Renders ONE verdict: APPROVED only when every lens is
      clean.
      [... trecho real truncado; caso completo tem 5.050 caracteres]
  </input>
  <output>
    {"case_id":"EX02","security_relevance":"SECONDARY","security_focus":false,
    "operational_security":true,"operation_level":"reasoning",
    "security_functions":["DETECT"],
    "security_concerns":["secrets_in_code","hardcoded_credentials"],
    "operational_capability":["source_code_analysis"],
    "evidence":["description"],"confidence":"high","rule_applied":"R-3",
    "grc_case":false,"secondary_mention_boundary":false,
    "possible_non_english":false,
    "note":"Dois lentes de segurança (secrets, credenciais) entre cerca de vinte lentes de revisão coordenadas — segurança é uma dimensão, não o propósito central."}
  </output>
</example>
<example id="EX03">
  <input>
    name: zero-to-running
    description: Automate local development environment setup for multi-service applications. Use when developers need to quickly set up or configure local dev environments with frontend, backend, PostgreSQL, Redis, and Kubernetes orchestration.
    body: |
      # Zero-to-Running Developer Environment
      ## Configuration File Creation
      Generate externalized configuration (.env.example or config/dev.yml):
      # Database credentials (mock/dev only)
      DB_PASSWORD=dev_password_change_in_production
      **Patterns:**
      - Separate dev/prod concerns clearly
      - Use secure defaults
      - Document credential management pattern
      [... trecho real truncado; caso completo tem 9.022 caracteres, sem outra
      menção a segurança além desta]
  </input>
  <output>
    {"case_id":"EX03","security_relevance":"MENTION","security_focus":false,
    "operational_security":false,"operation_level":"n/a",
    "security_functions":[],"security_concerns":[],"operational_capability":[],
    "evidence":["body"],"confidence":"high","rule_applied":"R-2",
    "grc_case":false,"secondary_mention_boundary":true,
    "possible_non_english":false,
    "note":"Diz 'use secure defaults' e 'document credential management pattern' — recomendação pontual, não procedimento acionável."}
  </output>
</example>
<example id="EX04">
  <input>
    name: cybersec-testing-ransomware-recovery-procedures
    description: Test and validate ransomware recovery procedures including backup restore operations, RTO/RPO target verification, recovery sequencing, and clean restore validation to ensure organizational resilience against destructive ransomware attacks.
    body: |
      > Nota per Kimi Code: questa skill è convertita dal pacchetto Anthropic
      > Cybersecurity Skills. Descrivi in linguaggio naturale il task di
      > cybersecurity che vuoi affrontare.

      # Testing Ransomware Recovery Procedures
      ## When to Use
      - Validating that ransomware recovery plans actually work under realistic conditions
      - Measuring RTO/RPO against business requirements
      - Testing backup restore operations to confirm data integrity after simulated encryption
      - Conducting tabletop exercises or live recovery drills for ransomware scenarios
      [... trecho real truncado; caso completo tem 7.095 caracteres, restante em inglês]
  </input>
  <output>
    {"case_id":"EX04","security_relevance":"PRIMARY","security_focus":true,
    "operational_security":true,"operation_level":"executable",
    "security_functions":["TEST","RECOVER"],
    "security_concerns":["ransomware","disaster_recovery"],
    "operational_capability":["remediation","command_execution"],
    "evidence":["description","body"],"confidence":"high","rule_applied":"R-1",
    "grc_case":false,"secondary_mention_boundary":false,
    "possible_non_english":true,
    "note":"Teste e validação de recuperação de ransomware — claramente PRIMARY. Há uma frase em italiano embutida no corpo; sinalizada, não muda a classe (R-9)."}
  </output>
</example>
<example id="EX05">
  <input>
    name: meta-ads-audit
    description: Meta Ads audit — audience analysis, creative fatigue, budget pacing, lead quality.
    body: |
      # Meta Ads Audit
      Comprehensive Meta Ads (Facebook + Instagram) account audit using live data.
      ## Full Audit Steps
      1. Account Discovery
      2. Campaign Overview (last 30 days)
      3. Ad Set Analysis — audience overlap, frequency saturation
      4. Creative Performance — flag fatigue, low CTR
      [... trecho real truncado; caso completo tem 2.446 caracteres, nada relativo
      a segurança computacional em nenhum ponto]
  </input>
  <output>
    {"case_id":"EX05","security_relevance":"NONE","security_focus":false,
    "operational_security":false,"operation_level":"n/a",
    "security_functions":[],"security_concerns":[],"operational_capability":[],
    "evidence":[],"confidence":"high","rule_applied":"R-5",
    "grc_case":false,"secondary_mention_boundary":false,
    "possible_non_english":false,
    "note":"'Audit' aqui é auditoria de anúncios (marketing), não auditoria de segurança — homônimo, R-5."}
  </output>
</example>
<example id="EX06">
  <input>
    name: (sem front matter — exemplo ilustrativo, não é um caso real do dataset)
    body: |
      Quick helper for repetitive tasks. See related tools for more.
      [texto propositalmente curto e genérico — este é o único exemplo
      fictício do conjunto, mantido assim de propósito: um corpo realista e
      mais longo tornaria o caso menos ambíguo, contradizendo o ponto que
      ele ensina]
  </input>
  <output>
    {"case_id":"EX06","security_relevance":"AMBIGUOUS","security_focus":null,
    "operational_security":null,"operation_level":null,
    "security_functions":[],"security_concerns":[],"operational_capability":[],
    "evidence":["body"],"confidence":"low","rule_applied":"R-8",
    "grc_case":false,"secondary_mention_boundary":false,
    "possible_non_english":false,
    "note":"Sem front matter e corpo genérico demais para dizer o que a skill faz — evidência insuficiente, não motivo para forçar NONE."}
  </output>
</example>
<example id="EX07">
  <input>
    name: draft-vendor-onboarding-questionnaire
    description: Drafting a risk-tiered vendor onboarding questionnaire from vendor management policies and internal directives, requiring identification of cross-document inconsistencies and healthcare compliance questions.
    body: |
      # Skill: Draft Vendor Onboarding Questionnaire
      ## Subject-matter triage
      Identify the governing vendor framework first, then map each source
      document to the control area it governs: onboarding, privacy, security,
      finance, insurance, business continuity, subcontracting, sanctions, and
      ethics. Treat the most formal policy as the baseline, then reconcile
      more specific or more protective requirements from other documents.
      [... trecho real truncado; caso completo tem 9.133 caracteres — nenhuma
      etapa inspeciona configuração, código ou sistema computacional]
  </input>
  <output>
    {"case_id":"EX07","security_relevance":"NONE","security_focus":false,
    "operational_security":false,"operation_level":"n/a",
    "security_functions":[],"security_concerns":[],"operational_capability":[],
    "evidence":["body"],"confidence":"medium","rule_applied":"R-10",
    "grc_case":true,"secondary_mention_boundary":false,
    "possible_non_english":false,
    "note":"GRC organizacional: onboarding de fornecedor, seguro, sanções, continuidade de negócio. 'Security' é uma das nove áreas de controle listadas, mas nada aqui inspeciona sistema computacional — R-10, NONE."}
  </output>
</example>
</examples>

<output_format>
Escreva UM objeto JSON por linha (formato JSONL — uma linha completa e
válida por caso, sem vírgula entre linhas, sem colchete envolvendo o
arquivo inteiro) no arquivo de saída indicado pelo operador no momento da
invocação (ver §5 — o nome do arquivo de saída não faz parte deste
prompt, para não revelar que a saída será comparada entre modelos).

Cada linha segue exatamente o schema da §3, incluindo o `case_id` do
arquivo que originou aquela linha. Escreva a linha de cada caso assim que
terminar de classificá-lo — não acumule tudo em memória para escrever de
uma vez só ao final; se a sessão for interrompida, o trabalho já escrito
não deve ser perdido.

Depois de processar TODOS os arquivos do diretório, na última linha da
sua resposta visível (fora do arquivo de saída) informe apenas: quantos
casos foram processados e quantos arquivos existiam no diretório — para o
operador confirmar que nada ficou de fora. Nenhum outro texto depois
disso.

**Autovalidação, antes de encerrar:** releia o arquivo de saída que você
escreveu. Confirme que (a) tem exatamente uma linha por arquivo de caso
processado, (b) cada linha é um JSON válido isoladamente, (c) todos os
campos do schema aparecem em cada linha, mesmo quando vazios (`[]`,
`null`, conforme o schema pede). Corrija antes de encerrar se algo faltar.
</output_format>
```

> [!note] Origem dos exemplos (revisado em 2026-09-03)
> A primeira versão deste prompt usava os 7 casos **fictícios** de
> `EXP-005_annotation_example.csv` (só `name` + uma frase de nota, sem
> texto real de `SKILL.md`) e reaproveitava dois casos não ingleses
> (turco, português) para ilustrar `possible_non_english` — desproporcional
> à população real, que é 100% inglês por construção. Corrigido: seis dos
> sete exemplos agora usam **texto literal real** dos casos já citados como
> âncora em [[Codebook]] §8 (consultados via DuckDB sobre `data/raw/gitskills`,
> truncados para caber no prompt, com o corte marcado explicitamente).
> Apenas **EX06** (`AMBIGUOUS`) permanece fictício — de propósito: um corpo
> genérico curto *é* o ponto que ensina, um caso real mais longo o
> descaracterizaria.
>
> **Achado incidental:** o caso real de EX04
> (`cybersec-testing-ransomware-recovery-procedures`) contém uma frase em
> **italiano** embutida num skill vendido/convertido de outro pacote,
> mesmo sendo majoritariamente em inglês — evidência real de que a mistura
> de idiomas de mesma escrita latina (italiano/português/espanhol dentro de
> inglês) **não é capturada** pelo limiar numérico que [[Decision Log#D-025]]
> emprestou de R-9 (que exige ≥40 caracteres **não latinos**, pensado para
> mistura com CJK/cirílico/etc.). Isso é uma lacuna real na operacionalização
> de "100% inglês", não hipotética — registrada em
> [[Decision Log#D-025]] para correção.

---

## 4. Schema JSON (idêntico nos três fornecedores; sintaxe de aplicação difere)

```json
{
  "type": "object",
  "properties": {
    "case_id": {"type": "string"},
    "security_relevance": {"type": "string", "enum": ["PRIMARY", "SECONDARY", "MENTION", "NONE", "AMBIGUOUS"]},
    "security_focus": {"type": ["boolean", "null"]},
    "operational_security": {"type": ["boolean", "null"]},
    "operation_level": {"type": ["string", "null"], "enum": ["reasoning", "executable", "mixed", "n/a", null]},
    "security_functions": {"type": "array", "items": {"type": "string", "enum": ["PREVENT", "DETECT", "ASSESS", "TEST", "RESPOND", "RECOVER"]}},
    "security_concerns": {"type": "array", "items": {"type": "string"}},
    "operational_capability": {"type": "array", "items": {"type": "string"}},
    "evidence": {"type": "array", "items": {"type": "string", "enum": ["description", "body", "bundled_artifacts"]}},
    "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
    "rule_applied": {"type": "string", "enum": ["R-1", "R-2", "R-3", "R-4", "R-5", "R-6", "R-7", "R-8", "R-9", "R-10"]},
    "grc_case": {"type": "boolean"},
    "secondary_mention_boundary": {"type": "boolean"},
    "possible_non_english": {"type": "boolean"},
    "note": {"type": "string"}
  },
  "required": ["case_id", "security_relevance", "security_focus", "operational_security", "operation_level", "security_functions", "security_concerns", "operational_capability", "evidence", "confidence", "rule_applied", "grc_case", "secondary_mention_boundary", "possible_non_english", "note"],
  "additionalProperties": false
}
```

`security_concerns` e `operational_capability` ficam como arrays de string
livre (o Codebook os trata como vocabulário candidato/livre, não fechado —
ver [[Codebook]] §5); os demais campos enumerados são fechados porque o
Codebook os fixa.

---

## 5. Como invocar cada CLI

**Padrão geral**, independente de qual CLI:

1. Isole os 100 arquivos-caso num diretório que a CLI possa ler
   (`results/EXP-013_llm_cases/`, já gerado por [[EXP-013]]) — **não** dê
   acesso à raiz do repositório. O diretório não contém `Decision Log`,
   `Codebook` nem nenhuma resposta esperada — só os 100 arquivos cegos —
   mas restringir o acesso é uma segunda camada de proteção, caso a CLI
   tenha por padrão visibilidade do diretório de trabalho inteiro.
2. Passe o bloco `<role>` + `<task>` + `<definition>` + `<classes>` +
   `<dimensions>` + `<rules>` + `<constraints>` + `<examples>` + o schema
   da §3 como a instrução/prompt inicial da sessão.
3. Diga à CLI, **fora do texto do prompt compartilhado** (para não expor
   a comparação entre modelos ao próprio modelo), o nome do arquivo de
   saída — diferente por modelo, para o operador distinguir depois:
   `results/EXP-013_gpt_output.jsonl`,
   `results/EXP-013_claude_output.jsonl`,
   `results/EXP-013_gemini_output.jsonl` (sugestão de nomenclatura; use a
   que preferir, contanto que registre qual arquivo veio de qual modelo).
4. Rode as três sessões **sem nenhuma delas ver o diretório de trabalho
   ou a saída das outras** — sessões separadas, sem histórico
   compartilhado.

**Exemplo concreto (Claude Code CLI)** — adaptar a sintaxe equivalente
para as CLIs de GPT-5.6 Sol e Gemini 3.1 Pro, que este documento não
prescreve por não ter a sintaxe exata verificada:

```bash
claude --print \
  --append-system-prompt "$(cat prompt_role.txt)" \
  "Leia results/EXP-013_llm_cases/, classifique cada caso conforme as \
   instruções, e escreva o JSONL em results/EXP-013_claude_output.jsonl"
```

**O que se perde, sem a API bruta — e como isso é compensado:**

| Perda | Compensação neste desenho |
|---|---|
| Schema JSON aplicado no servidor (garante formato) | Autovalidação em texto (§4) + JSONL (uma linha ruim não derruba as outras) |
| `temperature` controlável | Best-effort: usar o parâmetro/flag de determinismo que a CLI expuser, se houver; **registrar se não houver controle disponível** — é uma limitação a declarar, não a esconder |
| Identificador exato de versão/snapshot do modelo por chamada | Registrar a versão que a CLI reporta ao iniciar (ex.: `claude --version`, ou o que a própria CLI imprimir), mesmo que menos preciso que um parâmetro de API |

**Parâmetros a fixar e registrar de qualquer forma** (exigido por
[[Decision Log#D-008]] — LLM não é ground truth sem registro de modelo,
versão, prompt e configuração):

- A configuração de determinismo efetivamente usada em cada CLI (ou a
  ausência dela, declarada).
- Versão/build de cada CLI e, quando disponível, do modelo por trás dela.
- O texto deste prompt (cópia versionada — este arquivo) e a data/hora de
  cada execução.
- **Cegamento** ([[Decision Log#D-021]], estendido a [[Decision Log#D-026]]):
  cada modelo recebe exatamente `name`, `description` e o corpo do
  `SKILL.md` — nada de tier, sinal preliminar, motivo de seleção,
  `file_sha`, nome de repositório ou qualquer metadado fora do que já está
  nos arquivos de `results/EXP-013_llm_cases/`.
- Nenhuma menção, em nenhuma das três sessões, de que a saída será
  comparada entre modelos — isso é decidido depois, no script de
  agregação, não deve influenciar o julgamento individual.
- **Cegamento entre modelos, explícito e não negociável** ([[Decision Log#D-026]]):
  as três sessões são totalmente independentes — nenhuma vê a saída ou
  classificação de outra, em nenhum momento.

## 6. O que já foi resolvido desde a versão anterior (2026-09-03)

- **Critério operacional de "skill em inglês"** ([[Decision Log#D-025]]):
  100% inglês. A primeira operacionalização (limiar de R-9) se mostrou
  incapaz de capturar mistura de mesma escrita latina — corrigida em
  [[EXP-013]] (detecção por parágrafo com `lingua`). A amostra já reflete
  isso: [[EXP-013]] gerou os 100 casos em `results/EXP-013_llm_cases/`.
- **Regra de desempate e escopo da adjudicação** ([[Decision Log#D-026]]):
  qualquer discordância entre os três modelos, em qualquer dimensão, leva
  o caso inteiro à adjudicação humana — lógica do script de agregação
  (§7), não do prompt.
- **Cegamento entre modelos**: confirmado como regra explícita (§5).
- **Modo de invocação**: CLI com acesso ao diretório, não API programática
  — prompt reformulado para processar o diretório inteiro em vez de um
  caso por chamada, com JSONL + autovalidação como substituto do schema
  aplicado no servidor (§2, §4, §5).

## 7. O que ainda falta (não resolvido aqui)

- **Script de agregação/discordância** — lê os três `.jsonl` de saída,
  casa por `case_id`, decide unanimidade vs. discordância em qualquer
  dimensão (regra já fixada em [[Decision Log#D-026]]), e produz a lista
  de casos para adjudicação humana. Confirmado como necessário, ainda não
  escrito.
- Nenhum critério numérico de quantos casos de discordância seriam
  "poucos demais" para validar o classificador com confiança — mesma
  lacuna que [[Decision Log#D-024]] registra para "validação
  satisfatória" de E-7.
- Sintaxe exata das CLIs de GPT-5.6 Sol e Gemini 3.1 Pro não verificada
  neste documento (só a do Claude Code) — adaptar na hora.

## Ligações

[[Decision Log]] (ver D-025, D-026, D-021, D-008) · [[Codebook]] ·
[[EXP-013]] · [[EXP-005]] · [[Guia do Anotador Humano (D-026)]] ·
[[QI-1 Methodology]] · [[03 - Methodology]]
