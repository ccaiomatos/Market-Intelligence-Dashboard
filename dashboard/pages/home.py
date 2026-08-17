import streamlit as st

from core.features.returns import daily_return, cumulative_return
from core.features.risk import rolling_volatility, drawdown, sharpe_ratio
from dashboard.data_access import load_data, load_risk_free_rate, search_assets_cached


def render():
  st.title("Market Intelligence Dashboard")

  query = st.text_input("Buscar ativo (ex: Petrobras, Apple, Bitcoin)")
  results = search_assets_cached(query)

  if not results:
      st.info("Digite algo pra buscar um ativo.")
      return

  labels = [f"{r['name']} ({r['ticker']})" for r in results]
  choice = st.selectbox("Resultados", options=labels)
  candidate = results[labels.index(choice)]

  if not st.button("Confirmar ativo"):
    st.stop() 
  
  asset_name = candidate["name"]
  ticker = candidate["ticker"]

  try:
    df = load_data(ticker)
  except ValueError as e:
    st.error(str(e))
    return

  st.subheader(f"Últimos preços — {asset_name}")
  st.dataframe(df.tail(10))
  st.line_chart(df["Close"])

  df["daily_return"] = daily_return(df["Close"])
  df["cumulative_return"] = cumulative_return(df["daily_return"])

  st.subheader("Retorno acumulado")
  st.line_chart(df["cumulative_return"])

  df["volatility"] = rolling_volatility(df["daily_return"])
  df["drawdown"] = drawdown(df["Close"])

  col1, col2 = st.columns(2)
  with col1:
      st.subheader("Volatilidade (janela 21d, anualizada)")
      st.line_chart(df["volatility"])
  with col2:
      st.subheader("Drawdown")
      st.line_chart(df["drawdown"])

  selic = load_risk_free_rate()
  sharpe = sharpe_ratio(df["daily_return"].dropna(), risk_free_rate=selic)
  st.metric("Sharpe Ratio (anualizado)", f"{sharpe:.2f}")

render()