---
tipo: codebook
version: 3.2
data: 2026-09-29
substitui: v3.1 (2026-09-21)
decisoes: D-034, D-035, D-036, D-037, D-038, D-039
status: vigente para calibração — pendente κ ≥ 0,80 (D-039)
---

# Codebook — Classificação de Security Skills

Instrumento canônico de anotação. Definição, classes e dimensões fornecidas pelo pesquisador; operacionalização e âncoras derivadas dos dados.

> [!warning]- Histórico de versões
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
>
> **v3.0** ([[Decision Log#D-034]], [[Decision Log#D-035]]): Reescrita completa. 
> Substitui a abordagem de três classes (PRIMARY/SECONDARY/NONE) por uma
> classificação em duas etapas: (1) participação no ciclo de desenvolvimento
> de software e (2) presença de segurança neste contexto.
>
> **v3.1** ([[Decision Log#D-036]], [[Decision Log#D-037]], [[Decision Log#D-038]]): Estabelece que a anotação será 100% manual para 385 casos de SDLC (substituindo classificação primária por LLM). Formaliza a amostragem com reposição (descarte de não-SDLC) e calibração de $\kappa \ge 0.8$ nos primeiros 20-40 casos.
>
> **v3.2** ([[Decision Log#D-039]]): Refinamento pós-piloto. A anotação dos primeiros 40 casos revelou 16 divergências sistemáticas em dois eixos: (1) fronteira tooling/meta-agente vs. SDLC e (2) guardrails operacionais confundidos com segurança. Introduz o **Teste do Artefato Computacional** (R-1 reformulado), o **Teste do Adversário** (R-12), regras para ferramentas de ecossistema (R-1a), instruções híbridas (R-12a) e scan completo (R-13). Expande exclusões e exemplos sintéticos. Descarta os 40 casos do piloto da amostra final por contaminação codebook↔amostra.

---

## 1. Definição e pergunta de pesquisa

- **QI-1 reformulada:** "Entre as Agent Skills voltadas ao desenvolvimento de software, qual a prevalência de considerações de segurança?"
- **Unidade de análise:** O conteúdo distinto (`dedup_primary = 1`), conforme [[Decision Log#D-001]].
- **População Elegível:** Restrita a skills 100% em inglês ([[Decision Log#D-025]]) e com tamanho mínimo suficiente para avaliação (`length(description) + body_chars >= 200`). O dataset base para a amostragem considera apenas a intersecção desses filtros.

---

## 2. Estágio 1 — É skill de desenvolvimento de software? (sim/não)

**Definição:** Entende-se por desenvolvimento de software todo o ciclo de vida (SDLC): requisitos de sistema, frontend, backend, banco de dados, infraestrutura, DevOps, CI/CD, observabilidade, segurança, testes, arquitetura, documentação técnica de software.

**Teste do Artefato Computacional (R-1 reformulado, D-039):** A skill instrui diretamente a **produzir, transformar, testar, deployar, monitorar ou documentar um artefato computacional** (código-fonte, binário, container, script, configuração de infraestrutura, esquema de banco de dados, pipeline de CI/CD, documentação técnica de API)?

**CONTA como desenvolvimento de software (→ sim):**
- Skills que escrevem, depuram, refatoram ou analisam código-fonte ou scripts.
- Configuração de infraestrutura como código (Docker, Kubernetes, Terraform, servidores web).
- Pipelines de CI/CD, automação de build, deploy, release e versionamento semântico.
- Testes de software (unitários, integração, e2e, carga, segurança).
- Modelagem, migração ou consultas a bancos de dados e APIs.
- Documentação técnica estritamente voltada a software (README de código, Swagger/OpenAPI, documentação de arquitetura de sistema).
- Skills que operam ferramentas do ecossistema de desenvolvimento (npm, pip, Docker registry, Git hosting, package managers) **quando a ação descrita faz parte de um workflow de build, release ou manutenção de dependências** (R-1a, D-039).
- Se uma skill trabalha com qualquer etapa do SDLC e *também* menciona guardrails de agente, ela ENTRA — o guardrail não a desclassifica.

**NÃO CONTA como desenvolvimento de software (→ não):**
- Skills puramente de orquestração de agente sem produção de artefato de software (gerência de memória/contexto do agente, analytics de uso do agente, triagem de sessão do agente, atualização de skills do agente).
- **Design de produto genérico, UX teórica, ou requisitos não-software** (D-039): princípios de design (Norman, gestalt, ergonomia), design de produto físico, requisitos de negócio sem relação direta com artefato computacional. Conta como SDLC apenas quando a skill instrui a implementar ou especificar tecnicamente um componente de software.
- **Operação de sistemas existentes como usuário final** (D-039): skills que instruem o agente a operar software existente (executar trades em DEX, rodar pipelines de bioinformática pré-construídos, configurar dashboards de analytics) sem produzir, modificar ou manter artefatos de software. O uso de comandos técnicos (CLI, API calls, scripts de automação) **não é suficiente** para classificar como SDLC — o critério é se a skill produz ou mantém um artefato de software.
- Marketing, design gráfico, vídeo, geração de imagens.
- Pesquisa acadêmica (não computacional).
- Gestão financeira, RH.
- GRC sem objeto computacional.
- Arquivos que não são instruções (logs gerados, dumps de saída).

> [!tip] Teste discriminante para design e requisitos (D-039)
> Se os requisitos ou o design descrito pudessem ser igualmente aplicados a um produto não-software (um edifício, uma porta, um formulário em papel), então **não é SDLC**. Se são intrinsecamente sobre a estrutura, comportamento ou interface de um sistema computacional, **é SDLC**.

> [!tip] Teste discriminante para operação vs. construção (D-039)
> Se a skill opera software existente **E** simultaneamente produz ou modifica código/configuração como parte de um workflow de desenvolvimento (ex: "execute o pipeline de testes E corrija os bugs encontrados"), classifique como SDLC. Se apenas opera, não é SDLC.

**Exemplos sintéticos para o Estágio 1:**

| Descrição sintética | is_sdlc | Justificativa |
|---------------------|---------|---------------|
| Skill que gerencia o lifecycle de workers de memória de um agente IA (start, stop, export/import de contexto) | `false` | Orquestra agente, não produz artefato de software |
| Skill que investiga falhas em sessões de agente e recomenda ajustes em skills | `false` | Meta-agente: diagnostica o agente, não o software |
| Skill que analisa uso de tokens e custos de um agente de codificação | `false` | Analytics de uso do agente |
| Skill que configura 2FA no npm registry para proteger publicação de pacotes | `true` | Ferramenta de ecossistema em workflow de release (R-1a) |
| Skill que executa swaps de tokens em DEX (DeFi), com verificação de checksum e trust boundaries | `false` | Opera sistema financeiro como trader, não constrói software |
| Skill de design cognitivo (affordances, signifiers) aplicável a portas, controles e interfaces digitais | `false` | Design genérico de produto; aplicável a não-software |
| Skill que converte documentos acadêmicos de PDF para Markdown | `false` | Operação de ferramenta utilitária, não produz artefato de software |
| Skill que atualiza e instala skills do agente Claude | `false` | Gerencia o agente, não artefatos de software |
| Skill que gera scaffolding Go, implementa e testa com TDD | `true` | Produz código-fonte com testes |
| Skill de code review que verifica correctness, performance e injection/segredos em PRs | `true` | Avalia artefato de software (código) |

---

## 3. Estágio 2 — Existe segurança nessa skill? (sim/não)

Apenas aplicável se o Estágio 1 for "sim". Refere-se à segurança no contexto de desenvolvimento de software ([[Decision Log#D-035]]).

**CONTA como segurança (→ sim):**
- Proteção contra prompt injection.
- Defesa contra malware.
- Critérios e considerações de segurança ao escrever código.
- Testes de segurança (SAST, DAST, pentest, fuzzing).
- Referências a arquivos de segurança no repositório (ex: "leia SECURITY.md"). *Basta um ponteiro; registrar para análise posterior.*
- Gestão de segredos: não commitar `.env`, variáveis de ambiente, secret vaults.
- Rate limiting como proteção contra abuso.
- Desenvolver ou gerenciar autenticação segura no backend (OAuth 2.0, PKCE, JWT seguro).
- Skills de teste que incluem testar auth.
- Validação de input contra injection.
- OWASP, CVE, análise de vulnerabilidade. Lista de ameaças nomeadas sem verbo (ex: "Security: OWASP Top 10") conta como `true` aqui; a profundidade dessa segurança é separada na segunda classificação (open coding, QI-2).
- Menção a pipeline de segurança no CI/CD.
- **Integridade de supply chain** (D-039): verificação de hash/checksum de binários ou pacotes antes de instalação, pinning de versões com verificação criptográfica, assinatura digital de artefatos.
- **Trust boundaries em dados externos** (D-039): instruções para tratar dados retornados de APIs externas, CLIs, ou smart contracts como não-confiáveis (untrusted), com filtragem antes de processamento pelo agente.
- **Segurança embarcada em workflows** (D-039): skills de code review, CI/CD, ou testes que incluam uma dimensão explícita de segurança (ex: "verifique SQLi, XSS, command injection") contam como `has_security: true`, mesmo que segurança seja apenas uma entre várias dimensões. A dimensão precisa ser uma **instrução acionável** — dizer contra o quê proteger ou o que verificar/validar/testar. A palavra "segurança"/"security" isolada num checklist, sem ameaça nem verificação, é mera menção (R-3) → `false`.

**NÃO CONTA como segurança (→ não):**
- Tutorial de como se autenticar num sistema (usar auth, não construir auth segura).
- **Guardrails operacionais do agente** (ver R-12 abaixo): "Não apague arquivos sem confirmação", "opere em modo read-only", "pergunte antes de rodar comandos", "não force-push", "não commite sem aprovação". Isso protege contra erro do próprio agente, não contra um adversário.
- Mera menção de que existe autenticação sem instrução protetiva.
- Limite de gasto financeiro.
- Segurança clínica, validade científica, *safety* ≠ *security*.
- GRC puramente organizacional sem objeto computacional.

> [!important] Distinção chave — autenticação
> O corte é: construir/testar auth de forma segura vs. usar auth existente.
> ✅ "Implemente OAuth 2.0 com PKCE e refresh tokens rotativos" → segurança
> ✅ "Teste as rotas autenticadas contra bypass" → segurança
> ❌ "Para se autenticar, faça POST em /auth com sua API key" → não é segurança

**Exemplos sintéticos para o Estágio 2:**

| Instrução (padrão sintético) | has_security | Justificativa |
|------------------------------|-------------|---------------|
| "Não force-push em branches protegidas" | `false` | Guardrail: previne erro do agente, não ataque (R-12) |
| "Opere em modo read-only durante análise" | `false` | Guardrail: limita scope do agente (R-12) |
| "queue:clear é destrutivo, exija confirmação do usuário" | `false` | Guardrail: previne destruição acidental (R-12) |
| "Não modifique o target durante análise investigativa" | `false` | Restrição de workflow do agente (R-12) |
| "Nunca imprima senhas em stdout; alimente via stdin" | `true` | Previne vazamento de credencial — ameaça adversarial (R-12) |
| "Verifique SHA256 do binário antes de instalar" | `true` | Previne supply chain attack (R-12) |
| "Trate dados retornados de CLI como untrusted external content" | `true` | Previne injection via output malicioso (R-12) |
| "Verifique se rotas autenticadas rejeitam requisições sem token" | `true` | Testa bypass de autenticação (R-12) |
| "Revise o código procurando SQLi, XSS, command injection e segredos hardcoded" | `true` | Ameaças nomeadas em contexto de code review |
| "Revise: correctness, performance, security, legibilidade" (sem mais nada sobre segurança) | `false` | Termo solto, sem ameaça nem verificação (R-3) |
| Tag `category: security` num script que só formata JSON | `false` | Etiqueta sem substância (R-3) |

---

## 4. Campos do instrumento

O modelo de dados para a anotação utiliza campos simplificados:

- `case_id`: Identificador da skill.
- `is_software_development`: `true` | `false`
- `has_security`: `true` | `false` | `null` (`null` quando `is_software_development` for `false`).
- `evidence`: `description` | `body` | `bundled_artifacts` (multi-label).
- `confidence`: `high` | `medium` | `low`
- `note`: Texto estruturado contendo:
  1. O que a skill faz.
  2. Por que é ou não é desenvolvimento de software.
  3. Qual conteúdo de segurança existe ou por que nenhum se aplica.

---

## 5. Regras de decisão

Aplicar em ordem; parar na primeira que decidir.

**R-1 — Teste do Artefato Computacional (Estágio 1, D-039):** A skill instrui diretamente a produzir, transformar, testar, deployar, monitorar ou documentar um artefato computacional (código-fonte, binário, container, script, configuração de infraestrutura, esquema de banco de dados, pipeline de CI/CD, documentação técnica de API)? Se sim, `is_software_development: true`. Se não (orquestração pura de agente, meta-agente, operação de sistema existente como usuário final, texto, vídeo, GRC corporativo), `is_software_development: false` e a avaliação se encerra.
**R-1a — Ferramentas de ecossistema de desenvolvimento (D-039):** Skills que operam ferramentas do ecossistema de desenvolvimento (npm, pip, Docker registry, Git hosting, package managers) contam como SDLC se e somente se a ação descrita fizer parte de um workflow de build, release ou manutenção de dependências de software.
**R-2 — Teste do Estágio 2 (Presença de Segurança):** Se R-1 for verdadeiro, leia **todo** o conteúdo (R-13) e, para cada candidata a instrução de segurança voltada a sistemas computacionais, aplique o Teste do Adversário (R-12/R-12a). A pergunta é apenas sobre **presença** (sim/não), independentemente se é o foco principal. Se ao menos uma passar, `has_security: true`.
**R-3 — Locus da evidência:** Casamento de termos de segurança apenas em tags, categorias, nome do arquivo ou listas genéricas ("related skills") não conta como conteúdo de segurança.
**R-4 — Homônimos:** Termos de segurança com duplo sentido (ex: audit ≠ security audit, token ≠ auth token, permission = UX permission) devem ser filtrados conforme a intenção; safety ≠ security.
**R-5 — Artefatos associados:** Se `has_scripts = 1` e o script opera funções de segurança englobadas (`bundled_artifacts`), classifique pelo comportamento conjunto se o arquivo principal for uma instrução.
**R-6 — Objeto protegido:** A segurança pode incidir sobre o código produzido, a infraestrutura, o agente/harness ou a própria skill — desde que o alvo seja um objeto computacional.
**R-7 — Idioma:** O idioma original nunca decide a classificação; termos técnicos de segurança em inglês dentro de outro idioma são evidência válida.
**R-8 — Escopo de GRC:** Governança, Risco e Conformidade entra na classificação apenas se houver inspeção ou ação sobre propriedades de segurança de sistemas computacionais.
**R-9 — Não é instrução (Saída Gerada):** Se o arquivo for nitidamente um log, dump ou relatório gerado e não uma instrução prospectiva, marque `is_software_development: false` e anote para exclusão de frame posterior.
**R-10 — Fechamento e Confiança:** Não há classe de dúvida (ex-`AMBIGUOUS`). Faça a sua melhor escolha binária em R-1 e R-2 baseada na evidência. Se o caso for limítrofe ou ambíguo, rebaixe o campo `confidence` para `medium` ou `low`.
**R-11 — Cegamento:** O anotador humano não vê o sinal preliminar de triagem ou a saída da LLM antes ou durante a sua anotação.
**R-12 — Teste do Adversário (D-039, aplicado dentro da R-2):** "Esta instrução protege contra uma **ameaça adversarial ou vulnerabilidade exploratável** no software/sistema produzido, ou protege contra **erro operacional do próprio agente**?" Se protege contra ameaça adversarial → segurança. Se protege contra erro do agente → guardrail operacional, não é segurança.
**R-12a — Instrução Híbrida (D-039):** Quando uma instrução simultaneamente previne erro operacional e protege contra ameaça adversarial, classifique como segurança. A presença de componente de segurança prevalece.
**R-13 — Scan Completo (D-039, aplicado dentro da R-2):** O anotador deve ler **todo o conteúdo** do caso antes de decidir. Segurança pode aparecer em qualquer seção, não apenas no título ou na descrição. Um falso negativo por leitura parcial é mais grave que uma anotação lenta.

---

## 6. Exclusões de frame

Aplicadas no frame e não como classificação, removendo a skill da análise:

- **Sem evidência classificável:** Contagem de caracteres combinada muito baixa (`length(description) + body_chars < 200`).
- **Evidência truncada com dúvida:** Script truncado/faltante cujo texto remanescente seja insatisfatório para julgar os estágios (necessário reportar com limites de Manski).
- **Não é arquivo de instrução:** O arquivo não atua como instrução (`not_an_instruction_artifact`); por exemplo, é uma saída de dump ou log.
- **Filtro de População (Não-SDLC):** Conforme D-037, skills que falham no Estágio 1 (`is_software_development = false`) são registradas para o cálculo da taxa de descarte geral, mas **removidas e repostas** na contagem da amostra principal, garantindo que o dataset final de $n=385$ seja 100% composto por skills de SDLC.
- **Dados de desenvolvimento do instrumento (D-039):** Os casos CASE001–CASE040 (piloto de calibração) são excluídos da amostra final por contaminação codebook↔amostra. Preservados como evidência do processo de refinamento.

---

## 7. Confiabilidade

> [!info] Procedimento de Calibração Manual (D-036, D-039)
> A anotação do *ground truth* (que compõe a amostra final de $n=385$ skills de SDLC) é feita 100% por humanos. O protocolo exige:
> 1. **Piloto (CASE001–CASE040, D-039):** Desenvolvimento do instrumento. Anotação independente, identificação de divergências, refinamento das regras (Codebook v3.1 → v3.2). Dados descartados da amostra final.
> 2. **Calibração (a partir de CASE041):** Anotação independente e cega com Codebook v3.2 (20 a 40 casos novos). Cálculo de **Cohen's $\kappa$**, visando um limiar $\kappa \ge 0.8$. Reconciliação se necessário. Se κ < 0,80 e as regras forem alteradas, os casos desta rodada também passam a ser dados de desenvolvimento do instrumento (mesma lógica da D-039); a nova calibração começa no primeiro caso ainda não visto.
> 3. **Produção:** Após calibração, prosseguir com a anotação do restante até obter 385 casos válidos de SDLC, onde deve ser atingida a **saturação teórica** para a RQ2 (Open Coding).

Os coeficientes a reportar para as decisões binárias (e qualitativas) continuam a ser:
1. Concordância bruta ($p_o$)
2. **Cohen's $\kappa$** (para 2 avaliadores independentes)
3. **Krippendorff's $\alpha$**
4. **Gwet's AC1** (essencial como resguardo a paradoxos de kappa em distribuições desbalanceadas)

---

## 8. Limites conhecidos

- **Limiares de inclusão (Estágio 2):** Ao ser identificador binário da presença de segurança, a super-inclusão poderá exigir separação posterior através de open-coding;
- **Referências indiretas:** Quando há apenas a menção "consulte SECURITY.md", tem-se uma marcação de segurança (sim) sem saber a categoria exata desta proteção até um mapeamento qualitativo aprofundado;
- **Ambiguidades em Autenticação e Configuração:** Distinguir a construção/proteção da autenticação do uso puro de chaves API poderá exigir jurisprudência robusta em casos limítrofes;
- **Fila de casos:** Após o piloto restam 560 candidatos (CASE041–CASE600). Com a taxa de SDLC do piloto (22/40 no anotador H; ~0,55), a expectativa é de ~308 SDLC, abaixo da cota de 385. A fila **deve ser estendida antes da Fase 2** para ≥ ~700 candidatos a partir do CASE041, recalculando com a taxa observada na calibração. A ordem por hash é mantida (os novos casos seguem o CASE600) (D-039).

---

## 9. Ligações

[[Decision Log]] · [[QI-1 Methodology]] · [[QI-2 Methodology]] · [[QI-3 Coverage Methodology]] · [[EXP-013]] · [[Classification and Sampling Precedents]] · [[01 - Research Question]]
