---
tipo: indice
data: 2026-09-05
---

# Arquivo — fora do caminho crítico

> [!important] Arquivado ≠ irrelevante ≠ falso
> Nada aqui foi descartado por estar errado. Estes arquivos saíram do caminho
> crítico da QI-1 porque o desenho mudou. **Vários ainda são citáveis**, e a
> coluna "ainda vale" diz o quê. Os wikilinks continuam funcionando — o
> Obsidian resolve `[[EXP-002]]` independente da pasta.

## Experimentos

| Arquivo | Por que saiu | O que ainda vale |
|---|---|---|
| [[EXP-001]] | Auditoria estrutural, concluída | **Os denominadores canônicos** (3.797.117 ocorrências · 1.877.981 representantes) e a invalidação do notebook legado. Base de D-001 e D-002 |
| [[EXP-002]] | Candidate retrieval; D-018 reordenou para depois de E-6, e o filtro por keyword foi rejeitado em 2026-09-03 | **Que recuperação ampla por keyword atinge 78,69% da população** (1.477.763 de 1.877.981) — foi esse número que descartou o filtro por keyword. Também as âncoras reais do Codebook |
| [[EXP-003]] | Distribuição de idiomas sob o desenho multilíngue, hoje substituído por D-025 | Linhagem do denominador: 14,21% não inglês pela detecção de idioma dominante, contra 16,333% pela detecção por parágrafo do EXP-013 — a diferença **é** o efeito da correção |
| [[EXP-004]] | Validação entre detectores de idioma | Concordância 0,987 entre `lingua` e `py3langid`. **Concordância, não acurácia** — ressalva que continua valendo |
| [[EXP-005]] | Piloto de 50 casos; substituído pelo desenho de D-026 | Artefato histórico. O formulário cego serviu de molde para os posteriores |
| [[EXP-012]] | PoC do classificador; **não é** a resposta da QI-1 (D-023) | Que o pipeline treino→seleção→inferência em escala funciona, e o custo real. Divergência "melhor em CV" vs "implantado" |

## Instrumentos substituídos

| Arquivo | Substituído por | Nota |
|---|---|---|
| `Classification Prompt (D-026).md` | [[Classification Prompt]] | Esquema de 5 classes do Codebook v2.3. **Produziu o [[EXP-013]]** — é a referência de schema para ler aquelas saídas |
| `Guia do Anotador Humano (D-026).md` | [[Guia do Anotador Humano]] | Idem. Cuidado: mandava preferir a classe **mais baixa** na dúvida, regra que a v2.5 **inverteu** |

## Metodologia e literatura fora de escopo

| Arquivo | Por que saiu |
|---|---|
| `Multilingual Strategy.md` | O próprio cabeçalho declara: superada como desenho principal por D-025. As medições seguem válidas; a camada de idioma virou **filtro**, não eixo de estratificação (L1–L5 não existem mais) |
| `Multilingual Methodology Review.md` | Revisão de literatura para o desenho multilíngue. Volta a ser relevante **se** a população voltar a incluir outros idiomas |

## Reuniões

`2026-08-22 - Pauta para o Orientador.md` — pauta anterior às decisões D-025 a
D-029.

---

## Quando reabrir isto

- **Se D-025 for revisada** (população voltar a incluir outros idiomas):
  `Multilingual Strategy`, `Multilingual Methodology Review`, EXP-003 e EXP-004
  voltam ao caminho crítico.
- **Ao escrever a seção de método:** EXP-001 (denominadores) e EXP-002 (por que
  keyword não filtra) são citação direta.
- **Ao ler `results/_arquivo/`:** o schema daquelas saídas está no
  `Classification Prompt (D-026).md` daqui.
