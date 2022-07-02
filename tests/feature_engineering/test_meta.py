import numpy as np
import pandas as pd


from ml_experiment_tools.feature_engineering import MetaFeature


def test_meta_feature():
    np.random.seed(0)
    size = 10000
    category_1 = ['A', 'B', 'C']
    category_2 = ['a', 'b', 'c']
    mean_std_dict = {
        ('A', 'a'): (10, 1),
        ('A', 'b'): (7, 2),
        ('A', 'c'): (3, 5),
        ('B', 'a'): (8, 1),
        ('B', 'b'): (4, 2),
        ('B', 'c'): (2, 5),
        ('C', 'a'): (15, 1),
        ('C', 'b'): (6, 2),
        ('C', 'c'): (1, 5),
    }

    dfs = []
    for cat_1 in category_1:
        for cat_2 in category_2:
            df = pd.DataFrame({
                'category_1': [cat_1] * size,
                'category_2': [cat_2] * size,
                'indicator': np.random.normal(
                    loc=mean_std_dict[(cat_1, cat_2)][0],
                    scale=mean_std_dict[(cat_1, cat_2)][1],
                    size=size
                )
            })
            dfs.append(df)

    df = pd.concat(dfs, ignore_index=True)
    meta = MetaFeature()
    result = meta.fit_transform(df)
    
    assert result.shape[1] == (len(df.columns) + 3 * 6)
