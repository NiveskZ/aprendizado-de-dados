# ML Classification Pipeline

A repeatable workflow for binary classification on tabular data.

## Step 1 — Define the target

If the raw target is continuous, use a cutoff. State the logic explicitly:

```python
targets = np.where(df['target_col'] > df['target_col'].median(), 1, 0)
```

Check balance: `targets.sum() / targets.shape[0]`.
Aim for 40–60%. If badly imbalanced, consider class weights or AUC/F1 over accuracy.

## Step 2 — Select inputs

Drop the target and any non-predictive columns (identifiers, leakage columns, low-variance features).
Create a checkpoint — see `references/datasets.md` for which columns to drop per project.

## Step 3 — Scale only numerical features

Never scale dummy variables or binary flags. Use an explicit omit list:

```python
columns_to_omit = ['dummy_col_1', 'dummy_col_2', 'binary_flag']
columns_to_scale = [c for c in inputs.columns if c not in columns_to_omit]
```

Use the `CustomScaler` from `references/custom_scaler.py`. It wraps StandardScaler,
returns a DataFrame with column names preserved, and can be pickled with the model.

## Step 4 — Split before fitting the scaler

```python
x_train, x_test, y_train, y_test = train_test_split(
    scaled_inputs, targets, test_size=0.2, random_state=20)
```

Fit the scaler on training data only. Never fit on the full dataset — that leaks test information.

## Step 5 — Fit and interpret

```python
from sklearn.linear_model import LogisticRegression
reg = LogisticRegression(max_iter=1000)
reg.fit(x_train, y_train)
```

Build an odds-ratio table — this is the business deliverable:

```python
summary = pd.DataFrame(columns=['Feature'], data=inputs.columns.values)
summary['Coefficient'] = np.transpose(reg.coef_)
summary.index += 1
summary.loc[0] = ['Intercept', reg.intercept_[0]]
summary = summary.sort_index()
summary['Odds_ratio'] = np.exp(summary.Coefficient)
summary.sort_values('Odds_ratio', ascending=False)
```

Odds ratio > 1 increases the odds of the positive class. Interpret top features in plain language.

## Step 6 — Evaluate honestly

```python
from sklearn import metrics

y_pred = reg.predict(x_test)
print(metrics.confusion_matrix(y_test, y_pred))
print(metrics.classification_report(y_test, y_pred))
auc = metrics.roc_auc_score(y_test, reg.predict_proba(x_test)[:, 1])
print(f'ROC-AUC: {auc:.4f}')
```

## Step 7 — Save for deployment

```python
import pickle
pickle.dump(reg, open('model', 'wb'))
pickle.dump(scaler, open('scaler', 'wb'))
```

**Critical:** always import `CustomScaler` from your module file before pickling,
so the pickle stores the correct class reference:

```python
from my_module import CustomScaler  # do this in the modeling file
```

On new data: `scaler.transform(X)` only — never `scaler.fit(X)`.
