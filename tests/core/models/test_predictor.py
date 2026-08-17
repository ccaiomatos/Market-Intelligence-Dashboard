from unittest.mock import patch

import numpy as np
import pandas as pd
import pytest

from core.models.predictor import train_model


def _fake_features(n=30, seed=0):
    rng = np.random.RandomState(seed)
    lag_1 = rng.randn(n) * 0.01
    target = (lag_1 > 0).astype(float)
    return pd.DataFrame({"lag_1": lag_1, "target": target})


def test_train_model_returns_fitted_model_and_valid_accuracy():
    features = _fake_features()

    model, accuracy = train_model(features)

    predictions = model.predict(features.drop(columns="target"))
    assert len(predictions) == len(features)
    assert 0.0 <= accuracy <= 1.0


def test_train_model_splits_data_without_shuffling_to_avoid_leakage():
    features = _fake_features()


    with patch("core.models.predictor.train_test_split") as mock_split:
        x = features.drop(columns="target")
        y = features["target"]
        split_point = int(len(features) * 0.8)
        mock_split.return_value = (
            x.iloc[:split_point], x.iloc[split_point:],
            y.iloc[:split_point], y.iloc[split_point:],
        )

        train_model(features)

        _, kwargs = mock_split.call_args
        assert kwargs["shuffle"] is False