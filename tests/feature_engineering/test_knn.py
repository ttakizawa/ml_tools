import pytest
import numpy as np

from ml_experiment_tools.feature_engineering import KNNFeature


@pytest.mark.parametrize('n_neighbors', [1, 2, 3])
def test_knn_feature(n_neighbors):
    fold = 3
    knn = KNNFeature(n_neighbors=n_neighbors, folds=fold)
    X = np.random.randn((n_neighbors + 1) * 2 * fold, 2)
    y = np.array([0] * (n_neighbors + 1) * fold + [1] * (n_neighbors + 1) * fold)

    result = knn.fit_transform(X, y)

    assert result.shape == (len(X), 2 * n_neighbors)
