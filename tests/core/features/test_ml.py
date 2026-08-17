import pandas as pd
import pytest

from core.features.ml import build_features, build_latest_features


def test_build_features_calculates_correct_lag_and_target_values():
    returns = pd.Series([0.01, -0.02, 0.03, 0.01, -0.01])

    result = build_features(returns, n_lags=1)
    assert result.loc[1, "lag_1"] == pytest.approx(0.01)
    assert result.loc[1, "target"] == 1.0

    assert result.loc[3, "lag_1"] == pytest.approx(0.03)
    assert result.loc[3, "target"] == 0.0


def test_build_features_drops_rows_with_incomplete_lag_or_missing_target():
    returns = pd.Series([0.01, -0.02, 0.03, 0.01, -0.01])

    result = build_features(returns, n_lags=1)

    assert 0 not in result.index
    assert 4 not in result.index
    assert len(result) == 3


def test_build_latest_features_uses_most_recent_date_as_reference():
    returns = pd.Series([0.01, -0.02, 0.03, 0.01, -0.01])

    result = build_latest_features(returns, n_lags=2)

    assert result.iloc[0]["lag_1"] == pytest.approx(0.01)
    assert result.iloc[0]["lag_2"] == pytest.approx(0.03)
    assert len(result) == 1  # apenas uma linha, a mais recente