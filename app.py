import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="CLUSTER//OPS",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- LOAD DATA ----------------
df = pd.read_csv("clustered_countries.csv")
df_orig = pd.read_csv("Country-data.csv")
df['country'] = df_orig['country']
df = df.merge(df_orig, on='country', how='left')

# Coordinates lookup
COORDS = {
    'Afghanistan': [33.93, 67.71], 'Albania': [41.15, 20.17], 'Algeria': [28.03, 1.66],
    'Angola': [-11.20, 17.87], 'Antigua and Barbuda': [17.06, -61.80], 'Argentina': [-38.42, -63.62],
    'Armenia': [40.07, 45.04], 'Australia': [-25.27, 133.78], 'Austria': [47.52, 14.55],
    'Azerbaijan': [40.14, 47.58], 'Bahamas': [25.03, -77.40], 'Bangladesh': [23.68, 90.36],
    'Belarus': [53.71, 27.95], 'Belgium': [50.50, 4.47], 'Belize': [17.19, -88.50],
    'Benin': [9.31, 2.32], 'Bhutan': [27.51, 90.43], 'Bolivia': [-16.29, -63.59],
    'Bosnia and Herzegovina': [43.92, 17.68], 'Botswana': [-22.33, 24.68],
    'Brazil': [-14.24, -51.93], 'Bulgaria': [42.73, 25.49], 'Burkina Faso': [12.36, -1.56],
    'Burundi': [-3.37, 29.92], 'Cambodia': [12.57, 104.99], 'Cameroon': [3.85, 11.50],
    'Canada': [56.13, -106.35], 'Cape Verde': [16.54, -23.04], 'Central African Republic': [6.61, 20.94],
    'Chad': [15.45, 18.73], 'Chile': [-35.68, -71.54], 'China': [35.86, 104.20],
    'Colombia': [4.57, -74.30], 'Comoros': [-11.88, 43.87], 'Congo, Dem. Rep.': [-4.04, 21.76],
    'Congo, Rep.': [-0.23, 15.83], 'Costa Rica': [9.75, -83.75], 'Croatia': [45.10, 15.20],
    'Czech Republic': [49.82, 15.47], 'Denmark': [56.26, 9.50], 'Djibouti': [11.83, 42.59],
    'Dominican Republic': [18.74, -70.16], 'Ecuador': [-1.83, -78.18], 'Egypt': [26.82, 30.80],
    'El Salvador': [13.79, -88.90], 'Equatorial Guinea': [1.65, 10.27], 'Eritrea': [15.18, 39.78],
    'Estonia': [58.60, 25.01], 'Ethiopia': [9.15, 40.49], 'Fiji': [-16.58, 179.41],
    'Finland': [61.92, 25.75], 'France': [46.23, 2.21], 'Gabon': [-0.80, 11.61],
    'Gambia': [13.44, -15.31], 'Georgia': [42.32, 43.36], 'Germany': [51.17, 10.45],
    'Ghana': [7.95, -1.02], 'Greece': [39.07, 21.82], 'Guatemala': [15.78, -90.23],
    'Guinea': [9.95, -11.24], 'Guinea-Bissau': [11.80, -15.18], 'Guyana': [4.86, -58.93],
    'Haiti': [18.97, -72.29], 'Honduras': [15.20, -86.24], 'Hungary': [47.16, 19.50],
    'India': [20.59, 78.96], 'Indonesia': [-0.79, 113.92], 'Iran': [32.43, 53.69],
    'Iraq': [33.22, 43.68], 'Ireland': [53.41, -8.24], 'Israel': [31.05, 34.85],
    'Italy': [41.87, 12.57], 'Jamaica': [18.11, -77.30], 'Japan': [36.20, 138.25],
    'Jordan': [30.59, 36.24], 'Kazakhstan': [48.02, 66.92], 'Kenya': [-0.02, 37.91],
    'Kiribati': [-3.37, -168.73], 'Kuwait': [29.31, 47.48], 'Kyrgyz Republic': [41.20, 74.76],
    'Laos': [19.86, 102.50], 'Latvia': [56.88, 24.60], 'Lebanon': [33.85, 35.86],
    'Lesotho': [-29.61, 28.23], 'Liberia': [6.43, -9.43], 'Libya': [26.34, 17.23],
    'Lithuania': [55.17, 23.88], 'Luxembourg': [49.82, 6.13], 'Macedonia': [41.61, 21.75],
    'Madagascar': [-18.77, 46.87], 'Malawi': [-13.25, 34.30], 'Malaysia': [4.21, 101.98],
    'Maldives': [3.20, 73.22], 'Mali': [17.57, -3.99], 'Malta': [35.94, 14.38],
    'Mauritania': [21.01, -10.94], 'Mauritius': [-20.35, 57.55], 'Mexico': [23.63, -102.55],
    'Moldova': [47.41, 28.37], 'Mongolia': [46.86, 103.85], 'Montenegro': [42.71, 19.37],
    'Morocco': [31.79, -7.09], 'Mozambique': [-18.67, 35.53], 'Myanmar': [21.92, 95.96],
    'Namibia': [-22.96, 18.49], 'Nepal': [28.39, 84.12], 'Netherlands': [52.13, 5.29],
    'New Zealand': [-40.90, 174.89], 'Nicaragua': [12.87, -85.21], 'Niger': [17.61, 8.08],
    'Nigeria': [9.08, 8.68], 'Norway': [60.47, 8.47], 'Oman': [21.51, 55.92],
    'Pakistan': [30.38, 69.35], 'Panama': [8.54, -80.78], 'Papua New Guinea': [-6.31, 143.96],
    'Paraguay': [-23.44, -58.44], 'Peru': [-9.19, -75.02], 'Philippines': [12.88, 121.77],
    'Poland': [51.92, 19.15], 'Portugal': [39.40, -8.22], 'Qatar': [25.35, 51.18],
    'Romania': [45.94, 24.97], 'Russia': [61.52, 105.32], 'Rwanda': [-1.94, 29.87],
    'Samoa': [-13.76, -172.10], 'Sao Tome and Principe': [0.19, 6.61], 'Saudi Arabia': [23.89, 45.08],
    'Senegal': [14.50, -14.45], 'Sierra Leone': [8.46, -11.78], 'Slovak Republic': [48.67, 19.70],
    'Slovenia': [46.15, 14.99], 'Solomon Islands': [-9.64, 160.16], 'Somalia': [5.15, 46.20],
    'South Africa': [-30.56, 22.94], 'Spain': [40.46, -3.75], 'Sri Lanka': [7.87, 80.77],
    'Sudan': [12.86, 30.22], 'Suriname': [3.92, -56.03], 'Swaziland': [-26.52, 31.47],
    'Sweden': [60.13, 18.64], 'Switzerland': [46.82, 8.23], 'Syria': [34.80, 38.99],
    'Tajikistan': [38.86, 71.28], 'Tanzania': [-6.37, 34.89], 'Thailand': [15.87, 100.99],
    'Timor-Leste': [-8.87, 125.73], 'Togo': [8.62, 0.82], 'Tonga': [-21.18, -175.20],
    'Trinidad and Tobago': [10.69, -61.22], 'Tunisia': [33.89, 9.54], 'Turkey': [38.96, 35.24],
    'Turkmenistan': [38.97, 59.56], 'Uganda': [1.37, 32.29], 'Ukraine': [48.38, 31.17],
    'United Arab Emirates': [23.42, 53.85], 'United Kingdom': [55.38, -3.44],
    'United States': [37.09, -95.71], 'Uruguay': [-32.52, -55.77], 'Uzbekistan': [41.38, 64.59],
    'Vanuatu': [-15.38, 166.96], 'Venezuela': [6.42, -66.59], 'Vietnam': [14.06, 108.28],
    'Yemen': [15.55, 48.52], 'Zambia': [-13.13, 27.85], 'Zimbabwe': [-19.02, 29.15],
    'Ivory Coast': [7.54, -5.55],
}

df['lat'] = df['country'].map(lambda c: COORDS.get(c, [None, None])[0])
df['lng'] = df['country'].map(lambda c: COORDS.get(c, [None, None])[1])
df = df.dropna(subset=['lat', 'lng'])

# Cluster color mapping — hacker palette
CLUSTER_COLORS = {
    0: '#ff003c',   # Critical Red  — underdeveloped / high risk
    1: '#00ffe5',   # Cyan          — developing
    2: '#ffcc00',   # Gold          — emerging
    3: '#39ff14',   # Neon Green    — developed / high income
}

CLUSTER_LABELS = {
    0: 'CRITICAL_RISK',
    1: 'DEVELOPING',
    2: 'EMERGING',
    3: 'HIGH_INCOME',
}

# rgba fill colors for Plotly (rejects 8-digit hex)
CLUSTER_FILL = {
    0: 'rgba(255,0,60,0.08)',
    1: 'rgba(0,255,229,0.08)',
    2: 'rgba(255,204,0,0.08)',
    3: 'rgba(57,255,20,0.08)',
}
CLUSTER_BOX_FILL = {
    0: 'rgba(255,0,60,0.12)',
    1: 'rgba(0,255,229,0.12)',
    2: 'rgba(255,204,0,0.12)',
    3: 'rgba(57,255,20,0.12)',
}

df['cluster_color'] = df['KMeans_Pred'].map(CLUSTER_COLORS)
df['cluster_label'] = df['KMeans_Pred'].map(CLUSTER_LABELS)

# ================ CUSTOM CSS — HACKER TERMINAL ================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Share Tech Mono', monospace !important;
    background: #000 !important;
    color: #00ffe5 !important;
    font-size: 14px !important;
}

.stApp {
    background: #000000 !important;
}

/* Scanline overlay */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0,255,229,0.015) 2px,
        rgba(0,255,229,0.015) 4px
    );
    pointer-events: none;
    z-index: 9999;
}

.block-container {
    padding: 1rem 2rem !important;
    max-width: 100% !important;
}

/* ---- Sidebar ---- */
section[data-testid="stSidebar"] {
    background: #050a0a !important;
    border-right: 1px solid #00ffe520 !important;
}

section[data-testid="stSidebar"] * {
    color: #00ffe5 !important;
}

/* ---- Header ---- */
.hacker-title {
    font-family: 'Orbitron', monospace;
    font-size: 3.2rem;
    font-weight: 900;
    color: #00ffe5;
    text-shadow:
        0 0 10px #00ffe5,
        0 0 30px #00ffe580,
        0 0 60px #00ffe530;
    letter-spacing: 6px;
    text-align: center;
    animation: flicker 4s infinite;
    margin: 0;
    padding: 0.5rem 0;
}

.hacker-sub {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.75rem;
    color: #00ffe580;
    letter-spacing: 4px;
    text-align: center;
    text-transform: uppercase;
    margin-bottom: 0.2rem;
}

.hacker-divider {
    border: none;
    border-top: 1px solid #00ffe530;
    margin: 0.8rem 0;
}

@keyframes flicker {
    0%, 95%, 100% { opacity: 1; }
    96% { opacity: 0.85; }
    97% { opacity: 1; }
    98% { opacity: 0.9; }
    99% { opacity: 1; }
}

/* ---- Metric Cards ---- */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 1.2rem;
}

.metric-card {
    background: #0a0f0f;
    border: 1px solid #00ffe520;
    border-top: 2px solid #00ffe5;
    padding: 14px 18px;
    position: relative;
    overflow: hidden;
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(135deg, #00ffe508 0%, transparent 60%);
    pointer-events: none;
}

.metric-label {
    font-size: 0.6rem;
    letter-spacing: 3px;
    color: #00ffe560;
    text-transform: uppercase;
    margin-bottom: 4px;
}

.metric-value {
    font-family: 'Orbitron', monospace;
    font-size: 1.6rem;
    font-weight: 700;
    color: #00ffe5;
    text-shadow: 0 0 8px #00ffe560;
    line-height: 1;
}

.metric-unit {
    font-size: 0.6rem;
    color: #00ffe540;
    letter-spacing: 2px;
    margin-top: 2px;
}

/* ---- Cluster badges ---- */
.cluster-0 { color: #ff003c !important; text-shadow: 0 0 8px #ff003c80; }
.cluster-1 { color: #00ffe5 !important; text-shadow: 0 0 8px #00ffe580; }
.cluster-2 { color: #ffcc00 !important; text-shadow: 0 0 8px #ffcc0080; }
.cluster-3 { color: #39ff14 !important; text-shadow: 0 0 8px #39ff1480; }

.badge {
    display: inline-block;
    padding: 2px 10px;
    font-size: 0.65rem;
    letter-spacing: 2px;
    border-radius: 0;
    font-family: 'Orbitron', monospace;
    font-weight: 700;
}
.badge-0 { background: #ff003c18; border: 1px solid #ff003c; color: #ff003c; }
.badge-1 { background: #00ffe518; border: 1px solid #00ffe5; color: #00ffe5; }
.badge-2 { background: #ffcc0018; border: 1px solid #ffcc00; color: #ffcc00; }
.badge-3 { background: #39ff1418; border: 1px solid #39ff14; color: #39ff14; }

/* ---- Panel/Glass ---- */
.panel {
    background: #060c0c;
    border: 1px solid #00ffe518;
    padding: 16px 20px;
    margin-bottom: 12px;
    position: relative;
}

.panel-title {
    font-family: 'Orbitron', monospace;
    font-size: 1rem;
    letter-spacing: 4px;
    color: #00ffe5;
    text-transform: uppercase;
    margin-bottom: 14px;
    border-bottom: 2px solid rgba(0,255,229,0.3);
    padding-bottom: 10px;
    text-shadow: 0 0 8px rgba(0,255,229,0.5);
}

/* ---- Country detail card ---- */
.country-card {
    background: #0a1010;
    border: 1px solid #00ffe520;
    border-left: 3px solid #00ffe5;
    padding: 16px;
    margin-bottom: 8px;
    font-size: 0.8rem;
}

.country-name {
    font-family: 'Orbitron', monospace;
    font-size: 1rem;
    font-weight: 700;
    color: #fff;
    letter-spacing: 2px;
    margin-bottom: 8px;
}

.stat-row {
    display: flex;
    justify-content: space-between;
    border-bottom: 1px solid #00ffe510;
    padding: 4px 0;
    font-size: 0.72rem;
}

.stat-key { color: #00ffe560; letter-spacing: 1px; }
.stat-val { color: #fff; font-weight: bold; }

/* ---- Selectbox & widgets ---- */
.stSelectbox > div > div {
    background: #0a0f0f !important;
    border: 1px solid #00ffe530 !important;
    color: #00ffe5 !important;
    font-family: 'Share Tech Mono', monospace !important;
    border-radius: 0 !important;
}

.stMultiSelect > div > div {
    background: #0a0f0f !important;
    border: 1px solid #00ffe530 !important;
    border-radius: 0 !important;
}

.stSlider > div > div > div {
    background: #00ffe5 !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #050a0a !important;
    border-bottom: 1px solid #00ffe520 !important;
    gap: 0 !important;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #00ffe550 !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 0.8rem !important;
    letter-spacing: 3px !important;
    border-radius: 0 !important;
    padding: 8px 20px !important;
    border: none !important;
}

.stTabs [aria-selected="true"] {
    color: #00ffe5 !important;
    border-bottom: 2px solid #00ffe5 !important;
    text-shadow: 0 0 8px #00ffe560 !important;
}

.stDataFrame {
    background: #060c0c !important;
    border: 1px solid #00ffe520 !important;
}

/* Sidebar widgets */
.stRadio > label, .stCheckbox > label {
    color: #00ffe5 !important;
    font-size: 0.75rem !important;
    letter-spacing: 1px !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #050a0a; }
::-webkit-scrollbar-thumb { background: #00ffe540; border-radius: 0; }
::-webkit-scrollbar-thumb:hover { background: #00ffe5; }

/* Markdown text — readable overrides */
p, li { color: #00ffe5 !important; font-size: 0.85rem; line-height: 1.6; }
h1, h2, h3, h4 {
    color: #00ffe5 !important;
    font-family: 'Orbitron', monospace !important;
    letter-spacing: 3px !important;
}

/* Slider labels and values — ensure visible */
[data-testid="stSlider"] label,
[data-testid="stSlider"] p {
    color: #00ffe5 !important;
    font-size: 0.7rem !important;
    letter-spacing: 2px !important;
}
[data-testid="stSlider"] [data-testid="stTickBarMin"],
[data-testid="stSlider"] [data-testid="stTickBarMax"],
[data-testid="stSlider"] span {
    color: #00ffe580 !important;
    font-size: 0.65rem !important;
}

/* Selectbox text */
[data-testid="stSelectbox"] label,
[data-testid="stSelectbox"] p {
    color: #00ffe5 !important;
    font-size: 0.7rem !important;
}
[data-testid="stSelectbox"] div[data-baseweb="select"] span {
    color: #00ffe5 !important;
}

/* Checkbox labels */
[data-testid="stCheckbox"] label,
[data-testid="stCheckbox"] p,
[data-testid="stCheckbox"] span {
    color: #00ffe5 !important;
    font-size: 0.75rem !important;
}

/* Input text */
[data-testid="stTextInput"] input {
    background: #0a1010 !important;
    color: #00ffe5 !important;
    border: 1px solid #00ffe530 !important;
    font-family: 'Share Tech Mono', monospace !important;
}

/* Sidebar labels */
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] p {
    color: #00ffe5 !important;
    font-size: 0.9rem !important;
    letter-spacing: 1px !important;
}

/* Metric delta text */
[data-testid="stMetricDelta"] {
    color: #39ff14 !important;
    font-size: 0.65rem !important;
}

/* Plotly charts bg — no border, free globe */
.js-plotly-plot { border: none !important; background: transparent !important; }
.stPlotlyChart { border: none !important; background: transparent !important; padding: 0 !important; }

/* Status bar */
.status-bar {
    display: flex;
    justify-content: space-between;
    font-size: 0.75rem;
    letter-spacing: 2px;
    color: #00ffe540;
    border-top: 1px solid #00ffe515;
    padding-top: 6px;
    margin-top: 8px;
}

.blink {
    animation: blink 1s step-end infinite;
}
@keyframes blink {
    50% { opacity: 0; }
}

/* Override st.metric */
[data-testid="metric-container"] {
    background: #0a0f0f !important;
    border: 1px solid #00ffe520 !important;
    border-top: 2px solid #00ffe5 !important;
    padding: 12px !important;
}
[data-testid="metric-container"] label {
    font-size: 0.6rem !important;
    letter-spacing: 3px !important;
    color: #00ffe560 !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: 'Orbitron', monospace !important;
    font-size: 2.2rem !important;
    color: #00ffe5 !important;
    text-shadow: 0 0 16px rgba(0,255,229,0.7) !important;
    font-weight: 900 !important;
}
[data-testid="metric-container"] label {
    font-size: 0.75rem !important;
    letter-spacing: 3px !important;
    color: #00ffe560 !important;
}

/* Footer */
.footer {
    text-align: center;
    font-size: 0.55rem;
    letter-spacing: 4px;
    color: #00ffe530;
    margin-top: 2rem;
    border-top: 1px solid #00ffe515;
    padding-top: 12px;
}

/* Progress bars */
.progress-bar-wrap {
    background: #0a0f0f;
    border: 1px solid #00ffe520;
    height: 6px;
    margin-top: 3px;
    position: relative;
    overflow: hidden;
}
.progress-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, #00ffe5, #00ffe580);
    box-shadow: 0 0 8px #00ffe5;
}

/* Live status dot */
.live-dot {
    display: inline-block;
    width: 7px; height: 7px;
    background: #39ff14;
    border-radius: 50%;
    box-shadow: 0 0 8px #39ff14;
    animation: pulse-dot 1.5s ease-in-out infinite;
    margin-right: 6px;
    vertical-align: middle;
}
@keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.7); }
}

/* Top nav bar */
.top-nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #050a0a;
    border: 1px solid rgba(0,255,229,0.15);
    border-top: 3px solid #00ffe5;
    padding: 12px 24px;
    margin-bottom: 12px;
    font-size: 0.85rem;
    letter-spacing: 3px;
}
.nav-brand {
    font-family: 'Orbitron', monospace;
    font-size: 1.6rem;
    font-weight: 900;
    color: #00ffe5;
    text-shadow: 0 0 14px #00ffe5, 0 0 35px rgba(0,255,229,0.6);
    letter-spacing: 8px;
}
.nav-status { color: #39ff14; font-size: 0.85rem; letter-spacing: 3px; font-weight: bold; }
.nav-info { color: #00ffe5; font-size: 0.85rem; letter-spacing: 2px; }

/* Big stat numbers like reference image */
.big-stat {
    font-family: 'Orbitron', monospace;
    font-size: 2.4rem;
    font-weight: 900;
    color: #00ffe5;
    text-shadow: 0 0 10px #00ffe580;
    letter-spacing: 2px;
    line-height: 1;
}
.big-stat-label {
    font-size: 0.85rem;
    letter-spacing: 3px;
    color: #00ffe550;
    text-transform: uppercase;
    margin-bottom: 2px;
}
.big-stat-delta {
    font-size: 0.65rem;
    letter-spacing: 1px;
    margin-top: 2px;
}
.delta-pos { color: #39ff14; }
.delta-neg { color: #ff003c; }

/* Events feed like right panel in reference */
.event-feed {
    font-size: 0.85rem;
    letter-spacing: 1px;
}
.event-item {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding: 6px 0;
    border-bottom: 1px solid #00ffe510;
}
.event-icon { color: #00ffe560; margin-right: 8px; }
.event-country { color: #fff; }
.event-cluster { font-size: 0.55rem; letter-spacing: 2px; }
.event-tag {
    font-size: 0.72rem;
    padding: 3px 8px;
    border-radius: 0;
    font-family: 'Orbitron', monospace;
    letter-spacing: 2px;
    font-weight: bold;
    white-space: nowrap;
}
.tag-0 { background: #ff003c20; border: 1px solid #ff003c; color: #ff003c; }
.tag-1 { background: #00ffe520; border: 1px solid #00ffe5; color: #00ffe5; }
.tag-2 { background: #ffcc0020; border: 1px solid #ffcc00; color: #ffcc00; }
.tag-3 { background: #39ff1420; border: 1px solid #39ff14; color: #39ff14; }

/* Contributions heatmap grid */
.contrib-grid {
    display: grid;
    grid-template-columns: repeat(8, 1fr);
    gap: 3px;
    margin-top: 6px;
}
.contrib-cell {
    height: 12px;
    border-radius: 1px;
    background: #00ffe530;
}
.contrib-cell.high { background: #00ffe5; box-shadow: 0 0 4px #00ffe5; }
.contrib-cell.mid { background: #00ffe590; }
.contrib-cell.low { background: #00ffe530; }
.contrib-cell.off { background: #0a1010; }
</style>
""", unsafe_allow_html=True)


# ================ HEADER ================
import datetime
now_utc = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S UTC")

st.markdown(f"""
<div class="top-nav">
    <div>
        <span class="nav-brand">CLUSTER//OPS</span>
        <span style="font-size:0.55rem; color:#00ffe540; margin-left:14px; letter-spacing:2px;">v2.5 · KMEANS+PCA</span>
    </div>
    <div style="display:flex; gap:24px; align-items:center;">
        <span><span class="live-dot"></span><span class="nav-status">LIVE</span></span>
        <span class="nav-info">Global</span>
        <span style="background:#ff003c20; border:1px solid #ff003c; color:#ff003c; padding:2px 10px; font-size:0.55rem; letter-spacing:2px; font-family:'Orbitron',monospace;">DEFCON 4</span>
    </div>
    <div style="text-align:right;">
        <div class="nav-info">{now_utc}</div>
        <div style="color:#00ffe540; font-size:0.5rem; letter-spacing:2px; margin-top:2px;">167 NATIONS · K=4</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ================ SIDEBAR ================
with st.sidebar:
    st.markdown("""
    <div style="font-family:'Orbitron',monospace; font-size:0.7rem; letter-spacing:4px; color:#00ffe5; margin-bottom:16px; border-bottom:1px solid #00ffe520; padding-bottom:8px;">
    ⬡ CONTROL_PANEL
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="font-size:0.6rem; letter-spacing:2px; color:#00ffe560; margin-bottom:4px;">SELECT CLUSTER NODE</div>', unsafe_allow_html=True)
    all_clusters = sorted(df['KMeans_Pred'].unique())
    cluster_options = {f"CLUSTER_{c} [{CLUSTER_LABELS[c]}]": c for c in all_clusters}
    cluster_options["ALL CLUSTERS"] = -1
    selected_label = st.selectbox("Select Cluster Node", list(cluster_options.keys()), label_visibility="collapsed")
    selected_cluster = cluster_options[selected_label]

    st.markdown('<hr style="border-color:#00ffe515; margin:12px 0;">', unsafe_allow_html=True)

    st.markdown('<div style="font-size:0.6rem; letter-spacing:2px; color:#00ffe560; margin-bottom:4px;">FILTER BY METRIC</div>', unsafe_allow_html=True)
    gdpp_range = st.slider("GDP/capita range", int(df['gdpp'].min()), int(df['gdpp'].max()),
                           (int(df['gdpp'].min()), int(df['gdpp'].max())), label_visibility="visible")

    life_range = st.slider("Life expectancy", float(df['life_expec'].min()), float(df['life_expec'].max()),
                           (float(df['life_expec'].min()), float(df['life_expec'].max())), label_visibility="visible")

    st.markdown('<hr style="border-color:#00ffe515; margin:12px 0;">', unsafe_allow_html=True)

    st.markdown('<div style="font-size:0.6rem; letter-spacing:2px; color:#00ffe560; margin-bottom:4px;">GLOBE PROJECTION</div>', unsafe_allow_html=True)
    projection = st.selectbox("Globe Projection", ["orthographic", "natural earth", "mercator", "azimuthal equal area"],
                               label_visibility="collapsed")

    show_arcs = st.checkbox("Show connection arcs", value=False)
    show_labels = st.checkbox("Show country labels", value=True)

    st.markdown("""
    <div style="margin-top:20px; font-size:0.55rem; letter-spacing:2px; color:#00ffe530; border-top:1px solid #00ffe515; padding-top:10px;">
    <span class="blink">▮</span> CLUSTER//OPS v2.0 · KMEANS · PCA<br>
    ░░░░░░░░░░░░░░░░░░░░░░░░░░<br>
    ALL SYSTEMS NOMINAL
    </div>
    """, unsafe_allow_html=True)


# ================ FILTER DATA ================
mask = (df['gdpp'] >= gdpp_range[0]) & (df['gdpp'] <= gdpp_range[1]) & \
       (df['life_expec'] >= life_range[0]) & (df['life_expec'] <= life_range[1])
if selected_cluster != -1:
    mask &= (df['KMeans_Pred'] == selected_cluster)
filtered = df[mask].copy()


# ================ METRICS ================
cluster_counts = df['KMeans_Pred'].value_counts().sort_index()
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("TOTAL NODES", f"{len(filtered)}", f"of {len(df)}")
with m2:
    avg_gdp = int(filtered['gdpp'].mean()) if len(filtered) > 0 else 0
    st.metric("AVG GDP/CAPITA", f"${avg_gdp:,}")
with m3:
    avg_life = round(filtered['life_expec'].mean(), 1) if len(filtered) > 0 else 0
    st.metric("AVG LIFE EXPEC", f"{avg_life} yrs")
with m4:
    avg_mort = round(filtered['child_mort'].mean(), 1) if len(filtered) > 0 else 0
    st.metric("AVG CHILD MORT", f"{avg_mort}‰")

st.markdown('<hr style="border-color:#00ffe515; margin:0.5rem 0;">', unsafe_allow_html=True)


# ================ TABS ================
tab1, tab2, tab3, tab4 = st.tabs(["🌐  GLOBE", "⬡  PCA_SPACE", "▦  ANALYTICS", "◈  DATA_MATRIX"])

# ---- TAB 1: GLOBE ----
with tab1:
    col_left, col_globe, col_right = st.columns([1, 4, 1])

    with col_left:
        # Left stats panel like reference image
        st.markdown('<div class="panel-title">◈ GLOBAL STATS</div>', unsafe_allow_html=True)
        
        total_countries = len(df)
        filtered_count = len(filtered)
        avg_gdp_all = int(df['gdpp'].mean())
        
        for cluster_id, label in CLUSTER_LABELS.items():
            count = len(df[df['KMeans_Pred'] == cluster_id])
            color = CLUSTER_COLORS[cluster_id]
            pct = round(count / total_countries * 100, 1)
            st.markdown(f"""
            <div style="margin-bottom:14px;">
                <div style="font-size:0.82rem; letter-spacing:3px; color:{color}; font-family:'Orbitron',monospace; margin-bottom:4px; text-shadow:0 0 6px {color}80;">[{cluster_id}] {label}</div>
                <div class="big-stat" style="color:{color}; font-size:1.6rem;">{count:,}</div>
                <div style="font-size:0.82rem; color:#ffffff; letter-spacing:2px; margin-top:2px;">NATIONS</div>
                <div class="progress-bar-wrap" style="margin-top:4px;">
                    <div class="progress-bar-fill" style="width:{pct}%; background:linear-gradient(90deg, {color}, {color}80); box-shadow: 0 0 6px {color};"></div>
                </div>
                <div style="font-size:0.55rem; color:{color}60; letter-spacing:2px; margin-top:2px;">{pct}% of TOTAL</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<hr style="border-color:#00ffe515; margin:10px 0;">', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="margin-bottom:10px;">
            <div class="big-stat-label">TOTAL NODES</div>
            <div class="big-stat">{filtered_count}</div>
            <div style="font-size:0.55rem; color:#00ffe550; letter-spacing:2px;">of {total_countries} COUNTRIES</div>
        </div>
        <div>
            <div class="big-stat-label">AVG GDP/CAP</div>
            <div class="big-stat" style="font-size:1.1rem;">${avg_gdp_all:,}</div>
        </div>
        """, unsafe_allow_html=True)

    with col_globe:
        # Build globe
        fig_globe = go.Figure()

        clusters_to_show = all_clusters if selected_cluster == -1 else [selected_cluster]

        for c in all_clusters:
            cdf = filtered[filtered['KMeans_Pred'] == c] if c in clusters_to_show else pd.DataFrame()
            if len(cdf) == 0:
                continue

            color = CLUSTER_COLORS[c]

            fig_globe.add_trace(go.Scattergeo(
                lat=cdf['lat'],
                lon=cdf['lng'],
                mode='markers+text' if show_labels else 'markers',
                marker=dict(
                    size=10,
                    color=color,
                    opacity=0.9,
                    line=dict(width=1, color='rgba(0,0,0,0.5)'),
                    symbol='circle',
                ),
                text=cdf['country'] if show_labels else None,
                textposition='top center',
                textfont=dict(size=9, color=color, family='Share Tech Mono'),
                customdata=cdf[['country', 'gdpp', 'life_expec', 'child_mort', 'income', 'cluster_label']].values,
                hovertemplate=(
                    "<b style='color:" + color + "'>%{customdata[0]}</b><br>"
                    "━━━━━━━━━━━━━━━━<br>"
                    "CLUSTER : %{customdata[5]}<br>"
                    "GDP/CAP : $%{customdata[1]:,.0f}<br>"
                    "LIFE EXP: %{customdata[2]:.1f} yrs<br>"
                    "CHILD MORT: %{customdata[3]:.1f}‰<br>"
                    "INCOME  : $%{customdata[4]:,.0f}<br>"
                    "<extra></extra>"
                ),
                name=f"[{c}] {CLUSTER_LABELS[c]}",
                showlegend=True,
            ))

        # Optional: connection arcs from centroid
        if show_arcs and len(filtered) > 1:
            centroid_lat = filtered['lat'].mean()
            centroid_lon = filtered['lng'].mean()
            sample = filtered.sample(min(20, len(filtered)), random_state=42)
            for _, row in sample.iterrows():
                fig_globe.add_trace(go.Scattergeo(
                    lat=[centroid_lat, row['lat']],
                    lon=[centroid_lon, row['lng']],
                    mode='lines',
                    line=dict(width=0.5, color='rgba(0,255,229,0.12)'),
                    showlegend=False,
                    hoverinfo='skip',
                ))

        proj_map = {
            "orthographic": "orthographic",
            "natural earth": "natural earth",
            "mercator": "mercator",
            "azimuthal equal area": "azimuthal equal area"
        }

        fig_globe.update_geos(
            projection_type=proj_map[projection],
            showland=True, landcolor='#0d1f1f',
            showocean=True, oceancolor='#040d0d',
            showcountries=True, countrycolor='#1a4040',
            showcoastlines=True, coastlinecolor='#1a5555',
            showframe=False,
            bgcolor='#000000',
            lataxis_showgrid=True,
            lonaxis_showgrid=True,
            lataxis=dict(gridcolor='rgba(0,255,229,0.05)'),
            lonaxis=dict(gridcolor='rgba(0,255,229,0.05)'),
        )

        fig_globe.update_layout(
            paper_bgcolor='#000000',
            plot_bgcolor='#000000',
            geo_bgcolor='#000000',
            margin=dict(l=0, r=0, t=0, b=0),
            height=720,
            legend=dict(
                font=dict(family='Share Tech Mono', size=10, color='#00ffe5'),
                bgcolor='rgba(6,12,12,0.8)',
                bordercolor='rgba(0,255,229,0.13)',
                borderwidth=1,
                x=0.01, y=0.01,
            ),
            hoverlabel=dict(
                bgcolor='#060c0c',
                font=dict(family='Share Tech Mono', size=11, color='#00ffe5'),
                bordercolor='rgba(0,255,229,0.25)',
            ),
        )

        st.plotly_chart(fig_globe, use_container_width=True, config={'displayModeBar': False})

    with col_right:
        # Right events feed like reference image
        st.markdown('<div class="panel-title">◈ EVENTS FEED</div>', unsafe_allow_html=True)

        top_events = filtered.nlargest(12, 'gdpp')[['country', 'KMeans_Pred', 'cluster_label', 'gdpp', 'life_expec']].reset_index(drop=True)
        
        for _, row in top_events.iterrows():
            c_id = row['KMeans_Pred']
            color = CLUSTER_COLORS[c_id]
            gdp_fmt = f"${int(row['gdpp']):,}"
            label_short = CLUSTER_LABELS[c_id][:4]
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; align-items:center;
                        padding:8px 0; border-bottom:1px solid rgba(0,255,229,0.12);">
                <div>
                    <div style="color:{color}; font-size:1rem; font-family:'Orbitron',monospace;
                                font-weight:700; letter-spacing:1px; text-shadow:0 0 6px {color}80;">
                        {row['country'][:18]}
                    </div>
                    <div style="color:#ffffff; font-size:0.82rem; letter-spacing:1px; margin-top:3px;">
                        GDP: <b style="color:{color};">{gdp_fmt}</b> &nbsp;·&nbsp; LE: <b style="color:#fff;">{row['life_expec']:.0f} yrs</b>
                    </div>
                </div>
                <div style="background:{color}22; border:1px solid {color}; color:{color};
                            font-family:'Orbitron',monospace; font-size:0.72rem;
                            font-weight:700; padding:4px 8px; letter-spacing:2px;
                            text-shadow:0 0 6px {color}; min-width:48px; text-align:center;">
                    {label_short}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<hr style="border-color:#00ffe515; margin:10px 0;">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">◈ ANALYTICS</div>', unsafe_allow_html=True)

        # Mini contribution heatmap
        st.markdown(f"""
        <div style="font-size:0.85rem; letter-spacing:3px; color:#00ffe5; margin-bottom:8px; font-family:'Orbitron',monospace;">CLUSTER DENSITY</div>
        <div class="contrib-grid">
        {''.join([f'<div class="contrib-cell {"high" if i % 7 == 0 else "mid" if i % 3 == 0 else "low" if i % 2 == 0 else "off"}"></div>' for i in range(32)])}
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="margin-top:12px;">
            <div style="display:flex; justify-content:space-between; font-size:1rem; padding:7px 0; border-bottom:1px solid rgba(0,255,229,0.15);">
                <span style="color:#00ffe5; letter-spacing:3px; font-family:'Orbitron',monospace; font-size:0.8rem;">NATIONS</span>
                <span style="color:#39ff14; font-family:'Orbitron',monospace; font-size:1.3rem; font-weight:900; text-shadow:0 0 8px #39ff14;">+{len(filtered)}</span>
            </div>
            <div style="display:flex; justify-content:space-between; font-size:1rem; padding:7px 0; border-bottom:1px solid rgba(0,255,229,0.15);">
                <span style="color:#00ffe5; letter-spacing:3px; font-family:'Orbitron',monospace; font-size:0.8rem;">CLUSTERS</span>
                <span style="color:#00ffe5; font-family:'Orbitron',monospace; font-size:1.3rem; font-weight:900; text-shadow:0 0 8px #00ffe5;">4</span>
            </div>
            <div style="display:flex; justify-content:space-between; font-size:1rem; padding:7px 0; border-bottom:1px solid rgba(0,255,229,0.15);">
                <span style="color:#00ffe5; letter-spacing:3px; font-family:'Orbitron',monospace; font-size:0.8rem;">ALGO</span>
                <span style="color:#ffcc00; font-family:'Orbitron',monospace; font-size:1rem; font-weight:900; text-shadow:0 0 8px #ffcc00;">KMEANS</span>
            </div>
            <div style="display:flex; justify-content:space-between; font-size:1rem; padding:7px 0;">
                <span style="color:#00ffe5; letter-spacing:3px; font-family:'Orbitron',monospace; font-size:0.8rem;">DIM·RED</span>
                <span style="color:#ff003c; font-family:'Orbitron',monospace; font-size:1rem; font-weight:900; text-shadow:0 0 8px #ff003c;">PCA</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Bottom row: GDP bar chart fills blank space ──
    st.markdown('<div class="panel-title" style="margin-top:1rem;">◈ GDP/CAPITA BY CLUSTER · TOP 20 NATIONS</div>', unsafe_allow_html=True)
    top20 = filtered.nlargest(20, 'gdpp')[['country', 'gdpp', 'KMeans_Pred', 'cluster_label']].copy()
    top20['color'] = top20['KMeans_Pred'].map(CLUSTER_COLORS)
    fig_bar = go.Figure(go.Bar(
        x=top20['country'],
        y=top20['gdpp'],
        marker_color=top20['color'],
        marker_line_width=0,
        hovertemplate='<b>%{x}</b><br>GDP/CAP: $%{y:,.0f}<extra></extra>',
    ))
    fig_bar.update_layout(
        paper_bgcolor='#000000', plot_bgcolor='#040d0d',
        font=dict(family='Share Tech Mono', color='#00ffe5', size=12),
        xaxis=dict(gridcolor='rgba(0,255,229,0.06)', tickangle=-40, tickfont=dict(size=11, color='#00ffe5')),
        yaxis=dict(gridcolor='rgba(0,255,229,0.06)', tickprefix='$', tickfont=dict(size=11, color='#00ffe5')),
        margin=dict(l=10, r=10, t=10, b=80),
        height=280,
        bargap=0.3,
        hoverlabel=dict(bgcolor='#060c0c', font=dict(family='Share Tech Mono', color='#00ffe5', size=12)),
    )
    st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})


# ---- TAB 2: PCA SPACE ----
with tab2:
    c1, c2 = st.columns([2, 1])

    with c1:
        color_seq = [CLUSTER_COLORS[c] for c in sorted(df['KMeans_Pred'].unique())]

        fig_pca = px.scatter(
            filtered,
            x='PC1', y='PC2',
            color='cluster_label',
            color_discrete_sequence=color_seq,
            hover_data={'country': True, 'gdpp': True, 'life_expec': True, 'child_mort': True,
                        'PC1': ':.3f', 'PC2': ':.3f', 'cluster_label': True},
            title='',
            labels={'cluster_label': 'CLUSTER', 'PC1': 'PC1 AXIS', 'PC2': 'PC2 AXIS'},
        )
        fig_pca.update_traces(
            marker=dict(size=9, opacity=0.85, line=dict(width=0.5, color='rgba(0,0,0,0.5)')),
        )
        fig_pca.update_layout(
            paper_bgcolor='#000000',
            plot_bgcolor='#040d0d',
            font=dict(family='Share Tech Mono', color='#00ffe5', size=13),
            xaxis=dict(gridcolor='rgba(0,255,229,0.06)', zerolinecolor='rgba(0,255,229,0.13)', tickfont=dict(color='rgba(0,255,229,0.6)')),
            yaxis=dict(gridcolor='rgba(0,255,229,0.06)', zerolinecolor='rgba(0,255,229,0.13)', tickfont=dict(color='rgba(0,255,229,0.6)')),
            legend=dict(bgcolor='#060c0c', bordercolor='rgba(0,255,229,0.13)', borderwidth=1),
            margin=dict(l=10, r=10, t=10, b=10),
            height=420,
            hoverlabel=dict(bgcolor='#060c0c', font=dict(family='Share Tech Mono', size=11, color='#00ffe5'), bordercolor='rgba(0,255,229,0.25)'),
        )
        st.plotly_chart(fig_pca, use_container_width=True, config={'displayModeBar': False})

    with c2:
        # Radar chart for selected cluster averages
        st.markdown('<div class="panel-title">CLUSTER SIGNATURE</div>', unsafe_allow_html=True)
        metrics = ['child_mort', 'exports', 'health', 'income', 'life_expec', 'gdpp']
        labels = ['CHILD_MORT', 'EXPORTS', 'HEALTH', 'INCOME', 'LIFE_EXP', 'GDP/CAP']

        fig_radar = go.Figure()
        for c in all_clusters:
            cdf = df[df['KMeans_Pred'] == c]
            vals = []
            for m in metrics:
                mn, mx = df[m].min(), df[m].max()
                norm = (cdf[m].mean() - mn) / (mx - mn) if mx != mn else 0
                vals.append(round(norm, 3))
            vals.append(vals[0])  # close loop

            fig_radar.add_trace(go.Scatterpolar(
                r=vals,
                theta=labels + [labels[0]],
                fill='toself',
                name=f"C{c}:{CLUSTER_LABELS[c]}",
                line=dict(color=CLUSTER_COLORS[c], width=2),
                fillcolor=CLUSTER_FILL[c],
            ))

        fig_radar.update_layout(
            polar=dict(
                bgcolor='#040d0d',
                radialaxis=dict(visible=True, range=[0, 1], gridcolor='rgba(0,255,229,0.08)',
                                tickfont=dict(color='rgba(0,255,229,0.25)', size=8), showticklabels=False),
                angularaxis=dict(tickfont=dict(color='#00ffe5', size=10, family='Share Tech Mono'),
                                 gridcolor='rgba(0,255,229,0.08)', linecolor='rgba(0,255,229,0.13)'),
            ),
            paper_bgcolor='#000000',
            font=dict(family='Share Tech Mono', color='#00ffe5', size=13),
            legend=dict(bgcolor='#060c0c', bordercolor='rgba(0,255,229,0.13)', borderwidth=1, font=dict(size=10)),
            margin=dict(l=10, r=10, t=10, b=10),
            height=380,
        )
        st.plotly_chart(fig_radar, use_container_width=True, config={'displayModeBar': False})


# ---- TAB 3: ANALYTICS ----
with tab3:
    a1, a2 = st.columns(2)

    with a1:
        # Distribution donut
        cluster_counts_f = filtered['KMeans_Pred'].value_counts().reset_index()
        cluster_counts_f.columns = ['KMeans_Pred', 'count']
        cluster_counts_f['label'] = cluster_counts_f['KMeans_Pred'].map(CLUSTER_LABELS)
        cluster_counts_f['color'] = cluster_counts_f['KMeans_Pred'].map(CLUSTER_COLORS)

        fig_donut = go.Figure(go.Pie(
            labels=cluster_counts_f['label'],
            values=cluster_counts_f['count'],
            hole=0.65,
            marker=dict(colors=cluster_counts_f['color'], line=dict(color='#000', width=2)),
            textfont=dict(family='Share Tech Mono', color='#00ffe5', size=13),
            hovertemplate='<b>%{label}</b><br>%{value} nations<br>%{percent}<extra></extra>',
        ))
        fig_donut.add_annotation(
            text=f"<b>{len(filtered)}</b><br><span style='font-size:10'>NODES</span>",
            x=0.5, y=0.5, font_size=18, showarrow=False,
            font=dict(color='#00ffe5', family='Orbitron')
        )
        fig_donut.update_layout(
            paper_bgcolor='#000000', plot_bgcolor='#000000',
            font=dict(family='Share Tech Mono', color='#00ffe5'),
            legend=dict(bgcolor='#060c0c', bordercolor='rgba(0,255,229,0.13)', borderwidth=1),
            margin=dict(l=10, r=10, t=10, b=10), height=340,
            hoverlabel=dict(bgcolor='#060c0c', font=dict(family='Share Tech Mono', color='#00ffe5')),
        )
        st.plotly_chart(fig_donut, use_container_width=True, config={'displayModeBar': False})

    with a2:
        # Box plot GDP by cluster
        fig_box = go.Figure()
        for c in all_clusters:
            cdf = filtered[filtered['KMeans_Pred'] == c]
            if len(cdf) == 0:
                continue
            fig_box.add_trace(go.Box(
                y=cdf['gdpp'],
                name=f"C{c}",
                marker_color=CLUSTER_COLORS[c],
                line_color=CLUSTER_COLORS[c],
                fillcolor=CLUSTER_BOX_FILL[c],
                boxmean=True,
            ))
        fig_box.update_layout(
            paper_bgcolor='#000000', plot_bgcolor='#040d0d',
            font=dict(family='Share Tech Mono', color='#00ffe5', size=13),
            xaxis=dict(gridcolor='rgba(0,255,229,0.06)', title='CLUSTER'),
            yaxis=dict(gridcolor='rgba(0,255,229,0.06)', title='GDP/CAPITA ($)'),
            margin=dict(l=10, r=10, t=10, b=10), height=340,
            showlegend=False,
            hoverlabel=dict(bgcolor='#060c0c', font=dict(family='Share Tech Mono', color='#00ffe5')),
        )
        st.plotly_chart(fig_box, use_container_width=True, config={'displayModeBar': False})

    # Scatter matrix
    st.markdown('<div class="panel-title">CORRELATION MATRIX · GDP vs LIFE EXPECTANCY vs CHILD MORTALITY</div>', unsafe_allow_html=True)
    fig_scatter3 = px.scatter(
        filtered, x='gdpp', y='life_expec',
        size='child_mort', size_max=30,
        color='cluster_label',
        color_discrete_sequence=list(CLUSTER_COLORS.values()),
        hover_data=['country', 'gdpp', 'life_expec', 'child_mort'],
        labels={'gdpp': 'GDP/CAPITA ($)', 'life_expec': 'LIFE EXPECTANCY', 'cluster_label': 'CLUSTER'},
    )
    fig_scatter3.update_layout(
        paper_bgcolor='#000000', plot_bgcolor='#040d0d',
        font=dict(family='Share Tech Mono', color='#00ffe5', size=13),
        xaxis=dict(gridcolor='rgba(0,255,229,0.06)', zerolinecolor='rgba(0,255,229,0.13)'),
        yaxis=dict(gridcolor='rgba(0,255,229,0.06)', zerolinecolor='rgba(0,255,229,0.13)'),
        legend=dict(bgcolor='#060c0c', bordercolor='rgba(0,255,229,0.13)', borderwidth=1),
        margin=dict(l=10, r=10, t=10, b=10), height=340,
        hoverlabel=dict(bgcolor='#060c0c', font=dict(family='Share Tech Mono', color='#00ffe5')),
    )
    st.plotly_chart(fig_scatter3, use_container_width=True, config={'displayModeBar': False})


# ---- TAB 4: DATA MATRIX ----
with tab4:
    st.markdown('<div class="panel-title">RAW DATA MATRIX · FILTERED RESULTS</div>', unsafe_allow_html=True)

    search = st.text_input("", placeholder=">> SEARCH COUNTRY...", label_visibility="collapsed")
    if search:
        display_df = filtered[filtered['country'].str.contains(search, case=False)]
    else:
        display_df = filtered

    display_cols = ['country', 'cluster_label', 'gdpp', 'income', 'life_expec',
                    'child_mort', 'exports', 'imports', 'health', 'inflation', 'total_fer', 'PC1', 'PC2']
    display_df = display_df[display_cols].rename(columns={
        'country': 'COUNTRY', 'cluster_label': 'CLUSTER', 'gdpp': 'GDP/CAP',
        'income': 'INCOME', 'life_expec': 'LIFE_EXP', 'child_mort': 'CHILD_MORT',
        'exports': 'EXPORTS%', 'imports': 'IMPORTS%', 'health': 'HEALTH%',
        'inflation': 'INFLATION', 'total_fer': 'FERTILITY', 'PC1': 'PC1', 'PC2': 'PC2'
    })

    label_to_color = {label: CLUSTER_COLORS[k] for k, label in CLUSTER_LABELS.items()}
    def color_cluster(v):
        return f'color: {label_to_color.get(v, "#00ffe5")}; font-weight: bold;'
    try:
        styled = display_df.style.map(color_cluster, subset=['CLUSTER'])
    except AttributeError:
        styled = display_df.style.applymap(color_cluster, subset=['CLUSTER'])
    st.dataframe(styled, use_container_width=True, height=420)

    st.markdown(f"""
    <div class="status-bar">
        <span>ROWS: {len(display_df)}</span>
        <span>COLS: {len(display_df.columns)}</span>
        <span>ALGO: K-MEANS (K=4)</span>
        <span>DIM-REDUCE: PCA</span>
        <span><span class="blink">▮</span> LIVE</span>
    </div>
    """, unsafe_allow_html=True)


# ================ FOOTER ================
st.markdown("""
<div class="footer">
    CLUSTER//OPS · UNSUPERVISED ML · K-MEANS CLUSTERING · PCA DIMENSIONALITY REDUCTION · 167 NATIONS ANALYZED<br>
    <span class="blink">▮</span> ALL SYSTEMS NOMINAL · BUILT WITH PYTHON · STREAMLIT · PLOTLY
</div>
""", unsafe_allow_html=True)
