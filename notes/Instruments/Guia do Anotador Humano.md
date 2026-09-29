---
tipo: instrumento
questao: QI-1
data: 2026-09-29
decisoes: D-034, D-035, D-036, D-037, D-038, D-039
substitui: Guia do Anotador Humano (v3.1)
status: vigente para a anotação do EXP-019 (Codebook v3.2)
---

# Guia do Anotador Humano — Codebook v3.2

Guia prático e direto para a anotação manual dos pesquisadores (Havillon e Victor) no experimento **EXP-019**. Este guia sintetiza o [[Codebook]] **v3.2** (D-039). Em caso de qualquer divergência ou caso limítrofe complexo, **as regras formais do Codebook prevalecem**.

> [!important] O que mudou em relação à v3.1 (D-039)
> 1. **Os 40 primeiros casos (CASE001–CASE040) foram descartados da amostra.** Eles serviram como piloto de desenvolvimento do instrumento. As regras foram refinadas a partir das divergências nesses casos — incluí-los na amostra final seria contaminação codebook↔amostra.
> 2. **A calibração reinicia do CASE041** com as regras refinadas abaixo.
> 3. **Novas regras operacionais** para os dois problemas mais frequentes:
>    - **Teste do Artefato Computacional** (Estágio 1): resolve a ambiguidade tooling/meta-agente vs. SDLC.
>    - **Teste do Adversário** (Estágio 2): formaliza a distinção guardrail operacional vs. segurança.
> 4. **Novos exemplos sintéticos** em ambos os estágios.

---

## 1. Onde estão os arquivos e como anotar

1. **Os arquivos da skill:** Estão na pasta `results/EXP-019_cases/` numerados como `CASE001.md`, `CASE002.md`, etc.
2. **Sua planilha de anotação:**
   - Havillon: `results/EXP-019_annotation_form_havillon.csv`
   - Victor: `results/EXP-019_annotation_form_victor.csv`
3. **Ordem de Anotação:** Sequencial, **partindo do CASE041** (os casos CASE001–CASE040 são dados de piloto e não fazem parte da amostra).

---

## 2. Protocolo de Execução e Fases (D-036, D-037, D-039)

Nossa meta estatística é obter exatamente **385 skills válidas de desenvolvimento de software (SDLC)**.

1. **Fase 0: Piloto (CASE001–CASE040) — CONCLUÍDA**
   - Serviu para desenvolver e refinar o Codebook (v3.1 → v3.2).
   - Esses casos **não entram** na amostra final nem no cálculo de concordância.
   - As planilhas de anotação do piloto são preservadas como evidência do processo de refinamento.

2. **Fase 1: Calibração (a partir de CASE041)**
   - Os pesquisadores anotam de forma **independente e cega** entre **20 a 40 novos casos** usando o Codebook v3.2.
   - Calculamos o índice de concordância (**Cohen's $\kappa$**) com meta de $\kappa \ge 0.80$.
   - Se o limiar for atingido, esses casos **entram** na amostra final.
   - Se não, reconciliamos divergências e, se necessário, ajustamos regras (novo ciclo).

3. **Fase 2: Produção (após calibração)**
   - Continuem anotando os casos da fila.
   - **Regra de Reposição (D-037):** Se uma skill **não** for de desenvolvimento de software (`is_software_development = false`), ela é registrada, mas **descartada da cota dos 385**. Você passa para o próximo caso da fila até totalizar exatamente 385 casos onde `is_software_development = true`.

---

## 3. Estágio 1 — É desenvolvimento de software (SDLC)?

Entende-se por desenvolvimento de software **todo o ciclo de vida (SDLC)**: levantamento de requisitos de sistema, arquitetura, frontend, backend, banco de dados, infraestrutura, DevOps, CI/CD, observabilidade, segurança, testes e documentação técnica de software.

### Teste do Artefato Computacional (R-1, D-039)

> **Pergunte:** A skill instrui diretamente a **produzir, transformar, testar, deployar, monitorar ou documentar um artefato computacional** (código-fonte, binário, container, script, configuração de infra, schema de banco, pipeline de CI/CD, doc técnica de API)?

Se **sim** → `is_software_development: true`.
Se **não** → `is_software_development: false`.

### ✅ CONTA como SDLC (`is_software_development: true`):
- Skills que escrevem, depuram, refatoram ou analisam código de programação ou scripts.
- Configuração de infraestrutura, Docker, Kubernetes, Terraform, servidores web.
- Pipelines de CI/CD, automação de build, deploy, release e versionamento semântico.
- Testes de software (unitários, integração, e2e, carga, segurança).
- Modelagem, migração ou consultas a bancos de dados e APIs.
- Documentação técnica estritamente voltada a software (README de código, Swagger/OpenAPI, documentação de arquitetura).
- Ferramentas de ecossistema (npm, pip, Docker registry, Git hosting) **quando a ação faz parte de um workflow de build, release ou manutenção de dependências** (R-1a).
- Skills que tratam de guardrails de agentes — **o guardrail não desclassifica** se a skill já for SDLC por outro motivo.

### ❌ NÃO CONTA como SDLC (`is_software_development: false`):
- **Orquestração pura de agente:** gerência de memória/contexto, analytics de uso, triagem de sessão, atualização de skills do agente.
- **Design de produto genérico ou requisitos não-software:** princípios de design (Norman, gestalt, ergonomia), design de produto físico, requisitos de negócio sem artefato computacional.
- **Operação de sistemas existentes como usuário final:** executar trades em DEX, operar pipeline de bioinformática pré-construído, configurar dashboards. Usar comandos técnicos (CLI, API) **não é suficiente** — o critério é se a skill produz/mantém artefato de software.
- Criação de conteúdo: marketing, redação, design gráfico, geração de imagens/vídeos.
- Pesquisa acadêmica, médica, clínica ou científica sem código/objeto computacional.
- Gestão de RH, finanças, compras, planilhas administrativas.
- GRC corporativo puramente organizacional (compliance de fornecedores, contratos).
- Arquivos que não são instruções (logs gerados, dumps de saída — marcar como `false`).

> [!tip] Teste discriminante para design/requisitos
> Se os requisitos ou o design pudessem ser aplicados a um produto não-software (edifício, porta, formulário em papel), **não é SDLC**. Se são intrinsecamente sobre estrutura/comportamento de um sistema computacional, **é SDLC**.

> [!tip] Teste discriminante para operação vs. construção
> Se a skill opera software existente **E** simultaneamente produz ou modifica código/configuração, **é SDLC**. Se apenas opera, **não é SDLC**.

> [!tip] Regra de Parada
> Se `is_software_development: false`, o campo `has_security` fica **vazio (nulo)** e a avaliação daquele caso se encerra.

### Exemplos sintéticos — Estágio 1

| Padrão | is_sdlc | Justificativa |
|--------|---------|---------------|
| Gerencia lifecycle de workers de memória de agente IA | `false` | Orquestra agente, não produz artefato |
| Investiga falhas em sessões de agente e recomenda ajustes | `false` | Meta-agente |
| Analisa uso de tokens e custos de agente de codificação | `false` | Analytics do agente |
| Configura 2FA no npm registry para proteger publicação | `true` | Ferramenta de ecossistema em workflow de release |
| Executa swaps de tokens em DEX (DeFi) | `false` | Opera sistema financeiro como trader |
| Design cognitivo (affordances, signifiers) para portas e interfaces | `false` | Design genérico; aplicável a não-software |
| Converte PDFs acadêmicos para Markdown | `false` | Operação utilitária |
| Gera scaffolding Go, implementa e testa com TDD | `true` | Produz código-fonte |
| Code review avaliando correctness, segurança e performance | `true` | Avalia artefato de software |

---

## 4. Estágio 2 — Existe segurança nessa skill?

Apenas aplicável se a skill for de desenvolvimento de software (`is_software_development: true`). 
A pergunta avalia a **presença** de salvaguardas, verificações ou preocupações de segurança em sistemas computacionais ([[Decision Log#D-035]]).

### Teste do Adversário (R-12, D-039)

> **Pergunte:** Esta instrução protege contra uma **ameaça adversarial ou vulnerabilidade exploratável** no software/sistema produzido, ou protege contra **erro operacional do próprio agente**?

| Modelo de ameaça | Classificação |
|-----------------|---------------|
| Adversário externo / vulnerabilidade exploratável | ✅ **Segurança** |
| Erro do próprio agente durante execução | ❌ **Guardrail operacional — NÃO é segurança** |
| Dano não-adversarial (safety ≠ security) | ❌ **NÃO é segurança** |

> [!important] Instrução híbrida (R-12a)
> Quando uma instrução **simultaneamente** previne erro operacional e protege contra ameaça adversarial, classifique como **segurança**. A presença de componente de segurança prevalece.

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
- **Integridade de supply chain (D-039):** Verificação de hash/checksum de binários ou pacotes antes de instalação, pinning de versões com verificação criptográfica.
- **Trust boundaries (D-039):** Instruções para tratar dados de APIs externas, CLIs ou smart contracts como untrusted, com filtragem antes de processamento.
- **Segurança embarcada em workflows (D-039):** Skills de code review, CI/CD ou testes que incluam uma dimensão explícita de segurança (ex: "verifique SQLi, XSS, command injection"), mesmo que segurança seja apenas uma entre várias dimensões.

### ❌ NÃO CONTA como Segurança (`has_security: false`):
- **Uso trivial de autenticação:** Instruir o agente a passar uma API key ou fazer POST em `/login` para consumir uma API (isso é uso, não construção ou proteção).
- **Guardrails operacionais do agente (R-12):** "Não apague arquivos sem confirmação", "opere em modo read-only", "pergunte antes de rodar comandos", "não force-push", "não commite sem aprovação", "enabled: false para push/create-pr". Isso protege contra erro do próprio agente, não contra um adversário de segurança do software.
- **Mera menção sem proteção:** Dizer que o sistema possui tela de login, sem qualquer instrução protetiva ou de segurança.
- **Segurança física, clínica ou financeira:** Limite de gastos de API, segurança de pacientes, termos de conformidade contábil.
- **Etiqueta sem substância:** Tag `category: security` num script que só formata JSON.
- **Homônimos:** *"Audit"* de performance/SEO; *"token"* como limite de janela de contexto de LLM.

> [!important] O Corte Crucial em Autenticação
> - ✅ *"Implemente OAuth 2.0 com fluxo Authorization Code + PKCE e armazene tokens de forma segura"* → **Segurança (`true`)**
> - ✅ *"Escreva testes unitários para verificar se rotas protegidas rejeitam requisições sem token"* → **Segurança (`true`)**
> - ❌ *"Para conectar ao Notion, forneça sua chave NOTION_API_KEY no cabeçalho"* → **Não é segurança (`false`)**

### Exemplos sintéticos — Estágio 2 (Teste do Adversário)

| Instrução (padrão sintético) | has_security | Justificativa |
|------------------------------|-------------|---------------|
| "Não force-push em branches protegidas" | `false` | Guardrail: previne erro do agente |
| "Opere em modo read-only durante análise" | `false` | Guardrail: limita scope do agente |
| "Comando X é destrutivo, exija confirmação" | `false` | Guardrail: previne destruição acidental |
| "Não modifique o target durante análise" | `false` | Restrição de workflow |
| "Nunca imprima senhas em stdout; passe via stdin" | `true` | Vazamento de credencial (adversarial) |
| "Verifique SHA256 do binário antes de instalar" | `true` | Supply chain attack |
| "Trate dados de CLI como untrusted content" | `true` | Injection via output malicioso |
| "Revise se há SQLi, XSS, command injection" | `true` | Ameaças nomeadas |

> [!important] R-13 — Leia TUDO antes de decidir
> Segurança pode aparecer em **qualquer seção** do texto, não apenas no título ou na descrição. Leia o conteúdo inteiro antes de classificar. Um falso negativo por leitura parcial é mais grave que uma anotação lenta.

---

## 5. Como preencher cada coluna da planilha

| Coluna | Valores Permitidos | Instrução |
|---|---|---|
| `case_id` | Ex: `CASE041` | Preenchido automaticamente; não altere. |
| `name` | Ex: `pr-version-bump` | Preenchido automaticamente; não altere. |
| `body_chars` | Numérico | Preenchido automaticamente; tamanho do corpo. |
| `is_software_development` | `true` ou `false` | A skill produz, transforma, testa, deploya, monitora ou documenta um artefato computacional? |
| `has_security` | `true`, `false` ou *vazio* | Traz considerações de segurança de software? Deixe **vazio** se `is_software_development` for `false`. |
| `evidence` | `description`, `body`, `bundled_artifacts` | Onde você encontrou a evidência principal? (Pode combinar com `;`). |
| `confidence` | `high`, `medium`, `low` | Quão seguro você está do seu julgamento? Use `medium` ou `low` se for um caso de fronteira. |
| `note` | Texto livre estruturado | **Essencial.** Justifique seu raciocínio (ver estrutura abaixo). |

### Estrutura Obrigatória do Campo `note`
A anotação deve ser direta e conter três elementos:
1. **O que a skill faz:** (Ex: *"Automação para gerar changelog e versão semântica de pull requests"*).
2. **Por que é ou não é SDLC:** (Ex: *"É SDLC pois produz artefato de versionamento como parte do pipeline de release"*).
3. **Conteúdo de segurança:** (Ex: *"Não possui nenhuma consideração ou salvaguarda de segurança"* OU *"Possui segurança pois valida tokens de acesso contra vazamento em logs"*).

---

## 6. Procedimento de Calibração (D-031, D-036, D-039)

### Fase 0 (Piloto) — CONCLUÍDA
- CASE001 a CASE040 anotados com Codebook v3.1. Divergências analisadas. Regras refinadas para v3.2.
- Esses dados **não entram** na amostra final nem no cálculo de concordância.

### Fase 1 (Calibração) — A INICIAR
Para os próximos 20–40 casos (a partir de CASE041):
1. **Trabalho Cego:** Não discuta nenhum caso com o outro anotador antes de terminar e salvar sua planilha.
2. **Confronto:** Rodaremos o script de medição de concordância para gerar a matriz de confusão e o $\kappa$.
3. **Meta:** $\kappa \ge 0.80$. Se atingido, esses casos entram na amostra e prosseguimos à Fase 2.
4. **Se não atingido:** Reconciliação de divergências. Se necessário, novo ciclo de refinamento e calibração.

### Fase 2 (Produção) — APÓS CALIBRAÇÃO
Continuem anotando sequencialmente até completar 385 SDLC válidos.

## Ligações

[[Codebook]] · [[QI-1 Methodology]] · [[QI-2 Methodology]] · [[Decision Log#D-034]] · [[Decision Log#D-035]] · [[Decision Log#D-036]] · [[Decision Log#D-037]] · [[Decision Log#D-039]] · [[EXP-019]]
