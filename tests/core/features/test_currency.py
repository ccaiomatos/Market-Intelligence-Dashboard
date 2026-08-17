import pandas as pd
import pytest

from core.features.currency import convert_series


def test_convert_series_multiplies_price_by_matching_rate():
    dates = pd.to_datetime(["2024-01-01", "2024-01-02"])
    prices = pd.Series([100, 200], index=dates)
    fx_rate = pd.Series([5.0, 5.0], index=dates)

    result = convert_series(prices, fx_rate)

    assert result.iloc[0] == pytest.approx(500.0)
    assert result.iloc[1] == pytest.approx(1000.0)


def test_convert_series_forward_fills_missing_rate_dates():
    dates = pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-03"])
    prices = pd.Series([100, 200, 300], index=dates)
    fx_rate = pd.Series([5.0, 5.2], index=pd.to_datetime(["2024-01-01", "2024-01-03"]))

    result = convert_series(prices, fx_rate)

    assert result.iloc[1] == pytest.approx(200 * 5.0)


def test_convert_series_is_nan_when_no_prior_rate_exists():
    dates = pd.to_datetime(["2024-01-01", "2024-01-02"])
    prices = pd.Series([100, 200], index=dates)

    fx_rate = pd.Series([5.2], index=pd.to_datetime(["2024-01-02"]))

    result = convert_series(prices, fx_rate)

    assert pd.isna(result.iloc[0])