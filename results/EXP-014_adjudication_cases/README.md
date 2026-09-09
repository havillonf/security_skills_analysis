# Casos para auditoria humana — EXP-014

Os **16 casos** em que os avaliadores divergiram e que exigem decisão humana
([[Decision Log#D-026]]). Cada `<case_id>.md` traz o `SKILL.md` completo.

## Como usar

1. Abra `results/EXP-014_adjudication_form.csv`.
2. Para cada `case_id`, leia o arquivo correspondente **desta pasta**, do zero.
3. Classifique seguindo `notes/Instruments/Guia do Anotador Humano.md`
   (Codebook **v2.6**).

> [!danger] Não abra antes de decidir
> `EXP-014_gpt_output.jsonl`, `EXP-014_claude_output.jsonl` e
> `EXP-014_comparison_report.jsonl` contêm o rótulo dos modelos. Ver a
> saída deles antes de decidir contamina a adjudicação e invalida a
> independência que sustenta o D-026.

## Por que esta pasta existe, separada de `EXP-013_llm_cases/`

| | `EXP-013_llm_cases/` | esta pasta |
|---|---|---|
| Conteúdo | os 100 casos do ensemble | só os 16 que precisam de decisão humana |
| Git | gitignored | **versionada** |
| Papel | **diretório cego** — o prompt manda o modelo ler tudo dali | material de leitura do humano |

Nunca escreva saída dentro de `EXP-013_llm_cases/`. Esta pasta não tem esse
problema: nada aqui é lido por modelo nenhum de forma automática.

## Procedência

`PROVENANCE.csv` traz, por caso, o repositório de origem, o caminho do arquivo
e a **licença declarada** do repositório. O conteúdo é de terceiros, público no
GitHub, reproduzido aqui para tornar a auditoria verificável. Ao citar um caso
no texto do TCC, use essa tabela para atribuir corretamente.

Distribuição de licenças nesta pasta:

| Licença | Casos |
|---|---:|
| `NAO DECLARADA` | 14 |
| `MIT` | 2 |

## Reprodutibilidade

Gerado por `scripts/build_adjudication_package.py`, a partir de
`EXP-014_adjudication_form.csv` e `EXP-013_llm_sample.csv`. O script é
idempotente e **nunca sobrescreve o formulário**.
