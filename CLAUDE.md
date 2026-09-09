# CLAUDE.md — Instruções para trabalhar neste repositório

Este arquivo orienta sessões do Claude Code neste projeto. Ele **não** é
documentação do projeto em si (isso é `README.md`) nem o estado acumulado de
decisões (isso é `MEMORY.md`). Separação de responsabilidades:

- **`README.md`** — documentação geral e pública do projeto (o que é, como
  rodar, como citar).
- **`CLAUDE.md`** (este arquivo) — como o agente deve trabalhar aqui.
- **`MEMORY.md`** — estado acumulado, decisões e contexto de continuidade
  entre sessões. É um *ponteiro* resumido; a fonte da verdade metodológica
  continua sendo `notes/Decisions/Decision Log.md` e `notes/03 - Methodology.md`.

## No início de qualquer trabalho relevante

1. Rode `git branch --show-current`. A branch `Q1` normalmente está muito à
   frente de `main` — não assuma que `main` reflete o estado atual do
   projeto (ver `MEMORY.md` §9).
2. Leia `MEMORY.md` para o estado atual (etapas concluídas, pendências,
   decisões que não devem ser revertidas sem razão explícita).
3. Onde as coisas estão (reorganizado em 2026-09-05):
   - `notes/Decisions/` — `Codebook.md` (o instrumento, **v2.5**) e
     `Decision Log.md` (**índice de status no topo** — leia-o em vez de
     percorrer as 29 entradas). **Não dividir o Decision Log**: o valor dele
     é ser registro único e cronológico.
   - `notes/Instruments/` — o que se usa para anotar, em ordem de uso:
     `Classification Prompt.md` (etapa 1, para as CLIs) ·
     `Guia do Anotador Humano.md` (etapa 1, adjudicação) ·
     `Taxonomy Coding Protocol.md` (etapa 2, open coding — **não testado**).
     Instrumentos são nomeados **pelo que são**, com versão no frontmatter —
     não por decisão. Não crie `Instrumento (D-XXX).md`.
   - `notes/Experiments/` — só o caminho crítico (EXP-013, EXP-014).
     O resto está em `notes/_arquivo/`, **não apagado** — ver o `README.md`
     de lá, que diz o que ainda é citável de cada um.
   - `notes/Literature/` — `README.md` (índice), `Protocolo de Busca.md`,
     `Resultado da Busca.md` e uma nota por referência.
   - `referencias.bib` na raiz.
4. Consulte `README.md` para setup/dataset, e as skills abaixo quando a
   tarefa exigir:
   - `project-context` — antes de analisar dados, escrever código, interpretar
     resultados ou responder qualquer pergunta sobre o repositório.
   - `data-analysis` — antes de consultar/agregar/amostrar o dataset (regras de
     DuckDB, denominadores corretos, reprodutibilidade).
   - `security-analysis` — antes de definir critério de inclusão, anotar
     amostra, desenhar amostragem, validar classificador ou interpretar
     qualquer resultado sobre skills de segurança.

## Quando atualizar o `MEMORY.md`

Atualize (ou peça para atualizar) sempre que houver:

- uma nova decisão metodológica registrada no Decision Log;
- mudança estrutural relevante (novo módulo/script central, reorganização de
  `notes/`, mudança de convenção de nomeação `EXP-XXX`);
- nova integração externa (novo dataset, novo modelo/API externo);
- conclusão de uma etapa significativa do plano (`03 - Methodology.md`) —
  por exemplo, fechar o E-5 humano, produzir o gold set do E-6, validar um
  classificador no E-7.

Não registre detalhes triviais, logs de execução ou informação facilmente
reconstruível lendo o código/notas — isso é ruído que compete por atenção
com o que realmente importa para continuidade.

## Regras de trabalho específicas deste repositório

- **Nunca commite sem o pesquisador pedir explicitamente.** Isso vale mesmo
  depois de completar uma tarefa grande — reporte o que foi feito e espere
  confirmação.
- **Todo número que for citado no texto do TCC precisa vir de um script
  versionado em `scripts/`, com saída em `results/`, referenciado por um
  `EXP-XXX`.** Antes de criar um novo `EXP-XXX`, confira
  `notes/03 - Methodology.md` §8 — vários números já estão reservados para
  etapas futuras do caminho crítico.
- **Preserve decisões existentes até haver evidência de que precisam
  mudar.** Decisões de alto impacto (definição de "segurança", threshold,
  unidade de análise, descarte de volume de dados, escolha de modelo
  definitivo) exigem aprovação humana explícita e uma nova entrada no
  Decision Log — não decida isso sozinho nem reverta uma decisão anterior em
  silêncio.
- **`results/README.md` é o índice das saídas** — qual arquivo pertence a qual
  `EXP-XXX`, quem gera, quem consome, e qual é o da etapa atual. Leia-o em vez
  de percorrer o diretório.
- **`data/` é gitignored** — nunca versionar Parquet do dataset. `results/`
  e `models/` têm política mista (agregados pequenos versionados, binários
  e texto de terceiros gitignored) — ver `.gitignore` e `MEMORY.md` §3 antes
  de adicionar um arquivo novo a um desses diretórios.
- Separe sempre **observação** (o que os dados mostram), **interpretação**
  (uma explicação possível) e **conclusão** (sustentada por método e
  evidência) — não misture as três ao reportar um resultado.

## Armadilhas ativas deste repositório

Coisas que já morderam e vão morder de novo:

- **O plugin `remember` vaza cegamento.** No [[EXP-014]] ele injetou, no
  início da sessão de um avaliador, achados da análise anterior — inclusive
  **a direção do viés do outro avaliador**. Não deixa rastro na saída.
  **Antes de qualquer rodada cega, desativar explicitamente**; se não for
  possível, declarar como limitação.
- **Nunca escreva saída dentro de `results/EXP-013_llm_cases/`.** O prompt
  manda o modelo ler tudo daquele diretório — um arquivo de output ali fica
  visível para o avaliador seguinte. Já aconteceu.
- **`uv run` falha em silêncio nesta máquina** (exit 120, sem saída). Os
  scripts do caminho crítico usam só stdlib: rode `python script.py` direto.
  `uv run` só quando houver dependência real (duckdb, lingua).
- **`ProcessPoolExecutor` quebra no Windows + `uv run`** (spawn). Use
  `ThreadPoolExecutor`, ou WSL — que tem instabilidade própria aqui.
- **Mover arquivos com o Obsidian aberto** desatualiza o índice dele e
  produz "falha ao abrir". Wikilinks resolvem por nome, então mover é
  seguro; **renomear quebra** e exige atualizar as referências.

## Ao lidar com referências bibliográficas

- **Nunca escreva entrada de `.bib` de memória.** Use a fonte autoritativa:
  ```bash
  curl -sLH "Accept: application/x-bibtex" https://doi.org/<DOI>
  curl -s "https://export.arxiv.org/api/query?id_list=<ID>"
  ```
- **Busca por título produz falso positivo.** Já aconteceu aqui: *"Learning
  from Disagreement: A Survey"* casou com um artigo de economia no SSRN, só
  pela palavra "disagreement" — teria virado citação fabricada com DOI real
  de outro artigo. **Sempre confira se o título devolvido é o que foi
  pedido.** Nenhuma ferramenta (nem MCP) é imune a isso.
- **Verificado ≠ lido.** O campo `leitura:` nas notas de
  `notes/Literature/` diz se o texto foi de fato recuperado. Não afirme que
  uma referência sustenta algo sem que alguém a tenha lido.
