import pandas as pd
from sklearn.preprocessing import (
    OneHotEncoder as sk_OneHotEncoder,
    LabelEncoder as sk_LabelEncoder
)

from ml_experiment_tools.utils import get_logger


logger = get_logger(__name__)


class OneHotEncoder:
    def __init__(self, column, drop='first', handle_unknown='error'):
        self.column = column
        self.drop = drop
        self.le = sk_LabelEncoder()
        self.ohe = sk_OneHotEncoder(drop=drop, handle_unknown=handle_unknown)

    def fit(self, df):
        if df[self.column].nunique() > 1000:
            logger.warning(f"{self.column}'s unique_count: {df[self.column].nunique()}. It is too many labels.")
        labels = self.le.fit_transform(df[self.column])
        self.ohe.fit(labels.reshape(-1, 1))

    def fit_transform(self, df):
        self.fit(df)
        return self.transform(df)

    def transform(self, df):
        labels = self.le.transform(df[self.column])
        encoded = self.ohe.transform(labels.reshape(-1, 1)).astype(int)
        if self.drop == "first":
            names = [(self.column + "_") + str(s) for s in self.le.classes_[1:]]
        else:
            names = [(self.column + "_") + str(s) for s in self.le.classes_]

        self.names = names
        one_hot_df = pd.DataFrame(
            index=df.index,
            columns=names,
            data=encoded.toarray(),
            dtype=int
        )
        df = pd.concat([df, one_hot_df], axis=1)
        return df
