import numpy as np
import pandas as pd

TPY = 252 # TRADES PER YEAR

def rolling_volatility(returns:pd.Series, window: int = 21) -> pd.Series:
  """
  Volatilidade móvel: desvio padrão dos retornos diários em uma janela
  (default 21 dias), anualizada.
  """
  return returns.rolling(window).std() * np.sqrt(TPY)

def annualized_volatility(returns: pd.Series) -> float:
  """ Volatilidade anual considerando todo o período disponível"""
  return returns.std() * np.sqrt(TPY)

def drawdown(prices: pd.Series) -> pd.Series:
  """
  Drawndown: queda percentual em relação ao pico histórico. 
  Sempre <= 0
  """
  running_max = prices.cummax()
  return (prices / running_max) - 1

def sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.1) -> float:
  """
  Retorno médio a cada unidade de risco (retorno médio acima do "livre de risco"
  dividido pela volatilidade)
  """
  excess_daily_rf = risk_free_rate / TPY
  excess_return = returns.mean() - excess_daily_rf

  if returns.std() == 0:
    return np.nan
  
  return (excess_return / returns.std()) * np.sqrt(TPY)