# Referência de testes estatísticos

## Quando usar cada teste

| Situação | Teste | Python |
|---|---|---|
| Verificar normalidade | Shapiro-Wilk (n < 50) ou K-S | `stats.shapiro()` / `stats.kstest()` |
| Comparar médias — 2 grupos, normal | t de Student | `stats.ttest_ind()` |
| Comparar médias — 2 grupos, não normal | Mann-Whitney | `stats.mannwhitneyu()` |
| Comparar médias — 3+ grupos, normal | ANOVA | `stats.f_oneway()` |
| ANOVA com post-hoc | Tukey | `statsmodels.stats.multicomp.pairwise_tukeyhsd()` |
| Associação entre variáveis categóricas | Qui-quadrado | `stats.chi2_contingency()` |
| Eventos raros / contagens | Poisson | `stats.poisson` |

## Premissas a verificar antes de aplicar testes paramétricos
1. Normalidade (Shapiro-Wilk)
2. Homogeneidade de variâncias (Levene: `stats.levene()`)
3. Independência das observações

## Para este dataset de absenteísmo
- 'Absenteeism Time in Hours': **não normal** (Shapiro-Wilk p ≈ 1e-42)
  → usar mediana como ponto de corte, não média
  → comparações entre grupos: Mann-Whitney, não t de Student
- Variáveis categóricas (Reason groups, Education): qui-quadrado para associação com target
- Correlação entre numéricas: Spearman (não Pearson) dado a não normalidade
  ```python
  df[colunas_numericas].corr(method='spearman')
  ```
