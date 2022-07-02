import itertools
import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype
from sklearn.base import BaseEstimator, TransformerMixin


class MetaFeature(BaseEstimator, TransformerMixin):

    def __init__(self, subset='auto', indicators='auto'):
        if type(subset) == str and subset != 'auto':
            self.subset = [subset]
        else:
            self.subset = subset
        if type(indicators) == str and indicators != 'auto':
            self.indicators = [indicators]
        else:
            self.indicators = indicators
        self.features = []
        self.agg_dict = dict()

    def fit(self, X: pd.DataFrame):
        if self.subset == 'auto':
            self.subset = X.columns[np.where(X.dtypes == type(object()))[0]]

        if self.indicators == 'auto':
            self.indicators = [col for col in X.columns if is_numeric_dtype(X[col])]

        for indicator in self.indicators:
            for i in range(1, len(self.subset) + 1):
                for col_set in itertools.combinations(self.subset, i):
                    agg = X.groupby(list(col_set))[indicator].agg(
                        ['sum', 'mean', 'median', 'std', 'min', 'max']
                    ).rename(columns={
                        'sum': f'sum_{indicator}_{"_".join(col_set)}',
                        'mean': f'mean_{indicator}_{"_".join(col_set)}',
                        'median': f'mean_{indicator}_{"_".join(col_set)}',
                        'std': f'std_{indicator}_{"_".join(col_set)}',
                        'min': f'min_{indicator}_{"_".join(col_set)}',
                        'max': f'max_{indicator}_{"_".join(col_set)}',
                    })
                    self.features.extend(agg.columns)
                    self.agg_dict[(indicator, col_set)] = agg.reset_index()

    def transform(self, X):
        for indicator in self.indicators:
            for i in range(1, len(self.subset) + 1):
                for col_set in itertools.combinations(self.subset, i):
                    agg = self.agg_dict[(indicator, col_set)]
                    X = pd.merge(X, agg, on=col_set, how='left')

        return X

    def fit_transform(self, X: pd.DataFrame) -> pd.DataFrame:
        self.fit(X)
        return self.transform(X)
