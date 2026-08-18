import unicodedata

import yfinance as yf

_ALIASES: dict[str, list[dict]] = {
  """
  Dicionário com apelidos comuns de empresas -> ticker B3.
  """
  "petrobras": [
    {"name": "Petróleo Brasileiro S.A. - Petrobras", "ticker": "PETR4.SA"},
    {"name": "Petróleo Brasileiro S.A. - Petrobras (ON)", "ticker": "PETR3.SA"},
  ],
  "vale": [{"name": "Vale S.A.", "ticker": "VALE3.SA"}],
  "itau": [{"name": "Itaú Unibanco Holding S.A.", "ticker": "ITUB4.SA"}],
  "bradesco": [{"name": "Banco Bradesco S.A.", "ticker": "BBDC4.SA"}],
  "banco do brasil": [{"name": "Banco do Brasil S.A.", "ticker": "BBAS3.SA"}],
  "ambev": [{"name": "Ambev S.A.", "ticker": "ABEV3.SA"}],
  "magazine luiza": [{"name": "Magazine Luiza S.A.", "ticker": "MGLU3.SA"}],
  "magalu": [{"name": "Magazine Luiza S.A.", "ticker": "MGLU3.SA"}],
  "weg": [{"name": "WEG S.A.", "ticker": "WEGE3.SA"}],
  "b3": [{"name": "B3 S.A. - Brasil, Bolsa, Balcão", "ticker": "B3SA3.SA"}],
  "gerdau": [{"name": "Gerdau S.A.", "ticker": "GGBR4.SA"}],
  "jbs": [{"name": "JBS S.A.", "ticker": "JBSS3.SA"}],
  "localiza": [{"name": "Localiza Rent a Car S.A.", "ticker": "RENT3.SA"}],
  "natura": [{"name": "Natura &Co Holding S.A.", "ticker": "NTCO3.SA"}],
  "santander": [{"name": "Banco Santander (Brasil) S.A.", "ticker": "SANB11.SA"}],
}


def _normalize(text: str) -> str:
  """Remove acentos e caixa para permitir match tipo 'petrobras' == 'Petrobrás'."""
  nfkd = unicodedata.normalize("NFKD", text.strip().lower())
  return "".join(c for c in nfkd if not unicodedata.combining(c))


def _alias_matches(query: str) -> list[dict]:
  norm_query = _normalize(query)
  matches = []
  for alias, entries in _ALIASES.items():
    if alias in norm_query or norm_query in alias:
      matches.extend(entries)
  return matches


def search_assets(query: str) -> list[dict]:
  """
  Busca livre de ativos, retorna até 8 resultados com o nome
  e ticker individual.
  """
  if not query:
    return []

  results = list(_alias_matches(query))

  try:
    yahoo_quotes = yf.Search(query, max_results=8, enable_fuzzy_query=True).quotes
  except Exception:
    yahoo_quotes = []

  seen_tickers = {r["ticker"] for r in results}
  for r in yahoo_quotes:
    ticker = r.get("symbol")
    name = r.get("shortname")
    if not ticker or not name or ticker in seen_tickers:
      continue
    results.append({"name": name, "ticker": ticker})
    seen_tickers.add(ticker)

  return results[:8]