# 📈 Dashboard de Ações 2025

Dashboard interativo para análise da cotação e performance das principais ações brasileiras e latinoamericanas em 2025.

## Ações acompanhadas

| Empresa | Ticker |
|---|---|
| Petrobras | PETR4.SA |
| Itaú Unibanco | ITUB4.SA |
| MercadoLibre | MELI |
| Vale | VALE3.SA |

## Funcionalidades

- **Visão Geral** — métricas de retorno, máxima e mínima do período, e gráfico de performance comparativa normalizada (base 100)
- **Análise Individual** — gráfico candlestick e volume diário por ação
- **Correlação** — heatmap de correlação dos retornos diários entre as ações
- Filtro de período e seleção de ações pela sidebar
- Dados em tempo real via Yahoo Finance (cache de 1 hora)

## Instalação

```bash
pip install -r requirements.txt
```

## Como usar

```bash
streamlit run app.py
```

Acesse `http://localhost:8501` no browser.

## Stack

- [Streamlit](https://streamlit.io/) — framework web
- [yfinance](https://github.com/ranaroussi/yfinance) — dados históricos do Yahoo Finance
- [Plotly](https://plotly.com/python/) — gráficos interativos
- [pandas](https://pandas.pydata.org/) — manipulação de dados

---

Projeto criado pelo [Claude Code](https://claude.ai/code) via terminal.
