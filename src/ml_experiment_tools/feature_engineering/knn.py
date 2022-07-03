import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import KFold
from sklearn.neighbors import NearestNeighbors


class KNNFeature(BaseEstimator, TransformerMixin):

    def __init__(self, n_neighbors=1, folds=5):
        self.n_neighbors = n_neighbors
        self.folds = folds
        # key: (class_num, fold_num)
        self.nn_dict = {}

    def fit(self, X, y):
        self.class_num = len(set(y))
        kf = KFold(n_splits=self.folds, shuffle=True)

        fold = 0
        for train_index, test_index in kf.split(X):
            X_train, _ = X[train_index], X[test_index]
            y_train = y[train_index]

            for class_index in range(self.class_num):
                inclass_X = X_train[y_train == class_index]
                nn = NearestNeighbors(
                    n_neighbors=self.n_neighbors)
                nn.fit(inclass_X)
                self.nn_dict[(class_index, fold)] = nn

            fold += 1

    def transform(self, X):
        distances = []
        for class_index in range(self.class_num):
            distance = np.empty((len(X), self.n_neighbors))
            for fold in range(self.folds):
                dist, _ = self.nn_dict[(class_index, fold)].kneighbors(X)
                distance += dist
            distance /= self.folds
            distances.append(distance)
        res = np.hstack(distances)
        columns = [
            f'class_{i}_neighbor_{j}' for i in range(self.class_num)
            for j in range(self.n_neighbors)
        ]
        return pd.DataFrame(data=res, columns=columns)

    def fit_transform(self, X, y):
        self.fit(X, y)
        return self.transform(X)
