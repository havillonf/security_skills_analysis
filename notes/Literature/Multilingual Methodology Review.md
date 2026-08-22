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

[[EXP-004]] mostrou que a detecção é confiável onde há massa e ruim na cauda.
Estratos revisados:

```text
L1  en                       ~84,6%   detecção confiável (concordância 1,00)
L2  zh                        ~6,0%   confiável
L3  ja + ko                   ~3,0%   confiável
L4  de + es + pt + fr + it    ~4,0%   confiável (concordância 1,00)
L5  cauda + und + mixed       ~2,4%   NÃO estratificar internamente
```

Mudança em relação à proposta anterior: **L5 passa a absorver `mixed` e a cauda
inteira**, porque a concordância de 0,667 naquele estrato não sustenta separação por
idioma. `la` entra em L5, não como idioma.

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
