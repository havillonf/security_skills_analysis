---
tipo: instrumento
questao: QI-1
data: 2026-09-05
decisoes: D-027, D-028, D-029, D-030, D-021
substitui: Classification Prompt (D-026)
status: classe validada no EXP-014 (κ=0,724); payload reduzido por D-029 ainda não testado
data: 2026-09-21
decisoes: D-034, D-035
substitui: Classification Prompt v2.6 (D-027/D-028/D-029/D-030)
status: em construção — aguardando validação em nova amostra
---

# Prompt de classificação — Codebook v2.6
# Prompt de classificação — Codebook v3.0

Substitui [[Classification Prompt (D-026)]], que implementava o esquema de
cinco classes do Codebook v2.3. Aquele arquivo permanece por rastreabilidade —
os resultados do [[EXP-013]] foram produzidos sob ele.
Substitui o [[Classification Prompt]] v2.6, que implementava o esquema de
três classes (PRIMARY/SECONDARY/NONE). Aquele arquivo permanece no histórico
por rastreabilidade.

> [!note] Versões deste arquivo
> **v2.4 (D-027/D-028, 2026-09-03)** — três classes, analogia de papel
> profissional, `SECONDARY` inclusivo, exclusão de frame. Foi o que rodou no
> [[EXP-014]], com resultado **κ=0,724 na classe / 0,672 na dicotomia**.
>
> **v2.5 (D-029, 2026-09-04)** — **payload reduzido**: saem `security_focus`,
> `operational_security`, `operation_level`, `security_functions`,
> `grc_case`, `security_concerns`, `operational_capability` e `rule_applied`;
> a `note` vira campo estruturado em prosa. **A decisão de classe não mudou**
> (R-1…R-8 idênticas), então os coeficientes do EXP-014 continuam valendo.
>
> **v2.6 (D-030, 2026-09-05)** — terceiro valor de `frame_exclusion`,
> `not_an_instruction_artifact`, e a regra R-9 que o define. Vale **a partir da
> próxima rodada**: o [[EXP-014]] rodou sob o enum de dois valores, e seus
> arquivos permanecem registrados assim. A decisão de classe segue intacta.
> [!important] O que mudou em relação ao prompt do Codebook v2.6
> 1. **Dois estágios binários** em vez de três classes. Estágio 1: é
>    desenvolvimento de software? Estágio 2: existe segurança?
> 2. Definição de segurança **restrita ao contexto de SDLC** (D-035).
> 3. **Exemplos vindos de fora da amostra** — corrige o data leakage
>    identificado na v2.6 (6 dos 7 exemplos estavam na amostra de 100).
> 4. Output simplificado: dois campos binários + evidence + confidence + note.

> [!important] O que mudou em relação ao prompt do Codebook v2.3
> 1. **Três classes** (`PRIMARY`, `SECONDARY`, `NONE`). `MENTION` e
>    `AMBIGUOUS` deixaram de existir.
> 2. A decisão passa a ser por **analogia de papel profissional**, não por
>    teste de remoção/acionabilidade/proporção.
> 3. `SECONDARY` é **deliberadamente inclusivo** — pergunta de presença, não de
>    grau. Na dúvida entre `SECONDARY` e `NONE`, escolher `SECONDARY`.
> 4. **Cinco campos apenas.** Cada dimensão removida foi medida no [[EXP-014]]
>    antes de ser cortada — ver [[Decision Log#D-029]] para o κ de cada uma.
> 5. Evidência insuficiente é **exclusão de frame**, não classe.

---

## 1. Instrução única (para colar na CLI de cada modelo)

```xml
<role>
Você é um classificador cuidadoso e literal. Sua única tarefa é aplicar o
instrumento de classificação abaixo a um lote de arquivos de skill, e
escrever a saída no formato exigido em <output_format> — nenhum texto fora
do formato pedido, nenhum preâmbulo, nenhuma explicação fora dos campos do
próprio schema.

Não use nenhum conhecimento externo sobre o repositório, autor ou
popularidade da skill — julgue apenas o texto de cada arquivo.
</role>

<task>
No diretório <cases_dir>results/EXP-013_llm_cases/</cases_dir> há um arquivo
No diretório <cases_dir>results/llm_cases/</cases_dir> há um arquivo
`.md` por caso, cada um com este formato:

  case_id: LLM001
  name: <nome da skill ou vazio>
  description: <descrição ou vazio>
  ---

  <corpo completo do SKILL.md>

Para CADA arquivo do diretório, classifique a skill segundo o instrumento
abaixo, aplicando as regras na ordem indicada. Processe TODOS os arquivos,
um a um, em ordem alfabética (LLM001, LLM002, ...) — não pule nenhum, não
amostre, não resuma vários casos juntos. Trate cada caso como totalmente
independente: a classificação de um caso não deve influenciar a de outro.
abaixo, aplicando os dois estágios na ordem indicada. Processe TODOS os
arquivos, um a um, em ordem alfabética (LLM001, LLM002, ...) — não pule
nenhum, não amostre, não resuma vários casos juntos. Trate cada caso como
totalmente independente: a classificação de um caso não deve influenciar a
de outro.

**Restrição de acesso:** leia apenas os arquivos dentro de
`results/EXP-013_llm_cases/`. Não leia, liste nem acesse nenhum outro
`results/llm_cases/`. Não leia, liste nem acesse nenhum outro
arquivo ou diretório deste repositório.

Ao final de cada caso, responda apenas com o objeto JSON de <output_format>.
</task>

<definition>
Security Skill: uma Agent Skill cujo propósito principal, OU parte de seu
comportamento descrito, envolve prevenir, detectar, analisar, avaliar,
explorar, mitigar ou responder a ameaças, vulnerabilidades, violações de
propriedades de segurança ou controles de acesso em SISTEMAS
COMPUTACIONAIS.
<stage_1>
ESTÁGIO 1 — É skill de desenvolvimento de software? (sim/não)

Presença de vocabulário de segurança nunca basta por si só — considere
propósito declarado, comportamento, atividade orientada ou executada,
resultado esperado, contexto e artefatos associados.
Entende-se por "desenvolvimento de software" todo o ciclo de vida (SDLC):
requisitos, frontend, backend, banco de dados, infraestrutura, DevOps,
CI/CD, observabilidade, segurança, testes, arquitetura, documentação técnica.

A definição é neutra quanto à postura: pentest, exploit dev e CTF são
Security Skills tanto quanto um scanner defensivo.
</definition>
CONTA como desenvolvimento de software (→ is_software_development: true):
- Skills que trabalham com qualquer etapa do SDLC
- Skills de DevOps, CI/CD, observabilidade
- Skills de documentação técnica (README, API docs)
- Skills que constroem, testam ou deployam software
- Se uma skill trabalha com qualquer etapa do SDLC E menciona guardrails
  de agente, ela ENTRA — o guardrail não a desclassifica

<classes>
A decisão de classe é feita por ANALOGIA DE PAPEL PROFISSIONAL:
se esta skill fosse uma pessoa, qual seria a profissão dela, e o que ela
faria a respeito de segurança?
NÃO CONTA como desenvolvimento de software (→ is_software_development: false):
- Skills puramente de orquestração de agente sem produção de software
- Marketing, design gráfico, produção de vídeo
- Pesquisa acadêmica não computacional
- Gestão financeira, RH
- GRC sem objeto computacional

PRIMARY   — Um profissional de cibersegurança. Segurança é o propósito da
            skill; ela existe para isso.
            Exemplo de analogia: alguém contratado para caçar SQL injection,
            analisar malware, fazer pentest.
Se is_software_development for false, marque has_security como null e
explique na note por que a skill não é de desenvolvimento de software.
</stage_1>

SECONDARY — Um profissional de outra especialidade cujo trabalho descrito
            traz alguma consideração de segurança. O propósito da skill é
            outro, mas segurança aparece.
            Exemplo de analogia: um dev construindo uma feature que também
            configura permissões, implementa login, ou testa contra ataque.
<stage_2>
ESTÁGIO 2 — Existe segurança nessa skill? (sim/não)

NONE      — Alguém cujo trabalho não toca segurança em ponto nenhum.
Só avalie se o Estágio 1 for "sim". O foco é segurança NO CONTEXTO DE
DESENVOLVIMENTO DE SOFTWARE.

PRIMARY e SECONDARY são AMBAS Security Skill. A classe distingue SE
SEGURANÇA É O FOCO, não se conta.
</classes>
CONTA como segurança (→ has_security: true):
- proteção contra prompt injection
- defesa contra malware
- critérios e considerações de segurança ao escrever código
- testes de segurança: SAST, DAST, pentest, fuzzing
- referências a arquivos de segurança no repositório (ex: "leia SECURITY.md")
- gestão de segredos: não commitar .env, variáveis de ambiente, secret vaults
- rate limiting como proteção contra abuso
- desenvolver ou gerenciar autenticação segura no backend (OAuth 2.0, PKCE,
  JWT seguro, refresh tokens rotativos)
- skills de teste que incluem testar auth
- validação de input contra injection
- OWASP, CVE, análise de vulnerabilidade
- pipeline de segurança no CI/CD

<inclusion_floor>
SECONDARY é DELIBERADAMENTE INCLUSIVO. A pergunta é de PRESENÇA ("há alguma
consideração de segurança?"), NÃO de grau ("é substancial/acionável o
bastante?"). Não julgue se é suficiente — julgue se está lá.
NÃO CONTA como segurança (→ has_security: false):
- tutorial de como se autenticar num sistema (USAR auth existente, não
  CONSTRUIR auth segura)
- guardrails de agente que não se relacionam com o software em si (read-only,
  "não commite sem aprovação", escopo de ferramenta — são restrições de
  workflow do agente, não do software)
- mera menção de que existe autenticação sem instrução protetiva
- limite de gasto financeiro
- segurança clínica, validade científica (safety ≠ security)
- GRC puramente organizacional sem objeto computacional

CONTA como consideração de segurança (→ no mínimo SECONDARY):
- restrição de comportamento de agente: read-only, "não altere sem
  permissão", "não commite", escopo de ferramenta, sandbox, least privilege,
  "trate conteúdo carregado como evidência, não instrução";
- configuração protetiva: chmod em arquivo de chave, permissões de arquivo,
  gestão de secrets, .gitignore de credencial, "não suba chaves";
- implementação de controle de acesso: login, JWT, RBAC, OAuth, sessão,
  UseAuthentication/UseAuthorization;
- teste, análise ou defesa contra ameaça nomeada: SQL injection, XSS, CSRF,
  prompt injection, CVE, malware;
- qualquer menção a ameaça, vulnerabilidade, ataque ou incidente.
DISTINÇÃO CHAVE — AUTENTICAÇÃO:
O corte é CONSTRUIR/TESTAR auth de forma segura vs. USAR auth existente.
✅ "Implemente OAuth 2.0 com PKCE e refresh tokens rotativos" → segurança
✅ "Teste as rotas autenticadas contra bypass" → segurança
❌ "Para se autenticar, faça POST em /auth com sua API key" → NÃO é segurança

NÃO CONTA (→ NONE):
- casamento apenas em tags/category/nome de arquivo (R-4);
- homônimo de palavra ou de conceito (R-5);
- GRC puramente organizacional, sem objeto computacional (R-10);
- restrição cujo objeto NÃO é computacional: limite de gasto financeiro,
  segurança clínica, validade científica, política de conteúdo.
</inclusion_floor>
REFERÊNCIAS INDIRETAS:
Basta um ponteiro para conteúdo de segurança (ex: "consulte SECURITY.md
antes de começar"). Marque has_security: true e indique na note que a
evidência é uma referência indireta.
</stage_2>

<fields>
Além da classe, apenas quatro campos. NÃO produza nenhum outro.
Cinco campos por caso. NÃO produza nenhum outro.

evidence — onde você viu o que decidiu: description | body |
  bundled_artifacts (multi-label; lista vazia se NONE sem evidência).
is_software_development — true se a skill participa do SDLC, false caso
  contrário. Decisão do Estágio 1.

frame_exclusion — "" em quase todos os casos. Dois valores possíveis:
  "truncated_undecidable" APENAS quando o texto referencia um
  script/arquivo indisponível SEM o qual é impossível decidir se há
  consideração de segurança.
  "not_an_instruction_artifact" quando o arquivo não é instrução, e sim
  saída gerada. Ver R-9.
has_security — true se há presença de segurança no contexto de SDLC, false
  se não há. null APENAS quando is_software_development for false (o
  Estágio 2 não se aplica). Decisão do Estágio 2.

confidence — high | medium | low. Sua certeza. É metadado de triagem,
  não entra em nenhum cálculo; seja honesto em vez de conservador.
evidence — onde você viu o que decidiu: description | body |
  bundled_artifacts (multi-label; lista vazia se não há evidência de
  segurança).

note — a justificativa, e o campo MAIS IMPORTANTE depois da classe.
  Escreva UMA frase contendo TRÊS elementos:
    (1) o papel profissional — "seria um analista de malware", "seria um
        designer gráfico";
    (2) qual é o conteúdo de segurança, em termos próximos ao texto
        observado — ou, se NONE, POR QUE não conta (homônimo de palavra?
        de conceito? objeto não computacional? só etiqueta?);
    (3) o elemento concreto que sustenta — o trecho, o comando, a seção.
confidence — high | medium | low. Sua certeza na classificação completa
  (ambos estágios). Seja honesto em vez de conservador.

  A nota será lida em bloco depois, junto com as demais, para derivar as
  categorias da taxonomia. Descreva a preocupação em termos próximos ao
  texto, NÃO tente encaixá-la numa categoria conhecida — a normalização é
  feita depois, com o corpus inteiro à vista.
note — a justificativa, e o campo MAIS IMPORTANTE. Escreva UMA a DUAS
  frases contendo:
    (1) o que a skill faz (ex: "skill de backend em Node.js");
    (2) por que é ou não é desenvolvimento de software;
    (3) qual conteúdo de segurança existe, ou por que nenhum se aplica.
</fields>

<rules>
Aplicar em ordem; parar na primeira que decidir.
Aplicar em ordem.

R-1 — Teste do papel profissional. Se esta skill fosse uma pessoa, qual seria
      a profissão dela? Profissional de cibersegurança → PRIMARY. Outra
      profissão, mas o texto traz consideração de segurança → SECONDARY.
      Outra profissão, sem consideração alguma → NONE.
R-1 — Estágio 1: Teste de participação no SDLC. A skill trabalha com
      alguma etapa do ciclo de desenvolvimento de software? Use <stage_1>.

R-2 — Teste de presença (separa SECONDARY de NONE). A pergunta é EXISTE
      consideração de segurança, não É SUBSTANCIAL. Use <inclusion_floor>.
      NA DÚVIDA entre SECONDARY e NONE, escolha SECONDARY com
      confidence: low.
R-2 — Estágio 2: Teste de presença de segurança. Se o Estágio 1 for "sim",
      há presença de segurança no contexto de SDLC? Use <stage_2>.

R-3 — Teste de foco (separa PRIMARY de SECONDARY). Segurança organiza a
      skill e as demais dimensões são subordinadas → PRIMARY. Segurança é uma
      entre várias dimensões, ou aparece dentro de um objetivo maior →
      SECONDARY. Proporção textual isolada não decide: scanner curto é
      PRIMARY; skill longa com um parágrafo de segurança é SECONDARY.
R-3 — Locus da evidência. Casamento apenas em tags, category, nome de
      arquivo ou lista de "related skills" NÃO conta como evidência de
      segurança.

R-4 — Locus da evidência. Casamento apenas em tags, category, nome de arquivo
      ou lista de "related skills" NÃO conta.

R-5 — Homônimos. Termo de segurança em sentido não-securitário não conta.
R-4 — Homônimos. Termo de segurança em sentido não-securitário não conta.
      De palavra: "audit" como auditoria de anúncios; "token" como token de
      LLM; "permission" como permissão de UX.
      De conceito: safety ≠ security; guardrail de qualidade ≠ guardrail de
      segurança; limite de gasto ≠ controle de acesso. Decide-se pelo OBJETO
      PROTEGIDO: precisa ser sistema computacional.

R-6 — Artefatos associados. Se o texto indica script que executa função de
R-5 — Artefatos associados. Se o texto indica script que executa função de
      segurança, classifique pelo comportamento conjunto e marque
      evidence: bundled_artifacts. Se o script é necessário e não está
      disponível: classifique pela evidência restante com confidence: low.
      Só se o texto restante NÃO permitir decidir, marque
      frame_exclusion: "truncated_undecidable".
      evidence: bundled_artifacts.

R-7 — Objeto protegido não restringe a classe. Vale para código, infra,
      agente/harness ou a própria skill — desde que computacional.
R-6 — Idioma. O idioma do texto NUNCA decide a classificação.

R-10 — Escopo de GRC. Governança, risco e conformidade entram apenas quando a
      atividade incide sobre propriedades de segurança de sistemas
      computacionais. Dentro: auditoria de IAM, revisão de política de
      acesso, avaliação de risco de dependência, conformidade que inspeciona
      configuração ou código. Fora: questionário contratual de fornecedor,
      conformidade regulatória sem objeto computacional, gestão de risco
      corporativo → NONE.
R-7 — Escopo de GRC. Governança, risco e conformidade entram apenas quando
      a atividade incide sobre propriedades de segurança de sistemas
      computacionais. Fora: questionário contratual, conformidade regulatória
      sem objeto computacional.

R-9 — Não é instrução. Antes de classificar, pergunte: este arquivo diz a um
      executor O QUE FAZER, ou relata O QUE JÁ FOI FEITO? Se é saída gerada —
      relatório, log, dump de resultados, documento de contexto produzido por
      um workflow — marque frame_exclusion: "not_an_instruction_artifact" e
      classifique mesmo assim, explicando na note.
      Sinais, quase sempre no topo: "Generated:", "Date Range:", "Input Type:",
      "Source:", "Document Metadata", "Analysis date"; resultados com data,
      link, score, nome/versão do modelo; prosa toda no passado, relatando.
      ATENÇÃO: name/description vazios NÃO são motivo de exclusão. A maioria
      desses arquivos é skill legítima com front matter fora da spec — o
      front matter pode aparecer intacto algumas linhas abaixo. Julgue o
      CONTEÚDO. Na dúvida entre "skill mal formatada" e "saída gerada", é
      skill.
R-8 — Não é instrução. Se o arquivo é saída gerada (relatório, log, dump),
      não é instrução para um executor: marque is_software_development: false
      e explique na note.

R-8 — Fechamento. NÃO existe classe de dúvida. Evidência suficiente com
      limite discutível → SECONDARY, confidence: low. Evidência insuficiente
      para decidir → frame_exclusion, nunca uma classe.
R-9 — Fechamento. NÃO existe campo de dúvida. Decida de forma binária
      cada estágio. Na dúvida no Estágio 2, marque has_security: true com
      confidence: low — o custo de incluir demais é recuperável, o de
      excluir demais não.
</rules>

<examples>
<example id="EX01">
  <input>
    name: performing-malware-ioc-extraction
    description: Analyzing malicious software to identify actionable indicators of compromise including file hashes, network indicators (C2 domains, IPs, URLs), registry modifications, mutex names.
    name: cybersec-testing-ransomware-recovery
    description: Test and validate ransomware recovery procedures including
      backup restore operations, RTO/RPO target verification, recovery
      sequence validation.
    body: |
      Static analysis with PE parsing and string extraction, dynamic analysis
      with sandbox detonation, automated IOC extraction using YARA, formatting
      results as STIX 2.1 indicators.
      Automated testing of backup restoration, simulated ransomware
      encryption, validation of recovery time objectives, tabletop
      exercises for incident response teams.
  </input>
  <output>
    {"case_id":"EX01","security_relevance":"PRIMARY",
    "evidence":["description","body"],"frame_exclusion":"","confidence":"high",
    "note":"Analista de malware: segurança é a profissão da skill; a seção de extração prescreve YARA e saída em STIX 2.1."}
    {"case_id":"EX01","is_software_development":true,"has_security":true,
    "evidence":["description","body"],"confidence":"high",
    "note":"Skill de teste de recuperação contra ransomware: é desenvolvimento/teste (SDLC) e segurança é o foco central — simulação de criptografia ransomware e validação de RTO/RPO."}
  </output>
</example>

<example id="EX02">
  <input>
    name: code-review
    description: Review code across every judgment lens in one pass.
    body: |
      Lenses: code-kiss, code-dry, code-early-return, code-solid, code-smells,
      code-no-keys (no hardcoded secrets), code-no-credentials (no embedded
      logins / plaintext passwords). Also check OWASP Top 10: injection, XSS,
      CSRF, broken authorization.
  </input>
  <output>
    {"case_id":"EX02","security_relevance":"SECONDARY",
    "evidence":["body"],"frame_exclusion":"","confidence":"high",
    "note":"Dev revisor de código: o propósito é revisão geral, mas há uma lente dedicada a OWASP Top 10 nomeando injection, XSS, CSRF e authz quebrada."}
    {"case_id":"EX02","is_software_development":true,"has_security":true,
    "evidence":["body"],"confidence":"high",
    "note":"Skill de revisão de código (SDLC): entre as lentes de revisão há checagens de segurança — OWASP Top 10, no-hardcoded-secrets, no-credentials, injection, XSS, CSRF."}
  </output>
</example>

<example id="EX03">
  <input>
    name: gemini-cli-runtime
    description: Internal helper contract for calling the gemini-companion runtime.
    name: database-migration
    description: Create and manage database migrations for schema changes.
    body: |
      Execution rules: the rescue subagent is a forwarder, not an orchestrator.
      Do not call setup, review, status or cancel. Do not inspect the repo or
      solve the task yourself. The Gemini CLI runs read-only via headless -p.
      Generate migration files with proper naming conventions. Include
      up/down methods. Validate foreign keys and indexes. Run migrate
      and rollback commands. Check for breaking changes in production.
  </input>
  <output>
    {"case_id":"EX03","security_relevance":"SECONDARY",
    "evidence":["body"],"frame_exclusion":"","confidence":"low",
    "note":"Restrição de comportamento de agente (read-only, escopo de subcomando) conta como consideração de segurança por PRESENÇA, ainda que o propósito seja encaminhar trabalho."}
    {"case_id":"EX03","is_software_development":true,"has_security":false,
    "evidence":[],"confidence":"high",
    "note":"Skill de migração de banco (SDLC): valida foreign keys e indexes, roda rollback — tudo é processo de desenvolvimento, sem nenhuma consideração de segurança."}
  </output>
</example>

<example id="EX04">
  <input>
    name: openclaw-1ly-payments
    description: Integration for payments; covers MCP server setup, wallet env vars, budget limits.
    name: retro-smile
    description: Generate a photorealistic analog-film street portrait of a
      teenager on a subway platform.
    body: |
      ## Guardrails
      - Auto-spend when within ONELY_BUDGET_PER_CALL and ONELY_BUDGET_DAILY.
      - Keep wallet keys local; do not upload keys.
      - Secure wallet file permissions: chmod 600 /path/to/wallet.json
      Capture as if on a disposable camera from the 1990s. Natural light,
      slight grain, warm tones. Subject smiling, candid pose.
  </input>
  <output>
    {"case_id":"EX04","security_relevance":"SECONDARY",
    "evidence":["body"],"frame_exclusion":"","confidence":"medium",
    "note":"Propósito é pagamento, mas chmod 600 em chave privada é configuração protetiva presente. O limite de gasto NÃO conta (objeto financeiro, não computacional, R-5)."}
    {"case_id":"EX04","is_software_development":false,"has_security":null,
    "evidence":[],"confidence":"high",
    "note":"Skill de geração de imagem: não participa do SDLC em nenhuma etapa. Estágio 2 não se aplica."}
  </output>
</example>

<example id="EX05">
  <input>
    name: meta-ads-audit
    description: Audit Meta advertising campaigns for performance and budget efficiency.
    body: |
      Review ad sets, check spend pacing, flag underperforming creatives,
      produce an audit report with recommendations.
  </input>
  <output>
    {"case_id":"EX05","security_relevance":"NONE",
    "evidence":[],"frame_exclusion":"","confidence":"high",
    "note":"'Audit' aqui é auditoria de anúncios, homônimo de palavra. Nenhuma consideração de segurança computacional."}
  </output>
</example>

<example id="EX06">
  <input>
    name: draft-vendor-onboarding-questionnaire
    description: Draft a vendor onboarding questionnaire covering contracts, insurance, sanctions and business continuity.
    description: Draft a vendor onboarding questionnaire covering contracts,
      insurance, sanctions and business continuity.
    body: |
      Sections: corporate identity, contractual terms, insurance coverage,
      sanctions screening, business continuity plan, information security
      policy attestation.
  </input>
  <output>
    {"case_id":"EX06","security_relevance":"NONE",
    "evidence":[],"frame_exclusion":"","confidence":"medium",
    "note":"GRC puramente organizacional: questionário contratual, sem inspeção de configuração ou código. R-10 manda NONE."}
    {"case_id":"EX05","is_software_development":false,"has_security":null,
    "evidence":[],"confidence":"high",
    "note":"Skill de GRC organizacional: questionário contratual de fornecedor. Menciona 'information security' mas como atestação documental, sem objeto computacional. Não é desenvolvimento de software."}
  </output>
</example>

<example id="EX07">
<example id="EX06">
  <input>
    name: scientific-discovery-agents
    description: Guidelines for biomedical discovery agents.
    name: api-integration-helper
    description: Helper for integrating third-party APIs into the backend.
    body: |
      Define explicit tool and data boundaries, stopping rules, human
      checkpoints before publishing, and guardrails against leakage between
      train and validation cohorts.
      Set up HTTP client with retry logic. Configure API key from environment
      variable. Make authenticated requests using Bearer token. Parse JSON
      responses. Handle rate limiting and pagination.
  </input>
  <output>
    {"case_id":"EX07","security_relevance":"NONE",
    "evidence":[],"frame_exclusion":"","confidence":"low",
    "note":"'Guardrail' e 'leakage' aqui têm objeto não computacional (validade científica e segurança clínica). Homônimo de conceito, R-5."}
    {"case_id":"EX06","is_software_development":true,"has_security":false,
    "evidence":[],"confidence":"medium",
    "note":"Skill de integração de API no backend (SDLC): configura API key de env var e faz requests autenticadas, mas é tutorial de COMO USAR auth existente, não de como construir auth segura. Gestão de segredos aqui é apenas configuração operacional, não instrução protetiva."}
  </output>
</example>
</examples>

<output_format>
Um objeto JSON por caso, um por linha (JSONL), na ordem dos case_id.
Nenhum texto fora dos objetos JSON. Todos os campos são obrigatórios.

{"case_id":"...","security_relevance":"PRIMARY|SECONDARY|NONE",
"evidence":[...],"frame_exclusion":"","confidence":"high|medium|low",
"note":"papel profissional + qual e o conteudo de seguranca (ou por que nao conta) + o elemento concreto"}
{"case_id":"...","is_software_development":true|false,
"has_security":true|false|null,
"evidence":[...],"confidence":"high|medium|low",
"note":"o que a skill faz + por que é/não é dev de software + qual segurança existe ou por que não"}

frame_exclusion: use "" (vazio) em quase todos os casos. Use
"not_an_instruction_artifact" quando o arquivo for saída gerada e não
instrução (R-9). Use
"truncated_undecidable" APENAS quando o texto referencia um script/arquivo
indisponível SEM o qual é impossível decidir se há consideração de segurança
— e nesse caso security_relevance deve ser "NONE" e será descartado depois.
has_security: use null APENAS quando is_software_development for false.
</output_format>

<constraints>
- Não leia nenhum arquivo fora de results/EXP-013_llm_cases/.
- Não leia nenhum arquivo fora de results/llm_cases/.
- Não pule casos, não amostre, não agrupe.
- Não ajuste seu critério ao longo do lote.
- Idioma do texto NUNCA decide a classe.
- Na dúvida entre SECONDARY e NONE: SECONDARY com confidence low.
- Idioma do texto NUNCA decide a classificação.
- Na dúvida no Estágio 2: has_security true com confidence low.
- Escreva a saída em UM arquivo JSONL, com TODOS os casos. Verifique ao final
  que o número de linhas é igual ao número de arquivos do diretório.
</constraints>
```

---

## 2. Schema JSON

```json
{
  "type": "object",
  "properties": {
    "case_id": {"type": "string"},
    "security_relevance": {"type": "string", "enum": ["PRIMARY", "SECONDARY", "NONE"]},
    "evidence": {"type": "array", "items": {"type": "string", "enum": ["description", "body", "bundled_artifacts"]}},
    "frame_exclusion": {"type": "string",
                        "enum": ["", "truncated_undecidable",
                                 "not_an_instruction_artifact"]},
    "is_software_development": {"type": "boolean"},
    "has_security": {"type": ["boolean", "null"]},
    "evidence": {
      "type": "array",
      "items": {"type": "string", "enum": ["description", "body", "bundled_artifacts"]}
    },
    "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
    "note": {"type": "string", "minLength": 40}
  },
  "required": ["case_id", "security_relevance", "evidence", "frame_exclusion", "confidence", "note"],
  "required": ["case_id", "is_software_development", "has_security", "evidence", "confidence", "note"],
  "additionalProperties": false
}
```

> [!warning] Conformidade de schema — falha conhecida
> No [[EXP-013]], **nenhum dos três modelos** preencheu `possible_non_english`,
> que era campo obrigatório do schema da v2.3 — falha simétrica, provavelmente
> porque as sessões de CLI receberam só a versão narrativa do prompt, sem
> validação estrita. Ao rodar esta versão, **conferir campo a campo na primeira
> saída** antes de processar o lote inteiro, e conferir que o número de linhas
> do JSONL bate com o número de arquivos.

---

## 3. Execução no re-teste (2 modelos)
## 3. Execução (2 modelos)

Decisão do pesquisador (2026-09-03): rodar o re-teste com **Claude Opus e
GPT** apenas — cota do Gemini esgotada — e adjudicar manualmente **toda**
divergência.
Mantém o desenho do D-026: dois modelos (Claude + GPT), adjudicação humana
em toda divergência. Com dois avaliadores, a estatística é Cohen's κ.

Consequências metodológicas:
Diferença em relação ao EXP-014: o κ é calculado **por estágio** (dois valores
binários), não por classificação de três classes.

- Com dois avaliadores a estatística é **Cohen's κ**, não Fleiss'.
- Não existe regra de maioria: toda divergência vai para o humano. É mais
  limpo que o desenho de três, não menos.
- A comparação com a v2.3 só é válida sobre **os mesmos 100 casos** do
  [[EXP-013]]. Não trocar a amostra.
- Ao comparar, usar o κ de duas vias da v2.3 entre os mesmos dois modelos —
  não o Fleiss' de três, que não é comparável.
Saída de cada modelo em `results/EXP-018_{claude,gpt}_output.jsonl`.

Saída de cada modelo em `results/EXP-014_{claude,gpt}_output.jsonl`.
---

## 4. Nota sobre exemplos

> [!important] Exemplos de fora da amostra
> Todos os exemplos deste prompt (EX01 a EX06) usam skills que **NÃO
> pertencem à amostra** que será classificada. Isso corrige o data leakage
> identificado no prompt v2.6, onde 6 dos 7 exemplos estavam na amostra
> de 100 casos do EXP-013.
>
> Fontes dos exemplos:
> - EX01: `cybersec-testing-ransomware-recovery` (âncora do Codebook)
> - EX02: `code-review` (conteúdo mais frequente do dataset, não sorteado)
> - EX03: `database-migration` (skill genérica de SDLC)
> - EX04: `retro-smile` (geração de imagem, não-dev)
> - EX05: `draft-vendor-onboarding-questionnaire` (GRC organizacional)
> - EX06: Exemplo sintético de integração de API (caso ambíguo auth)

---

## Ligações

[[Codebook]] (v2.6) · [[Decision Log#D-027]] · [[Decision Log#D-028]] ·
[[Decision Log#D-030]] ·
[[Guia do Anotador Humano]] · [[EXP-013]] ·
[[Classification Prompt (D-026)]] (versão anterior, v2.3)
[[Codebook]] (v3.0) · [[Decision Log#D-034]] · [[Decision Log#D-035]] ·
[[Classification Prompt (D-026)]] (v2.3, histórico) ·
[[EXP-013]] (amostra anterior)
