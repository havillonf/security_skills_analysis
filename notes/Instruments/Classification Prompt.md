---
tipo: instrumento
questao: QI-1
data: 2026-09-21
decisoes: D-034, D-035
substitui: Classification Prompt v2.6 (D-027/D-028/D-029/D-030)
status: em construção — aguardando validação em nova amostra
---

# Prompt de classificação — Codebook v3.0

Substitui o prompt v2.6, que implementava o esquema de três classes. Aquele
arquivo permanece no histórico por rastreabilidade.

> [!important] O que mudou em relação ao prompt v2.6
> 1. **Dois estágios binários** em vez de três classes. Estágio 1: é
>    desenvolvimento de software? Estágio 2: existe segurança?
> 2. Definição de segurança **restrita ao contexto de SDLC** (D-035).
> 3. **Exemplos vindos de fora da amostra** — corrige o data leakage
>    identificado na v2.6 (6 dos 7 exemplos estavam na amostra de 100).
> 4. Output simplificado: dois campos binários + evidence + confidence + note.
> 5. Não há distinção entre segurança como foco principal ou secundário —
>    a classificação é binária: há ou não há segurança.

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
No diretório <cases_dir>results/llm_cases/</cases_dir> há um arquivo
`.md` por caso, cada um com este formato:

  case_id: LLM001
  name: <nome da skill ou vazio>
  description: <descrição ou vazio>
  ---

  <corpo completo do SKILL.md>

Para CADA arquivo do diretório, classifique a skill segundo o instrumento
abaixo, aplicando os dois estágios na ordem indicada. Processe TODOS os
arquivos, um a um, em ordem alfabética (LLM001, LLM002, ...) — não pule
nenhum, não amostre, não resuma vários casos juntos. Trate cada caso como
totalmente independente: a classificação de um caso não deve influenciar a
de outro.

**Restrição de acesso:** leia apenas os arquivos dentro de
`results/llm_cases/`. Não leia, liste nem acesse nenhum outro
arquivo ou diretório deste repositório.

Ao final de cada caso, responda apenas com o objeto JSON de <output_format>.
</task>

<stage_1>
ESTÁGIO 1 — É skill de desenvolvimento de software? (sim/não)

Entende-se por "desenvolvimento de software" todo o ciclo de vida (SDLC):
requisitos, frontend, backend, banco de dados, infraestrutura, DevOps,
CI/CD, observabilidade, segurança, testes, arquitetura, documentação técnica.

CONTA como desenvolvimento de software (→ is_software_development: true):
- Skills que trabalham com qualquer etapa do SDLC
- Skills de DevOps, CI/CD, observabilidade
- Skills de documentação técnica (README, API docs)
- Skills que constroem, testam ou deployam software
- Se uma skill trabalha com qualquer etapa do SDLC E menciona guardrails
  de agente, ela ENTRA — o guardrail não a desclassifica

NÃO CONTA como desenvolvimento de software (→ is_software_development: false):
- Skills puramente de orquestração de agente sem produção de software
- Marketing, design gráfico, produção de vídeo
- Pesquisa acadêmica não computacional
- Gestão financeira, RH
- GRC sem objeto computacional

Se is_software_development for false, marque has_security como null e
explique na note por que a skill não é de desenvolvimento de software.
</stage_1>

<stage_2>
ESTÁGIO 2 — Existe segurança nessa skill? (sim/não)

Só avalie se o Estágio 1 for "sim". O foco é segurança NO CONTEXTO DE
DESENVOLVIMENTO DE SOFTWARE. Não distinguimos se segurança é o foco
principal ou secundário — apenas se há ou não há presença de segurança.

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

DISTINÇÃO CHAVE — AUTENTICAÇÃO:
O corte é CONSTRUIR/TESTAR auth de forma segura vs. USAR auth existente.
✅ "Implemente OAuth 2.0 com PKCE e refresh tokens rotativos" → segurança
✅ "Teste as rotas autenticadas contra bypass" → segurança
❌ "Para se autenticar, faça POST em /auth com sua API key" → NÃO é segurança

REFERÊNCIAS INDIRETAS:
Basta um ponteiro para conteúdo de segurança (ex: "consulte SECURITY.md
antes de começar"). Marque has_security: true e indique na note que a
evidência é uma referência indireta.
</stage_2>

<fields>
Cinco campos por caso. NÃO produza nenhum outro.

is_software_development — true se a skill participa do SDLC, false caso
  contrário. Decisão do Estágio 1.

has_security — true se há presença de segurança no contexto de SDLC, false
  se não há. null APENAS quando is_software_development for false (o
  Estágio 2 não se aplica). Decisão do Estágio 2.

evidence — onde você viu o que decidiu: description | body |
  bundled_artifacts (multi-label; lista vazia se não há evidência de
  segurança).

confidence — high | medium | low. Sua certeza na classificação completa
  (ambos estágios). Seja honesto em vez de conservador.

note — a justificativa, e o campo MAIS IMPORTANTE. Escreva UMA a DUAS
  frases contendo:
    (1) o que a skill faz (ex: "skill de backend em Node.js");
    (2) por que é ou não é desenvolvimento de software;
    (3) qual conteúdo de segurança existe, ou por que nenhum se aplica.
</fields>

<rules>
Aplicar em ordem.

R-1 — Estágio 1: Teste de participação no SDLC. A skill trabalha com
      alguma etapa do ciclo de desenvolvimento de software? Use <stage_1>.

R-2 — Estágio 2: Teste de presença de segurança. Se o Estágio 1 for "sim",
      há presença de segurança no contexto de SDLC? Use <stage_2>.

R-3 — Locus da evidência. Casamento apenas em tags, category, nome de
      arquivo ou lista de "related skills" NÃO conta como evidência de
      segurança.

R-4 — Homônimos. Termo de segurança em sentido não-securitário não conta.
      De palavra: "audit" como auditoria de anúncios; "token" como token de
      LLM; "permission" como permissão de UX.
      De conceito: safety ≠ security; guardrail de qualidade ≠ guardrail de
      segurança; limite de gasto ≠ controle de acesso. Decide-se pelo OBJETO
      PROTEGIDO: precisa ser sistema computacional.

R-5 — Artefatos associados. Se o texto indica script que executa função de
      segurança, classifique pelo comportamento conjunto e marque
      evidence: bundled_artifacts.

R-6 — Idioma. O idioma do texto NUNCA decide a classificação.

R-7 — Escopo de GRC. Governança, risco e conformidade entram apenas quando
      a atividade incide sobre propriedades de segurança de sistemas
      computacionais. Fora: questionário contratual, conformidade regulatória
      sem objeto computacional.

R-8 — Não é instrução. Se o arquivo é saída gerada (relatório, log, dump),
      não é instrução para um executor: marque is_software_development: false
      e explique na note.

R-9 — Fechamento. NÃO existe campo de dúvida. Decida de forma binária
      cada estágio. Na dúvida no Estágio 2, marque has_security: true com
      confidence: low — o custo de incluir demais é recuperável, o de
      excluir demais não.
</rules>

<examples>
<example id="EX01">
  <input>
    name: cybersec-testing-ransomware-recovery
    description: Test and validate ransomware recovery procedures including
      backup restore operations, RTO/RPO target verification, recovery
      sequence validation.
    body: |
      Automated testing of backup restoration, simulated ransomware
      encryption, validation of recovery time objectives, tabletop
      exercises for incident response teams.
  </input>
  <output>
    {"case_id":"EX01","is_software_development":true,"has_security":true,
    "evidence":["description","body"],"confidence":"high",
    "note":"Skill de teste de recuperação contra ransomware: participa do SDLC (testes) e segurança está presente — simulação de criptografia ransomware e validação de RTO/RPO."}
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
    {"case_id":"EX02","is_software_development":true,"has_security":true,
    "evidence":["body"],"confidence":"high",
    "note":"Skill de revisão de código (SDLC): entre as lentes de revisão há checagens de segurança — OWASP Top 10, no-hardcoded-secrets, no-credentials, injection, XSS, CSRF."}
  </output>
</example>

<example id="EX03">
  <input>
    name: database-migration
    description: Create and manage database migrations for schema changes.
    body: |
      Generate migration files with proper naming conventions. Include
      up/down methods. Validate foreign keys and indexes. Run migrate
      and rollback commands. Check for breaking changes in production.
  </input>
  <output>
    {"case_id":"EX03","is_software_development":true,"has_security":false,
    "evidence":[],"confidence":"high",
    "note":"Skill de migração de banco (SDLC): valida foreign keys e indexes, roda rollback — tudo é processo de desenvolvimento, sem nenhuma consideração de segurança."}
  </output>
</example>

<example id="EX04">
  <input>
    name: retro-smile
    description: Generate a photorealistic analog-film street portrait of a
      teenager on a subway platform.
    body: |
      Capture as if on a disposable camera from the 1990s. Natural light,
      slight grain, warm tones. Subject smiling, candid pose.
  </input>
  <output>
    {"case_id":"EX04","is_software_development":false,"has_security":null,
    "evidence":[],"confidence":"high",
    "note":"Skill de geração de imagem: não participa do SDLC em nenhuma etapa. Estágio 2 não se aplica."}
  </output>
</example>

<example id="EX05">
  <input>
    name: draft-vendor-onboarding-questionnaire
    description: Draft a vendor onboarding questionnaire covering contracts,
      insurance, sanctions and business continuity.
    body: |
      Sections: corporate identity, contractual terms, insurance coverage,
      sanctions screening, business continuity plan, information security
      policy attestation.
  </input>
  <output>
    {"case_id":"EX05","is_software_development":false,"has_security":null,
    "evidence":[],"confidence":"high",
    "note":"Skill de GRC organizacional: questionário contratual de fornecedor. Menciona 'information security' mas como atestação documental, sem objeto computacional. Não é desenvolvimento de software."}
  </output>
</example>

<example id="EX06">
  <input>
    name: api-integration-helper
    description: Helper for integrating third-party APIs into the backend.
    body: |
      Set up HTTP client with retry logic. Configure API key from environment
      variable. Make authenticated requests using Bearer token. Parse JSON
      responses. Handle rate limiting and pagination.
  </input>
  <output>
    {"case_id":"EX06","is_software_development":true,"has_security":false,
    "evidence":[],"confidence":"medium",
    "note":"Skill de integração de API no backend (SDLC): configura API key de env var e faz requests autenticadas, mas é tutorial de COMO USAR auth existente, não de como construir auth segura. Gestão de segredos aqui é apenas configuração operacional, não instrução protetiva."}
  </output>
</example>
</examples>

<output_format>
Um objeto JSON por caso, um por linha (JSONL), na ordem dos case_id.
Nenhum texto fora dos objetos JSON. Todos os campos são obrigatórios.

{"case_id":"...","is_software_development":true|false,
"has_security":true|false|null,
"evidence":[...],"confidence":"high|medium|low",
"note":"o que a skill faz + por que é/não é dev de software + qual segurança existe ou por que não"}

has_security: use null APENAS quando is_software_development for false.
</output_format>

<constraints>
- Não leia nenhum arquivo fora de results/llm_cases/.
- Não pule casos, não amostre, não agrupe.
- Não ajuste seu critério ao longo do lote.
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
    "is_software_development": {"type": "boolean"},
    "has_security": {"type": ["boolean", "null"]},
    "evidence": {
      "type": "array",
      "items": {"type": "string", "enum": ["description", "body", "bundled_artifacts"]}
    },
    "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
    "note": {"type": "string", "minLength": 40}
  },
  "required": ["case_id", "is_software_development", "has_security", "evidence", "confidence", "note"],
  "additionalProperties": false
}
```

---

## 3. Execução (2 modelos)

Mantém o desenho do D-026: dois modelos (Claude + GPT), adjudicação humana
em toda divergência. Com dois avaliadores, a estatística é Cohen's κ.

O κ é calculado **por estágio** (duas decisões binárias independentes).

Saída de cada modelo em `results/EXP-018_{claude,gpt}_output.jsonl`.

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

[[Codebook]] (v3.0) · [[Decision Log#D-034]] · [[Decision Log#D-035]]
