import pandas as pd
import pytest

from core.features.risk import annualized_volatility, drawdown, rolling_volatility, sharpe_ratio


def test_drawdown_is_zero_when_price_is_at_new_peak():
    prices = pd.Series([100, 120, 130])  

    result = drawdown(prices)

    assert (result == 0).all()


def test_drawdown_compares_to_historical_peak_not_previous_price():
    prices = pd.Series([100, 120, 90, 95])  

    result = drawdown(prices)

    
    assert result.iloc[2] == pytest.approx(90 / 120 - 1)
    assert result.iloc[3] == pytest.approx(95 / 120 - 1)


def test_annualized_volatility_scales_std_by_sqrt_trading_days():
    returns = pd.Series([0.0, 0.02])

    result = annualized_volatility(returns)

    
    assert result == pytest.approx(0.2244994432064365)


def test_annualized_volatility_is_nan_with_single_data_point():
    returns = pd.Series([0.01])  

    result = annualized_volatility(returns)

    assert pd.isna(result)


def test_rolling_volatility_is_nan_before_window_is_filled():
    returns = pd.Series([0.01, 0.03, -0.01])

    result = rolling_volatility(returns, window=2)

    assert pd.isna(result.iloc[0])


def test_rolling_volatility_calculates_correct_value_once_window_fills():
    returns = pd.Series([0.01, 0.03, -0.01])

    result = rolling_volatility(returns, window=2)

    assert result.iloc[1] == pytest.approx(0.224499, rel=1e-4)
    assert result.iloc[2] == pytest.approx(0.448999, rel=1e-4)


def test_sharpe_ratio_calculates_correct_value():
    returns = pd.Series([0.01, 0.03, -0.01])

    result = sharpe_ratio(returns, risk_free_rate=0.1)

    assert result == pytest.approx(7.622283539019415)


def test_sharpe_ratio_is_nan_when_returns_have_zero_volatility():
    returns = pd.Series([0.01, 0.01, 0.01])  

    result = sharpe_ratio(returns)

    assert pd.isna(result)