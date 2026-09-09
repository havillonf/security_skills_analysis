---
tipo: literatura
leitura: misto — ver por item
usado-em: scripts/compute_agreement.py, Codebook v2.5 sec.8, EXP-014
---

# Coeficientes de concordancia — o canone

Conjunto que sustenta `scripts/compute_agreement.py`. Agrupadas porque sao
usadas **juntas**: a decisao do projeto e reportar todas e mostrar que
convergem, em vez de escolher uma.

## Por que varias, e nao uma

Nenhum coeficiente e suficiente sozinho, e cada um falha de um jeito
diferente. Convergencia entre coeficientes com pressupostos distintos e
argumento mais forte que qualquer um isolado — e blinda contra a pergunta
*"por que voce escolheu justo esse?"*.

---

## Cohen's kappa

**Cohen (1960).** Padrao de facto para dois avaliadores, categorias nominais.
Corrige acaso pelas marginais de cada avaliador.

**Fraqueza:** o *paradoxo do kappa* — com marginais desbalanceadas, kappa
despenca mesmo com concordancia bruta alta.

## Krippendorff's alpha

**Hayes & Krippendorff (2007)** — `hayes2007answering`, verificada.

> [!note] O livro *Content Analysis* (Krippendorff) foi descartado
> O projeto usa Krippendorff **apenas como coeficiente**. Para isso, a
> referencia canonica e o artigo de 2007, e o guia aplicado a engenharia
> de software e `sequeira2020krippendorff`. A metodologia do livro nao e
> usada em lugar nenhum — o argumento de unidades nao codificaveis vem do
> GAO e do Lombard. Citar o livro exigiria escolher a edicao (2a/3a/4a),
> e nao ha ganho.
Padrao-ouro da analise de conteudo. Generaliza para qualquer numero de
avaliadores, dados faltantes e niveis de medida. Krippendorff argumenta
explicitamente que alpha deve substituir kappa.

Guia aplicado a engenharia de software, util por ser do nosso campo:
https://arxiv.org/pdf/2008.00977

## Gwet's AC1

**Gwet (2008).** Projetado para corrigir o paradoxo do kappa; usa probabilidade
de acaso que nao colapsa sob prevalencia extrema.

**Contestado.** Ha literatura recente argumentando que AC1 **nao** e substituto
para kappa: *"Gwet's AC1 is not a substitute for Cohen's kappa"* —
https://www.researchgate.net/publication/370676423

Por isso a postura no projeto nao e escolher um vencedor: e reportar os dois e
usar a **diferenca entre eles como diagnostico**. No [[EXP-014]] kappa=0,724 e
AC1=0,776 ficaram quase colados, mostrando que o paradoxo **nao** distorce
nossos dados.

## Brennan-Prediger

**Brennan & Prediger (1981).** Correcao por acaso assumindo distribuicao
uniforme. Robusto a prevalencia, mas depende do numero de categorias.

## O paradoxo do kappa e seus diagnosticos

**Feinstein & Cicchetti (1990)**, *High agreement but low kappa: the problems
of two paradoxes* — https://www.researchgate.net/publication/20808295

Dois paradoxos: (1) kappa baixo com concordancia alta; (2) marginais
desbalanceadas produzindo kappa **maior** que marginais equilibradas.
Consequencia operacional adotada: **nunca reportar kappa sem a concordancia
bruta ao lado.**

**Byrt, Bishop & Carlin (1993)**, *Bias, prevalence and kappa*.
Definem **indice de prevalencia (PI)** e **indice de vies (BI)**, que
diagnosticam *por que* kappa esta deprimido. No EXP-014: PI=0,20 e BI=0,12 —
desbalanceamento moderado, longe do regime patologico.

Revisao acessivel: *High Agreement and High Prevalence: The Paradox of Cohen's
Kappa* — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5712640/

## Qual coeficiente e qual IC usar

**Zapf et al. (2016)**, *BMC Medical Research Methodology* —
https://link.springer.com/article/10.1186/s12874-016-0200-9

Para dados nominais completos, Fleiss' K e Krippendorff's alpha **com IC por
bootstrap** sao igualmente adequados; com dados faltantes ou ordem superior,
alpha e o recomendado. **E a citacao que justifica termos reportado IC
bootstrap.**

## Faixas de interpretacao

**Landis & Koch (1977).** <=0,20 leve · 0,21-0,40 sofrivel · 0,41-0,60 moderada
· 0,61-0,80 substancial · >0,80 quase perfeita.

Sao **convencao, nao lei** — usar como referencia comunicativa, sempre com o
valor e o IC ao lado.

## McNemar

**McNemar (1947).** Testa se a discordancia e **sistematica** (um avaliador
sobe consistentemente) ou simetrica. Coeficientes de concordancia nao fazem
essa distincao.

No [[EXP-014]]: **p=0,0042**, 14 casos contra 2 — vies direcional que
sobreviveu a mudanca de esquema. Sem este teste, o achado ficaria invisivel.

## Ressalva geral

Os classicos (Cohen, Landis & Koch, Feinstein, Byrt, Gwet, Krippendorff,
McNemar) entraram no projeto **via implementacao e via resumo**, nao por
leitura direta dos originais. As formulas em `compute_agreement.py` estao
corretas e verificadas, mas **para citar no TCC, ler os originais** — sao todos
curtos e canonicos.

## Ligacoes

[[EXP-014]] · [[Codebook]] · [[Classification and Sampling Precedents]]
