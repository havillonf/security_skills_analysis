---
tipo: checklist
data: 2026-09-05
acompanha: referencias.bib
---

# Verificação de referências

Estado de `referencias.bib` (raiz do projeto): **27 entradas**.

> [!success] Nenhuma entrada foi reconstruída de memória
> **14 via Crossref** (content negotiation no DOI — registro do próprio
> editor) · **10 via API do arXiv** (busca por ID, sem ambiguidade) ·
> **3 manuais** a partir de documento oficial na web.

> [!danger] Verificado ≠ lido
> Isto trata de **metadados**. Se o texto foi efetivamente lido está no campo
> `leitura:` da nota de cada referência — e só **duas** estão como
> `conteudo-recuperado`. Citar sem ler é problema separado, e maior.

---

## ✅ Metadados resolvidos — nada a conferir

### Coeficientes de concordância

| Chave | Referência | Fonte |
|---|---|---|
| `cohen1960kappa` | *Educ. Psychol. Meas.* 20(1), 37–46 | Crossref |
| `landis1977measurement` | *Biometrics* 33(1), 159 | Crossref |
| `feinstein1990paradoxes` | *J. Clin. Epidemiol.* 43(6), 543–549 | Crossref |
| `byrt1993bias` | *J. Clin. Epidemiol.* 46(5), 423–429 | Crossref |
| `gwet2008ac1` | *Br. J. Math. Stat. Psychol.* 61(1), 29–48 | Crossref |
| `hayes2007answering` | DOI 10.1080/19312450709336664 | Crossref |
| `mcnemar1947note` | *Psychometrika*, DOI 10.1007/bf02295996 | Crossref |
| `zapf2016interrater` | *BMC Med. Res. Methodol.* | Crossref |
| `lombard2002intercoder` | *Human Communication Research* | Crossref |

### Método e desenho

| Chave | Referência | Fonte |
|---|---|---|
| `baltes2022sampling` | Baltes & Ralph, *EMSE* **27(4)**, 2022 | Crossref |
| `uma2021disagreement` | Uma, Fornaciari, Hovy, Paun, Plank, Poesio — **JAIR 72**, 1385–1470, 2021 | Crossref |
| `egami2023surrogate` | Egami, Hinck, Stewart, Wei — **NeurIPS 36**, 68589–68601, 2023 | Crossref |
| `manski1989anatomy` | Manski, *J. Human Resources* 24(3), 1989 | Crossref |
| `sequeira2020krippendorff` | Guia de α para ES — **publicado no JSS (2023)** | arXiv |

### Segurança e agent skills

| Chave | Referência | Fonte |
|---|---|---|
| `liu2026agentskills` | Liu et al. — *Agent Skills in the Wild* | arXiv |
| `zhao2026sere` | Zhao et al. — **aceito na ICSE 2026** | arXiv |
| `barrera2023securityadvice` | Barrera, Bellman, van Oorschot — *J. Cybersecurity* 9(1), tyad013 | Crossref |
| `aiteammates2026` | *Security in the Age of AI Teammates* | arXiv |
| `ceur2021securitytools` | *Classification of Software Security Tools* | manual |
| `nist_samate` | NIST SAMATE Tool Taxonomy | manual |

### Anotação por LLM

| Chave | Referência | Fonte |
|---|---|---|
| `goodall2026ethnographic` | Goodall et al. | arXiv |
| `assistants2025` | *Effective Assistants, Not Good Independent Annotators* — **ACL 2026 Findings** | arXiv |
| `promptbank2026` | *A Validated Prompt Bank...* | arXiv |
| `beyondconsensus2026` | *Beyond Consensus* | arXiv |
| `adjudicators2026` | *LLMs as Annotators and Adjudicators* | arXiv |

### Dataset e análise de conteúdo

| Chave | Referência | Fonte |
|---|---|---|
| `destefanis2026gitskills` | Destefanis, Graziotin, Vaccargiu, Ortu | arXiv |
| `gao1996content` | GAO/PEMD-10.3.1 | manual |

---

## ⚠️ Ressalvas por entrada — ler antes de citar

- [x] **`destefanis2026gitskills`** — **DECIDIDO:** citar como preprint do
  arXiv, não como MSR 2027. Os anais de 2027 não existem hoje, logo páginas,
  editora e DOI da versão publicada são inverificáveis. Quando a MSR publicar,
  trocar para `@inproceedings` com `year=2027`.

- [x] **`manski1989anatomy`** — **DECIDIDO pelo pesquisador:** *Anatomy of the
  Selection Problem* (J. Human Resources 24(3), 1989) é a referência adotada
  para o argumento de identificação parcial em D-028.

- [ ] **`goodall2026ethnographic`** — os valores **κ=0,233 e 0,573 não estão
  no abstract**. A direção do achado está confirmada; a magnitude, não. Ler o
  corpo antes de citar número.

- [ ] **`zhao2026sere`** — faltam páginas e editora dos anais da ICSE 2026.

- [ ] **`assistants2025`** e **`sequeira2020krippendorff`** — saíram em
  veículo (ACL 2026 Findings e JSS 2023). **Preferir a versão publicada** ao
  preprint.

- [ ] **`ceur2021securitytools`** — faltam autores, ano e páginas. Abrir o PDF.

- [ ] **`gao1996content`** — ano inferido. Confirmar no documento.

---

## ❌ Descartada, com motivo

- [x] **Krippendorff, *Content Analysis* (livro)** — **não entra.**
  Levantamento no repositório mostrou que o projeto usa Krippendorff em
  **um único papel: α como coeficiente de concordância** — implementado em
  `compute_agreement.py`, citado no Codebook §8 e no Taxonomy Coding Protocol
  §5.2. Para isso a referência canônica é `hayes2007answering` (verificada), e
  o guia aplicado a engenharia de software é `sequeira2020krippendorff`.

  A metodologia de análise de conteúdo do livro **não é usada em lugar
  nenhum** — o argumento de unidades não codificáveis vem de `gao1996content`
  e `lombard2002intercoder`. Citar o livro exigiria escolher entre 2ª/3ª/4ª
  edição (paginação diferente) sem ganho algum.

  Se o orientador preferir citá-lo assim mesmo, é uma consulta na Sage.

**Nenhuma outra pendência de metadados. As 27 entradas estão resolvidas.**

---

## Lição desta rodada, que vale guardar

A busca automática **por título produziu um falso positivo grave**: a consulta
por *"Learning from Disagreement: A Survey"* casou com *"Disagreement à la
Taylor: Evidence from Survey Microdata"* (Dräger & Lamla, 2015, economia,
SSRN) — apenas pela palavra "disagreement".

Se tivesse sido aceito sem inspeção, entraria no TCC como **citação fabricada
com DOI real de outro artigo** — o pior tipo de erro, porque parece verificado.

Foi corrigido adicionando **guarda de similaridade de Jaccard ≥ 0,60** nos
tokens do título, mais inspeção manual das que ficaram no limite. Com a
guarda, a mesma consulta retornou o DOI correto do JAIR (similaridade 1,00).

**Nenhuma ferramenta de busca por título é imune a isso** — nem MCP. O que
protege é conferir se o título devolvido é o que você pediu.

## Como conferir, se precisar refazer

```bash
# BibTeX autoritativo a partir de qualquer DOI
curl -sLH "Accept: application/x-bibtex" https://doi.org/<DOI>

# metadados oficiais de preprint do arXiv
curl -s "https://export.arxiv.org/api/query?id_list=<ID>"
```

O `id_list` do arXiv busca por **identificador**, não por título — não tem o
modo de falha acima.

## Ligações

`referencias.bib` · `notes/Literature/README.md` · [[Protocolo de Busca]] ·
[[Resultado da Busca]]
