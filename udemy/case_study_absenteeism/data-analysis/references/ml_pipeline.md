# Pipeline padrão de classificação — Absenteísmo

## Features removidas antes de treinar
Após pré-processamento, remover antes do modelo:
- 'Absenteeism Time in Hours' (substituída pelo target)
- 'Day of the Week' (baixo poder preditivo — eliminação retroativa)
- 'Daily Work Load Average' (baixo poder preditivo — eliminação retroativa)
- 'Distance to Work' (baixo poder preditivo — eliminação retroativa)

## Scaler customizado
Escalar APENAS variáveis numéricas contínuas.
Colunas a OMITIR do scaler (não escalar):
```python
colunas_a_omitir = ['Reason_1', 'Reason_2', 'Reason_3', 'Reason_4', 'Education']
colunas_a_escalar = [c for c in inputs.columns if c not in colunas_a_omitir]
```
O CustomScaler está em `references/custom_scaler.py`.
Sempre salvar o scaler junto com o modelo em pickle — ele armazena mean_ e var_ do treino.

## Divisão treino/teste
```python
x_treino, x_teste, y_treino, y_teste = train_test_split(
    inputs_escalados, targets, test_size=0.2, random_state=20)
```

## Modelo
- Algoritmo: LogisticRegression(max_iter=1000)
- Acurácia treino esperada: ~0.77
- Acurácia teste esperada: ~0.75
- ROC-AUC esperado: ~0.78

## Tabela de odds ratio (entregável de negócio)
```python
tabela = pd.DataFrame(columns=['Feature'], data=inputs.columns.values)
tabela['Coeficiente'] = np.transpose(reg.coef_)
tabela.index += 1
tabela.loc[0] = ['Intercepto', reg.intercept_[0]]
tabela = tabela.sort_index()
tabela['Odds_ratio'] = np.exp(tabela.Coeficiente)
tabela.sort_values('Odds_ratio', ascending=False)
```

## Métricas mínimas obrigatórias
Não reportar apenas acurácia. Sempre incluir:
- `metrics.confusion_matrix(y_teste, y_pred)`
- `metrics.roc_auc_score(y_teste, reg.predict_proba(x_teste)[:, 1])`

## Deployment
- Salvar: `pickle.dump(reg, open('model', 'wb'))`
- Salvar: `pickle.dump(scaler, open('scaler', 'wb'))`
- Em dados novos: apenas `scaler.transform()`, NUNCA `scaler.fit()`
- Interface do módulo: `AbsenteeismModel('model', 'scaler')`
  - `.load_and_clean_data(arquivo_csv)`
  - `.predicted_outputs()` → DataFrame com Probability e Prediction
