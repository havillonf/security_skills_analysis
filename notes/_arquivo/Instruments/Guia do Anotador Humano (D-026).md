---
tipo: instrumento
questao: QI-1
data: 2026-09-03
decisoes: D-026, D-021
status: proposto — não testado
---

# Guia do anotador humano — o que você precisa saber para classificar

Resumo em linguagem simples do [[Codebook]] v2.3, para quem for fazer a
adjudicação humana prevista em [[Decision Log#D-026]]. Não substitui o
Codebook — é a porta de entrada para quem vai classificar sem querer ler
o documento técnico inteiro primeiro.

> [!important] Quando você entra nesta etapa
> Três modelos de IA classificam cada skill de forma independente. Você só
> vê os casos em que eles **discordaram** em algum ponto — nunca os casos
> em que os três concordaram. Quando você recebe um caso, classifique-o
> **do zero**, sem ver o que nenhum dos três modelos respondeu. Isso evita
> que a resposta de um modelo influencie a sua — o mesmo motivo pelo qual
> os três modelos nunca veem a resposta um do outro. *(Esta é a leitura
> adotada para operacionalizar D-026 — não estava escrita literalmente na
> decisão original; se não for essa a intenção, precisa de correção antes
> de você começar.)*
>
> Sua decisão vale para o **caso inteiro**, não só para o campo em que os
> modelos discordaram.

---

## 1. A pergunta que você está respondendo

Para cada skill, pergunte:

> Essa instrução tem, como propósito principal **ou** como parte real do
> que faz, alguma relação com prevenir, detectar, testar, explorar,
> mitigar ou responder a ameaças, falhas ou violações de segurança em
> **sistemas de computador**?

Duas coisas importantes:

- **Não basta a skill falar sobre segurança.** O que importa é o que ela
  realmente propõe fazer.
- **"Sistemas de computador"** inclui código, aplicações, infraestrutura,
  configuração, contas de acesso, dependências de software, agentes de IA
  e modelos. Não inclui contratos, seguros, políticas de RH ou processos
  organizacionais — mesmo quando a palavra "segurança" aparece neles (ver
  §3.2 abaixo).

---

## 2. As cinco categorias, em linguagem simples

| Categoria | O que significa | Exemplo |
|---|---|---|
| **PRIMARY** | Segurança é o motivo da skill existir. Se tirar a parte de segurança, a skill não faz mais sentido. | Uma skill que analisa malware e extrai indicadores de ataque. |
| **SECONDARY** | Segurança é uma parte real e útil, mas a skill serve principalmente para outra coisa. | Uma skill de revisão de código que, entre várias verificações (estilo, duplicação, design), também procura senhas expostas no código. |
| **MENTION** | A skill só cita segurança de passagem, sem instruir como fazer. | Uma skill de configuração de ambiente que diz "use senhas seguras" numa frase e segue para outro assunto. |
| **NONE** | Não tem nada a ver com segurança de sistemas. | Uma skill que audita campanhas de anúncios no Facebook. |
| **AMBIGUOUS** | Você não tem informação suficiente para decidir com confiança. | O texto é curto demais, genérico demais, ou depende de um arquivo que você não tem acesso. |

**AMBIGUOUS não é "eu não sei" nem preguiça de decidir — é uma resposta
válida e esperada em alguns casos.** É melhor admitir que a evidência não
alcança do que forçar uma categoria.

---

## 3. Perguntas que ajudam a decidir

### 3.1 O teste da remoção e o teste do "o que fazer"

- **Se eu apagasse tudo que fala de segurança, a skill continuaria fazendo
  sentido?**
  - Não → **PRIMARY**.
  - Sim, mas perderia uma parte útil e concreta → **SECONDARY**.
  - Sim, ficaria praticamente igual → **MENTION** ou **NONE**.
- **O texto diz o que fazer** — um passo a passo, um comando, uma
  ferramenta a rodar, um critério de decisão — **ou só avisa/recomenda em
  uma frase?**
  - Diz o que fazer → pode ser PRIMARY ou SECONDARY.
  - Só avisa → no máximo **MENTION**.
- **Segurança é uma entre várias partes da skill, todas mais ou menos do
  mesmo tamanho e importância?** → **SECONDARY**. **Segurança domina o
  texto e organiza a skill inteira?** → **PRIMARY**.

### 3.2 GRC — governança, risco e conformidade

Esse é o caso mais fácil de errar. Regra: **só conta como segurança
quando a skill realmente inspeciona configuração, código ou
infraestrutura.**

- **Conta:** revisar permissões de acesso, checar configuração contra um
  guia técnico, avaliar risco de uma dependência de software.
- **Não conta:** questionário de fornecedor sobre contrato, seguro,
  sanções, continuidade de negócio — mesmo que a palavra "segurança"
  apareça no meio da lista de tópicos. Isso é **NONE**, não MENTION.
- **Caso misto:** se uma parte do documento realmente pede evidência
  técnica (ex.: certificação de criptografia, MFA), classifique pela parte
  técnica, com confiança baixa.

### 3.3 Palavra parecida, sentido diferente (homônimos)

Leia o contexto, nunca a palavra isolada:

- **"Audit"** pode ser auditoria de marketing/anúncios, não de segurança.
- **"Token"** costuma ser token de contexto de um modelo de IA, não
  token de autenticação.
- **"Permission"** pode ser permissão de arquivo do sistema operacional,
  não controle de acesso de segurança.

### 3.4 Scripts e arquivos que a skill usa mas você não vê o conteúdo

Se a skill descreve um comportamento de segurança mas depende de um
arquivo (script, wordlist, template) que não está disponível para você
ler, e isso muda o que você classificaria: use **AMBIGUOUS**, não tente
adivinhar o conteúdo do arquivo.

### 3.5 Idioma nunca decide a classe

A amostra que chega até você deveria ser 100% em inglês (ver
[[Decision Log#D-025]]). Se, ainda assim, você perceber que uma skill não
está em inglês (ou tem uma frase substancial em outro idioma no meio),
classifique normalmente pelas regras acima — **o idioma nunca é motivo
para marcar AMBIGUOUS** — e avise separadamente que aquele caso pode ter
vazado o filtro de amostragem. Isso é um problema do desenho da amostra,
não da classificação em si.

---

## 4. O que anotar, além da categoria

- **Uma frase curta** explicando por que você decidiu assim — o suficiente
  para outra pessoa entender sua decisão sem perguntar.
- Se o caso ficou **na fronteira entre SECONDARY e MENTION**, marque isso
  explicitamente — é a distinção mais importante desta pesquisa (é ela
  que muda o resultado final).
- Se a skill envolve **governança/risco/conformidade** (§3.2), marque
  isso também, mesmo quando a resposta final for NONE.

---

## 5. Quando ficar em dúvida

Prefira classificar na categoria **mais baixa** com confiança baixa a
forçar uma categoria mais alta sem ter certeza. Uma resposta honesta e
mais cautelosa vale mais do que uma resposta confiante e errada.

---

## 6. Onde ver mais detalhes

Este guia é um resumo para decidir rápido. A referência completa — todas
as regras numeradas (R-1 a R-11), mais exemplos reais do próprio dataset —
está em [[Codebook]] v2.3. Em caso de dúvida real entre este guia e o
Codebook, o Codebook é a fonte de verdade.

## Ligações

[[Codebook]] · [[Decision Log]] (ver D-026, D-021) ·
[[Classification Prompt (D-026)]]
