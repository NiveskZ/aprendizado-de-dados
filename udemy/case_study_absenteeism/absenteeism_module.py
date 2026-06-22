import numpy as np
import pandas as pd
import pickle
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler


class CustomScaler(BaseEstimator, TransformerMixin):
    def __init__(self, columns, copy=True, with_mean=True, with_std=True):
        self.scaler = StandardScaler(copy=copy, with_mean=with_mean, with_std=with_std)
        self.columns = columns
        self.mean_ = None
        self.var_ = None

    def fit(self, X, y=None):
        self.scaler.fit(X[self.columns], y)
        self.mean_ = np.mean(X[self.columns], axis=0)
        self.var_ = np.var(X[self.columns], axis=0)
        return self

    def transform(self, X, y=None, copy=None):
        init_col_order = X.columns
        X_scaled = pd.DataFrame(
            self.scaler.transform(X[self.columns]),
            columns=self.columns, index=X.index)
        X_not_scaled = X.loc[:, ~X.columns.isin(self.columns)]
        return pd.concat([X_not_scaled, X_scaled], axis=1)[init_col_order]


class _ScalerUnpickler(pickle.Unpickler):
    """Resolve o CustomScaler independente de onde foi salvo (main ou módulo)."""
    def find_class(self, module, name):
        if name == 'CustomScaler':
            return CustomScaler
        return super().find_class(module, name)


class AbsenteeismModel:
    def __init__(self, model_file, scaler_file):
        with open(model_file, 'rb') as m:
            self.reg = pickle.load(m)
        with open(scaler_file, 'rb') as s:
            self.scaler = _ScalerUnpickler(s).load()
        self.data = None
        self.preprocessed_data = None

    def load_and_clean_data(self, data_file):
        df = pd.read_csv(data_file)
        self.df_with_predictions = df.copy()
        df = df.drop(['ID'], axis=1)
        df['Absenteeism Time in Hours'] = 'NaN'

        reason_columns = pd.get_dummies(df['Reason for Absence'], drop_first=True).astype(int)
        reason_type_1 = reason_columns.loc[:, 1:14].max(axis=1)
        reason_type_2 = reason_columns.loc[:, 15:17].max(axis=1)
        reason_type_3 = reason_columns.loc[:, 18:21].max(axis=1)
        reason_type_4 = reason_columns.loc[:, 22:].max(axis=1)

        df = df.drop(['Reason for Absence'], axis=1)
        df = pd.concat([df, reason_type_1, reason_type_2, reason_type_3, reason_type_4], axis=1)
        df.columns = ['Date', 'Transportation Expense', 'Distance to Work', 'Age',
                      'Daily Work Load Average', 'Body Mass Index', 'Education',
                      'Children', 'Pets', 'Absenteeism Time in Hours',
                      'Reason_1', 'Reason_2', 'Reason_3', 'Reason_4']
        df = df[['Reason_1', 'Reason_2', 'Reason_3', 'Reason_4', 'Date',
                 'Transportation Expense', 'Distance to Work', 'Age',
                 'Daily Work Load Average', 'Body Mass Index', 'Education',
                 'Children', 'Pets', 'Absenteeism Time in Hours']]

        df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
        df['Month Value'] = df['Date'].apply(lambda x: x.month)
        df['Day of the Week'] = df['Date'].apply(lambda x: x.weekday())
        df = df.drop(['Date'], axis=1)
        df = df[['Reason_1', 'Reason_2', 'Reason_3', 'Reason_4', 'Month Value',
                 'Day of the Week', 'Transportation Expense', 'Distance to Work', 'Age',
                 'Daily Work Load Average', 'Body Mass Index', 'Education',
                 'Children', 'Pets', 'Absenteeism Time in Hours']]

        df['Education'] = df['Education'].map({1: 0, 2: 1, 3: 1, 4: 1})
        df = df.fillna(value=0)
        df = df.drop(['Absenteeism Time in Hours'], axis=1)
        df = df.drop(['Day of the Week', 'Daily Work Load Average', 'Distance to Work'], axis=1)

        self.preprocessed_data = df.copy()
        self.data = self.scaler.transform(df)

    def predicted_probability(self):
        if self.data is not None:
            return self.reg.predict_proba(self.data)[:, 1]

    def predicted_output_category(self):
        if self.data is not None:
            return self.reg.predict(self.data)

    def predicted_outputs(self):
        if self.data is not None:
            self.preprocessed_data['Probability'] = self.reg.predict_proba(self.data)[:, 1]
            self.preprocessed_data['Prediction'] = self.reg.predict(self.data)
            return self.preprocessed_data
