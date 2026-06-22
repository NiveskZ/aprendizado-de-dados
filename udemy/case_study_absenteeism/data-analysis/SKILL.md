---
name: data-analysis
description: Análise exploratória e modelagem preditiva em Python para datasets tabulares. Use quando o usuário pedir para analisar dados, explorar um dataset, criar visualizações, construir um modelo ou responder perguntas de negócio a partir de dados. Acionado por: "analisa esse dataset", "explora os dados", "qual a distribuição de", "correlação entre", "prevê", "classifica", "qual feature mais impacta".
---

# Skill: Análise de Dados e Modelagem Preditiva

Esta skill define o fluxo padrão de análise e os datasets disponíveis neste projeto.
Carrega detalhes do domínio sob demanda a partir de `references/`.

## Fluxo padrão (siga esta ordem)

1. **Entender os dados primeiro** — sempre antes de qualquer transformação
   - `df.shape`, `df.info()`, `df.describe()`, `df.head()`
   - Verificar valores ausentes e tipos
   - Inspecionar a distribuição da variável-alvo

2. **Formular a pergunta em termos estatísticos** antes de escrever código
   - Definir o que é "sucesso" para este dataset (ex: mediana como ponto de corte)
   - Verificar premissas antes de aplicar qualquer teste

3. **Transformar com checkpoints**
   - Sempre copiar para nova variável antes de modificar: `df_novo = df.copy()`
   - Verificar que é um objeto independente: `df_novo is df` deve ser `False`

4. **Modelar**
   - Ver `references/datasets.md` para conhecer as features disponíveis
   - Ver `references/ml_pipeline.md` para o pipeline padrão de classificação

5. **Interpretar em linguagem de negócio**
   - Resultados numéricos sem arredondamento, exatamente como retornados
   - Odds ratio para regressão logística: exp(coeficiente)
   - Conectar cada achado ao problema de negócio original

## Quando carregar referências adicionais

- Perguntas sobre colunas, tipos ou significado das features → ler `references/datasets.md`
- Tarefa de ML (classificação, regressão) → ler `references/ml_pipeline.md`
- Dúvida sobre qual teste estatístico usar → ler `references/estatistica.md`

## Regras de produção

- Nunca escalar variáveis dummy ou flags binárias (0/1)
- Nunca re-ajustar o scaler em dados novos: apenas `transform`, nunca `fit`
- Nunca sobrescrever o CSV bruto original
- Preferir `SELECT` (leitura) antes de qualquer operação destrutiva
