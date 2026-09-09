# ROTEIRO.md — Proposta de TCC

> Documento de trabalho para alinhamento com o orientador e base para a
> escrita formal do TCC. Reflete o estado real do repositório na branch
> `Q1` nesta data. Não é nota do caderno científico (`notes/`) nem
> substitui o `Decision Log` — cada afirmação metodológica remete à
> decisão ou ao experimento que a sustenta.
>
> **Convenção de honestidade dos números.** Este documento distingue três
> estados: **✅ concluído** (script versionado, saída em `results/`,
> `EXP-XXX` correspondente), **🟡 em andamento** (existe artefato parcial,
> falta etapa para virar resultado), **⬜ planejado** (desenhado, não
> executado). Nenhum número de prevalência ainda existe — isso é dito
> explicitamente onde relevante, não só uma vez no início.

---

## 1. Título provisório

**Prevalência de Skills de Segurança na População Pública de Agent Skills:
uma Estimativa Estratificada a partir do Dataset GitSkills**

Alternativas:

1. *Segurança em Agent Skills: Estimando a Prevalência na População
   Pública do GitSkills*
2. *Da Menção à Prática: Estimando a Prevalência de Segurança em Agent
   Skills Públicas com Amostragem Assistida por Classificador*
3. *Skills de Segurança na Prática: Prevalência e Desafios de
   Classificação em Artefatos de Instrução para Agentes de IA*

Critério de escolha entre elas: a primeira nomeia o método (estimativa
estratificada) no título, o que é mais preciso mas mais longo; a segunda
e a terceira priorizam legibilidade para um leitor fora do nicho. Decisão
cabe ao orientador/pesquisador.

---

## 2. Contextualização

Desde a publicação da especificação **Agent Skills** pela Anthropic (out.
2025), agentes de IA baseados em LLM passaram a carregar comportamento por
meio de pacotes de **linguagem natural** — pastas com um arquivo
`SKILL.md` que descreve, em prosa, quando e como uma capacidade deve ser
usada, opcionalmente acompanhado de scripts e arquivos de referência. O
agente decide **probabilisticamente em tempo de execução** se uma skill
se aplica à tarefa corrente.

Esse formato tem três propriedades que o tornam um objeto de interesse
para engenharia de software empírica e, especificamente, para segurança:
é instrução em linguagem natural (não código verificável por compilador),
é selecionado de forma não determinística, e é distribuído **sem package
manager, sem assinatura e sem registro central** — ao contrário de
pacotes npm, PyPI ou extensões de navegador, que têm ao menos alguma
camada de curadoria ou verificação.

Um artefato com essas propriedades pode **carregar ou transmitir**
práticas de segurança de duas formas distintas: (a) como *conteúdo* — a
skill instrui o agente sobre segurança (ex.: um scanner de
vulnerabilidades, uma revisão de código com checklist OWASP); ou (b) como
*comportamento estrutural da própria skill* — permissões declaradas em
`allowed-tools`, scripts empacotados, divergência entre cópias. Este TCC
trata do primeiro eixo; o segundo é discutido em §12 (Escopo e não
escopo) como extensão preservada, não descartada.

O dataset **GitSkills** (Destefanis, Graziotin, Vaccargiu & Ortu, MSR
'27, [arXiv:2608.10906](https://arxiv.org/abs/2608.10906)), coletado em
julho de 2026 e publicado sob CC-BY-4.0, é a primeira coleta em larga
escala desse ecossistema: 3.797.117 ocorrências de arquivo `SKILL.md` em
repositórios públicos do GitHub, das quais 1.877.981 são conteúdos
distintos. Isso cria uma oportunidade pouco comum em pesquisa de
segurança de software: medir empiricamente, numa população real e não
curada, algo que até agora só existe como preocupação declarada em texto
de especificação e em discussões de comunidade.

---

## 3. Problema de pesquisa

**Formulação.** Qual é a prevalência de skills relacionadas a segurança
na população pública de Agent Skills, e como essa prevalência se
distribui entre skills cujo propósito central é segurança e skills em
que segurança é uma capacidade acessória?

Isso é diferente de perguntar "quantas skills mencionam uma palavra de
segurança". O projeto já mediu essa segunda coisa como passo exploratório
inicial ([[EXP-001]], `results/_arquivo/EXP-001_profile.json`): **52,93%** dos
conteúdos distintos citam ao menos um termo de segurança no corpo, contra
apenas **4,09%** que declaram segurança no front matter (`name`/
`description`). O fator ~13× entre as duas medidas é o próprio motivo
pelo qual contagem de palavra-chave não responde à pergunta de pesquisa:
termos como `token` (20,69% dos casos), `audit` (16,24%) e `permission`
(10,07%) aparecem majoritariamente em sentido alheio a segurança — token
de contexto de LLM, log de auditoria genérico, permissão de arquivo — e
mesmo quando o termo casa em sentido correto, isso não distingue uma
skill cujo propósito é segurança de uma skill que apenas recomenda "guarde
credenciais com segurança" numa frase.

O problema científico não é apenas encontrar palavras relacionadas à segurança. 
Primeiro, é preciso definir claramente o que será considerado uma **skill de segurança**. 
Depois, é necessário usar um método de amostragem que permita estimar quantas 
dessas skills existem na população, com uma margem de incerteza conhecida.

---

## 4. Motivação e relevância

**Relevância científica.** O ecossistema de Agent Skills é recente
(especificação de out. 2025) e o próprio paper que introduz o GitSkills
declara usos pretendidos para o dataset sem executá-los — inclusive na
direção de segurança. Este trabalho ocupa essa lacuna com um método
explícito, o que é incomum na literatura ainda inicial sobre artefatos
agênticos: a maior parte do discurso sobre "segurança de agentes de IA"
hoje é qualitativa ou baseada em estudos de caso, não em prevalência
medida sobre uma população real.

**Relevância prática.** Se uma fração não trivial da população de skills
tem segurança como capacidade central ou substancial, isso importa para
quem consome esses artefatos sem revisão formal — desenvolvedores que
instalam skills de terceiros em agentes de codificação, por exemplo.
Inversamente, se a prevalência real for muito menor do que sugerem
métricas ingênuas de palavra-chave (como o fator 52,93% vs. 4,09% já
sugere), isso também é um resultado relevante: mostra o tamanho do erro
que uma leitura superficial do ecossistema cometeria.

**Relação com segurança de software, agentes de LLM e desenvolvimento
assistido por IA.** O trabalho se conecta a três linhas que normalmente
não se cruzam: (i) mineração de repositórios (MSR) aplicada a artefatos
de configuração/instrução, não a código-fonte tradicional; (ii)
segurança de sistemas baseados em LLM, onde a superfície de risco inclui
o próprio conteúdo textual interpretado pelo modelo; e (iii) supply
chain de desenvolvimento assistido por IA, um domínio em que ainda não
há mecanismo de registro ou assinatura equivalente ao de gerenciadores de
pacote tradicionais.

---

## 5. Objetivo geral

Estimar, com incerteza estatística quantificada, a prevalência de
**Security Skills** (`SEC-PRIMARY` + `SEC-SECONDARY`) na população pública
de Agent Skills representada pelo dataset GitSkills, e caracterizar essa
prevalência de forma desagregada (por classe, por idioma, por difusão).

Este objetivo é o núcleo do TCC e não muda com a decisão descrita abaixo.
O que muda ([[Decision Log#D-024]], 2026-08-27) é que, **uma vez validado
satisfatoriamente o classificador usado para alcançá-lo**, o projeto passa
a ter dois desdobramentos planejados e sequenciados — caracterizar os
tipos de preocupação de segurança presentes nas skills identificadas (Q2,
§9.6) e comparar esse resultado a referenciais de segurança reconhecidos
para investigar possíveis lacunas de cobertura (Q3, §9.7). Ambos são
condicionais a um **gate metodológico** (§9.5): não são garantidos como
entrega deste TCC, apenas planejados como próxima etapa se e quando o
classificador de Q1 atingir desempenho satisfatório.

## Objetivos específicos

Derivados diretamente de **QI-1** ([[Decision Log#D-011]]) e do desenho
metodológico em vigor (Desenho C, [[Decision Log#D-014]]):

1. **Definir e testar** um instrumento de classificação operacional para
   "skill de segurança", capaz de distinguir propósito central de
   capacidade acessória de menção incidental (E-1 — ✅; E-5/E-6 no novo
   desenho de [[Decision Log#D-026]] — ⬜).
2. **Caracterizar a população** em estrutura, integridade referencial e
   distribuição de idiomas, estabelecendo os denominadores corretos para
   qualquer percentual reportado (E-0, E-3, E-3b — ✅; denominador restrito
   a inglês calculado em [[EXP-013]] — 1.571.243 de 1.877.981, 83,667% —,
   sob o frame status quo de [[Decision Log#D-022]], ainda em aberto).
3. **Produzir um padrão-ouro** — sob [[Decision Log#D-026]] (2026-09-03), um
   conjunto misto de rótulos por consenso entre três LLMs e rótulos
   adjudicados por humano nos casos de discordância, com a fração de cada
   origem declarada — para servir de referência de validação (E-5/E-6 —
   ⬜).
4. **Treinar e validar um classificador de triagem** contra esse padrão-
   ouro, com desempenho reportado por classe e por idioma (E-7 — ⬜; uma
   prova de conceito de engenharia já existe fora do caminho crítico —
   ver §9, EXP-012). **Este objetivo também funciona como gate para os
   objetivos 8 e 9** ([[Decision Log#D-024]]).
5. **Classificar a população inteira** com esse classificador validado,
   para formar os estratos do estimador e o conjunto de entrada de Q2
   (E-8 — ⬜).
6. **Estimar a prevalência** de Security Skill com intervalo de confiança
   de 95%, desagregada em `PRIMARY`/`SECONDARY`, por conteúdo distinto e
   por ocorrência, com a taxa de `AMBIGUOUS` reportada à parte (E-9 —
   ⬜).
7. **Avaliar a robustez** dessa estimativa sob denominadores alternativos,
   exclusão de repositórios/donos concentradores, e definições
   alternativas de "skill de segurança" (E-10 — ⬜).
8. **(Condicional ao gate do objetivo 4 — Q2)** Caracterizar, por
   codificação qualitativa bottom-up sobre a população classificada como
   `PRIMARY`/`SECONDARY` em E-8, quais tipos de preocupação, prática ou
   tema de segurança aparecem no ecossistema, produzindo uma taxonomia
   emergente validada (§9.6 — ⬜, não iniciado).
9. **(Condicional ao objetivo 8 estar estabilizado — Q3)** Comparar a
   taxonomia emergente de Q2 com referenciais de segurança reconhecidos
   (ex.: OWASP, conforme já mapeado em [[QI-3 Coverage Methodology]]),
   para discutir possíveis lacunas de cobertura ou representação, com
   denominador condicional por aplicabilidade (§9.7 — ⬜, não iniciado;
   bloqueado também por [[Decision Log#D-009]], em aberto).

Cada objetivo específico corresponde a uma etapa nomeada do plano em
[[03 - Methodology]] (objetivos 1–7) ou nas metodologias de extensão
[[QI-2 Methodology]] / [[QI-3 Coverage Methodology]] (objetivos 8–9) — não
há objetivo sem etapa executora nem etapa sem objetivo que a justifique
(verificado nesta revisão; ver §18).

---

## 6. Questões de pesquisa

> [!important] Questão central adotada pelo pesquisador
> **QI-1. Qual a prevalência de skills de segurança na população pública
> de Agent Skills?** ([[Decision Log#D-011]], 2026-08-22)

Formalização: Security Skill = `SEC-PRIMARY` + `SEC-SECONDARY`
([[Codebook]] v2.3), sempre reportadas separadamente além do agregado,
porque `code-review` — uma skill de revisão genérica de código com seção
de segurança acionável — classifica como `SECONDARY` e é o nome mais
frequente entre as skills que declaram segurança no front matter (1.292
conteúdos distintos). Reportar só o agregado deixaria esse resultado
carregado por revisão de código genérica, não por skills especificamente
de segurança.

QI-1 é a questão nucleadora e a única no **caminho crítico imediato**
deste TCC — seu desenho (Desenho C, §9.1) não depende de QI-2 nem de
QI-3. Desde [[Decision Log#D-024]] (2026-08-27), porém, QI-2 e QI-3
deixaram de ser apenas "extensões documentadas para o futuro" e passam a
ter **execução planejada e formalmente sequenciada**, condicionada a um
gate metodológico sobre o classificador de QI-1 (§9.5):

> **QI-1 → validação satisfatória do classificador (E-7) → QI-2 → QI-3**

- **QI-2. Que tipos de preocupação de segurança as skills expressam, e
  como se distribuem?** Metodologia escrita (open coding bottom-up,
  taxonomia emergente, [[QI-2 Methodology]]), candidate retrieval já
  medido ([[EXP-002]], histórico — não é mais o conjunto de entrada
  planejado). Nenhuma distribuição foi calculada. Só começa depois de o
  classificador de QI-1 ser validado em E-7; o conjunto analisado é a
  população `PRIMARY`/`SECONDARY` produzida em E-8, não uma classificação
  preliminar (§9.6).
- **QI-3. Que lacunas existem — o que as skills de segurança *não*
  cobrem, frente a referenciais reconhecidos de segurança?** Metodologia
  escrita (crosswalk top-down, denominador condicional por
  aplicabilidade, [[QI-3 Coverage Methodology]]), não iniciada. Bloqueada
  por desenho até a taxonomia da QI-2 estabilizar — e, transitivamente,
  até o gate de QI-2 ser cumprido ([[Decision Log#D-009]], escopo de
  aplicabilidade, permanece em aberto separadamente; §9.7).

Se o gate não for cumprido dentro do prazo deste trabalho, QI-2 e QI-3
permanecem como trabalho futuro não executado — ver §14 e §15. Um
conjunto adicional de questões propostas pelo pesquisador durante a
exploração inicial (QP-1 a QP-5 — permissões declaradas, scripts
empacotados, divergência entre cópias, manutenção de skills de
segurança, convenções emergentes de risco) está registrado em
[[01 - Research Question]], mas nenhuma foi adotada como parte deste
TCC, nem está sujeita à sequência acima; são candidatas a trabalho
futuro, citadas em §14.

---

## 7. Definições fundamentais

A operacionalização completa está no [[Codebook]] v2.3 (10 seções,
regras R-1 a R-11); aqui, o essencial para entender o restante do
documento.

**Security Skill** (definição do pesquisador, [[Decision Log#D-004]]):
uma Agent Skill cujo **propósito principal**, ou uma **parte substancial
de seu comportamento operacional**, é prevenir, detectar, analisar,
avaliar, explorar, mitigar ou responder a ameaças, vulnerabilidades,
violações de propriedades de segurança ou controles de acesso em
sistemas computacionais. Presença de vocabulário de segurança nunca
basta por si só.

Cinco classes, ordinais e mutuamente exclusivas, com uma classe fora da
ordem:

| Classe | Significado |
|---|---|
| `SEC-PRIMARY` | segurança é o propósito central da skill |
| `SEC-SECONDARY` | segurança é capacidade ou etapa substancial de um objetivo maior |
| `SEC-MENTION` | recomendação ou observação incidental, não acionável |
| `NONE` | sem preocupação de segurança relevante |
| `AMBIGUOUS` | evidência insuficiente para classificar com confiança (fora da ordem; fica fora do numerador **e** do denominador de qualquer prevalência) |

**Por que a distinção é metodologicamente necessária.** A fronteira que
efetivamente decide o número final da pesquisa é `SECONDARY` × `MENTION`
— confundir `PRIMARY` com `SECONDARY` não altera a prevalência agregada
(ambos contam como Security Skill), mas confundir `SECONDARY` com
`MENTION` altera diretamente. O caso `code-review` ilustra o teste
operacional (R-1, "teste de remoção"): removido o conteúdo de segurança,
a skill perderia capacidade operacional descrita (seção com OWASP Top
10, injeção, XSS, CSRF, falhas de autorização) → `SECONDARY`. Já uma
skill que apenas escreve *"Store credentials in a secure config"* não
perde nada de operacional ao remover essa frase → `MENTION` (R-2, "teste
de acionabilidade": conteúdo acionável diz **o que fazer**, não apenas o
que evitar).

Regra auxiliar relevante para a formulação do problema (§3): recuperação
por palavra-chave mede *menção*, não *propósito* — daí o fator ~13× entre
52,93% (keyword) e 4,09% (front matter declarado), e daí a necessidade
do instrumento de cinco classes em vez de um filtro binário de texto.

---

## 8. Dataset e unidade de análise

**GitSkills** — quatro tabelas relacionadas por chave exata (sem fuzzy
matching neste projeto):

| Tabela | Linhas | Grão |
|---|---|---|
| `artifacts` | 3.797.117 | uma **ocorrência** de arquivo `SKILL.md` |
| `artifact_siblings` | 7.264.865 | um arquivo/diretório vizinho de um representante |
| `repos` | 282.200 | um repositório |
| `mining_runs` | 7 | uma execução de coleta |

**População considerada.** Restrita a **skills em inglês** desde 2026-09-03
([[Decision Log#D-025]], revisa [[Decision Log#D-012]]). Denominador real
calculado em [[EXP-013]] (2026-09-03): **1.571.243 de 1.877.981
conteúdos distintos (83,667%)** passam no critério de 100% inglês;
306.738 (16,333%) ficam fora. Sem duplicatas. Válido enquanto
[[Decision Log#D-022]] (elegibilidade da população) permanecer com o
frame status quo — se mudar, recalcular.

**Unidade de análise.** `artifacts` mistura dois grãos na mesma tabela:
cada linha é uma *ocorrência* de arquivo, mas apenas as linhas com
`dedup_primary = 1` (1.877.981 de 3.797.117) têm `content`, front matter
e composição preenchidos — as demais só têm metadados de localização. A
unidade primária adotada é o **conteúdo distinto** (`dedup_primary = 1`),
com contagem por ocorrência reportada em paralelo como medida de difusão
([[Decision Log#D-001]]). Justificativa: contar ocorrência faz uma
skill popular copiada milhares de vezes pesar proporcionalmente mais que
uma escrita à mão, o que é viés puro para uma pergunta sobre "o que se
escreve".

**Problemas relevantes, já verificados nos dados:**

- **Duplicatas e near-duplicates.** 60,8% das ocorrências (2.307.637 de
  3.797.117) são cópias de um conteúdo que aparece mais de uma vez. Pior:
  a deduplicação por hash **não elimina near-duplicates**
  ([[EXP-002]]) — pacotes replicados entre donos com variações mínimas
  produzem `file_sha` distintos e continuam contando como observações
  independentes quando não são. Isso enfraquece a premissa "1 conteúdo =
  1 voto" sem invalidar a escolha de unidade; toda estimativa deste TCC
  reporta concentração por repositório **e** por dono
  ([[Decision Log#D-001]] ressalva). Deduplicação semântica fica como
  análise de robustez, não como pipeline principal
  ([[Decision Log#D-017]]).
- **Idiomas.** 14,21% ± 0,48 pp da população completa não é inglês
  ([[EXP-003]]), com direção de viés conhecida (superestimação —
  [[EXP-004]]). A detecção agora serve de **filtro** para a restrição a
  inglês ([[Decision Log#D-025]]), não de eixo de estratificação; ainda
  sem acurácia medida contra julgamento humano (§9.3).
- **Concentração por repositório/autor.** 282.200 repositórios, 195.841
  contas distintas. Repositórios concentram muitas skills e contas
  concentram muitos repositórios — qualquer resultado precisa reportar
  quantos repositórios e quantos donos distintos o sustentam, e não pode
  assumir independência entre observações.
- **Elegibilidade da população — questão em aberto.** O único filtro
  operacional hoje é `dedup_primary = 1 AND content IS NOT NULL`, mas o
  próprio paper do GitSkills documenta que o frame de descoberta (por
  nome de arquivo) inclui falsos positivos deliberados e artefatos
  anteriores ao formato. Pelo menos ~12,7 mil unidades (0,7%) são
  inelegíveis por inspeção óbvia (stubs de menos de 80 caracteres,
  alvos de symlink); quantas mais existem é desconhecido. Esta é uma
  **decisão pendente de aprovação humana** ([[Decision Log#D-022]], em
  aberto) que afeta diretamente o denominador de QI-1 — ver §11 e §13.

---

## 9. Metodologia

### 9.1 Desenho amostral adotado — Desenho C

O desenho principal ([[Decision Log#D-014]]) é **amostragem estratificada
com classificador de triagem**:

1. um classificador automático atribui uma classe *prevista* a toda a
   população;
2. essa previsão **não é o resultado científico** — serve só para formar
   estratos (classe prevista, e grupo linguístico enquanto a população era
   multilíngue; desde [[Decision Log#D-025]] a população é restrita a
   inglês e esse segundo eixo deixa de ser central — ver §9.3);
3. sorteia-se uma amostra probabilística **dentro de cada estrato**;
4. os itens amostrados são anotados manualmente por um humano;
5. a prevalência final é estimada por ponderação estratificada sobre a
   anotação humana, não sobre a previsão do modelo.

Estimador:

$$\hat{p} = \sum_h \frac{N_h}{N}\,\hat{p}_h \qquad
\widehat{\mathrm{Var}}(\hat{p}) = \sum_h \left(\frac{N_h}{N}\right)^{2}
\left(1 - \frac{n_h}{N_h}\right)\frac{\hat{p}_h(1-\hat{p}_h)}{n_h - 1}$$

com `N_h` o tamanho do estrato na população, `n_h` o tamanho da amostra
anotada naquele estrato, e `p̂_h` a proporção de Security Skill observada
**na anotação humana** — nunca na previsão do modelo. O fator
`(1 - n_h/N_h)` é a correção para população finita, relevante em estratos
pequenos com sobre-amostragem forte (ex.: idiomas minoritários).

**Papel do classificador — e seu limite.** Sob seis condições de
validade explícitas (cobertura total da população, nada descartado por
previsão, seleção probabilística dentro do estrato, `N_h` correto,
partição — cada unidade em exatamente um estrato —, e desfecho = anotação
humana), o erro do classificador de triagem afeta **principalmente a
eficiência** da estratificação (estratos menos puros exigem amostras
maiores para a mesma precisão), não a validade da estimativa em si. Isso
não é garantia absoluta: se o erro do classificador quebrar alguma das
seis condições — por exemplo, correlacionar-se simultaneamente com o
desfecho e com a chance de seleção — a validade é comprometida.

O desenho tem apoio na literatura de inferência estatística com rótulos
substitutos: Egami et al. (NeurIPS 2023, *Design-based Supervised
Learning*) mostram que usar diretamente saídas de classificador como se
fossem o desfecho produz viés substancial e intervalos de confiança
inválidos mesmo com classificadores de 80–90% de acurácia — e que a
correção exige amostragem probabilística de rótulos-ouro, exatamente o
que o Desenho C implementa.

**Alternativa descartada explicitamente:** classificar toda a população
com um modelo (LLM ou não) e contar os positivos como se fosse a
prevalência (Desenho B). Rejeitada porque herda o viés do classificador
sem quantificá-lo — não é estimativa, é saída de modelo. Este ponto é
central e será retomado em §10, porque é exatamente o erro que um
resultado preliminar já produzido no projeto (EXP-012) **não pode**
cometer ao ser reportado.

### 9.2 Classificação em duas etapas: classificador ≠ validação

Este é o ponto do desenho mais fácil de comunicar mal, então vale
explicitar a separação de papéis:

| Papel | Instrumento | O que produz | Pode virar prevalência? |
|---|---|---|---|
| Formar estratos | classificador de triagem, roda na população inteira | classe prevista por item, `N_h` | **não** |
| Medir o desfecho | anotação humana, roda só na amostra | classe verdadeira por item amostrado, `p̂_h` | insumo do estimador |
| Responder a QI-1 | estimador estratificado (§9.1) | `p̂` com IC | **sim** |

O classificador nunca é avaliado contra si mesmo, e a anotação humana
nunca é substituída por consenso entre modelos ([[Decision Log#D-008]]:
LLM não é ground truth).

### 9.3 Golden set e validação do classificador

> [!important] Desenho substituído em 2026-09-03 — [[Decision Log#D-025]] e [[Decision Log#D-026]]
> Por decisão do orientador, duas coisas mudaram desde a versão anterior
> deste roteiro: (1) a população-alvo passa a ser restrita a **skills em
> inglês** ([[Decision Log#D-025]], revisa [[Decision Log#D-012]]); (2) o
> padrão-ouro deixa de vir de um piloto humano cego estratificado por
> idioma e passa a vir de um **ensemble de três LLMs com adjudicação
> humana restrita aos casos de discordância** ([[Decision Log#D-026]],
> revisa [[Decision Log#D-019]]).

O padrão-ouro (E-5/E-6, ⬜) passa a ser produzido assim:

1. sorteia-se uma amostra **aleatória nova de n = 100**, sobre a população
   restrita a inglês — não os 50 casos de [[EXP-005]], que foram
   estratificados sob o desenho multilíngue anterior e não são
   reaproveitados aqui;
2. três modelos — **GPT-5.6 Sol**, **Claude Opus** e **Gemini 3.1 Pro** —
   classificam os 100 casos **independentemente**, aplicando o
   [[Codebook]] v2.3, sem ver o sinal preliminar de triagem;
3. onde os três **concordam**, o rótulo de consenso é aceito;
4. onde **discordam**, um anotador humano adjudica o caso.

> [!danger] Isto reverte uma restrição que o projeto tratava como inegociável
> [[Decision Log#D-019]] proibia explicitamente usar consenso entre
> modelos como substituto de confiabilidade interavaliadores humana, e
> [[Decision Log#D-008]] afirma que LLM nunca é verdade de referência sem
> validação humana. Sob este novo desenho, os casos em que os três LLMs
> concordam **nunca são vistos por um humano** — o consenso entre modelos
> funciona, na prática, como ground truth para a maior parte da amostra (a
> fração exata depende da taxa de discordância, ainda desconhecida). Isto
> é registrado explicitamente, por instrução do orientador — não aplicado
> em silêncio.

**Riscos declarados, não resolvidos por este desenho** (detalhe completo
em [[Decision Log#D-026]]):

- **viés sistemático compartilhado entre os três modelos fica invisível**
  nos casos de consenso — [[EXP-012]] já mostrou, com dados de validação
  cruzada, que um classificador barato falha sistematicamente na fronteira
  `SECONDARY`/`MENTION` (F1 = 0,000 em todos os 5 repeats); se os três
  LLMs compartilharem esse tipo de dificuldade, nada neste desenho captura
  o erro;
- **amostragem aleatória simples, não estratificada** — diferente do
  piloto anterior (que sobre-amostrava deliberadamente a fronteira
  `SECONDARY`/`MENTION`), esta amostra pode conter poucos casos
  `PRIMARY`/`SECONDARY` e menos ainda na fronteira mais informativa;
- **a estatística de confiabilidade muda de natureza** — o framework de
  kappa do [[Codebook]] §9 pressupõe dois anotadores humanos
  independentes; aqui a métrica análoga (concordância unânime entre LLMs,
  taxa de adjudicação humana) não é equivalente e deve ser reportada como
  tal, não como um kappa interavaliadores humano.

O classificador definitivo (E-7, ⬜) é validado contra esse padrão-ouro
misto com precisão, recall e F1 **por classe**, com intervalo de
confiança e matriz de confusão completa; o eixo "por idioma" deixa de ser
central porque a população-alvo já é aproximadamente monolíngue por
construção (§9.4). A análise de erro exigida distingue explicitamente o
impacto de cada tipo de confusão:

| Confusão | Impacto na prevalência agregada |
|---|---|
| `PRIMARY` ↔ `SECONDARY` | nenhum — muda só a desagregação |
| **`SECONDARY` ↔ `MENTION`** | **direto — é o erro que decide o resultado** |
| `MENTION` ↔ `NONE` | nenhum |
| qualquer classe ↔ `AMBIGUOUS` | muda o denominador |

### 9.4 Como o erro do classificador entra na estimativa de prevalência

Formalmente, o erro do classificador de triagem **não** entra na fórmula
do estimador da §9.1 — porque o desfecho ali é `p̂_h` da anotação humana,
não da previsão. O erro entra por dois caminhos indiretos, ambos já
antecipados no desenho:

1. **Eficiência.** Um classificador ruim produz estratos impuros, o que
   exige amostras maiores por estrato para atingir a mesma margem de
   erro. Isso é custo, não viés.
2. **Validade condicional.** Se o erro do classificador for
   correlacionado com o próprio desfecho *e* isso afetar a probabilidade
   de seleção de forma não corrigida, a estimativa deixa de ser válida.
   Sob a população multilíngue anterior, isso motivava medir desempenho
   **por idioma** e estratificar por grupo linguístico. Desde
   [[Decision Log#D-025]] (2026-09-03), a população-alvo é restrita a
   inglês, então esse mecanismo específico deixa de ser o principal — mas
   o princípio permanece: qualquer variável em que o classificador erre de
   forma correlacionada com a seleção (por exemplo, comprimento do texto,
   presença de scripts) precisa ser considerada.

Tratamento de `AMBIGUOUS`: como sua taxa varia por estrato, o denominador
de itens classificáveis é ele próprio uma quantidade estimada, e o
estimador correto é uma **razão entre dois estimadores estratificados**
(proporção de Security Skill sobre proporção de não-`AMBIGUOUS`), com
variância por método delta ou bootstrap estratificado — não pela fórmula
de proporção simples da §9.1. Limites inferior/superior (`p_min`,
`p_max`, tratando todo `AMBIGUOUS` como não-Security ou como Security,
respectivamente) são reportados junto. Está proposto, mas ainda não
aprovado como regra final, um teto: se a taxa ponderada de `AMBIGUOUS`
superar 20%, a prevalência não seria reportável como número pontual,
apenas como intervalo.

### 9.5 A sequência Q1 → validação → Q2 → Q3 e o gate metodológico

> [!important] Decisão formal — [[Decision Log#D-024]] (2026-08-27)
> QI-2 e QI-3 têm execução planejada, na ordem **QI-1 → validação
> satisfatória do classificador de triagem (E-7) → QI-2 → QI-3**. Isso não
> altera nada do desenho já estabelecido para QI-1 (§9.1–§9.4); acrescenta
> o que acontece **depois**, se e quando o classificador atingir
> desempenho satisfatório.

**Por que o gate é a validação do classificador, e não a estimativa final
de prevalência.** QI-2 precisa apenas do **conjunto de skills
classificado como Security Skill** — a saída de E-8 (classificação da
população pelo classificador validado) — não da estimativa de prevalência
com IC de E-9, nem da robustez de E-10, nem da consolidação de E-11. Por
isso o gate está posicionado logo após E-7, e E-9/E-10/E-11 podem correr
em paralelo a QI-2/QI-3 em vez de bloqueá-las. Formalmente:

```text
E-6  gold set humano
   |
E-7  classificador validado  ─────────────────────►  GATE
   |                                                    |
E-8  classificação da população                         |
   |            \                                       |
   |             \── conjunto SEC-PRIMARY/SECONDARY ─────┘
   |                          |
E-9  estimativa (QI-1)        ▼
E-10 robustez (QI-1)     Q2  taxonomia emergente (§9.6)
E-11 consolidação (QI-1)      |
                               ▼
                          Q3  crosswalk / cobertura (§9.7)
```

**Por que a validação funciona como gate, não como formalidade.** Usar a
saída de um classificador **não validado** como base para Q2 repetiria,
na QI-2, exatamente o erro que o Desenho C existe para evitar na QI-1
(Desenho B, §9.1: contar previsões de modelo como se fossem resultado). A
prova de conceito já executada (EXP-012, §11.3) é um exemplo concreto do
risco: o modelo implantado nela tem F1 = 0,000 documentado para
`SECONDARY` em toda a validação cruzada — se um classificador com essa
falha fosse usado para formar o conjunto de entrada de Q2, a taxonomia
emergente **nunca veria** exemplos de `SECONDARY`, e a distorção entraria
na análise qualitativa sem ser percebida como tal. **Se o desempenho de
E-7 não for suficiente para sustentar essa base, o método deve ser
revisado antes de avançar para Q2** — não se prossegue com um conjunto
identificado por um classificador conhecidamente fraco.

> [!warning] Critério de "satisfatório" — decisão pendente, não inventada aqui
> Este projeto **ainda não define numericamente** o que conta como
> validação satisfatória (ex.: F1 mínimo por classe, recall mínimo para
> `SECONDARY` — a classe cuja confusão com `MENTION` decide a prevalência,
> §9.3 —, desempenho mínimo por idioma). E-7 já exige que essas métricas
> sejam medidas e reportadas com IC; não exige, ainda, um limiar de
> aprovação. Fixar esse limiar **antes** de ver o resultado de E-7 é
> trabalho pendente — inventar um número aqui repetiria o erro que o
> Desenho C existe para evitar (ajustar critério depois de ver o dado).
> Até essa decisão ser tomada, avançar ou não para Q2 é julgamento humano
> caso a caso, não uma regra automática.

### 9.6 Metodologia de Q2 — taxonomia emergente de preocupações de segurança

**Status: planejado, não iniciado.** Nenhuma distribuição foi calculada;
nenhuma categoria abaixo é definitiva. O que segue resume o desenho já
registrado em [[QI-2 Methodology]], sem antecipar resultado.

**Conjunto de skills analisado.** A partir do gate de §9.5: a população
classificada como `SEC-PRIMARY`/`SEC-SECONDARY` pelo classificador
**validado** de E-7, produzida em E-8 — não o pool de candidate retrieval
por palavra-chave de [[EXP-002]] (78,69% dos representantes, §11.1),
que serviu apenas como exploração inicial e histórico, e não como base de
entrada sob esta decisão. Dentro desse conjunto, a amostragem para
codificação qualitativa é separada da amostragem de prevalência de QI-1
— usar a mesma amostra estratificada para as duas coisas infla
artificialmente as classes sobre-amostradas ([[QI-2 Methodology]] §3).

**Como a análise qualitativa/categorização será feita.** Abordagem
**bottom-up**: open coding sobre o texto das skills classificadas, sem
partir de um framework externo. Três dimensões nunca colapsadas — sobre
qual preocupação a skill atua (`security_concern`), o que ela faz em
relação a essa preocupação (`security_function`: PREVENT/DETECT/ASSESS/
TEST/RESPOND/RECOVER) e como ela operacionaliza isso
(`operational_capability`) — porque o mesmo `concern` pode ter
comportamentos completamente diferentes (ex.: SQL Injection detectado e
testado vs. SQL Injection prevenido por revisão de código).

**Como categorias emergentes serão criadas, refinadas e consolidadas.**
Processo iterativo, registrado a cada rodada (códigos novos, códigos
fundidos, códigos abandonados, casos fronteiriços): amostra exploratória
→ open coding → códigos recorrentes → agrupamento conceitual → codebook
preliminar → nova amostra → refinamento → repetir até estabilizar →
taxonomia estabilizada. O histórico de mudanças fica versionado (ver
[[Security Taxonomy]]). Refinar o codebook depois de ver o resultado
final é racionalização, não refinamento — mudanças só entre iterações
declaradas, nunca depois de fechar uma leitura.

**Etapas que exigem validação humana.** Todas as etapas de rotulagem.
Especificamente: (i) o próprio open coding é humano, não delegado a LLM;
(ii) a versão estabilizada do codebook precisa de amostra anotada por
humano, idealmente com dois anotadores independentes e adjudicação
registrada de discordâncias; (iii) a classificação final em escala exige
validação contra esse gold set (precisão, recall, F1 por classe, com IC e
matriz de confusão) antes de qualquer número ser reportado. LLM pode
assistir triagem e sugerir códigos candidatos — como já ocorreu na
primeira passagem exploratória registrada em [[Security Taxonomy]] v0.1
— mas nunca é ground truth ([[Decision Log#D-008]]); toda saída de LLM
usada precisa registrar modelo, versão, prompt e temperatura.

**Como se evita que uma taxonomia externa determine antecipadamente as
categorias.** Por regra explícita e anterior à análise
([[QI-2 Methodology]]): **nunca usar OWASP, MITRE ou qualquer referencial
externo para construir a taxonomia empírica de Q2.** Fazer isso criaria
circularidade — encontrar apenas o que já se esperava encontrar — e
esconderia preocupações próprias do ecossistema de Agent Skills que
nenhum framework existente cobre. Referenciais externos só entram
**depois** da taxonomia estabilizada, exclusivamente como instrumento de
comparação em Q3 (§9.7), nunca como fonte das categorias de Q2.

**Denominadores.** Reportados em camadas explícitas, para não deixar
`MENTION` dominar uma distribuição de "tudo que menciona segurança":
proporção sobre toda ocorrência relacionada a segurança, sobre
`PRIMARY`+`SECONDARY`, sobre `security_focus = true` e sobre
`operational_security = true` separadamente — a distância entre essas
camadas é, em si, um resultado potencial (segurança mencionada vs.
segurança operacionalizada), não algo a assumir antes de medir.

### 9.7 Metodologia de Q3 — cobertura frente a referenciais externos

**Status: planejado, não iniciado, bloqueado por Q2.** O único insumo já
produzido é um sinal preliminar de 48 casos ([[EXP-002]]): duas skills
(`cybersec-testing-ransomware-recovery`, `ics-monitoring-dragos`) sem
correspondência no OWASP Top 10 — indício, não conclusão, de que um único
framework não cobre o objeto. O que segue resume o desenho já registrado
em [[QI-3 Coverage Methodology]].

**Papel dos referenciais externos.** Explicitamente **instrumento de
comparação**, nunca fonte das categorias de Q2 (§9.6). Candidatos já
mapeados, com o que cada um permite observar e sua limitação: OWASP Top
10 (vulnerabilidades de aplicação clássicas; não cobre agente/LLM), OWASP
Top 10 for LLM/GenAI (prompt injection, data leakage; categorias ainda em
evolução), OWASP Top 10 for Agentic Applications (uso indevido de
ferramenta, autonomia; estabilidade a verificar), MITRE ATLAS (táticas
adversariais contra ML; não orientado a prática de desenvolvimento), NIST
CSF (PREVENT/DETECT/RESPOND/RECOVER; alto nível, pouca granularidade). A
escolha entre eles precisa de justificativa registrada, não é feita por
completude.

**Lógica da comparação — dados primeiro, referencial depois.**

```text
dados → categorias observadas em Q2 → comparação com referenciais
externos em Q3 → identificação e discussão de possíveis lacunas
```

Nunca a ordem inversa. O crosswalk mapeia a taxonomia empírica de Q2
contra cada framework (relações 1:1, 1:N, N:1 ou sem correspondência);
categorias empíricas sem correspondência externa são, em si, um resultado
(preocupações próprias do ecossistema, não capturadas pelos referenciais)
e categorias externas sem correspondência empírica são o material de
lacuna propriamente dito.

**Denominador condicional — nunca a população inteira de Security
Skills.** Calcular lacuna sobre todas as Security Skills produz lacuna
artificial (prompt injection não é esperado numa skill que não interage
com LLM). O denominador correto é *skills às quais a preocupação é
aplicável*, não *todas as Security Skills*. Determinar aplicabilidade é
uma classificação própria — derivada, quando possível, de atributos já
anotados em Q2 (concern, capability, artefato-alvo), com um rótulo
`uncertain` explícito que nunca é somado silenciosamente a nenhum lado.
O escopo de aplicabilidade de cada preocupação é uma **decisão pendente
de aprovação humana** separada ([[Decision Log#D-009]]) — determina o
próprio denominador de Q3 e precisa ser fixado antes do cálculo.

**Como se evita tratar ausência como evidência de vulnerabilidade.**
Regra explícita: zero ocorrências observadas nunca é prova de
inexistência. Em vez de "as skills não cobrem X", a linguagem exigida é
"não foi observada cobertura explícita de X segundo os critérios
adotados" ou "X apresentou cobertura limitada entre as skills para as
quais o risco foi considerado aplicável". Para toda ausência observada,
cinco explicações concorrentes precisam ser consideradas antes de
qualquer leitura como lacuna real: a preocupação de fato não é coberta;
está descrita com outra terminologia (inclusive em outro idioma); o
método de classificação não a identificou; não é aplicável àquela
população; ou a informação está em artefatos empacotados ainda não
examinados (`composition_truncated = 1`, 13,4% dos representantes). Uma
escala de seis níveis (`STRONG_COVERAGE` a `NOT_APPLICABLE`, passando por
`UNCERTAIN`) substitui o binário coberto/não coberto, e qualquer limiar
quantitativo usado nela passa por análise de sensibilidade antes de
sustentar uma conclusão.

---

## 10. Pipeline experimental

Ordem **metodológica**, não cronológica de criação dos arquivos —
reconstruída a partir de [[03 - Methodology]] e do Decision Log.

```text
E-0  Auditoria estrutural                         ✅ EXP-001
E-1  Definição e instrumento (Codebook)           ✅ D-004/D-006, Codebook v2.3
E-2b Candidate retrieval (inglês)                 ✅ EXP-002
        |
E-3  Distribuição de idiomas                      ✅ EXP-003
E-3b Concordância entre detectores de idioma      ✅ EXP-004
        |
(D-025)  restrição da população a inglês (2026-09-03, orientador)
        |
E-5/E-6  amostra n=100 (inglês) + ensemble de 3 LLMs   ⬜ (D-026; substitui
         (GPT-5.6 Sol, Claude Opus, Gemini 3.1 Pro) +      o piloto humano
         adjudicação humana na discordância                cego anterior)
        |
E-4  Candidate retrieval reordenado, por recall    ⬜ (depois de E-5/E-6, ver abaixo)
        |
E-7  Classificador validado                        ⬜
        |
E-8  Classificação da população -> estratos (N_h)  ⬜
        |
E-9  Estimativa de prevalência com IC               ⬜ ← responde QI-1
        |
E-10 Robustez e revisão adversarial                 ⬜
        |
E-11 Literatura e consolidação                       ⬜ (literatura pode correr em paralelo)
```

**Por que o candidate retrieval (E-4) vem depois do gold set (E-6), e
não antes.** Essa é uma reordenação deliberada e aprovada
([[Decision Log#D-018]]), não um acidente de execução. Sob o Desenho C, o
retrieval não determina elegibilidade — nenhuma skill é descartada por
não ser recuperada por palavra-chave, diferente de um desenho onde o
retrieval filtraria a população antes da amostragem. A escolha entre
retrieval lexical e semântico deve ser feita por **recall medido contra
um gold set independente** (produzido pelo desenho de
[[Decision Log#D-026]] — consenso entre LLMs + adjudicação humana na
discordância, §9.3); fixar o retrieval antes de esse gold set existir
criaria circularidade — o instrumento de recuperação passaria
a definir aquilo contra o que ele próprio seria avaliado depois.

**Uma ramificação paralela, fora do caminho crítico:** EXP-012 (§11)
usou um golden set assistido por LLM (não o gold set humano de E-6) para
provar o pipeline de treino → comparação de modelos → classificação em
escala ponta a ponta. Não substitui nenhuma etapa E-6/E-7/E-8 e está
identificado dessa forma em todo o projeto ([[Decision Log#D-023]]).

**Nota sobre numeração.** O plano metodológico ([[03 - Methodology]],
[[QI-1 Methodology]]) reserva `EXP-006` a `EXP-011` para as etapas E-6 a
E-11 do caminho crítico. Como esses números ainda não foram usados, a
prova de conceito paralela recebeu o número seguinte disponível,
`EXP-012`, especificamente para não colidir com a reserva. Pelo mesmo
motivo, nenhum número `EXP-XXX` é reservado agora para as etapas de Q2/Q3
— serão numerados quando cada etapa efetivamente rodar, seguindo a mesma
convenção.

**Depois de E-7 — a sequência gated para Q2 e Q3
([[Decision Log#D-024]]).** Este pipeline cobre apenas o caminho crítico
de QI-1. A partir de E-7 (classificador validado), o projeto tem uma
segunda ramificação planejada e condicionada a um gate de desempenho —
diagrama completo, papel do gate e o que ainda está pendente de decisão
em §9.5; metodologia de cada etapa em §9.6 (Q2) e §9.7 (Q3). Em resumo:

```text
                     E-7 validado (gate) ──▶ E-8 classificação
                                                    │
                    E-9 → E-10 → E-11        Q2 taxonomia emergente
                    (continuam QI-1,               │
                     em paralelo)             Q3 crosswalk / cobertura
```

Nenhuma etapa de Q2/Q3 está marcada como concluída ou em andamento neste
documento — todas são ⬜, porque o gate (E-7) ainda não foi executado.

---

## 11. Resultados preliminares

> [!warning] Nenhum destes números é a resposta da QI-1
> Nenhum resultado abaixo passou pelo padrão-ouro humano (E-6) nem pelo
> classificador validado (E-7). Todos são exploratórios ou de prova de
> conceito, e assim identificados individualmente.

### 11.1 Resultados exploratórios (E-0, população inteira, sem classificação)

De [[EXP-001]], `results/_arquivo/EXP-001_profile.json` — medem *menção*, não
*prevalência de propósito*:

- **52,93%** dos 1.877.981 conteúdos distintos citam ao menos um termo de
  segurança no corpo do texto.
- **4,09%** dos 1.625.701 conteúdos com `name`/`description` preenchidos
  declaram segurança nesses campos.
- Fator ~13× entre as duas medidas — evidência direta de que palavra-
  chave mede menção, não propósito (§3, §7).
- **78,69%** dos representantes citam algum termo de segurança sob o
  léxico mais amplo de candidate retrieval ([[EXP-002]]) — outro número
  que reforça a mesma conclusão: recuperação por palavra-chave não é
  filtro útil para esta pergunta.

O resultado de um notebook exploratório anterior a este projeto ("1,1%
das skills mencionam segurança") está formalmente **invalidado**
([[Decision Log#D-002]]): foi calculado sobre as primeiras 5.000 linhas
do Parquet sem ordenação — um bloco patologicamente não representativo
(mediana de 42 caracteres, majoritariamente alvos de symlink). Não é
citável.

### 11.2 Distribuição de idiomas (E-3/E-3b)

> [!important] Histórico — [[Decision Log#D-025]] (2026-09-03)
> Medida antes da restrição a inglês. Continua válida; agora alimenta um
> filtro, não uma estratificação.

- **14,21% ± 0,48 pp** da população completa não é escrita em inglês
  (chinês sozinho ~6%) — [[EXP-003]]. Direção de viés conhecida:
  provavelmente superestimado, porque o detector confunde texto técnico
  inglês com idiomas raros.
- Concordância entre dois detectores independentes: **0,987 global**
  (0,967–1,000 por grupo linguístico) — [[EXP-004]] v2. É concordância
  entre instrumentos automáticos, **não acurácia contra julgamento
  humano** — essa medida segue sem existir, porque o novo E-5/E-6
  ([[Decision Log#D-026]]) não é mais uma anotação humana completa.
- **Denominador real sob o critério de 100% inglês** (não o mesmo método
  de EXP-003 acima — ver [[EXP-013]]): **83,667%** da população
  (1.571.243 de 1.877.981) passam; 16,333% (306.738) ficam fora por
  conter ao menos um parágrafo em outro idioma. Número mais baixo que os
  85,79% que EXP-003 sugeriria, porque o critério por parágrafo pega
  mistura que a detecção de idioma dominante do documento inteiro não
  pegava.

### 11.3 Prova de conceito do classificador — EXP-012 (fora do caminho crítico)

> [!danger] Não confundir com um resultado preliminar da QI-1
> O golden set usado aqui (n=49, excluindo 1 `AMBIGUOUS`) foi **anotado
> com assistência de LLM**, não por um humano seguindo o protocolo de E-6
> — é o "golden set operacional v1" da prova de conceito, congelado no
> commit `a90ce044...` ([[Decision Log#D-023]]). Trata-se de uma
> demonstração de engenharia (o pipeline treino→validação→classificação
> roda ponta a ponta), não de uma medição científica válida da
> prevalência.

Três modelos foram comparados por validação cruzada agrupada e repetida
(`StratifiedGroupKFold`, 5 splits × 5 seeds, agrupada por repositório
para não vazar conteúdo do mesmo repo entre treino e validação):

| Modelo | Representação | F1 binário (Security vs. resto) | macro-F1 (4 classes) |
|---|---|---|---|
| A — TF-IDF + Regressão Logística | n-gramas de caractere | 0,158 | 0,209 |
| B — TF-IDF + SVM Linear | n-gramas de caractere | 0,206 | 0,208 |
| **C — Embeddings multilíngues + Regressão Logística** | `paraphrase-multilingual-MiniLM-L12-v2` | **0,663** | **0,467** |

**Achado que decidiu contra os modelos TF-IDF por si só:** nos modelos A
e B, as classes `SECONDARY` e `MENTION` têm F1 = 0,000 em **todos** os 5
repeats de validação cruzada — o modelo nunca prevê essas classes. Isso é
grave justamente na fronteira que decide a prevalência (§9.3).

O modelo C venceu em todos os critérios de desempenho, mas **não foi o
modelo implantado** na classificação da população inteira: o custo
computacional medido (17–19 documentos/segundo em CPU, sem GPU
disponível) projetava ~27–30 horas para os 1.877.981 conteúdos, inviável
no escopo desta prova de conceito de uma semana. O modelo implantado foi
**B (TF-IDF + SVM Linear)**, apesar do desempenho fraco documentado, com
o resultado explicitamente rotulado como preliminar em todo artefato
gerado ([[Decision Log#D-023]]).

**Resultado da classificação da população inteira pelo modelo B**
(`results/_arquivo/EXP-012_population_summary.json`):

| Classe prevista | n | % |
|---|---|---|
| `NONE` | 1.815.753 | 96,686 |
| `PRIMARY` | 58.066 | 3,092 |
| `MENTION` | 3.154 | 0,168 |
| `SECONDARY` | 1.008 | 0,054 |

`SECURITY` previsto (`PRIMARY`+`SECONDARY`): **30.281 (1,612%)**. Este
número é uma **contagem de previsões de um classificador com desempenho
fraco medido e documentado**, não uma estimativa de prevalência — é
exatamente a categoria de número que o Desenho C (§9.1) foi desenhado
para nunca reportar como resposta. `SECONDARY` está quase ausente na
saída em escala (0,054%), consistente com o achado de F1=0 na validação
cruzada: o modelo implantado essencialmente não reconhece essa classe.

**Por que este resultado é reportado aqui mesmo assim.** Ele demonstra
que o pipeline de ponta a ponta (congelamento de golden set → treino →
validação cruzada agrupada → seleção sob restrição de custo →
classificação em escala) é executável neste dataset e neste ambiente de
computação — informação de engenharia relevante para dimensionar E-7/E-8
— sem que isso implique qualquer afirmação sobre a prevalência real.

---

## 12. Validade e ameaças

- **Viés de seleção do representante.** A escolha de qual ocorrência
  representa um conteúdo duplicado (`dedup_primary = 1`) não é aleatória
  — prefere arquivos em caminhos como `.claude/skills/`, possivelmente
  favorecendo skills mais convencionais/bem formadas
  ([[Decision Log#D-001]]).
- **Duplicatas e near-duplicates.** Deduplicação por hash não captura
  pacotes replicados com variações mínimas; a premissa "1 conteúdo = 1
  observação independente" é mais fraca do que parece. Mitigação adotada:
  reportar concentração por repositório e por dono em toda estimativa;
  deduplicação semântica como análise de robustez, não como pipeline
  principal ([[Decision Log#D-017]]).
- **Erro de classificação (do classificador de triagem).** Tratado
  formalmente pelo desenho (§9.1, §9.4): sob as condições de validade,
  afeta eficiência, não viés — mas essa não é uma garantia incondicional,
  e a prova de conceito já demonstrada (§11.3) mostra um classificador
  real com desempenho fraco e uma falha sistemática precisamente na
  fronteira crítica (`SECONDARY`/`MENTION`).
- **Subjetividade da anotação e fronteira `SECONDARY`/`MENTION`.** É a
  única confusão que altera a prevalência agregada (§9.3). O piloto
  anterior era desenhado para estressar exatamente essa fronteira (3 dos
  50 casos eram reforços dirigidos a ela); a amostra nova de n=100 sob
  [[Decision Log#D-026]] é **aleatória simples**, não estratificada, e
  pode conter poucos casos nessa fronteira — risco declarado, não
  resolvido (§9.3).
- **Consenso entre LLMs como padrão-ouro para a maior parte da amostra.**
  Desde [[Decision Log#D-026]] (2026-09-03), casos em que os três modelos
  concordam **não são revisados por humano** — reverte a restrição que o
  projeto tratava como inegociável até então
  ([[Decision Log#D-019]], [[Decision Log#D-008]]). Viés sistemático
  compartilhado entre os três modelos (por exemplo, na mesma fronteira
  `SECONDARY`/`MENTION` onde [[EXP-012]] já documentou falha de um
  classificador barato) ficaria invisível. Precisa ser declarado
  explicitamente no texto final, com a fração de casos aceitos só por
  consenso reportada.
- **Idiomas.** População restrita a inglês desde [[Decision Log#D-025]]
  (2026-09-03, revisa [[Decision Log#D-012]]). Critério fixado (100%, via
  limiares de `mixed`/`und` de R-9) tem uma lacuna conhecida: não captura
  mistura de idiomas de mesma escrita latina (achado real ao construir
  [[Classification Prompt (D-026)]] — ver aviso em
  [[Decision Log#D-025]]). Detector de idioma ainda sem acurácia medida
  contra julgamento humano.
- **Elegibilidade da população / denominador.** [[Decision Log#D-022]]
  segue em aberto: o frame atual (`dedup_primary=1 AND content IS NOT
  NULL`) inclui unidades demonstravelmente não-skills (stubs, alvos de
  symlink). Enquanto essa decisão não for tomada, o denominador de QI-1
  não está fechado — e cada stub incluído deprime artificialmente
  qualquer prevalência calculada, pelo mesmo mecanismo que invalidou o
  notebook exploratório original ([[Decision Log#D-002]]).
- **Generalização.** O dataset é uma coleta única, datada (julho de
  2026), de um ecossistema muito recente e em rápida evolução (a
  especificação Agent Skills tem menos de um ano). Resultados descrevem
  essa população numa data específica, não uma propriedade estável do
  ecossistema. Desde [[Decision Log#D-025]] (2026-09-03), a restrição a
  skills em inglês reduz ainda mais o escopo de generalização: os
  resultados passam a valer para a subpopulação em inglês
  (1.571.243 de 1.877.981, **83,667%**, calculado em [[EXP-013]]), não
  para a população multilíngue completa do GitSkills.
- **Anotador único (pesquisador).** Se o desenho final permanecer com um
  único pesquisador/anotador humano — o que é o caso hoje —, isso é uma
  limitação estrutural do TCC, declarada aqui e a ser reafirmada na
  seção de ameaças à validade do texto final, não escondida atrás de
  concordância entre modelos.

**Específicas de Q2 e Q3 ([[Decision Log#D-024]]), aplicáveis apenas se e
quando o gate de §9.5 for cumprido:**

- **Qualidade do classificador de entrada propaga-se para Q2.** O
  conjunto de skills que Q2 analisa vem inteiramente de E-8, que por sua
  vez vem do classificador validado em E-7. Um classificador com recall
  baixo para alguma classe ou idioma produz uma taxonomia enviesada por
  construção — a prova de conceito de EXP-012 (§11.3), com F1 = 0,000
  documentado para `SECONDARY`, é um exemplo concreto do que esse risco
  parece na prática, e é exatamente o que o gate de §9.5 existe para
  impedir de entrar em Q2 sem escrutínio.
- **Subjetividade da codificação qualitativa e deriva do codebook.**
  Open coding é interpretativo por natureza; refinar categorias depois de
  ver o resultado final é racionalização, não refinamento — mitigado por
  exigir que mudanças de codebook sejam datadas e ocorram só entre
  iterações declaradas ([[QI-2 Methodology]] §4).
- **Escolha de referencial externo em Q3.** Nenhum framework único cobre
  o objeto (sinal preliminar: duas skills de recuperação de ransomware e
  monitoramento ICS/OT sem correspondência no OWASP Top 10, `n=48`,
  [[EXP-002]]). A escolha de quais referenciais usar é uma decisão
  justificada, não exaustiva, e molda o que pode aparecer como lacuna.
- **Denominador de aplicabilidade em Q3.** Determina o próprio resultado
  de cobertura e depende de uma decisão humana ainda pendente
  ([[Decision Log#D-009]]). Sem essa decisão, nenhum número de cobertura
  de Q3 é calculável, pelo mesmo motivo que [[Decision Log#D-022]]
  bloqueia qualquer prevalência pontual de Q1.
- **Ausência não é evidência de ausência.** Risco específico de Q3:
  interpretar zero cobertura observada de uma preocupação como prova de
  que o ecossistema não a trata, quando pode ser efeito de terminologia
  diferente, do método de classificação, de inaplicabilidade, ou de
  conteúdo em artefatos empacotados não examinados (§9.7).
- **Dependência entre observações, herdada de Q1.** As mesmas
  concentrações por repositório e por dono que ameaçam a prevalência de
  QI-1 ameaçam qualquer distribuição de preocupações em Q2 — um pacote
  replicado por poucos donos pode dominar a frequência de um `concern`
  sem refletir o que a comunidade mais ampla pratica.

---

## 13. Contribuições esperadas

**Empírica.** Uma estimativa de prevalência defensável e reproduzível de
skills de segurança num ecossistema onde hoje só existem contagens de
palavra-chave — com o contraste entre método ingênuo (52,93%/4,09%) e
método validado servindo, por si só, como evidência do tamanho do erro
que a abordagem ingênua comete.

**Metodológica.** Um desenho de amostragem estratificada com
classificador de triagem (Desenho C) aplicado a um problema de
prevalência com classe minoritária, incluindo um achado de processo já
obtido durante o próprio desenvolvimento do instrumento: a auditoria
adversarial do formulário de anotação revelou que a primeira versão
expunha o sinal de triagem ao anotador antes do julgamento humano — um
viés que ficaria correlacionado com a probabilidade de seleção, a única
falha que o desenho admite ser capaz de destruir sua própria validade. A
correção (cegamento, regra R-11, [[Decision Log#D-021]]) e o raciocínio
que a motivou são, em si, um resultado metodológico reaproveitável por
outros trabalhos de MSR que combinem classificador de triagem com
anotação humana.

**Para segurança de agentes e desenvolvimento assistido por IA.** Uma
caracterização empírica inicial de um tipo de artefato (instrução em
linguagem natural, selecionada probabilisticamente, sem registro nem
assinatura) que a literatura de segurança de sistemas baseados em LLM
ainda trata majoritariamente de forma qualitativa.

**Condicional ao gate de §9.5 — Q2 e Q3.** Se o classificador de QI-1 for
validado com desempenho satisfatório dentro do prazo deste trabalho, o
projeto pode ainda contribuir com uma taxonomia emergente e validada de
preocupações de segurança específica do ecossistema de Agent Skills (Q2)
e uma primeira comparação sistemática dessa taxonomia contra referenciais
reconhecidos, com denominador de aplicabilidade explícito (Q3) — em vez
das leituras qualitativas ad hoc que hoje predominam sobre "o que agentes
de IA fazem em matéria de segurança". Esta é uma contribuição **potencial
e condicional**, não garantida: se o gate não for cumprido a tempo, ela
permanece como trabalho futuro (§14, §15).

---

## 14. Escopo e não escopo

**O trabalho pretende responder:**

- A prevalência de Security Skill (`PRIMARY`+`SECONDARY`) na população
  pública do GitSkills, com intervalo de confiança de 95%.
- Essa prevalência desagregada em `PRIMARY` e `SECONDARY` separadamente.
- A mesma prevalência por conteúdo distinto (unidade primária) e por
  ocorrência (medida de difusão).
- A taxa de casos `AMBIGUOUS`, com seus limites inferior/superior.
- O desempenho do classificador de triagem por classe e por idioma.
- A robustez dessa estimativa sob denominadores e definições alternativas
  (E-10).

**O trabalho pretende responder, condicionalmente a um gate metodológico
([[Decision Log#D-024]], §9.5) — não garantido, mas planejado:**

- Quais tipos de preocupação, prática ou tema de segurança aparecem nas
  skills identificadas como Security Skill pelo classificador validado de
  QI-1, por meio de taxonomia emergente construída a partir dos dados
  (Q2, §9.6).
- Como essa taxonomia se compara a referenciais de segurança reconhecidos
  (ex.: OWASP), discutindo possíveis lacunas de **cobertura ou
  representação** — nunca "ausência = vulnerabilidade" (Q3, §9.7).

Estes dois itens só entram na entrega final se o classificador de QI-1
for validado com desempenho satisfatório a tempo; caso contrário, ficam
registrados como trabalho futuro (§15).

**O trabalho não pretende, e não poderá, concluir a partir destes
dados — independentemente do gate acima:**

- **Prevalência sobre a população multilíngue completa do GitSkills.**
  Desde [[Decision Log#D-025]] (2026-09-03, decisão do orientador), a
  população-alvo é restrita a skills em **inglês**. Skills em outros
  idiomas (~14,21% da população medida, [[EXP-003]]) ficam fora do
  escopo da estimativa — o trabalho caracteriza a prevalência entre
  skills em inglês, não no ecossistema multilíngue completo.
- **Causalidade.** Nenhuma hipótese candidata registrada em
  [[02 - Hypotheses]] é causal por natureza testável neste desenho; onde
  direção temporal seria necessária (ex.: divergência entre cópias),
  o subconjunto com histórico disponível é enviesado (MNAR) para locais
  padrão do formato, o que impede afirmações de causalidade ou de ataque
  de supply chain.
- **Que a ausência de uma categoria em Q2/Q3 seja, por si só, evidência
  de vulnerabilidade** — a linguagem exigida é de cobertura limitada ou
  não observada, nunca de ausência comprovada (§9.7).
- **A segurança da própria skill como artefato** (permissões declaradas
  em `allowed-tools`, scripts empacotados, superfície de execução) — eixo
  ortogonal à classificação de propósito usada aqui
  ([[Decision Log#D-007]]), correspondente às questões propostas QP-1/
  QP-2, não adotadas neste TCC.
- **Generalização para além do GitSkills / julho de 2026** — o
  ecossistema de Agent Skills é novo e muda rapidamente; a estimativa
  descreve uma população coletada numa data específica.
- **Qualquer prevalência pontual antes de E-9 estar concluída.** Os
  números de §11 são exploratórios ou de prova de conceito e não devem
  ser citados como resultado, inclusive fora deste documento.

---

## 15. Próximas etapas

**Concluído** (script versionado + saída em `results/` + `EXP-XXX`):
E-0 (auditoria estrutural), E-1 (Codebook v2.3), E-2b (candidate retrieval
inglês), E-3 (distribuição de idiomas), E-3b (validação de concordância
entre detectores).

**Substituído em 2026-09-03** ([[Decision Log#D-025]],
[[Decision Log#D-026]]): o piloto humano cego de n=50 ([[EXP-005]]) deixou
de ser a próxima etapa. Permanece gerado e válido como artefato histórico,
mas não é mais executado como parte do caminho crítico.

**E-5/E-6, progresso real (2026-09-03):**

1. ✅ amostra de n=100 gerada — [[EXP-013]], com o filtro de "100% inglês"
   corrigido na prática (a primeira operacionalização tinha uma lacuna
   real, ver [[Decision Log#D-025]]);
2. ✅ prompt reformulado para invocação via **CLI de cada modelo com
   acesso ao diretório** (decisão do pesquisador — não API programática) —
   [[Classification Prompt (D-026)]];
3. ✅ script de agregação/discordância escrito e testado com dados
   sintéticos — `scripts/aggregate_llm_classifications.py`;
4. ⬜ **validar o prompt** antes de rodar em escala — ainda não feito;
5. ⬜ rodar as três CLIs (GPT-5.6 Sol, Claude Opus, Gemini 3.1 Pro) contra
   `results/EXP-013_llm_cases/`, cada uma de forma totalmente
   independente;
6. ⬜ agregar as três saídas e adjudicar humanamente os casos discordantes
   ([[Guia do Anotador Humano (D-026)]]).

**Bloqueado por decisão pendente:** apenas [[Decision Log#D-022]]
(elegibilidade da população / denominador) continua recomendável resolver
antes ou durante esta etapa, pelo mesmo motivo de antes — nada relativo a
D-025/D-026 bloqueia mais a execução.

**Planejado, na ordem do caminho crítico:** E-5/E-6 (acima) → E-4
(retrieval reordenado, escolhido por recall) → E-7 (classificador
validado por classe — **também o gate de [[Decision Log#D-024]]**) → E-8
(classificação da população, `N_h` e conjunto `PRIMARY`/`SECONDARY`) →
E-9 (estimativa de prevalência com IC — **responde a QI-1**, agora sobre
a população restrita a inglês) → E-10 (robustez) → E-11 (consolidação;
revisão de literatura pode correr em paralelo desde já).

**Planejado, condicional ao gate ([[Decision Log#D-024]]) — não iniciado,
sem data prevista:**

- **Q2** (§9.6): a partir do conjunto `PRIMARY`/`SECONDARY` de E-8 —
  amostra exploratória → open coding humano → codebook preliminar →
  iteração até estabilizar → validação (gold set próprio, concordância) →
  classificação em escala. Nenhuma etapa executada; nenhum código
  `EXP-XXX` reservado ainda (ver nota de numeração, §10).
- **Q3** (§9.7): a partir da taxonomia estabilizada de Q2 — escolha
  justificada de referenciais externos → definição do escopo de
  aplicabilidade (depende de [[Decision Log#D-009]]) → crosswalk →
  níveis de cobertura → discussão de lacunas. Bloqueado por Q2 e,
  transitivamente, pelo mesmo gate.

Se o gate não for cumprido dentro do prazo deste trabalho, os dois itens
acima permanecem como trabalho futuro no capítulo de conclusão, não como
capítulos de resultado (§16).

**Decisões metodológicas que permanecem abertas** e precisam de
aprovação humana explícita antes de fechar as etapas correspondentes:

- [[Decision Log#D-022]] — critério de elegibilidade da população
  (denominador de QI-1).
- [[Decision Log#D-009]] — escopo de aplicabilidade da QI-3 (não afeta o
  caminho crítico de QI-1, mas bloqueia o cálculo de qualquer cobertura
  em Q3).
- Teto de taxa de `AMBIGUOUS` acima do qual a prevalência deixa de ser
  reportável como ponto ([[QI-1 Methodology]] §4) — proposto, não
  formalmente aprovado.
- [[Decision Log#D-015]] — desenho multi-estágio como alternativa se a
  classificação da população inteira se mostrar inviável; a decisão fica
  pendente até E-5 fornecer dados reais de custo por item.
- **[[Decision Log#D-024]] — critério numérico de "validação
  satisfatória" do classificador de QI-1** (F1 mínimo por classe, recall
  mínimo para `SECONDARY`, desempenho mínimo por idioma). Sem essa
  decisão, o gate de Q2/Q3 não pode ser avaliado de forma objetiva — fica
  como julgamento humano caso a caso até ser fixada.
Resolvidas em 2026-09-03, não mais abertas: [[Decision Log#D-025]]
(critério operacional de "skill em inglês" — 100%, via limiares de
`mixed`/`und` de R-9) e [[Decision Log#D-026]] (regra de desempate —
qualquer discordância entre os três LLMs, em qualquer dimensão, leva o
caso à adjudicação humana; cegamento entre modelos confirmado como regra
explícita).

---

## 16. Estrutura provável da monografia

| Capítulo | Função |
|---|---|
| 1. Introdução | Contexto (§2), problema (§3), objetivos (§5), questões (§6), justificativa (§4) |
| 2. Referencial teórico | Agent Skills como artefato; segurança em sistemas baseados em LLM; desenvolvimento assistido por IA; métodos de mineração de repositórios (MSR); inferência com rótulos substitutos (design-based supervised learning) |
| 3. Dataset e unidade de análise | GitSkills, tabelas, população, unidade de análise, problemas conhecidos (§8) |
| 4. Metodologia | Definição operacional (§7), Desenho C (§9), estimador, papel e limite do classificador, tratamento de `AMBIGUOUS` |
| 5. Pipeline experimental | Reconstrução das etapas concluídas e planejadas, em ordem metodológica (§10) |
| 6. Resultados — QI-1 | Estimativa final de QI-1 com IC, desagregações — **capítulo a escrever depois de E-9**; até lá, resultados preliminares ficam claramente marcados como tal (§11) |
| 7. Resultados — Q2/Q3 (condicional) | Taxonomia emergente e comparação com referenciais externos — **capítulo incluído somente se o gate de [[Decision Log#D-024]] (§9.5) for cumprido dentro do prazo**; caso contrário, este capítulo não existe e Q2/Q3 aparecem apenas como trabalho futuro no capítulo 9 |
| 8. Ameaças à validade e discussão | §12 (inclui bullets específicos de Q2/Q3, condicionais ao capítulo 7 existir), comparação com a literatura disponível sobre segurança de artefatos agênticos |
| 9. Conclusão | Contribuições (§13, incluindo a contribuição condicional de Q2/Q3), limitações, escopo e não escopo (§14), trabalho futuro (QP-1..5, e QI-2/QI-3 caso o gate não tenha sido cumprido a tempo) |

---

## 17. Roteiro para apresentar a proposta ao orientador

Versão condensada, sequência lógica para apresentação oral:

1. **Contexto** — Agent Skills é um formato novo (out. 2025) de
   instrução em linguagem natural para agentes de IA, distribuído sem
   registro nem assinatura; o GitSkills é a primeira coleta pública em
   larga escala desse ecossistema (~1,9 milhão de skills distintas).
2. **Problema** — não se sabe, com rigor, que fração desse ecossistema
   de fato trata de segurança como propósito ou capacidade substancial;
   medidas ingênuas de palavra-chave (52,93%) divergem por um fator de
   13× de medidas de propósito declarado (4,09%), mostrando que a
   pergunta exige um instrumento de classificação, não busca textual.
3. **Pergunta** — QI-1: qual a prevalência de Security Skills
   (`PRIMARY`+`SECONDARY`) na população pública de Agent Skills?
4. **Dados** — GitSkills, 1.877.981 conteúdos distintos no total; população
   restrita a **inglês** desde 2026-09-03 (D-025), denominador ainda não
   recomputado, e D-022 (elegibilidade) segue em aberto.
5. **Método** — Desenho C: classificador de triagem forma estratos,
   amostra probabilística dentro de cada estrato é anotada, e a
   prevalência é estimada por ponderação estratificada sobre a
   anotação — nunca sobre a previsão do modelo. O padrão-ouro que alimenta
   essa anotação tem um desenho próprio desde 2026-09-03 (item 6).
6. **Estágio atual** — instrumento de classificação definido (Codebook
   v2.3); estrutura do dataset caracterizada; o piloto humano cego de 50
   casos foi substituído pelo desenho de D-026 — amostra nova de n=100 em
   inglês, classificada por três LLMs (GPT-5.6 Sol, Claude Opus, Gemini
   3.1 Pro) com adjudicação humana só na discordância; ainda não
   executado. Uma prova de conceito de engenharia do pipeline completo já
   roda ponta a ponta sob o desenho anterior, fora do caminho crítico.
7. **Próximos passos** — validar o prompt de classificação contra casos
   conhecidos; sortear e classificar a amostra de n=100 (E-5/E-6);
   resolver a questão pendente de elegibilidade da
   população (D-022); depois, validar o classificador definitivo,
   classificar a população e produzir a estimativa (E-7 a E-9).
8. **Sequência planejada depois de QI-1** — decisão registrada em
   2026-08-27 ([[Decision Log#D-024]]): se e quando o classificador de
   QI-1 for validado com desempenho satisfatório em E-7 (critério
   numérico ainda a definir com o orientador), o projeto segue para QI-2
   (taxonomia emergente de preocupações de segurança, construída
   bottom-up sobre as skills identificadas, nunca a partir de OWASP/MITRE)
   e, só depois de essa taxonomia estabilizar, para QI-3 (comparação com
   referenciais externos, discutindo lacunas de cobertura sem tratar
   ausência como evidência de vulnerabilidade). Se o gate não for
   cumprido a tempo, esses dois passos ficam como trabalho futuro, não
   como capítulo de resultado.
9. **Contribuição esperada** — primeira estimativa defensável de
   prevalência de segurança neste ecossistema, mais um desenho
   metodológico (classificador de triagem + amostragem estratificada)
   reaproveitável em problemas MSR semelhantes; condicionalmente, uma
   taxonomia empírica de preocupações de segurança e uma primeira
   comparação sistemática com referenciais reconhecidos.

---

## 18. Autorrevisão crítica

Revisão deste documento, procurando especificamente pelos cinco pontos
solicitados.

**Inconsistências metodológicas encontradas (e como ficam registradas
aqui, sem "correção silenciosa"):**

- O denominador central da pesquisa (N = 1.877.981) é usado em todo o
  documento como se fosse fixo, mas [[Decision Log#D-022]] está
  formalmente em aberto e pode alterá-lo. Isso não é um erro deste
  roteiro — é o estado real do projeto — mas significa que **todo número
  de prevalência futuro herdará essa indefinição** até D-022 ser resolvida.
  Recomenda-se resolvê-la antes de fechar E-6, não depois.
- [[QI-1 Methodology]] §4 especifica um estimador mais complexo (razão
  entre dois estimadores estratificados, com variância por bootstrap) do
  que a versão simplificada de proporção estratificada descrita em
  §9.1/§9.4 deste roteiro. As duas não se contradizem — a segunda é a
  forma completa que trata `AMBIGUOUS` corretamente — mas a nota de
  metodologia (E-9) precisa citar explicitamente qual das duas formas
  será implementada, para não ambiguar entre "prevalência simples" e
  "razão de prevalências" no texto final do TCC.

**Questões de pesquisa não respondidas pelo método atual:** nenhuma. Os
objetivos específicos 1–7 (§5) cobrem inteiramente QI-1, subordinados ao
caminho crítico imediato (§6). Desde [[Decision Log#D-024]], os objetivos
8–9 cobrem QI-2 e QI-3 respectivamente, ambos marcados como condicionais
ao gate — nenhuma das três questões fica sem objetivo, e nenhum objetivo
fica sem questão que o justifique.

**Objetivos que não correspondem às questões de pesquisa:** nenhum
encontrado — os sete primeiros objetivos específicos (§5) mapeiam 1:1
para as etapas E-1/E-5, E-0/E-3/E-3b, E-6, E-7, E-8, E-9 e E-10, todas
subordinadas a QI-1; os objetivos 8 e 9, acrescentados por
[[Decision Log#D-024]], mapeiam 1:1 para QI-2 (§9.6) e QI-3 (§9.7)
respectivamente, e estão marcados como condicionais ao gate em todo lugar
onde aparecem — não há objetivo que prometa mais do que o desenho atual
sustenta.

**Conclusões mais fortes do que os dados permitem:** o maior risco
identificado nesta revisão não está no texto deste roteiro (que marca
explicitamente §11.3 como não-prevalência), mas é um risco **para a
escrita futura do TCC**: o número 1,612% de EXP-012 é fluente, único e
tentador de citar informalmente. Este roteiro reforça três vezes (no
aviso de §11, no corpo de §11.3 e aqui) que ele não pode aparecer no
texto final como estimativa, nem mesmo como "estimativa preliminar da
QI-1" — é resultado de engenharia sobre um classificador com F1=0,000
documentado para a classe que mais importa.

**Etapas ausentes entre anotação, classificação, validação e
inferência:** nenhuma etapa está ausente na sequência E-5/E-6→E-4→E-7→
E-8→E-9 (§10); a ordem já foi objeto de uma correção formal registrada
([[Decision Log#D-018]], reordenação de E-4). Desde 2026-09-03
([[Decision Log#D-025]], [[Decision Log#D-026]]), o ponto de atenção
mudou de natureza: não é mais só execução pendente (o piloto anterior
estava gerado, faltava anotar) — as duas decisões operacionais que
bloqueavam a amostra de n=100 (definição de "skill em inglês"; regra de
desempate entre os três LLMs) foram fixadas em 2026-09-03, ver §15. O que
falta agora é puramente execução: validar o prompt, sortear a amostra,
rodar os três modelos.

**Revisão adicional após [[Decision Log#D-024]] (execução sequencial
Q1 → validação → Q2 → Q3):**

- **Gate sem threshold numérico.** A decisão formaliza *que* existe um
  gate (§9.5), mas não *quanto* desempenho conta como satisfatório. Isso
  é reportado como decisão pendente em três lugares (§9.5, §15, Decision
  Log D-024) deliberadamente, e não resolvido aqui — inventar um número
  agora seria exatamente o erro que o gate existe para evitar. Antes de
  E-7 rodar de fato, essa lacuna precisa virar decisão do
  pesquisador/orientador, não ficar pendente indefinidamente.
- **Risco de otimismo no cronograma.** Listar Q2 e Q3 em quase todas as
  seções do documento (§5, §6, §9, §10, §12, §13, §14, §15, §16, §17)
  cria uma leitura possível de que são entregas certas. Não são — cada
  menção neste roteiro as trata como condicionais, e o capítulo 7 da
  estrutura da monografia (§16) só existe se o gate for cumprido a tempo.
  Isso precisa continuar explícito na escrita final do TCC, não só aqui.
- **Consistência do objetivo geral.** §5 mantém o objetivo geral como
  apenas QI-1, tratando Q2/Q3 como desdobramento condicional nos
  objetivos específicos 8–9, não como parte do objetivo geral em si.
  Verificado como coerente: o título (§1) e a contribuição empírica
  central (§13) continuam ancorados exclusivamente em QI-1, que é o que
  o projeto de fato garante produzir.
- **QI-2 herda um risco já observado no projeto, não hipotético.** O
  aviso de §9.5 sobre EXP-012 (F1 = 0,000 para `SECONDARY`) não é um
  cenário teórico — é o desempenho de um classificador real já treinado
  neste projeto. Isso reforça, com evidência própria do projeto, por que
  o gate não é uma formalidade.

**Revisão adicional após [[Decision Log#D-025]] e [[Decision Log#D-026]]
(reunião com o orientador, 2026-09-03):**

- **Maior reversão de princípio já registrada neste projeto.**
  [[Decision Log#D-019]] chamava a restrição contra usar consenso entre
  LLMs como ground truth de "inegociável". D-026 a reverte explicitamente,
  por instrução do orientador. Isso está documentado com o mesmo nível de
  destaque em três lugares (Decision Log, [[03 - Methodology]], §9.3
  deste roteiro) — mas é o ponto do documento que mais precisa de atenção
  na banca: a defesa deste TCC deve conseguir explicar **por que** essa
  reversão foi aceita, não só que foi aceita.
- **Motivação da reunião não registrada.** Nem [[Decision Log#D-025]] nem
  [[Decision Log#D-026]] documentam a razão pela qual o orientador propôs
  essas mudanças (viabilidade de prazo, redução de escopo, preferência
  metodológica). Isso é uma lacuna factual, não uma omissão deliberada —
  registrar assim que for comunicada evita que o texto final do TCC
  precise inventar uma justificativa post-hoc.
- **Duas pendências que bloqueavam a execução foram fixadas na mesma
  reunião, 2026-09-03** — diferente do padrão anterior do projeto, em que
  decisões pendentes (D-009, D-015, D-022) não impediam a próxima etapa de
  rodar, aqui a definição operacional de "inglês" (D-025: 100%, via
  limiares de R-9) e a regra de desempate (D-026: qualquer discordância,
  em qualquer dimensão, vai a adjudicação humana; cegamento entre modelos
  explícito) eram bloqueantes e precisaram ser resolvidas antes de
  sortear a amostra — o que já aconteceu. A operacionalização de "caso
  inteiro vai a adjudicação" (em vez de campo a campo) é uma leitura
  razoável registrada em [[Decision Log#D-026]], não uma especificação
  literal da reunião — checar com o orientador se essa leitura é a
  intencionada antes de rodar.
- **Trabalho multilíngue não é desperdiçado, mas fica com um papel menor
  do que tinha.** [[EXP-003]], [[EXP-004]] e [[Multilingual Strategy]]
  representam esforço real de desenho e medição. Sob D-025 eles continuam
  válidos (como caracterização histórica e como camada de filtro
  reaproveitada), mas deixam de ser o eixo central do desenho amostral.
  Isso deve ser reconhecido explicitamente na escrita final, não tratado
  como se nunca tivesse existido.
- **Consistência de escopo verificada.** §14 lista a restrição a inglês
  como não-escopo explícito, e §8 agora reporta o denominador real
  (83,667%, [[EXP-013]]), não mais uma aproximação. Nenhuma seção deste
  roteiro afirma um número de prevalência que pressuponha a população
  multilíngue — verificado nesta revisão. O denominador em si **não é a
  prevalência de QI-1** (que ainda depende de E-9): é só o tamanho da
  população-alvo sob D-025.

---

## Ligações

`README.md` · `MEMORY.md` · [[00 - Research Overview]] ·
[[01 - Research Question]] · [[02 - Hypotheses]] · [[03 - Methodology]] ·
[[QI-1 Methodology]] · [[QI-2 Methodology]] ·
[[QI-3 Coverage Methodology]] · [[Security Taxonomy]] · [[Codebook]] ·
[[Decision Log]] (ver especialmente D-024) · [[EXP-001]] · [[EXP-002]] ·
[[EXP-003]] · [[EXP-004]] · [[EXP-005]] · [[EXP-012]] ·
`.claude/skills/project-context/SKILL.md` ·
`.claude/skills/security-analysis/SKILL.md`
