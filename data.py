import streamlit as st
import yfinance as yf
import pandas as pd


TICKERS = {
    "PETR4.SA": "Petrobras",
    "ITUB4.SA": "Itaú",
    "MELI": "MercadoLibre",
    "VALE3.SA": "Vale",
}


@st.cache_data(ttl=3600)
def load_data(tickers: list[str], start: str, end: str) -> dict[str, pd.DataFrame]:
    result = {}
    for ticker in tickers:
        df = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=True)
        if not df.empty:
            df.index = pd.to_datetime(df.index)
            result[ticker] = df
    return result
