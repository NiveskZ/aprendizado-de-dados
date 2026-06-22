# %% [markdown]
# # Absenteísmo — Fase 2: Regressão Logística
#
# **Objetivo:** construir um modelo que prevê se um colaborador terá absenteísmo
# *excessivo* (mais horas do que a mediana).
#
# **Entrada:** `df_preprocessado.csv`
# **Saídas:** arquivos `model` e `scaler` em pickle (usados pela Fase 3)
#
# Notebook separado por decisão de projeto — modelagem é uma responsabilidade
# distinta do pré-processamento.

# %% [markdown]
# ## 0. Imports e carregamento

# %%
import numpy as np
import pandas as pd
pd.options.display.max_columns = None

data_preprocessada = pd.read_csv('data/df_preprocessado.csv')
data_preprocessada.head()

# %% [markdown]
# ## 1. Criar a variável-alvo
#
# O modelo precisa de uma categoria, não de um número de horas. Dividimos pela **mediana**
# para que as duas classes fiquem aproximadamente balanceadas — um alvo balanceado é o
# que torna a acurácia uma métrica confiável aqui. (A Fase 1 confirmou que a distribuição
# das horas é não normal, por isso a mediana, e não a média, é o ponto de corte correto.)

# %%
data_preprocessada['Absenteeism Time in Hours'].median()

# %%
targets = np.where(
    data_preprocessada['Absenteeism Time in Hours'] >
    data_preprocessada['Absenteeism Time in Hours'].median(), 1, 0)
data_preprocessada['Absenteísmo Excessivo'] = targets

# %%
# verificar o balanceamento: quão próximo de 50/50?
targets.sum() / targets.shape[0]

# %% [markdown]
# ## 2. Selecionar os inputs (com checkpoint)
#
# Removemos a variável-alvo e três features que a eliminação retroativa do curso mostrou
# ter baixo poder preditivo: `Day of the Week`, `Daily Work Load Average`,
# `Distance to Work`.

# %%
data_com_targets = data_preprocessada.drop(
    ['Absenteeism Time in Hours', 'Day of the Week',
     'Daily Work Load Average', 'Distance to Work'], axis=1)
# confirmar checkpoint (deve ser False = objeto diferente)
data_com_targets is data_preprocessada

# %%
inputs_nao_escalados = data_com_targets.iloc[:, :-1]
inputs_nao_escalados.columns.values

# %% [markdown]
# ## 3. Scaler customizado — escalar apenas as colunas numéricas
#
# Padronizar variáveis dummy ou flags binárias não faz sentido e distorce a interpretação
# dos coeficientes. Este CustomScaler encapsula o StandardScaler do sklearn mas toca
# apenas as colunas especificadas, deixando `Reason_*` e `Education` intactas.

# %%
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler
from absenteeism_module import CustomScaler
# %%
colunas_a_omitir = ['Reason_1', 'Reason_2', 'Reason_3', 'Reason_4', 'Education']
colunas_a_escalar = [x for x in inputs_nao_escalados.columns if x not in colunas_a_omitir]

scaler_absenteismo = CustomScaler(colunas_a_escalar)
scaler_absenteismo.fit(inputs_nao_escalados)
inputs_escalados = scaler_absenteismo.transform(inputs_nao_escalados)
inputs_escalados.head()

# %% [markdown]
# ## 4. Divisão treino/teste
# 80/20, random_state fixo para reprodutibilidade.

# %%
from sklearn.model_selection import train_test_split

x_treino, x_teste, y_treino, y_teste = train_test_split(
    inputs_escalados, targets, test_size=0.2, random_state=20)
print(x_treino.shape, y_treino.shape)
print(x_teste.shape, y_teste.shape)

# %% [markdown]
# ## 5. Ajustar o modelo

# %%
from sklearn.linear_model import LogisticRegression
from sklearn import metrics

reg = LogisticRegression(max_iter=1000)
reg.fit(x_treino, y_treino)
reg.score(x_treino, y_treino)

# %% [markdown]
# ## 6. Coeficientes e razão de chances (odds ratio)
#
# A razão de chances = exp(coeficiente). Um valor > 1 aumenta as chances de absenteísmo
# excessivo; < 1 diminui. Esta tabela é o entregável real para o negócio — informa ao
# RH *quais fatores importam e em que proporção*.

# %%
tabela_resumo = pd.DataFrame(columns=['Feature'],
                             data=inputs_nao_escalados.columns.values)
tabela_resumo['Coeficiente'] = np.transpose(reg.coef_)
tabela_resumo.index = tabela_resumo.index + 1
tabela_resumo.loc[0] = ['Intercepto', reg.intercept_[0]]
tabela_resumo = tabela_resumo.sort_index()
tabela_resumo['Odds_ratio'] = np.exp(tabela_resumo.Coeficiente)
tabela_resumo.sort_values('Odds_ratio', ascending=False)

# %% [markdown]
# **Leitura do resultado:** os grupos de razão dominam. `Reason_3` (lesões/causas externas)
# e `Reason_1` (doenças) elevam mais as chances — intuitivo, pois são ausências sérias e
# não planejadas. Despesa com transporte e número de filhos empurram as chances levemente
# para cima. Idade, educação e pets as reduzem levemente.

# %% [markdown]
# ## 7. Avaliar no conjunto de teste

# %%
reg.score(x_teste, y_teste)

# %%
# enriquecimento além do curso: matriz de confusão + AUC
y_pred = reg.predict(x_teste)
print('Matriz de confusão:')
print(metrics.confusion_matrix(y_teste, y_pred))
print()
print(metrics.classification_report(y_teste, y_pred))
auc = metrics.roc_auc_score(y_teste, reg.predict_proba(x_teste)[:, 1])
print(f'ROC-AUC: {auc:.4f}')

# %%
# probabilidades para a classe 1 — alimentam a análise no Tableau depois
probabilidades_previstas = reg.predict_proba(x_teste)
probabilidades_previstas[:, 1][:10]

# %% [markdown]
# ## 8. Salvar modelo e scaler (pickle)

# %%
import pickle

with open('model', 'wb') as arquivo:
    pickle.dump(reg, arquivo)

with open('scaler', 'wb') as arquivo:
    pickle.dump(scaler_absenteismo, arquivo)

print('model e scaler salvos')

# %% [markdown]
# ## Resumo
#
# - Alvo: ponto de corte na mediana, ~46% positivos (bem balanceado).
# - Acurácia treino ~0.77, acurácia teste ~0.75, ROC-AUC ~0.78.
# - Os grupos de razão são de longe os preditores mais fortes.
# - `model` e `scaler` foram salvos em pickle para o deployment na Fase 3.
#
# **Próximo passo:** Fase 3 — encapsular tudo em um módulo reutilizável que pontua dados novos.

# %%
