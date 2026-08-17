import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from core.features.returns import daily_return, cumulative_return
from core.features.correlation import correlation_matrix
from dashboard.data_access import load_data, search_assets_cached, load_currency, load_fx_rate, load_risk_free_rate
from core.features.currency import convert_series
from core.features.portfolio import validate_weights, portfolio_returns, portfolio_volatility
from core.features.risk import sharpe_ratio, drawdown

TARGET_CURRENCY = "BRL"

def render():
    if "selected_assets" not in st.session_state:
      st.session_state.selected_assets = []

    query = st.text_input("Buscar ativo para adicionar")
    results = search_assets_cached(query)

    if results:
      labels = [f"{r['name']} ({r['ticker']})" for r in results]
      choice = st.selectbox("Resultados", options=labels)

      if st.button("Adicionar"):
          asset = results[labels.index(choice)]
          already_added = any(a["ticker"] == asset["ticker"] for a in st.session_state.selected_assets)
          if not already_added:
            st.session_state.selected_assets.append(asset)
    
    st.write("Ativos selecionados:")
    st.caption("Defina o peso (%) de cada ativo na carteira. Os pesos representam a distribuição do capital investido e devem somar 100%.")
    weights = []
    n_assets = len(st.session_state.selected_assets)
    for asset in st.session_state.selected_assets:
      col1, col2, col3 = st.columns([3, 1, 1])
      col1.write(f"{asset['name']} ({asset['ticker']})")
      weight_pct = col2.number_input(
        "Peso (%)",
        min_value=0.0, max_value=100.0, step=1.0,
        value=round(100 / n_assets, 2),
        key=f"weight_{asset['ticker']}",
        label_visibility="collapsed",
      )
      weights.append(weight_pct / 100)
      if col3.button("Remover", key=asset["ticker"]):
        st.session_state.selected_assets.remove(asset)
        st.rerun()

    st.title("Comparação entre ativos")

    if len(st.session_state.selected_assets) < 2:
      st.info("Adicione pelo menos 2 ativos para comparar.")
      return
    try:
      validate_weights(weights)
      weights_valid = True
    except ValueError as e:
      st.warning(str(e))
      weights_valid = False

    returns = {}
    for asset in st.session_state.selected_assets:
      ticker = asset["ticker"]

      try:
          prices = load_data(ticker)["Close"]
      except ValueError as e:
          st.error(str(e))
          return
      
      native_currency = load_currency(ticker)

      if native_currency != TARGET_CURRENCY:
        fx_rate = load_fx_rate(native_currency, TARGET_CURRENCY)
        prices = convert_series(prices, fx_rate)

      returns[asset["name"]] = daily_return(prices)

    returns_df = pd.concat(returns, axis=1)

    st.subheader("Retorno acumulado (normalizado)")
    cumulative = returns_df.apply(cumulative_return)
    st.line_chart(cumulative)

    st.subheader("Correlação entre retornos diários")
    corr = correlation_matrix(returns_df.dropna())

    fig, ax = plt.subplots()
    im = ax.imshow(corr, vmin=-1, vmax=1, cmap="coolwarm")
    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right")
    ax.set_yticklabels(corr.columns)
    for i in range(len(corr.columns)):
        for j in range(len(corr.columns)):
            ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center")
    fig.colorbar(im)
    st.pyplot(fig)

    st.subheader("Carteira")
    if not weights_valid:
      st.info("Ajuste os pesos para que somem 100% e veja as métricas da carteira.")
    else:
      aligned_returns = returns_df.dropna()
      port_returns = portfolio_returns(aligned_returns, weights)
      port_value = 1 + cumulative_return(port_returns)

      selic = load_risk_free_rate()
      vol = portfolio_volatility(aligned_returns, weights)
      sharpe = sharpe_ratio(port_returns, risk_free_rate=selic)

      col1, col2 = st.columns(2)
      col1.metric("Volatilidade anualizada", f"{vol:.1%}")
      col2.metric("Sharpe Ratio (anualizado)", f"{sharpe:.2f}")

      st.write("Evolução histórica da carteira")
      st.line_chart(port_value - 1)

      st.write("Drawdown da carteira")
      st.line_chart(drawdown(port_value))

render()