# %% [markdown]
# # Absenteísmo — Fase 3: Integração / Deployment
#
# **Objetivo:** carregar o modelo treinado pelo `absenteeism_module`, pontuar dados novos
# e exportar as predições para o Tableau.
#
# **Entradas:** `absenteeism_module.py`, `model`, `scaler`, `Absenteeism_new_data.csv`
# **Saída:** `Absenteeism_predictions.csv`
#
# Este notebook contém quase nenhuma lógica — esse é exatamente o ponto. Todo o
# pré-processamento e a pontuação estão encapsulados no módulo, então o deployment
# se resume a três chamadas.

# %% [markdown]
# ## 1. Importar o módulo

# %%
from absenteeism_module import AbsenteeismModel

# %% [markdown]
# ## 2. Carregar o modelo e pontuar dados novos

# %%
modelo = AbsenteeismModel('model', 'scaler')
modelo.load_and_clean_data('data/Absenteeism_new_data.csv')

# %% [markdown]
# ## 3. Obter as predições

# %%
# tabela completa com Probability (de absenteísmo excessivo) e Prediction (0/1)
modelo.predicted_outputs().head()

# %%
# também é possível obter as partes separadamente, se necessário
modelo.predicted_probability()[:10]

# %%
modelo.predicted_output_category()[:10]

# %% [markdown]
# ## 4. Exportar para o Tableau

# %%
modelo.predicted_outputs().to_csv('data/Absenteeism_predictions.csv', index=False)
print('Predições exportadas.')

# %% [markdown]
# ## Resumo
#
# O módulo transforma a pontuação de dados novos em uma operação de três linhas.
# O CSV exportado traz a probabilidade e a classe prevista de cada colaborador junto
# com suas features, pronto para os dashboards do Tableau na Fase 4.
#
# **Observação:** o scaler é apenas *transformado* em dados novos, nunca re-ajustado —
# os parâmetros ajustados vêm do conjunto de treino, salvos em pickle na Fase 2.
