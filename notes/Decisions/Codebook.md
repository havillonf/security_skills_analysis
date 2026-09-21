---
tipo: codebook
version: 3.0
data: 2026-09-21
substitui: v2.6 (2026-09-05)
decisoes: D-034, D-035
status: em construção — aguardando validação em nova amostra
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

---

## 1. Definição e pergunta de pesquisa

- **QI-1 reformulada:** "Entre as Agent Skills voltadas ao desenvolvimento de software, qual a prevalência de considerações de segurança?"
- **Unidade de análise:** O conteúdo distinto (`dedup_primary = 1`), conforme [[Decision Log#D-001]].
- **População:** Restrita a skills 100% em inglês ([[Decision Log#D-025]]).

---

## 2. Estágio 1 — É skill de desenvolvimento de software? (sim/não)

**Definição:** Entende-se por desenvolvimento de software todo o ciclo de vida (SDLC): requisitos, frontend, backend, banco de dados, infraestrutura, DevOps, CI/CD, observabilidade, segurança, testes, arquitetura, documentação técnica.

**CONTA como desenvolvimento de software (→ sim):**
- Skills que trabalham com qualquer etapa do SDLC.
- Skills de DevOps, CI/CD, observabilidade.
- Skills de documentação técnica (ex: README, API docs).
- Skills que constroem, testam ou deployam software.
- Se uma skill trabalha com qualquer etapa do SDLC (backend, frontend, banco, infra, testes, etc.) e menciona guardrails de agente, ela ENTRA — o guardrail não a desclassifica.

**NÃO CONTA como desenvolvimento de software (→ não):**
- Skills puramente de orquestração de agente sem produção de software.
- Marketing, design gráfico, vídeo.
- Pesquisa acadêmica (não computacional).
- Gestão financeira, RH.
- GRC sem objeto computacional.

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
- OWASP, CVE, análise de vulnerabilidade.
- Menção a pipeline de segurança no CI/CD.

**NÃO CONTA como segurança (→ não):**
- Tutorial de como se autenticar num sistema (usar auth, não construir auth segura).
- Guardrails de agente que não se relacionam com o software em si (read-only, "não commite sem aprovação", escopo de ferramenta).
- Mera menção de que existe autenticação sem instrução protetiva.
- Limite de gasto financeiro.
- Segurança clínica, validade científica, *safety* ≠ *security*.
- GRC puramente organizacional sem objeto computacional.

> [!important] Distinção chave — autenticação
> O corte é: construir/testar auth de forma segura vs. usar auth existente.
> ✅ "Implemente OAuth 2.0 com PKCE e refresh tokens rotativos" → segurança
> ✅ "Teste as rotas autenticadas contra bypass" → segurança
> ❌ "Para se autenticar, faça POST em /auth com sua API key" → não é segurança

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

**R-1 — Locus da evidência:** O casamento de termos de segurança apenas em tags, categorias ou nomes de arquivo não conta como segurança válida.
**R-2 — Homônimos:** Termos de segurança com duplo sentido (ex: audit ≠ security audit, token ≠ auth token) devem ser filtrados conforme a intenção.
**R-3 — Artefatos associados:** Artefatos englobados (`bundled_artifacts`) que operam funções de segurança contam para as classificações se o arquivo for uma instrução.
**R-4 — Idioma:** O idioma nunca decide a classificação; termos de segurança em inglês dentro de outro idioma ainda são evidência.
**R-5 — Escopo de GRC:** Governança, Risco e Conformidade entra na classificação desde que inclua inspeção ou ação sobre um sistema computacional.
**R-6 — Não é instrução:** Se o arquivo for saída gerada (dump, relatório, log), marque `is_software_development: false` (será excluído no frame posteriormente).
**R-7 — Fechamento e Confiança:** Não há campo de dúvida. Decida de forma binária cada estágio baseado na melhor evidência. Se o caso for limítrofe, ambíguo ou não se encaixar perfeitamente nos critérios, reflita essa incerteza rebaixando o campo `confidence` para `medium` ou `low`.

---

## 6. Exclusões de frame

Aplicadas no frame e não como classificação, removendo a skill da análise:

- **Sem evidência classificável:** Contagem de caracteres combinada muito baixa (`length(description) + body_chars < 200`).
- **Evidência truncada com dúvida:** Script truncado/faltante cujo texto remanescente seja insatisfatório para julgar os estágios (necessário reportar com limites de Manski).
- **Não é arquivo de instrução:** O arquivo não atua como instrução (`not_an_instruction_artifact`); por exemplo, é uma saída de dump ou log.

---

## 7. Confiabilidade

> [!warning] Medição pendente
> Esta versão (v3.0) ainda **não teve confiabilidade medida**, já que muda o esquema para classificação binária de duas etapas, invalidando as métricas anteriores da v2.4/v2.6.

Os coeficientes a reportar para ambas as decisões binárias continuam a ser:
1. Concordância bruta ($p_o$)
2. **Cohen's $\kappa$** (ou Fleiss para $>2$ avaliadores)
3. **Krippendorff's $\alpha$**
4. **Gwet's AC1** (essencial como resguardo a paradoxos de kappa em distribuições desbalanceadas)

É necessário apresentar limites de confiança por *bootstrap* e testar discordância sistemática via teste de McNemar na nova amostra.

---

## 8. Limites conhecidos

- **Sem medição atual:** Confiabilidade da nova abordagem binária ainda não aferida empiricamente;
- **Limiares de inclusão (Estágio 2):** Ao ser identificador binário da presença de segurança, a super-inclusão poderá exigir separação posterior através de open-coding;
- **Referências indiretas:** Quando há apenas a menção "consulte SECURITY.md", tem-se uma marcação de segurança (sim) sem saber a categoria exata desta proteção até um mapeamento qualitativo aprofundado;
- **Ambiguidades em Autenticação e Configuração:** Distinguir a construção/proteção da autenticação do uso puro de chaves API poderá exigir jurisprudência robusta em casos limítrofes.

---

## 9. Ligações

[[Decision Log]] · [[QI-1 Methodology]] · [[QI-2 Methodology]] · [[QI-3 Coverage Methodology]] · [[EXP-013]] · [[Classification and Sampling Precedents]] · [[01 - Research Question]]
