# Dataset Reference

## How to use this file

Document each dataset your project uses. For each one, describe:
- File name and size
- Column names, types, and business meaning
- Which columns to drop before modeling (identifiers, leakage)
- Target variable definition and any cutoff logic
- Known quirks or gotchas (skewed distributions, encoding conventions, etc.)

## Template

```
## [dataset_name].csv
N rows, M columns. [Brief description of what this dataset represents.]

| Column | Type | Description |
|---|---|---|
| id | int | Row identifier — drop before modeling |
| target_col | int/float | Target variable — see definition below |
| feature_1 | int | [Business meaning] |
| ... | | |

### Target definition
[Explain how the binary/multiclass target is derived from raw columns, and why.]

### Known issues
[Skewed distributions, imbalanced classes, encoding conventions, etc.]
```

## Example entry

```
## sales_data.csv
1200 rows, 8 columns. Monthly sales records with customer attributes.

| Column | Type | Description |
|---|---|---|
| customer_id | int | Identifier — drop before modeling |
| region | str | Sales region — encode as dummy |
| age | int | Customer age in years |
| purchase_amount | float | Target variable (raw) |

### Target definition
Binary: 1 if purchase_amount > median(purchase_amount), else 0.
Median used because distribution is right-skewed (Shapiro-Wilk p < 0.05).

### Known issues
~15% missing values in `age` — impute with median before modeling.
```
