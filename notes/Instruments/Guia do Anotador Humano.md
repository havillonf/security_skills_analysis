---
tipo: instrumento
questao: QI-1
data: 2026-09-23
decisoes: D-034, D-035, D-036, D-037, D-038
substitui: Guia do Anotador Humano (v2.6)
status: vigente para a anotação do EXP-019 (Codebook v3.1)
---

# Guia do Anotador Humano — Codebook v3.1

Guia prático e direto para a anotação manual dos pesquisadores (Havillon e Victor) no experimento **EXP-019**. Este guia sintetiza o [[Codebook]] **v3.1**. Em caso de qualquer divergência ou caso limítrofe complexo, **as regras formais do Codebook prevalecem**.

> [!important] Mudança Fundamental em relação às versões anteriores (D-034/D-035)
> 1. **Não existem mais as classes `PRIMARY`, `SECONDARY` e `NONE`.**
> 2. A classificação agora opera em **dois estágios binários independentes**:
>    - **Estágio 1:** É desenvolvimento de software (SDLC)? (`true` / `false`)
>    - **Estágio 2:** Há salvaguardas ou considerações de segurança no contexto de software? (`true` / `false` / `vazio`)
> 3. **A anotação é 100% humana (D-036):** Não dependemos de consenso prévio de LLM. Você anota os casos diretamente para construir o *Ground Truth* e responder à RQ1.

---

## 1. Onde estão os arquivos e como anotar

1. **Os arquivos da skill:** Estão na pasta `results/EXP-019_cases/` numerados como `CASE001.md`, `CASE002.md`, etc.
2. **Sua planilha de anotação:**
   - Havillon: `results/EXP-019_annotation_form_havillon.csv`
   - Victor: `results/EXP-019_annotation_form_victor.csv`
3. **Ordem de Anotação:** Sempre sequencial, partindo do `CASE001`.

---

## 2. Protocolo de Execução e Amostragem com Reposição (D-036, D-037)

Nossa meta estatística é obter exatamente **385 skills válidas de desenvolvimento de software (SDLC)**.

1. **Fase 1: Calibração (CASE001 a CASE040)**
   - Os pesquisadores anotam de forma **independente e cega** os primeiros **20 a 40 casos**.
   - Calculamos o índice de concordância (**Cohen's $\kappa$**) com meta de $\kappa \ge 0.80$.
   - Reconciliamos as divergências para alinhar o entendimento conceitual.
2. **Fase 2: Conclusão da Fila (Amostragem com Reposição)**
   - Continuem anotando os casos da fila.
   - **Regra de Reposição (D-037):** Se uma skill **não** for de desenvolvimento de software (`is_software_development = false`), ela é registrada, mas **descartada da cota dos 385**. Você passa para o próximo caso da fila até totalizar exatamente 385 casos onde `is_software_development = true`.

---

## 3. Estágio 1 — É desenvolvimento de software (SDLC)?

Entende-se por desenvolvimento de software **todo o ciclo de vida (SDLC)**: levantamento de requisitos, arquitetura, frontend, backend, banco de dados, infraestrutura, DevOps, CI/CD, observabilidade, segurança, testes e documentação técnica de software.

### ✅ CONTA como SDLC (`is_software_development: true`):
- Skills que escrevem, depuram, refatoram ou analisam código de programação ou scripts.
- Configuração de infraestrutura, Docker, Kubernetes, Terraform, servidores web.
- Pipelines de CI/CD, automação de build, deploy, release e versionamento semântico.
- Testes de software (unitários, integração, e2e, carga, segurança).
- Modelagem, migração ou consultas a bancos de dados e APIs.
- Documentação técnica estritamente voltada a software (README de código, Swagger/OpenAPI, documentação de arquitetura).
- Skills que tratam de guardrails de agentes ou orquestração, **desde que atuem sobre a construção ou execução de software**.

### ❌ NÃO CONTA como SDLC (`is_software_development: false`):
- Orquestração pura de agente ou produtividade pessoal sem manipulação de software.
- Criação de conteúdo: marketing, redação, design gráfico, geração de imagens/vídeos.
- Pesquisa acadêmica, médica, clínica ou científica sem código/objeto computacional.
- Gestão de RH, finanças, compras, planilhas administrativas.
- GRC corporativo puramente organizacional (compliance de fornecedores, contratos).
- Arquivos que não são instruções (logs gerados, dumps de saída — marcar como `false`).

> [!tip] Regra de Parada
> Se `is_software_development: false`, o campo `has_security` fica **vazio (nulo)** e a avaliação daquele caso se encerra.

---

## 4. Estágio 2 — Existe segurança nessa skill?

Apenas aplicável se a skill for de desenvolvimento de software (`is_software_development: true`). 
A pergunta avalia a **presença** de salvaguardas, verificações ou preocupações de segurança em sistemas computacionais ([[Decision Log#D-035]]).

### ✅ CONTA como Segurança (`has_security: true`):
- **Defesa de IA/Agente:** Proteção contra prompt injection, mitigação de vazamento de contexto sensível em LLMs.
- **Defesa contra Malware e Ameaças:** Análise ou detecção de artefatos maliciosos, ransomware, botnets.
- **Boas Práticas de Código Seguro:** Diretrizes para evitar vulnerabilidades de software (validação de entrada, sanitização, escaping).
- **Testes de Segurança:** SAST, DAST, pentesting, fuzzing, escaneamento de vulnerabilidades em dependências (SCA).
- **Gestão de Segredos:** Instruções para não versionar `.env`, uso de secret managers/vaults, variáveis de ambiente para credenciais.
- **Controle de Abuso:** Implementação de rate limiting, proteção contra DoS/brute force.
- **Construção/Gestão de Autenticação Segura:** Implementação segura de OAuth 2.0, PKCE, rotação de JWT, hashing de senhas com salt, RBAC no backend.
- **Testes de Auth:** Testar rotas autenticadas contra bypass, escalonamento de privilégios.
- **Ameaças Nomeadas:** CVEs, referências a OWASP, CWE, XSS, CSRF, SQLi, SSRF.
- **Ponteiros de Segurança:** Menções formais como *"consulte o arquivo SECURITY.md do repositório"* ou verificação de assinatura digital.

### ❌ NÃO CONTA como Segurança (`has_security: false`):
- **Uso trivial de autenticação:** Instruir o agente a passar uma API key ou fazer POST em `/login` para consumir uma API (isso é uso, não construção ou proteção).
- **Guardrails operacionais do agente:** "Não apague arquivos sem confirmação", "opere em modo read-only", "pergunte antes de rodar comandos". Isso protege contra erro do próprio agente, não contra um adversário de segurança do software.
- **Mera menção sem proteção:** Dizer que o sistema possui tela de login, sem qualquer instrução protetiva ou de segurança.
- **Segurança física, clínica ou financeira:** Limite de gastos de API, segurança de pacientes, termos de conformidade contábil.
- **Etiqueta sem substância:** Tag `category: security` num script que só formata JSON.
- **Homônimos:** *"Audit"* de performance/SEO; *"token"* como limite de janela de contexto de LLM.

> [!important] O Corte Crucial em Autenticação
> - ✅ *"Implemente OAuth 2.0 com fluxo Authorization Code + PKCE e armazene tokens de forma segura"* → **Segurança (`true`)**
> - ✅ *"Escreva testes unitários para verificar se rotas protegidas rejeitam requisições sem token"* → **Segurança (`true`)**
> - ❌ *"Para conectar ao Notion, forneça sua chave NOTION_API_KEY no cabeçalho"* → **Não é segurança (`false`)**

---

## 5. Como preencher cada coluna da planilha

| Coluna | Valores Permitidos | Instrução |
|---|---|---|
| `case_id` | Ex: `CASE001` | Preenchido automaticamente; não altere. |
| `name` | Ex: `pr-version-bump` | Preenchido automaticamente; não altere. |
| `body_chars` | Numérico | Preenchido automaticamente; tamanho do corpo. |
| `is_software_development` | `true` ou `false` | A skill atua no ciclo de desenvolvimento de software (SDLC)? |
| `has_security` | `true`, `false` ou *vazio* | Traz considerações de segurança de software? Deixe **vazio** se `is_software_development` for `false`. |
| `evidence` | `description`, `body`, `bundled_artifacts` | Onde você encontrou a evidência principal? (Pode combinar com `;`). |
| `confidence` | `high`, `medium`, `low` | Quão seguro você está do seu julgamento? Use `medium` ou `low` se for um caso de fronteira. |
| `note` | Texto livre estruturado | **Essencial.** Justifique seu raciocínio (ver estrutura abaixo). |

### Estrutura Obrigatória do Campo `note`
A anotação deve ser direta e conter três elementos:
1. **O que a skill faz:** (Ex: *"Automação para gerar changelog e versão semântica de pull requests"*).
2. **Por que é ou não é SDLC:** (Ex: *"É SDLC pois atua diretamente na etapa de release e versionamento do código"*).
3. **Conteúdo de segurança:** (Ex: *"Não possui nenhuma consideração ou salvaguarda de segurança"* OU *"Possui segurança pois valida tokens de acesso contra vazamento em logs"*).

---

## 6. Procedimento de Calibração Independente (D-031, D-036)

Para os casos de calibração (`CASE001` a `CASE040`):
1. **Trabalho Cego:** Não discuta nenhum caso com o outro anotador antes de terminar os 40 casos e salvar sua planilha.
2. **Confronto:** Rodaremos o script de medição de concordância para gerar a matriz de confusão e o $\kappa$.
3. **Reconciliação:** Reunião conjunta para discutir casos em que houve divergência. Erros de digitação ou contradição com a própria nota são ajustados; divergências conceituais são debatidas até consenso ou levadas ao orientador se persistir dúvida.

## Ligações

[[Codebook]] · [[QI-1 Methodology]] · [[QI-2 Methodology]] · [[Decision Log#D-034]] · [[Decision Log#D-035]] · [[Decision Log#D-036]] · [[Decision Log#D-037]] · [[EXP-019]]
