---
tipo: instrumento
questao: QI-1
data: 2026-09-05
decisoes: D-027, D-028, D-029, D-030, D-021
substitui: Classification Prompt (D-026)
status: classe validada no EXP-014 (κ=0,724); payload reduzido por D-029 ainda não testado
---

# Prompt de classificação — Codebook v2.6

Substitui [[Classification Prompt (D-026)]], que implementava o esquema de
cinco classes do Codebook v2.3. Aquele arquivo permanece por rastreabilidade —
os resultados do [[EXP-013]] foram produzidos sob ele.

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

**Restrição de acesso:** leia apenas os arquivos dentro de
`results/EXP-013_llm_cases/`. Não leia, liste nem acesse nenhum outro
arquivo ou diretório deste repositório.

Ao final de cada caso, responda apenas com o objeto JSON de <output_format>.
</task>

<definition>
Security Skill: uma Agent Skill cujo propósito principal, OU parte de seu
comportamento descrito, envolve prevenir, detectar, analisar, avaliar,
explorar, mitigar ou responder a ameaças, vulnerabilidades, violações de
propriedades de segurança ou controles de acesso em SISTEMAS
COMPUTACIONAIS.

Presença de vocabulário de segurança nunca basta por si só — considere
propósito declarado, comportamento, atividade orientada ou executada,
resultado esperado, contexto e artefatos associados.

A definição é neutra quanto à postura: pentest, exploit dev e CTF são
Security Skills tanto quanto um scanner defensivo.
</definition>

<classes>
A decisão de classe é feita por ANALOGIA DE PAPEL PROFISSIONAL:
se esta skill fosse uma pessoa, qual seria a profissão dela, e o que ela
faria a respeito de segurança?

PRIMARY   — Um profissional de cibersegurança. Segurança é o propósito da
            skill; ela existe para isso.
            Exemplo de analogia: alguém contratado para caçar SQL injection,
            analisar malware, fazer pentest.

SECONDARY — Um profissional de outra especialidade cujo trabalho descrito
            traz alguma consideração de segurança. O propósito da skill é
            outro, mas segurança aparece.
            Exemplo de analogia: um dev construindo uma feature que também
            configura permissões, implementa login, ou testa contra ataque.

NONE      — Alguém cujo trabalho não toca segurança em ponto nenhum.

PRIMARY e SECONDARY são AMBAS Security Skill. A classe distingue SE
SEGURANÇA É O FOCO, não se conta.
</classes>

<inclusion_floor>
SECONDARY é DELIBERADAMENTE INCLUSIVO. A pergunta é de PRESENÇA ("há alguma
consideração de segurança?"), NÃO de grau ("é substancial/acionável o
bastante?"). Não julgue se é suficiente — julgue se está lá.

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

NÃO CONTA (→ NONE):
- casamento apenas em tags/category/nome de arquivo (R-4);
- homônimo de palavra ou de conceito (R-5);
- GRC puramente organizacional, sem objeto computacional (R-10);
- restrição cujo objeto NÃO é computacional: limite de gasto financeiro,
  segurança clínica, validade científica, política de conteúdo.
</inclusion_floor>

<fields>
Além da classe, apenas quatro campos. NÃO produza nenhum outro.

evidence — onde você viu o que decidiu: description | body |
  bundled_artifacts (multi-label; lista vazia se NONE sem evidência).

frame_exclusion — "" em quase todos os casos. Dois valores possíveis:
  "truncated_undecidable" APENAS quando o texto referencia um
  script/arquivo indisponível SEM o qual é impossível decidir se há
  consideração de segurança.
  "not_an_instruction_artifact" quando o arquivo não é instrução, e sim
  saída gerada. Ver R-9.

confidence — high | medium | low. Sua certeza. É metadado de triagem,
  não entra em nenhum cálculo; seja honesto em vez de conservador.

note — a justificativa, e o campo MAIS IMPORTANTE depois da classe.
  Escreva UMA frase contendo TRÊS elementos:
    (1) o papel profissional — "seria um analista de malware", "seria um
        designer gráfico";
    (2) qual é o conteúdo de segurança, em termos próximos ao texto
        observado — ou, se NONE, POR QUE não conta (homônimo de palavra?
        de conceito? objeto não computacional? só etiqueta?);
    (3) o elemento concreto que sustenta — o trecho, o comando, a seção.

  A nota será lida em bloco depois, junto com as demais, para derivar as
  categorias da taxonomia. Descreva a preocupação em termos próximos ao
  texto, NÃO tente encaixá-la numa categoria conhecida — a normalização é
  feita depois, com o corpus inteiro à vista.
</fields>

<rules>
Aplicar em ordem; parar na primeira que decidir.

R-1 — Teste do papel profissional. Se esta skill fosse uma pessoa, qual seria
      a profissão dela? Profissional de cibersegurança → PRIMARY. Outra
      profissão, mas o texto traz consideração de segurança → SECONDARY.
      Outra profissão, sem consideração alguma → NONE.

R-2 — Teste de presença (separa SECONDARY de NONE). A pergunta é EXISTE
      consideração de segurança, não É SUBSTANCIAL. Use <inclusion_floor>.
      NA DÚVIDA entre SECONDARY e NONE, escolha SECONDARY com
      confidence: low.

R-3 — Teste de foco (separa PRIMARY de SECONDARY). Segurança organiza a
      skill e as demais dimensões são subordinadas → PRIMARY. Segurança é uma
      entre várias dimensões, ou aparece dentro de um objetivo maior →
      SECONDARY. Proporção textual isolada não decide: scanner curto é
      PRIMARY; skill longa com um parágrafo de segurança é SECONDARY.

R-4 — Locus da evidência. Casamento apenas em tags, category, nome de arquivo
      ou lista de "related skills" NÃO conta.

R-5 — Homônimos. Termo de segurança em sentido não-securitário não conta.
      De palavra: "audit" como auditoria de anúncios; "token" como token de
      LLM; "permission" como permissão de UX.
      De conceito: safety ≠ security; guardrail de qualidade ≠ guardrail de
      segurança; limite de gasto ≠ controle de acesso. Decide-se pelo OBJETO
      PROTEGIDO: precisa ser sistema computacional.

R-6 — Artefatos associados. Se o texto indica script que executa função de
      segurança, classifique pelo comportamento conjunto e marque
      evidence: bundled_artifacts. Se o script é necessário e não está
      disponível: classifique pela evidência restante com confidence: low.
      Só se o texto restante NÃO permitir decidir, marque
      frame_exclusion: "truncated_undecidable".

R-7 — Objeto protegido não restringe a classe. Vale para código, infra,
      agente/harness ou a própria skill — desde que computacional.

R-10 — Escopo de GRC. Governança, risco e conformidade entram apenas quando a
      atividade incide sobre propriedades de segurança de sistemas
      computacionais. Dentro: auditoria de IAM, revisão de política de
      acesso, avaliação de risco de dependência, conformidade que inspeciona
      configuração ou código. Fora: questionário contratual de fornecedor,
      conformidade regulatória sem objeto computacional, gestão de risco
      corporativo → NONE.

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

R-8 — Fechamento. NÃO existe classe de dúvida. Evidência suficiente com
      limite discutível → SECONDARY, confidence: low. Evidência insuficiente
      para decidir → frame_exclusion, nunca uma classe.
</rules>

<examples>
<example id="EX01">
  <input>
    name: performing-malware-ioc-extraction
    description: Analyzing malicious software to identify actionable indicators of compromise including file hashes, network indicators (C2 domains, IPs, URLs), registry modifications, mutex names.
    body: |
      Static analysis with PE parsing and string extraction, dynamic analysis
      with sandbox detonation, automated IOC extraction using YARA, formatting
      results as STIX 2.1 indicators.
  </input>
  <output>
    {"case_id":"EX01","security_relevance":"PRIMARY",
    "evidence":["description","body"],"frame_exclusion":"","confidence":"high",
    "note":"Analista de malware: segurança é a profissão da skill; a seção de extração prescreve YARA e saída em STIX 2.1."}
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
  </output>
</example>

<example id="EX03">
  <input>
    name: gemini-cli-runtime
    description: Internal helper contract for calling the gemini-companion runtime.
    body: |
      Execution rules: the rescue subagent is a forwarder, not an orchestrator.
      Do not call setup, review, status or cancel. Do not inspect the repo or
      solve the task yourself. The Gemini CLI runs read-only via headless -p.
  </input>
  <output>
    {"case_id":"EX03","security_relevance":"SECONDARY",
    "evidence":["body"],"frame_exclusion":"","confidence":"low",
    "note":"Restrição de comportamento de agente (read-only, escopo de subcomando) conta como consideração de segurança por PRESENÇA, ainda que o propósito seja encaminhar trabalho."}
  </output>
</example>

<example id="EX04">
  <input>
    name: openclaw-1ly-payments
    description: Integration for payments; covers MCP server setup, wallet env vars, budget limits.
    body: |
      ## Guardrails
      - Auto-spend when within ONELY_BUDGET_PER_CALL and ONELY_BUDGET_DAILY.
      - Keep wallet keys local; do not upload keys.
      - Secure wallet file permissions: chmod 600 /path/to/wallet.json
  </input>
  <output>
    {"case_id":"EX04","security_relevance":"SECONDARY",
    "evidence":["body"],"frame_exclusion":"","confidence":"medium",
    "note":"Propósito é pagamento, mas chmod 600 em chave privada é configuração protetiva presente. O limite de gasto NÃO conta (objeto financeiro, não computacional, R-5)."}
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
    body: |
      Sections: corporate identity, contractual terms, insurance coverage,
      sanctions screening, business continuity plan, information security
      policy attestation.
  </input>
  <output>
    {"case_id":"EX06","security_relevance":"NONE",
    "evidence":[],"frame_exclusion":"","confidence":"medium",
    "note":"GRC puramente organizacional: questionário contratual, sem inspeção de configuração ou código. R-10 manda NONE."}
  </output>
</example>

<example id="EX07">
  <input>
    name: scientific-discovery-agents
    description: Guidelines for biomedical discovery agents.
    body: |
      Define explicit tool and data boundaries, stopping rules, human
      checkpoints before publishing, and guardrails against leakage between
      train and validation cohorts.
  </input>
  <output>
    {"case_id":"EX07","security_relevance":"NONE",
    "evidence":[],"frame_exclusion":"","confidence":"low",
    "note":"'Guardrail' e 'leakage' aqui têm objeto não computacional (validade científica e segurança clínica). Homônimo de conceito, R-5."}
  </output>
</example>
</examples>

<output_format>
Um objeto JSON por caso, um por linha (JSONL), na ordem dos case_id.
Nenhum texto fora dos objetos JSON. Todos os campos são obrigatórios.

{"case_id":"...","security_relevance":"PRIMARY|SECONDARY|NONE",
"evidence":[...],"frame_exclusion":"","confidence":"high|medium|low",
"note":"papel profissional + qual e o conteudo de seguranca (ou por que nao conta) + o elemento concreto"}

frame_exclusion: use "" (vazio) em quase todos os casos. Use
"not_an_instruction_artifact" quando o arquivo for saída gerada e não
instrução (R-9). Use
"truncated_undecidable" APENAS quando o texto referencia um script/arquivo
indisponível SEM o qual é impossível decidir se há consideração de segurança
— e nesse caso security_relevance deve ser "NONE" e será descartado depois.
</output_format>

<constraints>
- Não leia nenhum arquivo fora de results/EXP-013_llm_cases/.
- Não pule casos, não amostre, não agrupe.
- Não ajuste seu critério ao longo do lote.
- Idioma do texto NUNCA decide a classe.
- Na dúvida entre SECONDARY e NONE: SECONDARY com confidence low.
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
    "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
    "note": {"type": "string", "minLength": 40}
  },
  "required": ["case_id", "security_relevance", "evidence", "frame_exclusion", "confidence", "note"],
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

Decisão do pesquisador (2026-09-03): rodar o re-teste com **Claude Opus e
GPT** apenas — cota do Gemini esgotada — e adjudicar manualmente **toda**
divergência.

Consequências metodológicas:

- Com dois avaliadores a estatística é **Cohen's κ**, não Fleiss'.
- Não existe regra de maioria: toda divergência vai para o humano. É mais
  limpo que o desenho de três, não menos.
- A comparação com a v2.3 só é válida sobre **os mesmos 100 casos** do
  [[EXP-013]]. Não trocar a amostra.
- Ao comparar, usar o κ de duas vias da v2.3 entre os mesmos dois modelos —
  não o Fleiss' de três, que não é comparável.

Saída de cada modelo em `results/EXP-014_{claude,gpt}_output.jsonl`.

---

## Ligações

[[Codebook]] (v2.6) · [[Decision Log#D-027]] · [[Decision Log#D-028]] ·
[[Decision Log#D-030]] ·
[[Guia do Anotador Humano]] · [[EXP-013]] ·
[[Classification Prompt (D-026)]] (versão anterior, v2.3)
