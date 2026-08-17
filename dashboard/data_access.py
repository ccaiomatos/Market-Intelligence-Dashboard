import streamlit as st

from core.data.loader import get_historical_data, get_currency
from core.data.selic import get_selic_rate
from core.data.search import search_assets
from core.data.fx import get_fx_rate

@st.cache_data(ttl=3600)
def load_data(ticker: str):
    return get_historical_data(ticker)

@st.cache_data(ttl=86400)
def load_risk_free_rate():
    return get_selic_rate()

@st.cache_data(ttl=3600)
def search_assets_cached(query: str):
    return search_assets(query)

@st.cache_data(ttl=86400)
def load_currency(ticker: str) -> str:
    return get_currency(ticker)


@st.cache_data(ttl=3600)
def load_fx_rate(from_currency: str, to_currency: str):
    return get_fx_rate(from_currency, to_currency)
