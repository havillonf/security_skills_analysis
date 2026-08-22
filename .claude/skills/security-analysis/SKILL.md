---
name: security-analysis
description: O que "segurança" significa no projeto security_skills_analysis e como identificar, classificar e estimar a prevalência de Security Skills com validade. Questão central é a QI-1 (prevalência); a skill opera em três modos - CLASSIFICATION (aplicar o codebook, caminho crítico da QI-1), DISCOVERY (QI-2, open coding) e COVERAGE (QI-3, crosswalk). Cobre a população multilíngue. Use ao definir critérios de inclusão, anotar amostras, desenhar amostragem, validar classificador, ou interpretar qualquer resultado sobre skills de segurança no GitSkills.
---

# Análise de segurança em GitSkills

Pré-requisitos: `project-context`, `data-analysis`.

Instrumento canônico: **`notes/Decisions/Codebook.md` v2.3**. Esta skill orienta
*como operar*; o codebook define *o que vale*. Em divergência, o codebook manda.

> [!important] Questão central: **QI-1 — prevalência** (D-011). Desenho C (D-014).
> O objetivo é uma **estimativa com incerteza**, não uma contagem.
>
> **Desenho C — amostragem estratificada com classificador de triagem.** O
> classificador atribui classe prevista à população e isso **forma estratos**; o
> desfecho da estimação é a **anotação humana** sobre amostra probabilística dentro
> de cada estrato. Estimador `p̂ = Σ_h (N_h/N)·p̂_h`, com correção para população
> finita.
>
> Três números que **não** podem ser confundidos:
> contagem prevista pelo modelo · proporção observada na amostra humana ·
> estimativa estratificada. **Só a terceira é prevalência.**
>
> Desenho em `notes/Methodology/QI-1 Methodology.md`; plano em
> `notes/03 - Methodology.md`. Trabalho na branch `Q1`.
> QI-2 e QI-3 seguem documentadas como extensões, fora do caminho crítico.

> [!danger] A população inclui **todos os idiomas** (D-012)
> A língua em que uma skill foi escrita **não determina** se ela entra na pesquisa.
> Não descarte por idioma. Não classifique conteúdo não inglês como `NONE` ou
> `AMBIGUOUS` por não entendê-lo — isso é problema de processo (R-9), não de classe.
> Ausência de termos ingleses **não é** ausência de preocupação de segurança.
>
> Medido: **14,21% ± 0,48 pp não é inglês** (~267 mil conteúdos); zh 5,99%.
> Estratos **L1** en · **L2** zh · **L3** ja+ko · **L4** de/es/pt/fr/it ·
> **L5** cauda+und (não subdividir — ~2% da população em mais de dez idiomas, sem
> suporte amostral). `mixed` é **atributo transversal**, não grupo: skill em chinês
> com termos ingleses continua em L2. `la` é artefato do detector para texto inglês,
> nunca um idioma. Concordância entre detectores (EXP-004 v2): 0,987 global,
> 0,967–1,000 por grupo — **concordância, não acurácia**.
> Estratégia completa: `notes/Methodology/Multilingual Strategy.md`.

> [!note] Escopo de GRC (R-10, D-016 — proposta)
> Governança, risco e conformidade entram **só quando a atividade incide sobre
> propriedades de segurança de sistemas computacionais**. Auditoria de IAM entra;
> questionário contratual de fornecedor não. GRC organizacional puro é `NONE`, não
> `MENTION`. Aguarda aprovação do pesquisador.

---

## Definição adotada (D-004, revisada por D-006)

> **Security Skill:** uma Agent Skill cujo **propósito principal**, ou uma **parte
> substancial de seu comportamento operacional**, é prevenir, detectar, analisar,
> avaliar, explorar, mitigar ou responder a ameaças, vulnerabilidades, violações de
> propriedades de segurança ou controles de acesso em sistemas computacionais.

Vocabulário de segurança **nunca** basta. Consideram-se propósito declarado,
comportamento, atividade orientada ou executada, resultado esperado, contexto e
artefatos associados.

| `security_relevance` | Significado |
|---|---|
| `PRIMARY` | segurança é o propósito principal |
| `SECONDARY` | capacidade ou etapa substancial de um objetivo maior |
| `MENTION` | recomendação ou preocupação incidental |
| `NONE` | sem preocupação de segurança relevante |
| `AMBIGUOUS` | evidência insuficiente — **nunca force outra classe**, e **nunca por idioma** |

**Security Skill = `PRIMARY` + `SECONDARY`.** `AMBIGUOUS` fica fora do numerador
**e** do denominador, com contagem sempre reportada.

Dimensões independentes registradas em paralelo — `security_focus`,
`operational_security`, `operation_level`, `security_functions`,
`security_concerns`, `operational_capability`, `evidence`, `confidence`. Definições
e regras R-1..R-9 no codebook (R-9 = idioma).

### A distinção central

*Falar sobre* segurança ≠ *fazer* segurança.

> "Store credentials securely" — `MENTION`
> "Detect leaked credentials in a repository and generate a security report" —
> `PRIMARY`, operacional

`operational_security = true` **não** exige execução de ferramenta externa.
*"Analise este código e encontre possibilidades de SQL Injection"* é operacional por
raciocínio; *"Execute SQLMap e valide"* é operacional executável. A diferença vai em
`operation_level`, não em `operational_security`.

---

## Os três modos

Declare em qual modo está operando antes de agir. Eles têm regras incompatíveis.

### `DISCOVERY` — QI-2, open coding

Descobrir preocupações e construir/refinar a taxonomia empírica.

> [!danger] Regra inegociável
> **Never use an external coverage framework to construct the empirical taxonomy
> used to answer QI-2. External frameworks may be introduced after the empirical
> taxonomy has been stabilized, for crosswalk and QI-3 analysis.**
>
> Não use OWASP, MITRE, NIST ou qualquer referencial externo para decidir quais
> categorias devem existir. Isso cria circularidade — encontraríamos o que fomos
> procurar — e esconde padrões próprios do ecossistema de Agent Skills.

Como operar: permanecer próximo ao texto observado; registrar exemplo literal por
código; registrar casos fronteiriços e sobreposições; multi-label livre; criar
códigos sem economia na primeira passagem, fundir e podar depois; datar toda
mudança. Não buscar taxonomia perfeita na primeira iteração.

Saída: [[Security Taxonomy]], versionada. Processo: `notes/Methodology/QI-2 Methodology.md`.

### `CLASSIFICATION` — aplicar o codebook ⭐ caminho crítico da QI-1

Só depois do codebook estabilizado.

Como operar: aplicar R-1..R-9 em ordem, parando na primeira que decide; registrar
`evidence` (description / body / bundled_artifacts) e `confidence`; multi-label onde
previsto; usar `AMBIGUOUS` sem hesitação quando a evidência não sustenta; anotar a
regra que decidiu.

Nunca classifique sem citar a evidência textual. "Parece de segurança" não é
anotação.

Registrar sempre `language` (ISO 639-1, ou `mixed`, ou `und` — nunca `la`),
`language_detector_agreement` e `used_translation`. Se precisar de tradução para
decidir, o original é preservado e a tradução é apoio marcado — nunca substituição
(D-013). Preferir classificar **no idioma original** a traduzir antes: traduzir
introduz um erro que depois não se separa do erro do classificador.

**A contagem de positivos do classificador não é a prevalência.** Ela forma os
estratos; a estimativa vem do estimador estratificado (QI-1 Methodology §3).
Egami et al. (NeurIPS 2023) mostram que usar rótulos de surrogate diretamente produz
viés substancial e IC inválidos **mesmo com acurácia de 80–90%**.

### `COVERAGE` — QI-3, crosswalk

Só depois da taxonomia empírica estabilizada.

Como operar: escolher frameworks com justificativa (não todos); determinar
**aplicabilidade antes de cobertura**; construir crosswalk admitindo 1:1, 1:N, N:1 e
*sem correspondência*; usar a escala de seis níveis; rodar sensitivity analysis em
todo limiar. Processo: `notes/Methodology/QI-3 Coverage Methodology.md`.

Denominador **condicional**, sempre:

```text
   skills que cobrem P              e NUNCA:   skills que cobrem P
─────────────────────────                     ─────────────────────
 skills às quais P é aplicável                 todas as Security Skills
```

---

## Por que keyword sozinha não serve

Medido ([[EXP-001]]) — as frequências são fato; o *sentido* predominante é
**hipótese não testada** ([[02 - Hypotheses|H-2]]):

- `token` aparece em **20,69%** dos representantes. *Hipótese:* na maioria, token de
  LLM, não de autenticação. **Não verificada.**
- `audit` em **16,24%**. *Hipótese:* frequentemente "audit log" ou revisão genérica.
  *Caso real observado:* `meta-ads-audit` é auditoria de anúncios — `NONE` (R-5).
- `permission` em **10,07%**. *Hipótese:* permissão de arquivo ou de ferramenta.

H-2 é barata de testar (~20 ocorrências anotadas quanto ao sentido) e está marcada
como "fazer cedo". O léxico estrito do piloto exclui esses termos **com base na
hipótese** — se ela estiver errada, T0 concentrará Security Skills e a
estratificação perderá eficiência.
- Casamento apenas em `tags`/`category` não conta. *Caso real:* `go-playwright-v2`
  traz `category: testing-security` e é automação de browser — `NONE` (R-4).
- **Densidade de keyword não separa as classes.** Com ≥6 keywords distintas aparecem
  `security-review` (647) e `vulnerability-scanner` (91), mas também `code-review`
  (325) e `plan-ceo-review` (154).

Keyword serve para **candidate retrieval**, jamais como classificador.

> [!warning] O retrieval em inglês quase não filtra
> Recuperação ampla com 60 termos devolve **78,69% dos representantes**
> (1.477.763 de 1.877.981) — [[EXP-002]]. Não existe atalho por keyword: a redução
> real acontece na classificação. Ao escolher um retrieval mais estrito, o critério
> é **recall contra o gold set**, nunca tamanho do pool.
>
> E esse retrieval é **só em inglês** — inadequado como desenho final sob D-012.
> Substituto em `notes/Methodology/Multilingual Strategy.md` §3. Traduzir a lista de
> keywords **não** produz retrieval multilíngue confiável.

> [!warning] `code-review` não é "segurança incidental"
> É **`SECONDARY`**: tem seção dedicada e acionável (OWASP Top 10, injection, XSS,
> CSRF, falhas de authz). Descartá-lo como ruído seria erro de classificação, não
> limpeza de dados. É o nome mais frequente do conjunto (1.292 conteúdos), então
> `SECONDARY` tende a dominar — **sempre reporte PRIMARY e SECONDARY separados**.

### Sinal melhor que keyword

Parte das skills **declara o domínio** no front matter (`domain: cybersecurity`,
`metadata.category: cybersecurity`). Canal de recuperação potencialmente muito mais
preciso. Ver [[EXP-002]] para a medição.

---

## Eixos descritivos

Aplicam-se **apenas** a `PRIMARY` e `SECONDARY`, e são ortogonais à classe.

**Objeto protegido** — código produzido · agente/harness (prompt injection,
jailbreak, guardrails) · a própria skill.

**Postura** — defensivo (revisão, hardening, threat modeling) · ofensivo (pentest,
exploit dev, red team, CTF) · ambos · educacional.

> Percentuais que antes apareciam aqui (~4,98%, ~3,47%, ~2,30%) foram **removidos**:
> vinham de uma consulta exploratória avulsa, nunca salva em `results/` nem
> registrada num `EXP-XXX`. Todo número citado precisa de script e artefato.

Ofensivo não é ilegítimo: pentest e CTF são trabalho autorizado e pesquisa legítima.
Categoria descritiva, jamais juízo de malícia. Se alguma análise sugerir conteúdo
genuinamente malicioso, isso vira achado a relatar com cuidado — nunca rótulo
aplicado em massa por heurística.

---

## Eixo B: segurança **da** skill (D-007)

Duas perguntas diferentes, mantidas **independentes**:

| Eixo | Pergunta |
|---|---|
| **A** | O que a skill faz em segurança? |
| **B** | A própria skill opera de forma segura? |

**Nunca use o eixo B para decidir se a skill pertence ao domínio de segurança.** Uma
skill `NONE` que declara `allowed-tools: Bash(*)` é altamente relevante para
segurança e continua `NONE`.

Superfície mensurável neste dataset (material de QP-1/QP-2, não do codebook):

- **Execução:** `has_scripts = 1` em 214.507 representantes (11,4%); texto dos
  scripts em `artifact_siblings.content` (3.497.752 arquivos).
- **Permissões declaradas:** `allowed-tools` em ~10% de uma amostra de 2.000.
- **Auto-declaração de risco:** campos `risk` (~2,8%) e `disable-model-invocation`
  (~3,0%), fora da spec original.
- **Genealogia de clones:** 388.501 conteúdos com cópias, 60,8% das ocorrências.

**Cuidado causal:** divergência entre cópias não prova ataque. Bifurcação, adaptação
e melhoria são mais prováveis. Direção temporal só é defensável para os 458.548
arquivos com histórico — subconjunto MNAR, enviesado para locais padrão.

---

## Validação — nada disso é resultado sem isto

1. Codebook antes da anotação ✅ (v2.0)
2. Amostra anotada; **dois anotadores** quando viável
3. Discordâncias analisadas e adjudicação registrada
4. Concordância: **kappa ponderado** nos quatro ordinais (excluindo `AMBIGUOUS`,
   que está fora da ordem); kappa/α na dicotomia PRIMARY+SECONDARY vs resto;
   Krippendorff's α ou Jaccard nas dimensões multi-label
5. Gold set versionado em `results/`
6. Classificador automático validado contra o gold set: precisão, recall, F1
   **por classe** e para a dicotomia, com IC e matriz de confusão

> [!danger] LLM não é ground truth (D-008)
> Claude pode assistir triagem, sugerir códigos e pré-classificar em escala. Nada
> disso é verdade de referência. Todo uso em resultado registra modelo, versão,
> prompt e temperatura, e passa por validação contra gold set humano.

Camadas de denominador, sempre explícitas — ver `QI-2 Methodology` §5:
A (tudo que menciona) · B (PRIMARY+SECONDARY) · C (`security_focus`) ·
D (`operational_security`). A distância entre A e D é resultado potencial da
pesquisa, não pressuposto.

---

## Ameaças à validade

- **Multilinguismo — confirmado.** 48 casos de [[EXP-002]] trouxeram francês,
  chinês, russo, coreano, italiano e japonês. A população inclui todos os idiomas
  (D-012); [[EXP-003]] mede a distribuição. Risco real: léxico e âncoras enviesados
  para inglês reduzem o recall em outros idiomas e **subestimam a prevalência**
  neles. Avaliar desempenho **por idioma** — F1 global bom não é evidência de
  uniformidade.
- **Concentração por autor.** Existem pacotes publicados por fornecedor ("Anthropic
  Cybersecurity Skills"). Se replicarem muito, poucos autores dominam a distribuição
  de concerns — confundir **difusão** com **preocupação**.
- **Construto.** "Security Skill" é categoria nossa. Reporte sensibilidade a
  definições alternativas; se a conclusão só vale sob uma, isso é o achado.
- **Seleção.** GitSkills é limite inferior: só branch default, < 384 KB, repos
  ativos com < 500.000 arquivos, forks só com mais stars que o pai, e apenas
  repositórios públicos.
- **Sobrevivência.** Snapshot de julho/2026. Skills removidas — inclusive removidas
  *por serem* problemáticas — não aparecem.
- **Dependência.** 60,8% das ocorrências são cópias; deduplique por `file_sha` e
  verifique dominância por poucos repos ou donos.
- **Frequência ≠ importância.** Skill em 50.000 repos é mais copiada, não mais
  importante.
- **Ausência de evidência ≠ evidência de ausência.** Ver `QI-3 Coverage Methodology`
  §6 e as cinco explicações concorrentes obrigatórias para toda ausência observada.

## Regra

Nunca afirme que uma skill "é insegura", "tem vulnerabilidade" ou "é maliciosa" com
base em correspondência textual. Isso sustenta, no máximo, "o texto contém o padrão
X". Além disso exige inspeção manual do caso concreto — e, se envolver repositório
identificável, cuidado ético adicional antes de publicar.
