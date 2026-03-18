import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import json
import warnings
warnings.filterwarnings('ignore')
if "portfolio" not in st.session_state:
    st.session_state.portfolio = {}

if "cash" not in st.session_state:
    st.session_state.cash = 100000

# ─────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Stock Market Prediction",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────────
# CSS — LIGHT THEME
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --bg-base:    #f5f7fa;
  --bg-surface: #ffffff;
  --bg-raised:  #eef1f6;
  --border-sub: #dde3ec;
  --border-mid: #c8d0de;
  --gold-light: #8a6200;
  --gold-mid:   #b8860b;
  --gold-dark:  #c9a84c;
  --gold-glow:  #c9a84c18;
  --gold-bdr:   #c9a84c40;
  --txt-pri:    #1a2236;
  --txt-sec:    #4a5568;
  --txt-muted:  #8a9ab0;
  --green:      #0f9960;
  --green-bg:   #e8f8f0;
  --red:        #c0392b;
  --red-bg:     #fdecea;
  --blue:       #1a6eb5;
  --blue-bg:    #e8f0fb;
  --shadow:     0 2px 12px rgba(30,50,100,0.08);
  --shadow-lg:  0 6px 28px rgba(30,50,100,0.13);
}

html, body, [class*="css"] {
  background-color: var(--bg-base) !important;
  color: var(--txt-pri) !important;
  font-family: 'Inter', sans-serif !important;
}
.main .block-container {
  background: var(--bg-base) !important;
  padding: 1.5rem 2rem !important;
  max-width: 1600px;
}

/* MASTHEAD */
.qe-masthead {
  display: flex; align-items: flex-start;
  justify-content: space-between;
  padding: 1rem 1.5rem 1rem 1.5rem;
  border-radius: 12px;
  background: linear-gradient(120deg, #ffffff 60%, #f0f4ff 100%);
  box-shadow: var(--shadow);
  border: 1px solid var(--border-sub);
  margin-bottom: 1.5rem;
}
.qe-wordmark {
  font-family: 'Cormorant Garamond', serif;
  font-size: 2rem; font-weight: 700;
  color: var(--gold-mid); letter-spacing: 0.5px; line-height: 1;
}
.qe-wordmark em { color: var(--txt-pri); font-style: normal; font-weight: 400; }
.qe-tag {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.52rem; letter-spacing: 3px;
  color: var(--gold-mid); border: 1px solid var(--gold-bdr);
  background: var(--gold-glow); padding: 3px 10px;
  border-radius: 20px; vertical-align: super; margin-left: 10px;
}
.qe-sub { font-size: 0.78rem; color: var(--txt-muted); letter-spacing: 0.4px; margin-top: 5px; }
.qe-live {
  display: flex; align-items: center; gap: 7px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem; color: var(--green); letter-spacing: 1.5px;
  background: var(--green-bg); padding: 6px 14px; border-radius: 20px;
  border: 1px solid #b6e8d4;
}
.qe-dot {
  width: 7px; height: 7px; border-radius: 50%;
  background: var(--green); box-shadow: 0 0 7px var(--green);
  animation: blink 2.2s ease-in-out infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:.25} }

/* COMPANY CARD */
.company-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-sub);
  border-left: 4px solid var(--gold-dark);
  border-radius: 10px;
  padding: 1.1rem 1.4rem;
  margin-bottom: 1.3rem;
  box-shadow: var(--shadow);
}
.company-card-name {
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.65rem; font-weight: 700;
  color: var(--gold-mid); line-height: 1.1;
}
.company-card-meta {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.58rem; letter-spacing: 2px;
  color: var(--txt-muted); text-transform: uppercase; margin-top: 4px;
}
.company-card-stats {
  display: flex; gap: 2rem; flex-wrap: wrap;
  margin-top: 0.9rem; padding-top: 0.9rem;
  border-top: 1px solid var(--border-sub);
}
.stat-item { text-align: center; }
.stat-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.5rem; letter-spacing: 2px;
  color: var(--txt-muted); text-transform: uppercase; margin-bottom: 2px;
}
.stat-value {
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.1rem; font-weight: 600; color: var(--gold-mid);
}

/* SNAP CARDS */
.snap-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-sub);
  border-top: 3px solid var(--gold-dark);
  border-radius: 10px;
  padding: 0.85rem 1rem;
  box-shadow: var(--shadow);
  transition: box-shadow 0.2s, border-top-color 0.2s;
}
.snap-card:hover { box-shadow: var(--shadow-lg); border-top-color: var(--gold-mid); }
.snap-card-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.52rem; letter-spacing: 2px;
  color: var(--txt-muted); text-transform: uppercase; margin-bottom: 4px;
}
.snap-card-value {
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.45rem; font-weight: 600; color: var(--txt-pri); line-height: 1.1;
}
.snap-card-delta-pos { font-family: 'JetBrains Mono', monospace; font-size: 0.66rem; color: var(--green); background: var(--green-bg); padding: 1px 6px; border-radius: 10px; }
.snap-card-delta-neg { font-family: 'JetBrains Mono', monospace; font-size: 0.66rem; color: var(--red); background: var(--red-bg); padding: 1px 6px; border-radius: 10px; }
.snap-card-delta-neu { font-family: 'JetBrains Mono', monospace; font-size: 0.66rem; color: var(--txt-muted); }

/* SECTION HEADER */
.sec-head {
  display: flex; align-items: center; gap: 10px;
  margin: 1.6rem 0 0.9rem 0;
}
.sec-line { flex:1; height:1px; background:linear-gradient(90deg,var(--border-mid),transparent); }
.sec-dot  { width:5px; height:5px; border-radius:50%; background:var(--gold-dark); flex-shrink:0; }
.sec-txt  {
  font-family:'JetBrains Mono',monospace; font-size:0.58rem;
  letter-spacing:3.5px; color:var(--gold-mid);
  text-transform:uppercase; white-space:nowrap;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
  background: #ffffff !important;
  border-right: 1px solid var(--border-sub) !important;
  min-width: 340px !important;
  max-width: 360px !important;
}
section[data-testid="stSidebar"] * { color: var(--txt-pri) !important; }
.sb-logo {
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.25rem; font-weight: 700;
  color: var(--gold-mid) !important;
  padding: 1rem 0 1.2rem 0;
  border-bottom: 2px solid var(--gold-glow);
  margin-bottom: 1.2rem; letter-spacing: 0.3px;
}
.sb-head {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.56rem; letter-spacing: 3px;
  color: var(--txt-muted) !important;
  text-transform: uppercase;
  margin: 1.2rem 0 0.4rem 0;
}

/* PORTFOLIO CARD */
.port-card {
  background: var(--bg-raised);
  border: 1px solid var(--border-sub);
  border-radius: 10px;
  padding: 0.85rem 1rem;
  margin: 0.4rem 0;
  box-shadow: 0 1px 6px rgba(30,50,100,0.05);
}
.port-ticker {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.78rem; font-weight: 600;
  color: var(--gold-mid);
}
.port-name {
  font-size: 0.7rem; color: var(--txt-muted); margin-top: 1px;
}
.port-row {
  display: flex; justify-content: space-between; align-items: center;
  margin-top: 0.45rem; padding-top: 0.45rem;
  border-top: 1px solid var(--border-sub);
  font-size: 0.72rem; color: var(--txt-sec);
}
.port-worth {
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.05rem; font-weight: 600; color: var(--txt-pri);
}
.port-pnl-pos { color: var(--green); font-size: 0.7rem; font-family: 'JetBrains Mono', monospace; }
.port-pnl-neg { color: var(--red);   font-size: 0.7rem; font-family: 'JetBrains Mono', monospace; }

/* BUY/SELL PILL */
.pill-buy  { display:inline-block; background:var(--green-bg); color:var(--green); border:1px solid #b6e8d4; border-radius:12px; font-size:0.62rem; padding:2px 10px; font-family:'JetBrains Mono',monospace; letter-spacing:1px; }
.pill-sell { display:inline-block; background:var(--red-bg);   color:var(--red);   border:1px solid #f5b7b1; border-radius:12px; font-size:0.62rem; padding:2px 10px; font-family:'JetBrains Mono',monospace; letter-spacing:1px; }

/* TOTAL WEALTH BANNER */
.wealth-banner {
  background: linear-gradient(120deg, #f0f7ff 0%, #fdf8ee 100%);
  border: 1.5px solid var(--gold-bdr);
  border-radius: 12px;
  padding: 1rem 1.2rem;
  margin-bottom: 0.8rem;
  box-shadow: 0 2px 10px rgba(180,140,40,0.1);
}
.wealth-label { font-family:'JetBrains Mono',monospace; font-size:0.55rem; letter-spacing:3px; color:var(--txt-muted); text-transform:uppercase; }
.wealth-value { font-family:'Cormorant Garamond',serif; font-size:2rem; font-weight:700; color:var(--gold-mid); }
.wealth-sub   { font-size:0.72rem; color:var(--txt-muted); margin-top:2px; }

/* SIGNAL PANELS */
.sig-panel {
  display: flex; align-items: center; gap: 1.2rem;
  border-radius: 10px; padding: 1rem 1.5rem; margin: 0.5rem 0;
}
.sig-icon { font-size: 1.4rem; line-height: 1; }
.sig-label { font-family: 'Cormorant Garamond', serif; font-size: 1.35rem; font-weight: 600; }
.sig-sub   { font-family: 'JetBrains Mono', monospace; font-size: 0.58rem; letter-spacing: 1.5px; margin-top: 2px; opacity: 0.7; }
.sig-buy  { background:var(--green-bg); border:1px solid #b6e8d4; border-left:4px solid var(--green); color:var(--green); }
.sig-sell { background:var(--red-bg);   border:1px solid #f5b7b1; border-left:4px solid var(--red);   color:var(--red); }
.sig-hold { background:var(--gold-glow); border:1px solid var(--gold-bdr); border-left:4px solid var(--gold-dark); color:var(--gold-mid); }

/* RECOMMENDATION CARD */
.rec-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-sub);
  border-radius: 10px;
  padding: 1rem 1.2rem;
  margin: 0.4rem 0;
  box-shadow: var(--shadow);
}
.rec-title { font-family:'JetBrains Mono',monospace; font-size:0.57rem; letter-spacing:3px; color:var(--gold-mid); text-transform:uppercase; margin-bottom:0.4rem; }
.rec-body  { font-size:0.82rem; color:var(--txt-sec); line-height:1.65; }
.rec-body strong { color:var(--txt-pri); }

/* INFO CARD */
.info-card { background:var(--bg-surface); border:1px solid var(--border-sub); border-radius:10px; padding:1rem 1.3rem; margin-bottom:1rem; box-shadow:var(--shadow); }
.info-card-title { font-family:'JetBrains Mono',monospace; font-size:0.55rem; letter-spacing:3px; color:var(--gold-mid); text-transform:uppercase; margin-bottom:0.5rem; }
.info-card-body { font-size:0.83rem; color:var(--txt-sec); line-height:1.65; }
.info-card-body strong { color:var(--txt-pri); font-weight:500; }

/* INPUTS */
.stTextInput input {
  background: #f8faff !important;
  border: 1px solid var(--border-mid) !important;
  border-radius: 8px !important; color: var(--txt-pri) !important;
  font-family: 'JetBrains Mono', monospace !important; font-size: 0.85rem !important;
}
.stTextInput input:focus { border-color: var(--gold-dark) !important; box-shadow: 0 0 0 3px var(--gold-glow) !important; }
.stSelectbox > div > div { background: #f8faff !important; border: 1px solid var(--border-mid) !important; border-radius: 8px !important; }
.stNumberInput input { background: #f8faff !important; border: 1px solid var(--border-mid) !important; border-radius: 8px !important; color: var(--txt-pri) !important; }

/* METRICS */
[data-testid="stMetric"] {
  background: var(--bg-surface) !important;
  border: 1px solid var(--border-sub) !important;
  border-top: 3px solid var(--gold-dark) !important;
  border-radius: 10px !important; padding: 1rem 1.2rem !important;
  box-shadow: var(--shadow) !important;
}
[data-testid="stMetricLabel"] p { font-family:'JetBrains Mono',monospace !important; font-size:0.55rem !important; letter-spacing:2.5px !important; color:var(--txt-muted) !important; text-transform:uppercase !important; }
[data-testid="stMetricValue"] { font-family:'Cormorant Garamond',serif !important; font-size:1.65rem !important; font-weight:600 !important; color:var(--txt-pri) !important; }
[data-testid="stMetricDelta"] { font-family:'JetBrains Mono',monospace !important; font-size:0.67rem !important; }

/* TABS */
.stTabs [data-baseweb="tab-list"] { background:transparent !important; border-bottom:2px solid var(--border-sub) !important; gap:0 !important; }
.stTabs [data-baseweb="tab"] { background:transparent !important; color:var(--txt-muted) !important; font-family:'JetBrains Mono',monospace !important; font-size:0.6rem !important; letter-spacing:2px !important; border:none !important; border-bottom:2px solid transparent !important; padding:0.65rem 1.4rem !important; text-transform:uppercase; margin-bottom:-2px; }
.stTabs [aria-selected="true"] { color:var(--gold-mid) !important; border-bottom:2px solid var(--gold-dark) !important; background:transparent !important; }

/* BUTTON */
.stButton > button {
  background: linear-gradient(135deg, var(--gold-dark), #a07830) !important;
  border: none !important; color: #fff !important;
  font-family:'JetBrains Mono',monospace !important; font-size:0.67rem !important;
  letter-spacing:2px !important; border-radius:8px !important;
  padding:0.55rem 1.6rem !important; text-transform:uppercase !important;
  box-shadow:0 3px 14px rgba(180,140,40,0.25) !important; transition:all 0.2s !important;
}
.stButton > button:hover { transform:translateY(-1px) !important; box-shadow:0 5px 20px rgba(180,140,40,0.38) !important; }

/* DATAFRAME */
.stDataFrame { border:1px solid var(--border-sub) !important; border-radius:10px !important; }

/* MISC */
hr { border-color: var(--border-sub) !important; }
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb { background: var(--border-mid); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--gold-dark); }
#MainMenu, footer, header { visibility: hidden; }
.stSpinner > div { border-top-color: var(--gold-dark) !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# MATPLOTLIB LIGHT THEME
# ─────────────────────────────────────────────────────────────────
BG    = '#ffffff'
BG2   = '#f5f7fa'
GOLD  = '#b8860b'
GOLD2 = '#c9a84c'
GREEN = '#0f9960'
RED   = '#c0392b'
BLUE  = '#1a6eb5'
DIM   = '#c8d0de'
TEXT  = '#4a5568'

plt.rcParams.update({
    'figure.facecolor': BG2, 'axes.facecolor': BG,
    'axes.edgecolor': '#dde3ec', 'axes.labelcolor': TEXT,
    'axes.titlecolor': '#1a2236', 'axes.titlesize': 9.5,
    'xtick.color': TEXT, 'ytick.color': TEXT,
    'xtick.labelsize': 7.5, 'ytick.labelsize': 7.5,
    'grid.color': '#eef1f6', 'grid.linewidth': 0.6,
    'text.color': '#1a2236', 'legend.facecolor': BG,
    'legend.edgecolor': '#dde3ec', 'legend.labelcolor': TEXT,
    'legend.fontsize': 8, 'font.family': 'monospace',
    'font.size': 8.5, 'figure.dpi': 110,
})

# ─────────────────────────────────────────────────────────────────
# STOCK UNIVERSE
# ─────────────────────────────────────────────────────────────────
STOCK_UNIVERSE = {
    "🇮🇳 India — Large Cap": [
        ("Reliance Industries","RELIANCE.NS"),("Tata Consultancy","TCS.NS"),
        ("Infosys","INFY.NS"),("HDFC Bank","HDFCBANK.NS"),("ICICI Bank","ICICIBANK.NS"),
        ("State Bank of India","SBIN.NS"),("Bharti Airtel","BHARTIARTL.NS"),
        ("Kotak Mahindra Bank","KOTAKBANK.NS"),("ITC Limited","ITC.NS"),
        ("Larsen & Toubro","LT.NS"),("Axis Bank","AXISBANK.NS"),("Wipro","WIPRO.NS"),
        ("Maruti Suzuki","MARUTI.NS"),("Bajaj Finance","BAJFINANCE.NS"),
        ("HCL Technologies","HCLTECH.NS"),("Adani Enterprises","ADANIENT.NS"),
        ("Titan Company","TITAN.NS"),("Nestle India","NESTLEIND.NS"),
        ("Sun Pharma","SUNPHARMA.NS"),("Asian Paints","ASIANPAINT.NS"),
        ("Hindustan Unilever","HINDUNILVR.NS"),("UltraTech Cement","ULTRACEMCO.NS"),
        ("Power Grid","POWERGRID.NS"),("NTPC","NTPC.NS"),("Tech Mahindra","TECHM.NS"),
        ("Bajaj Auto","BAJAJ-AUTO.NS"),("Tata Motors","TATAMOTORS.NS"),
        ("Tata Steel","TATASTEEL.NS"),("JSW Steel","JSWSTEEL.NS"),("Cipla","CIPLA.NS"),
    ],
    "🇺🇸 USA — Technology": [
        ("Apple","AAPL"),("Microsoft","MSFT"),("NVIDIA","NVDA"),("Alphabet (Google)","GOOGL"),
        ("Meta Platforms","META"),("Amazon","AMZN"),("Tesla","TSLA"),("Netflix","NFLX"),
        ("Adobe","ADBE"),("Salesforce","CRM"),("Intel","INTC"),("AMD","AMD"),
        ("Qualcomm","QCOM"),("Broadcom","AVGO"),("Texas Instruments","TXN"),
        ("Palantir","PLTR"),("Snowflake","SNOW"),("Uber","UBER"),("Airbnb","ABNB"),("Spotify","SPOT"),
    ],
    "🇺🇸 USA — Finance": [
        ("JPMorgan Chase","JPM"),("Bank of America","BAC"),("Goldman Sachs","GS"),
        ("Morgan Stanley","MS"),("Wells Fargo","WFC"),("Visa","V"),("Mastercard","MA"),
        ("American Express","AXP"),("BlackRock","BLK"),("Berkshire Hathaway","BRK-B"),
        ("Citigroup","C"),("PayPal","PYPL"),
    ],
    "🇺🇸 USA — Healthcare": [
        ("Johnson & Johnson","JNJ"),("UnitedHealth","UNH"),("Pfizer","PFE"),
        ("Eli Lilly","LLY"),("AbbVie","ABBV"),("Merck","MRK"),("Moderna","MRNA"),
        ("Intuitive Surgical","ISRG"),
    ],
    "🇺🇸 USA — Consumer & Energy": [
        ("Walmart","WMT"),("Coca-Cola","KO"),("PepsiCo","PEP"),("McDonald's","MCD"),
        ("Nike","NKE"),("Starbucks","SBUX"),("Procter & Gamble","PG"),
        ("ExxonMobil","XOM"),("Chevron","CVX"),
    ],
    "🇬🇧 United Kingdom": [
        ("Shell","SHEL"),("BP","BP"),("HSBC","HSBC"),("Barclays","BCS"),
        ("Unilever","UL"),("AstraZeneca","AZN"),("GlaxoSmithKline","GSK"),
        ("Diageo","DEO"),("Rio Tinto","RIO"),
    ],
    "🇩🇪 Germany": [
        ("SAP","SAP"),("Siemens","SIEGY"),("BMW","BMWYY"),("Volkswagen","VWAGY"),
        ("Deutsche Bank","DB"),("Bayer","BAYRY"),("BASF","BASFY"),
    ],
    "🇯🇵 Japan": [
        ("Toyota","TM"),("Sony","SONY"),("SoftBank","SFTBY"),("Honda","HMC"),
        ("Canon","CAJ"),("Nintendo","NTDOY"),("Panasonic","PCRFY"),
    ],
    "🇨🇳 China": [
        ("Alibaba","BABA"),("Tencent","TCEHY"),("JD.com","JD"),("Baidu","BIDU"),
        ("NIO","NIO"),("BYD","BYDDY"),("PDD Holdings","PDD"),
    ],
    "🌐 ETFs & Indices": [
        ("S&P 500 ETF","SPY"),("NASDAQ 100","QQQ"),("Dow Jones","DIA"),
        ("Nifty 50 ETF","NIFTYBEES.NS"),("Gold ETF","GLD"),("Bitcoin ETF","IBIT"),
        ("Small Cap ETF","IWM"),("Emerging Markets","EEM"),
    ],
}

# Flat symbol -> name lookup
TICKER_NAME = {s: n for grp in STOCK_UNIVERSE.values() for n, s in grp}

# ─────────────────────────────────────────────────────────────────
# SESSION STATE — PORTFOLIO
# ─────────────────────────────────────────────────────────────────
if 'portfolio' not in st.session_state:
    # portfolio = {ticker: {qty, avg_price}}
    st.session_state.portfolio = {}
if 'cash' not in st.session_state:
    st.session_state.cash = 100_000.0   # starting virtual cash
if 'trade_log' not in st.session_state:
    st.session_state.trade_log = []    # list of trade dicts

# ─────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────
def sec(label):
    st.markdown(f"""<div class="sec-head">
      <div class="sec-dot"></div>
      <div class="sec-txt">{label}</div>
      <div class="sec-line"></div>
    </div>""", unsafe_allow_html=True)

def style_ax(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#dde3ec')
    ax.spines['bottom'].set_color('#dde3ec')
    ax.grid(True, alpha=0.5, linestyle='--')

def compute_ai_score(ticker, period="6mo"):

    try:
        df = yf.download(ticker, period=period, progress=False)

        if df.empty:
            return 0, "HOLD", ["No market data available"]

        close = df["Close"]

        score = 0
        reasons = []

        # ---------------- RSI ----------------
        delta = close.diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(14).mean()
        avg_loss = loss.rolling(14).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        rsi_val = float(rsi.iloc[-1])

        if rsi_val < 30:
            score += 25
            reasons.append("RSI oversold — bullish reversal possible")
        elif rsi_val > 70:
            score -= 25
            reasons.append("RSI overbought — possible pullback")

        # ---------------- SMA TREND ----------------
        sma20 = close.rolling(20).mean()
        sma50 = close.rolling(50).mean()

        sma20_last = float(sma20.iloc[-1])
        sma50_last = float(sma50.iloc[-1])

        if sma20_last > sma50_last:
            score += 20
            reasons.append("Short SMA above long — uptrend")
        else:
            score -= 20
            reasons.append("Short SMA below long — downtrend")

        # ---------------- MACD ----------------
        ema12 = close.ewm(span=12).mean()
        ema26 = close.ewm(span=26).mean()

        macd = ema12 - ema26
        signal = macd.ewm(span=9).mean()

        macd_last = float(macd.iloc[-1])
        signal_last = float(signal.iloc[-1])

        if macd_last > signal_last:
            score += 20
            reasons.append("MACD bullish crossover")
        else:
            score -= 20
            reasons.append("MACD bearish crossover")

        # ---------------- MOMENTUM ----------------
        momentum = (close.iloc[-1] / close.iloc[-20] - 1) * 100

        if momentum > 5:
            score += 15
            reasons.append("Strong recent momentum")
        elif momentum < -5:
            score -= 15
            reasons.append("Weak recent momentum")

        # ---------------- FINAL SIGNAL ----------------
        if score >= 30:
            signal_txt = "BUY"
        elif score <= -30:
            signal_txt = "SELL"
        else:
            signal_txt = "HOLD"

        score = int(np.clip(score, -100, 100))

        return score, signal_txt, reasons

    except Exception:
        return 0, "HOLD", ["Analysis failed"]

@st.cache_data(ttl=120)
def fetch_stock(sym, per):
    d = yf.download(sym, period=per, auto_adjust=True, progress=False)
    d.dropna(inplace=True)
    if isinstance(d.columns, pd.MultiIndex):
        d.columns = d.columns.get_level_values(0)
    return d

@st.cache_data(ttl=120)
def fetch_info(sym):
    try:
        info = yf.Ticker(sym).info
        return {
            "name":       info.get("longName", sym),
            "sector":     info.get("sector", "—"),
            "industry":   info.get("industry", "—"),
            "country":    info.get("country", "—"),
            "currency":   info.get("currency", "—"),
            "exchange":   info.get("exchange", "—"),
            "market_cap": info.get("marketCap"),
            "pe_ratio":   info.get("trailingPE"),
            "52w_high":   info.get("fiftyTwoWeekHigh"),
            "52w_low":    info.get("fiftyTwoWeekLow"),
            "beta":       info.get("beta"),
            "dividend":   info.get("dividendYield"),
            "eps":        info.get("trailingEps"),
            "summary":    info.get("longBusinessSummary", ""),
            "website":    info.get("website", ""),
        }
    except:
        return {"name": sym, "sector": "—", "industry": "—", "country": "—",
                "currency": "—", "exchange": "—"}

@st.cache_data(ttl=120)
def get_live_price(sym):
    try:
        d = yf.download(sym, period="2d", auto_adjust=True, progress=False)
        if isinstance(d.columns, pd.MultiIndex): d.columns = d.columns.get_level_values(0)
        c = d['Close'].squeeze()
        return float(c.iloc[-1]) if len(c) > 0 else None
    except:
        return None

def compute_indicators(df, sma_short, sma_long, rsi_period):
    close = df['Close'].squeeze()
    df['SMA_Short'] = close.rolling(sma_short).mean()
    df['SMA_Long']  = close.rolling(sma_long).mean()
    df['EMA_21']    = close.ewm(span=21, adjust=False).mean()
    delta = close.diff()
    gain  = delta.clip(lower=0).rolling(rsi_period).mean()
    loss  = (-delta.clip(upper=0)).rolling(rsi_period).mean()
    df['RSI'] = 100 - (100 / (1 + gain / loss))
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    df['MACD']        = ema12 - ema26
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['MACD_Hist']   = df['MACD'] - df['Signal_Line']
    df['BB_Mid']   = close.rolling(20).mean()
    df['BB_Upper'] = df['BB_Mid'] + 2*close.rolling(20).std()
    df['BB_Lower'] = df['BB_Mid'] - 2*close.rolling(20).std()
    df['BB_B']     = (close - df['BB_Lower']) / (df['BB_Upper'] - df['BB_Lower'])
    h, l = df['High'].squeeze(), df['Low'].squeeze()
    tr = pd.concat([(h-l), (h-close.shift()).abs(), (l-close.shift()).abs()], axis=1).max(axis=1)
    df['ATR'] = tr.rolling(14).mean()
    df['Signal'] = 0
    df.loc[df['SMA_Short'] > df['SMA_Long'], 'Signal'] =  1
    df.loc[df['SMA_Short'] < df['SMA_Long'], 'Signal'] = -1
    df['Returns']          = close.pct_change()
    df['Strategy_Returns'] = df['Returns'] * df['Signal'].shift(1)
    low14  = l.rolling(14).min()
    high14 = h.rolling(14).max()
    df['Stoch_K'] = 100*(close-low14)/(high14-low14)
    df['Stoch_D'] = df['Stoch_K'].rolling(3).mean()
    df['ROC']     = close.pct_change(10)*100
    return df

def fmt_mcap(v):
    if not v: return "—"
    if v >= 1e12: return f"{v/1e12:.2f}T"
    if v >= 1e9:  return f"{v/1e9:.1f}B"
    return f"{v/1e6:.0f}M"

def safe_last(series, default=float('nan')):
    try:
        s = series.dropna() if hasattr(series, 'dropna') else series
        if len(s) == 0: return default
        return float(s.iloc[-1])
    except: return default

def fmt(v, fmt_str=".2f", fallback="—"):
    try:
        if np.isnan(v): return fallback
        return format(v, fmt_str)
    except: return fallback

# ─────────────────────────────────────────────────────────────────
# AI RECOMMENDATION ENGINE
# ─────────────────────────────────────────────────────────────────
def compute_ai_score(ticker, period="1y"):
    """Returns score -100 to 100, signal, and key reasons."""
    try:
        df = fetch_stock(ticker, period)
        if df is None or len(df) < 30:
            return 0, "HOLD", []
        df = compute_indicators(df, 20, 50, 14)
        close = df['Close'].squeeze()
        rsi   = safe_last(df['RSI'])
        macd  = safe_last(df['MACD'])
        sig   = safe_last(df['Signal_Line'])
        bb_b  = safe_last(df['BB_B'])
        sk    = safe_last(df['Stoch_K'])
        sma_s = safe_last(df['SMA_Short'])
        sma_l = safe_last(df['SMA_Long'])
        rets  = df['Returns'].dropna()
        score = 0
        reasons = []

        if not np.isnan(rsi):
            if rsi < 30:   score += 30; reasons.append("RSI oversold — potential rebound")
            elif rsi < 45: score += 15; reasons.append("RSI neutral-low — mild buy zone")
            elif rsi > 70: score -= 30; reasons.append("RSI overbought — caution")
            elif rsi > 60: score -= 10; reasons.append("RSI elevated")

        if not np.isnan(macd) and not np.isnan(sig):
            if macd > sig:   score += 20; reasons.append("MACD bullish crossover")
            else:            score -= 20; reasons.append("MACD bearish crossover")

        if not np.isnan(sma_s) and not np.isnan(sma_l):
            if sma_s > sma_l: score += 20; reasons.append("Short SMA above long — uptrend")
            else:             score -= 20; reasons.append("Short SMA below long — downtrend")

        if not np.isnan(bb_b):
            if bb_b < 0.2:  score += 15; reasons.append("Price near lower Bollinger Band")
            elif bb_b > 0.8:score -= 15; reasons.append("Price near upper Bollinger Band")

        if not np.isnan(sk):
            if sk < 20:  score += 15; reasons.append("Stochastic oversold")
            elif sk > 80:score -= 15; reasons.append("Stochastic overbought")

        mom = float(rets.tail(5).mean()) * 100
        if mom > 0.3:  score += 10; reasons.append("Strong recent momentum")
        elif mom < -0.3: score -= 10; reasons.append("Weak recent momentum")

        score = max(-100, min(100, score))
        if score >= 40:   signal = "STRONG BUY"
        elif score >= 15: signal = "BUY"
        elif score <= -40:signal = "STRONG SELL"
        elif score <= -15:signal = "SELL"
        else:             signal = "HOLD"
        return score, signal, reasons[:4]
    except:
        return 0, "HOLD", []

# ─────────────────────────────────────────────────────────────────
# SIDEBAR — PORTFOLIO DASHBOARD
# ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sb-logo">◈ Stock Market Prediction</div>', unsafe_allow_html=True)

    # ── PORTFOLIO WEALTH SUMMARY ──────────────────────────────────
    portfolio_tickers = list(st.session_state.portfolio.keys())
    total_invested = sum(
        v['qty'] * v['buy_price']
        for v in st.session_state.portfolio.values()
    )
    total_current = 0.0
    live_prices = {}
    for tk in portfolio_tickers:
        p = get_live_price(tk)
        live_prices[tk] = p if p else st.session_state.portfolio[tk]['buy_price']
        total_current += st.session_state.portfolio[tk]['qty'] * live_prices[tk]

    total_worth = total_current + st.session_state.cash
    pnl_total   = total_current - total_invested
    pnl_pct     = (pnl_total / total_invested * 100) if total_invested > 0 else 0

    pnl_color = "#0f9960" if pnl_total >= 0 else "#c0392b"
    pnl_arrow = "▲" if pnl_total >= 0 else "▼"


    # ── INDICATOR SETTINGS ────────────────────────────────────────
    st.markdown('<div class="sb-head">⚙ Indicator Settings</div>', unsafe_allow_html=True)
    sma_short  = st.slider("Short SMA", 5, 50, 20)
    sma_long   = st.slider("Long SMA",  20, 200, 50)
    rsi_period = st.slider("RSI Period", 7, 30, 14)

    
    # ── HOLDINGS ─────────────────────────────────────────────────
    st.markdown('<div class="sb-head">📊 My Holdings</div>', unsafe_allow_html=True)

    if not st.session_state.portfolio:
        st.markdown('<div style="font-size:0.78rem;color:#aaa;padding:6px 0;">No stocks held. Start buying above.</div>', unsafe_allow_html=True)
    else:
        for tk, data in st.session_state.portfolio.items():
            cur = live_prices.get(tk, data['buy_price'])
            worth = data['qty'] * cur
            pnl_s = (cur - data['buy_price']) * data['qty']
            pnl_pct_s = (cur - data['buy_price']) / data['buy_price'] * 100
            pnl_cls = "port-pnl-pos" if pnl_s >= 0 else "port-pnl-neg"
            arrow = "▲" if pnl_s >= 0 else "▼"
            nm = TICKER_NAME.get(tk, tk)
            st.markdown(f"""
            <div class="port-card">
              <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                  <div class="port-ticker">{tk}</div>
                  <div class="port-name">{nm[:28]}</div>
                </div>
                <div class="port-worth">₹{worth:,.0f}</div>
              </div>
              <div class="port-row">
                <span>{data['qty']} shares @ ₹{data['buy_price']:,.2f}</span>
                <span class="{pnl_cls}">{arrow} ₹{abs(pnl_s):,.0f} ({pnl_pct_s:+.1f}%)</span>
              </div>
            </div>
            """, unsafe_allow_html=True)

    # ── WATCHLIST ─────────────────────────────────────────────────
    st.markdown('<div class="sb-head">👁 Watchlist</div>', unsafe_allow_html=True)
    if 'watchlist_tickers' not in st.session_state:
        st.session_state.watchlist_tickers = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "AAPL", "MSFT"]
    watchlist_input = ",".join(st.session_state.watchlist_tickers)

    # ── COMPARE ───────────────────────────────────────────────────
    st.markdown('<div class="sb-head">⚖ Compare Portfolio</div>', unsafe_allow_html=True)
    compare_input = st.text_input("Compare tickers", value="AAPL,MSFT,NVDA,TSLA")



# ─────────────────────────────────────────────────────────────────
# MAIN CONTENT — COMPANY SELECTOR
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="qe-masthead">
  <div>
    <div class="qe-wordmark">Stock Market<em> Prediction</em></div>
    <div class="qe-sub">Professional Stock Intelligence · Real-time Analysis · AI-powered Signals · Virtual Trading</div>
  </div>
  <div class="qe-live"><div class="qe-dot"></div>LIVE DATA</div>
</div>
""", unsafe_allow_html=True)

sel_col1, sel_col2, sel_col3, sel_col4 = st.columns([2, 2.5, 1.2, 1])

with sel_col1:
    st.markdown('<div class="sb-head" style="margin-top:0">Sector / Region</div>', unsafe_allow_html=True)
    selected_sector = st.selectbox("Sector", list(STOCK_UNIVERSE.keys()), label_visibility="collapsed")

with sel_col2:
    st.markdown('<div class="sb-head" style="margin-top:0">Company</div>', unsafe_allow_html=True)
    company_options  = [f"{n}  ({s})" for n, s in STOCK_UNIVERSE[selected_sector]]
    selected_company = st.selectbox("Company", company_options, label_visibility="collapsed")
    selected_ticker  = STOCK_UNIVERSE[selected_sector][company_options.index(selected_company)][1]

with sel_col3:
    st.markdown('<div class="sb-head" style="margin-top:0">Time Period</div>', unsafe_allow_html=True)
    period = st.selectbox("Period", ["1mo","3mo","6mo","1y","2y","5y"], index=3, label_visibility="collapsed")

with sel_col4:
    st.markdown('<div class="sb-head" style="margin-top:0">Custom Ticker</div>', unsafe_allow_html=True)
    custom_ticker = st.text_input("Custom", value="", placeholder="e.g. RELIANCE.NS", label_visibility="collapsed")
    if custom_ticker.strip():
        selected_ticker = custom_ticker.strip().upper()

# ─────────────────────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────────────────────
with st.spinner(f"Fetching live data for {selected_ticker}..."):
    try:
        df   = fetch_stock(selected_ticker, period)
        info = fetch_info(selected_ticker)
    except Exception as e:
        st.error(f"Error fetching {selected_ticker}: {e}")
        st.stop()

if df.empty:
    st.error(f"No data returned for **{selected_ticker}**. Try a different symbol.")
    st.stop()

df = compute_indicators(df, sma_short, sma_long, rsi_period)
close = df['Close'].squeeze()
cum_mkt   = (1 + df['Returns']).cumprod()
cum_strat = (1 + df['Strategy_Returns']).cumprod()

# ─────────────────────────────────────────────────────────────────
# COMPANY HEADER CARD
# ─────────────────────────────────────────────────────────────────
cname    = info.get("name", selected_ticker)
csector  = info.get("sector", "—")
cindustry= info.get("industry", "—")
ccountry = info.get("country", "—")
ccurr    = info.get("currency", "—")
mcap     = fmt_mcap(info.get("market_cap"))
pe       = f"{info.get('pe_ratio'):.1f}" if info.get("pe_ratio") else "—"
beta     = f"{info.get('beta'):.2f}"     if info.get("beta")     else "—"
eps      = f"{info.get('eps'):.2f}"      if info.get("eps")      else "—"
w52h     = f"{info.get('52w_high'):,.2f}" if info.get("52w_high") else "—"
w52l     = f"{info.get('52w_low'):,.2f}"  if info.get("52w_low")  else "—"
div      = f"{info.get('dividend')*100:.2f}%" if info.get("dividend") else "—"

st.markdown(f"""
<div class="company-card">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:1rem;">
    <div>
      <div class="company-card-name">{cname}</div>
      <div class="company-card-meta">
        {selected_ticker} &nbsp;·&nbsp; {csector} &nbsp;·&nbsp; {cindustry}
        &nbsp;·&nbsp; {ccountry} &nbsp;·&nbsp; {ccurr}
      </div>
    </div>
    <div style="font-family:'JetBrains Mono',monospace;font-size:0.58rem;color:#aaa;">
      Real-time · yfinance
    </div>
  </div>
  <div class="company-card-stats">
    <div class="stat-item"><div class="stat-label">Market Cap</div><div class="stat-value">{mcap}</div></div>
    <div class="stat-item"><div class="stat-label">P/E Ratio</div><div class="stat-value">{pe}</div></div>
    <div class="stat-item"><div class="stat-label">EPS</div><div class="stat-value">{eps}</div></div>
    <div class="stat-item"><div class="stat-label">Beta</div><div class="stat-value">{beta}</div></div>
    <div class="stat-item"><div class="stat-label">52W High</div><div class="stat-value">{w52h}</div></div>
    <div class="stat-item"><div class="stat-label">52W Low</div><div class="stat-value">{w52l}</div></div>
    <div class="stat-item"><div class="stat-label">Dividend</div><div class="stat-value">{div}</div></div>
  </div>
</div>
""", unsafe_allow_html=True)

summary = info.get("summary", "")
if summary:
    with st.expander("📋  Company Overview", expanded=False):
        st.markdown(f'<div style="font-size:0.83rem;color:#4a5568;line-height:1.7;">{summary[:700]}{"..." if len(summary)>700 else ""}</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# LIVE SNAPSHOT
# ─────────────────────────────────────────────────────────────────
if len(df) < 30:
    st.warning(f"⚠️  Only {len(df)} rows of data. Please select a longer period.")
    st.stop()

latest  = safe_last(close)
prev    = safe_last(close.iloc[:-1], default=latest)
day_chg = (latest - prev) / prev * 100 if prev else 0.0
per_chg = (latest - float(close.iloc[0])) / float(close.iloc[0]) * 100
vol_20  = safe_last(df['Returns'].rolling(20).std()) * np.sqrt(252)
rsi_val = safe_last(df['RSI'])
atr_val = safe_last(df['ATR'])
macd_val= safe_last(df['MACD'])
sig_val = safe_last(df['Signal_Line'])
bb_b    = safe_last(df['BB_B'])
stoch_k = safe_last(df['Stoch_K'])
volume  = safe_last(df['Volume'].squeeze())
high_d  = safe_last(df['High'].squeeze())
low_d   = safe_last(df['Low'].squeeze())

def delta_color(v):
    if v and v > 0: return "snap-card-delta-pos"
    if v and v < 0: return "snap-card-delta-neg"
    return "snap-card-delta-neu"

def delta_arrow(v): return f"▲ {abs(v):.2f}%" if v >= 0 else f"▼ {abs(v):.2f}%"

sec(f"Live Market Snapshot  —  {cname}")

snapshots = [
    ("Last Close",       f"{latest:,.2f}",    day_chg,  delta_arrow(day_chg)),
    ("Day High",         f"{high_d:,.2f}",    None,     ""),
    ("Day Low",          f"{low_d:,.2f}",     None,     ""),
    ("Period Return",    f"{per_chg:+.1f}%",  per_chg,  delta_arrow(per_chg)),
    ("20D Volatility",   f"{vol_20:.1%}",     None,     "High" if vol_20>0.3 else "Low"),
    ("RSI (14)",         f"{rsi_val:.1f}",    None,     "Overbought" if rsi_val>70 else "Oversold" if rsi_val<30 else "Neutral"),
    ("ATR (14)",         f"{atr_val:.2f}",    None,     ""),
    ("MACD Signal",      "Bullish" if macd_val>sig_val else "Bearish", None, f"{macd_val:.3f}"),
    ("Stoch %K",         f"{stoch_k:.1f}",   None,     "OB" if stoch_k>80 else "OS" if stoch_k<20 else "Neutral"),
    ("BB Position",      f"{bb_b:.2f}",       None,     "Upper" if bb_b>0.8 else "Lower" if bb_b<0.2 else "Mid"),
    ("Volume",           f"{volume:,.0f}",    None,     ""),
    ("Strategy Signal",  "BUY" if df['Signal'].iloc[-1]==1 else "SELL" if df['Signal'].iloc[-1]==-1 else "HOLD",
                         None, "SMA Crossover"),
]

cols = st.columns(6)
for i, (label, value, chg, sub) in enumerate(snapshots):
    c = cols[i % 6]
    sub_class = delta_color(chg) if chg is not None else "snap-card-delta-neu"
    c.markdown(f"""
    <div class="snap-card">
      <div class="snap-card-label">{label}</div>
      <div class="snap-card-value">{value}</div>
      <div class="{sub_class}">{sub}</div>
    </div>""", unsafe_allow_html=True)



# ─────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Analysis",
    "Technicals",
    "AI Predictor",
    "Risk",
    "Watchlist",
    "Compare",
    "Portfolio"
])

# ══════════════════════════════════════════════════════════════
# TAB 1 · ANALYSIS
# ══════════════════════════════════════════════════════════════
with tab1:
    sec(f"Price Action — {cname}")

    fig, axes = plt.subplots(3, 1, figsize=(14, 11),
                              gridspec_kw={'height_ratios': [3.5, 1, 1.2], 'hspace': 0.07})
    fig.patch.set_facecolor(BG2)

    ax = axes[0]
    ax.fill_between(df.index, df['BB_Upper'], df['BB_Lower'], alpha=0.08, color=GOLD)
    ax.plot(df.index, df['BB_Upper'], color=GOLD,  lw=0.6, alpha=0.35)
    ax.plot(df.index, df['BB_Lower'], color=GOLD,  lw=0.6, alpha=0.35)
    ax.plot(df.index, close,           color='#1a2236', lw=1.5, label='Price', zorder=3)
    ax.plot(df.index, df['SMA_Short'], color=GOLD2,    lw=1.1, label=f'SMA {sma_short}')
    ax.plot(df.index, df['SMA_Long'],  color=GOLD,     lw=1.1, label=f'SMA {sma_long}', linestyle='--')
    ax.plot(df.index, df['EMA_21'],    color=BLUE,     lw=0.9, label='EMA 21', linestyle=':', alpha=0.7)
    buys  = df[df['Signal'].diff() ==  2]
    sells = df[df['Signal'].diff() == -2]
    ax.scatter(buys.index,  buys['Close'],  marker='^', color=GREEN, s=55, zorder=5, edgecolors='none', label='Buy Signal')
    ax.scatter(sells.index, sells['Close'], marker='v', color=RED,   s=55, zorder=5, edgecolors='none', label='Sell Signal')
    ax.set_title(f"{cname}  ({selected_ticker})  ·  Price & Moving Averages  |  Bollinger Bands",
                  fontsize=10, color='#1a2236', pad=12)
    ax.legend(loc='upper left', framealpha=0.8, fontsize=8)
    style_ax(ax); ax.tick_params(labelbottom=False)

    ax2 = axes[1]
    ax2.bar(df.index, df['Volume'].squeeze(),
             color=[GREEN if r >= 0 else RED for r in df['Returns'].fillna(0)],
             alpha=0.5, width=1)
    ax2.set_ylabel('Vol', fontsize=7.5, color=TEXT)
    style_ax(ax2); ax2.tick_params(labelbottom=False)

    ax3 = axes[2]
    ax3.plot(df.index, df['RSI'], color=GOLD2, lw=1.2)
    ax3.fill_between(df.index, df['RSI'], 70, where=(df['RSI'] >= 70), alpha=0.2, color=RED)
    ax3.fill_between(df.index, df['RSI'], 30, where=(df['RSI'] <= 30), alpha=0.2, color=GREEN)
    ax3.axhline(70, color=RED,   lw=0.7, linestyle='--', alpha=0.5)
    ax3.axhline(30, color=GREEN, lw=0.7, linestyle='--', alpha=0.5)
    ax3.axhline(50, color=DIM,   lw=0.5, linestyle=':')
    ax3.set_ylim(0, 100); ax3.set_ylabel('RSI', fontsize=7.5, color=TEXT)
    style_ax(ax3)
    fig.tight_layout(); st.pyplot(fig, use_container_width=True); plt.close(fig)

    sec(f"MACD — {cname}")
    fig2, ax4 = plt.subplots(figsize=(14, 3.5))
    fig2.patch.set_facecolor(BG2)
    ax4.bar(df.index, df['MACD_Hist'],
             color=[GREEN if v >= 0 else RED for v in df['MACD_Hist'].fillna(0)],
             alpha=0.5, width=1)
    ax4.plot(df.index, df['MACD'],        color=GOLD2, lw=1.3, label='MACD')
    ax4.plot(df.index, df['Signal_Line'], color=BLUE,  lw=1.1, label='Signal', linestyle='--')
    ax4.axhline(0, color=DIM, lw=0.7)
    ax4.legend(framealpha=0.8); ax4.set_title(f"{cname}  ·  MACD", fontsize=9.5)
    style_ax(ax4); fig2.tight_layout(); st.pyplot(fig2, use_container_width=True); plt.close(fig2)


    sec("Recent Data")
    st.dataframe(df[['Open','High','Low','Close','Volume','SMA_Short','SMA_Long','RSI','MACD']].tail(10).round(2), use_container_width=True)

# ══════════════════════════════════════════════════════════════
# TAB 2 · TECHNICALS
# ══════════════════════════════════════════════════════════════
with tab2:
    sec(f"Technical Indicators — {cname}")
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    fig.patch.set_facecolor(BG2)

    ax = axes[0, 0]
    ax.plot(df.index, df['BB_B'], color=GOLD2, lw=1.2)
    ax.fill_between(df.index, df['BB_B'], 1, where=(df['BB_B'] >= 1), alpha=0.2, color=RED)
    ax.fill_between(df.index, df['BB_B'], 0, where=(df['BB_B'] <= 0), alpha=0.2, color=GREEN)
    ax.axhline(1, color=RED,   lw=0.7, linestyle='--', alpha=0.5)
    ax.axhline(0, color=GREEN, lw=0.7, linestyle='--', alpha=0.5)
    ax.set_title(f'{cname}  ·  Bollinger Band %B', fontsize=9); style_ax(ax)

    ax = axes[0, 1]
    ax.plot(df.index, df['ATR'], color=GOLD, lw=1.3)
    ax.fill_between(df.index, df['ATR'], alpha=0.13, color=GOLD)
    ax.set_title(f'{cname}  ·  ATR (14)', fontsize=9); style_ax(ax)

    ax = axes[1, 0]
    ax.plot(df.index, df['Stoch_K'], color=GOLD2, lw=1.2, label='%K')
    ax.plot(df.index, df['Stoch_D'], color=BLUE,  lw=1.0, label='%D', linestyle='--')
    ax.axhline(80, color=RED,   lw=0.7, linestyle='--', alpha=0.5)
    ax.axhline(20, color=GREEN, lw=0.7, linestyle='--', alpha=0.5)
    ax.set_ylim(0, 100); ax.set_title(f'{cname}  ·  Stochastic Oscillator', fontsize=9)
    ax.legend(framealpha=0.8); style_ax(ax)

    ax = axes[1, 1]
    ax.plot(df.index, df['ROC'], color=GOLD, lw=1.2)
    ax.fill_between(df.index, df['ROC'], 0, where=(df['ROC'] >= 0), alpha=0.15, color=GREEN)
    ax.fill_between(df.index, df['ROC'], 0, where=(df['ROC'] <  0), alpha=0.15, color=RED)
    ax.axhline(0, color=DIM, lw=0.8)
    ax.set_title(f'{cname}  ·  Rate of Change (10)', fontsize=9); style_ax(ax)

    fig.tight_layout(pad=2.5); st.pyplot(fig, use_container_width=True); plt.close(fig)

    sec("Indicator Summary")
    def lbl(v, hi, lo):
        if v >= hi: return "⬤ Overbought"
        if v <= lo: return "⬤ Oversold"
        return "○ Neutral"

    st.dataframe(pd.DataFrame({
        "Indicator": ["RSI (14)", "Stochastic %K", "MACD vs Signal", "BB %B", "SMA Crossover"],
        "Value":     [f"{rsi_val:.1f}", f"{stoch_k:.1f}", f"{macd_val:.4f}", f"{bb_b:.2f}",
                       "Above" if safe_last(df['SMA_Short']) > safe_last(df['SMA_Long']) else "Below"],
        "Reading":   [lbl(rsi_val,70,30), lbl(stoch_k,80,20),
                       "⬤ Bullish" if macd_val > sig_val else "⬤ Bearish",
                       lbl(bb_b*100,100,0),
                       "⬤ Bullish" if safe_last(df['SMA_Short']) > safe_last(df['SMA_Long']) else "⬤ Bearish"],
    }), use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════
# TAB 3 · AI PREDICTOR
# ══════════════════════════════════════════════════════════════
with tab3:
    sec(f"AI Price Prediction — {cname}")
    st.markdown(f"""
    <div class="info-card">
      <div class="info-card-title">Model · {cname} ({selected_ticker})</div>
      <div class="info-card-body">
        Predicting the <strong>next session's closing price</strong> using a Linear Regression ensemble
        trained on RSI, MACD, Bollinger Band width, ATR, SMA spread, and lagged close prices
        from <strong>{period}</strong> of historical data.
      </div>
    </div>""", unsafe_allow_html=True)

    fig_p, ax_p = plt.subplots(figsize=(14, 2.8))
    fig_p.patch.set_facecolor(BG2)
    ax_p.plot(close.index, close, color=GOLD2, lw=1.4)
    ax_p.fill_between(close.index, close, float(close.min()), alpha=0.1, color=GOLD)
    ax_p.scatter([close.index[-1]], [latest], color=GREEN if day_chg >= 0 else RED, s=60, zorder=5)
    ax_p.axhline(latest, color=GREEN if day_chg >= 0 else RED, lw=0.7, linestyle='--', alpha=0.5)
    ax_p.set_title(f"{cname}  ·  Latest: {latest:,.2f}  ({day_chg:+.2f}%)", fontsize=9.5)
    style_ax(ax_p); fig_p.tight_layout(); st.pyplot(fig_p, use_container_width=True); plt.close(fig_p)

    if st.button("▶  Run AI Prediction"):
        with st.spinner(f"Computing prediction for {cname}..."):
            try:
                from predict import predict_stock
                pred_val = predict_stock(selected_ticker)
            except ImportError:
                from sklearn.linear_model import LinearRegression
                feat  = ['SMA_Short','SMA_Long','RSI','MACD','Signal_Line','ATR']
                dm    = df[feat + ['Close']].dropna().copy()
                for lag in [1, 2, 3, 5]: dm[f'lag_{lag}'] = dm['Close'].shift(lag)
                dm.dropna(inplace=True)
                xcols = feat + [f'lag_{l}' for l in [1, 2, 3, 5]]
                X, y  = dm[xcols].values, dm['Close'].values
                split = int(len(X) * 0.85)
                mdl   = LinearRegression().fit(X[:split], y[:split])
                pred_val = float(mdl.predict(dm[xcols].iloc[-1:].values)[0])

                y_all = mdl.predict(X)
                fig_fit, ax_fit = plt.subplots(figsize=(14, 3.5))
                fig_fit.patch.set_facecolor(BG2)
                ax_fit.plot(dm.index, y,     color='#1a2236', lw=1.0, label='Actual',  alpha=0.8)
                ax_fit.plot(dm.index, y_all, color=GOLD2,     lw=1.0, label='Fitted',  alpha=0.8, linestyle='--')
                ax_fit.scatter([dm.index[-1]], [pred_val], color=GREEN, s=80, zorder=5, label=f'Next: {pred_val:,.2f}')
                ax_fit.set_title(f"{cname}  ·  Actual vs Fitted Model", fontsize=9.5)
                ax_fit.legend(framealpha=0.8); style_ax(ax_fit)
                fig_fit.tight_layout(); st.pyplot(fig_fit, use_container_width=True); plt.close(fig_fit)

            pct = (pred_val - latest) / latest * 100
            ca  = "#0f9960" if pct >= 0 else "#c0392b"
            ca_bg = "#e8f8f0" if pct >= 0 else "#fdecea"
            ca_bd = "#b6e8d4" if pct >= 0 else "#f5b7b1"
            st.markdown(f"""
            <div style="background:{ca_bg};border:1.5px solid {ca_bd};border-left:5px solid {ca};
              border-radius:12px;padding:1.2rem 1.6rem;margin:1rem 0;
              display:flex;align-items:center;gap:2.5rem;flex-wrap:wrap;">
              <div style="font-family:'JetBrains Mono',monospace;font-size:0.58rem;
                letter-spacing:2px;color:#aaa;text-transform:uppercase;">
                Prediction — <span style="color:{GOLD}">{cname}</span>
              </div>
              <div>
                <span style="font-family:'Cormorant Garamond',serif;font-size:1.6rem;
                  font-weight:600;color:{ca};">
                  {"▲" if pct>=0 else "▼"} &nbsp; {pred_val:,.2f}
                </span>
                <span style="font-family:'JetBrains Mono',monospace;font-size:0.82rem;
                  color:{ca};margin-left:10px;">{pct:+.2f}%</span>
              </div>
              <div style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:#4a5568;">
                Current close: {latest:,.2f}
              </div>
            </div>""", unsafe_allow_html=True)

            pr1, pr2, pr3 = st.columns(3)
            pr1.metric("Current Close",   f"{latest:,.2f}")
            pr2.metric("Predicted Close", f"{pred_val:,.2f}", f"{pct:+.2f}%")
            pr3.metric("Direction",       "▲  UP" if pct >= 0 else "▼  DOWN")

    sec("Feature Signal Readings")
    st.dataframe(pd.DataFrame({
        'Feature': ['RSI (14)', 'MACD vs Signal', 'SMA Spread', 'BB %B', 'ATR / Price'],
        'Value': [
            f"{rsi_val:.1f}",
            f"{macd_val - sig_val:.4f}",
            f"{(safe_last(df['SMA_Short']) - safe_last(df['SMA_Long'])) / safe_last(df['SMA_Long']) * 100:.2f}%" if not np.isnan(safe_last(df['SMA_Long'])) else "—",
            f"{bb_b:.2f}",
            f"{atr_val / latest * 100:.2f}%",
        ],
        'Interpretation': [
            "Overbought" if rsi_val > 70 else "Oversold" if rsi_val < 30 else "Neutral",
            "Bullish" if macd_val > sig_val else "Bearish",
            "Bull Momentum" if safe_last(df['SMA_Short']) > safe_last(df['SMA_Long']) else "Bear Momentum",
            "Near Upper Band" if bb_b > 0.8 else "Near Lower Band" if bb_b < 0.2 else "Mid-Range",
            "High Volatility" if atr_val / latest * 100 > 2 else "Low Volatility",
        ]
    }), use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════
# TAB 4 · RISK
# ══════════════════════════════════════════════════════════════
with tab4:
    sec(f"Risk Analysis — {cname}")
    rets    = df['Returns'].dropna()
    ann_vol = float(rets.std() * np.sqrt(252))
    rfr     = 0.05 / 252
    sharpe  = float((rets.mean() - rfr) / rets.std() * np.sqrt(252))
    neg     = rets[rets < 0]
    sortino = float((rets.mean() - rfr) / neg.std() * np.sqrt(252)) if neg.std() > 0 else 0
    cr      = (1 + rets).cumprod(); rm = cr.cummax(); dd = (cr - rm) / rm
    max_dd  = float(dd.min())
    calmar  = float((cr.iloc[-1] - 1) / abs(max_dd)) if max_dd != 0 else 0
    var95   = float(np.percentile(rets, 5))
    cvar95  = float(rets[rets <= var95].mean())
    skew    = float(rets.skew())

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Annual Volatility", f"{ann_vol:.1%}")
    m2.metric("Sharpe Ratio",      f"{sharpe:.2f}", "Strong" if sharpe > 1 else "Weak")
    m3.metric("Sortino Ratio",     f"{sortino:.2f}")
    m4.metric("Calmar Ratio",      f"{calmar:.2f}")
    

    fig, axes = plt.subplots(1, 3, figsize=(14, 4.2))
    fig.patch.set_facecolor(BG2)

    ax = axes[0]
    n, bins, patches = ax.hist(rets * 100, bins=55, color=BLUE, alpha=0.6, edgecolor='none')
    for patch, left in zip(patches, bins[:-1]):
        if left < var95 * 100: patch.set_facecolor(RED); patch.set_alpha(0.7)
    ax.axvline(var95 * 100,  color=RED,  lw=1.5, linestyle='--', label=f'VaR  {var95:.2%}')
    ax.axvline(cvar95 * 100, color=GOLD, lw=1.2, linestyle=':',  label=f'CVaR {cvar95:.2%}')
    ax.axvline(0, color=DIM, lw=0.8)
    ax.set_title(f"{cname}  ·  Returns Distribution", fontsize=9)
    ax.legend(fontsize=7, framealpha=0.8); ax.set_xlabel("Return (%)", fontsize=8)
    style_ax(ax)

    ax = axes[1]
    ax.fill_between(dd.index, dd * 100, 0, color=RED, alpha=0.28)
    ax.plot(dd.index, dd * 100, color=RED, lw=0.9)
    ax.set_title(f"{cname}  ·  Drawdown (%)", fontsize=9); style_ax(ax)

    rv = rets.rolling(21).std() * np.sqrt(252)
    ax = axes[2]
    ax.plot(rv.index, rv * 100, color=GOLD2, lw=1.3)
    ax.fill_between(rv.index, rv * 100, alpha=0.14, color=GOLD)
    ax.set_title(f"{cname}  ·  Rolling 21D Volatility (%)", fontsize=9); style_ax(ax)

    fig.tight_layout(pad=2.2); st.pyplot(fig, use_container_width=True); plt.close(fig)

    sec("Trading Signal")
    sig = int(df['Signal'].iloc[-1])
    if sig == 1:
        st.markdown("""<div class="sig-panel sig-buy">
          <div class="sig-icon">▲</div>
          <div><div class="sig-label">BUY SIGNAL</div>
          <div class="sig-sub">SMA CROSSOVER · SHORT ABOVE LONG · BULLISH MOMENTUM</div></div>
        </div>""", unsafe_allow_html=True)
    elif sig == -1:
        st.markdown("""<div class="sig-panel sig-sell">
          <div class="sig-icon">▼</div>
          <div><div class="sig-label">SELL SIGNAL</div>
          <div class="sig-sub">SMA CROSSOVER · SHORT BELOW LONG · BEARISH MOMENTUM</div></div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div class="sig-panel sig-hold">
          <div class="sig-icon">◉</div>
          <div><div class="sig-label">HOLD</div>
          <div class="sig-sub">NO CLEAR DIRECTIONAL SIGNAL · AWAIT CONFIRMATION</div></div>
        </div>""", unsafe_allow_html=True)
# ══════════════════════════════════════════════════════════════
# TAB 5 · WATCHLIST
# ══════════════════════════════════════════════════════════════
with tab5:

    sec("Watchlist Manager")

    if "watchlist_tickers" not in st.session_state:
        st.session_state.watchlist_tickers = []

    # ── Prepare dropdown options ──
    all_tickers_flat = [(n, s) for grp in STOCK_UNIVERSE.values() for n, s in grp]
    all_options = [f"{n}  ({s})" for n, s in all_tickers_flat]
    all_symbols = [s for _, s in all_tickers_flat]

    wl_c1, wl_c2, wl_c3 = st.columns([3,1,1])

    with wl_c1:
        add_choice = st.selectbox(
            "Select stock to add to watchlist",
            ["— pick a stock —"] + all_options
        )

    with wl_c2:
        st.markdown("<div style='margin-top:27px'></div>", unsafe_allow_html=True)

        if st.button("➕ Add to Watchlist"):
            if add_choice != "— pick a stock —":
                idx = all_options.index(add_choice)
                sym = all_symbols[idx]

                if sym not in st.session_state.watchlist_tickers:
                    st.session_state.watchlist_tickers.append(sym)
                    st.success(f"Added {sym}")
                    st.rerun()
                else:
                    st.info(f"{sym} already exists")

    with wl_c3:
        st.markdown("<div style='margin-top:27px'></div>", unsafe_allow_html=True)

        if st.session_state.watchlist_tickers:
            to_remove = st.selectbox(
                "Remove",
                ["— select —"] + st.session_state.watchlist_tickers,
                label_visibility="collapsed"
            )

            if st.button("➖ Remove"):
                if to_remove != "— select —":
                    st.session_state.watchlist_tickers.remove(to_remove)
                    st.success(f"Removed {to_remove}")
                    st.rerun()

    # ── Custom ticker add ──
    custom_col, custom_btn = st.columns([3,1])

    with custom_col:
        custom_ticker = st.text_input(
            "Or type custom ticker(s) to add (comma-separated)",
            placeholder="e.g. NVDA, BAJFINANCE.NS"
        )

    with custom_btn:
        st.markdown("<div style='margin-top:27px'></div>", unsafe_allow_html=True)

        if st.button("➕ Add Custom"):
            added = []

            for t in [x.strip().upper() for x in custom_ticker.split(",") if x.strip()]:
                if t not in st.session_state.watchlist_tickers:
                    st.session_state.watchlist_tickers.append(t)
                    added.append(t)

            if added:
                st.success(f"Added: {', '.join(added)}")
                st.rerun()

    # ── Watchlist pills ──
    if st.session_state.watchlist_tickers:

        pills_html = "".join([
            f'<span style="display:inline-block;background:#e8f0fb;color:#1a6eb5;'
            f'border:1px solid #b6cff5;border-radius:14px;padding:3px 12px;'
            f'font-family:JetBrains Mono,monospace;font-size:0.68rem;margin:3px 4px;">'
            f'{t}</span>'
            for t in st.session_state.watchlist_tickers
        ])

        st.markdown(f"""
        <div style="background:#f5f7fa;border:1px solid #dde3ec;border-radius:10px;
          padding:10px 14px;margin:8px 0 16px 0;">
          <div style="font-family:'JetBrains Mono',monospace;font-size:0.55rem;
            letter-spacing:2.5px;color:#8a9ab0;text-transform:uppercase;margin-bottom:6px;">
            Current Watchlist ({len(st.session_state.watchlist_tickers)} stocks)
          </div>
          {pills_html}
        </div>
        """, unsafe_allow_html=True)

    else:
        st.info("Your watchlist is empty. Add stocks above.")

    # ─────────────────────────────────────
    # Watchlist Analysis
    # ─────────────────────────────────────

    if st.session_state.watchlist_tickers:

        st.subheader("Watchlist Analysis")

        for i, stock in enumerate(st.session_state.watchlist_tickers):

            col1, col2 = st.columns([3,1])

            col1.write(f"**{stock}**")

            if col2.button("RE-ANALYZE", key=f"watch_{i}"):

                st.write(f"### Re-Analyzing {stock}")

                df = yf.download(stock, period="6mo", progress=False)

                if df.empty:
                    st.error("Unable to fetch stock data")
                else:

                    close = df["Close"].dropna()

                    # MACD
                    ema12 = close.ewm(span=12, adjust=False).mean()
                    ema26 = close.ewm(span=26, adjust=False).mean()

                    macd = ema12 - ema26
                    signal = macd.ewm(span=9, adjust=False).mean()

                    macd_last = float(macd.iloc[-1])
                    signal_last = float(signal.iloc[-1])

                    macd_signal = "Bullish" if macd_last > signal_last else "Bearish"

                    # RSI
                    delta = close.diff()

                    gain = delta.clip(lower=0)
                    loss = -delta.clip(upper=0)

                    avg_gain = gain.rolling(14).mean()
                    avg_loss = loss.rolling(14).mean()

                    rs = avg_gain / avg_loss
                    rsi = 100 - (100 / (1 + rs))

                    rsi_value = float(rsi.iloc[-1])

                    # TREND
                    sma20 = close.rolling(20).mean()
                    sma50 = close.rolling(50).mean()

                    sma20_last = float(sma20.iloc[-1])
                    sma50_last = float(sma50.iloc[-1])

                    trend = "Uptrend" if sma20_last > sma50_last else "Downtrend"

                    # VOLATILITY
                    volatility = float(close.pct_change().std() * np.sqrt(252))

                    if volatility < 0.20:
                        risk = "Low"
                    elif volatility < 0.35:
                        risk = "Medium"
                    else:
                        risk = "High"

                    # AI SCORE
                    score = 0

                    if macd_signal == "Bullish":
                        score += 30
                    else:
                        score -= 20

                    if rsi_value < 30:
                        score += 25
                    elif rsi_value > 70:
                        score -= 25

                    if trend == "Uptrend":
                        score += 25
                    else:
                        score -= 15

                    if risk == "Low":
                        score += 20
                    elif risk == "Medium":
                        score += 5
                    else:
                        score -= 10

                    score = max(min(score,100),-100)

                    # DISPLAY RESULTS
                    st.write(f"MACD Signal: **{macd_signal}**")
                    st.write(f"RSI Value: **{rsi_value:.2f}**")
                    st.write(f"Trend: **{trend}**")
                    st.write(f"Risk Level: **{risk}**")
                    st.write(f"AI Score: **{score} / 100**")

                    if score >= 40:
                        st.success(f"✅ Recommendation: STRONG BUY ({score}% confidence)")
                    elif score >= 15:
                        st.success(f"📈 Recommendation: BUY ({score}% confidence)")
                    elif score > -10:
                        st.warning("⚠ Recommendation: HOLD")
                    else:
                        st.error("🚨 Recommendation: SELL / AVOID")

# ══════════════════════════════════════════════════════════════
# TAB 6 · COMPARE
# ══════════════════════════════════════════════════════════════
with tab6:
    sec("Portfolio Comparison Tool")

    comp_tickers = [t.strip().upper() for t in compare_input.split(',') if t.strip()]
    PAL = [GOLD2, BLUE, GREEN, '#9b59b6', RED, '#e67e22']

    @st.cache_data(ttl=120)
    def get_compare(tickers, per):
        out = {}
        for t in tickers:
            try:
                d = yf.download(t, period=per, auto_adjust=True, progress=False)
                if isinstance(d.columns, pd.MultiIndex):
                    d.columns = d.columns.get_level_values(0)
                if not d.empty:
                    out[t] = d['Close'].squeeze()
            except:
                pass
        return out

    with st.spinner("Loading comparison data..."):
        comp = get_compare(comp_tickers, period)

    if comp:

        fig_c, axes_c = plt.subplots(2, 2, figsize=(14, 9))
        fig_c.patch.set_facecolor(BG2)

        # Normalized Price
        ax = axes_c[0, 0]
        for i, (t, p) in enumerate(comp.items()):
            norm = p / float(p.iloc[0]) * 100
            ax.plot(norm.index, norm, color=PAL[i % len(PAL)], lw=1.4, label=t)

        ax.axhline(100, color=DIM, lw=0.8, linestyle='--')
        ax.set_title("Normalized Price — Base 100", fontsize=9)
        ax.legend(framealpha=0.8)
        style_ax(ax)

        # Cumulative Returns
        ax = axes_c[0, 1]
        for i, (t, p) in enumerate(comp.items()):
            r = p.pct_change().dropna()
            c2 = (1 + r).cumprod()

            ax.plot(
                c2.index,
                c2,
                color=PAL[i % len(PAL)],
                lw=1.4,
                label=f"{t} {(float(c2.iloc[-1]) - 1) * 100:+.1f}%"
            )

        ax.axhline(1, color=DIM, lw=0.6, linestyle=':')
        ax.set_title("Cumulative Returns", fontsize=9)
        ax.legend(framealpha=0.8)
        style_ax(ax)

        # Annual Volatility
        ax = axes_c[1, 0]

        vols = [
            float(p.pct_change().dropna().std() * np.sqrt(252) * 100)
            for p in comp.values()
        ]

        labs = list(comp.keys())

        bars = ax.bar(
            labs,
            vols,
            color=[PAL[i % len(PAL)] for i in range(len(labs))],
            alpha=0.75,
            width=0.45
        )

        for bar, v in zip(bars, vols):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.3,
                f'{v:.1f}%',
                ha='center',
                va='bottom',
                fontsize=8
            )

        ax.set_title("Annual Volatility (%)", fontsize=9)
        ax.grid(True, alpha=0.3, axis='y')

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Correlation Matrix
        ax = axes_c[1, 1]

        if len(comp) >= 2:

            rdf = pd.DataFrame(
                {t: p.pct_change().dropna() for t, p in comp.items()}
            ).dropna()

            corr = rdf.corr()

            tls = list(corr.columns)
            n = len(tls)

            cmap = LinearSegmentedColormap.from_list(
                'rg',
                [RED, '#f5f7fa', GREEN],
                N=256
            )

            ax.imshow(corr.values, cmap=cmap, vmin=-1, vmax=1, aspect='auto')

            ax.set_xticks(range(n))
            ax.set_yticks(range(n))

            ax.set_xticklabels(tls, fontsize=8)
            ax.set_yticklabels(tls, fontsize=8)

            for i in range(n):
                for j in range(n):
                    ax.text(
                        j,
                        i,
                        f'{corr.values[i, j]:.2f}',
                        ha='center',
                        va='center',
                        fontsize=8
                    )

            ax.set_title("Return Correlation Matrix", fontsize=9)

        else:
            ax.text(
                0.5,
                0.5,
                'Add 2+ tickers for correlation',
                ha='center',
                va='center',
                transform=ax.transAxes,
                color=DIM
            )

        fig_c.tight_layout(pad=2.5)
        st.pyplot(fig_c, use_container_width=True)
        plt.close(fig_c)

        # Performance Summary
        sec("Performance Summary")

        rows = []

        for t, p in comp.items():

            r = p.pct_change().dropna()

            tot = (float(p.iloc[-1]) - float(p.iloc[0])) / float(p.iloc[0]) * 100

            av = float(r.std() * np.sqrt(252) * 100)

            sh = (
                float((r.mean() - 0.05 / 252) / r.std() * np.sqrt(252))
                if r.std() > 0 else 0
            )

            c2 = (1 + r).cumprod()

            dd2 = float(((c2 - c2.cummax()) / c2.cummax()).min() * 100)

            rows.append({
                "Ticker": t,
                "Total Return": f"{tot:+.2f}%",
                "Ann. Volatility": f"{av:.2f}%",
                "Sharpe Ratio": f"{sh:.2f}",
                "Max Drawdown": f"{abs(dd2):.2f}%"
            })

        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        # ───────────────────────────────
        # AI Investment Recommendation
        # ───────────────────────────────

        sec("📊 AI Investment Recommendation")

        rec_scores = []

        for ticker in comp_tickers:

            df_c = fetch_stock(ticker, "6mo")

            if not df_c.empty:

                returns = df_c['Close'].pct_change().dropna()

                total_return = (
                    (df_c['Close'].iloc[-1] / df_c['Close'].iloc[0]) - 1
                ) * 100

                volatility = returns.std() * np.sqrt(252) * 100

                score = total_return - (volatility * 0.5)

                rec_scores.append({
                    "Ticker": ticker,
                    "Return": total_return,
                    "Volatility": volatility,
                    "Score": score
                })

        rec_df = pd.DataFrame(rec_scores)

        if not rec_df.empty:

            best_stock = rec_df.sort_values("Score", ascending=False).iloc[0]

            st.success(
                f"✅ Based on return and risk analysis, "
                f"**{best_stock['Ticker']}** looks like the best stock to invest in right now."
            )

            st.dataframe(rec_df.round(2), use_container_width=True)

    else:
        st.warning("Could not load comparison data. Check tickers.")

# ══════════════════════════════════════════════════════════════
# TAB 7 · PORTFOLIO
# ══════════════════════════════════════════════════════════════

with tab7:

    st.subheader("Portfolio Dashboard")

    portfolio = st.session_state.portfolio
    cash = st.session_state.cash


    # ─────────────────────────────────────────────
    # INVEST IN STOCKS (MULTIPLE STOCK SELECTION)
    # ─────────────────────────────────────────────

    st.subheader("Invest in Stocks")

    # Create list of all stocks
    all_tickers = [(n, s) for grp in STOCK_UNIVERSE.values() for n, s in grp]
    ticker_labels = [f"{name} ({sym})" for name, sym in all_tickers]

    col1, col2, col3 = st.columns([3,1,1])

    with col1:
        chosen = st.selectbox("Select stock", ticker_labels)

        invest_ticker = all_tickers[ticker_labels.index(chosen)][1]

    with col2:
        qty = st.number_input("Quantity", min_value=1, step=1, value=1)

    with col3:
        try:
            price = yf.Ticker(invest_ticker).history(period="1d")["Close"].iloc[-1]
        except:
            price = 0

        st.write(f"Price: ₹{price:,.2f}")


    if st.button("BUY STOCK"):

        cost = qty * price

        if cash >= cost:

            if invest_ticker not in portfolio:

                portfolio[invest_ticker] = {
                    "qty": qty,
                    "buy_price": price
                }

            else:

                old_qty = portfolio[invest_ticker]["qty"]
                old_price = portfolio[invest_ticker]["buy_price"]

                new_qty = old_qty + qty
                new_avg = ((old_qty * old_price) + (qty * price)) / new_qty

                portfolio[invest_ticker]["qty"] = new_qty
                portfolio[invest_ticker]["buy_price"] = new_avg

            st.session_state.cash -= cost

            st.success(f"Bought {qty} shares of {invest_ticker}")

            st.rerun()

        else:
            st.error("Not enough cash")

    st.divider()


    # ─────────────────────────────────────────────
    # PORTFOLIO CALCULATIONS
    # ─────────────────────────────────────────────

    total_invested = 0
    total_value = 0

    rows = []

    for ticker, data in portfolio.items():

        qty = data["qty"]
        buy_price = data["buy_price"]

        try:
            price = yf.Ticker(ticker).history(period="1d")["Close"].iloc[-1]
        except:
            price = buy_price

        invested = qty * buy_price
        value = qty * price

        pnl = value - invested

        total_invested += invested
        total_value += value

        rows.append({
            "Ticker": ticker,
            "Quantity": qty,
            "Buy Price": round(buy_price,2),
            "Current Price": round(price,2),
            "Value": round(value,2),
            "P/L": round(pnl,2)
        })


    total_assets = total_value + cash
    profit = total_value - total_invested
    return_pct = (profit / total_invested * 100) if total_invested > 0 else 0


    # ─────────────────────────────────────────────
    # PORTFOLIO METRICS
    # ─────────────────────────────────────────────

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Cash", f"₹{cash:,.0f}")
    c2.metric("Invested", f"₹{total_invested:,.0f}")
    c3.metric("Portfolio Value", f"₹{total_value:,.0f}")
    c4.metric("Total Return", f"{return_pct:.2f}%")

    st.divider()


    # ─────────────────────────────────────────────
    # HOLDINGS TABLE
    # ─────────────────────────────────────────────

    if rows:

        st.subheader("Holdings")

        df_port = pd.DataFrame(rows)

        st.dataframe(df_port, use_container_width=True)


        # ─────────────────────────────────────────
        # PORTFOLIO ALLOCATION
        # ─────────────────────────────────────────

        st.subheader("Portfolio Allocation")

        labels = df_port["Ticker"]
        values = df_port["Value"]

        fig, ax = plt.subplots()

        ax.pie(values, labels=labels, autopct='%1.1f%%')

        ax.set_title("Portfolio Allocation")

        st.pyplot(fig)

    else:

        st.info("No stocks in portfolio yet.")