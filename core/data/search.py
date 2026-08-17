import yfinance as yf

def search_assets(query:str) -> list[dict]:
  """
  Busca livre de ativos, retorna até 8 resultados com o nome
  e ticker individual
  """
  if not query:
    return []
  results = yf.Search(query, max_results=8).quotes
  return [{"name": r["shortname"], "ticker": r["symbol"]} for r in results]