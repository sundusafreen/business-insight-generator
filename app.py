"""
InsightIQ — AI Business Decision Engine
Features: Sentiment Analysis · Charts-in-Report · AI Chat · Multi-format Export
"""

import os, io, re, json, warnings
import pandas as pd
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

warnings.filterwarnings("ignore")
load_dotenv()

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="InsightIQ · AI Business Analyst",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --bg:#070B14; --bg2:#0B0F1A; --surface:#0F1624; --surface2:#151D2E;
  --surface3:#1A2338; --border:#1E2D45; --border2:#243550;
  --accent:#3B82F6; --accent2:#6366F1; --accent3:#8B5CF6;
  --success:#10B981; --warning:#F59E0B; --danger:#EF4444;
  --text:#F1F5F9; --text2:#CBD5E1; --muted:#64748B; --muted2:#475569;
  --r:16px; --r-sm:10px; --r-xs:6px;
  --shadow-lg:0 20px 60px rgba(0,0,0,.6);
  --shadow-md:0 8px 32px rgba(0,0,0,.4);
  --shadow-sm:0 4px 16px rgba(0,0,0,.3);
  --glow-blue:0 0 40px rgba(59,130,246,.15);
  --glow-green:0 0 30px rgba(16,185,129,.15);
  --grad:linear-gradient(135deg,#3B82F6,#6366F1,#8B5CF6);
  --grad-soft:linear-gradient(135deg,rgba(59,130,246,.1),rgba(99,102,241,.1));
}
*,*::before,*::after{box-sizing:border-box;}
html,body,[class*="css"],.stApp{
  font-family:'Inter',-apple-system,sans-serif!important;
  background:var(--bg)!important; color:var(--text)!important;
  -webkit-font-smoothing:antialiased;
}
#MainMenu,footer,header,[data-testid="stToolbar"],
[data-testid="stDecoration"],[data-testid="stStatusWidget"]{display:none!important;}
::-webkit-scrollbar{width:3px;height:3px;}
::-webkit-scrollbar-track{background:transparent;}
::-webkit-scrollbar-thumb{background:var(--border2);border-radius:3px;}

@keyframes fadeUp{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}
@keyframes shimmer{0%{background-position:-200% center}100%{background-position:200% center}}
.fade-up{animation:fadeUp .45s ease forwards;}
.fade-in{animation:fadeIn .35s ease forwards;}

/* SIDEBAR */
section[data-testid="stSidebar"]{
  background:var(--surface)!important;
  border-right:1px solid var(--border)!important;
  width:264px!important;
}
section[data-testid="stSidebar"]>div{padding:0!important;}

/* SELECTBOX */
.stSelectbox>div>div{
  background:var(--surface2)!important;border:1px solid var(--border)!important;
  border-radius:var(--r-sm)!important;color:var(--text2)!important;font-size:13px!important;
  transition:border-color .2s!important;
}
.stSelectbox>div>div:hover{border-color:var(--accent)!important;}
.stSelectbox label,.stRadio>label,.stCheckbox>label{
  color:var(--muted)!important;font-size:10px!important;font-weight:600!important;
  letter-spacing:.1em!important;text-transform:uppercase!important;
}

/* RADIO / CHECKBOX */
.stRadio [data-testid="stMarkdownContainer"] p,
.stCheckbox label p{color:var(--text2)!important;font-size:13px!important;}

/* BUTTONS */
.stButton>button{
  background:var(--grad)!important;color:#fff!important;border:none!important;
  border-radius:var(--r-sm)!important;font-family:'Inter',sans-serif!important;
  font-size:13px!important;font-weight:600!important;padding:11px 22px!important;
  transition:all .2s cubic-bezier(.4,0,.2,1)!important;
  box-shadow:0 4px 15px rgba(59,130,246,.3)!important;
}
.stButton>button:hover{
  transform:translateY(-2px)!important;
  box-shadow:0 8px 25px rgba(59,130,246,.45)!important;filter:brightness(1.1)!important;
}
.stButton>button:active{transform:translateY(0)!important;}

/* TEXT INPUT */
.stTextInput input{
  background:var(--surface2)!important;border:1px solid var(--border)!important;
  border-radius:var(--r-sm)!important;color:var(--text)!important;
  font-family:'Inter',sans-serif!important;font-size:14px!important;
  padding:10px 14px!important;transition:border-color .2s!important;
}
.stTextInput input:focus{border-color:var(--accent)!important;box-shadow:var(--glow-blue)!important;}
.stTextInput label{
  color:var(--muted)!important;font-size:10px!important;font-weight:600!important;
  letter-spacing:.1em!important;text-transform:uppercase!important;
}

/* METRICS */
div[data-testid="stMetric"]{
  background:var(--surface)!important;border:1px solid var(--border)!important;
  border-radius:var(--r)!important;padding:20px 22px!important;
  position:relative!important;overflow:hidden!important;
  transition:all .25s cubic-bezier(.4,0,.2,1)!important;
}
div[data-testid="stMetric"]::after{
  content:'';position:absolute;top:0;left:0;width:2px;height:100%;background:var(--grad);
}
div[data-testid="stMetric"]:hover{
  border-color:var(--accent)!important;transform:translateY(-3px)!important;
  box-shadow:var(--glow-blue)!important;
}
div[data-testid="stMetricLabel"] p{
  color:var(--muted)!important;font-size:10px!important;font-weight:600!important;
  letter-spacing:.1em!important;text-transform:uppercase!important;
}
div[data-testid="stMetricValue"]{
  color:var(--text)!important;font-size:28px!important;font-weight:800!important;
  letter-spacing:-.03em!important;
}

/* TABS */
.stTabs [data-baseweb="tab-list"]{
  background:var(--surface)!important;border-radius:50px!important;
  padding:4px 5px!important;border:1px solid var(--border)!important;
  display:inline-flex!important;gap:2px!important;margin-bottom:24px!important;
  box-shadow:var(--shadow-sm)!important;
}
.stTabs [data-baseweb="tab"]{
  background:transparent!important;color:var(--muted)!important;border-radius:50px!important;
  font-size:12px!important;font-weight:600!important;padding:8px 16px!important;
  border:none!important;transition:all .2s ease!important;white-space:nowrap!important;
}
.stTabs [data-baseweb="tab"]:hover{color:var(--text2)!important;}
.stTabs [aria-selected="true"]{
  background:var(--grad)!important;color:#fff!important;
  box-shadow:0 4px 15px rgba(59,130,246,.4)!important;
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"]{display:none!important;}

/* DATAFRAME */
.stDataFrame{border:1px solid var(--border)!important;border-radius:var(--r)!important;overflow:hidden!important;}

/* ALERTS */
.stSuccess{background:rgba(16,185,129,.08)!important;border:1px solid rgba(16,185,129,.25)!important;border-radius:var(--r-sm)!important;}
.stInfo{background:rgba(59,130,246,.06)!important;border:1px solid rgba(59,130,246,.2)!important;border-radius:var(--r-sm)!important;}
.stWarning{background:rgba(245,158,11,.06)!important;border:1px solid rgba(245,158,11,.2)!important;border-radius:var(--r-sm)!important;}
.stError{background:rgba(239,68,68,.08)!important;border:1px solid rgba(239,68,68,.2)!important;border-radius:var(--r-sm)!important;}
.stSpinner>div{border-top-color:var(--accent)!important;}

/* ── CUSTOM COMPONENTS ── */
.iq-section{
  font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;
  color:var(--muted);margin:20px 0 14px;padding-bottom:10px;
  border-bottom:1px solid var(--border);
}
.iq-card{
  background:var(--surface);border:1px solid var(--border);border-radius:var(--r);
  padding:22px;transition:all .25s cubic-bezier(.4,0,.2,1);
}
.iq-card:hover{border-color:var(--border2);box-shadow:var(--shadow-md);transform:translateY(-1px);}
.iq-card-glow{border-color:rgba(59,130,246,.2);background:linear-gradient(135deg,var(--surface),rgba(59,130,246,.04));}

.iq-badge{display:inline-flex;align-items:center;gap:4px;font-size:10px;font-weight:700;
  letter-spacing:.08em;text-transform:uppercase;padding:4px 10px;border-radius:50px;}
.iq-badge-blue{background:rgba(59,130,246,.12);border:1px solid rgba(59,130,246,.3);color:#93C5FD;}
.iq-badge-green{background:rgba(16,185,129,.1);border:1px solid rgba(16,185,129,.28);color:#6EE7B7;}
.iq-badge-red{background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.28);color:#FCA5A5;}
.iq-badge-gold{background:linear-gradient(135deg,rgba(245,158,11,.15),rgba(239,68,68,.1));border:1px solid rgba(245,158,11,.3);color:#FCD34D;}
.iq-badge-purple{background:rgba(139,92,246,.12);border:1px solid rgba(139,92,246,.3);color:#C4B5FD;}

.iq-div{height:1px;background:var(--border);margin:20px 0;}

/* CHAT BUBBLES */
.iq-msg-user{display:flex;justify-content:flex-end;margin:10px 0;animation:fadeUp .3s ease;}
.iq-bubble-user{
  background:var(--grad);color:#fff;padding:12px 18px;
  border-radius:18px 18px 4px 18px;max-width:70%;font-size:14px;line-height:1.65;
  box-shadow:0 4px 20px rgba(59,130,246,.3);
}
.iq-msg-ai{display:flex;align-items:flex-start;gap:10px;margin:10px 0;animation:fadeUp .3s ease;}
.iq-avatar{
  width:32px;height:32px;background:var(--grad);border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  font-size:11px;font-weight:800;color:#fff;flex-shrink:0;
  box-shadow:0 4px 12px rgba(59,130,246,.3);
}
.iq-bubble-ai{
  background:var(--surface2);border:1px solid var(--border2);color:var(--text2);
  padding:13px 18px;border-radius:4px 18px 18px 18px;max-width:76%;
  font-size:14px;line-height:1.75;box-shadow:var(--shadow-sm);
}

/* SENTIMENT BARS */
.sent-bar-wrap{background:var(--surface2);border-radius:50px;height:10px;overflow:hidden;margin:6px 0;}
.sent-bar{height:100%;border-radius:50px;transition:width .8s cubic-bezier(.4,0,.2,1);}

/* REPORT SECTION */
.report-section{
  background:var(--surface);border:1px solid var(--border);border-radius:var(--r);
  padding:22px 26px;margin-bottom:16px;
  transition:all .2s ease;
}
.report-section:hover{border-color:var(--border2);}
.report-section-title{
  font-size:13px;font-weight:700;color:var(--text);margin-bottom:12px;
  display:flex;align-items:center;gap:8px;
}
.report-section-body{font-size:13px;color:var(--text2);line-height:1.8;}

/* LOCKED */
.iq-locked-wrap{position:relative;}
.iq-lock-blur{filter:blur(4px);pointer-events:none;user-select:none;}
.iq-lock-overlay{
  position:absolute;inset:0;display:flex;flex-direction:column;
  align-items:center;justify-content:center;
  background:rgba(7,11,20,.75);backdrop-filter:blur(4px);
  border-radius:var(--r);border:1px solid var(--border2);z-index:5;gap:8px;
}

/* USE CASE CARDS */
.iq-usecase{
  background:var(--surface);border:1px solid var(--border);border-radius:var(--r);
  padding:18px 20px;transition:all .2s ease;
}
.iq-usecase:hover{border-color:var(--accent);box-shadow:var(--glow-blue);transform:translateY(-2px);}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────
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

SAMPLE_REVIEWS = """review_id,product,review_text,rating
1,Widget A,"Absolutely love this product! Works perfectly and great value.",5
2,Widget B,"Decent quality but took too long to arrive. Packaging was damaged.",3
3,Widget A,"Outstanding! Exceeded my expectations. Will definitely buy again.",5
4,Widget B,"Product broke after one week. Very disappointed with the quality.",1
5,Widget A,"Good product overall, minor issues with setup but support helped.",4
6,Widget B,"Not worth the price. Cheaper alternatives available elsewhere.",2
7,Widget A,"Fast delivery, excellent packaging, product works as described.",5
8,Widget B,"Average product. Does the job but nothing special about it.",3
9,Widget A,"Best purchase this year! Highly recommend to everyone.",5
10,Widget B,"Customer service was unhelpful when I had issues. Frustrating.",2"""

INDUSTRY_PROMPTS = {
    "General":   "Focus on revenue trends, performance gaps, and growth drivers.",
    "Ecommerce": "Focus on AOV, conversion rates, cart abandonment, and seasonal trends.",
    "SaaS":      "Focus on MRR, churn rate, CAC, LTV, and expansion revenue.",
    "Retail":    "Focus on sell-through rate, inventory turnover, basket size, and margin.",
    "Marketing": "Focus on ROAS, CPL, CTR, funnel conversion, and campaign ROI.",
}

USE_CASES = [
    ("📈","Sales Analysis","Revenue trends, top performers, growth opportunities"),
    ("💬","Review Sentiment","Analyze customer reviews and feedback automatically"),
    ("🎯","Customer Insights","Segments, behavior patterns, satisfaction drivers"),
    ("💰","Revenue Trends","MRR growth, churn impact, expansion revenue"),
    ("📊","Marketing ROI","Campaign performance, ROAS, and attribution"),
    ("🔮","Forecasting","Predict future trends and model scenarios"),
]

SECTION_ICONS = {
    "data overview":           "📊",
    "key findings":            "🔍",
    "trend analysis":          "📈",
    "risk signals":            "⚠️",
    "strategic recommendations":"✅",
    "executive takeaway":      "💡",
    "recommendations":         "✅",
    "sentiment overview":      "💬",
    "top issues":              "🔴",
    "positive highlights":     "🟢",
}

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
for k,v in [("messages",[]),("report_cache",None),("df",None),
            ("pending_input",None),("sentiment_cache",None),("last_sent","")]:
    if k not in st.session_state: st.session_state[k]=v

# ─────────────────────────────────────────────────────────────────────────────
# GROQ CLIENT
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_resource
def get_client():
    key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY","")
    return Groq(api_key=key) if key else None

client = get_client()

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def load_data(f):
    return pd.read_csv(f) if f.name.endswith(".csv") else pd.read_excel(f)

def clean_text(t):
    return re.sub(r'[^\x00-\x7F]+','',t).strip()

def get_data_context(df, n=8):
    num = df.select_dtypes(include='number')
    return f"""DATASET: {df.shape[0]} rows × {df.shape[1]} cols
Columns: {list(df.columns)}
Missing: {df.isnull().sum().to_dict()}
Stats:\n{num.describe().round(2).to_string() if not num.empty else 'N/A'}
Sample:\n{df.head(n).to_csv(index=False)}"""

def call_ai(system, user):
    if not client:
        return "⚠️ No API key. Add GROQ_API_KEY to secrets."
    try:
        r = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=1800,
            messages=[{"role":"system","content":system},
                      {"role":"user",  "content":user}]
        )
        return r.choices[0].message.content
    except Exception as e:
        return f"⚠️ API error: {str(e)}"

def generate_kpis(df):
    missing = int(df.isnull().sum().sum())
    return {
        "rows":    df.shape[0],
        "cols":    df.shape[1],
        "missing": missing,
        "complete":f"{100-missing/df.size*100:.1f}%",
        "num_cols":len(df.select_dtypes(include='number').columns),
    }

# ── SENTIMENT DETECTION ───────────────────────────────────────────────────────
def detect_text_columns(df):
    """Find columns that likely contain review/feedback text."""
    text_cols = []
    for col in df.columns:
        if df[col].dtype == object:
            sample = df[col].dropna().head(20)
            avg_len = sample.astype(str).str.len().mean()
            if avg_len > 30:  # Long strings = likely reviews
                text_cols.append(col)
    return text_cols

def detect_score_columns(df):
    """Find columns that likely contain numeric ratings/scores."""
    score_cols = []
    score_keywords = ['rating','score','review','sentiment','stars','grade','feedback','satisfaction']
    for col in df.columns:
        col_lower = col.lower()
        if any(k in col_lower for k in score_keywords):
            if df[col].dtype in ['float64','int64']:
                score_cols.append(col)
    return score_cols

def has_sentiment_data(df):
    """Return True if dataset has text reviews or score columns."""
    return bool(detect_text_columns(df) or detect_score_columns(df))

def run_sentiment_analysis(df):
    """
    Auto-detect and run sentiment analysis.
    Returns dict with results.
    """
    text_cols  = detect_text_columns(df)
    score_cols = detect_score_columns(df)
    results    = {"type": None, "text_col": None, "score_col": None,
                  "distribution": {}, "themes_pos": [], "themes_neg": [],
                  "recommendations": "", "sample_df": None}

    # ── Case 1: Raw text reviews ──
    if text_cols:
        col = text_cols[0]
        results["type"]     = "text"
        results["text_col"] = col

        reviews = df[col].dropna().astype(str).tolist()
        batch   = reviews[:40]  # Limit to 40 for API

        sys_p = """You are a sentiment analysis expert. Analyze the reviews and return ONLY valid JSON.
No explanation. No markdown. Return exactly this structure:
{
  "distribution": {"Positive": 0, "Neutral": 0, "Negative": 0},
  "themes_positive": ["theme1", "theme2", "theme3"],
  "themes_negative": ["theme1", "theme2", "theme3"],
  "summary": "One sentence summary of overall sentiment"
}"""
        usr_p = f"Analyze these {len(batch)} reviews:\n" + "\n".join(
            [f"{i+1}. {r[:200]}" for i,r in enumerate(batch)])

        raw = call_ai(sys_p, usr_p)
        try:
            # Strip any markdown fences
            clean = re.sub(r'```json|```','', raw).strip()
            data  = json.loads(clean)
            results["distribution"]  = data.get("distribution", {})
            results["themes_pos"]    = data.get("themes_positive", [])
            results["themes_neg"]    = data.get("themes_negative", [])
            results["summary"]       = data.get("summary", "")
        except Exception:
            results["distribution"] = {"Positive":0,"Neutral":0,"Negative":0}

        # Also label each review
        label_sys = """Label each review as Positive, Neutral, or Negative.
Return ONLY a JSON array of labels matching the input order.
Example: ["Positive","Negative","Neutral"]"""
        label_raw = call_ai(label_sys,
            f"Reviews:\n" + "\n".join([f"{i+1}. {r[:150]}" for i,r in enumerate(batch)]))
        try:
            clean_labels = re.sub(r'```json|```','', label_raw).strip()
            labels = json.loads(clean_labels)
            sample = df[col].dropna().head(40).reset_index(drop=True)
            results["sample_df"] = pd.DataFrame({
                "Review": sample,
                "Sentiment": labels[:len(sample)]
            })
        except Exception:
            pass

    # ── Case 2: Numeric scores ──
    elif score_cols:
        col = score_cols[0]
        results["type"]      = "scores"
        results["score_col"] = col
        scores = df[col].dropna()
        max_score = scores.max()
        # Normalize to 0-10 scale for bucketing
        if max_score <= 5:
            pos = (scores >= 4).sum()
            neu = ((scores >= 3) & (scores < 4)).sum()
            neg = (scores < 3).sum()
        else:
            pos = (scores >= 7).sum()
            neu = ((scores >= 5) & (scores < 7)).sum()
            neg = (scores < 5).sum()
        results["distribution"] = {
            "Positive": int(pos),
            "Neutral":  int(neu),
            "Negative": int(neg),
        }

    # ── AI recommendations ──
    total = sum(results["distribution"].values()) or 1
    pct   = {k: round(v/total*100) for k,v in results["distribution"].items()}
    rec_sys = f"""You are a customer experience consultant.
Based on sentiment data, give 4 specific, actionable recommendations.
Format as numbered list with bold titles. Be concrete."""
    rec_usr = f"""Sentiment: {pct}%
Positive themes: {results['themes_pos']}
Negative themes: {results['themes_neg']}
Dataset columns: {list(df.columns)}"""
    results["recommendations"] = call_ai(rec_sys, rec_usr)

    return results

# ── REPORT WITH CHARTS ────────────────────────────────────────────────────────
def parse_report_sections(report_text):
    """Split report into sections keyed by ### heading."""
    sections = []
    current_title = "Introduction"
    current_body  = []

    for line in report_text.split("\n"):
        line = line.strip()
        if line.startswith("## "):
            if current_body:
                sections.append({"title": current_title, "body": "\n".join(current_body)})
            current_title = line[3:]
            current_body  = []
        elif line.startswith("### "):
            if current_body:
                sections.append({"title": current_title, "body": "\n".join(current_body)})
            current_title = line[4:]
            current_body  = []
        elif line:
            current_body.append(line)

    if current_body:
        sections.append({"title": current_title, "body": "\n".join(current_body)})

    return sections

def render_section_chart(df, section_title):
    """
    Render a relevant chart based on section title.
    Returns True if a chart was rendered.
    """
    num_cols = df.select_dtypes(include='number').columns.tolist()
    cat_cols = [c for c in df.columns if df[c].nunique() < 20 and df[c].dtype == object]
    date_col = next((c for c in df.columns if 'date' in c.lower()), None)

    title_lower = section_title.lower()

    if not num_cols:
        return False

    # Trend Analysis → line chart
    if any(w in title_lower for w in ["trend","time","growth","monthly","quarterly"]):
        if date_col and num_cols:
            y = num_cols[0]
            try:
                st.markdown(f"<div style='font-size:11px;color:var(--muted);margin-bottom:6px;font-weight:600'>"
                            f"📈 {y} over {date_col}</div>", unsafe_allow_html=True)
                st.line_chart(df.set_index(date_col)[y], use_container_width=True)
                return True
            except Exception:
                pass

    # Key Findings / Overview → bar chart
    if any(w in title_lower for w in ["finding","overview","performance","sales","revenue"]):
        if cat_cols and num_cols:
            x, y = cat_cols[0], num_cols[0]
            st.markdown(f"<div style='font-size:11px;color:var(--muted);margin-bottom:6px;font-weight:600'>"
                        f"📊 {y} by {x}</div>", unsafe_allow_html=True)
            st.bar_chart(df.groupby(x)[y].sum().reset_index().set_index(x),
                         use_container_width=True)
            return True

    # Risk Signals → show highest risk metric
    if any(w in title_lower for w in ["risk","return","loss","churn","issue"]):
        risk_keywords = ['return','loss','churn','refund','cancel','issue','complaint']
        risk_cols = [c for c in num_cols if any(k in c.lower() for k in risk_keywords)]
        plot_col  = risk_cols[0] if risk_cols else num_cols[-1]
        if cat_cols:
            x = cat_cols[0]
            st.markdown(f"<div style='font-size:11px;color:var(--muted);margin-bottom:6px;font-weight:600'>"
                        f"⚠️ {plot_col} by {x}</div>", unsafe_allow_html=True)
            st.bar_chart(df.groupby(x)[plot_col].sum().reset_index().set_index(x),
                         use_container_width=True)
            return True

    return False

def render_report_with_charts(df, report_text):
    """Render report sections with auto-inserted charts."""
    sections = parse_report_sections(report_text)

    for sec in sections:
        title     = sec["title"]
        body      = sec["body"]
        title_low = title.lower()
        icon      = next((v for k,v in SECTION_ICONS.items() if k in title_low), "◈")

        st.markdown(f"""
        <div class="report-section">
          <div class="report-section-title">{icon} {title}</div>
          <div class="report-section-body">{body.replace(chr(10),'<br>')}</div>
        </div>
        """, unsafe_allow_html=True)

        # Insert chart after relevant sections
        if any(w in title_low for w in
               ["finding","trend","risk","overview","performance","sales","revenue"]):
            render_section_chart(df, title)

# ── PDF EXPORT ────────────────────────────────────────────────────────────────
def generate_pdf(report):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf,pagesize=A4,rightMargin=20*mm,leftMargin=20*mm,
                            topMargin=20*mm,bottomMargin=20*mm)
    S=getSampleStyleSheet()
    st_={
        't': ParagraphStyle('T',parent=S['Title'],  fontSize=20,spaceAfter=12),
        'h1':ParagraphStyle('H1',parent=S['Heading1'],fontSize=15,spaceAfter=8,spaceBefore=14),
        'h2':ParagraphStyle('H2',parent=S['Heading2'],fontSize=12,spaceAfter=6,spaceBefore=10),
        'b': ParagraphStyle('B', parent=S['Normal'],  fontSize=10,spaceAfter=4,leading=14),
        'bl':ParagraphStyle('BL',parent=S['Normal'],  fontSize=10,leftIndent=14,spaceAfter=3,leading=14),
    }
    story=[Paragraph("InsightIQ — Business Analysis Report",st_['t']),Spacer(1,5*mm)]
    for line in report.split("\n"):
        line=clean_text(line.strip())
        if not line:                      story.append(Spacer(1,3*mm))
        elif line.startswith("## "):      story.append(Paragraph(line[3:],st_['h1']))
        elif line.startswith("### "):     story.append(Paragraph(line[4:],st_['h2']))
        elif line.startswith(("- ","* ")):story.append(Paragraph("• "+line[2:],st_['bl']))
        else:                             story.append(Paragraph(line,st_['b']))
    doc.build(story); buf.seek(0)
    return buf

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:28px 20px 20px">
      <div style="display:flex;align-items:center;gap:12px">
        <div style="width:38px;height:38px;
          background:linear-gradient(135deg,#3B82F6,#6366F1,#8B5CF6);
          border-radius:11px;display:flex;align-items:center;justify-content:center;
          font-size:14px;font-weight:900;color:#fff;
          box-shadow:0 4px 16px rgba(59,130,246,.4);flex-shrink:0">IQ</div>
        <div>
          <div style="font-size:17px;font-weight:800;color:#F1F5F9;letter-spacing:-.02em">InsightIQ</div>
          <div style="font-size:10px;color:#3B82F6;letter-spacing:.12em;text-transform:uppercase;margin-top:2px;font-weight:600">AI ANALYST</div>
        </div>
      </div>
    </div>
    <div style="height:1px;background:#1E2D45;margin:0 16px 20px"></div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="padding:0 16px">', unsafe_allow_html=True)
    industry    = st.selectbox("Industry", ["General","Ecommerce","SaaS","Retail","Marketing"])
    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    report_type = st.selectbox("Report Type", [
        "Executive Summary","Sales Performance",
        "Trend Analysis","Strategic Recommendations","Risk Analysis"
    ])
    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    export_fmt  = st.radio("Export Format", ["Markdown (.md)","Word (.docx)","PDF (.pdf)"])
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div style="height:1px;background:#1E2D45;margin:16px 16px 20px"></div>', unsafe_allow_html=True)

    st.markdown('<div style="padding:0 16px">', unsafe_allow_html=True)
    is_premium = st.checkbox("⚡ Pro Mode")
    if is_premium:
        st.markdown('<div style="margin-top:10px"><span class="iq-badge iq-badge-gold">✦ Pro Active</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="position:fixed;bottom:0;left:0;width:264px;
      padding:14px 20px;border-top:1px solid #1E2D45;background:#0F1624">
      <div style="font-size:11px;color:#1E3A5F;line-height:1.8">
        Powered by <span style="color:#3B82F6;font-weight:600">Groq</span> ·
        Llama <span style="color:#6366F1;font-weight:600">3.3 70B</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
df = st.session_state.df

# ═══════════════════════════════════════════════════════════════════════════════
# LANDING PAGE
# ═══════════════════════════════════════════════════════════════════════════════
if df is None:
    st.markdown("""
    <div class="fade-up" style="max-width:700px;margin:52px auto 0;text-align:center;padding:0 20px">
      <div style="margin-bottom:20px">
        <span class="iq-badge iq-badge-blue">✦ AI-Powered · Sentiment · Charts · Recommendations</span>
      </div>
      <h1 style="font-size:50px;font-weight:900;color:#F1F5F9;line-height:1.08;
          letter-spacing:-.04em;margin-bottom:18px">
        Your AI<br>
        <span style="background:linear-gradient(135deg,#3B82F6,#6366F1,#8B5CF6);
          -webkit-background-clip:text;-webkit-text-fill-color:transparent;
          background-clip:text">Business Analyst</span>
      </h1>
      <p style="font-size:17px;color:#64748B;line-height:1.65;margin-bottom:36px">
        Upload sales data or customer reviews.<br>
        Get instant analysis, sentiment insights, and recommendations.
      </p>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_c, col_r = st.columns([1, 2.2, 1])
    with col_c:
        uploaded_files = st.file_uploader(
            "⬆ Drag & drop your CSV or Excel file",
            type=["csv","xlsx","xls"],
            accept_multiple_files=True,
            label_visibility="visible"
        )
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        scol1, scol2 = st.columns(2)
        with scol1:
            if st.button("📊 Sample Sales Data", use_container_width=True):
                st.session_state.df = pd.read_csv(io.StringIO(SAMPLE_CSV))
                st.session_state.messages = []
                st.session_state.report_cache = None
                st.session_state.sentiment_cache = None
                st.rerun()
        with scol2:
            if st.button("💬 Sample Reviews Data", use_container_width=True):
                st.session_state.df = pd.read_csv(io.StringIO(SAMPLE_REVIEWS))
                st.session_state.messages = []
                st.session_state.report_cache = None
                st.session_state.sentiment_cache = None
                st.rerun()

    if uploaded_files:
        sel = uploaded_files[0]
        if len(uploaded_files) > 1:
            chosen = st.selectbox("Select file",[f.name for f in uploaded_files])
            sel = next(f for f in uploaded_files if f.name == chosen)
        try:
            with st.spinner("Loading…"):
                st.session_state.df = load_data(sel)
            st.session_state.messages = []
            st.session_state.report_cache = None
            st.session_state.sentiment_cache = None
            st.rerun()
        except Exception as e:
            st.error(f"Could not read file: {e}")

    # Use case grid
    st.markdown("""
    <div style="max-width:860px;margin:40px auto 0;padding:0 20px">
      <div style="font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;
          color:#475569;text-align:center;margin-bottom:20px">What you can analyze</div>
    </div>
    """, unsafe_allow_html=True)
    uc_cols = st.columns(3)
    for i,(icon,title,desc) in enumerate(USE_CASES):
        with uc_cols[i%3]:
            st.markdown(f"""
            <div class="iq-usecase">
              <div style="font-size:22px;margin-bottom:8px">{icon}</div>
              <div style="font-size:13px;font-weight:600;color:var(--text);margin-bottom:4px">{title}</div>
              <div style="font-size:12px;color:var(--muted);line-height:1.5">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
else:
    kpis         = generate_kpis(df)
    has_sentiment = has_sentiment_data(df)

    # Top bar
    top_l, top_r = st.columns([3,1])
    with top_l:
        badges = '<span class="iq-badge iq-badge-green" style="margin-right:6px">● Live</span>'
        if has_sentiment:
            badges += '<span class="iq-badge iq-badge-purple">💬 Sentiment Ready</span>'
        if is_premium:
            badges += '<span class="iq-badge iq-badge-gold" style="margin-left:6px">✦ Pro</span>'
        st.markdown(f"""
        <div class="fade-in" style="padding:20px 0 4px">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px">
            <div style="font-size:24px;font-weight:800;color:#F1F5F9;letter-spacing:-.03em">Dashboard</div>
            {badges}
          </div>
          <div style="font-size:13px;color:#64748B">
            {df.shape[0]:,} rows · {df.shape[1]} columns ·
            <span style="color:#3B82F6;font-weight:500">{industry}</span> mode
          </div>
        </div>
        """, unsafe_allow_html=True)
    with top_r:
        st.markdown("<div style='padding-top:20px'></div>", unsafe_allow_html=True)
        if st.button("↑ New Dataset", use_container_width=True):
            st.session_state.df = None
            st.session_state.messages = []
            st.session_state.report_cache = None
            st.session_state.sentiment_cache = None
            st.rerun()

    # KPI row
    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("Total Rows",     f"{kpis['rows']:,}")
    c2.metric("Columns",        kpis['cols'])
    c3.metric("Missing Values", kpis['missing'])
    c4.metric("Completeness",   kpis['complete'])
    c5.metric("Numeric Cols",   kpis['num_cols'])
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # Build tab list dynamically
    tab_labels = ["  📊  Overview  ","  📈  Insights  ","  🤖  AI Analyst  ",
                  "  📋  Reports  ","  ⬇️  Export  "]
    if has_sentiment:
        tab_labels.insert(2, "  💬  Sentiment  ")

    tabs = st.tabs(tab_labels)  # tab index counter

    # ══ OVERVIEW ══════════════════════════════════════════════════
    with tabs[0]:
        st.markdown('<div class="iq-section">Data Preview</div>', unsafe_allow_html=True)
        st.dataframe(df.head(5), use_container_width=True)
        ca,cb = st.columns(2)
        with ca:
            st.markdown('<div class="iq-section" style="margin-top:20px">Column Schema</div>', unsafe_allow_html=True)
            st.dataframe(pd.DataFrame({
                "Column":   df.columns,
                "Type":     df.dtypes.astype(str).values,
                "Non-Null": df.count().values,
                "Missing":  df.isnull().sum().values,
            }), use_container_width=True, hide_index=True)
        with cb:
            st.markdown('<div class="iq-section" style="margin-top:20px">Numeric Summary</div>', unsafe_allow_html=True)
            num = df.select_dtypes(include='number')
            st.dataframe(num.describe().round(2) if not num.empty
                         else pd.DataFrame({"info":["No numeric columns"]}),
                         use_container_width=True)

    # ══ INSIGHTS (CHARTS) ═════════════════════════════════════════
    with tabs[1]:
        num_cols = df.select_dtypes(include='number').columns.tolist()
        cat_cols = [c for c in df.columns if df[c].nunique()<25 and df[c].dtype==object]
        date_col = next((c for c in df.columns if 'date' in c.lower()), None)

        if not num_cols:
            st.warning("No numeric columns for visualization.")
        else:
            v1,v2,v3 = st.tabs(["  Bar Chart  ","  Line Chart  ","  Correlation  "])
            with v1:
                r1,r2 = st.columns(2)
                y = r1.selectbox("Metric (Y)", num_cols, key="by")
                x = r2.selectbox("Group by",  cat_cols if cat_cols else num_cols, key="bx")
                st.bar_chart(df.groupby(x)[y].sum().reset_index().set_index(x),
                             use_container_width=True)
            with v2:
                r1,r2 = st.columns(2)
                ly = r1.selectbox("Metric", num_cols, key="ly")
                lx = r2.selectbox("X axis", ([date_col]+num_cols) if date_col else num_cols, key="lx")
                try:    st.line_chart(df.set_index(lx)[ly], use_container_width=True)
                except: st.line_chart(df[ly], use_container_width=True)
            with v3:
                corr = df[num_cols].corr().round(2)
                try:
                    st.dataframe(
                        corr.style.background_gradient(cmap="RdYlGn",axis=None).format("{:.2f}"),
                        use_container_width=True)
                except Exception:
                    st.dataframe(corr, use_container_width=True)
                st.caption("Green = positive · Red = negative correlation")

    # ══ SENTIMENT (CONDITIONAL) ═══════════════════════════════════
    if has_sentiment:
        with tabs[2]:
            st.markdown('<div class="iq-section">Sentiment Analysis</div>', unsafe_allow_html=True)

            text_cols  = detect_text_columns(df)
            score_cols = detect_score_columns(df)

            # Detection info
            if text_cols:
                st.markdown(f'<span class="iq-badge iq-badge-purple" style="margin-bottom:16px;display:inline-flex">💬 Text reviews detected in: {", ".join(text_cols)}</span>',
                            unsafe_allow_html=True)
            if score_cols:
                st.markdown(f'<span class="iq-badge iq-badge-blue" style="margin-bottom:16px;display:inline-flex">⭐ Score columns detected: {", ".join(score_cols)}</span>',
                            unsafe_allow_html=True)

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

            if st.button("🔍 Run Sentiment Analysis", type="primary", use_container_width=False):
                with st.spinner("Analysing reviews… this may take 20–30 seconds…"):
                    st.session_state.sentiment_cache = run_sentiment_analysis(df)

            if st.session_state.sentiment_cache:
                res   = st.session_state.sentiment_cache
                dist  = res["distribution"]
                total = sum(dist.values()) or 1

                # ── Sentiment Score Cards ──
                sa,sb,sc = st.columns(3)
                pos_pct = round(dist.get("Positive",0)/total*100)
                neu_pct = round(dist.get("Neutral", 0)/total*100)
                neg_pct = round(dist.get("Negative",0)/total*100)

                sa.metric("😊 Positive", f"{pos_pct}%", f"{dist.get('Positive',0)} reviews")
                sb.metric("😐 Neutral",  f"{neu_pct}%", f"{dist.get('Neutral', 0)} reviews")
                sc.metric("😞 Negative", f"{neg_pct}%", f"{dist.get('Negative',0)} reviews")

                st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

                # ── Sentiment Bar ──
                st.markdown(f"""
                <div style="margin-bottom:20px">
                  <div style="font-size:11px;color:var(--muted);margin-bottom:8px;font-weight:600;letter-spacing:.08em;text-transform:uppercase">
                    Overall Sentiment Distribution
                  </div>
                  <div style="display:flex;height:12px;border-radius:50px;overflow:hidden;gap:2px">
                    <div style="width:{pos_pct}%;background:#10B981;border-radius:50px 0 0 50px"></div>
                    <div style="width:{neu_pct}%;background:#F59E0B"></div>
                    <div style="width:{neg_pct}%;background:#EF4444;border-radius:0 50px 50px 0"></div>
                  </div>
                  <div style="display:flex;gap:20px;margin-top:8px;font-size:11px">
                    <span style="color:#10B981">● Positive {pos_pct}%</span>
                    <span style="color:#F59E0B">● Neutral {neu_pct}%</span>
                    <span style="color:#EF4444">● Negative {neg_pct}%</span>
                  </div>
                </div>
                """, unsafe_allow_html=True)

                # ── Chart ──
                if dist:
                    st.bar_chart(pd.DataFrame({"Count": dist}), use_container_width=True)

                # ── Themes ──
                if res["themes_pos"] or res["themes_neg"]:
                    th_a, th_b = st.columns(2)
                    with th_a:
                        st.markdown('<div class="iq-section">✅ What Customers Love</div>', unsafe_allow_html=True)
                        for t in res["themes_pos"]:
                            st.markdown(f'<div style="padding:8px 12px;background:rgba(16,185,129,.08);border:1px solid rgba(16,185,129,.2);border-radius:8px;font-size:13px;color:#6EE7B7;margin-bottom:6px">✓ {t}</div>',
                                        unsafe_allow_html=True)
                    with th_b:
                        st.markdown('<div class="iq-section">⚠️ Pain Points</div>', unsafe_allow_html=True)
                        for t in res["themes_neg"]:
                            st.markdown(f'<div style="padding:8px 12px;background:rgba(239,68,68,.08);border:1px solid rgba(239,68,68,.2);border-radius:8px;font-size:13px;color:#FCA5A5;margin-bottom:6px">✗ {t}</div>',
                                        unsafe_allow_html=True)

                # ── Labelled samples ──
                if res.get("sample_df") is not None:
                    st.markdown('<div class="iq-section" style="margin-top:20px">Labelled Reviews Sample</div>',
                                unsafe_allow_html=True)
                    st.dataframe(res["sample_df"], use_container_width=True, hide_index=True)

                # ── AI Recommendations ──
                if res["recommendations"]:
                    st.markdown('<div class="iq-section" style="margin-top:20px">🎯 Recommendations</div>',
                                unsafe_allow_html=True)
                    st.markdown(
                        f'<div class="iq-card iq-card-glow" style="font-size:14px;color:var(--text2);line-height:1.8">'
                        + res["recommendations"].replace('\n','<br>')
                        + '</div>',
                        unsafe_allow_html=True)

    # ══ AI ANALYST (CHAT) ══════════════════════════════════════════
    with tabs[3]:
        st.markdown('<div class="iq-section">AI Analyst · Ask Anything</div>', unsafe_allow_html=True)

        sugg_cols = st.columns(4)
        prompts = [
            "What trends do you see?",
            "Which segment performs best?",
            "What should I improve?",
            "Top 3 risks in my data?",
        ]
        for i,p in enumerate(prompts):
            if sugg_cols[i].button(p, key=f"p{i}", use_container_width=True):
                st.session_state["pending_input"] = p

        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

        # Text input + send button (chat_input not allowed inside tabs)
        ic, bc = st.columns([5,1])
        with ic:
            typed = st.text_input("msg",
                placeholder="Ask anything… e.g. 'What are the top revenue drivers?'",
                label_visibility="collapsed", key="chat_text")
        with bc:
            send = st.button("Send →", use_container_width=True, key="chat_send")

        if send and typed and typed != st.session_state.get("last_sent",""):
            st.session_state["pending_input"] = typed
            st.session_state["last_sent"] = typed

        # Process pending
        if st.session_state.get("pending_input"):
            inp = st.session_state.pop("pending_input")
            st.session_state.messages.append({"role":"user","content":inp})
            history = "\n".join([f"{m['role'].upper()}: {m['content']}"
                                  for m in st.session_state.messages[-8:]])
            sys_p = f"""You are InsightIQ, an elite AI business analyst.
Industry: {industry}. {INDUSTRY_PROMPTS[industry]}
Answer precisely. Use bullet points. Cite actual numbers from the data.
If the data contains reviews, include sentiment observations."""
            usr_p = f"Dataset:\n{get_data_context(df)}\n\nHistory:\n{history}\n\nQuestion: {inp}"
            with st.spinner("AI is thinking…"):
                reply = call_ai(sys_p, usr_p)
            st.session_state.messages.append({"role":"assistant","content":reply})

        # Render messages
        if not st.session_state.messages:
            st.markdown("""
            <div style="text-align:center;padding:50px 20px">
              <div style="font-size:40px;opacity:.3;margin-bottom:14px">🤖</div>
              <div style="font-size:15px;font-weight:600;color:#475569;margin-bottom:6px">Ask your first question</div>
              <div style="font-size:13px;color:#374151">Use the suggestions above or type below</div>
            </div>""", unsafe_allow_html=True)
        else:
            for m in st.session_state.messages:
                if m["role"]=="user":
                    st.markdown(f'<div class="iq-msg-user"><div class="iq-bubble-user">{m["content"]}</div></div>',
                                unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="iq-msg-ai"><div class="iq-avatar">IQ</div>'
                                f'<div class="iq-bubble-ai">{m["content"].replace(chr(10),"<br>")}</div></div>',
                                unsafe_allow_html=True)
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
            if st.button("Clear conversation", key="clr"):
                st.session_state.messages = []
                st.rerun()

    # ══ REPORTS (WITH INLINE CHARTS) ══════════════════════════════
    with tabs[4]:
        st.markdown('<div class="iq-section">Report Generator · Charts Included</div>', unsafe_allow_html=True)

        focus = st.text_input("Custom focus (optional)",
            placeholder="e.g. Focus on Q1 vs Q2 regional gap")

        btn1, btn2 = st.columns(2)
        with btn1:
            if st.button("⚡ Generate Report + Charts", type="primary", use_container_width=True):
                sys_p = f"""You are an elite business intelligence analyst writing a {report_type}.
Industry: {industry}. {INDUSTRY_PROMPTS[industry]}
Structure the report exactly with these section headers (use ### for each):
### Data Overview
### Key Findings
### Trend Analysis
### Risk Signals
### Strategic Recommendations
### Executive Takeaway
Use real numbers. Be specific. Charts will be auto-inserted after each section."""
                with st.spinner("Generating report with charts…"):
                    st.session_state.report_cache = call_ai(
                        sys_p,
                        get_data_context(df)+(f"\nFocus: {focus}" if focus else "")
                    )

        with btn2:
            if is_premium:
                if st.button("🎯 Deep Recommendations", use_container_width=True):
                    sys_p = f"""You are a McKinsey-level consultant.
Industry: {industry}. {INDUSTRY_PROMPTS[industry]}
Deliver 5 specific prioritized recommendations.
Each: **Bold Title**, Problem, Action, Expected Impact, Timeline."""
                    with st.spinner("Generating deep recommendations…"):
                        st.session_state.report_cache = call_ai(sys_p, get_data_context(df))
            else:
                st.markdown("""
                <div class="iq-locked-wrap">
                  <div class="iq-lock-blur">
                    <div style="background:#1A2338;border-radius:14px;padding:20px;height:80px"></div>
                  </div>
                  <div class="iq-lock-overlay">
                    <span style="font-size:20px">🔒</span>
                    <div style="font-size:14px;font-weight:700;color:var(--text)">Pro Feature</div>
                    <div style="font-size:12px;color:var(--muted)">Enable Pro Mode in sidebar</div>
                  </div>
                </div>""", unsafe_allow_html=True)

        # ── Render report with embedded charts ──
        if st.session_state.report_cache:
            st.markdown('<div class="iq-div"></div>', unsafe_allow_html=True)
            st.markdown("""
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:16px">
              <span class="iq-badge iq-badge-blue">📊 Charts auto-embedded per section</span>
            </div>
            """, unsafe_allow_html=True)
            render_report_with_charts(df, st.session_state.report_cache)

    # ══ EXPORT ════════════════════════════════════════════════════
    with tabs[5]:
        st.markdown('<div class="iq-section">Export</div>', unsafe_allow_html=True)

        if not st.session_state.report_cache:
            st.markdown("""
            <div style="text-align:center;padding:50px 20px">
              <div style="font-size:38px;opacity:.3;margin-bottom:14px">📄</div>
              <div style="font-size:15px;font-weight:600;color:#475569;margin-bottom:6px">No report yet</div>
              <div style="font-size:13px;color:#374151">Generate a report in the Reports tab first</div>
            </div>""", unsafe_allow_html=True)
        else:
            report = st.session_state.report_cache
            with st.expander("Preview report"):
                st.text(report[:700]+"…" if len(report)>700 else report)

            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

            if export_fmt=="Markdown (.md)":
                st.download_button("⬇️ Download as Markdown", data=report,
                    file_name="insightiq_report.md", mime="text/markdown",
                    use_container_width=True)

            elif export_fmt=="Word (.docx)":
                try:
                    from docx import Document
                    doc=Document()
                    doc.add_heading("InsightIQ — Business Analysis Report",0)
                    for line in report.split("\n"):
                        line=line.strip()
                        if not line: continue
                        if line.startswith("## "):        doc.add_heading(line[3:],1)
                        elif line.startswith("### "):     doc.add_heading(line[4:],2)
                        elif line.startswith(("- ","* ")):doc.add_paragraph(line[2:],style="List Bullet")
                        else:                            doc.add_paragraph(line)
                    buf=io.BytesIO(); doc.save(buf); buf.seek(0)
                    st.download_button("⬇️ Download as Word", data=buf,
                        file_name="insightiq_report.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True)
                except ImportError:
                    st.error("pip install python-docx")

            elif export_fmt=="PDF (.pdf)":
                try:
                    st.download_button("⬇️ Download as PDF",
                        data=generate_pdf(report),
                        file_name="insightiq_report.pdf",
                        mime="application/pdf",
                        use_container_width=True)
                except ImportError:
                    st.error("pip install reportlab")

            st.markdown('<div class="iq-div"></div>', unsafe_allow_html=True)
            st.download_button("⬇️ Export Dataset as CSV",
                data=df.to_csv(index=False).encode("utf-8"),
                file_name="dataset_export.csv", mime="text/csv",
                use_container_width=True)