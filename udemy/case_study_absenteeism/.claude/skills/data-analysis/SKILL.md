---
name: data-analysis
description: Exploratory analysis and supervised ML on tabular datasets in Python. Use when the user wants to explore data, build visualizations, run statistical tests, train a classification or regression model, or answer business questions from a dataset. Triggers on: "analyze this dataset", "explore the data", "distribution of", "correlation between", "predict whether", "classify", "which feature most impacts", "build a model", "evaluate the model".
---

# Skill: Data Analysis and Predictive Modeling

This skill defines the standard analysis workflow and guardrails for tabular data projects.
Load reference files from `references/` on demand — only when relevant to the current task.

## Standard workflow (follow this order)

**1. Understand before transforming**
- `df.shape`, `df.info()`, `df.describe()`, `df.head()`
- Check for missing values, dtypes, and target distribution
- Inspect for class imbalance if the target is categorical

**2. State the question statistically before writing code**
- What is the target? Is it continuous or categorical?
- If binary: how will you define the cutoff and why?
- Which features are likely predictive and which are identifiers to drop?

**3. Transform with checkpoints**
- Always copy to a new variable before modifying: `df_new = df.copy()`
- Confirm it is independent: `df_new is df` must be `False`
- Validate transformed output against a reference when one exists

**4. Model**
- Load `references/ml_pipeline.md` for the classification pipeline
- Load `references/statistics.md` for test selection guidance
- Load `references/datasets.md` for domain-specific column descriptions

**5. Interpret in business terms**
- Report numeric results as returned — no rounding unless requested
- For logistic regression: use odds ratio = exp(coefficient)
- Connect each finding to the original business question

## When to load each reference file

| Situation | Load |
|---|---|
| Questions about columns, types, target definition | `references/datasets.md` |
| Classification or regression task | `references/ml_pipeline.md` |
| Which statistical test to use | `references/statistics.md` |
| Need the CustomScaler implementation | `references/custom_scaler.py` |

## Guardrails

- Never scale dummy variables, one-hot columns, or binary 0/1 flags
- Never re-fit the scaler on new data — `transform` only, using fitted parameters from training
- Never overwrite the raw source file — always work on a copy
- Check assumptions before applying any statistical test (normality, variance homogeneity)
- Report at minimum two metrics for classification: accuracy + one threshold-independent metric (AUC or F1)
