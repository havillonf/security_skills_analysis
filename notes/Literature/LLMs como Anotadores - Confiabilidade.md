---
tipo: literatura
leitura: abstract-verificado; numeros do corpo NAO confirmados
usado-em: RQ-C — justificativa e limites de D-026
---

# LLMs como anotadores — confiabilidade

Familia de trabalhos sobre usar LLMs para anotacao, e quanto se pode confiar.

- **Large language models struggle with ethnographic text annotation** —
  https://arxiv.org/pdf/2601.12099
- **Large Language Models Are Effective Human Annotation Assistants, But Not
  Good Independent Annotators** — https://arxiv.org/pdf/2503.06778
- **Comparing large language models and human annotators in latent content
  analysis** (*Scientific Reports*) —
  https://www.nature.com/articles/s41598-025-96508-3
- **Large Language Models as Automatic Annotators and Annotation Adjudicators
  for Fine-Grained Opinion Analysis** — https://arxiv.org/pdf/2601.16800
- **A human-LLM collaborative annotation approach for screening articles** —
  https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12481989/

## No que nos ajudou

**1. Calibra nosso kappa LLM-LLM, e favoravelmente — mas com um numero NAO
CONFIRMADO.** A sintese do buscador reportou concordancia **LLM-LLM
kappa=0,233** contra **humano-humano kappa=0,573** no estudo de anotacao
etnografica. **Fui ao abstract do artigo e esses valores nao estao la** — o
resumo afirma apenas que *"a confiabilidade entre codificadores humanos
estabeleceu um teto aproximado para a acuracia dos LLMs"* e que os modelos
tiveram desempenho inferior mesmo em features onde a concordancia humana era
forte.

**Nao citar 0,233 nem 0,573 sem abrir o texto completo.** A direcao do achado
(LLMs concordam menos entre si que humanos) esta confirmada pelo abstract; a
magnitude, nao.

Nosso [[EXP-014]] deu **kappa=0,672 entre dois LLMs**. Isso e substancialmente
acima do que essa literatura observa em tarefa interpretativa, o que sugere que
o instrumento v2.4/v2.5 esta fazendo trabalho real de restringir o julgamento —
nao que a tarefa seja trivial.

**2. Sustenta o desenho de [[Decision Log#D-026]], e delimita o que ele pode
afirmar.** O titulo *"Effective Human Annotation Assistants, But Not Good
Independent Annotators"* e praticamente a tese do nosso desenho: LLM classifica
em escala, humano adjudica. Serve como citacao direta para justificar por que
nao aceitamos consenso de LLM como ground truth sem revisao.

**3. Alerta sobre dependencia de tarefa.** Em analise de conteudo latente, LLMs
igualaram humanos em sentimento e inclinacao politica, mas **nao** em
intensidade emocional e sarcasmo. Concordancia alta numa dimensao nao autoriza
extrapolar para outra — no nosso caso, o kappa da classe nao autoriza supor que
a etapa 2 (taxonomia) sera igualmente confiavel.

## Ressalvas

**O fetch do artigo principal falhou** (PDF nao extraiu os valores). Os kappa
0,233 e 0,573 vieram de **resumo de busca**. Sao numeros que eu usaria numa
comparacao importante — **confirmar no texto antes de citar**.

Dominios distantes (etnografia, opiniao, sentimento). A transferencia para
classificacao de artefato tecnico e argumentavel, nao automatica.

## Ligacoes

[[Decision Log#D-026]] · [[EXP-014]] · [[Learning from Disagreement]] · [[Resultado da Busca]]
