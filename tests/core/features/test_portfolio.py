import pandas as pd
import pytest

from core.features.portfolio import portfolio_returns, portfolio_volatility, validate_weights
from core.features.risk import annualized_volatility


def test_validate_weights_accepts_weights_that_sum_to_one():
    weights = [0.5, 0.3, 0.2]

    validate_weights(weights)  


def test_validate_weights_rejects_weights_that_dont_sum_to_one():
    weights = [0.5, 0.3, 0.1]  # soma 0.9, não 1.0

    with pytest.raises(ValueError):
        validate_weights(weights)


def test_portfolio_returns_calculates_weighted_sum():
    returns_by_asset = pd.DataFrame({
        "ATIVO_A": [0.10, 0.20],
        "ATIVO_B": [0.30, 0.00],
    })
    weights = [0.5, 0.5]

    result = portfolio_returns(returns_by_asset, weights)


    assert result.iloc[0] == pytest.approx(0.20)
    assert result.iloc[1] == pytest.approx(0.10)


def test_portfolio_returns_ignores_asset_with_zero_weight():
    returns_by_asset = pd.DataFrame({
        "ATIVO_A": [0.10],
        "ATIVO_B": [999.0],  
    })
    weights = [1.0, 0.0]

    result = portfolio_returns(returns_by_asset, weights)

    assert result.iloc[0] == pytest.approx(0.10)


def test_portfolio_volatility_calculates_correct_value():
    returns_by_asset = pd.DataFrame({
        "ATIVO_A": [0.01, 0.02, -0.01, 0.03],
        "ATIVO_B": [0.02, 0.01, 0.00, 0.01],
    })
    weights = [0.5, 0.5]

    result = portfolio_volatility(returns_by_asset, weights)

    assert result == pytest.approx(0.1759971590679804)


def test_portfolio_volatility_matches_single_asset_volatility_when_fully_concentrated():
    asset_returns = pd.Series([0.01, 0.02, -0.01, 0.03])
    returns_by_asset = pd.DataFrame({
        "ATIVO_A": asset_returns,
        "ATIVO_B": [0.02, 0.01, 0.00, 0.01],  
    })

    result = portfolio_volatility(returns_by_asset, weights=[1.0, 0.0])

    assert result == pytest.approx(annualized_volatility(asset_returns))