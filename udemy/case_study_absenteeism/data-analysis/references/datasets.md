# Datasets deste projeto

## Absenteeism_data.csv (bruto)
700 linhas, 12 colunas. Nunca modificar.

| Coluna | Tipo | Descrição |
|---|---|---|
| ID | int | Identificador do colaborador — remover antes de modelar |
| Reason for Absence | int | Código CID 0-28 (ver agrupamento abaixo) |
| Date | str | DD/MM/AAAA — extrair mês e dia da semana |
| Transportation Expense | int | Custo mensal de transporte |
| Distance to Work | int | Quilômetros |
| Age | int | Anos |
| Daily Work Load Average | float | Minutos por dia |
| Body Mass Index | int | IMC |
| Education | int | 1=ensino médio, 2=graduação, 3=pós, 4=mestre/doutor |
| Children | int | Número de filhos |
| Pets | int | Número de pets |
| Absenteeism Time in Hours | int | **Variável-alvo** (bruta) |

### Agrupamento dos motivos de ausência
get_dummies() na coluna Reason for Absence, drop_first=True, depois .max(axis=1) por grupo:
- Reason_1: colunas 1-14 (doenças — categorias CID I a XIV)
- Reason_2: colunas 15-17 (gravidez e relacionados)
- Reason_3: colunas 18-21 (causas externas / lesões)
- Reason_4: colunas 22-28 (razões leves / não especificadas)

## df_preprocessado.csv (pré-processado)
15 colunas. Referência de validação — não modificar.

Colunas em ordem: Reason_1, Reason_2, Reason_3, Reason_4, Month Value,
Day of the Week, Transportation Expense, Distance to Work, Age,
Daily Work Load Average, Body Mass Index, Education, Children, Pets,
Absenteeism Time in Hours.

Education: 0 se valor original era 1 (ensino médio), 1 caso contrário.

## Absenteeism_new_data.csv (dados novos)
Mesmo formato que o bruto. Usado para pontuar com o módulo treinado.

## Absenteeism_predictions.csv (saída)
Gerado pelo módulo. Contém todas as colunas pré-processadas + Probability + Prediction.
Alimenta os dashboards do Tableau.

## Definição da variável-alvo (ML)
- Mediana de 'Absenteeism Time in Hours' = 3.0
- Target = 1 se horas > mediana, caso contrário 0
- Justificativa: distribuição fortemente não normal (Shapiro-Wilk p < 0.05),
  mediana é mais robusta que a média; produz classes aproximadamente balanceadas (~46% positivos)
