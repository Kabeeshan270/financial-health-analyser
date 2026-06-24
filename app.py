import yfinance as yf
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# force background colour via injected style tag
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"], [data-testid="stAppViewBlockContainer"],
[data-testid="stVerticalBlock"], .stApp, .main, .block-container {
    background-color: #f1f5f9 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Financial Health Analyser",
    layout="wide"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* hide default streamlit header and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* page background — force override all streamlit wrappers */
    .stApp, .stApp > div, .stApp > div > div,
    .block-container, [data-testid="stAppViewContainer"],
    [data-testid="stAppViewBlockContainer"],
    [data-testid="stVerticalBlock"] {
        background-color: #f1f5f9 !important;
    }

    /* hero header */
    .hero {
        background: #0f172a;
        padding: 2rem 2rem 1.75rem;
        border-radius: 14px;
        margin-bottom: 1.5rem;
    }
    .hero-label {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.1em;
        color: #475569;
        text-transform: uppercase;
        margin-bottom: 6px;
    }
    .hero-title {
        font-size: 28px;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 4px;
    }
    .hero-sub {
        font-size: 13px;
        color: #64748b;
        margin-bottom: 1.25rem;
    }
    .badge-row {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
        margin-bottom: 1.5rem;
    }
    .badge {
        font-size: 11px;
        font-weight: 600;
        padding: 4px 12px;
        border-radius: 20px;
    }
    .badge-blue  { background: #1e3a5f; color: #93c5fd; }
    .badge-green { background: #14532d; color: #86efac; }
    .badge-gray  { background: #1e293b; color: #94a3b8; }
    .stat-row {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
    }
    .stat-card {
        background: #1e293b;
        border-radius: 10px;
        padding: 14px 16px;
    }
    .stat-label {
        font-size: 11px;
        color: #64748b;
        margin-bottom: 4px;
        font-weight: 500;
    }
    .stat-value {
        font-size: 22px;
        font-weight: 700;
        color: #f8fafc;
    }
    .stat-sub {
        font-size: 11px;
        color: #475569;
        margin-top: 2px;
    }

    /* section headers */
    .section-title {
        font-size: 15px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 2px;
        margin-top: 0.25rem;
    }
    .section-cap {
        font-size: 12px;
        color: #64748b;
        margin-bottom: 14px;
    }

    /* metric cards */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 10px;
        margin-bottom: 12px;
    }
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 14px 16px;
    }
    .metric-label {
        font-size: 11px;
        color: #64748b;
        font-weight: 600;
        margin-bottom: 6px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-value-green  { font-size: 24px; font-weight: 700; color: #16a34a; margin-bottom: 4px; }
    .metric-value-red    { font-size: 24px; font-weight: 700; color: #dc2626; margin-bottom: 4px; }
    .metric-value-amber  { font-size: 24px; font-weight: 700; color: #d97706; margin-bottom: 4px; }
    .metric-delta-up     { font-size: 11px; color: #16a34a; }
    .metric-delta-down   { font-size: 11px; color: #dc2626; }
    .metric-bench        { font-size: 10px; color: #94a3b8; margin-top: 4px; }

    /* interpretation panels */
    .interpretation {
        border-left: 3px solid #3b82f6;
        background: #eff6ff;
        padding: 10px 14px;
        border-radius: 0 8px 8px 0;
        font-size: 13px;
        color: #1e40af;
        line-height: 1.6;
        margin-top: 8px;
    }

    /* health score */
    .score-wrapper {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        display: flex;
        align-items: center;
        gap: 2rem;
        margin-bottom: 12px;
    }
    .score-big   { font-size: 52px; font-weight: 800; color: #16a34a; line-height: 1; }
    .score-label { font-size: 13px; font-weight: 700; color: #16a34a; margin-top: 4px; }
    .score-bars  { flex: 1; display: flex; flex-direction: column; gap: 10px; }
    .bar-row     { display: flex; align-items: center; gap: 10px; font-size: 12px; }
    .bar-label   { width: 100px; color: #64748b; flex-shrink: 0; font-weight: 500; }
    .bar-track   { flex: 1; height: 6px; background: #e2e8f0; border-radius: 3px; overflow: hidden; }
    .bar-fill-green { height: 100%; border-radius: 3px; background: #16a34a; }
    .bar-fill-blue  { height: 100%; border-radius: 3px; background: #2563eb; }
    .bar-fill-amber { height: 100%; border-radius: 3px; background: #d97706; }
    .bar-fill-red   { height: 100%; border-radius: 3px; background: #dc2626; }
    .bar-val     { width: 40px; text-align: right; font-weight: 700; color: #374151; font-size: 12px; }

    /* divider */
    .divider { height: 1px; background: #e2e8f0; margin: 1.5rem 0; }
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ════════════════════════════════════════════════════════════════════════════════

def get_row(df, row_name):
    if row_name in df.index:
        return df.loc[row_name]
    return None

def safe_divide(a, b):
    try:
        if b is None or a is None:
            return None
        result = a / b
        result = result.replace([float('inf'), float('-inf')], None)
        return result
    except:
        return None

def format_large_number(n):
    if n is None:
        return "N/A"
    if abs(n) >= 1e12:
        return f"${n/1e12:.2f}T"
    elif abs(n) >= 1e9:
        return f"${n/1e9:.2f}B"
    elif abs(n) >= 1e6:
        return f"${n/1e6:.2f}M"
    else:
        return f"${n:,.0f}"

def yoy_delta(series):
    try:
        latest   = series.iloc[0]
        previous = series.iloc[1]
        if latest is None or previous is None:
            return None, None
        delta = latest - previous
        return delta, delta >= 0
    except:
        return None, None

def score_ratio(value, benchmark, higher_is_better=True, max_multiplier=3):
    if value is None:
        return 50
    if higher_is_better:
        ratio = value / benchmark if benchmark != 0 else 1
    else:
        ratio = benchmark / value if value != 0 else 1
    score = min(100, max(0, (ratio / max_multiplier) * 100))
    return round(score, 1)

def fetch_and_calculate(ticker_str):
    # fetches all data and calculates all ratios for a given ticker
    # returns a dictionary of everything we need so we can cache it in session_state
    ticker        = yf.Ticker(ticker_str)
    info          = ticker.info
    balance_sheet = ticker.balance_sheet
    income_stmt   = ticker.income_stmt
    cashflow      = ticker.cashflow

    if balance_sheet.empty:
        return None

    # ratios
    ca   = get_row(balance_sheet, "Current Assets")
    cl   = get_row(balance_sheet, "Current Liabilities")
    inv  = get_row(balance_sheet, "Inventory")
    cr   = safe_divide(ca, cl)
    qa   = (ca - inv) if inv is not None and ca is not None else ca
    qr   = safe_divide(qa, cl)

    gp   = get_row(income_stmt, "Gross Profit")
    rev  = get_row(income_stmt, "Total Revenue")
    ni   = get_row(income_stmt, "Net Income")
    gm   = safe_divide(gp, rev)
    nm   = safe_divide(ni, rev)

    eq   = get_row(balance_sheet, "Stockholders Equity")
    ta   = get_row(balance_sheet, "Total Assets")
    roe  = safe_divide(ni, eq)
    roa  = safe_divide(ni, ta)

    td   = get_row(balance_sheet, "Total Debt")
    de   = safe_divide(td, eq)
    eb   = get_row(income_stmt, "EBIT")
    ie   = get_row(income_stmt, "Interest Expense")
    iep  = ie.abs() if ie is not None else None
    ic   = safe_divide(eb, iep)

    # scores
    cr_score  = score_ratio(cr.iloc[0]  if cr  is not None else None, 1.5)
    qr_score  = score_ratio(qr.iloc[0]  if qr  is not None else None, 1.0)
    gm_score  = score_ratio(gm.iloc[0]  if gm  is not None else None, 0.40)
    nm_score  = score_ratio(nm.iloc[0]  if nm  is not None else None, 0.10)
    roe_score = score_ratio(roe.iloc[0] if roe is not None else None, 0.15)
    roa_score = score_ratio(roa.iloc[0] if roa is not None else None, 0.05)
    de_score  = score_ratio(de.iloc[0]  if de  is not None else None, 2.0, higher_is_better=False)
    ic_score  = score_ratio(ic.iloc[0]  if ic  is not None else None, 3.0)

    liq_score  = round((cr_score + qr_score) / 2, 1)
    prof_score = round((gm_score + nm_score + roe_score + roa_score) / 4, 1)
    lev_score  = round((de_score + ic_score) / 2, 1)
    overall    = round((liq_score * 0.30) + (prof_score * 0.40) + (lev_score * 0.30), 1)

    return {
        "info": info, "balance_sheet": balance_sheet,
        "income_stmt": income_stmt, "cashflow": cashflow,
        "cr": cr, "qr": qr, "gm": gm, "nm": nm,
        "roe": roe, "roa": roa, "de": de, "ic": ic,
        "liq_score": liq_score, "prof_score": prof_score,
        "lev_score": lev_score, "overall": overall
    }

def latest_val(series, pct=False):
    try:
        v = series.iloc[0]
        if v is None:
            return "N/A"
        return f"{v*100:.1f}%" if pct else f"{v:.2f}"
    except:
        return "N/A"

# ════════════════════════════════════════════════════════════════════════════════
# HEADER
# ════════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div style="margin-bottom: 1.5rem;">
    <p style="font-size:11px; font-weight:600; letter-spacing:0.1em; color:#64748b; text-transform:uppercase; margin-bottom:4px;">Tool</p>
    <h1 style="font-size:28px; font-weight:700; color:#0f172a; margin-bottom:4px;">Financial Health Analyser</h1>
    <p style="font-size:14px; color:#64748b;">Enter any US-listed stock ticker to analyse liquidity, profitability, leverage, and overall financial health.</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    ticker_input = st.text_input(
        "Stock Ticker",
        value="NVDA",
        placeholder="e.g. NVDA, MSFT, JPM, GS"
    ).upper().strip()
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    analyse = st.button("Analyse", use_container_width=True)

# ── Store result in session state so comparison doesn't wipe it ───────────────
if analyse:
    with st.spinner(f"Fetching data for {ticker_input}..."):
        result = fetch_and_calculate(ticker_input)
    if result is None:
        st.error(f"No data found for **{ticker_input}**. Please check the ticker and try again.")
        st.stop()
    st.session_state["result"]       = result
    st.session_state["ticker_input"] = ticker_input

# ── Only render the rest if we have data ──────────────────────────────────────
if "result" not in st.session_state:
    st.stop()

result       = st.session_state["result"]
ticker_input = st.session_state["ticker_input"]

info          = result["info"]
balance_sheet = result["balance_sheet"]
income_stmt   = result["income_stmt"]
cashflow      = result["cashflow"]
cr            = result["cr"]
qr            = result["qr"]
gm            = result["gm"]
nm            = result["nm"]
roe           = result["roe"]
roa           = result["roa"]
de            = result["de"]
ic            = result["ic"]
liq_score     = result["liq_score"]
prof_score    = result["prof_score"]
lev_score     = result["lev_score"]
overall_score = result["overall"]

company_name = info.get("longName",          ticker_input)
sector       = info.get("sector",             "N/A")
industry     = info.get("industry",           "N/A")
country      = info.get("country",            "N/A")
exchange     = info.get("exchange",           "N/A")
share_price  = info.get("currentPrice",       info.get("regularMarketPrice", None))
market_cap   = info.get("marketCap",          None)
pe_ratio     = info.get("trailingPE",         None)
description  = info.get("longBusinessSummary","")
dates        = balance_sheet.columns.tolist()
date_labels  = [d.strftime("%b %Y") for d in dates]

# ════════════════════════════════════════════════════════════════════════════════
# COMPANY OVERVIEW
# ════════════════════════════════════════════════════════════════════════════════

st.markdown(f"""
<div style="background:#0f172a; padding:2rem; border-radius:14px; margin-bottom:1.5rem;">
    <p style="font-size:11px; font-weight:600; letter-spacing:0.1em; color:#475569; text-transform:uppercase; margin-bottom:6px;">Company Analysis</p>
    <h2 style="font-size:28px; font-weight:700; color:#f8fafc; margin-bottom:4px;">{company_name}</h2>
    <p style="font-size:13px; color:#64748b; margin-bottom:1.25rem;">Financial statements · Ratio analysis · Health score</p>
    <div style="display:flex; gap:8px; flex-wrap:wrap; margin-bottom:1.5rem;">
        <span style="font-size:11px; font-weight:600; padding:4px 12px; border-radius:20px; background:#1e3a5f; color:#93c5fd;">{ticker_input} · {exchange}</span>
        <span style="font-size:11px; font-weight:600; padding:4px 12px; border-radius:20px; background:#14532d; color:#86efac;">{industry}</span>
        <span style="font-size:11px; font-weight:600; padding:4px 12px; border-radius:20px; background:#1e293b; color:#94a3b8;">{country}</span>
    </div>
    <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:12px;">
        <div style="background:#1e293b; border-radius:10px; padding:14px 16px;">
            <p style="font-size:11px; color:#64748b; margin-bottom:4px; font-weight:500;">Share price</p>
            <p style="font-size:22px; font-weight:700; color:#f8fafc;">{"${:,.2f}".format(share_price) if share_price else "N/A"}</p>
            <p style="font-size:11px; color:#475569; margin-top:2px;">Live via Yahoo Finance</p>
        </div>
        <div style="background:#1e293b; border-radius:10px; padding:14px 16px;">
            <p style="font-size:11px; color:#64748b; margin-bottom:4px; font-weight:500;">Market cap</p>
            <p style="font-size:22px; font-weight:700; color:#f8fafc;">{format_large_number(market_cap)}</p>
            <p style="font-size:11px; color:#475569; margin-top:2px;">Latest filing</p>
        </div>
        <div style="background:#1e293b; border-radius:10px; padding:14px 16px;">
            <p style="font-size:11px; color:#64748b; margin-bottom:4px; font-weight:500;">P/E ratio</p>
            <p style="font-size:22px; font-weight:700; color:#f8fafc;">{f"{pe_ratio:.1f}x" if pe_ratio else "N/A"}</p>
            <p style="font-size:11px; color:#475569; margin-top:2px;">Trailing twelve months</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

if description:
    with st.expander("About this company"):
        st.write(description)

# ════════════════════════════════════════════════════════════════════════════════
# LIQUIDITY
# ════════════════════════════════════════════════════════════════════════════════

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<p class="section-title">Liquidity</p>', unsafe_allow_html=True)
st.markdown('<p class="section-cap">Can the company pay its short-term debts?</p>', unsafe_allow_html=True)

liq_col1, liq_col2 = st.columns(2)
with liq_col1:
    if cr is not None:
        val = cr.iloc[0]
        delta, improved = yoy_delta(cr)
        delta_str = f"{'+' if improved else ''}{delta:.2f} vs last year" if delta is not None else None
        st.metric("Current Ratio", f"{val:.2f}", delta=delta_str, help="Above 1.5 is healthy.")
with liq_col2:
    if qr is not None:
        val = qr.iloc[0]
        delta, improved = yoy_delta(qr)
        delta_str = f"{'+' if improved else ''}{delta:.2f} vs last year" if delta is not None else None
        st.metric("Quick Ratio", f"{val:.2f}", delta=delta_str, help="Above 1.0 is healthy.")

if cr is not None:
    cr_val = cr.iloc[0]
    if cr_val >= 2.0:
        liq_comment = f"With a current ratio of {cr_val:.2f}, {company_name} holds strong short-term liquidity — it can cover current liabilities {cr_val:.1f}x over, indicating very low near-term financial distress risk."
    elif cr_val >= 1.5:
        liq_comment = f"{company_name}'s current ratio of {cr_val:.2f} sits above the 1.5 benchmark, suggesting adequate short-term liquidity with a reasonable buffer against unexpected obligations."
    elif cr_val >= 1.0:
        liq_comment = f"A current ratio of {cr_val:.2f} means {company_name} can technically cover short-term liabilities, but the margin is thin — worth monitoring alongside cash flow trends."
    else:
        liq_comment = f"{company_name}'s current ratio of {cr_val:.2f} falls below 1.0, meaning current liabilities exceed current assets. This warrants close attention to near-term cash flow."
    st.markdown(f'<div class="interpretation">{liq_comment}</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# PROFITABILITY
# ════════════════════════════════════════════════════════════════════════════════

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<p class="section-title">Profitability</p>', unsafe_allow_html=True)
st.markdown('<p class="section-cap">How efficiently is the company generating profit?</p>', unsafe_allow_html=True)

pro_col1, pro_col2, pro_col3, pro_col4 = st.columns(4)
with pro_col1:
    if gm is not None:
        val = gm.iloc[0] * 100
        delta, improved = yoy_delta(gm * 100)
        delta_str = f"{'+' if improved else ''}{delta:.1f}% vs last year" if delta is not None else None
        st.metric("Gross Margin", f"{val:.1f}%", delta=delta_str)
with pro_col2:
    if nm is not None:
        val = nm.iloc[0] * 100
        delta, improved = yoy_delta(nm * 100)
        delta_str = f"{'+' if improved else ''}{delta:.1f}% vs last year" if delta is not None else None
        st.metric("Net Margin", f"{val:.1f}%", delta=delta_str)
with pro_col3:
    if roe is not None:
        val = roe.iloc[0] * 100
        delta, improved = yoy_delta(roe * 100)
        delta_str = f"{'+' if improved else ''}{delta:.1f}% vs last year" if delta is not None else None
        st.metric("ROE", f"{val:.1f}%", delta=delta_str)
with pro_col4:
    if roa is not None:
        val = roa.iloc[0] * 100
        delta, improved = yoy_delta(roa * 100)
        delta_str = f"{'+' if improved else''}{delta:.1f}% vs last year" if delta is not None else None
        st.metric("ROA", f"{val:.1f}%", delta=delta_str)

if nm is not None:
    nm_val  = nm.iloc[0] * 100
    roe_val = roe.iloc[0] * 100 if roe is not None else None
    if nm_val >= 20:
        prof_comment = f"{company_name} retains {nm_val:.1f}% of every dollar of revenue as net profit — well above the 10% benchmark. "
    elif nm_val >= 10:
        prof_comment = f"With a net margin of {nm_val:.1f}%, {company_name} clears the 10% benchmark, reflecting solid but not exceptional cost control. "
    else:
        prof_comment = f"A net margin of {nm_val:.1f}% falls below the 10% benchmark, suggesting pricing pressure or high operating costs relative to revenue. "
    if roe_val and roe_val >= 15:
        prof_comment += f"An ROE of {roe_val:.1f}% signals strong returns being generated on shareholder equity."
    st.markdown(f'<div class="interpretation">{prof_comment}</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# LEVERAGE
# ════════════════════════════════════════════════════════════════════════════════

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<p class="section-title">Leverage</p>', unsafe_allow_html=True)
st.markdown('<p class="section-cap">How much debt is the company carrying?</p>', unsafe_allow_html=True)


lev_col1, lev_col2 = st.columns(2)
with lev_col1:
    if de is not None:
        val = de.iloc[0]
        delta, improved = yoy_delta(de)
        delta_str = f"{'+' if improved else ''}{delta:.2f} vs last year" if delta is not None else None
        st.metric("Debt to Equity", f"{val:.2f}", delta=delta_str, delta_color="inverse")
with lev_col2:
    if ic is not None:
        val = ic.iloc[0]
        delta, improved = yoy_delta(ic)
        delta_str = f"{'+' if improved else ''}{delta:.2f} vs last year" if delta is not None else None
        st.metric("Interest Coverage", f"{val:.2f}x", delta=delta_str)

if de is not None:
    de_val = de.iloc[0]
    ic_val = ic.iloc[0] if ic is not None else None
    if de_val <= 0.5:
        lev_comment = f"{company_name}'s debt-to-equity ratio of {de_val:.2f} is exceptionally low, indicating the company operates almost entirely on equity with minimal reliance on debt financing. "
    elif de_val <= 1.5:
        lev_comment = f"A debt-to-equity ratio of {de_val:.2f} sits within a healthy range, suggesting a balanced capital structure without excessive leverage. "
    else:
        lev_comment = f"A debt-to-equity ratio of {de_val:.2f} is relatively high — the company is significantly debt-financed, which amplifies both potential returns and financial risk. "
    if ic_val and ic_val >= 3:
        lev_comment += f"An interest coverage ratio of {ic_val:.1f}x confirms the company can comfortably service its debt obligations."
    elif ic_val:
        lev_comment += f"An interest coverage ratio of {ic_val:.1f}x is below the 3.0 benchmark, suggesting limited headroom on debt servicing."
    st.markdown(f'<div class="interpretation">{lev_comment}</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# TREND CHARTS
# ════════════════════════════════════════════════════════════════════════════════

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<p class="section-title">5-Year Trends</p>', unsafe_allow_html=True)
st.caption("Green bars are above the healthy benchmark, red bars are below.")

def make_bar_chart(values, title, benchmark, y_format="ratio", color_inverse=False):
    if values is None:
        return None
    vals = [round(float(v), 4) if v is not None else None for v in values]
    bar_colors = []
    for v in vals:
        if v is None:
            bar_colors.append("#d1d5db")
        elif color_inverse:
            bar_colors.append("#22c55e" if v <= benchmark else "#ef4444")
        else:
            bar_colors.append("#22c55e" if v >= benchmark else "#ef4444")
    if y_format == "percent":
        hover     = [f"{v*100:.1f}%" if v is not None else "N/A" for v in vals]
        y_vals    = [v * 100 if v is not None else None for v in vals]
        bench_val = benchmark * 100
        y_title   = "%"
    else:
        hover     = [f"{v:.2f}" if v is not None else "N/A" for v in vals]
        y_vals    = vals
        bench_val = benchmark
        y_title   = "ratio"
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=date_labels,
        y=y_vals,
        marker_color=bar_colors,
        name=title,
        hovertemplate="%{x}<br>" + title + ": %{customdata}<extra></extra>",
        customdata=hover
    ))
    fig.add_hline(
        y=bench_val,
        line_dash="dot",
        line_color="#6b7280",
        line_width=1.5,
        annotation_text=f"Benchmark: {bench_val}{'%' if y_format == 'percent' else ''}",
        annotation_position="top right",
        annotation_font_size=11,
        annotation_font_color="#6b7280"
    )
    fig.update_layout(
        template="plotly_white",
        title=dict(text=title, font=dict(size=14)),
        height=280,
        margin=dict(l=40, r=40, t=50, b=40),
        showlegend=False,
        yaxis=dict(title=y_title, tickfont=dict(size=11)),
        xaxis=dict(tickfont=dict(size=11)),
        plot_bgcolor="white",
        paper_bgcolor="white"
    )
    return fig

st.markdown("**Liquidity**")
chart_col1, chart_col2 = st.columns(2)
with chart_col1:
    fig = make_bar_chart(cr, "Current Ratio", benchmark=1.5)
    if fig:
        st.plotly_chart(fig, use_container_width=True)
with chart_col2:
    fig = make_bar_chart(qr, "Quick Ratio", benchmark=1.0)
    if fig:
        st.plotly_chart(fig, use_container_width=True)

st.markdown("**Profitability**")
chart_col3, chart_col4 = st.columns(2)
with chart_col3:
    fig = make_bar_chart(gm, "Gross Margin", benchmark=0.40, y_format="percent")
    if fig:
        st.plotly_chart(fig, use_container_width=True)
with chart_col4:
    fig = make_bar_chart(nm, "Net Margin", benchmark=0.10, y_format="percent")
    if fig:
        st.plotly_chart(fig, use_container_width=True)

chart_col5, chart_col6 = st.columns(2)
with chart_col5:
    fig = make_bar_chart(roe, "Return on Equity (ROE)", benchmark=0.15, y_format="percent")
    if fig:
        st.plotly_chart(fig, use_container_width=True)
with chart_col6:
    fig = make_bar_chart(roa, "Return on Assets (ROA)", benchmark=0.05, y_format="percent")
    if fig:
        st.plotly_chart(fig, use_container_width=True)

st.markdown("**Leverage**")
chart_col7, chart_col8 = st.columns(2)
with chart_col7:
    fig = make_bar_chart(de, "Debt to Equity", benchmark=2.0, color_inverse=True)
    if fig:
        st.plotly_chart(fig, use_container_width=True)
with chart_col8:
    fig = make_bar_chart(ic, "Interest Coverage", benchmark=3.0)
    if fig:
        st.plotly_chart(fig, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════════
# HEALTH SCORE
# ════════════════════════════════════════════════════════════════════════════════

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<p class="section-title">Overall Financial Health Score</p>', unsafe_allow_html=True)
st.markdown('<p class="section-cap">Weighted across liquidity (30%), profitability (40%), and leverage (30%). Simplified model — not a credit rating.</p>', unsafe_allow_html=True)

if overall_score >= 80:
    score_label = "Excellent"
    score_color = "#22c55e"
elif overall_score >= 60:
    score_label = "Good"
    score_color = "#3b82f6"
elif overall_score >= 40:
    score_label = "Fair"
    score_color = "#f59e0b"
else:
    score_label = "Weak"
    score_color = "#ef4444"

gauge_fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=overall_score,
    number=dict(suffix="/100", font=dict(size=36, color=score_color)),
    gauge=dict(
        axis=dict(
            range=[0, 100],
            tickwidth=1,
            tickcolor="#d1d5db",
            tickvals=[0, 20, 40, 60, 80, 100],
            ticktext=["0", "20", "40", "60", "80", "100"],
            tickfont=dict(size=11)
        ),
        bar=dict(color=score_color, thickness=0.3),
        bgcolor="white",
        borderwidth=0,
        steps=[
            dict(range=[0,  40],  color="#fee2e2"),
            dict(range=[40, 60],  color="#fef9c3"),
            dict(range=[60, 80],  color="#dbeafe"),
            dict(range=[80, 100], color="#dcfce7"),
        ],
        threshold=dict(
            line=dict(color="#374151", width=2),
            thickness=0.75,
            value=overall_score
        )
    ),
    title=dict(text=score_label, font=dict(size=20, color=score_color))
))

gauge_fig.update_layout(
    template="plotly_white",
    height=300,
    margin=dict(l=40, r=40, t=40, b=20),
    paper_bgcolor="white",
    font=dict(family="sans-serif")
)

gauge_col, breakdown_col = st.columns([2, 1])
with gauge_col:
    st.plotly_chart(gauge_fig, use_container_width=True)
with breakdown_col:
    st.markdown("**Score breakdown**")
    st.markdown("<br>", unsafe_allow_html=True)
    st.caption(" Liquidity (30% weight)")
    st.progress(int(liq_score),  text=f"{liq_score}/100")
    st.markdown("<br>", unsafe_allow_html=True)
    st.caption(" Profitability (40% weight)")
    st.progress(int(prof_score), text=f"{prof_score}/100")
    st.markdown("<br>", unsafe_allow_html=True)
    st.caption(" Leverage (30% weight)")
    st.progress(int(lev_score),  text=f"{lev_score}/100")

st.markdown(f"""
<div class="interpretation">
{company_name} achieves an overall financial health score of <strong>{overall_score}/100</strong> ({score_label}).
Profitability is the strongest dimension at {prof_score}/100,
liquidity scores {liq_score}/100,
and leverage scores {lev_score}/100.
This is a simplified quantitative model based on publicly available financial statements —
it should be used as a starting point for analysis, not a definitive assessment.
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# COMPANY COMPARISON
# ════════════════════════════════════════════════════════════════════════════════

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<p class="section-title">Compare Against Another Company</p>', unsafe_allow_html=True)
st.markdown('<p class="section-cap">Enter a second ticker to compare financial health side by side.</p>', unsafe_allow_html=True)

compare_col1, compare_col2 = st.columns([3, 1])
with compare_col1:
    compare_ticker = st.text_input(
        "Second Stock Ticker",
        value="",
        placeholder="e.g. AMD, INTC, MSFT"
    ).upper().strip()
with compare_col2:
    st.markdown("<br>", unsafe_allow_html=True)
    compare_btn = st.button("Compare", use_container_width=True)

if compare_btn and compare_ticker:
    with st.spinner(f"Fetching data for {compare_ticker}..."):
        result2 = fetch_and_calculate(compare_ticker)
    if result2 is None:
        st.error(f"No data found for **{compare_ticker}**. Please check the ticker and try again.")
    else:
        st.session_state["result2"]         = result2
        st.session_state["compare_ticker"]  = compare_ticker

if "result2" in st.session_state:
    result2      = st.session_state["result2"]
    compare_ticker = st.session_state["compare_ticker"]

    company_name2 = result2["info"].get("longName", compare_ticker)
    cr2   = result2["cr"];   qr2  = result2["qr"]
    gm2   = result2["gm"];   nm2  = result2["nm"]
    roe2  = result2["roe"];  roa2 = result2["roa"]
    de2   = result2["de"];   ic2  = result2["ic"]
    liq2  = result2["liq_score"]
    prof2 = result2["prof_score"]
    lev2  = result2["lev_score"]
    over2 = result2["overall"]

    st.markdown("---")
    st.markdown(f"### {company_name}  vs  {company_name2}")

    comparison_data = {
        "Metric": [
            "Current Ratio", "Quick Ratio",
            "Gross Margin", "Net Margin", "ROE", "ROA",
            "Debt to Equity", "Interest Coverage",
            "— Liquidity Score", "— Profitability Score",
            "— Leverage Score", " Overall Score"
        ],
        "Benchmark": [
            "> 1.5", "> 1.0", "> 40%", "> 10%",
            "> 15%", "> 5%", "< 2.0", "> 3.0x",
            "/100", "/100", "/100", "/100"
        ],
        company_name: [
            latest_val(cr),  latest_val(qr),
            latest_val(gm,  pct=True), latest_val(nm,  pct=True),
            latest_val(roe, pct=True), latest_val(roa, pct=True),
            latest_val(de),
            f"{ic.iloc[0]:.1f}x" if ic is not None else "N/A",
            f"{liq_score}", f"{prof_score}", f"{lev_score}", f"{overall_score}"
        ],
        company_name2: [
            latest_val(cr2),  latest_val(qr2),
            latest_val(gm2,  pct=True), latest_val(nm2,  pct=True),
            latest_val(roe2, pct=True), latest_val(roa2, pct=True),
            latest_val(de2),
            f"{ic2.iloc[0]:.1f}x" if ic2 is not None else "N/A",
            f"{liq2}", f"{prof2}", f"{lev2}", f"{over2}"
        ]
    }

    st.dataframe(pd.DataFrame(comparison_data), use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**Health score comparison**")

    compare_fig = go.Figure()
    compare_fig.add_trace(go.Bar(
        name=company_name,
        x=["Liquidity", "Profitability", "Leverage", "Overall"],
        y=[liq_score, prof_score, lev_score, overall_score],
        marker_color="#3b82f6",
        text=[f"{s}" for s in [liq_score, prof_score, lev_score, overall_score]],
        textposition="outside"
    ))
    compare_fig.add_trace(go.Bar(
        name=company_name2,
        x=["Liquidity", "Profitability", "Leverage", "Overall"],
        y=[liq2, prof2, lev2, over2],
        marker_color="#f59e0b",
        text=[f"{s}" for s in [liq2, prof2, lev2, over2]],
        textposition="outside"
    ))
    compare_fig.update_layout(
        template="plotly_white",
        barmode="group",
        height=350,
        margin=dict(l=40, r=40, t=40, b=40),
        yaxis=dict(range=[0, 115], title="Score /100", tickfont=dict(size=11)),
        xaxis=dict(tickfont=dict(size=12)),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor="white",
        paper_bgcolor="white"
    )
    st.plotly_chart(compare_fig, use_container_width=True)

    liq_winner  = company_name if liq_score  >= liq2  else company_name2
    prof_winner = company_name if prof_score >= prof2 else company_name2
    lev_winner  = company_name if lev_score  >= lev2  else company_name2
    overall_winner = company_name if overall_score >= over2 else company_name2
    winning_score  = overall_score if overall_winner == company_name else over2

    summary = (
        f"{overall_winner} leads overall with a financial health score of {winning_score}/100. "
        f"{liq_winner} demonstrates stronger liquidity, "
        f"{prof_winner} shows superior profitability, "
        f"and {lev_winner} carries a more favourable leverage position. "
        f"Both scores are derived from the same weighted model and should be interpreted "
        f"alongside qualitative factors such as industry context, growth stage, and management strategy."
    )
    st.markdown(f'<div class="interpretation">{summary}</div>', unsafe_allow_html=True)

# ── Raw data ──────────────────────────────────────────────────────────────────
st.markdown("---")
with st.expander("📂 Raw Financial Statements"):
    st.markdown("**Balance Sheet**")
    st.dataframe(balance_sheet)
    st.markdown("**Income Statement**")
    st.dataframe(income_stmt)
    st.markdown("**Cash Flow Statement**")
    st.dataframe(cashflow)