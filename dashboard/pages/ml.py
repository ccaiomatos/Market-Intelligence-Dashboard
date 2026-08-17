import pandas as pd
import streamlit as st

from core.features.returns import daily_return
from core.features.ml import build_features, build_latest_features
from core.models.predictor import train_model
from dashboard.data_access import load_data, search_assets_cached



def render():
    st.title("Machine Learning — Previsão de Tendência")
    st.caption(
        "Estimativa da probabilidade de alta com base em um modelo treinado com base nos padrões anteriores"
    )

    with st.form("busca_ativo"):
        query = st.text_input("Buscar ativo (ex: Petrobras, Apple, Bitcoin)")
        buscar = st.form_submit_button("Buscar")

    if not buscar or not query:
        st.info("Digite algo e clique em Buscar.")
        return

    results = search_assets_cached(query)
    if not results:
        st.warning("Nenhum ativo encontrado.")
        return

    labels = [f"{r['name']} ({r['ticker']})" for r in results]
    choice = st.selectbox("Resultados", options=labels)
    candidate = results[labels.index(choice)]

    if not st.button("Confirmar ativo"):
        st.stop()

    ticker = candidate["ticker"]

    try:
        prices = load_data(ticker)["Close"]
    except ValueError as e:
        st.error(str(e))
        return

    returns = daily_return(prices)

    features = build_features(returns, n_lags=5)

    if len(features) < 50:
        st.warning("Dados insuficientes para treinar o modelo com esse ativo.")
        return

    model, accuracy = train_model(features)

    st.metric("Acurácia no conjunto de teste", f"{accuracy:.1%}")
    st.caption(
        "Referência: 50% = mesmo que chute aleatório. "
        "Valores próximos disso são esperados em dados financeiros reais."
    )

    st.subheader("Importância das features")
    importances = pd.Series(
        model.feature_importances_, index=features.drop(columns="target").columns
    ).sort_values(ascending=False)
    st.bar_chart(importances)

    st.subheader("Previsão para o próximo dia")
    latest_features = build_latest_features(returns, n_lags=5)
    prediction = model.predict(latest_features)[0]
    proba = model.predict_proba(latest_features)[0]

    direction = "ALTA" if prediction == 1 else "BAIXA"
    st.metric("Direção prevista", direction, f"confiança: {max(proba):.1%}")


render()
