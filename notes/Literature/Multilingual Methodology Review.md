---
tipo: literatura
data: 2026-08-22
questao: QI-1
branch: Q1
status: revisao focada - primeira rodada
---

# Multilingual Methodology Review

Revisão metodológica focada: como estudos empíricos comparáveis trataram conteúdo
multilíngue, amostragem e classificação em escala. Fundamenta [[03 - Methodology|E-4]]
e [[03 - Methodology|E-5]] e o desenho de [[Decision Log#D-014]].

> [!warning] Escopo e honestidade da busca
> Revisão **focada**, não sistemática. Feita por busca web em agosto/2026, sem
> protocolo de string de busca nem screening documentado. Não substitui uma SLR.
> Só entram trabalhos cuja existência e conteúdo foram verificados na fonte —
> nenhuma referência foi inferida ou reconstruída de memória.
>
> **Lacuna reconhecida:** não localizei nesta rodada trabalho de MSR que trate
> explicitamente *validação de detecção de idioma* como questão metodológica. Isso
> pode significar ausência na literatura ou insuficiência da busca. Ver §Divergências.

---

## Trabalhos encontrados

| Trabalho | Autores | Venue | Ano | Fonte | Objeto | Relevância metodológica |
|---|---|---|---|---|---|---|
| **Using Imperfect Surrogates for Downstream Inference: Design-based Supervised Learning (DSL)** | Egami, Hinck, Stewart, Wei | NeurIPS | 2023 | [arXiv:2306.04746](https://arxiv.org/abs/2306.04746) | anotação por LLM em ciências sociais | **Máxima.** Fundamenta o Desenho C e a rejeição do Desenho B |
| **Sampling in Software Engineering Research: A Critical Review and Guidelines** | Baltes, Ralph | EMSE 27(94) | 2022 | [10.1007/s10664-021-10072-8](https://doi.org/10.1007/s10664-021-10072-8) · [arXiv:2002.07764](https://arxiv.org/abs/2002.07764) | prática amostral em ES | **Alta.** Justifica amostragem probabilística explícita |
| **From Registry to Repository: How AI Agent Skills Are Written, Adapted, and Maintained** | Gao, Lulla, Lin, Baltes, Treude, Zahedi | arXiv (preprint) | 2026 | [arXiv:2607.00911](https://arxiv.org/abs/2607.00911) | **Agent Skills** | **Máxima como trabalho relacionado.** Define a lacuna que a QI-1 ocupa |
| **Categorizing the Content of GitHub README Files** | Prana, Treude, Thung, Atapattu, Lo | EMSE 24 | 2019 | [10.1007/s10664-018-9660-3](https://doi.org/10.1007/s10664-018-9660-3) · [arXiv:1802.06997](https://arxiv.org/abs/1802.06997) | seções de README | **Alta.** Modelo de anotação manual + classificador em artefato textual de GitHub |
| **GitHub Multilingual Repositories Dataset** | GitHub (blog técnico) | — | 2026 | [github.blog](https://github.blog/ai-and-ml/llms/accelerating-researchers-and-developers-building-multilingual-ai-with-a-new-open-dataset/) | 40 M+ repos, 80 M+ classificações | **Alta** para detecção de idioma. Fonte secundária (não revisada por pares) |
| **langid.py: An Off-the-shelf Language Identification Tool** | Lui, Baldwin | ACL (demos) | 2012 | [aclanthology.org/P12-3005](https://aclanthology.org/P12-3005/) | ferramenta | Fonte primária do detector usado em [[EXP-003]] |
| **Prediction-Powered Inference** | Angelopoulos et al. | — | 2023– | família de métodos ([arXiv:2309.16598](https://arxiv.org/abs/2309.16598) e correlatos) | inferência com predições de ML | Média. Alternativa/complemento ao DSL |

---

## Estratégia linguística por trabalho

| Trabalho | Language detection | Tradução | Retrieval | Amostragem | Gold set | Métricas por idioma |
|---|---|---|---|---|---|---|
| DSL (Egami et al.) | n/a | n/a | n/a | **probabilística obrigatória** para os rótulos gold | expert labels + surrogates LLM | não aplicável |
| Baltes & Ralph | n/a | n/a | n/a | tema central: aleatória e estratificada, raras na área | n/a | n/a |
| Gao et al. (Agent Skills) | **não tratado** | não | registries + GitHub | temática de 180 skills; 444 modificações | anotação qualitativa | **não reportadas** |
| Prana et al. (README) | não é foco declarado | não | n/a | 393 repos aleatórios; 4.226 seções anotadas | anotação manual → classificador (F1 0,746) | **não reportadas** |
| GitHub Multilingual Dataset | **3 detectores** (fastText, gcld3, lingua-py), saídas **mantidas separadas**; corte 0,5 | não | n/a | amostra de 150 caracteres por repo | não há | reconhece variação de calibração por idioma |
| Lui & Baldwin | a própria ferramenta | n/a | n/a | n/a | benchmarks de LID | n/a |

---

## Padrões recorrentes

1. **Anotação humana como âncora, classificador como escala.** Prana et al. e Gao et
   al. seguem o mesmo esqueleto: anotar amostra à mão, depois automatizar. É o
   consenso de fato para artefato textual de GitHub.
2. **Amostragem probabilística é a exceção, não a regra** (Baltes & Ralph): amostra
   aleatória é rara e estratégias sofisticadas são muito raras em ES. Adotar o
   Desenho C já coloca este estudo acima da prática típica da área.
3. **Detecção de idioma é reconhecidamente difícil em repositórios.** O GitHub
   registra explicitamente: texto curto, badges, templates, comandos, snippets e
   conteúdo misto; calibração varia para idiomas de menor recurso.
4. **Manter múltiplos detectores em vez de colapsar.** Prática do dataset do GitHub,
   e exatamente o que [[EXP-004]] confirmou empiricamente ser necessário aqui.

## Divergências e lacunas

- **Não há consenso sobre tratamento de idioma em MSR.** Prana et al. e Gao et al.
  simplesmente **não reportam** estratégia linguística. Isso não é descuido isolado:
  sugere que a prática dominante é ignorar idioma, o que torna a decisão
  [[Decision Log#D-012|D-012]] uma posição mais rigorosa que a norma da área — e
  também significa que **não há um método consagrado a copiar**.
- **Validação de detector de idioma não foi encontrada** como prática reportada em
  MSR. O GitHub reconhece o problema mas não publica acurácia validada.
- **Tradução antes de classificar** não apareceu documentada em nenhum dos trabalhos
  examinados — nem a favor nem contra. Não há evidência da literatura para apoiar ou
  rejeitar a estratégia B.

## Aplicação ao nosso estudo

**Transferível:**

- DSL/PPI → o núcleo estatístico do Desenho C. O achado de Egami et al. de que
  *"direct use of surrogate labels leads to substantial bias and invalid confidence
  intervals, even with high surrogate accuracy of 80–90%"* é a justificativa
  publicada mais forte para **não** reportar a contagem do classificador como
  prevalência.
- Múltiplos detectores com saídas preservadas (GitHub) → já adotado em [[EXP-004]].
- Anotar → classificar → validar (Prana et al.) → esqueleto de E-5 a E-7.

**Não transferível:**

- Escala. Prana et al. anotaram 4.226 seções de 393 repos; Gao et al. mineraram
  ~41 mil skills. Nossa população é **1.877.981 conteúdos** — duas ordens de
  grandeza acima. Anotação exaustiva está fora de questão em qualquer cenário.
- A ausência de tratamento linguístico nos trabalhos comparáveis **não é** licença
  para repeti-la; é a lacuna que este estudo pode ocupar.

**Posicionamento em relação a Gao et al. (2026).** É o trabalho relacionado mais
próximo — mesma comunidade, mesmo artefato, mesmo ano. Diferenças que sustentam a
contribuição da QI-1:

| | Gao et al. 2026 | Este estudo |
|---|---|---|
| População | 18.463 (skills.sh) + 23.199 (GitHub) | 1.877.981 conteúdos distintos |
| Foco | autoria, reuso, manutenção | **segurança** |
| Classificação | LLM → SWEBOK KAs | LLM como **triagem**, desfecho humano |
| Estimativa | contagens descritivas | **prevalência com IC** |
| Idioma | não tratado | população multilíngue explícita |
| Validação | concordância não reportada | gold set + métricas por classe e idioma |

> Ler o texto completo de Gao et al. antes de E-5. Pode haver sobreposição de
> escopo a declarar, e a categorização SWEBOK pode informar o codebook.

## Recomendação — estratégia multilíngue para a QI-1

Comparação das cinco alternativas do escopo:

| | Estratégia | Veredito |
|---|---|---|
| **A** | Classificação direta no idioma original | ✅ **adotar como principal** |
| **B** | Traduzir para inglês e então classificar | ❌ rejeitar como padrão |
| **C** | Híbrida (direta + tradução pontual) | ✅ **adotar como exceção** |
| **D** | Retrieval lexical multilíngue | 🟡 secundária |
| **E** | Retrieval semântico multilíngue | 🟡 avaliar só se D falhar |

**A — direta.** LLMs modernos são multilíngues por construção; classificar no
original evita introduzir um erro de tradução que depois não se separa do erro do
classificador. Custo igual ao da classificação em inglês. **Risco:** desempenho pode
cair em idiomas de menor recurso — daí a exigência de métricas por idioma.

**B — tradução prévia.** Rejeitada como padrão. Duplica custo (traduzir 1,88 M +
classificar), introduz perda semântica justamente em terminologia técnica de
segurança, e **não há evidência na literatura examinada** que a sustente. Contraria
[[Decision Log#D-013]].

**C — híbrida.** Tradução apenas como apoio à **anotação humana**, quando o anotador
não domina o idioma, com o original preservado e `used_translation` marcado.

**D — retrieval lexical multilíngue.** Secundária porque, no Desenho C, o retrieval
**não é o gargalo**: ele estratifica, e estratificação imperfeita custa precisão, não
validade. Além disso o retrieval inglês já cobre 78,69% ([[EXP-002]]) — há pouco a
ganhar em cobertura e muito a perder em complexidade.

**E — retrieval semântico.** Só se D demonstrar recall ruim em algum idioma **medido
contra o gold set**. Custo de embeddings sobre 1,88 M é relevante e a
reprodutibilidade depende de fixar versão de modelo.

## Impacto em E-4 — candidate retrieval multilíngue

O peso de E-4 **cai**. Justificativa: sob o Desenho C, o retrieval define estratos,
não a população elegível — nenhuma skill é descartada por não ser recuperada.

Portanto E-4 muda de "construir um léxico multilíngue completo" para:

1. Manter o retrieval inglês existente como **um sinal entre outros**, não como filtro.
2. Acrescentar sinais que **não dependem de léxico**: `domain:`/`category:` no front
   matter ([[EXP-002]]), presença de script, `has_scripts`.
3. Testar a hipótese registrada: `name`/`description` em inglês dá recall melhor em
   skills não inglesas (4,17% divergem entre front matter e corpo, [[EXP-003]]).
4. Medir **recall por idioma** contra o gold set assim que ele existir — antes disso
   não há critério para escolher entre D e E.

**Consequência de ordem:** E-4 deixa de ser pré-requisito rígido de E-5. O piloto de
anotação pode rodar sobre amostra estratificada por idioma **sem** léxico multilíngue
pronto. Ver §Ordem proposta.

## Impacto em E-5 — piloto de anotação

- Estratificar o piloto **por grupo linguístico**, não só pela fronteira
  `SECONDARY`/`MENTION`. Precisa haver caso não inglês desde o piloto.
- Incluir deliberadamente: casos `mixed`, casos de cauda, casos com muito código.
- Registrar `used_translation` e o tempo por item **por idioma** — se anotar em
  chinês custar três vezes mais, isso muda o dimensionamento do gold set.
- Aproveitar o piloto para produzir a **primeira medida de acurácia real de
  detecção de idioma** com julgamento humano, fechando a lacuna de [[EXP-004]].
- Seguir Prana et al. no esqueleto: anotar → medir concordância → classificador.

## Impacto no Desenho C — estratos linguísticos

[[EXP-004]] **v2** (a v1 estava errada — ver a própria nota) mede concordância entre
detectores por grupo real:

```text
L1  en                       ~85%     concordância 0,967
L2  zh                        ~6%     1,000
L3  ja + ko                   ~3%     1,000
L4  de + es + pt + fr + it    ~4%     1,000
L5  cauda + und           ~1,6-2,4%   0,967  -> não subdividir
```

**L5 não subdivide por falta de suporte amostral** (~2% em mais de dez idiomas), não
por falha de detecção. `mixed` **não** é grupo: é atributo transversal — tratá-lo
como grupo mandava todo o CJK para L5 e corromperia os pesos `N_h/N`. `la` entra em
L5 como artefato, nunca como idioma.

Estratificação final = **classe prevista × {L1…L5}**, com oversampling de L2–L5
corrigido pelos pesos `N_h/N`.

## Ordem proposta — revisão

A literatura sugere uma ordem melhor que a do plano atual:

> **Antecipar E-5 (piloto) em relação a E-4 (retrieval multilíngue).**

Motivo: sob o Desenho C o retrieval não determina elegibilidade, e o critério para
escolher entre retrieval lexical e semântico é **recall medido contra o gold set** —
que não existe antes do piloto. Construir o léxico primeiro seria decidir sem o dado
que decide.

Ordem revisada: `E-5 (piloto) → E-6 (gold set) → E-4 (retrieval, com recall medido)
→ E-7 …`

Requer aprovação — ver [[Decision Log]].


---

## Evidência para o desenho do gold set (E-6)

Segunda rodada de busca, focada em tamanho de gold set, dupla anotação, adjudicação
e confiabilidade. Mesma ressalva de escopo: revisão focada, não sistemática.

| Decisão | Trabalho | O que o trabalho fez (números) | Fonte | Verificação |
|---|---|---|---|---|
| **Anotador único no corpus + 2º passe cego só no estrato positivo** | Herzig, Just, Zeller — **ICSE 2013** | 7.401 issues. 1º autor anotou todos sozinho; 2º autor re-anotou **cego** apenas os 3.093 candidatos positivos; 340 conflitos (94% concordância bruta) resolvidos em par. 10.884 inspeções, ~4 min/item, **725 horas**. Declaram os resultados como **limite inferior** porque não verificaram falsos negativos do 1º passe | [10.1109/ICSE.2013.6606585](https://doi.org/10.1109/ICSE.2013.6606585) | texto completo |
| **Proporção de dupla anotação quando parcial** | Díaz, Pérez, Gallardo, González-Prieto — **JSS 2022** | Mapeamento de 49 estudos de ES. Só **8 declaram** o corpus de IRR; valores **25%, 20%, ~30%, 10%, ~10%, 26%, 10%, 20%** → faixa **10–30%, moda 20%**. Só **5 de 49** declaram limiar mínimo. **33 de 49** dizem "IRR" quando medem IRA | [10.1016/j.jss.2022.111520](https://doi.org/10.1016/j.jss.2022.111520) | preprint arXiv |
| **Regra de consenso + categoria "sem consenso" + anti-ancoragem** | Herbold et al. — **EMSE** (aceito) | 3.498 commits / 289.904 linhas, **4 anotadores por linha**, consenso = **≥3/4**, senão "sem consenso" (**14,3%** das linhas). Fleiss' κ = 0,67. Modelo binomial pré-registrado para separar ambiguidade real de ruído. Pré-rótulos heurísticos exibidos **com instrução explícita de ceticismo**, e testaram se funcionou | [arXiv:2011.06244](https://arxiv.org/abs/2011.06244) | texto completo |
| **Adjudicação por discordância humano-máquina** | Yu, Theisen, Williams, Menzies (HARMLESS) — **TSE 2021** | Firefox: 28.750 arquivos, **271 vulneráveis (0,94%)**. Hipótese: erros humanos concentram-se onde humano e máquina discordam. Dupla checagem de **50% dos inspecionados recuperou 96%** das vulnerabilidades perdidas | [arXiv:1803.06545](https://arxiv.org/abs/1803.06545) | texto completo |
| **LLM como apoio, nunca ground truth** | Ahmed, Devanbu, Treude, Pradel — **MSR 2025** (Distinguished Paper) | 6 LLMs × 10 tarefas. Krippendorff's α humano-humano vs humano-máquina: Goals 0,83 vs 0,77; **Static Analysis Warnings 0,80 vs 0,15**. Regra proposta: medir **concordância modelo-modelo**; se >0,5, substituir **um** rating humano por item. Conclusão: "não podemos substituir todos os humanos" | [10.1109/MSR66628.2025.00086](https://doi.org/10.1109/MSR66628.2025.00086) | texto completo |
| **Estratificação com FPC em MSR** | Gorostidi, Ait, Cabot, Cánovas Izquierdo — **ESEM 2024** | Estimador = média ponderada dos estratos; variância **com correção de população finita** `(1 − n_h/N_h)`. Alocação **proporcional**. Categórica com p=0,5, e=0,05: **n = 385**. Recomendam ≤4–6 variáveis de estratificação. Amostragem estratificada aparece em **apenas 3,2%** dos trabalhos de MSR | [10.1145/3674805.3690747](https://doi.org/10.1145/3674805.3690747) | texto completo |
| **Dimensionar para prevalência rara** | McGrath & Burke — *The American Statistician* **2024** | Margem de erro **relativa** `R = ε/p`, recomendada em [0,1; 0,5]. Com R=0,4 e 95%: **p=10⁻¹ → n≈220**; **p=10⁻² → n≈2.400–3.300**; **p=10⁻³ → n≈24.000–34.000** | [10.1080/00031305.2024.2350445](https://doi.org/10.1080/00031305.2024.2350445) | texto completo |
| **Anotação multilíngue por falante nativo** | Katzy et al. — arXiv 2605.05902 (**preprint**) | 12.500 comentários × 5 línguas, 6 autores, 500 pessoa-horas. **Ao menos um autor falante nativo por língua**; critérios de codificação deliberadamente *language-agnostic*. Escala ordinal → **κ com pesos quadráticos** | [arXiv:2605.05902](https://arxiv.org/abs/2605.05902) | completo, **não revisado por pares** |
| **Gold sets em LLM4MSR são pequenos** | De Martino et al. — arXiv 2508.02233 (**preprint**) | Rapid review de 31 artigos + survey com 22 respondentes. Conjuntos de validação de **"algumas dezenas"** (31 incidentes; 50 model cards) a 10 projetos | [arXiv:2508.02233](https://arxiv.org/abs/2508.02233) | completo, **não revisado por pares** |

### O que isso muda no desenho de E-6

1. **O tamanho não pode sair de conveniência.** Se a prevalência for da ordem de 1%,
   McGrath & Burke implicam **n ≈ 2.400–3.300** para amostra aleatória simples com
   margem relativa de 40%. Esse número é o argumento quantitativo a favor do
   Desenho C — e precisa ser apresentado como cálculo, não como justificativa
   post-hoc.
2. **Dupla anotação parcial de ~20%** é a prática defensável em ES quando total é
   inviável (Díaz et al.). Definida **antes** de ver resultados
   ([[Decision Log#D-019]]).
3. **Anotador único é aceito em MSR** — mas nenhum trabalho encontrado o aceita *sem*
   segundo passe. Herzig et al. mostram a forma honesta: 2º passe cego no estrato
   positivo + declarar o resultado como **limite inferior**.
4. **`AMBIGUOUS` tem precedente forte.** Herbold et al. modelam "sem consenso" como
   categoria de primeira classe (14,3% dos itens) — valida a escolha do [[Codebook]]
   como decisão metodológica, não como falha.
5. **Adjudicação dirigida por discordância** (HARMLESS) é mais eficiente que 20%
   aleatórios: mandar para 2ª anotação onde LLM e humano divergem.
6. **Critério pré-registrável para confiar na triagem** (Ahmed et al.): medir
   concordância modelo-modelo antes. O caso Static-Analysis (α 0,80 → 0,15) mostra
   que o fracasso é **específico da tarefa** e precisa ser medido, não presumido.
7. **Gorostidi et al. dá respaldo peer-reviewed em venue de ES** ao estimador
   `Σ_h (N_h/N)·p̂_h` **com FPC** — exatamente o de [[Decision Log#D-014]].
   **Divergência:** eles prescrevem alocação **proporcional**; classes raras exigem
   alocação **desproporcional** com oversampling. Nenhum trabalho de ES encontrado
   reconcilia os dois.

### Lacunas desta rodada

- **Nenhuma regra em MSR/ES para tamanho de gold set** em função da precisão desejada
  nas métricas do classificador — que é o que E-6 precisa.
- **Nenhum trabalho de ES** dimensiona amostra para prevalência rara com margem
  relativa; foi preciso sair da área.
- **Nenhum trabalho de ES combina** triagem por LLM + anotação humana como desfecho +
  estimador estratificado com FPC. **É o gap que a QI-1 ocupa.**
- **Nenhuma orientação em ES sobre α/κ para multi-label** aplicada empiricamente.
- **Nenhum protocolo em MSR para anotação em línguas que o anotador não domina.** As
  duas saídas documentadas são *excluir* (Prana et al., 48 repos) ou *ter um nativo
  por língua* (Katzy et al., preprint fora de MSR).
- **Nenhum estudo em MSR mede o efeito de ancoragem** de rótulos de LLM sobre
  anotadores.

### Artigos a verificar manualmente antes de E-6

1. **Herzig et al. ICSE 2013, §III + Fig. 1** — prioridade máxima. Verificar se a
   assimetria (só o estrato positivo re-anotado) é aceitável: produz **limite
   inferior**. Se a QI-1 precisa de estimativa não enviesada, os falsos negativos do
   classificador exigem amostragem própria.
2. **Herbold et al. EMSE, §3.5–3.6 e Threats** — consenso e anti-ancoragem;
   comparação útil mesmo com o cegamento de [[Decision Log#D-021]].
3. **Ahmed et al. MSR 2025, §IV-B e Fig. 11** — verificar se o limiar >0,5 vale para
   classificação de documentos.
4. **McGrath & Burke 2024, Tab. 1 e 3** — decide o tamanho do gold set.
5. **Yu et al. TSE 2021, §3.3.5–3.3.6 e RQ4** — verificar se a validação é por
   simulação (erro injetado) ou por erro humano real.
6. **Díaz et al. JSS 2022, §4** — confirmar na versão publicada os percentuais.

> **Ressalvas:** Katzy et al. e De Martino et al. são **preprints não revisados por
> pares**. McHugh (2012), fonte dos limiares de κ, **não foi verificada em texto
> completo** — verificar antes de citar valores.

## Ameaças à validade que permanecem

- **Revisão focada, não sistemática.** Trabalhos relevantes podem ter escapado.
- **Ausência de precedente.** Não há método consagrado de tratamento multilíngue em
  MSR a seguir; as escolhas aqui são argumentadas, não herdadas.
- **DSL/PPI vêm de fora da ES.** A transferência é conceitualmente sólida, mas não
  há precedente em MSR que a valide neste tipo de artefato.
- **Detecção de idioma sem ground truth humano** ([[EXP-004]]) — pendência real.
- **Desempenho do LLM por idioma é desconhecido** e só será medido em E-7. Se cair
  muito em algum idioma, é ameaça direta à estimativa de prevalência.
- **Gao et al. não foi lido integralmente** — risco de sobreposição não mapeada.

## Ligações

[[QI-1 Methodology]] · [[Multilingual Strategy]] · [[Decision Log]] · [[EXP-003]] ·
[[EXP-004]] · [[EXP-002]] · [[Codebook]] · [[03 - Methodology]]
