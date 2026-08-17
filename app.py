import streamlit as st

st.set_page_config(page_title="Market Intelligence Dashboard", layout = "wide")


pages = [
    st.Page("dashboard/pages/home.py", title="Visão Geral"),
    st.Page("dashboard/pages/comparison.py", title="Comparação"),
    st.Page("dashboard/pages/ml.py", title="Machine Learning"),
]

nav = st.navigation(pages)
nav.run()
