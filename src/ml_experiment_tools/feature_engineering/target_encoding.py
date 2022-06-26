import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class TargetEncoder(BaseEstimator, TransformerMixin):

    def __init__(self, categories='auto', k=1, f=1,
                 noise_level=0, random_state=None):
        if type(categories) == str and categories != 'auto':
            self.categories = [categories]
        else:
            self.categories = categories
        self.k = k
        self.f = f
        self.noise_level = noise_level
        self.encodings = dict()
        self.prior = None
        self.random_state = random_state

    def add_noise(self, series, noise_level):
        return series * (1 + noise_level * np.random.randn(len(series)))

    def fit(self, X: pd.DataFrame, y=None):
        if self.categories == 'auto':
            self.categories = X.columns[np.where(X.dtypes == type(object()))[0]]

        temp = X.loc[:, self.categories].copy()
        temp['target'] = y
        self.prior = np.mean(y)
        for variable in self.categories:
            avg = (temp.groupby(by=variable)['target'].agg(['mean', 'count']))
            # Compute smoothing
            smoothing = (1 / (1 + np.exp(-(avg['count'] - self.k) / self.f)))

            # The bigger the count the less full_avg is accpounted
            self.encodings[variable] = dict(
                self.prior * (1 - smoothing) + avg['mean'] * smoothing)

        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        Xt = X.copy()
        for variable in self.categories:
            Xt[variable].replace(self.encodings[variable], inplace=True)
            unknown_value = {
                value: self.prior for value in
                X[variable].unique() if value not in
                self.encodings[variable].keys()
            }
            if len(unknown_value) > 0:
                Xt[variable].replace(unknown_value, inplace=True)
            Xt[variable] = Xt[variable].astype(float)
            if self.noise_level > 0:
                if self.random_state is not None:
                    np.random.seed(self.random_state)
                Xt[variable] = self.add_noise(Xt[variable], self.noise_level)
        return Xt

    def fit_transform(self, X: pd.DataFrame, y=None) -> pd.DataFrame:
        self.fit(X, y)
        return self.transform(X)
