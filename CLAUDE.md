# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository

GitHub: https://github.com/douglasmodolo/acoes-2025-dashboard

**After every change to the project, commit and push to GitHub:**

```bash
git add -p                        # stage changes selectively
git commit -m "descrição clara"
git push
```

`gh` CLI is required for repo management. If `gh` is not on PATH in PowerShell, reload with:
```powershell
$env:PATH = [System.Environment]::GetEnvironmentVariable("PATH","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH","User")
```

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app runs at `http://localhost:8501` by default.

## Architecture

Three-file separation of concerns:

- **`data.py`** — data layer. `TICKERS` dict maps Yahoo Finance ticker symbols to display names. `load_data()` fetches OHLCV data via `yfinance` and is cached with `@st.cache_data(ttl=3600)` to avoid repeated network calls during a session.

- **`charts.py`** — presentation layer. Pure functions that each receive `data: dict[str, pd.DataFrame]` or a single `df` + `ticker` and return a `go.Figure`. No Streamlit calls here. Uses `df["Close"].squeeze()` everywhere because `yfinance` returns single-ticker DataFrames with a MultiIndex column that must be flattened.

- **`app.py`** — UI layer. Sidebar controls (date range, multiselect) drive `load_data()`, then routes to three tabs: Visão Geral (metrics + normalized performance), Análise Individual (candlestick + volume per ticker), Correlação (return heatmap).

## Key conventions

- All chart colors: green `#26a69a`, red `#ef5350`.
- Performance chart normalizes closing prices to base 100 on the first trading day of the selected period — this is intentional so stocks with very different price levels can be compared on the same axis.
- Volume bars are colored by the sign of the day's return, not absolute volume.
- To add a new stock, add it to `TICKERS` in `data.py` only — the rest of the app is driven by that dict.
