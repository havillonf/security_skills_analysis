---
tipo: literatura
leitura: conteudo-recuperado
usado-em: RQ-B — comparacao de confiabilidade e de estrategia de definicao
---

# SeRe — Security-Related Code Review Dataset

**arXiv 2601.01042** — https://arxiv.org/html/2601.01042

## O que e

Dataset de comentarios de revisao de codigo rotulados como relacionados ou nao
a seguranca, alinhado a atividade real de revisao.

**Definicao adotada:** um comentario e relacionado a seguranca se *"identifica
riscos potenciais de seguranca no codigo ou oferece recomendacoes para melhorar
a seguranca do codigo"*.

**Estrategia de definicao em duas partes** — e o ponto mais interessante para
nos:

| Camada | Como funciona |
|---|---|
| **Intensional** | Anotadores familiarizados com guias de codigo seguro (OWASP) para formar o conceito |
| **Extensional** | **Taxonomia CWE como referencia**: comentario mapeavel a uma categoria CWE e rotulado como de seguranca; sem mapeamento claro, recorre-se a definicao intensional |

**Anotacao:** 6 voluntarios proficientes em seguranca, rotulando
independentemente; discordancia resolvida por discussao ate consenso.

## Resultados de confiabilidade

| | |
|---|---|
| **Fleiss' kappa** | **0,88** |
| Amostras corretamente rotuladas (avaliacao humana) | 94% |
| Reviews de seguranca que mapeiam a vulnerabilidade CWE real | 84% |

## No que nos ajudou

**1. E o benchmark mais alto que encontramos — e explica por que.** kappa=0,88
contra nosso 0,672. Quatro diferencas explicam a distancia, e nenhuma delas
significa que nosso instrumento seja pior:

- **Unidade muito menor.** Comentario de revisao (curto, com um proposito) vs.
  `SKILL.md` inteiro (longo, multiproposito). Julgar "esse comentario levanta
  risco?" e incomparavelmente mais restrito que "esse documento inteiro e uma
  skill de seguranca?".
- **Tarefa binaria**, contra nossas tres classes.
- **6 anotadores humanos especialistas**, contra 2 LLMs.
- **Ancoragem externa via CWE.**

**2. Nomeia um trade-off que temos de decidir conscientemente.** A ancoragem
extensional em CWE e, muito provavelmente, o que mais eleva o kappa deles: ela
restringe drasticamente o espaco de julgamento.

Nos **poderiamos** fazer o mesmo — ancorar `security_relevance` em CWE ou OWASP
— e quase certamente subir a confiabilidade. **O custo seria encontrar apenas o
que esses catalogos ja conhecem.** Skills sobre restricao de comportamento de
agente, prompt injection ou escopo de ferramenta nao tem mapeamento CWE limpo,
e sao justamente a categoria mais caracteristica deste corpus (35% do desacordo
no [[EXP-013]]).

Ou seja: **kappa alto e cobertura do fenomeno novo estao em tensao direta
aqui.** Vale registrar essa escolha explicitamente no TCC em vez de deixar
parecer que nosso kappa e mais baixo por descuido.

**3. Confirma a pratica de resolver discordancia por discussao/consenso**, como
faz nosso desenho de adjudicacao.

## Ressalva

Dominio adjacente, nao igual: comentarios de revisao de codigo, nao skills.
A comparacao de kappa e informativa, nao equivalente.

## Ligacoes

[[EXP-014]] · [[Codebook]] · [[Taxonomias Externas de Seguranca]] · [[Resultado da Busca]]
