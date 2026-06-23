# Statistical Test Reference

## Test selection guide

| Situation | Test | scipy |
|---|---|---|
| Check normality (n < 50) | Shapiro-Wilk | `stats.shapiro(x)` |
| Check normality (n ≥ 50) | Kolmogorov-Smirnov | `stats.kstest(x, 'norm')` |
| Compare means — 2 groups, normal | t-test (independent) | `stats.ttest_ind(a, b)` |
| Compare means — 2 groups, non-normal | Mann-Whitney U | `stats.mannwhitneyu(a, b)` |
| Compare means — 3+ groups, normal | One-way ANOVA | `stats.f_oneway(*groups)` |
| ANOVA post-hoc | Tukey HSD | `statsmodels.stats.multicomp.pairwise_tukeyhsd` |
| Association between categoricals | Chi-square | `stats.chi2_contingency(table)` |
| Correlation — normal data | Pearson | `stats.pearsonr(x, y)` |
| Correlation — non-normal data | Spearman | `df.corr(method='spearman')` |
| Count/rate events | Poisson | `stats.poisson` |

## Assumptions to verify before parametric tests

1. **Normality** — Shapiro-Wilk or K-S
2. **Variance homogeneity** — Levene: `stats.levene(a, b)`
3. **Independence** — observations must be independent

## Interpreting results

- p < 0.05: reject H₀ at 5% significance (result is statistically significant)
- Always report **effect size** alongside p-value — statistical significance ≠ practical importance
- Right-skewed targets → use **median** as central measure, not mean
- Non-normal data → use **non-parametric tests** (Mann-Whitney, Spearman)

## Quick normality decision

```python
from scipy import stats

stat, p = stats.shapiro(df['column'])
print(f'Shapiro-Wilk: W={stat:.4f}, p={p:.2e}')
if p < 0.05:
    print('Non-normal — use median as cutoff; use non-parametric tests')
else:
    print('Normal — parametric tests applicable')
```
