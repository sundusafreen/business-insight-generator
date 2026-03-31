"""
InsightIQ — AI Business Analyst
Premium SaaS UI · Groq + Llama 3.3
"""

import os, io, re, warnings
import pandas as pd
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

warnings.filterwarnings("ignore")
load_dotenv()

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="InsightIQ · AI Business Analyst",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── PREMIUM CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --bg:         #0B0F19;
  --surface:    #111827;
  --surface2:   #1a2236;
  --border:     #1f2d45;
  --accent:     #3b82f6;
  --accent2:    #6366f1;
  --success:    #10b981;
  --warning:    #f59e0b;
  --danger:     #ef4444;
  --text:       #f1f5f9;
  --muted:      #64748b;
  --muted2:     #94a3b8;
  --radius:     14px;
  --radius-sm:  8px;
  --shadow:     0 4px 24px rgba(0,0,0,.4);
  --glow:       0 0 24px rgba(59,130,246,.18);
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"], .stApp {
  font-family: 'Inter', sans-serif !important;
  background: var(--bg) !important;
  color: var(--text) !important;
}

/* ── HIDE STREAMLIT CHROME ── */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"] { display: none !important; }

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
  background: var(--surface) !important;
  border-right: 1px solid var(--border) !important;
  padding: 0 !important;
}
section[data-testid="stSidebar"] > div { padding: 0 !important; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }

/* ── SELECTBOX ── */
.stSelectbox > div > div {
  background: var(--surface2) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-sm) !important;
  color: var(--text) !important;
  font-size: 13px !important;
}
.stSelectbox label {
  color: var(--muted) !important;
  font-size: 11px !important;
  letter-spacing: .06em !important;
  text-transform: uppercase !important;
  font-weight: 500 !important;
}

/* ── RADIO ── */
.stRadio label { color: var(--muted2) !important; font-size: 13px !important; }
.stRadio > label {
  color: var(--muted) !important;
  font-size: 11px !important;
  letter-spacing: .06em !important;
  text-transform: uppercase !important;
  font-weight: 500 !important;
}

/* ── CHECKBOX ── */
.stCheckbox label { color: var(--muted2) !important; font-size: 13px !important; }

/* ── BUTTONS ── */
.stButton > button {
  background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
  color: #fff !important;
  border: none !important;
  border-radius: var(--radius-sm) !important;
  font-family: 'Inter', sans-serif !important;
  font-size: 13px !important;
  font-weight: 600 !important;
  padding: 10px 20px !important;
  transition: all .2s ease !important;
  box-shadow: 0 2px 12px rgba(59,130,246,.25) !important;
  letter-spacing: .02em !important;
}
.stButton > button:hover {
  transform: translateY(-1px) !important;
  box-shadow: 0 6px 20px rgba(59,130,246,.4) !important;
  filter: brightness(1.08) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── FILE UPLOADER ── */
[data-testid="stFileUploader"] {
  background: var(--surface) !important;
  border: 2px dashed var(--border) !important;
  border-radius: var(--radius) !important;
  transition: border-color .2s !important;
}
[data-testid="stFileUploader"]:hover {
  border-color: var(--accent) !important;
}
[data-testid="stFileUploader"] label { color: var(--muted2) !important; }

/* ── METRICS ── */
div[data-testid="stMetric"] {
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  padding: 20px 24px !important;
  transition: all .2s ease !important;
  position: relative !important;
  overflow: hidden !important;
}
div[data-testid="stMetric"]::before {
  content: '';
  position: absolute;
  top: 0; left: 0;
  width: 3px; height: 100%;
  background: linear-gradient(180deg, var(--accent), var(--accent2));
  border-radius: 0 2px 2px 0;
}
div[data-testid="stMetric"]:hover {
  border-color: var(--accent) !important;
  box-shadow: var(--glow) !important;
  transform: translateY(-2px) !important;
}
div[data-testid="stMetricLabel"] {
  color: var(--muted) !important;
  font-size: 11px !important;
  letter-spacing: .08em !important;
  text-transform: uppercase !important;
  font-weight: 500 !important;
}
div[data-testid="stMetricValue"] {
  color: var(--text) !important;
  font-size: 28px !important;
  font-weight: 700 !important;
  font-family: 'Inter', sans-serif !important;
  letter-spacing: -.02em !important;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
  background: var(--surface) !important;
  border-radius: 50px !important;
  padding: 4px !important;
  border: 1px solid var(--border) !important;
  gap: 2px !important;
  display: inline-flex !important;
  margin-bottom: 24px !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  color: var(--muted) !important;
  border-radius: 50px !important;
  font-family: 'Inter', sans-serif !important;
  font-size: 13px !important;
  font-weight: 500 !important;
  padding: 8px 20px !important;
  border: none !important;
  transition: all .2s !important;
  white-space: nowrap !important;
}
.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
  color: #fff !important;
  box-shadow: 0 2px 12px rgba(59,130,246,.35) !important;
}
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }
.stTabs [data-baseweb="tab-border"]    { display: none !important; }

/* ── DATAFRAME ── */
.stDataFrame {
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  overflow: hidden !important;
}
.stDataFrame thead th {
  background: var(--surface2) !important;
  color: var(--muted2) !important;
  font-size: 11px !important;
  letter-spacing: .06em !important;
  text-transform: uppercase !important;
}

/* ── TEXT INPUT ── */
.stTextInput input, .stChatInput textarea,
[data-testid="stChatInputTextArea"] {
  background: var(--surface2) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-sm) !important;
  color: var(--text) !important;
  font-family: 'Inter', sans-serif !important;
  font-size: 14px !important;
}
.stChatInput, [data-testid="stChatInput"] {
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
}

/* ── SUCCESS / INFO / WARNING ── */
.stSuccess {
  background: rgba(16,185,129,.1) !important;
  border: 1px solid rgba(16,185,129,.3) !important;
  border-radius: var(--radius-sm) !important;
  color: #6ee7b7 !important;
}
.stInfo {
  background: rgba(59,130,246,.08) !important;
  border: 1px solid rgba(59,130,246,.2) !important;
  border-radius: var(--radius-sm) !important;
}
.stWarning {
  background: rgba(245,158,11,.08) !important;
  border: 1px solid rgba(245,158,11,.25) !important;
  border-radius: var(--radius-sm) !important;
}

/* ── SPINNER ── */
.stSpinner > div { border-top-color: var(--accent) !important; }

/* ── EXPANDER ── */
.streamlit-expanderHeader {
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-sm) !important;
  color: var(--muted2) !important;
  font-size: 13px !important;
}

/* ── CUSTOM COMPONENTS ── */
.iq-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 24px;
  margin-bottom: 16px;
  transition: all .2s ease;
}
.iq-card:hover {
  border-color: var(--accent);
  box-shadow: var(--glow);
}

.iq-section-title {
  font-size: 13px;
  font-weight: 600;
  letter-spacing: .08em;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 14px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--border);
}

.iq-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: rgba(16,185,129,.12);
  border: 1px solid rgba(16,185,129,.3);
  color: #6ee7b7;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: .06em;
  text-transform: uppercase;
  padding: 4px 10px;
  border-radius: 50px;
}

.iq-badge-premium {
  background: linear-gradient(135deg,rgba(245,158,11,.15),rgba(239,68,68,.15));
  border: 1px solid rgba(245,158,11,.35);
  color: #fcd34d;
}

.iq-chat-user {
  display: flex;
  justify-content: flex-end;
  margin: 10px 0;
}
.iq-chat-user-bubble {
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  color: #fff;
  padding: 12px 18px;
  border-radius: 18px 18px 4px 18px;
  max-width: 72%;
  font-size: 14px;
  line-height: 1.6;
  box-shadow: 0 4px 16px rgba(59,130,246,.25);
}

.iq-chat-ai {
  display: flex;
  justify-content: flex-start;
  margin: 10px 0;
  gap: 10px;
  align-items: flex-start;
}
.iq-chat-ai-avatar {
  width: 32px; height: 32px;
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 13px; font-weight: 700; color: #fff;
  flex-shrink: 0; margin-top: 2px;
}
.iq-chat-ai-bubble {
  background: var(--surface2);
  border: 1px solid var(--border);
  color: var(--muted2);
  padding: 14px 18px;
  border-radius: 4px 18px 18px 18px;
  max-width: 76%;
  font-size: 14px;
  line-height: 1.75;
}

.iq-suggestion-pill {
  display: inline-block;
  background: var(--surface2);
  border: 1px solid var(--border);
  color: var(--muted2);
  padding: 7px 14px;
  border-radius: 50px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all .15s;
  margin: 3px;
}
.iq-suggestion-pill:hover {
  border-color: var(--accent);
  color: var(--text);
  background: rgba(59,130,246,.08);
}

.iq-divider {
  height: 1px;
  background: var(--border);
  margin: 20px 0;
}

.iq-stat-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid var(--border);
  font-size: 13px;
}
.iq-stat-row:last-child { border-bottom: none; }
.iq-stat-key { color: var(--muted); }
.iq-stat-val { color: var(--text); font-weight: 600; font-family: 'JetBrains Mono', monospace; font-size: 12px; }

.iq-empty {
  text-align: center;
  padding: 80px 40px;
  color: var(--muted);
}
.iq-empty-icon { font-size: 40px; margin-bottom: 16px; opacity: .4; }
.iq-empty-title { font-size: 18px; font-weight: 600; color: var(--muted2); margin-bottom: 8px; }
.iq-empty-sub   { font-size: 14px; color: var(--muted); }

.iq-locked {
  position: relative;
  filter: blur(3px);
  pointer-events: none;
  user-select: none;
}
.iq-lock-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(11,15,25,.6);
  backdrop-filter: blur(2px);
  border-radius: var(--radius);
  z-index: 10;
}

/* Hero upload area */
.iq-upload-hero {
  border: 2px dashed var(--border);
  border-radius: var(--radius);
  padding: 40px 32px;
  text-align: center;
  transition: all .2s;
  background: var(--surface);
}
.iq-upload-hero:hover { border-color: var(--accent); box-shadow: var(--glow); }
.iq-upload-icon { font-size: 36px; margin-bottom: 12px; opacity: .5; }
.iq-upload-title { font-size: 16px; font-weight: 600; color: var(--text); margin-bottom: 6px; }
.iq-upload-sub { font-size: 13px; color: var(--muted); }
</style>
""", unsafe_allow_html=True)

# ── CONSTANTS ─────────────────────────────────────────────────────────────────
SAMPLE_CSV = """Date,Product,Region,Sales,Units,Returns,Marketing_Spend,Customer_Satisfaction
2024-01,Widget A,North,45200,312,14,8500,4.2
2024-01,Widget B,North,28900,198,8,4200,3.8
2024-01,Widget A,South,38700,267,21,7100,4.0
2024-01,Widget B,South,19400,133,5,3300,3.7
2024-02,Widget A,North,52100,359,11,9200,4.3
2024-02,Widget B,North,31200,214,9,4800,3.9
2024-02,Widget A,South,41800,288,18,7600,4.1
2024-02,Widget B,South,22700,156,6,3900,3.8
2024-03,Widget A,North,61400,423,16,10100,4.4
2024-03,Widget B,North,37500,258,12,5500,4.0
2024-03,Widget A,South,49200,339,23,8700,4.2
2024-03,Widget B,South,26800,184,7,4400,3.9"""

INDUSTRY_PROMPTS = {
    "General":   "Focus on revenue trends, performance gaps, and growth drivers.",
    "Ecommerce": "Focus on AOV, conversion rates, cart abandonment, and seasonal trends.",
    "SaaS":      "Focus on MRR, churn rate, CAC, LTV, and expansion revenue.",
    "Retail":    "Focus on sell-through rate, inventory turnover, basket size, and margin.",
    "Marketing": "Focus on ROAS, CPL, CTR, funnel conversion, and campaign ROI.",
}

# ── SESSION STATE ─────────────────────────────────────────────────────────────
for k, v in [("messages", []), ("report_cache", None), ("df", None), ("pending_input", None)]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── GROQ CLIENT ───────────────────────────────────────────────────────────────
@st.cache_resource
def get_client():
    key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", "")
    return Groq(api_key=key) if key else None

client = get_client()

# ── HELPERS ───────────────────────────────────────────────────────────────────
def load_data(f):
    return pd.read_csv(f) if f.name.endswith(".csv") else pd.read_excel(f)

def clean_text(t):
    return re.sub(r'[^\x00-\x7F]+', '', t).strip()

def get_data_context(df, n=8):
    num = df.select_dtypes(include='number')
    return f"""DATASET: {df.shape[0]} rows x {df.shape[1]} cols
Columns: {list(df.columns)}
Missing: {df.isnull().sum().to_dict()}
Stats:\n{num.describe().round(2).to_string() if not num.empty else 'N/A'}
Sample:\n{df.head(n).to_csv(index=False)}"""

def call_ai(system, user):
    if not client:
        return "⚠️ No API key. Add GROQ_API_KEY to your secrets."
    try:
        r = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=1500,
            messages=[{"role":"system","content":system},
                      {"role":"user",  "content":user}]
        )
        return r.choices[0].message.content
    except Exception as e:
        return f"⚠️ API error: {e}"

def generate_kpis(df):
    missing = int(df.isnull().sum().sum())
    return {
        "rows":     df.shape[0],
        "cols":     df.shape[1],
        "missing":  missing,
        "complete": f"{100 - missing/df.size*100:.1f}%",
        "num_cols": len(df.select_dtypes(include='number').columns),
    }

def generate_pdf(report):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, rightMargin=20*mm, leftMargin=20*mm,
                            topMargin=20*mm, bottomMargin=20*mm)
    S   = getSampleStyleSheet()
    s_t = ParagraphStyle('T',  parent=S['Title'],   fontSize=20, spaceAfter=12)
    s_h1= ParagraphStyle('H1', parent=S['Heading1'],fontSize=15, spaceAfter=8,  spaceBefore=14)
    s_h2= ParagraphStyle('H2', parent=S['Heading2'],fontSize=12, spaceAfter=6,  spaceBefore=10)
    s_b = ParagraphStyle('B',  parent=S['Normal'],  fontSize=10, spaceAfter=4,  leading=14)
    s_bl= ParagraphStyle('BL', parent=S['Normal'],  fontSize=10, leftIndent=14, spaceAfter=3, leading=14)
    story = [Paragraph("InsightIQ — Business Analysis Report", s_t), Spacer(1, 5*mm)]
    for line in report.split("\n"):
        line = clean_text(line.strip())
        if not line:                      story.append(Spacer(1, 3*mm))
        elif line.startswith("## "):      story.append(Paragraph(line[3:], s_h1))
        elif line.startswith("### "):     story.append(Paragraph(line[4:], s_h2))
        elif line.startswith(("- ","* ")): story.append(Paragraph("• "+line[2:], s_bl))
        else:                             story.append(Paragraph(line, s_b))
    doc.build(story); buf.seek(0)
    return buf

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo
    st.markdown("""
    <div style="padding:28px 24px 20px">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px">
            <div style="width:34px;height:34px;background:linear-gradient(135deg,#3b82f6,#6366f1);
                border-radius:10px;display:flex;align-items:center;justify-content:center;
                font-size:16px;font-weight:800;color:#fff;letter-spacing:-.02em">IQ</div>
            <div>
                <div style="font-size:16px;font-weight:700;color:#f1f5f9;letter-spacing:-.01em">InsightIQ</div>
                <div style="font-size:10px;color:#475569;letter-spacing:.1em;text-transform:uppercase">AI ANALYST</div>
            </div>
        </div>
    </div>
    <div style="height:1px;background:#1f2d45;margin:0 20px 20px"></div>
    """, unsafe_allow_html=True)

    # Controls
    with st.container():
        st.markdown('<div style="padding:0 16px">', unsafe_allow_html=True)
        industry    = st.selectbox("Industry", ["General","Ecommerce","SaaS","Retail","Marketing"])
        report_type = st.selectbox("Report Type", ["Executive Summary","Sales Performance",
                                                    "Trend Analysis","Strategic Recommendations","Risk Analysis"])
        export_fmt  = st.radio("Export Format", ["Markdown (.md)","Word (.docx)","PDF (.pdf)"])
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:1px;background:#1f2d45;margin:16px 20px"></div>', unsafe_allow_html=True)

    # Premium toggle
    with st.container():
        st.markdown('<div style="padding:0 16px">', unsafe_allow_html=True)
        is_premium = st.checkbox("⚡ Premium Mode")
        if is_premium:
            st.markdown('<div style="margin-top:8px"><span class="iq-badge iq-badge-premium">✦ Premium Active</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div style="position:fixed;bottom:0;left:0;width:260px;padding:16px 24px;
        border-top:1px solid #1f2d45;background:#111827">
        <div style="font-size:11px;color:#374151;line-height:1.6">
            Powered by <span style="color:#3b82f6;font-weight:600">Groq</span> ·
            Llama 3.3 70B<br>
            <span style="color:#1f2937">© 2024 InsightIQ</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

df = st.session_state.df

# ── MAIN AREA ─────────────────────────────────────────────────────────────────
main = st.container()
with main:

    if df is None:
        # ── HERO / UPLOAD STATE ───────────────────────────────────────────────
        st.markdown("""
        <div style="max-width:640px;margin:60px auto 40px;text-align:center;padding:0 24px">
            <div style="display:inline-flex;align-items:center;gap:8px;
                background:rgba(59,130,246,.1);border:1px solid rgba(59,130,246,.25);
                border-radius:50px;padding:6px 16px;margin-bottom:24px">
                <span style="color:#3b82f6;font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase">
                    ✦ AI-Powered Business Intelligence
                </span>
            </div>
            <h1 style="font-size:48px;font-weight:800;color:#f1f5f9;line-height:1.1;
                letter-spacing:-.03em;margin-bottom:16px">
                AI Business<br><span style="background:linear-gradient(135deg,#3b82f6,#6366f1);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent">Analyst</span>
            </h1>
            <p style="font-size:17px;color:#64748b;line-height:1.6;margin-bottom:36px">
                Upload your data. Ask anything.<br>Get boardroom-ready insights in seconds.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Centered upload
        col_l, col_c, col_r = st.columns([1, 2, 1])
        with col_c:
            uploaded_files = st.file_uploader(
                "↑ Drag & drop your CSV or Excel file here",
                type=["csv","xlsx","xls"],
                accept_multiple_files=True,
                label_visibility="visible"
            )
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            if st.button("✦ Load Sample Dataset", use_container_width=True):
                st.session_state.df = pd.read_csv(io.StringIO(SAMPLE_CSV))
                st.session_state.messages = []
                st.session_state.report_cache = None
                st.rerun()

        if uploaded_files:
            selected = uploaded_files[0]
            if len(uploaded_files) > 1:
                chosen   = st.selectbox("Select file", [f.name for f in uploaded_files])
                selected = next(f for f in uploaded_files if f.name == chosen)
            try:
                st.session_state.df = load_data(selected)
                st.session_state.messages = []
                st.session_state.report_cache = None
                st.rerun()
            except Exception as e:
                st.error(f"Could not read file: {e}")

        # Feature pills
        st.markdown("""
        <div style="max-width:640px;margin:32px auto 0;text-align:center">
            <div style="display:flex;flex-wrap:wrap;justify-content:center;gap:8px">
                <span class="iq-suggestion-pill">📊 Auto KPI Dashboard</span>
                <span class="iq-suggestion-pill">📈 Smart Visualizations</span>
                <span class="iq-suggestion-pill">🤖 AI Chat Assistant</span>
                <span class="iq-suggestion-pill">📋 Report Generation</span>
                <span class="iq-suggestion-pill">⬇️ Multi-format Export</span>
                <span class="iq-suggestion-pill">🏭 Industry Modes</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    else:
        # ── DATA LOADED — FULL DASHBOARD ──────────────────────────────────────

        # Top bar
        kpis = generate_kpis(df)
        top_l, top_r = st.columns([3, 1])
        with top_l:
            st.markdown(f"""
            <div style="padding:20px 0 16px">
                <div style="font-size:22px;font-weight:700;color:#f1f5f9;letter-spacing:-.02em">
                    Dashboard
                </div>
                <div style="font-size:13px;color:#64748b;margin-top:3px">
                    {df.shape[0]:,} rows · {df.shape[1]} columns · {industry} mode
                </div>
            </div>
            """, unsafe_allow_html=True)
        with top_r:
            if st.button("↑ New Dataset", use_container_width=True):
                st.session_state.df = None
                st.session_state.messages = []
                st.session_state.report_cache = None
                st.rerun()

        # KPI row
        c1,c2,c3,c4,c5 = st.columns(5)
        c1.metric("Total Rows",      f"{kpis['rows']:,}")
        c2.metric("Columns",         kpis['cols'])
        c3.metric("Missing Values",  kpis['missing'])
        c4.metric("Completeness",    kpis['complete'])
        c5.metric("Numeric Cols",    kpis['num_cols'])

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        # ── TABS ──────────────────────────────────────────────────────────────
        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            ["  📊  Overview  ","  📈  Visualize  ","  🤖  AI Chat  ",
             "  📋  Reports  ","  ⬇️  Export  "])

        # ══ TAB 1: OVERVIEW ══════════════════════════════════════════════════
        with tab1:
            st.markdown('<div class="iq-section-title">Data Preview</div>', unsafe_allow_html=True)
            st.dataframe(df.head(5), use_container_width=True)

            ca, cb = st.columns(2)
            with ca:
                st.markdown('<div class="iq-section-title" style="margin-top:20px">Column Schema</div>', unsafe_allow_html=True)
                schema = pd.DataFrame({
                    "Column":   df.columns,
                    "Type":     df.dtypes.astype(str).values,
                    "Non-Null": df.count().values,
                    "Missing":  df.isnull().sum().values,
                })
                st.dataframe(schema, use_container_width=True, hide_index=True)
            with cb:
                st.markdown('<div class="iq-section-title" style="margin-top:20px">Numeric Summary</div>', unsafe_allow_html=True)
                num = df.select_dtypes(include='number')
                if not num.empty:
                    st.dataframe(num.describe().round(2), use_container_width=True)
                else:
                    st.info("No numeric columns found.")

        # ══ TAB 2: VISUALIZE ═════════════════════════════════════════════════
        with tab2:
            num_cols = df.select_dtypes(include='number').columns.tolist()
            cat_cols = [c for c in df.columns if df[c].nunique() < 25 and df[c].dtype == object]
            date_col = next((c for c in df.columns if 'date' in c.lower()), None)

            if not num_cols:
                st.warning("No numeric columns detected for visualization.")
            else:
                v1, v2, v3 = st.tabs(["  Bar Chart  ","  Line Chart  ","  Correlation  "])

                with v1:
                    r1, r2 = st.columns(2)
                    y  = r1.selectbox("Metric (Y)", num_cols, key="by")
                    x  = r2.selectbox("Group by",  cat_cols if cat_cols else num_cols, key="bx")
                    st.bar_chart(df.groupby(x)[y].sum().reset_index().set_index(x), use_container_width=True)

                with v2:
                    r1, r2 = st.columns(2)
                    ly = r1.selectbox("Metric",  num_cols, key="ly")
                    lx = r2.selectbox("X axis", ([date_col]+num_cols) if date_col else num_cols, key="lx")
                    try:    st.line_chart(df.set_index(lx)[ly], use_container_width=True)
                    except: st.line_chart(df[ly], use_container_width=True)

                with v3:
                    corr = df[num_cols].corr().round(2)
                    try:
                        st.dataframe(
                            corr.style.background_gradient(cmap="RdYlGn", axis=None).format("{:.2f}"),
                            use_container_width=True)
                    except Exception:
                        st.dataframe(corr, use_container_width=True)
                    st.caption("Green = strong positive · Red = strong negative")

        # ══ TAB 3: AI CHAT ═══════════════════════════════════════════════════
        with tab3:
            st.markdown('<div class="iq-section-title">AI Chat Assistant</div>', unsafe_allow_html=True)

            # Suggestion pills
            st.markdown("<div style='margin-bottom:16px'>", unsafe_allow_html=True)
            sug_cols = st.columns(4)
            suggestions = [
                "What are the top trends?",
                "Which segment performs best?",
                "What risks should I know?",
                "Give 3 recommendations.",
            ]
            for i, s in enumerate(suggestions):
                if sug_cols[i].button(s, key=f"sug{i}", use_container_width=True):
                    st.session_state["pending_input"] = s
            st.markdown("</div>", unsafe_allow_html=True)

            # Process pending input (from suggestions OR chat input)
            user_input = st.chat_input("Ask anything about your data…")
            if user_input:
                st.session_state["pending_input"] = user_input

            if st.session_state.get("pending_input"):
                inp = st.session_state.pop("pending_input")
                st.session_state.messages.append({"role":"user","content":inp})

                history = "\n".join([
                    f"{m['role'].upper()}: {m['content']}"
                    for m in st.session_state.messages[-8:]
                ])
                sys_p = f"""You are InsightIQ, an elite AI business analyst built into a SaaS platform.
Industry: {industry}. {INDUSTRY_PROMPTS[industry]}
Answer with precision. Use bullet points. Cite specific numbers from the data.
Be concise but thorough. Format clearly."""
                usr_p = f"Dataset:\n{get_data_context(df)}\n\nConversation:\n{history}\n\nQuestion: {inp}"

                with st.spinner("Analysing your data…"):
                    reply = call_ai(sys_p, usr_p)
                st.session_state.messages.append({"role":"assistant","content":reply})

            # Render chat history
            if not st.session_state.messages:
                st.markdown("""
                <div class="iq-empty" style="padding:40px 20px">
                    <div class="iq-empty-icon">🤖</div>
                    <div class="iq-empty-title">Ask anything about your data</div>
                    <div class="iq-empty-sub">Use the suggestions above or type your question below</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                for m in st.session_state.messages:
                    if m["role"] == "user":
                        st.markdown(f"""
                        <div class="iq-chat-user">
                            <div class="iq-chat-user-bubble">{m['content']}</div>
                        </div>""", unsafe_allow_html=True)
                    else:
                        content = m['content'].replace('\n', '<br>')
                        st.markdown(f"""
                        <div class="iq-chat-ai">
                            <div class="iq-chat-ai-avatar">IQ</div>
                            <div class="iq-chat-ai-bubble">{content}</div>
                        </div>""", unsafe_allow_html=True)

                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                if st.button("Clear conversation", key="clear_chat"):
                    st.session_state.messages = []
                    st.rerun()

        # ══ TAB 4: REPORTS ═══════════════════════════════════════════════════
        with tab4:
            st.markdown('<div class="iq-section-title">Report Generator</div>', unsafe_allow_html=True)

            focus = st.text_input("Custom focus (optional)",
                                   placeholder="e.g. Focus on Q1 vs Q2 regional performance gap")

            btn1, btn2 = st.columns(2)
            with btn1:
                if st.button("⚡ Generate Report", type="primary", use_container_width=True):
                    sys_p = f"""You are an elite business intelligence analyst writing a {report_type}.
Industry: {industry}. {INDUSTRY_PROMPTS[industry]}
Structure the report exactly as:
## {report_type}
### Data Overview
### Key Findings
### Trend Analysis
### Risk Signals
### Strategic Recommendations
### Executive Takeaway
Use real numbers. No filler sentences."""
                    with st.spinner("Generating your report…"):
                        st.session_state.report_cache = call_ai(
                            sys_p,
                            get_data_context(df) + (f"\nFocus: {focus}" if focus else "")
                        )

            with btn2:
                if is_premium:
                    if st.button("🎯 Deep Recommendations", use_container_width=True):
                        sys_p = f"""You are a McKinsey-level business consultant.
Industry: {industry}. {INDUSTRY_PROMPTS[industry]}
Deliver 5 prioritized, specific recommendations.
Each must include: Problem identified, Recommended action, Expected impact, Timeline.
Use bold headers for each recommendation."""
                        with st.spinner("Generating deep recommendations…"):
                            st.session_state.report_cache = call_ai(sys_p, get_data_context(df))
                else:
                    st.markdown("""
                    <div style="border:1px dashed #1f2d45;border-radius:14px;padding:16px;
                        text-align:center;color:#374151;font-size:13px">
                        🎯 Deep Recommendations
                        <span style="background:linear-gradient(90deg,#f59e0b,#ef4444);
                            color:#fff;font-size:9px;font-weight:700;padding:2px 8px;
                            border-radius:50px;margin-left:6px;letter-spacing:.06em">
                            PREMIUM
                        </span>
                        <br><small style="color:#1f2937;margin-top:6px;display:block">
                            Enable Premium Mode in sidebar
                        </small>
                    </div>""", unsafe_allow_html=True)

            if st.session_state.report_cache:
                st.markdown('<div class="iq-divider"></div>', unsafe_allow_html=True)
                st.markdown(
                    f'<div class="iq-card" style="line-height:1.8;color:#94a3b8;font-size:14px">'
                    + st.session_state.report_cache.replace('\n', '<br>')
                    + '</div>',
                    unsafe_allow_html=True
                )

        # ══ TAB 5: EXPORT ════════════════════════════════════════════════════
        with tab5:
            st.markdown('<div class="iq-section-title">Export</div>', unsafe_allow_html=True)

            if not st.session_state.report_cache:
                st.markdown("""
                <div class="iq-empty">
                    <div class="iq-empty-icon">📄</div>
                    <div class="iq-empty-title">No report generated yet</div>
                    <div class="iq-empty-sub">Go to the Reports tab and generate a report first</div>
                </div>""", unsafe_allow_html=True)
            else:
                report = st.session_state.report_cache

                with st.expander("Preview report content"):
                    st.text(report[:600] + "…" if len(report) > 600 else report)

                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

                if export_fmt == "Markdown (.md)":
                    st.download_button("⬇️ Download as Markdown", data=report,
                        file_name="insightiq_report.md", mime="text/markdown",
                        use_container_width=True)

                elif export_fmt == "Word (.docx)":
                    try:
                        from docx import Document
                        doc = Document()
                        doc.add_heading("InsightIQ — Business Analysis Report", 0)
                        for line in report.split("\n"):
                            line = line.strip()
                            if not line: continue
                            if line.startswith("## "):        doc.add_heading(line[3:], 1)
                            elif line.startswith("### "):     doc.add_heading(line[4:], 2)
                            elif line.startswith(("- ","* ")): doc.add_paragraph(line[2:], style="List Bullet")
                            else:                             doc.add_paragraph(line)
                        buf = io.BytesIO(); doc.save(buf); buf.seek(0)
                        st.download_button("⬇️ Download as Word", data=buf,
                            file_name="insightiq_report.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            use_container_width=True)
                    except ImportError:
                        st.error("pip install python-docx")

                elif export_fmt == "PDF (.pdf)":
                    try:
                        st.download_button("⬇️ Download as PDF", data=generate_pdf(report),
                            file_name="insightiq_report.pdf", mime="application/pdf",
                            use_container_width=True)
                    except ImportError:
                        st.error("pip install reportlab")

                st.markdown('<div class="iq-divider"></div>', unsafe_allow_html=True)
                st.download_button("⬇️ Download Dataset as CSV",
                    data=df.to_csv(index=False).encode("utf-8"),
                    file_name="dataset_export.csv", mime="text/csv",
                    use_container_width=True)