import pandas as pd

from core.data.loader import get_historical_data


def get_fx_rate(from_currency: str, to_currency: str, period: str = "5y") -> pd.Series:
    """
    Busca a série histórica de câmbio from_currency -> to_currency.

    Tenta o par direto no Yahoo Finance. Se o par não
    existir nessa direção, tenta o par invertido e inverte a série
    (1 / taxa).
    """
    try:
        return get_historical_data(f"{from_currency}{to_currency}=X", period=period)["Close"]
    except ValueError:
        inverted = get_historical_data(f"{to_currency}{from_currency}=X", period=period)["Close"]
        return 1 / inverted