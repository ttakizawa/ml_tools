import pandas as pd
from ml_experiment_tools.feature_engineering import OneHotEncoder


def test_onehot_encoder():
    df = pd.DataFrame(
        {'col1': ['aaa', 'bbb', 'ccc']}
    )

    encoder = OneHotEncoder('col1')

    result = encoder.fit_transform(df)

    assert len(result) == len(df)
    assert len(result.columns) == 3
