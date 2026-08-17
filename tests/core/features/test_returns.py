import pandas as pd
import pytest

from core.features.returns import cumulative_return, daily_return


def test_daily_return_calculates_correct_percentage():
    prices = pd.Series([100, 110, 99])

    result = daily_return(prices)

    # 100 -> 110 = +10% | 110 -> 99 = -10%
    assert result.iloc[1] == pytest.approx(0.10)
    assert result.iloc[2] == pytest.approx(-0.10)


def test_daily_return_first_value_is_nan():
    prices = pd.Series([100, 110, 99])

    result = daily_return(prices)

    assert pd.isna(result.iloc[0])


def test_cumulative_return_compounds_instead_of_summing():
    returns = pd.Series([0.10, 0.10])  # dois dias seguidos de +10%

    result = cumulative_return(returns)

    # 1.10 * 1.10 - 1 = 0.21, e não 0.10 + 0.10 = 0.20
    assert result.iloc[1] == pytest.approx(0.21)


def test_cumulative_return_treats_leading_nan_as_zero():
    returns = pd.Series([float("nan"), 0.10])

    result = cumulative_return(returns)

    assert result.iloc[0] == 0.0