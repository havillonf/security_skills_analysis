---
tipo: reuniao
data: 2026-08-22
status: pauta - reuniao ainda nao realizada
participantes: Victor Brito, orientador
---

# Pauta para a reunião com o orientador

Documento de preparação. Linguagem de fala, para eu usar como roteiro.
Depois da reunião, registrar o que foi decidido em [[Decision Log]].

---

## 1. Resumo em um minuto

> "Eu estou trabalhando com um dataset chamado GitSkills. Ele tem 3,8 milhões de
> arquivos `SKILL.md` coletados do GitHub em julho de 2026. Uma *agent skill* é uma
> pasta com um arquivo de texto que dá instruções para um agente de IA — tipo o
> Claude Code. O agente lê esse texto e decide sozinho quando usar.
>
> O que me interessa é olhar isso pela lente de segurança. E tem uma coisa que torna
> o objeto interessante para engenharia de software: essas skills são texto em
> linguagem natural, não têm gerenciador de pacotes, não têm assinatura, ninguém
> revisa, e nenhum compilador verifica. É código que roda sem nada disso."

---

## 2. Onde eu estou hoje

O que já está pronto:

- Dataset baixado e conferido. A estrutura bate, as chaves ligam certo, sem
  registros órfãos.
- Um script de perfilamento que qualquer pessoa roda e reproduz todos os números.
- Uma definição escrita do que conta como "skill de segurança", com um codebook.
- Duas metodologias escritas: uma para a QI-2 e uma para a QI-3.
- Um caderno no Obsidian com decisões, experimentos e limitações registrados.

O que **não** está pronto:

- Nenhuma classificação foi feita ainda.
- **Nenhum número de resultado existe.** Nada de "X% das skills são de segurança".
- A questão central não está escolhida — é o principal motivo desta reunião.

---

## 3. Uma coisa que eu preciso contar logo

> "Eu tinha um resultado no notebook inicial dizendo que 1,1% das skills mencionavam
> segurança. Esse número estava errado e eu joguei fora.
>
> O erro foi de amostragem. Eu peguei as 5.000 primeiras linhas do arquivo achando
> que era uma amostra. Não era — as primeiras linhas do arquivo são um bloco
> específico, todas descobertas no mesmo momento, e a maioria nem tinha o texto da
> skill. Tinha um caminho de atalho de sistema, com 42 caracteres.
>
> Quando eu refiz do jeito certo, com as mesmas palavras-chave e no dataset inteiro,
> deu 52,93%. Quarenta e oito vezes maior.
>
> Está tudo registrado. O notebook antigo ficou marcado como legado e eu não uso
> nenhum número dele."

**Por que contar isso:** é honestidade metodológica, e mostra que o processo de
auditoria funcionou. Melhor eu levantar do que ele descobrir depois.

---

## 4. O que eu quero propor: a QI-2 como questão central

> **QI-2 — Que tipos de preocupação de segurança as skills expressam, e como essas
> preocupações se distribuem?**

### Por que eu gostei dessa

- É uma pergunta que **os dados conseguem responder**. Não depende de eu adivinhar
  intenção de ninguém.
- Ela produz uma **taxonomia** — que é uma contribuição concreta, algo que outra
  pessoa pode reusar e citar.
- O paper original do GitSkills lista usos possíveis do dataset, mas **não executa
  nenhum**. Então tem espaço real.
- Ela sustenta a distinção que eu acho mais interessante da pesquisa toda:
  a diferença entre **falar de segurança** e **fazer segurança**.

### Como eu pretendo fazer

De baixo para cima. Eu leio as skills, deixo as categorias surgirem do que está
escrito, e só **depois** comparo com frameworks tipo OWASP.

> "A ordem importa. Se eu começar pelo OWASP, eu vou achar exatamente o que o OWASP
> descreve e vou ficar cego para o resto. Isso seria circular."

E isso já apareceu na prática: numa amostra de 48 skills eu achei uma de segurança
de sistema industrial (ICS/OT, controlador lógico programável) e uma de recuperação
de ransomware. **Nenhuma das duas existe no OWASP Top 10.** Se eu tivesse partido
do OWASP, teria descartado as duas.

### O que eu já fiz da QI-2

- Montei a busca de candidatas e medi o resultado.
- Gerei uma amostra de descoberta com 48 skills, em 4 estratos.
- Fiz uma primeira leitura e rascunhei 7 grupos de categorias.

**Importante dizer:** essa primeira leitura foi feita com apoio de IA e está marcada
como **não validada**. Não é resultado. É ponto de partida para eu ler na mão.

---

## 5. As três coisas que eu preciso decidir com ele

### 5.1 A QI-2 basta como questão central de TCC?

> "Ela é descritiva. Ela gera uma taxonomia e mostra distribuições, mas não testa
> hipótese nem estabelece causa. Isso é suficiente para o TCC? E se a gente pensar
> em artigo depois, precisa de mais alguma coisa junto?"

**Alternativa que eu tenho no bolso, se ele achar pouco:** olhar as **propriedades
estruturais** das skills — quais permissões elas declaram (`allowed-tools`), quantas
empacotam script executável. É mais fácil de medir, não depende de julgamento, e
combina bem com a QI-2 como segundo eixo.

### 5.2 Quem anota, e anota sozinho?

> "Para isso ter validade, o ideal é ter dois anotadores independentes e calcular
> concordância. Se for só eu, isso vira uma limitação que eu tenho que declarar no
> texto. Tem alguém do grupo que poderia anotar uma parte? Ou a gente assume o
> anotador único e declara?"

Isso muda o que eu posso afirmar. Vale decidir antes de eu começar, não depois.

### 5.3 Segurança organizacional entra ou fica de fora?

Apareceu uma skill de questionário de risco de fornecedor — conformidade, contrato,
avaliação de terceiro.

> "Minha definição fala em 'sistemas computacionais'. Risco de fornecedor é
> organizacional, não técnico. Eu incluo isso como segurança ou corto o escopo para
> só o que é técnico?"

Não tem resposta óbvia. Muda o tamanho da população.

---

## 6. Dois riscos que eu preciso avisar

### 6.1 As skills se repetem muito — e isso atrapalha a contagem

> "Eu descobri uma coisa chata. Eu estava deduplicando por hash do conteúdo,
> achando que assim cada texto contava uma vez só.
>
> Mas aí eu olhei as skills que declaram `domain: cybersecurity`. São 13 mil
> conteúdos *diferentes* — só que vêm de **82 repositórios**. E os oito maiores
> donos têm quantidades quase iguais: 746, 743, 707, 688, 675...
>
> Ou seja: é o mesmo pacote de skills copiado entre várias pessoas, com mudancinhas
> mínimas. Muda o hash, mas não é observação independente."

**Por que isso importa:** se eu contar assim, a distribuição de preocupações vai
refletir o que alguns pacotes populares cobrem — não o que a comunidade se preocupa.
Eu estaria medindo **difusão**, não **preocupação**.

**O que eu proponho:** reportar sempre a concentração por repositório e por dono, e
testar deduplicação por similaridade como verificação de robustez — não no caminho
principal, porque isso exigiria escolher um limiar arbitrário.

### 6.2 Tem skill em vários idiomas

Em 48 skills eu vi francês, chinês, russo, coreano, italiano e japonês.

> "Se eu buscar e classificar só em inglês, eu perco essas e nem sei quantas são.
> Eu queria medir isso antes de escalar."

---

## 7. O tamanho do problema (para ele calibrar a expectativa)

- São **1,88 milhão** de conteúdos distintos.
- Buscar por palavra-chave **não filtra**: minha busca ampla pegou **78,69%** deles.
  Quase quatro em cada cinco skills falam de segurança de algum jeito.

> "Não tem atalho. Eu não consigo reduzir isso com regra de texto. O caminho é:
> eu anoto uma amostra na mão, uso isso como gabarito, treino ou valido um
> classificador contra o gabarito, e só então rodo em escala."

E uma coisa que eu não vou abrir mão:

> "IA não é gabarito. Ela pode me ajudar a pré-classificar, mas o padrão-ouro tem
> que ser humano, senão eu estou validando o modelo com ele mesmo."

---

## 8. O que eu faço depois da reunião

Se ele aprovar a QI-2:

1. Piloto de anotação com ~50 skills, focando na fronteira mais difícil — as skills
   em que segurança é parte do trabalho, mas não o objetivo principal (tipo
   `code-review`).
2. Ajustar o codebook conforme o que o piloto mostrar.
3. Medir quantas skills não são em inglês.
4. Aí sim, montar o gabarito e partir para escala.

Duas medições rápidas que eu posso rodar já: a fração de skills não-inglesas e a
concentração por dono no conjunto todo.

---

## 9. Perguntas diretas para levar

1. A QI-2 sozinha basta como questão central, ou você quer um segundo eixo junto?
2. Consigo um segundo anotador, ou assumo anotador único como limitação?
3. Segurança organizacional (risco de fornecedor, conformidade) entra no escopo?
4. Você quer mirar em artigo além do TCC? Isso muda o nível de rigor que eu preciso.
5. Qual o prazo real? A anotação é a parte lenta e eu preciso dimensionar a amostra.
6. Sobre a concentração por dono: eu reporto e sigo, ou você acha que precisa de
   tratamento mais forte?

---

## 10. Decisões pendentes já registradas

Se ele quiser ver o formal, está tudo em [[Decision Log]]:

| ID | Assunto | Estado |
|---|---|---|
| D-009 | Escopo de aplicabilidade da QI-3 | aguarda decisão |
| D-010 | Deduplicação por similaridade | aguarda decisão |
| — | Questão central | **é o assunto desta reunião** |
| — | GRC entra no escopo? | aguarda decisão |

---

## Depois da reunião — preencher

**Decidido:**

**Encaminhamentos:**

**Discordâncias / pontos a revisitar:**

## Ligações

[[00 - Research Overview]] · [[01 - Research Question]] · [[QI-2 Methodology]] ·
[[QI-3 Coverage Methodology]] · [[Codebook]] · [[Security Taxonomy]] ·
[[EXP-001]] · [[EXP-002]] · [[Decision Log]] · [[03 - Methodology]]
