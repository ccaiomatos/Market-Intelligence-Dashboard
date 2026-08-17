import pandas as pd


def convert_series(prices: pd.Series, fx_rate: pd.Series) -> pd.Series:
    """
    Converte uma série de preços para outra moeda, usando a série de
    câmbio fornecida. 
    """
    aligned_rate = fx_rate.reindex(prices.index, method="ffill")
    return prices * aligned_rate