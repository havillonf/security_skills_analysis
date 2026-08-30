---
tipo: hipóteses
atualizado: 2026-08-22
status: nenhuma testada
---

# Hipóteses

> [!danger] Nenhuma hipótese abaixo foi testada
> São conjecturas formuladas a partir do profiling ([[EXP-001]]) e da leitura do
> material. Estão registradas **antes** de qualquer teste, para que a análise seja
> confirmatória e não um exercicio de encontrar padrão depois do fato.
> Nenhuma foi definida pelo pesquisador.

Cada uma traz o que a falsificaria - se não há resultado capaz de refutar, não é
hipótese.

---

## H-1 - Segurança e majoritariamente acessoria, não propósito

**Enunciado.** Entre as skills que mencionam segurança, a maioria trata segurança
como um item entre outros, não como propósito central.

**Motivação.** 52,93% mencionam alguma keyword; 4,09% declaram no front matter -
fator ~13x. E o nome mais frequente entre as que declaram e `code-review` (1.292
conteúdos), revisão genérica.

**Falsificação.** Anotação manual de amostra aleatória mostrando maioria com
propósito central de segurança.

**Status.** Não testada. Requer codebook e amostra anotada.

---

## H-2 - Keywords de alta frequência são dominadas por sentido não-segurança

**Enunciado.** `token`, `audit` e `permission` aparecem majoritariamente em sentido
alheio a segurança (token de LLM, log de auditoria, permissão de arquivo).

**Motivação.** `token` em 20,69% - implausível como token de autenticação nessa
escala, dado que agent skills falam constantemente de janela de contexto e custo.

**Falsificação.** Amostra anotada em que a maioria das ocorrências esteja em sentido
de segurança.

**Status.** Não testada. Barata e de alto valor: decide se keyword serve para
triagem. **Fazer cedo.**

---

## H-3 - Skills com scripts concentram superficie de risco

**Enunciado.** Os 11,4% de representantes com `has_scripts = 1` concentram
desproporcionalmente padrões de execução de comando e acesso de rede.

**Motivação.** Skill de texto puro só influência o agente por instrução; skill com
script carrega código executável. Superficies diferentes por natureza.

**Falsificação.** Ausência de diferenca entre os grupos, ou padrões de execução
igualmente presentes no corpo das skills sem script.

**Status.** Não testada. **Confundidor óbvio:** skills com script tendem a ser
maiores e mais elaboradas. Controlar por `body_chars`.

---

## H-4 - Permissões declaradas são mais amplas que o necessário

**Enunciado.** Entre skills que declaram `allowed-tools`, uma parcela relevante
declara escopo mais amplo do que o corpo da skill de fato exige.

**Motivação.** Padrão conhecido em ecossistemas de permissão (extensões de browser,
apps mobile): declara-se o mais amplo por conveniência.

**Falsificação.** Escopo declarado alinhado ao uso descrito na maioria dos casos.

**Status.** Não testada. **Dificuldade seria:** "necessário" exige julgamento; o
critério precisa de codebook antes de qualquer medição, senao vira circular.

---

## H-5 - Cópias divergentes ampliam capacidade mais do que reduzem

**Enunciado.** Quando cópias de um mesmo conteúdo ancestral divergem, a divergência
introduz execução/rede mais frequentemente do que remove.

**Motivação.** E o analogo de supply chain que o paper do GitSkills sugere.

**Falsificação.** Simetria entre introdução e remoção, ou divergência dominada por
edição trivial (formatação, tradução, renomeação).

**Status.** Não testada. **Ressalva que pode inviabilizar:** exige direção temporal,
disponível só para os 458.548 arquivos com histórico, subconjunto MNAR enviesado
para locais padrão. Sem direção, a hipótese não é testável como enunciada.
Resultado mais provável e descritivo, não causal.

---

## H-6 - Convenções de segurança estão emergindo no front matter

**Enunciado.** Campos fora da spec original (`risk`, `disable-model-invocation`,
`user-invocable`) aparecem de forma não trivial, indicando convenção emergente de
controle de risco.

**Motivação.** Numa amostra de 2.000 com front matter valido: `allowed-tools` 205,
`user-invocable` 99, `disable-model-invocation` 60, `risk` 55.

**Falsificação.** Esses campos concentrados em poucos repositórios ou cópias de um
único template - convenção aparente sendo artefato de duplicação.

**Status.** Não testada. **Verificar concentração por repo/dono antes de qualquer
afirmação** - dado que 60,8% das ocorrências são cópias, e um risco real.

---

## Nota

Testar as seis multiplica comparações e infla falso positivo. Antes de qualquer
teste: escolher quais são **confirmatórias** (declaradas a priori, com correção para
múltiplas comparações) e quais ficam **exploratorias** (reportadas como tal, sem
p-valor apresentado como evidência).

## Ligações

[[01 - Research Question]] · [[EXP-001]] · [[Decision Log]] · [[03 - Methodology]]
