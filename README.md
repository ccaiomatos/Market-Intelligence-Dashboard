# Market Intelligence Dashboard

Dashboard de análise quantitativa de ativos financeiros (ações, cripto, índices),
construído em Python + Streamlit.

## Objetivo

Projeto de portfólio para demonstrar análise de dados, estatística financeira
e um pipeline simples de Machine Learning — não é um sistema de trading.

## Stack

Python · Streamlit · Pandas · NumPy · Matplotlib · yfinance · scikit-learn

## Como rodar

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Estrutura

```
core/        # lógica de negócio (dados, features, modelos) — sem Streamlit
dashboard/   # camada de apresentação (páginas Streamlit)
config/      # constantes e configurações (ex: ativos disponíveis)
app.py       # ponto de entrada
```

## Status

🚧 Em desenvolvimento.
