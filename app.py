import streamlit as st
import datetime
from data import load_data, TICKERS
from charts import performance_chart, candlestick_chart, volume_chart, correlation_heatmap

st.set_page_config(
    page_title="Ações 2025",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Dashboard de Ações — 2025")
st.caption("Petrobras · Itaú · MercadoLibre · Vale")

# Sidebar
with st.sidebar:
    st.header("Filtros")
    start_date = st.date_input("Data inicial", value=datetime.date(2025, 1, 2))
    end_date = st.date_input("Data final", value=datetime.date(2025, 12, 31))

    ticker_options = list(TICKERS.keys())
    ticker_labels = list(TICKERS.values())
    selected_labels = st.multiselect(
        "Ações",
        options=ticker_labels,
        default=ticker_labels,
    )
    selected_tickers = [t for t, l in TICKERS.items() if l in selected_labels]

if not selected_tickers:
    st.warning("Selecione ao menos uma ação na sidebar.")
    st.stop()

if start_date >= end_date:
    st.error("A data inicial deve ser anterior à data final.")
    st.stop()

with st.spinner("Carregando dados do Yahoo Finance..."):
    data = load_data(selected_tickers, str(start_date), str(end_date))

if not data:
    st.error("Não foi possível carregar dados. Verifique sua conexão.")
    st.stop()

# Tabs
tab1, tab2, tab3 = st.tabs(["Visão Geral", "Análise Individual", "Correlação"])

with tab1:
    cols = st.columns(len(data))
    for col, (ticker, df) in zip(cols, data.items()):
        close = df["Close"].squeeze()
        price_start = close.iloc[0]
        price_end = close.iloc[-1]
        pct = (price_end / price_start - 1) * 100
        col.metric(
            label=TICKERS[ticker],
            value=f"{price_end:.2f}",
            delta=f"{pct:+.2f}%",
        )

    st.plotly_chart(performance_chart(data), use_container_width=True)

    with st.expander("Estatísticas do período"):
        rows = []
        for ticker, df in data.items():
            close = df["Close"].squeeze()
            rows.append({
                "Ação": TICKERS[ticker],
                "Ticker": ticker,
                "Abertura": f"{close.iloc[0]:.2f}",
                "Fechamento": f"{close.iloc[-1]:.2f}",
                "Máxima": f"{close.max():.2f}",
                "Mínima": f"{close.min():.2f}",
                "Retorno %": f"{(close.iloc[-1] / close.iloc[0] - 1) * 100:+.2f}%",
            })
        st.dataframe(rows, use_container_width=True, hide_index=True)

with tab2:
    label_to_ticker = {v: k for k, v in TICKERS.items() if k in data}
    available_labels = [TICKERS[t] for t in data]
    selected_label = st.selectbox("Selecione a ação", options=available_labels)
    selected_ticker = label_to_ticker[selected_label]
    df = data[selected_ticker]

    st.plotly_chart(candlestick_chart(df, selected_ticker), use_container_width=True)
    st.plotly_chart(volume_chart(df, selected_ticker), use_container_width=True)

with tab3:
    if len(data) < 2:
        st.info("Selecione ao menos duas ações para ver a correlação.")
    else:
        st.plotly_chart(correlation_heatmap(data), use_container_width=True)
        st.caption(
            "Correlação de 1.0 = movimentos idênticos · -1.0 = movimentos opostos · 0 = sem relação linear"
        )
