---
tipo: metodologia
questao: QI-3
data: 2026-08-22
status: proposta; bloqueada por QI-2
atualizado: 2026-09-23
status: Proposta formalizada; sequenciada após a saturação da QI-2 (D-024)
---

# QI-3 — Metodologia de cobertura
# QI-3 — Metodologia de Cobertura e Análise de Lacunas (Gap Analysis)

> **QI-3. Que lacunas existem — o que as skills de segurança não cobrem?**
> **QI-3 (Gap Analysis / Conformidade). Quais lacunas existem entre as preocupações de segurança manifestadas nas skills e os frameworks consagrados de segurança de software (OWASP Top 10 e OWASP Top 10 for LLM)?**

> [!warning] Bloqueada por desenho
> A QI-3 **não pode começar** antes de a taxonomia empírica da
> [[QI-2 Methodology|QI-2]] estar razoavelmente estabilizada. Antecipar o crosswalk
> contamina a QI-2 com categorias externas e produz circularidade.
> [!warning] Sequenciamento Metodológico — Bloqueada por Desenho
> A QI-3 **não pode começar** antes de a taxonomia empírica da [[QI-2 Methodology|QI-2]] atingir estabilização e saturação teórica. Realizar o *crosswalk* antes contaminaria a análise qualitativa da QI-2 com categorias externas, induzindo circularidade.
>
> Desde [[Decision Log#D-024]] (2026-08-27), isso é parte de uma cadeia
> formal e sequenciada: **QI-1 → validação do classificador → QI-2 → QI-3**.
> Como QI-2 já depende do classificador de QI-1 estar validado, a QI-3 herda
> essa dependência **transitivamente** — não começa antes de QI-2 estabilizar
> e QI-2 não começa antes do gate de E-7.
> A sequência inegociável da pesquisa é: **QI-1 (Prevalência) → QI-2 (Taxonomia Empírica Bottom-Up) → QI-3 (Gap Analysis Top-Down)**.

---

## 1. Por que é metodologicamente diferente da QI-2
## 1. Direção Metodológica: Bottom-Up vs. Top-Down

| | QI-2 | QI-3 |
| Dimensão | QI-2 (Tipologia) | QI-3 (Gap Analysis) |
|---|---|---|
| Direção | bottom-up | top-down |
| Pergunta | o que existe nos dados? | o que se esperaria encontrar e não encontramos? |
| Fonte das categorias | os próprios dados | referenciais externos |
| Risco principal | deriva do codebook | circularidade e falsa lacuna |
| **Direção** | Bottom-up (indutiva) | Top-down (dedutiva / comparativa) |
| **Pergunta** | O que existe nos dados do ecossistema? | O que se esperaria encontrar com base nos frameworks e não encontramos? |
| **Fonte das categorias** | As próprias skills observadas | Referenciais consolidados de mercado |
| **Risco metodológico** | Deriva de conceitos | Encaixe forçado e falsa lacuna |

As duas etapas **não se misturam**. QI-2 termina antes de QI-3 começar.

---

## 2. Referencial externo
## 2. Referenciais Externos Adotados

Escolha **justificada**, não exaustiva. Não usar todos os frameworks disponíveis por
completude.
Para avaliar a completude das preocupações de segurança em software no contexto de agentes, adotam-se dois referenciais canônicos da OWASP:

Candidatos a avaliar quando a QI-2 estabilizar:
| Framework | Escopo no Estudo | O que Permite Observar |
|---|---|---|
| **OWASP Top 10 (Web/Software Tradicional)** | Componentes convencionais de software (APIs, banco, autenticação, controle de acesso) | Presença ou negligência de falhas clássicas (Broken Access Control, Injection, Cryptographic Failures) |
| **OWASP Top 10 for LLM Applications** | Camada agêntica e interfaces com modelos de IA | Proteção contra ameaças emergentes específicas (Prompt Injection, Insecure Output Handling, Sensitive Information Disclosure) |

| Framework | A que tipo de skill se aplica | O que permite observar | Limitação |
|---|---|---|---|
| OWASP Top 10 | skills sobre aplicações web | vulnerabilidades de aplicação clássicas | não cobre agente/LLM, nem infra/OT |
| OWASP Top 10 for LLM/GenAI | skills que lidam com LLM | prompt injection, data leakage, model risks | ecossistema recente, categorias em evolução |
| OWASP Top 10 for Agentic Applications | skills sobre agentes/ferramentas | uso indevido de ferramenta, autonomia | muito recente; estabilidade a verificar |
| MITRE ATLAS | skills sobre ameaças a sistemas de ML | táticas e técnicas adversariais | orientado a ameaça, não a prática de dev |
| NIST CSF (funções) | transversal | PREVENT/DETECT/RESPOND/RECOVER | alto nível; pouca granularidade de concern |

Para cada framework efetivamente adotado, registrar em `notes/Literature/`: por que
foi escolhido, a que subconjunto de skills se aplica, o que permite observar, e suas
limitações. **Fontes primárias/oficiais**; nunca blog como sustentação principal.
Não inventar referência.

> Sinal empírico preliminar ([[EXP-002]]): a amostra de descoberta trouxe
> `cybersec-testing-ransomware-recovery` e `ics-monitoring-dragos` — recuperação de
> ransomware e monitoramento ICS/OT. **Nenhum dos dois tem correspondência no OWASP
> Top 10.** Indício inicial de que um único framework não cobre o objeto. Observação
> de 48 casos, não conclusão.

---

## 3. Aplicabilidade antes de cobertura
## 3. Escopo de Aplicabilidade antes da Cobertura

> [!danger] Nunca use todas as Security Skills como denominador
> Calcular lacuna sobre a população inteira produz "lacuna" artificial: prompt
> injection não é esperado numa skill que não interage com LLM; SQL injection não é
> esperado numa skill que nunca toca banco relacional.
> [!danger] Risco de Falsa Lacuna: Denominador Incorreto
> Calcular a lacuna de um risco sobre a totalidade das skills gera conclusões artificiais: por exemplo, *Prompt Injection* não é aplicável a uma skill que apenas manipula consultas SQL tradicionais sem uso de LLMs; *SQL Injection* não é aplicável a uma skill estritamente de estilização CSS.

O denominador correto é condicional:
O cálculo de cobertura para cada preocupação $P$ deve ser estritamente condicional:

```text
        skills que cobrem a preocupação P
────────────────────────────────────────────────
   skills às quais P é aplicável (escopo de P)
```
$$\text{Taxa de Cobertura}(P) = \frac{\text{Skills que tratam } P}{\text{Skills às quais } P \text{ é tecnicamente aplicável}}$$

e **não**:
O escopo de aplicabilidade de $P$ é derivado dos atributos técnicos e do objetivo funcional anotados na QI-1 e na QI-2.

```text
        skills que cobrem a preocupação P
────────────────────────────────────────────────
            todas as Security Skills
```

### 3.1 Como determinar aplicabilidade

Aplicabilidade é uma **classificação própria**, com o mesmo rigor da classe
principal — não um filtro improvisado. Proposta:

1. Para cada preocupação `P` do crosswalk, definir por escrito o **escopo de
   aplicabilidade**: que características tornam `P` esperável numa skill.
2. Derivar o escopo de atributos **já anotados** na QI-2 (concern, capability,
   artefato-alvo), não de nova leitura ad hoc — assim a aplicabilidade herda a
   validação da QI-2.
3. Registrar `applicability` por par (skill, P): `applicable` · `not_applicable` ·
   `uncertain`.
4. `uncertain` entra no relatório, nunca é silenciosamente somado a nenhum lado.
5. Validar a regra de aplicabilidade numa amostra anotada, como qualquer outro
   instrumento.

**Decisão pendente de aprovação humana:** o escopo de aplicabilidade é subjetivo e
determina o denominador de toda a QI-3. Deve ser aprovado explicitamente antes do
cálculo — ver [[Decision Log#D-009]].

---

## 4. Níveis de cobertura
## 4. Procedimento de Crosswalk (Mapeamento de/para)

Binário `covered`/`not covered` é insuficiente. Escala proposta:
Uma vez concluída a taxonomia da QI-2, realiza-se o mapeamento bidirecional:

| Nível | Leitura |
|---|---|
| `STRONG_COVERAGE` | preocupação tratada com função e capacidade operacional explícitas |
| `MODERATE_COVERAGE` | tratada, com menos especificidade ou sem operacionalização clara |
| `LIMITED_COVERAGE` | aparece de forma marginal ou apenas como menção |
| `NO_OBSERVED_COVERAGE` | não observada segundo os critérios adotados |
| `UNCERTAIN` | evidência insuficiente |
| `NOT_APPLICABLE` | fora do escopo de aplicabilidade |

Os limiares **não podem ser arbitrários**. Se forem quantitativos:

1. propor ao menos duas alternativas;
2. justificar cada uma;
3. rodar **sensitivity analysis**;
4. verificar explicitamente se as conclusões mudam quando o limiar muda;
5. reportar o intervalo de variação junto do resultado.

Se uma conclusão só vale sob um limiar específico, **isso é o achado** — e deve ser
reportado, não escondido.

---

## 5. Crosswalk

Mapeamento explícito entre a taxonomia empírica e os referenciais externos.

Relações admitidas: **1:1 · 1:N · N:1 · sem correspondência**.

Regras:

- **Não force** uma categoria empírica a caber em OWASP/MITRE sem equivalência
  semântica adequada. Encaixe forçado destrói o resultado.
- Categorias empíricas **sem correspondência externa** são resultado importante:
  sugerem preocupações próprias do ecossistema de Agent Skills que os frameworks
  ainda não capturam.
- Categorias externas **sem correspondência empírica** são o material da QI-3
  propriamente dita — candidatas a lacuna, sujeitas às ressalvas da §6.
- O crosswalk é versionado e datado; mudanças posteriores registradas.

---

## 6. Linguagem para "lacunas"

> [!danger] Ausência de evidência não é evidência de ausência
> Zero ocorrências **nunca** é prova de inexistência.

Evitar: *"As skills não cobrem X."*

Preferir: *"Não foi observada cobertura explícita de X segundo os critérios
adotados"*, ou *"X apresentou cobertura limitada entre as skills para as quais o
risco foi considerado aplicável."*

Para **toda** ausência observada, considerar e registrar as cinco explicações
concorrentes:

1. a preocupação realmente não está coberta;
2. está descrita com outra terminologia (inclusive em outro idioma);
3. o método de classificação não a identificou;
4. não é aplicável àquela população;
5. a informação está em bundled artifacts ainda não examinados
   (`composition_truncated = 1` em 13,4% dos representantes).

Só é possível afirmar (1) depois de descartar as outras quatro com evidência. Se não
foram descartadas, o resultado é "não observada", não "ausente".

---

## 7. Resultado combinado QI-2 + QI-3

```text
 o que desenvolvedores de skills fazem
              │  QI-2 (bottom-up)
              ▼
      taxonomia empírica
              │  crosswalk
              ▼
      expectativa externa
              │  QI-3 (top-down)
              ▼
 cobertura forte / moderada / limitada /
 não observada / incerta / não aplicável
    Taxonomia Empírica (QI-2)                  Frameworks (OWASP)
   ┌────────────────────────┐                ┌───────────────────────┐
   │ Códigos e Dimensões    │◄──────────────►│ OWASP Top 10          │
   │ Emergentes dos Dados   │   Crosswalk    │ OWASP for LLM         │
   └────────────────────────┘                └───────────────────────┘
               │                                         │
               ▼                                         ▼
   Categorias Empíricas Sem                  Requisitos de Segurança Sem
   Equivalente Externo:                      Correspondência Empírica:
   -> Especificidades de Agent Skills        -> LACUNAS REAIS DE MERCADO (GAP)
```

Contribuições **potenciais** — hipóteses, não conclusões:
### Regras de Mapeamento:
1. **Não forçar equivalências:** Relações podem ser $1:1$, $1:N$, $N:1$ ou **sem correspondência**. Forçar categorias externas sem aderência semântica mascara os achados.
2. **Achados Positivos Próprios:** Categorias identificadas na QI-2 que não constam na OWASP evidenciam salvaguardas nativas de agentes ainda não padronizadas.
3. **Lacunas Reais:** Riscos críticos da OWASP com aplicabilidade clara na amostra, mas sem menção de proteção nas skills, constituem as lacunas principais reportadas na pesquisa.

- a distância entre **segurança mencionada** e **segurança operacionalizada**;
- preocupações reconhecidas por frameworks externos com pouca ou nenhuma
  correspondência observada nas skills relevantes;
- preocupações do ecossistema de Agent Skills sem correspondência em framework
  algum.

Nenhuma dessas pode ser assumida antes da análise.

---

## 8. Estado atual
## 5. Linguagem Científica para Relato de Lacunas

⬜ Não iniciada, por desenho. Depende de [[QI-2 Methodology|QI-2]] estabilizada,
que por sua vez depende do gate de validação do classificador de QI-1
([[Decision Log#D-024]]).
Conforme preceito empírico, a ausência de registro nas skills examinadas **não é prova de inexistência absoluta**.
- Evitar afirmações absolutistas: *"As skills de agentes não protegem contra X"*.
- Utilizar formulações defensáveis: *"Não foi observada menção ou implementação de defesas para X entre as skills nas quais o risco era diretamente aplicável"*.

O único insumo já produzido é o sinal preliminar da §2 (ransomware recovery e ICS/OT
sem correspondência no OWASP Top 10), a partir de 48 casos de descoberta.

## Ligações

[[01 - Research Question]] · [[QI-2 Methodology]] · [[Security Taxonomy]] ·
[[Codebook]] · [[EXP-002]] · [[03 - Methodology]] · [[Decision Log]]
[[01 - Research Question]] · [[QI-1 Methodology]] · [[QI-2 Methodology]] · [[Codebook]] · [[Security Taxonomy]] · [[Decision Log]]
