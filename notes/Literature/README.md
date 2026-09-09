---
tipo: indice
data: 2026-09-05
---

# Literatura

Uma nota por referência (ou família de referências), com: **o que é**, **o
intuito dos autores**, **no que nos ajudou** — com o número ou a decisão
concreta que ela sustenta — e **ressalvas**.

> [!danger] Leia o campo `leitura:` antes de citar qualquer uma
> Boa parte destas referências entrou no projeto por **resumo de busca**, não
> por leitura direta. Citar no TCC algo que não foi lido é risco real, e o
> campo `leitura:` no frontmatter de cada nota diz exatamente em que pé está:
>
> | Valor | Significa |
> |---|---|
> | `conteudo-recuperado` | O conteúdo foi efetivamente lido. Citável. |
> | `parcial` | Metadados/estrutura recuperados, conteúdo não confirmado. **Verificar antes de citar.** |
> | `resumo-de-busca` | Só o resumo do buscador. **Ler antes de citar.** |

## Como esta pasta foi construída

- [[Protocolo de Busca]] — protocolo declarado (perguntas, strings, critérios)
- [[Resultado da Busca]] — execução de 2026-09-05: o que entrou, o que foi
  excluído e **por quê**

## Por decisão que sustenta

| Onde é usada | Referência | Leitura |
|---|---|---|
| **Corroboração do resultado** (~7% em `PRIMARY`) | [[Agent Skills in the Wild]] | ✅ recuperado |
| **`operationality`** (Taxonomy Coding Protocol) | [[SAcoding - Actionability de Conselho de Seguranca]] | ✅ recuperado |
| **Benchmark de confiabilidade** e o trade-off CWE | [[SeRe - Security-Related Code Review Dataset]] | ✅ recuperado |
| **D-026** — desenho do ensemble | [[Consenso de LLMs com Adjudicacao Humana]] | ⚠️ parcial |
| **D-026** — limites do LLM como anotador | [[LLMs como Anotadores - Confiabilidade]] | ⚠️ resumo |
| **D-028** — exclusão de frame | [[Analise de Conteudo - Unidades Nao Codificaveis]] | ⚠️ resumo |
| **D-028** — controle de viés da exclusão | [[Identificacao Parcial - Limites de Manski]] | ⚠️ resumo |
| **D-028 / D-014** — corte e desenho amostral | [[Sampling in Software Engineering Research]] | ⚠️ resumo |
| **D-029** — remoção de `security_functions` | [[Taxonomias Externas de Seguranca]] | ⚠️ resumo |
| **`compute_agreement.py`** e Codebook §8 | [[Coeficientes de Concordancia]] | misto |
| **Relato da QI-1 em camadas** | [[Learning from Disagreement]] | ⚠️ resumo |

## Síntese temática

[[Classification and Sampling Precedents]] — a busca original que originou
estas notas, organizada por pergunta metodológica em vez de por artigo. Útil
para ver o argumento inteiro; as notas individuais são para citar.

## O que a literatura mudou no projeto

Três casos em que a busca **corrigiu** uma conclusão nossa, e não apenas
confirmou:

1. **[[SAcoding - Actionability de Conselho de Seguranca]]** mostrou que
   `operational_security` (77%) e `operation_level` (61%) — que havíamos
   chamado de "a pior medida do instrumento" — estão **dentro da faixa
   publicada** (80% e 46% no método de referência). A dificuldade é do
   construto, não do nosso instrumento.
2. **[[Agent Skills in the Wild]]** explicou por que o κ=0,86 deles não é
   comparável ao nosso: taxonomia de rótulo único, sem equivalente de
   `SECONDARY`. O kappa alto vem de contornar a fronteira difícil.
3. **[[Analise de Conteudo - Unidades Nao Codificaveis]]** trouxe um alerta
   contra nós — mudar o esquema no meio invalida a confiabilidade medida sob o
   esquema anterior —, que virou a distinção explícita entre o que transfere
   (v2.4→v2.5) e o que não transfere (v2.3→v2.4).

## Lacuna conhecida

**Não foi localizado nenhum trabalho** usando escala ordinal graduada de
*relevância* de segurança (primária / secundária / incidental / nenhuma) para
artefatos de software. As taxonomias existentes classificam por **função**, não
por **centralidade**. Ver [[Taxonomias Externas de Seguranca]] §2.

Isso é oportunidade e aviso ao mesmo tempo — e a busca **não foi sistemática**
(sem protocolo declarado, sem strings versionadas, sem critério de
inclusão/exclusão). Para virar seção de trabalhos relacionados no TCC, precisa
ser refeita com protocolo.
