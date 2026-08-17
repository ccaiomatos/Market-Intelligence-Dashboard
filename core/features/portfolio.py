import numpy as np
import pandas as pd

from core.features.risk import TPY
def validate_weights(weights: list[float]) -> None:
  """
  Garante que os pesos da carteira somem 100%
  """
  total = sum(weights)
  if not np.isclose(total, 1.0, atol =0.01):
    raise ValueError(f"Os pesos devem somar 100%. Soma atual")

def portfolio_returns(return_by_asset: pd.DataFrame, weights: list[float]) -> pd.Series:
  """
  Retorno diário da carteira: soma ponderada do retorno diário de cada ativoo
  """
  return return_by_asset.mul(weights, axis=1).sum(axis=1)


def portfolio_volatility(returns_by_asset: pd.DataFrame, weights: list[float]) -> float:
  """
  Volatilidade anualizada da carteira via matriz de covariancia dos retornos diários: 
  variancia da carteira = w^T . Σ . w, onde · é a matriz de covariância. Diferente de uma média
  ponderada das volatilidades individuais, isso considera a correlação entre os ativos.
  """

  weights = np.array(weights)
  cov_matrix = returns_by_asset.cov()
  portfolio_variance = weights @ cov_matrix.values @ weights
  return np.sqrt(portfolio_variance) * np.sqrt(TPY)