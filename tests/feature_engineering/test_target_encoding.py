import numpy as np
import pandas as pd

from ml_experiment_tools.feature_engineering import TargetEncoder


def test_target_encoding():
    np.random.seed(0)
    size = 10000
    categories = [('a', 0.8), ('b', 0.3)]
    dfs = []
    targets = []
    for category, rate in categories:
        df = pd.DataFrame({
            'category': [category] * size,
            'value': [1] * size,
        })
        dfs.append(df)
        targets.append(np.random.binomial(1, rate, size=size))

    df = pd.concat(dfs, ignore_index=True)
    y = np.hstack(targets)

    encoder = TargetEncoder(random_state=0)

    result = encoder.fit_transform(df, y)

    for category, rate in categories:
        np.testing.assert_approx_equal(
            result[df['category']==category]['category'].mean(),
            rate,
            significant=2)
