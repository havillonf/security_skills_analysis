---
tipo: taxonomia
questao: QI-2
version: 0.1
data: 2026-08-22
status: PRELIMINAR - primeira passagem, nao validada
---

# Security Taxonomy (emergente)

Taxonomia de `security_concerns` para a [[QI-2 Methodology|QI-2]]. Documento vivo:
cada iteração de open coding acrescenta, funde ou poda códigos, sempre com data.

> [!danger] v0.1 — não é resultado
> Estes códigos vêm de **uma única passagem exploratória sobre 48 skills**, feita
> **por LLM**, sobre uma amostra **estratificada para expor fronteiras** — não
> representativa da população. Servem como *ponto de partida* para o open coding
> humano, nada além disso.
>
> **Nenhuma frequência foi calculada e nenhuma deve ser citada.** LLM não é ground
> truth ([[Decision Log#D-008]]).

Fonte: [[EXP-002]] · `results/EXP-002_sample_preview.md`

---

## Códigos candidatos

Agrupamento conceitual provisório. A hierarquia é tentativa; fusões e divisões são
esperadas.

### G1 — Segurança de aplicação e código

| Código | Evidência observada |
|---|---|
| `injection_flaws` | seção de `code-review`: SQL injection, XSS, CSRF |
| `authn_authz_flaws` | `code-review`: "authentication and authorization flaws" |
| `secrets_in_code` | `code-review`: "secrets or credentials in code" |
| `secure_coding_guidance` | orientação de codificação segura sem procedimento |

### G2 — Identidade, credenciais e criptografia

| Código | Evidência observada |
|---|---|
| `key_management` | `azure-security-keyvault-keys-dotnet` — chaves criptográficas |
| `oauth_flows` | `google-drive-automation` — OAuth standalone |
| `credential_handling` | `zero-to-running`, `clawville` — nível MENTION |

### G3 — Infraestrutura, nuvem e IaC

| Código | Evidência observada |
|---|---|
| `iac_change_risk` | `ywc-iac-author` — Terraform + "blast-radius summary" |
| `infra_operations` | `vm-infrastructure-ops` — troubleshooting de VM GCP |

### G4 — Operações de segurança e resposta

| Código | Evidência observada |
|---|---|
| `malware_analysis` | `performing-malware-ioc-extraction` — extração de IOC |
| `threat_detection` | `ics-monitoring-dragos` — analítica de detecção |
| `threat_intelligence` | `ics-monitoring-dragos` — grupos VOLTZITE, CHERNOVITE |
| `incident_response` | cenários de resposta em `ics-monitoring-dragos` |
| `ransomware_recovery` | `cybersec-testing-ransomware-recovery-procedures` |
| `business_continuity` | RTO/RPO, backup restore, clean restore validation |

### G5 — OT / ICS

| Código | Evidência observada |
|---|---|
| `ot_ics_security` | `ics-monitoring-dragos` — PLCs Schneider/OMRON, OPC UA |

> Grupo inteiramente ausente do OWASP Top 10. Ver [[QI-3 Coverage Methodology]] §2.

### G6 — Governança, risco e conformidade (GRC)

| Código | Evidência observada |
|---|---|
| `third_party_risk` | `draft-vendor-onboarding-questionnaire` — risco de fornecedor |
| `compliance_mapping` | mesmo caso — conformidade em saúde, controles, evidência |

> Segurança como **governança**, não como técnica. Frameworks centrados em
> vulnerabilidade não capturam este grupo.

### G7 — Ecossistema de agentes (candidato, evidência fraca)

| Código | Evidência observada |
|---|---|
| `agent_tool_surface` | `native-mcp` — conexão a servidores MCP, descoberta de tools |
| `skill_supply_chain` | `port-project-codex` — porta skills entre ecossistemas |

> [!warning] Não confundir com o eixo B
> Estes dois casos são provavelmente `NONE`/`MENTION` **como Security Skills** — não
> fazem segurança. Aparecem aqui porque são o *objeto* da análise de segurança da
> própria skill ([[Decision Log#D-007]]). Manter separado: `security_concern`
> descreve sobre o que a skill **atua**, não o que ela **expõe**.

---

## Observações do open coding

1. **`code-review` domina a fronteira `SECONDARY`.** Consistente com [[EXP-001]]:
   nome mais frequente entre as que declaram segurança no front matter.
2. **A amostra é majoritariamente `NONE`/`MENTION`.** Coerente com o pool de
   candidate retrieval cobrir 78,69% dos representantes.
3. **Existe declaração explícita de domínio no front matter** (`domain: cybersecurity`,
   `metadata.category: cybersecurity`) — canal de recuperação potencialmente muito
   mais preciso que keyword. Ver [[EXP-002]].
4. **Há pacotes de skills publicados por fornecedor** ("Anthropic Cybersecurity
   Skills"). Se replicarem muito, poucos autores podem dominar a distribuição de
   concerns — risco direto de confundir **difusão** com **preocupação**.
5. **Multilinguismo é real:** francês, chinês, russo, coreano, italiano e japonês
   apareceram em 48 casos.

## Casos fronteiriços registrados

- `ywc-iac-author` — "blast-radius" é avaliação de risco de mudança. É
  `security_concern` ou qualidade operacional? **Não resolvido.**
- `draft-vendor-onboarding-questionnaire` — GRC conta como segurança sob a definição
  adotada? A definição fala em "sistemas computacionais"; risco de fornecedor é
  organizacional. **Requer decisão.**
- `native-mcp` — superfície de ferramenta do agente sem função de segurança.
- `meta-ads-audit` — homônimo puro (R-5), `NONE`.

## Sobreposições observadas

`ransomware_recovery` ⊂ `business_continuity` · `incident_response`
`threat_detection` ↔ `threat_intelligence` (coocorrem em `ics-monitoring-dragos`)
`credential_handling` ↔ `secrets_in_code` (mesma preocupação, momentos diferentes)

---

## Histórico

| Versão | Data | Mudança |
|---|---|---|
| 0.1 | 2026-08-22 | Semeadura por LLM sobre 48 casos de [[EXP-002]]. Não validada. |

## Ligações

[[QI-2 Methodology]] · [[QI-3 Coverage Methodology]] · [[Codebook]] · [[EXP-002]] ·
[[01 - Research Question]]
