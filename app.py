"""
InsightIQ — AI Business Decision Engine
World-class SaaS UI · Groq + Llama 3.3 · Production Ready
"""

import os, io, re, warnings
import pandas as pd
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

warnings.filterwarnings("ignore")
load_dotenv()

st.set_page_config(
    page_title="InsightIQ · AI Business Analyst",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap');
:root{--bg:#080c14;--bg2:#0d1117;--s:#111827;--s2:#161f2e;--s3:#1a2640;--b:#1e2d42;--b2:#243348;--a:#3b82f6;--a2:#6366f1;--a3:#8b5cf6;--ok:#10b981;--warn:#f59e0b;--err:#ef4444;--t:#f1f5f9;--t2:#cbd5e1;--m:#64748b;--m2:#475569;--r:16px;--rs:10px;}
*,*::before,*::after{box-sizing:border-box;}
html,body,[class*="css"],.stApp{font-family:'Inter',-apple-system,sans-serif!important;background:var(--bg)!important;color:var(--t)!important;-webkit-font-smoothing:antialiased;}
#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stDecoration"],[data-testid="stStatusWidget"]{display:none!important;}
::-webkit-scrollbar{width:3px;height:3px;}::-webkit-scrollbar-track{background:transparent;}::-webkit-scrollbar-thumb{background:var(--b2);border-radius:4px;}
section[data-testid="stSidebar"]{background:var(--bg2)!important;border-right:1px solid var(--b)!important;}
section[data-testid="stSidebar"]>div:first-child{padding-top:0!important;}
.stSelectbox>div>div,.stSelectbox [data-baseweb="select"]>div{background:var(--s2)!important;border:1px solid var(--b)!important;border-radius:var(--rs)!important;color:var(--t)!important;font-size:13px!important;}
.stSelectbox label,.stRadio>label,.stCheckbox>label{color:var(--m)!important;font-size:10px!important;font-weight:600!important;letter-spacing:.1em!important;text-transform:uppercase!important;}
.stRadio label span{color:var(--t2)!important;font-size:13px!important;}
.stTextInput input,.stTextArea textarea{background:var(--s2)!important;border:1px solid var(--b)!important;border-radius:var(--rs)!important;color:var(--t)!important;font-family:'Inter',sans-serif!important;font-size:14px!important;transition:border-color .2s!important;}
.stTextInput input:focus,.stTextArea textarea:focus{border-color:var(--a)!important;box-shadow:0 0 0 3px rgba(59,130,246,.12)!important;}
.stButton>button{background:linear-gradient(135deg,var(--a) 0%,var(--a2) 100%)!important;color:#fff!important;border:none!important;border-radius:var(--rs)!important;font-family:'Inter',sans-serif!important;font-size:13px!important;font-weight:600!important;padding:10px 22px!important;letter-spacing:.01em!important;transition:all .2s cubic-bezier(.4,0,.2,1)!important;box-shadow:0 1px 3px rgba(0,0,0,.3),0 0 16px rgba(59,130,246,.2)!important;}
.stButton>button:hover{transform:translateY(-2px) scale(1.01)!important;box-shadow:0 8px 24px rgba(59,130,246,.35)!important;filter:brightness(1.08)!important;}
.stButton>button:active{transform:translateY(0) scale(.99)!important;}
[data-testid="stFileUploader"] section{background:var(--s)!important;border:2px dashed var(--b2)!important;border-radius:var(--r)!important;padding:24px!important;transition:all .25s ease!important;}
[data-testid="stFileUploader"] section:hover{border-color:var(--a)!important;background:rgba(59,130,246,.04)!important;box-shadow:0 0 0 4px rgba(59,130,246,.08),0 0 32px rgba(59,130,246,.12)!important;}
div[data-testid="stMetric"]{background:var(--s)!important;border:1px solid var(--b)!important;border-radius:var(--r)!important;padding:22px 24px!important;position:relative!important;overflow:hidden!important;transition:all .25s cubic-bezier(.4,0,.2,1)!important;cursor:default!important;}
div[data-testid="stMetric"]::after{content:'';position:absolute;bottom:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--a),var(--a2));opacity:0;transition:opacity .25s;}
div[data-testid="stMetric"]:hover{border-color:var(--a)!important;transform:translateY(-3px)!important;box-shadow:0 12px 32px rgba(59,130,246,.15),0 0 0 1px rgba(59,130,246,.2)!important;}
div[data-testid="stMetric"]:hover::after{opacity:1;}
div[data-testid="stMetricLabel"]{color:var(--m)!important;font-size:10px!important;font-weight:700!important;letter-spacing:.12em!important;text-transform:uppercase!important;margin-bottom:6px!important;}
div[data-testid="stMetricValue"]{color:var(--t)!important;font-size:30px!important;font-weight:800!important;letter-spacing:-.03em!important;line-height:1!important;}
.stTabs [data-baseweb="tab-list"]{background:var(--s)!important;border:1px solid var(--b)!important;border-radius:50px!important;padding:4px 5px!important;gap:2px!important;display:inline-flex!important;margin-bottom:28px!important;box-shadow:0 2px 12px rgba(0,0,0,.3)!important;}
.stTabs [data-baseweb="tab"]{background:transparent!important;color:var(--m)!important;border:none!important;border-radius:50px!important;font-family:'Inter',sans-serif!important;font-size:13px!important;font-weight:500!important;padding:8px 22px!important;transition:all .2s ease!important;white-space:nowrap!important;}
.stTabs [data-baseweb="tab"]:hover{color:var(--t2)!important;}
.stTabs [aria-selected="true"]{background:linear-gradient(135deg,var(--a),var(--a2))!important;color:#fff!important;font-weight:600!important;box-shadow:0 2px 16px rgba(59,130,246,.4)!important;}
.stTabs [data-baseweb="tab-highlight"],.stTabs [data-baseweb="tab-border"]{display:none!important;}
.stDataFrame{border:1px solid var(--b)!important;border-radius:var(--r)!important;overflow:hidden!important;}
[data-testid="stChatInput"]{background:var(--s)!important;border:1px solid var(--b2)!important;border-radius:var(--r)!important;box-shadow:0 4px 20px rgba(0,0,0,.3)!important;}
[data-testid="stChatInput"]:focus-within{border-color:var(--a)!important;box-shadow:0 0 0 3px rgba(59,130,246,.12),0 4px 20px rgba(0,0,0,.3)!important;}
[data-testid="stChatInputTextArea"]{background:transparent!important;color:var(--t)!important;font-family:'Inter',sans-serif!important;font-size:14px!important;}
.stSuccess{background:rgba(16,185,129,.08)!important;border:1px solid rgba(16,185,129,.25)!important;border-radius:var(--rs)!important;}
.stInfo{background:rgba(59,130,246,.06)!important;border:1px solid rgba(59,130,246,.2)!important;border-radius:var(--rs)!important;}
.stWarning{background:rgba(245,158,11,.08)!important;border:1px solid rgba(245,158,11,.2)!important;border-radius:var(--rs)!important;}
.stError{background:rgba(239,68,68,.08)!important;border:1px solid rgba(239,68,68,.2)!important;border-radius:var(--rs)!important;}
.streamlit-expanderHeader{background:var(--s)!important;border:1px solid var(--b)!important;border-radius:var(--rs)!important;color:var(--m2)!important;font-size:13px!important;}
.stSpinner>div{border-top-color:var(--a)!important;}
@keyframes fadeUp{from{opacity:0;transform:translateY(16px);}to{opacity:1;transform:translateY(0);}}
.iq-f1{animation:fadeUp .5s ease both;}
.iq-f2{animation:fadeUp .5s .1s ease both;}
.iq-f3{animation:fadeUp .5s .2s ease both;}
.iq-f4{animation:fadeUp .5s .3s ease both;}
.iq-grad{background:linear-gradient(135deg,#60a5fa 0%,#a78bfa 50%,#f472b6 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.iq-card{background:var(--s);border:1px solid var(--b);border-radius:var(--r);padding:24px;transition:all .25s ease;}
.iq-card:hover{border-color:rgba(59,130,246,.35);box-shadow:0 8px 32px rgba(59,130,246,.1);transform:translateY(-2px);}
.iq-h{font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--m);margin:0 0 14px;padding-bottom:12px;border-bottom:1px solid var(--b);}
.iq-div{height:1px;background:var(--b);margin:20px 0;}
.iq-badge{display:inline-flex;align-items:center;gap:5px;font-size:10px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;padding:3px 10px;border-radius:50px;}
.iq-blue{background:rgba(59,130,246,.12);border:1px solid rgba(59,130,246,.25);color:#93c5fd;}
.iq-green{background:rgba(16,185,129,.1);border:1px solid rgba(16,185,129,.25);color:#6ee7b7;}
.iq-gold{background:linear-gradient(135deg,rgba(245,158,11,.15),rgba(239,68,68,.1));border:1px solid rgba(245,158,11,.3);color:#fcd34d;}
.iq-msg-u{display:flex;justify-content:flex-end;margin:12px 0;}
.iq-bub-u{background:linear-gradient(135deg,#2563eb,#4f46e5);color:#fff;padding:12px 18px;border-radius:20px 20px 4px 20px;max-width:70%;font-size:14px;line-height:1.65;box-shadow:0 4px 20px rgba(59,130,246,.3);word-wrap:break-word;}
.iq-msg-a{display:flex;align-items:flex-start;gap:10px;margin:12px 0;}
.iq-av{width:30px;height:30px;flex-shrink:0;background:linear-gradient(135deg,#3b82f6,#8b5cf6);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:800;color:#fff;box-shadow:0 0 12px rgba(59,130,246,.35);margin-top:2px;}
.iq-bub-a{background:var(--s2);border:1px solid var(--b2);color:var(--t2);padding:14px 18px;border-radius:4px 20px 20px 20px;max-width:78%;font-size:14px;line-height:1.75;word-wrap:break-word;}
.iq-empty{text-align:center;padding:64px 32px;}
.iq-empty-icon{font-size:44px;margin-bottom:16px;opacity:.35;}
.iq-empty-title{font-size:19px;font-weight:700;color:var(--t2);margin-bottom:8px;}
.iq-empty-sub{font-size:14px;color:var(--m);line-height:1.6;}
.iq-uc{background:var(--s2);border:1px solid var(--b);border-radius:var(--r);padding:20px;transition:all .2s;height:100%;}
.iq-uc:hover{border-color:rgba(59,130,246,.4);background:rgba(59,130,246,.04);transform:translateY(-2px);box-shadow:0 8px 24px rgba(59,130,246,.1);}
.iq-step{display:flex;align-items:flex-start;gap:12px;padding:12px 0;border-bottom:1px solid var(--b);}
.iq-step:last-child{border-bottom:none;}
.iq-step-n{width:26px;height:26px;flex-shrink:0;background:linear-gradient(135deg,var(--a),var(--a2));border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:800;color:#fff;}
.iq-report{background:var(--s);border:1px solid var(--b2);border-radius:var(--r);padding:28px 32px;line-height:1.85;color:var(--t2);font-size:14px;}
.iq-report h2{font-size:20px;font-weight:800;color:var(--t);margin:20px 0 12px;letter-spacing:-.02em;}
.iq-report h3{font-size:12px;font-weight:700;color:#60a5fa;margin:18px 0 8px;letter-spacing:.06em;text-transform:uppercase;}
.iq-lock-wrap{position:relative;}
.iq-lock-over{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;background:rgba(8,12,20,.8);backdrop-filter:blur(4px);border-radius:var(--r);z-index:10;gap:8px;}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

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

IND = {
    "General":   "Focus on revenue trends, performance gaps, and growth drivers.",
    "Ecommerce": "Focus on AOV, conversion rates, cart abandonment, and seasonal trends.",
    "SaaS":      "Focus on MRR, churn, CAC, LTV, and expansion revenue.",
    "Retail":    "Focus on sell-through, inventory turnover, basket size, and margin.",
    "Marketing": "Focus on ROAS, CPL, CTR, funnel conversion, and campaign ROI.",
}
USE_CASES=[("📈","Sales Analysis","Uncover revenue drivers and blockers."),
           ("👥","Customer Insights","Understand behaviour and segments."),
           ("💰","Revenue Trends","Track growth and forecast performance."),
           ("⚠️","Risk Detection","Find anomalies and churn signals.")]
STEPS=[("Upload","Drop your CSV or Excel file"),("Analyse","See KPIs and smart charts"),
       ("Ask","Chat with AI about your data"),("Decide","Get recs and export")]

for k,v in [("messages",[]),("report_cache",None),("df",None),("pending_input",None)]:
    if k not in st.session_state: st.session_state[k]=v

@st.cache_resource
def get_client():
    key=os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY","")
    return Groq(api_key=key) if key else None
client=get_client()

def load_data(f): return pd.read_csv(f) if f.name.endswith(".csv") else pd.read_excel(f)
def clean(t): return re.sub(r'[^\x00-\x7F]','',t).strip()
def ctx(df,n=8):
    num=df.select_dtypes(include='number')
    return f"Dataset: {df.shape[0]}r x {df.shape[1]}c\nCols:{list(df.columns)}\nMissing:{df.isnull().sum().to_dict()}\nStats:\n{num.describe().round(2).to_string() if not num.empty else 'N/A'}\nSample:\n{df.head(n).to_csv(index=False)}"
def ai(sys_p,usr_p):
    if not client: return "No API key. Add GROQ_API_KEY to secrets."
    try:
        r=client.chat.completions.create(model="llama-3.3-70b-versatile",max_tokens=1500,
            messages=[{"role":"system","content":sys_p},{"role":"user","content":usr_p}])
        return r.choices[0].message.content
    except Exception as e: return f"Error: {e}"
def kpis(df):
    m=int(df.isnull().sum().sum())
    return{"rows":df.shape[0],"cols":df.shape[1],"missing":m,
           "health":f"{100-m/max(df.size,1)*100:.1f}%","num":len(df.select_dtypes(include='number').columns)}
def make_pdf(report):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer
    buf=io.BytesIO()
    doc=SimpleDocTemplate(buf,pagesize=A4,rightMargin=20*mm,leftMargin=20*mm,topMargin=20*mm,bottomMargin=20*mm)
    S=getSampleStyleSheet()
    st_=ParagraphStyle('T',parent=S['Title'],fontSize=20,spaceAfter=12)
    h1=ParagraphStyle('H1',parent=S['Heading1'],fontSize=15,spaceAfter=8,spaceBefore=14)
    h2=ParagraphStyle('H2',parent=S['Heading2'],fontSize=12,spaceAfter=6,spaceBefore=10)
    bd=ParagraphStyle('B',parent=S['Normal'],fontSize=10,spaceAfter=4,leading=14)
    bl=ParagraphStyle('BL',parent=S['Normal'],fontSize=10,leftIndent=14,spaceAfter=3,leading=14)
    story=[Paragraph("InsightIQ Report",st_),Spacer(1,5*mm)]
    for line in report.split("\n"):
        line=clean(line.strip())
        if not line: story.append(Spacer(1,3*mm))
        elif line.startswith("## "): story.append(Paragraph(line[3:],h1))
        elif line.startswith("### "): story.append(Paragraph(line[4:],h2))
        elif line.startswith(("- ","* ")): story.append(Paragraph("• "+line[2:],bl))
        else: story.append(Paragraph(line,bd))
    doc.build(story); buf.seek(0); return buf

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("""
    <div style="padding:28px 22px 20px">
      <div style="display:flex;align-items:center;gap:11px">
        <div style="width:36px;height:36px;background:linear-gradient(135deg,#3b82f6,#8b5cf6);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:15px;font-weight:900;color:#fff;box-shadow:0 0 20px rgba(59,130,246,.3)">IQ</div>
        <div>
          <div style="font-size:17px;font-weight:800;color:#f1f5f9;letter-spacing:-.02em">InsightIQ</div>
          <div style="font-size:9px;color:#475569;letter-spacing:.14em;text-transform:uppercase">AI ANALYST · BETA</div>
        </div>
      </div>
    </div>
    <div class="iq-div" style="margin:0 0 18px"></div>
    """, unsafe_allow_html=True)

    df_state = st.session_state.df
    if df_state is not None:
        st.markdown(f"""<div style="margin:0 16px 18px;padding:11px 14px;background:rgba(16,185,129,.06);border:1px solid rgba(16,185,129,.2);border-radius:10px;display:flex;align-items:center;gap:8px">
        <span style="width:7px;height:7px;border-radius:50%;background:#10b981;box-shadow:0 0 8px #10b981;flex-shrink:0;display:inline-block"></span>
        <span style="font-size:12px;color:#6ee7b7;font-weight:500">Active · {df_state.shape[0]:,} rows</span></div>""", unsafe_allow_html=True)

    with st.container():
        st.markdown('<div style="padding:0 4px">', unsafe_allow_html=True)
        industry    = st.selectbox("Industry",["General","Ecommerce","SaaS","Retail","Marketing"])
        report_type = st.selectbox("Report Type",["Executive Summary","Sales Performance","Trend Analysis","Strategic Recommendations","Risk Analysis"])
        export_fmt  = st.radio("Export Format",["Markdown (.md)","Word (.docx)","PDF (.pdf)"])
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="iq-div"></div>', unsafe_allow_html=True)
    is_premium = st.checkbox("⚡ Unlock Premium")
    if is_premium:
        st.markdown("""<div style="margin-top:10px;padding:10px 14px;background:linear-gradient(135deg,rgba(245,158,11,.1),rgba(239,68,68,.08));border:1px solid rgba(245,158,11,.3);border-radius:10px">
        <div style="font-size:12px;font-weight:700;color:#fcd34d;margin-bottom:2px">✦ Pro Activated</div>
        <div style="font-size:11px;color:#78716c">All features unlocked</div></div>""", unsafe_allow_html=True)

    st.markdown('<div class="iq-div"></div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:10px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#475569;margin-bottom:12px">How it works</div>', unsafe_allow_html=True)
    for i,(t,s) in enumerate(STEPS):
        st.markdown(f"""<div class="iq-step"><div class="iq-step-n">{i+1}</div><div><div style="font-size:13px;font-weight:600;color:#f1f5f9;margin-bottom:2px">{t}</div><div style="font-size:12px;color:#64748b">{s}</div></div></div>""", unsafe_allow_html=True)
    st.markdown("""<div style="margin-top:24px;padding-top:16px;border-top:1px solid #1e2d42">
    <div style="font-size:11px;color:#1e293b;line-height:1.7">Powered by <span style="color:#3b82f6;font-weight:600">Groq</span> · Llama 3.3 70B<br><span style="color:#0f172a">© 2024 InsightIQ</span></div></div>""", unsafe_allow_html=True)

df = st.session_state.df

# ── MAIN ──
if df is None:
    st.markdown("""<div class="iq-f1" style="max-width:680px;margin:52px auto 40px;text-align:center;padding:0 16px">
    <div class="iq-badge iq-blue" style="margin-bottom:22px">✦ AI-Powered Decision Engine</div>
    <h1 style="font-size:52px;font-weight:900;color:#f1f5f9;line-height:1.06;letter-spacing:-.04em;margin-bottom:18px">
    Your AI<br><span class="iq-grad">Business Analyst</span></h1>
    <p style="font-size:18px;color:#64748b;line-height:1.65;font-weight:400">Turn raw data into decisions in seconds.<br>Upload a dataset. Ask anything. Get answers.</p></div>""", unsafe_allow_html=True)

    _,uc,_ = st.columns([1,2.2,1])
    with uc:
        st.markdown('<div class="iq-f2">', unsafe_allow_html=True)
        uploaded_files = st.file_uploader("⬆ Drag & drop your CSV or Excel file, or click to browse",type=["csv","xlsx","xls"],accept_multiple_files=True,label_visibility="visible")
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        st.markdown('<div class="iq-f3">', unsafe_allow_html=True)
        c1,c2=st.columns(2)
        with c1:
            if st.button("✦ Load Sample Dataset",use_container_width=True):
                st.session_state.df=pd.read_csv(io.StringIO(SAMPLE_CSV))
                st.session_state.messages=[]
                st.session_state.report_cache=None
                st.rerun()
        with c2:
            st.markdown("""<div style="padding:10px;text-align:center;font-size:11px;color:#475569;border:1px solid #1e2d42;border-radius:10px;line-height:1.5">CSV · XLSX · XLS<br><span style="color:#64748b">Up to 200 MB</span></div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        if uploaded_files:
            sel=uploaded_files[0]
            if len(uploaded_files)>1:
                ch=st.selectbox("Select",[f.name for f in uploaded_files])
                sel=next(f for f in uploaded_files if f.name==ch)
            try:
                st.session_state.df=load_data(sel)
                st.session_state.messages=[]
                st.session_state.report_cache=None
                st.rerun()
            except Exception as e: st.error(f"Error: {e}")

    st.markdown('<div class="iq-f4" style="max-width:860px;margin:44px auto 0"><div style="text-align:center;font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#475569;margin-bottom:20px">What you can analyse</div></div>', unsafe_allow_html=True)
    _,gc,_=st.columns([1,4,1])
    with gc:
        cols=st.columns(4)
        for i,(icon,title,sub) in enumerate(USE_CASES):
            with cols[i]:
                st.markdown(f'<div class="iq-uc"><div style="font-size:24px;margin-bottom:10px">{icon}</div><div style="font-size:14px;font-weight:700;color:#f1f5f9;margin-bottom:5px">{title}</div><div style="font-size:12px;color:#64748b;line-height:1.5">{sub}</div></div>', unsafe_allow_html=True)

else:
    k=kpis(df)
    tl,tr=st.columns([3,1])
    with tl:
        st.markdown(f"""<div style="padding:16px 0 20px;border-bottom:1px solid #1e2d42;margin-bottom:24px">
        <div style="font-size:20px;font-weight:800;color:#f1f5f9;letter-spacing:-.02em">Dashboard</div>
        <div style="font-size:13px;color:#64748b;margin-top:3px">{df.shape[0]:,} rows · {df.shape[1]} columns · {industry} mode <span class="iq-badge iq-green" style="margin-left:8px">● Live</span></div></div>""", unsafe_allow_html=True)
    with tr:
        st.markdown("<div style='padding-top:16px'></div>", unsafe_allow_html=True)
        if st.button("↑ New Dataset",use_container_width=True):
            st.session_state.df=None; st.session_state.messages=[]; st.session_state.report_cache=None; st.rerun()

    c1,c2,c3,c4,c5=st.columns(5)
    c1.metric("Total Rows",f"{k['rows']:,}")
    c2.metric("Columns",k['cols'])
    c3.metric("Missing",k['missing'])
    c4.metric("Health",k['health'])
    c5.metric("Numeric Cols",k['num'])
    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    tab1,tab2,tab3,tab4,tab5=st.tabs(["  📊  Overview  ","  📈  Insights  ","  🤖  AI Analyst  ","  📋  Reports  ","  ⬇️  Export  "])

    with tab1:
        st.markdown('<div class="iq-h">Data Preview</div>', unsafe_allow_html=True)
        st.dataframe(df.head(6),use_container_width=True)
        la,ra=st.columns(2)
        with la:
            st.markdown('<div class="iq-h" style="margin-top:20px">Column Schema</div>', unsafe_allow_html=True)
            st.dataframe(pd.DataFrame({"Column":df.columns,"Type":df.dtypes.astype(str).values,"Non-Null":df.count().values,"Missing":df.isnull().sum().values}),use_container_width=True,hide_index=True)
        with ra:
            st.markdown('<div class="iq-h" style="margin-top:20px">Numeric Summary</div>', unsafe_allow_html=True)
            num=df.select_dtypes(include='number')
            st.dataframe(num.describe().round(2) if not num.empty else pd.DataFrame(),use_container_width=True)

    with tab2:
        nc=df.select_dtypes(include='number').columns.tolist()
        cc=[c for c in df.columns if df[c].nunique()<30 and df[c].dtype==object]
        dc=next((c for c in df.columns if 'date' in c.lower()),None)
        if not nc: st.warning("No numeric columns found.")
        else:
            v1,v2,v3=st.tabs(["  Bar Chart  ","  Line Chart  ","  Correlation  "])
            with v1:
                r1,r2=st.columns(2)
                y=r1.selectbox("Metric",nc,key="by"); x=r2.selectbox("Group by",cc if cc else nc,key="bx")
                st.bar_chart(df.groupby(x)[y].sum().reset_index().set_index(x),use_container_width=True)
            with v2:
                r1,r2=st.columns(2)
                ly=r1.selectbox("Metric",nc,key="ly"); lx=r2.selectbox("X axis",([dc]+nc) if dc else nc,key="lx")
                try: st.line_chart(df.set_index(lx)[ly],use_container_width=True)
                except: st.line_chart(df[ly],use_container_width=True)
            with v3:
                corr=df[nc].corr().round(2)
                try: st.dataframe(corr.style.background_gradient(cmap="RdYlGn",axis=None).format("{:.2f}"),use_container_width=True)
                except: st.dataframe(corr,use_container_width=True)
                st.caption("Green = positive · Red = negative correlation")

    with tab3:
        st.markdown('<div class="iq-h">AI Analyst · Ask anything about your data</div>', unsafe_allow_html=True)
        sugg=["What trends do you see?","Which segment performs best?","What risks should I know?","Give 3 specific recommendations."]
        sc=st.columns(4)
        for i,s in enumerate(sugg):
            if sc[i].button(s,key=f"s{i}",use_container_width=True):
                st.session_state["pending_input"]=s

        user_input=st.chat_input("Ask anything about your data…")
        if user_input: st.session_state["pending_input"]=user_input

        if st.session_state.get("pending_input"):
            inp=st.session_state.pop("pending_input")
            st.session_state.messages.append({"role":"user","content":inp})
            history="\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages[-10:]])
            sp=f"You are InsightIQ, an elite AI business analyst. Industry: {industry}. {IND[industry]}\nBe precise, data-driven. Use bullet points. Cite numbers."
            up=f"Dataset:\n{ctx(df)}\n\nConversation:\n{history}\n\nQuestion: {inp}"
            with st.spinner("AI is thinking…"):
                reply=ai(sp,up)
            st.session_state.messages.append({"role":"assistant","content":reply})

        if not st.session_state.messages:
            st.markdown('<div class="iq-empty"><div class="iq-empty-icon">🤖</div><div class="iq-empty-title">Start a conversation</div><div class="iq-empty-sub">Click a suggestion above or type your question.<br>The AI has full context of your dataset.</div></div>', unsafe_allow_html=True)
        else:
            for m in st.session_state.messages:
                if m["role"]=="user":
                    st.markdown(f'<div class="iq-msg-u"><div class="iq-bub-u">{m["content"]}</div></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="iq-msg-a"><div class="iq-av">IQ</div><div class="iq-bub-a">{m["content"].replace(chr(10),"<br>")}</div></div>', unsafe_allow_html=True)
            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
            if st.button("Clear conversation",key="clr"):
                st.session_state.messages=[]; st.rerun()

    with tab4:
        st.markdown('<div class="iq-h">Report Generator</div>', unsafe_allow_html=True)
        focus=st.text_input("Custom focus (optional)",placeholder="e.g. Focus on Q1 vs Q2 regional gap")
        b1,b2=st.columns(2)
        with b1:
            if st.button("⚡ Generate Report",type="primary",use_container_width=True):
                sp=f"You are an elite business intelligence analyst writing a {report_type}.\nIndustry: {industry}. {IND[industry]}\nStructure:\n## {report_type}\n### Data Overview\n### Key Findings\n### Trend Analysis\n### Risk Signals\n### Strategic Recommendations\n### Executive Takeaway\nUse real numbers. No filler."
                with st.spinner("Generating report…"):
                    st.session_state.report_cache=ai(sp,ctx(df)+(f"\nFocus: {focus}" if focus else ""))
        with b2:
            if is_premium:
                if st.button("🎯 Deep Recommendations",use_container_width=True):
                    sp=f"You are a McKinsey-level consultant. Industry: {industry}. {IND[industry]}\nDeliver 5 prioritized recommendations. Each: Problem, Action, Impact, Timeline. Bold headers."
                    with st.spinner("Building recommendations…"):
                        st.session_state.report_cache=ai(sp,ctx(df))
            else:
                st.markdown("""<div class="iq-lock-wrap"><div style="border:1px dashed #1e2d42;border-radius:14px;padding:20px;text-align:center;opacity:.35;font-size:13px;color:#475569">🎯 Deep Recommendations<br><small>Advanced strategic analysis</small></div><div class="iq-lock-over"><div style="font-size:26px">🔒</div><div style="font-size:14px;font-weight:700;color:#f1f5f9">Premium Feature</div><div style="font-size:12px;color:#64748b">Enable Premium in sidebar</div></div></div>""", unsafe_allow_html=True)

        if st.session_state.report_cache:
            st.markdown('<div class="iq-div"></div>', unsafe_allow_html=True)
            rh=st.session_state.report_cache
            rh=re.sub(r'^## (.+)$',r'<h2>\1</h2>',rh,flags=re.M)
            rh=re.sub(r'^### (.+)$',r'<h3>\1</h3>',rh,flags=re.M)
            rh=re.sub(r'\*\*(.+?)\*\*',r'<strong style="color:#f1f5f9">\1</strong>',rh)
            rh=re.sub(r'^[-*] (.+)$',r'<li style="margin-bottom:5px">\1</li>',rh,flags=re.M)
            rh=rh.replace('\n\n','<br>')
            st.markdown(f'<div class="iq-report">{rh}</div>', unsafe_allow_html=True)

    with tab5:
        st.markdown('<div class="iq-h">Export & Download</div>', unsafe_allow_html=True)
        if not st.session_state.report_cache:
            st.markdown('<div class="iq-empty"><div class="iq-empty-icon">📄</div><div class="iq-empty-title">No report yet</div><div class="iq-empty-sub">Generate a report in the Reports tab first.</div></div>', unsafe_allow_html=True)
        else:
            report=st.session_state.report_cache
            with st.expander("Preview"): st.text(report[:600]+"…" if len(report)>600 else report)
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            if export_fmt=="Markdown (.md)":
                st.download_button("⬇️ Download Markdown",data=report,file_name="insightiq_report.md",mime="text/markdown",use_container_width=True)
            elif export_fmt=="Word (.docx)":
                try:
                    from docx import Document
                    doc=Document(); doc.add_heading("InsightIQ Report",0)
                    for line in report.split("\n"):
                        line=line.strip()
                        if not line: continue
                        if line.startswith("## "): doc.add_heading(line[3:],1)
                        elif line.startswith("### "): doc.add_heading(line[4:],2)
                        elif line.startswith(("- ","* ")): doc.add_paragraph(line[2:],style="List Bullet")
                        else: doc.add_paragraph(line)
                    buf=io.BytesIO(); doc.save(buf); buf.seek(0)
                    st.download_button("⬇️ Download Word",data=buf,file_name="insightiq_report.docx",mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",use_container_width=True)
                except ImportError: st.error("pip install python-docx")
            elif export_fmt=="PDF (.pdf)":
                try: st.download_button("⬇️ Download PDF",data=make_pdf(report),file_name="insightiq_report.pdf",mime="application/pdf",use_container_width=True)
                except ImportError: st.error("pip install reportlab")
            st.markdown('<div class="iq-div"></div>', unsafe_allow_html=True)
            st.download_button("⬇️ Download Dataset (CSV)",data=df.to_csv(index=False).encode("utf-8"),file_name="dataset.csv",mime="text/csv",use_container_width=True)