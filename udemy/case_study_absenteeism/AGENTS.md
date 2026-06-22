# AGENTS.md — General Working Context

## Who I am

Data analyst / data scientist working with Python, SQL, and business documentation.
Stack: Python (pandas, sklearn, matplotlib/seaborn, statsmodels), SQL (Oracle Database
and SQL Server in production), Jupyter notebooks, VS Code, Tableau.

Context: WiseDB — IT integrator specializing in cloud, databases, and critical
infrastructure. Projects span data analysis, performance diagnostics, automation,
and BI.

---

## How to work with me

### Default behavior

- Always Respond in Portuguese
- Be direct and objective. Skip preambles like "Great question" or "Certainly"
- When I ask for code, give me the code first, explanation after if needed
- When something has multiple valid approaches, show the one that fits production
  context first, mention alternatives briefly
- Do not suggest things I did not ask for

### On uncertainty

- If you are not sure about something, say so explicitly
- Do not hallucinate library APIs or SQL syntax — say "check the docs for this" if
  needed
- For Oracle-specific behavior (optimizer hints, AWR, Data Guard), prefer caution
  over confidence

---

## Python conventions

### General

- Python 3.10+
- Use type hints on function signatures
- Prefer explicit over implicit (no magic, no clever one-liners that sacrifice clarity)
- f-strings for string formatting
- Pathlib for file paths, not os.path

### Data analysis

- pandas for tabular data; numpy for array operations
- Always inspect before transforming: `.shape`, `.dtypes`, `.describe()`, `.head()`
- Create checkpoints: assign to a new variable instead of modifying in-place,
  verify with `df_new is df_old` (should be False)
- Never use ROUND, TRUNC, or display formatting on raw numeric outputs unless
  explicitly requested — show values as returned
- Column names: keep original names from the source unless there is a reason to
  rename; document renames
- Prefer `df.copy()` when creating a modified version you will use independently

### Machine learning

- sklearn pipelines when the workflow has more than two steps
- Always split before fitting the scaler — never fit on the full dataset
- Document the target definition and cutoff logic as a comment, not just code
- Save models with pickle; always save the scaler alongside the model
- Accuracy alone is not enough — include confusion matrix and at minimum one
  threshold-independent metric (ROC-AUC or similar)

### Notebooks

- One notebook per logical phase (preprocessing, modeling, integration)
- First cell: markdown with the purpose, inputs, and expected outputs of the notebook
- Use `# %%` cell markers for VS Code notebook compatibility
- Checkpoints at the end of each major transformation block
- Last cell: summary of what was produced and where it was saved

### Imports

Group in this order, one blank line between groups:
```python
# standard library
import os
from pathlib import Path

# third-party
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

# local
from module.my_module import MyClass
```

---

## SQL conventions

### General rules

- Always write a SELECT that shows the affected rows before any DML (INSERT,
  UPDATE, DELETE)
- Signal destructive operations explicitly with a comment: `-- DESTRUCTIVE: review before running`
- Indicate when a maintenance window or backup is advisable
- Use technical terms in English (tablespace, AWR, ASH, Data Guard, AG, execution plan)
- Comment only non-obvious logic — no author/date headers unless requested

### Oracle Database

- Prefer bind variables over literals in production queries
- Use `EXPLAIN PLAN FOR` + `DBMS_XPLAN.DISPLAY` for execution plans
- For performance work: lead with wait events and top SQLs, not full explain plans
  unless requested
- Avoid `SELECT *` in production code; always name columns explicitly
- When touching production: SELECT first, then DML in a transaction with explicit
  COMMIT only after verification

### SQL Server

- Use `SET NOCOUNT ON` in stored procedures
- Prefer `sys.dm_exec_*` DMVs for diagnostics
- Always check for implicit conversions in WHERE clauses (they kill index seeks)
- Named transactions for multi-step DML

---

## Statistics and analysis

When doing exploratory or statistical work, follow this sequence unless instructed
otherwise:

1. Understand the data (types, nulls, distributions, outliers)
2. State the question in statistical terms before writing code
3. Check assumptions before applying a test (normality, variance homogeneity, etc.)
4. Report effect size alongside p-value — statistical significance alone is not enough
5. Interpret results in business terms, not just statistical terms

Tests available in the repertoire: Shapiro-Wilk, K-S, T-test, ANOVA, Tukey,
Mann-Whitney, chi-square, Poisson. Use the right one for the data type and
distribution assumptions.

---

## Documentation and writing

- When generating technical documents, use clear section structure with headings
- Business language for executive summaries, technical language for appendices
- Avoid bullet-point overload — use prose for narrative, bullets only for true lists
- For WiseDB documents: formal tone, structured, complete sentences
- Never invent data or results — if something is missing, flag it explicitly

---

## File and project hygiene

- Raw data files are never modified — always work on a copy
- Outputs go to a dedicated `/output` or `/results` folder, never mixed with source data
- Temporary files and scratch notebooks are labeled as such (`_scratch`, `_temp`)
- requirements.txt or environment.yml at the project root when the project has
  more than two dependencies

---

## What not to do

- Do not add unrequested features, refactors, or "improvements"
- Do not wrap every response in markdown headers if a direct answer suffices
- Do not repeat back what I just said before answering
- Do not add disclaimers about consulting professionals for technical decisions
  I am qualified to make
- Do not scale dummy variables, binary flags, or ordinal columns encoded as 0/1
  in ML pipelines — only scale continuous numerical features
