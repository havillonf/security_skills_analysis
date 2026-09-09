---
tipo: literatura
leitura: conteudo-recuperado
usado-em: Taxonomy Coding Protocol (operationality)
---

# SAcoding — actionability de conselho de seguranca

> [!warning] Correcao de autoria (2026-09-05)
> Esta nota atribuia o trabalho a "Chowdhury & van Oorschot". **Errado.**
> Verificado na pagina do arXiv: os autores sao **David Barrera,
> Christopher Bellman e Paul C. van Oorschot**. O titulo completo do
> preprint e *A Close Look at a Systematic Method for Analyzing Sets of
> Security Advice*.

**Barrera, D., Bellman, C., & van Oorschot, P. C.**, *Journal of Cybersecurity*
9(1), 2023, tyad013 —
https://academic.oup.com/cybersecurity/article/9/1/tyad013/7217003
· preprint: https://arxiv.org/pdf/2209.04502

## O que e

Metodo sistematico para analisar **conjuntos de conselho de seguranca**,
medindo **actionability** e classificando cada item em:

| Categoria | Tag |
|---|---|
| Praticas (subdivididas por viabilidade e expertise do alvo) | P1-P6 |
| Politicas — abordagem geral sem tecnica especifica | P2 |
| Principios — regras gerais que historicamente melhoram seguranca | N |
| Resultados — estado final desejado, sem metodo | T/T' |
| Nao-uteis — obscuro, difuso, fora de escopo | M1-M2 |

**Acionavel = receber uma das quatro tags de pratica P3-P6.** Nao acionavel:
outcomes, principles, policies e itens obscuros.

**Procedimento:** arvore de decisao com **10 perguntas sim/nao sequenciais**
(Q1-Q10), cada resposta determinando a proxima, ate um no folha com a tag.
Nao e julgamento holistico.

## Intuito dos autores

Dar rigor a algo que ate entao era impressionista — "esse conselho de
seguranca e util?" — permitindo comparar documentos de orientacao entre si de
forma reprodutivel.

## No que nos ajudou

**1. Mostra que nossa dimensao fraca e fraca para todo mundo.** Este achado
**corrigiu uma conclusao nossa errada.** Haviamos classificado
`operational_security` (p_o=77%) e `operation_level` (p_o=61%) como "a pior
medida do instrumento", e dito que 61% "nao sustenta afirmacao de tese".

Os numeros publicados:

| | Concordancia |
|---|---|
| Acionabilidade, itens de tag unica | **80%** |
| Atribuicao completa de tag | **46%** |
| (comparavel) taxonomia de resposta a incidentes | kappa=0,39 -> 0,527 apos refinamento |

Nossos 77% estao **em cima do estado da arte**; os 61% ficam entre os dois
patamares deles. **A dificuldade e do construto, nao do nosso instrumento.**
Consequencia: nao esperar kappa alto em `operationality`, e reportar contra
este benchmark em vez de contra expectativa arbitraria.

**2. Da uma alternativa de desenho.** Arvore de decisao sequencial em vez de
escala holistica. Se a medicao de `operationality` sair fraca, converter para
arvore de 3-4 perguntas e a correcao indicada pela literatura — antes de
abandonar a dimensao.

**3. Fornece vocabulario estabelecido.** *practices · policies · principles ·
outcomes* e distincao publicada e citavel, proxima do nosso
`descriptive · procedural · executable`.

## Ressalva importante — isto NAO viola a regra da QI-2

A regra inegociavel proibe importar referencial externo para construir a
**taxonomia empirica de preocupacoes de seguranca** (OWASP, MITRE, NIST CSF).
SAcoding e **instrumento metodologico de acionabilidade**, nao taxonomia de
conteudo. Usar instrumento estabelecido para medir operacionalidade e boa
pratica; importar categorias de conteudo e que cria circularidade.

## Outras ressalvas

- Dominio de origem: **politicas e documentos de orientacao de seguranca
  organizacional**, nao agent skills. A transferencia e plausivel mas nao
  demonstrada.
- Os autores alertam: *"proporcoes similares entre codificadores nao implicam
  concordancia sobre a acionabilidade de itens individuais"* — distribuicao
  parecida pode esconder desacordo caso a caso.

## Ligacoes

[[Taxonomy Coding Protocol]] · [[EXP-014]] · [[Decision Log#D-029]]
