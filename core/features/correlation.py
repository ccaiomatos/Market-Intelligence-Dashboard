import pandas as pd

def correlation_matrix(returns_by_asset: pd.DataFrame) -> pd.DataFrame:
  """
  Recebe um DataFrame onde cada coluna são os retornos diários de um ativo 
  (mesmo indice de datas) e devolve uma matrix de correlação entre eles.
  """
  return returns_by_asset.corr()