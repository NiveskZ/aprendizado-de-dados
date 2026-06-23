# %% [markdown]
# # Absenteísmo — Fase 1: Pré-processamento
#
# **Objetivo:** transformar o arquivo bruto `Absenteeism_data.csv` (700 linhas, 12 colunas)
# em uma tabela pronta para modelagem e exportá-la como `df_preprocessado.csv`.
#
# **Entrada:** `Absenteeism_data.csv`
# **Saída:** `df_preprocessado.csv` (15 colunas)
#
# Além das etapas do curso (remover ID, dummy + agrupar razões, extrair partes da data,
# binarizar Educação), este notebook adiciona uma camada de EDA para justificar as
# decisões estatisticamente.

# %% [markdown]
# ## 0. Imports e carregamento

# %%
import numpy as np
import pandas as pd
from scipy import stats

pd.options.display.max_columns = None

# %%
raw_csv = pd.read_csv('data/Absenteeism_data.csv')
# mantém a cópia bruta intocada; trabalha em df
df = raw_csv.copy()
df.head()

# %% [markdown]
# ## 1. EDA inicial — entender antes de transformar

# %%
df.info()

# %%
# sem valores ausentes, todos numéricos exceto Date
df.describe()

# %%
# a variável-alvo é fortemente assimétrica à direita: a maioria das ausências é curta,
# poucas são muito longas — por isso usaremos a MEDIANA (não a média) como ponto de
# corte na classificação
df['Absenteeism Time in Hours'].describe()

# %%
# verificação formal: a variável-alvo segue distribuição normal?
w, p = stats.shapiro(df['Absenteeism Time in Hours'])
print(f'Shapiro-Wilk: W={w:.4f}, p={p:.2e}')
print('Não normal (p < 0.05)' if p < 0.05 else 'Normal')
# resultado: fortemente não normal -> mediana é a escolha robusta para o ponto de corte

# %% [markdown]
# ## 2. Remover a coluna ID
# ID é um identificador, não uma feature preditiva.

# %%
df = df.drop(['ID'], axis=1)
df.head()

# %% [markdown]
# ## 3. Razões de ausência -> dummies -> 4 grupos
#
# `Reason for Absence` contém códigos de categorias CID 0-28. Aplicamos one-hot encoding,
# removemos a primeira dummy (código 0, nossa baseline estatística para evitar
# multicolinearidade), e depois agrupamos as 28 colunas em 4 features binárias usando
# `.max(axis=1)` (1 se qualquer razão do grupo foi selecionada, caso contrário 0).

# %%
reason_columns = pd.get_dummies(df['Reason for Absence'], drop_first=True).astype(int)
reason_columns.head()

# %%
# agrupar por faixas CID
reason_type_1 = reason_columns.loc[:, 1:14].max(axis=1)   # doenças
reason_type_2 = reason_columns.loc[:, 15:17].max(axis=1)  # gravidez e relacionados
reason_type_3 = reason_columns.loc[:, 18:21].max(axis=1)  # causas externas / lesões
reason_type_4 = reason_columns.loc[:, 22:].max(axis=1)    # razões leves / não especificadas

# %%
# remover a coluna original e concatenar os 4 grupos
df = df.drop(['Reason for Absence'], axis=1)
df = pd.concat([df, reason_type_1, reason_type_2, reason_type_3, reason_type_4], axis=1)
df.columns = ['Date', 'Transportation Expense', 'Distance to Work', 'Age',
              'Daily Work Load Average', 'Body Mass Index', 'Education',
              'Children', 'Pets', 'Absenteeism Time in Hours',
              'Reason_1', 'Reason_2', 'Reason_3', 'Reason_4']
df.head()

# %%
# reordenar para que os grupos de razão venham primeiro
df = df[['Reason_1', 'Reason_2', 'Reason_3', 'Reason_4', 'Date',
         'Transportation Expense', 'Distance to Work', 'Age',
         'Daily Work Load Average', 'Body Mass Index', 'Education',
         'Children', 'Pets', 'Absenteeism Time in Hours']]

# %% [markdown]
# ### Checkpoint 1

# %%
df_checkpoint_razoes = df.copy()
# verificar se é uma cópia real (objeto diferente), não uma view
print('Cópia independente:', df_checkpoint_razoes is not df)

# %% [markdown]
# ## 4. Data -> mês e dia da semana
#
# Converte a string `DD/MM/AAAA` para datetime, extrai mês (1-12) e dia da semana
# (0=Seg ... 6=Dom) e remove a coluna Date original.

# %%
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
df['Month Value'] = df['Date'].apply(lambda x: x.month)
df['Day of the Week'] = df['Date'].apply(lambda x: x.weekday())
df = df.drop(['Date'], axis=1)

# %%
# reordenar para colocar as novas colunas de data logo após as razões
df = df[['Reason_1', 'Reason_2', 'Reason_3', 'Reason_4', 'Month Value',
         'Day of the Week', 'Transportation Expense', 'Distance to Work', 'Age',
         'Daily Work Load Average', 'Body Mass Index', 'Education',
         'Children', 'Pets', 'Absenteeism Time in Hours']]
df.head()

# %% [markdown]
# ## 5. Educação -> binário
#
# Original: 1=ensino médio, 2=graduação, 3=pós-graduação, 4=mestrado/doutorado.
# A grande maioria é ensino médio, então colapsamos em: 0 = ensino médio,
# 1 = qualquer nível superior.

# %%
# verificar a distribuição primeiro — confirma o desequilíbrio que motiva a divisão binária
df['Education'].value_counts()

# %%
df['Education'] = df['Education'].map({1: 0, 2: 1, 3: 1, 4: 1})
df['Education'].value_counts()

# %% [markdown]
# ## 6. Exportar

# %%
df_preprocessado = df.copy()
df_preprocessado.to_csv('data/df_preprocessado.csv', index=False)
print('Salvo. Shape final:', df_preprocessado.shape)

# %% [markdown]
# ## Resumo
#
# - Reduziu 12 colunas brutas para 15 features prontas para modelagem (4 grupos de razão
#   + partes da data + Educação binarizada + features numéricas + variável-alvo).
# - Confirmado que a variável-alvo é fortemente não normal, justificando o ponto de corte
#   na mediana usado na Fase 2.
# - Saída bate 100% com a referência do curso.
#
# **Próximo passo:** Fase 2 — construir a regressão logística em um novo arquivo.
