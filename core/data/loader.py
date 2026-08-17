import pandas as pd
import yfinance as yf

def get_historical_data(ticker: str, period: str = "5y", interval: str = "1d") -> pd.DataFrame:
  """
  Baixa um histórico de preços no yahoo finance

  Retorna um DataFrame com as colunas: Open, High, Close, Low e Volume,
  indexado por data. ValueError se o ticker não retornar nada.
  """
  data = yf.download(ticker, period = period, interval = interval, progress = False)

  if data.empty:
    raise ValueError(f"Nenhum dado retornado para o ticker '{ticker}'.")

  if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

  data = data.dropna()
  return data

def get_currency(ticker: str) -> str:
  """
  Descobre a moeda de um ativo
  """
  info = yf.Ticker(ticker).fast_info
  return info.get("currency", "USD")

