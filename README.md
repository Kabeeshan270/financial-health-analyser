# Financial Health Analyser

A Python web application that pulls real financial statements for any US-listed company and automatically calculates key accounting ratios, trends, and an overall financial health score.

Built as a portfolio project to demonstrate applied financial analysis and Python development skills.

## What it does

- Fetches live income statements, balance sheets, and cash flow statements via the Yahoo Finance API
- Calculates 8 financial ratios across three categories: liquidity, profitability, and leverage
- Plots 5-year ratio trends with industry benchmark lines for context
- Generates a weighted financial health score (0–100) across all three categories
- Compares two companies side by side with an auto-generated summary

## Ratios calculated

**Liquidity**
- Current Ratio
- Quick Ratio

**Profitability**
- Gross Margin
- Net Margin
- Return on Equity (ROE)
- Return on Assets (ROA)

**Leverage**
- Debt to Equity
- Interest Coverage

## Health score methodology

Each ratio is scored 0–100 based on its distance from an industry benchmark. Category scores are averaged within each group, then combined using a weighted formula:

- Liquidity: 30%
- Profitability: 40%
- Leverage: 30%

This is a simplified quantitative model intended as a starting point for analysis, not a substitute for a full credit or equity assessment.

## Tech stack

- Python 3.14
- Streamlit — web interface
- yfinance — financial data via Yahoo Finance API
- Plotly — interactive charts
- Pandas — data manipulation

## How to run locally

1. Clone the repository
```bash
git clone https://github.com/Kabeeshan270/financial-health-analyser.git
cd financial-health-analyser
```

2. Install dependencies
```bash
pip3 install streamlit yfinance plotly pandas
```

3. Run the app
```bash
streamlit run app.py
```

4. Open your browser at `http://localhost:8501`

## Example analysis

Analysing NVDA (NVIDIA Corporation) as of June 2026:

- Current Ratio: 3.91 — strong short-term liquidity
- Net Margin: 55.6% — exceptional profitability
- Debt to Equity: 0.07 — minimal leverage
- Overall Health Score: 93.9 / 100 (Excellent)