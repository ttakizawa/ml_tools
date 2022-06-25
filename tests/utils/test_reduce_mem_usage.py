import pandas as pd
import numpy as np

from ml_experiment_tools.utils import reduce_mem_usage


def test_reduce_mem_usage():
    df = pd.DataFrame({
        'col1': [np.iinfo(np.int8).min + 1, np.iinfo(np.int8).max - 1], # -> np.int8
        'col2': [np.iinfo(np.int16).min + 1, np.iinfo(np.int16).max - 1], # -> np.int16
        'col3': [np.iinfo(np.int32).min + 1, np.iinfo(np.int32).max - 1], # -> np.int32
        'col4': [np.iinfo(np.int64).min + 1, np.iinfo(np.int64).max - 1], # -> np.int64
        'col5': [np.finfo(np.float16).min + 1e-2, np.finfo(np.float16).max - 1e-2], # -> np.float16
        'col6': [np.finfo(np.float16).min - 1e-2, np.finfo(np.float16).max + 1e-2], # -> np.float32
        'col7': [np.finfo(np.float32).min - 1e-2, np.finfo(np.float32).max - 1e-2], # -> np.float64
        'col8': [True, False], # -> np.bool
        'col9': ["aaa", "bbb"], # -> np.object
    })
    start_mem = df.memory_usage().sum()

    expected = {
        'col1': np.int8,
        'col2': np.int16,
        'col3': np.int32,
        'col4': np.int64,
        'col5': np.float16,
        'col6': np.float32,
        'col7': np.float64,
        'col8': bool,
        'col9': object,
    }

    df = reduce_mem_usage(df)
    end_mem = df.memory_usage().sum()

    for col in df.columns:
        assert df[col].dtypes == expected[col]

    assert end_mem <= start_mem
