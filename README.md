# Security Skills Analysis

Estudo sobre a prevalência de **skills de segurança** na população pública de
Agent Skills, usando o dataset [GitSkills](https://zenodo.org/records/21875637).

> **Dataset:** Destefanis, G., Graziotin, D., Vaccargiu, M., & Ortu, M. (2027).
> *GitSkills: A Dataset of Agent Skills on GitHub*. MSR '27.
> [arXiv:2608.10906](https://arxiv.org/abs/2608.10906)

---

## A pergunta

> **QI-1 — Qual a prevalência de skills de segurança na população pública de
> Agent Skills?**

Uma **Security Skill** é uma skill cujo propósito principal (`PRIMARY`), ou
parte do comportamento descrito (`SECONDARY`), envolve prevenir, detectar,
analisar, avaliar, explorar, mitigar ou responder a ameaças em **sistemas
computacionais**. Definição completa: [`notes/Decisions/Codebook.md`](notes/Decisions/Codebook.md).

Extensões, fora do caminho crítico: **QI-2** (que preocupações de segurança
aparecem) e **QI-3** (cobertura frente a frameworks externos).

## Onde o projeto está

| Etapa | Estado |
|---|---|
| População definida | ✅ 1.571.243 skills 100% em inglês (de 1.877.981) |
| Instrumento de classificação | ✅ Codebook v2.5, três classes |
| Confiabilidade medida | ✅ Cohen's κ = 0,724 (classe) · 0,672 (dicotomia da QI-1) |
| Adjudicação humana | ⬜ 16 casos pendentes |
| Taxonomia de categorias (QI-2) | ⬜ protocolo escrito, não executado |
| Classificação em escala + estimativa | ⬜ |

Estado detalhado e pendências: [`MEMORY.md`](MEMORY.md).

## Por onde começar a ler

1. [`notes/00 - Research Overview.md`](notes/00%20-%20Research%20Overview.md) — o projeto em uma página
2. [`notes/Decisions/Codebook.md`](notes/Decisions/Codebook.md) — **o instrumento**: o que conta como skill de segurança
3. [`notes/Decisions/Decision Log.md`](notes/Decisions/Decision%20Log.md) — por que cada escolha foi feita (índice de status no topo)
4. [`notes/Experiments/EXP-014.md`](notes/Experiments/EXP-014.md) — o resultado mais recente

Para a versão em linguagem simples: [`notes/Resumo do Trabalho.md`](notes/Resumo%20do%20Trabalho.md).

---

## Estrutura

```
notes/                    caderno científico (Obsidian) — fonte da verdade
├── 00–03 *.md            visão geral · questão · hipóteses · plano de etapas
├── Decisions/            Codebook (o instrumento) · Decision Log (o porquê)
├── Instruments/          o que se usa para anotar, em ordem de uso:
│                           Classification Prompt.md      → etapa 1, para as LLMs
│                           Guia do Anotador Humano.md    → etapa 1, adjudicação
│                           Taxonomy Coding Protocol.md   → etapa 2, open coding
├── Methodology/          desenho estatístico de QI-1 · QI-2 · QI-3
├── Experiments/          EXP-013 (amostra) · EXP-014 (confiabilidade)
├── Literature/           trabalhos relacionados e precedentes metodológicos
├── Results/              Security Taxonomy (saída da etapa 2)
└── _arquivo/             fora do caminho crítico — ver README de lá

scripts/                  todo número citável nasce aqui
├── compute_agreement.py            Cohen · Krippendorff · Gwet AC1 · McNemar
├── aggregate_llm_classifications.py consenso vs. discordância
├── build_llm_ensemble_sample.py    amostra determinística
├── filter_population_english.py    filtro de idioma na população
└── build_adjudication_form.py      formulário cego

results/                  saída de cada EXP-XXX — comece pelo README.md de lá,
                          que indexa todo arquivo (_arquivo/ = esquema v2.3)
data/                     cache do dataset (gitignored)
```

## Desenho

**Desenho C** — amostragem estratificada com classificador de triagem.
A classificação em escala **nunca é o resultado**: ela forma os estratos, e a
prevalência vem do estimador `p̂ = Σ_h (N_h/N)·p̂_h` com anotação humana dentro
de cada estrato. Ver [`notes/Methodology/QI-1 Methodology.md`](notes/Methodology/QI-1%20Methodology.md).

A classificação acontece em **duas etapas**: primeiro a classe (5 campos), e
só depois, sobre `PRIMARY` ∪ `SECONDARY`, a taxonomia de categorias por open
coding.

## Como rodar

Não há `.venv`: as dependências são efêmeras via `uv`.

```bash
# concordância entre dois avaliadores
python scripts/compute_agreement.py \
  --a results/EXP-014_gpt_output.jsonl \
  --b results/EXP-014_claude_output.jsonl \
  --label-a gpt --label-b claude \
  --out results/EXP-014_agreement.json

# consenso vs. casos que vão para adjudicação humana
python scripts/aggregate_llm_classifications.py \
  --gpt results/EXP-014_gpt_output.jsonl \
  --claude results/EXP-014_claude_output.jsonl

# etapas que tocam o dataset precisam de dependências
uv run --with duckdb --with lingua-language-detector \
  python scripts/build_llm_ensemble_sample.py
```

O dataset não é versionado — cada pessoa baixa localmente do mirror
HuggingFace (`mvaccargiu/gitskills`) para `data/`.

## Convenções

- **Todo número que vai para o texto** nasce de script versionado em
  `scripts/`, com saída em `results/`, referenciado por um `EXP-XXX`.
- **Decisão metodológica não muda em silêncio**: vira entrada no Decision Log,
  com data, alternativas e consequências. Decisão revisada é marcada, não
  apagada.
- **Denominador sempre explícito** — o dataset mistura 3.797.117 ocorrências
  com 1.877.981 conteúdos distintos.
- Notas e commits em português; identificadores de código em inglês.

Instruções para agentes de IA trabalhando neste repositório: [`CLAUDE.md`](CLAUDE.md).
