import pandas as pd
import pytest

from core.features.correlation import correlation_matrix


def test_correlation_matrix_diagonal_is_always_one():
    returns_by_asset = pd.DataFrame({
        "ATIVO_A": [0.01, -0.02, 0.03, 0.01],
        "ATIVO_B": [0.02, 0.01, -0.01, 0.04],
    })

    result = correlation_matrix(returns_by_asset)

    assert result.loc["ATIVO_A", "ATIVO_A"] == pytest.approx(1.0)
    assert result.loc["ATIVO_B", "ATIVO_B"] == pytest.approx(1.0)


def test_correlation_matrix_identifies_perfect_positive_and_negative_correlation():
    ativo_a = [0.01, -0.02, 0.03, 0.01]
    returns_by_asset = pd.DataFrame({
        "ATIVO_A": ativo_a,
        "ATIVO_B": [v * 2 for v in ativo_a],   
        "ATIVO_C": [v * -1 for v in ativo_a],  
    })

    result = correlation_matrix(returns_by_asset)

    assert result.loc["ATIVO_A", "ATIVO_B"] == pytest.approx(1.0)
    assert result.loc["ATIVO_A", "ATIVO_C"] == pytest.approx(-1.0)