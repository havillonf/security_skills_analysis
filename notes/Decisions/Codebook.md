---
tipo: codebook
version: 2.3
data: 2026-08-22
substitui: v2.2 (2026-08-22)
decisoes: D-004, D-006, D-012, D-013, D-014, D-016
status: proposto para teste piloto
---
	
# Codebook — Classificação de Security Skills

Instrumento canônico de anotação. Definição, classes e dimensões fornecidas pelo
pesquisador; operacionalização e âncoras derivadas dos dados.

> [!warning] v2.3 — ainda não validada
> Escrita **antes** da anotação definitiva (etapa E-1 do plano; o piloto é E-5).
> Nenhuma anotação foi feita sob v1.0 ou v2.0, então não há retrabalho.
> **Não alterar em silêncio depois que a anotação começar.**
>
> **v2.0** ([[Decision Log#D-006]]): renomeou `NON-SEC` → `NONE`, acrescentou
> `AMBIGUOUS`, separou dimensões colapsadas na v1.0.
> **v2.1** ([[Decision Log#D-012]]): corrige o tratamento de idioma — barreira
> linguística do anotador **deixa de ser** caso de `AMBIGUOUS`; acrescenta a regra
> R-9 e os campos `language` e `used_translation`.
> **v2.2** ([[Decision Log#D-016]], [[Decision Log#D-014]]): operacionaliza `mixed`,
> acrescenta a regra R-10 (escopo de GRC) e o campo `language_detector_agreement`.
> **v2.3** ([[Decision Log#D-021]]): **remove as duas âncoras de `AMBIGUOUS` cuja
> única justificativa era barreira de idioma.** A v2.1 declarou essa correção mas
> ela nunca chegou às âncoras — o texto contraditório sobreviveu a três versões.
> Acrescenta a regra de cegamento e alinha a ficha de anotação.

---

## 1. Definição

> **Security Skill:** uma Agent Skill cujo **propósito principal**, ou uma **parte
> substancial de seu comportamento operacional**, é prevenir, detectar, analisar,
> avaliar, explorar, mitigar ou responder a ameaças, vulnerabilidades, violações de
> propriedades de segurança ou controles de acesso em sistemas computacionais.

Presença de vocabulário de segurança **nunca** basta. A classificação considera
propósito declarado, comportamento, atividade orientada ou executada, resultado
esperado, contexto e artefatos associados.

A inclusão de "explorar" torna a definição neutra quanto à postura: pentest,
exploit dev e CTF são Security Skills tanto quanto um scanner defensivo. Postura é
dimensão descritiva, **nunca** critério de inclusão nem juízo de malícia.

### 1.1 Unidade de análise

Um **conteúdo distinto** (`dedup_primary = 1`), n = 1.877.981. Ver
[[Decision Log#D-001]]. Anota-se o `SKILL.md`; artefatos associados
(`artifact_siblings`) entram quando necessários para determinar a capacidade real
(regra R-6).

---

## 2. Dimensões

Registradas **separadamente**. A v1.0 colapsava tudo numa classe ordinal e perdia a
distinção central da pesquisa: *falar sobre* segurança versus *fazer* segurança.

| Dimensão | Valores | Multi-label |
|---|---|---|
| `security_relevance` | PRIMARY · SECONDARY · MENTION · NONE · AMBIGUOUS | não |
| `security_focus` | true / false | não |
| `operational_security` | true / false | não |
| `operation_level` | reasoning · executable · mixed · n/a | não |
| `security_functions` | PREVENT · DETECT · ASSESS · TEST · RESPOND · RECOVER | **sim** |
| `security_concerns` | taxonomia emergente ([[Security Taxonomy]]) | **sim** |
| `operational_capability` | ver §5 | **sim** |
| `evidence` | description · body · bundled_artifacts | **sim** |
| `confidence` | high · medium · low | não |

`security_functions`, `security_concerns`, `operational_capability`,
`operation_level` e `security_focus` só se aplicam quando `security_relevance` ∈
{PRIMARY, SECONDARY}.

---

## 3. `security_relevance`

| Classe | Significado |
|---|---|
| `PRIMARY` | Segurança é o propósito principal da skill |
| `SECONDARY` | Segurança é capacidade ou etapa substancial de um objetivo maior |
| `MENTION` | Recomendação, observação ou preocupação incidental |
| `NONE` | Sem preocupação de segurança relevante |
| `AMBIGUOUS` | Evidência insuficiente para classificação confiável |

**`AMBIGUOUS` não é lixo nem categoria de descarte.** É um resultado. Nunca force
uma das outras quatro quando a evidência não sustenta. Casos frequentes observados:
skill sem front matter e corpo genérico; skill cuja capacidade real depende de script
não recuperado (`composition_truncated = 1`, 13,4% dos representantes); skill cujo
texto é genérico demais para revelar comportamento.

> [!danger] Idioma **nunca** é motivo de `AMBIGUOUS`
> Não dominar o idioma do texto é limitação **do anotador**, não do dado. Resolve-se
> por processo (R-9), não por classe. Marcar conteúdo não inglês como `AMBIGUOUS`
> enviesaria a estimativa de prevalência contra idiomas sub-representados — ver
> [[Decision Log#D-012]].

`PRIMARY` + `SECONDARY` = **Security Skill**. `AMBIGUOUS` fica **fora** do
numerador e **fora** do denominador em qualquer prevalência — e sua contagem é
reportada junto, sempre.

### 3.1 `SECURITY_FOCUSED` e `SECURITY_OPERATIONAL`

Duas propriedades independentes, ambas registradas:

**`security_focus = true`** quando segurança é o propósito predominante. Domínios
observados: análise de vulnerabilidades, pentest, SAST, DAST, revisão de segurança,
hardening, detecção de secrets, análise de malware, auditoria IAM, threat modeling,
vulnerability scanning, segurança de dependências, resposta a incidentes.

**`operational_security = true`** quando a skill *executa, automatiza, orienta ou
avalia* uma atividade concreta de segurança sobre código, aplicação, infraestrutura,
rede, agente, modelo ou outro artefato computacional.

> Não exija execução automática de ferramenta externa.
> *"Analise este código e encontre possibilidades de SQL Injection"* **é**
> operacional, ainda que a análise seja por raciocínio.
> *"Execute SQLMap e valide as injeções"* também é operacional, com capacidade
> executável mais forte.

Diferencie o **objetivo de segurança** da **forma de operacionalização** — a segunda
vai em `operation_level`, não em `operational_security`.

Combinações são informativas e nenhuma é contraditória:

| focus | operational | leitura |
|---|---|---|
| true | true | skill de segurança que faz segurança |
| true | false | skill de segurança puramente conceitual/educacional |
| false | true | skill de outro domínio com etapa concreta de segurança |
| false | false | tipicamente MENTION ou NONE |

---

## 4. Regras de decisão

Aplicar em ordem; parar na primeira que decidir.

**R-1 — Teste de remoção.** Removido todo o conteúdo de segurança, a skill ainda faz
o que se propõe?
Não, deixaria de cumprir seu propósito → `PRIMARY`.
Sim, mas perderia capacidade operacional descrita → `SECONDARY`.
Sim, praticamente inalterada → `MENTION` ou `NONE`.

**R-2 — Teste de acionabilidade.** Operacionaliza "substancial". Conteúdo de
segurança é acionável quando diz **o que fazer**, não apenas o que evitar:
procedimento, checklist, critério de severidade, categoria de falha a procurar,
ferramenta a executar, formato de relatório. Advertência, princípio ou aviso de uma
linha **não** é acionável. `SECONDARY` exige conteúdo acionável; sem isso, `MENTION`.

**R-3 — Teste de proporção.** Segurança como uma entre várias dimensões coordenadas
→ `SECONDARY`. Segurança organizando a skill, demais dimensões subordinadas →
`PRIMARY`. Proporção textual isolada não decide: scanner curto é PRIMARY; skill
longa com um parágrafo acionável é SECONDARY.

**R-4 — Locus da evidência.** Casamento apenas em `tags`, `category`, nome de
arquivo ou lista de "related skills" **não** conta como conteúdo de segurança.
*Caso real:* `go-playwright-v2` traz `category: testing-security` e é automação de
browser → `NONE`.

**R-5 — Homônimos.** Termo de segurança em sentido não-securitário não conta.
*Casos reais:* `meta-ads-audit` ("audit" = auditoria de anúncios) → `NONE`;
`token` como token de LLM; `permission` como permissão de arquivo.

**R-6 — Artefatos associados.** Se `has_scripts = 1` e o script executa função de
segurança que o `SKILL.md` mal menciona, classifique pelo **comportamento
operacional conjunto** — a definição fala de comportamento, não de texto. Marque
`evidence: bundled_artifacts`. Se o script for necessário e não estiver disponível
(`composition_truncated = 1`), use `AMBIGUOUS`.

**R-7 — Objeto protegido não restringe.** Vale para código produzido, agente/harness
ou a própria skill. Registrar como `security_concern`, não na classe.

**R-9 — Idioma.** A skill é elegível qualquer que seja o idioma. Se o anotador não
domina o idioma do texto: (a) rotear para anotador competente, ou (b) usar tradução
como apoio, **preservando o original** e marcando `used_translation: true`
([[Decision Log#D-013]]). Nunca classificar por idioma. Atenção a termos técnicos de
segurança em inglês embutidos em texto de outro idioma — são evidência válida.

*Operacionalização de `language`:*
- rotular pelo idioma da **prosa** (não do código, caminhos ou nomes de ferramenta);
- **`mixed`** quando duas ou mais línguas naturais carregam conteúdo substantivo —
  não basta um termo técnico inglês solto num texto em outro idioma;
- **`und`** quando a prosa é curta ou técnica demais para decidir;
- `la` (latim) **não é** rótulo válido neste corpus: é artefato do detector para
  texto técnico em inglês ([[EXP-004]]). Reclassificar como `en` ou `und`.

**R-10 — Escopo de GRC.** Governança, risco e conformidade entram **apenas quando a
atividade incide sobre propriedades de segurança de sistemas computacionais**
([[Decision Log#D-016]], proposta aguardando aprovação).

*Dentro:* auditoria de IAM, revisão de política de acesso, least privilege, mapeamento
de controles técnicos, avaliação de risco de dependência, conformidade que **inspeciona
configuração ou código**.
*Fora:* questionário de fornecedor contratual, conformidade regulatória sem objeto
computacional, gestão de risco corporativo, política como documento.

**Impacto nas classes (transcrição completa de [[Decision Log#D-016]]):**

| Situação | Classe |
|---|---|
| GRC técnico com procedimento acionável | `PRIMARY` ou `SECONDARY` conforme R-1/R-3 |
| GRC organizacional puro | `NONE` — não `MENTION` |
| Misto, parte técnica acionável | `SECONDARY`, `confidence: low` |
| Misto, parte técnica só mencionada | `MENTION` |
| Indeterminável | `AMBIGUOUS` |

GRC organizacional puro é `NONE`, não `MENTION`, porque `MENTION` pressupõe
preocupação de segurança **computacional** incidental — conformidade contratual não é
disso que trata.

**R-8 — Dúvida (regra de fechamento; aplicar por último).** Se a evidência é
insuficiente → `AMBIGUOUS` com `confidence: low`. Se há evidência mas o limite entre
duas classes é discutível → classe **mais baixa**, `confidence: low`, e o caso vai
para adjudicação.

**R-11 — Cegamento.** O anotador **não vê** o sinal preliminar de triagem (tier,
densidade de keyword, flags de GRC/code-review, grupo linguístico, motivo da
seleção) antes ou durante a anotação. Esses campos ficam em arquivo separado
(`EXP-005_strata_key.csv`), unido por `case_id` **somente depois** de a anotação
estar fechada. Ver [[Decision Log#D-021]].

> Ordem de aplicação: **R-11** (antes de começar) → **R-1 … R-7** (decisão) →
> **R-9, R-10** (idioma e GRC, transversais) → **R-8** (fechamento).

---

## 5. `operational_capability`

Como a capacidade é realizada. Multi-label. Categorias candidatas, a refinar
empiricamente:

`reasoning_or_guidance` · `source_code_analysis` · `static_analysis` ·
`dynamic_analysis` · `configuration_analysis` · `dependency_analysis` ·
`command_execution` · `network_scanning` · `vulnerability_scanning` ·
`exploitation` · `secret_scanning` · `remediation` · `other`

`operation_level`: `reasoning` (só raciocínio/orientação) · `executable` (invoca
ferramenta, script ou comando) · `mixed`.

---

## 6. `security_functions`

Multi-label. Não force função única.

`PREVENT` · `DETECT` · `ASSESS` · `TEST` · `RESPOND` · `RECOVER`

Exemplos: skill de pentest que identifica e valida SQLi → `TEST` + `DETECT`. Skill
que corrige queries vulneráveis → `PREVENT`, ou `ASSESS` + `PREVENT` conforme o
workflow.

Concern, function e capability **não devem ser colapsados**. São comportamentos
diferentes:

```text
Concern: SQL Injection | Function: DETECT + TEST | Capability: dynamic_analysis + exploitation
Concern: SQL Injection | Function: PREVENT       | Capability: source_code_analysis
```

---

## 7. Ficha de anotação

A ficha operacional é o CSV de [[EXP-005]]. **Campos humanos** (preenchidos pelo
anotador) e **campos automáticos** (na chave de estratos, invisíveis durante a
anotação por R-11) são arquivos separados.

> **Exemplo preenchido:** `results/EXP-005_annotation_example.csv` — 7 linhas
> fictícias cobrindo PRIMARY, SECONDARY, MENTION, NONE (comum e por GRC), AMBIGUOUS e
> um caso em português. Instruções em [[EXP-005]]§Como preencher o CSV.
>
> **No CSV, listas usam `;` como separador** (`DETECT;ASSESS`), porque a vírgula já
> separa colunas. Campo não aplicável fica **vazio**, nunca `n/a`.

```yaml
# --- campos HUMANOS: results/EXP-005_annotation_form.csv ---
case_id: P007
human_language: zh        # ISO 639-1, ou "mixed", ou "und". Nunca "la".
used_translation: false   # a decisão dependeu de tradução?
security_relevance: PRIMARY
security_focus: true
operational_security: true
operation_level: executable          # reasoning | executable | mixed | n/a
security_functions: [DETECT, ASSESS]
security_concerns: [malware, ioc_extraction]
operational_capability: [static_analysis, command_execution]
evidence: [description, body, bundled_artifacts]
confidence: high                     # high | medium | low
rule_applied: R-1                    # regra que decidiu
grc_case: false                      # caiu sob R-10?
secondary_mention_boundary: false    # ficou na fronteira SECONDARY/MENTION?
annotation_seconds: 145              # tempo cronometrado
difficulty: medium                   # easy | medium | hard
note: ""

# --- campos AUTOMATICOS: results/EXP-005_strata_key.csv ---
# NAO abrir antes de fechar a anotacao (R-11)
# case_id, file_sha, repo_full_name, path, tier, kw_density, domain_decl,
# fm_signal, grc_flag, code_review_flag, lang_group, lang_primary,
# lang_secondary, lang_secondary_conf, detector_agreement, is_mixed,
# minor_share, has_scripts, selection_reason
```

---

## 8. Âncoras (casos reais do dataset)

Todas de [[EXP-002]]; `file_sha` em `results/EXP-002_sample.parquet`.

**`PRIMARY` + focus + operational**
`performing-malware-ioc-extraction` (`0ef07f05`, kd=12, com scripts) — extração de
IOC de malware. `cybersec-testing-ransomware-recovery` (`2c503744`, kd=14) — testa e
valida procedimentos de recuperação de ransomware; funções `TEST` + `RECOVER`.
`azure-security-keyvault-keys-dotnet` (`33130fa7`, kd=9) — gestão de chaves
criptográficas.

**`SECONDARY`** — `code-review` com seção dedicada e acionável (OWASP Top 10,
injection, XSS, CSRF, falhas de authz). R-1: sem segurança continua funcional, porém
mutilada. R-2: acionável. R-3: uma de quatro dimensões coordenadas.

**`MENTION`** — `zero-to-running` (`ce17f013`): *"Use secure defaults | Document
credential management pattern"*. `clawville` (`cb4ba334`): *"Store Your Credentials
in a secure config"*. R-2: recomendação pontual, não acionável.

**`NONE`** — `meta-ads-audit` (R-5), `go-playwright-v2` (R-4), `retro-smile`
(geração de imagem), `algolia-autocomplete`, `pdf-goal-saver`.

**`AMBIGUOUS`** — `473b7b77` e `fba0c3f3`: sem front matter, corpo genérico demais
para revelar comportamento. Skill cuja capacidade real depende de script não
recuperado (`composition_truncated = 1`).

> [!danger] Âncoras removidas na v2.3
> A v2.2 listava aqui `oral-health-analyzer` e `self-recovery-limits` como
> `AMBIGUOUS` por *"idioma fora do domínio do anotador"* — em contradição direta com
> a regra R-9 e com [[Decision Log#D-012]], que declarava essa correção já feita.
> Ambos são casos de idioma não inglês perfeitamente classificáveis; [[EXP-002]] os
> lê como `NONE`/`MENTION`. Mantê-los como âncora produziria `AMBIGUOUS` sistemático
> para conteúdo zh/ru — removendo conteúdo não inglês do numerador **e** do
> denominador, e enviesando a prevalência para a fatia inglesa.

---

## 9. Confiabilidade

`security_relevance` tem quatro níveis **ordinais** (PRIMARY > SECONDARY > MENTION >
NONE) mais `AMBIGUOUS`, que está **fora da ordem** — não pode entrar num kappa
ponderado como se fosse um quinto degrau.

Estratégia:
1. **Kappa ponderado** (linear ou quadrático) sobre os quatro ordinais, excluindo
   `AMBIGUOUS`.
2. **Kappa simples ou Krippendorff's α** sobre a dicotomia que decide o resultado:
   Security Skill (PRIMARY+SECONDARY) vs resto.
3. **Concordância sobre `AMBIGUOUS`** reportada à parte: divergir sobre *o que é
   classificável* é achado metodológico, não ruído.
4. Dimensões multi-label (`functions`, `concerns`, `capability`) → **Krippendorff's
   α para dados nominais multi-valorados** ou Jaccard médio; kappa não se aplica.

A métrica final só é fixada **depois** de o desenho de anotação estar fechado.

Anotador único é ameaça à validade que **deve** ser declarada. LLM **não** é ground
truth — ver [[QI-2 Methodology]].

---

## 10. Limites conhecidos

- **"Substancial" continua sendo julgamento.** R-2 operacionaliza, não elimina. O
  piloto deve estressar exatamente a fronteira SECONDARY/MENTION.
- **Multilinguismo.** A população inclui todos os idiomas ([[Decision Log#D-012]]);
  **14,21% não é inglês** ([[EXP-003]]). As âncoras deste codebook são ainda
  **majoritariamente em inglês** — limitação real do instrumento, a corrigir
  acrescentando âncoras em zh, ja, de, ko, es e pt durante o piloto. Concordância e
  desempenho devem ser avaliados **por idioma**, não só no agregado.
- **Rótulo de idioma: concordância alta, acurácia desconhecida.** [[EXP-004]] v2 mede
  0,987 global (0,967–1,000 por grupo) entre `lingua` e `py3langid`. Isso é
  **concordância, não acurácia** — não há ground truth humano, e a primeira medida
  real sai deste piloto (campo `human_language`). A cauda é um estrato único (L5) por
  **falta de suporte amostral**, não por falha de detecção.
- **GRC é julgamento na fronteira.** R-10 reduz, não elimina, a ambiguidade. A
  concordância nesse subconjunto deve ser reportada **à parte** no piloto; se for
  ruim, reconsiderar excluir GRC por completo ([[Decision Log#D-016]] alternativa b).
- **Sem front matter:** 252.280 representantes não têm `name`+`description`; tendem a
  `AMBIGUOUS`.
- **Não mede a segurança *da* skill.** Uma skill `NONE` que declara
  `allowed-tools: Bash(*)` é altamente relevante para segurança e ainda assim `NONE`
  aqui. Eixo ortogonal — ver [[Decision Log#D-007]]. **Nunca use o eixo B para
  decidir a classe.**
- **Escala:** 1,9M conteúdos não são anotáveis à mão. Este codebook produz o
  padrão-ouro; aplicação em escala exige classificador validado contra ele.

## Ligações

[[Decision Log]] · [[QI-2 Methodology]] · [[QI-3 Coverage Methodology]] ·
[[Security Taxonomy]] · [[EXP-002]] · [[01 - Research Question]] · [[GitSkills]]
