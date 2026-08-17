import pandas as pd

def daily_return(prices: pd.Series) -> pd.Series:
  """
  Retorno percentual dia a dia: (preço hoje / preço ontem) - 1.
  """
  return prices.pct_change()

def cumulative_return(returns: pd.Series) -> pd.Series:
  """
  Retorno acumulado a partir de uma série de retornos diários.
  """
  return (1 + returns.fillna(0)).cumprod() - 1