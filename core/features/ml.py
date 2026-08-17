import pandas as pd
import numpy as np

def build_features(returns: pd.Series, n_lags: int = 5) -> pd.DataFrame:
  """
  Constrói um DataFrame de treino/teste a partir dos retornos diários.
  lag_N = retorno de N dias atrás.
  O dia mais recente (cujo "amanhã" não existe ainda nos dados) tem target = Nan
  propositalmente, e por isso deve ser descartado pelo dropna() para não entrar 
  no treino como rótulo descartado.
  """
  df = pd.DataFrame(index = returns.index)

  for lag in range(1, n_lags + 1):
    df[f"lag_{lag}"] = returns.shift(lag)

  future_return = returns.shift(-1)
  df["target"] = np.where(future_return > 0, 1, 0).astype(float)
  df.loc[future_return.isna(), "target"] = np.nan

  return df.dropna()

def build_latest_features(returns: pd.Series, n_lags: int = 5) -> pd.DataFrame:
  """
  Constrói uma linha de features do dia mais recente disponível, para 
  ser usada em inferência.
  """
  last_date = returns.index[-1]
  row = {
    f"lag_{lag}": returns.shift(lag).loc[last_date]
    for lag in range(1, n_lags + 1)
  }
  return pd.DataFrame([row], index=[last_date])