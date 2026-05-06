import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from data import TICKERS


def _label(ticker: str) -> str:
    return TICKERS.get(ticker, ticker)


def performance_chart(data: dict[str, pd.DataFrame]) -> go.Figure:
    fig = go.Figure()
    for ticker, df in data.items():
        close = df["Close"].squeeze()
        normalized = (close / close.iloc[0]) * 100
        fig.add_trace(go.Scatter(
            x=normalized.index,
            y=normalized,
            name=_label(ticker),
            mode="lines",
        ))
    fig.update_layout(
        title="Performance Comparativa (base 100)",
        xaxis_title="Data",
        yaxis_title="Índice (base 100)",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def candlestick_chart(df: pd.DataFrame, ticker: str) -> go.Figure:
    fig = go.Figure(go.Candlestick(
        x=df.index,
        open=df["Open"].squeeze(),
        high=df["High"].squeeze(),
        low=df["Low"].squeeze(),
        close=df["Close"].squeeze(),
        name=_label(ticker),
        increasing_line_color="#26a69a",
        decreasing_line_color="#ef5350",
    ))
    fig.update_layout(
        title=f"Candlestick — {_label(ticker)} ({ticker})",
        xaxis_title="Data",
        yaxis_title="Preço",
        xaxis_rangeslider_visible=False,
    )
    return fig


def volume_chart(df: pd.DataFrame, ticker: str) -> go.Figure:
    volume = df["Volume"].squeeze()
    colors = ["#26a69a" if v >= 0 else "#ef5350" for v in df["Close"].squeeze().pct_change().fillna(0)]
    fig = go.Figure(go.Bar(
        x=df.index,
        y=volume,
        name="Volume",
        marker_color=colors,
    ))
    fig.update_layout(
        title=f"Volume Diário — {_label(ticker)}",
        xaxis_title="Data",
        yaxis_title="Volume",
    )
    return fig


def correlation_heatmap(data: dict[str, pd.DataFrame]) -> go.Figure:
    returns = pd.DataFrame({
        _label(ticker): df["Close"].squeeze().pct_change()
        for ticker, df in data.items()
    }).dropna()

    corr = returns.corr()
    fig = px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale="RdBu",
        zmin=-1,
        zmax=1,
        title="Correlação dos Retornos Diários",
    )
    fig.update_layout(coloraxis_showscale=True)
    return fig
