---
name: ml-pipeline
description: Build a supervised classification pipeline in Python following a consistent, production-minded workflow. Use when the user wants to train a classifier (logistic regression, tree-based, etc.) from a tabular dataset, including target creation by cutoff, scaling only numerical features, train/test split, fitting, and an odds-ratio / coefficient interpretation table. Triggers on "build a classification model", "logistic regression", "train a classifier", "predict whether", "ML pipeline for this dataset".
---

# ML classification pipeline

A repeatable workflow for supervised binary classification on tabular data. Follow these
steps in order. Adapt details to the dataset, but keep the structure and the guardrails.

## Step 1 — Understand the data first

Before any transformation:
- `df.shape`, `df.info()`, `df.describe()`, `df.head()`
- Check for missing values and dtypes
- Inspect the target's distribution. If it is skewed/non-normal (check with
  Shapiro-Wilk for small samples), prefer the **median** over the mean for any cutoff.

## Step 2 — Define the target

If the raw target is continuous and you need a binary class, use a cutoff and state the
logic as a comment:

```python
targets = np.where(df['target_col'] > df['target_col'].median(), 1, 0)
```

Always check balance: `targets.sum() / targets.shape[0]`. Aim for roughly 40-60% — a
balanced target is what makes plain accuracy a trustworthy metric. If badly imbalanced,
note it and consider stratified split, class weights, or AUC/F1 over accuracy.

## Step 3 — Select inputs with a checkpoint

Drop the target and any features known to be non-predictive. Create a checkpoint by
copying to a new variable (never in-place) and verify it is a distinct object:

```python
data_with_targets = df.drop(['target_col', ...], axis=1)
data_with_targets is df   # must be False
```

## Step 4 — Scale ONLY numerical features

Never scale dummy variables, one-hot columns, or binary 0/1 flags — it is meaningless and
distorts coefficient interpretation. Use an explicit omit-list:

```python
columns_to_omit = ['dummy_1', 'dummy_2', 'binary_flag']
columns_to_scale = [c for c in inputs.columns if c not in columns_to_omit]
```

A CustomScaler that wraps StandardScaler and only touches selected columns is preferred,
because it returns a DataFrame (keeps column names) and can be pickled with the model.
See `references/custom_scaler.py` for a ready implementation.

## Step 5 — Split before fitting the scaler

Fit the scaler on training data conceptually, then split. Always set `random_state` for
reproducibility:

```python
x_train, x_test, y_train, y_test = train_test_split(
    scaled_inputs, targets, test_size=0.2, random_state=20)
```

Never fit the scaler on the full dataset including test rows — that leaks information.

## Step 6 — Fit and get a baseline accuracy

```python
reg = LogisticRegression(max_iter=1000)
reg.fit(x_train, y_train)
reg.score(x_train, y_train)
```

## Step 7 — Interpret coefficients (the real deliverable)

For logistic regression, build an odds-ratio table — this is what a business stakeholder
actually reads:

```python
summary = pd.DataFrame(columns=['Feature'], data=inputs.columns.values)
summary['Coefficient'] = np.transpose(reg.coef_)
summary.index += 1
summary.loc[0] = ['Intercept', reg.intercept_[0]]
summary = summary.sort_index()
summary['Odds_ratio'] = np.exp(summary.Coefficient)
summary.sort_values('Odds_ratio', ascending=False)
```

Odds ratio > 1 increases the odds of the positive class; < 1 decreases them. Interpret
the top features in plain business language.

## Step 8 — Evaluate honestly

Accuracy alone is not enough. Always report:
- Test accuracy: `reg.score(x_test, y_test)`
- Confusion matrix: `metrics.confusion_matrix(y_test, y_pred)`
- A threshold-independent metric: `metrics.roc_auc_score(y_test, reg.predict_proba(x_test)[:,1])`

## Step 9 — Save for deployment

Pickle the model AND the fitted scaler together — the scaler holds the training mean/var
needed to transform future data consistently:

```python
import pickle
pickle.dump(reg, open('model', 'wb'))
pickle.dump(scaler, open('scaler', 'wb'))
```

On new data: only `transform`, never `fit` again.

## Guardrails

- Inspect before transforming.
- Median over mean for cutoffs on skewed data.
- Scale numerical only.
- Split before fit.
- Report more than accuracy.
- Pickle scaler with model.
