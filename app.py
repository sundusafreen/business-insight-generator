"""
InsightIQ — AI Business Analyst Assistant
Production-grade Streamlit app · Groq + Llama 3.3
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

# ── CUSTOM CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #080b12; color: #e2e8f0; }
section[data-testid="stSidebar"] { background: #0d1117 !important; border-right: 1px solid #1e2433; }
header[data-testid="stHeader"] { display: none; }
.section-header { font-family: 'Syne', sans-serif; font-size: 17px; font-weight: 700; color: #f1f5f9;
    margin: 24px 0 14px; padding-bottom: 8px; border-bottom: 1px solid #1e2433; }
.chat-user { background: #1e2433; border-radius: 12px 12px 4px 12px; padding: 12px 16px;
    margin: 8px 0; margin-left: 20%; color: #e2e8f0; font-size: 14px; }
.chat-assistant { background: #0f1923; border: 1px solid #1e2433; border-radius: 12px 12px 12px 4px;
    padding: 14px 18px; margin: 8px 0; margin-right: 10%; color: #cbd5e1; font-size: 14px; line-height: 1.7; }
.chat-label { font-size: 10px; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 6px; }
.chat-label-user { color: #3b82f6; } .chat-label-ai { color: #10b981; }
.premium-badge { display: inline-block; background: linear-gradient(90deg,#f59e0b,#ef4444);
    color: white; font-size: 9px; letter-spacing: 0.1em; text-transform: uppercase; font-weight: 600;
    padding: 2px 8px; border-radius: 20px; margin-left: 8px; vertical-align: middle; }
.stButton > button { background: #1e40af; color: white; border: none; border-radius: 6px;
    font-family: 'DM Sans', sans-serif; font-weight: 500; }
.stButton > button:hover { background: #2563eb; border: none; }
div[data-testid="stMetric"] { background: #0d1117; border: 1px solid #1e2433;
    border-radius: 8px; padding: 16px; }
.stTabs [data-baseweb="tab-list"] { background: #0d1117; border-bottom: 1px solid #1e2433; }
.stTabs [data-baseweb="tab"] { color: #64748b; font-family: 'DM Sans', sans-serif; font-size: 13px; }
.stTabs [aria-selected="true"] { color: #3b82f6 !important; border-bottom: 2px solid #3b82f6 !important; }
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
for key, val in [("messages", []), ("report_cache", None), ("df", None)]:
    if key not in st.session_state:
        st.session_state[key] = val

# ── GROQ CLIENT ───────────────────────────────────────────────────────────────
@st.cache_resource
def get_client():
    key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", "")
    return Groq(api_key=key) if key else None

client = get_client()

# ── HELPER FUNCTIONS ──────────────────────────────────────────────────────────

def load_data(f) -> pd.DataFrame:
    """Load CSV or Excel file."""
    return pd.read_csv(f) if f.name.endswith(".csv") else pd.read_excel(f)

def clean_text(t: str) -> str:
    """Strip non-ASCII for PDF."""
    return re.sub(r'[^\x00-\x7F]+', '', t).strip()

def get_data_context(df: pd.DataFrame, n: int = 8) -> str:
    """Compact dataset summary for AI context."""
    num = df.select_dtypes(include='number')
    return f"""DATASET: {df.shape[0]} rows x {df.shape[1]} cols
Columns: {list(df.columns)}
Missing: {df.isnull().sum().to_dict()}
Stats:\n{num.describe().round(2).to_string() if not num.empty else 'N/A'}
Sample:\n{df.head(n).to_csv(index=False)}"""

def call_ai(system: str, user: str) -> str:
    """Call Groq API."""
    if not client:
        return "No API key found. Add GROQ_API_KEY to your .env or Streamlit secrets."
    try:
        r = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=1500,
            messages=[{"role": "system", "content": system},
                      {"role": "user",   "content": user}]
        )
        return r.choices[0].message.content
    except Exception as e:
        return f"API error: {e}"

def generate_kpis(df: pd.DataFrame) -> dict:
    """Compute dashboard KPIs."""
    missing = int(df.isnull().sum().sum())
    return {
        "rows":       df.shape[0],
        "cols":       df.shape[1],
        "missing":    missing,
        "complete":   f"{100 - missing/df.size*100:.1f}%",
        "num_cols":   len(df.select_dtypes(include='number').columns),
    }

def generate_pdf(report: str) -> io.BytesIO:
    """Build PDF with ReportLab."""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, rightMargin=20*mm, leftMargin=20*mm,
                            topMargin=20*mm, bottomMargin=20*mm)
    S = getSampleStyleSheet()
    s_t  = ParagraphStyle('T',  parent=S['Title'],   fontSize=20, spaceAfter=12)
    s_h1 = ParagraphStyle('H1', parent=S['Heading1'],fontSize=15, spaceAfter=8,  spaceBefore=14)
    s_h2 = ParagraphStyle('H2', parent=S['Heading2'],fontSize=12, spaceAfter=6,  spaceBefore=10)
    s_b  = ParagraphStyle('B',  parent=S['Normal'],  fontSize=10, spaceAfter=4,  leading=14)
    s_bl = ParagraphStyle('BL', parent=S['Normal'],  fontSize=10, leftIndent=14, spaceAfter=3, leading=14)
    story = [Paragraph("InsightIQ — Business Analysis Report", s_t), Spacer(1, 5*mm)]
    for line in report.split("\n"):
        line = clean_text(line.strip())
        if not line:                        story.append(Spacer(1, 3*mm))
        elif line.startswith("## "):        story.append(Paragraph(line[3:], s_h1))
        elif line.startswith("### "):       story.append(Paragraph(line[4:], s_h2))
        elif line.startswith(("- ","* ")): story.append(Paragraph("• "+line[2:], s_bl))
        else:                               story.append(Paragraph(line, s_b))
    doc.build(story)
    buf.seek(0)
    return buf

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:20px 0 8px'>
        <div style='font-family:Syne,sans-serif;font-size:22px;font-weight:800;color:#f1f5f9'>InsightIQ</div>
        <div style='font-size:11px;color:#475569;letter-spacing:.08em;margin-top:2px'>AI BUSINESS ANALYST</div>
    </div>""", unsafe_allow_html=True)
    st.divider()

    industry    = st.selectbox("Industry Mode",  ["General","Ecommerce","SaaS","Retail","Marketing"])
    report_type = st.selectbox("Report Type",    ["Executive Summary","Sales Performance",
                                                   "Trend Analysis","Strategic Recommendations","Risk Analysis"])
    export_fmt  = st.radio("Export Format",      ["Markdown (.md)","Word (.docx)","PDF (.pdf)"])
    st.divider()
    is_premium  = st.checkbox("⚡ Premium Mode", help="Unlock deep recommendations & advanced insights")
    if is_premium:
        st.success("Premium features unlocked")
    st.divider()
    st.caption("Powered by Groq · Llama 3.3 · 70B")

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='padding:32px 0 20px'>
    <div style='font-family:Syne,sans-serif;font-size:36px;font-weight:800;color:#f1f5f9;line-height:1.1'>
        AI Business Analyst</div>
    <div style='font-size:15px;color:#64748b;margin-top:8px'>
        Upload your data · Ask anything · Get boardroom-ready insights</div>
</div>""", unsafe_allow_html=True)

# ── FILE UPLOAD ───────────────────────────────────────────────────────────────
up_col, sample_col = st.columns([3, 1])
with up_col:
    uploaded_files = st.file_uploader("Upload CSV or Excel",
        type=["csv","xlsx","xls"], accept_multiple_files=True, label_visibility="collapsed")
with sample_col:
    if st.button("Load Sample Data", use_container_width=True):
        st.session_state.df = pd.read_csv(io.StringIO(SAMPLE_CSV))
        st.session_state.messages = []
        st.session_state.report_cache = None

if uploaded_files:
    selected = uploaded_files[0]
    if len(uploaded_files) > 1:
        chosen   = st.selectbox("Select file", [f.name for f in uploaded_files])
        selected = next(f for f in uploaded_files if f.name == chosen)
    try:
        st.session_state.df = load_data(selected)
        st.session_state.messages = []
        st.session_state.report_cache = None
    except Exception as e:
        st.error(f"Could not read file: {e}")

df = st.session_state.df

# ── MAIN CONTENT ──────────────────────────────────────────────────────────────
if df is not None:
    st.success(f"Dataset loaded — {df.shape[0]:,} rows · {df.shape[1]} columns")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["📊 Overview","📈 Visualize","🤖 AI Chat","📋 Reports","⬇️ Export"])

    # ── TAB 1: OVERVIEW ───────────────────────────────────────────────────────
    with tab1:
        kpis = generate_kpis(df)
        c1,c2,c3,c4,c5 = st.columns(5)
        c1.metric("Total Rows",      f"{kpis['rows']:,}")
        c2.metric("Total Columns",   kpis['cols'])
        c3.metric("Missing Values",  kpis['missing'])
        c4.metric("Completeness",    kpis['complete'])
        c5.metric("Numeric Columns", kpis['num_cols'])

        st.markdown('<div class="section-header">Data Preview</div>', unsafe_allow_html=True)
        st.dataframe(df.head(5), use_container_width=True)

        ca, cb = st.columns(2)
        with ca:
            st.markdown('<div class="section-header">Column Types</div>', unsafe_allow_html=True)
            st.dataframe(pd.DataFrame({
                "Column":  df.columns,
                "Type":    df.dtypes.astype(str).values,
                "Non-Null":df.count().values,
                "Missing": df.isnull().sum().values,
            }), use_container_width=True, hide_index=True)
        with cb:
            st.markdown('<div class="section-header">Numeric Summary</div>', unsafe_allow_html=True)
            num = df.select_dtypes(include='number')
            st.dataframe(num.describe().round(2) if not num.empty else pd.DataFrame(), use_container_width=True)

    # ── TAB 2: VISUALIZE ──────────────────────────────────────────────────────
    with tab2:
        num_cols = df.select_dtypes(include='number').columns.tolist()
        cat_cols = [c for c in df.columns if df[c].nunique() < 25 and df[c].dtype == object]
        date_col = next((c for c in df.columns if 'date' in c.lower()), None)

        if not num_cols:
            st.warning("No numeric columns detected.")
        else:
            v1,v2,v3 = st.tabs(["Bar Chart","Line Chart","Correlation Heatmap"])

            with v1:
                r1,r2 = st.columns(2)
                y = r1.selectbox("Metric",   num_cols,                          key="by")
                x = r2.selectbox("Group by", cat_cols if cat_cols else num_cols, key="bx")
                st.bar_chart(df.groupby(x)[y].sum().reset_index().set_index(x), use_container_width=True)

            with v2:
                r1,r2 = st.columns(2)
                ly = r1.selectbox("Metric", num_cols, key="ly")
                lx = r2.selectbox("X axis",  ([date_col]+num_cols) if date_col else num_cols, key="lx")
                try:    st.line_chart(df.set_index(lx)[ly], use_container_width=True)
                except: st.line_chart(df[ly], use_container_width=True)

            with v3:
                corr = df[num_cols].corr().round(2)
                st.dataframe(
                    corr.style.background_gradient(cmap="RdYlGn", axis=None).format("{:.2f}"),
                    use_container_width=True)
                st.caption("Green = strong positive · Red = strong negative correlation")

    # ── TAB 3: AI CHAT ────────────────────────────────────────────────────────
    with tab3:
        st.markdown('<div class="section-header">Ask Your Data Anything</div>', unsafe_allow_html=True)

        # Quick suggestions
        suggestions = ["What are the top trends?","Which segment performs best?",
                       "What risks should I know?","Give 3 actionable recommendations."]
        sc = st.columns(4)
        for i,s in enumerate(suggestions):
            if sc[i].button(s, key=f"sug{i}", use_container_width=True):
                st.session_state.messages.append({"role":"user","content":s})

        # Render history
        for m in st.session_state.messages:
            if m["role"] == "user":
                st.markdown(f'<div class="chat-user"><div class="chat-label chat-label-user">You</div>{m["content"]}</div>',
                            unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-assistant"><div class="chat-label chat-label-ai">◈ InsightIQ</div>{m["content"].replace(chr(10),"<br>")}</div>',
                            unsafe_allow_html=True)

        # Input
        if inp := st.chat_input("Ask about your data..."):
            st.session_state.messages.append({"role":"user","content":inp})
            history = "\n".join([f"{m['role'].upper()}: {m['content']}"
                                  for m in st.session_state.messages[-8:]])
            sys_p = f"""You are InsightIQ, an elite AI business analyst.
Industry: {industry}. {INDUSTRY_PROMPTS[industry]}
Be specific. Use numbers. Format with bullet points where helpful."""
            usr_p = f"Dataset:\n{get_data_context(df)}\n\nConversation:\n{history}\n\nQuestion: {inp}"
            with st.spinner("Analysing..."):
                reply = call_ai(sys_p, usr_p)
            st.session_state.messages.append({"role":"assistant","content":reply})
            st.rerun()

        if st.session_state.messages:
            if st.button("Clear Chat"):
                st.session_state.messages = []
                st.rerun()

    # ── TAB 4: REPORTS ────────────────────────────────────────────────────────
    with tab4:
        st.markdown('<div class="section-header">AI-Generated Report</div>', unsafe_allow_html=True)
        focus = st.text_input("Custom focus (optional)", placeholder="e.g. Q1 vs Q2 regional gap")

        r1, r2 = st.columns(2)
        with r1:
            if st.button("⚡ Generate Report", type="primary", use_container_width=True):
                sys_p = f"""You are an elite business intelligence analyst writing a {report_type}.
Industry: {industry}. {INDUSTRY_PROMPTS[industry]}
Structure:
## {report_type}
### Data Overview
### Key Findings
### Trend Analysis
### Risk Signals
### Strategic Recommendations
### Executive Takeaway
Use real numbers. No filler."""
                with st.spinner("Generating report..."):
                    st.session_state.report_cache = call_ai(sys_p, get_data_context(df) + (f"\nFocus: {focus}" if focus else ""))

        with r2:
            if is_premium:
                if st.button("🎯 Deep Recommendations", use_container_width=True):
                    sys_p = f"""You are a McKinsey-level consultant. Industry: {industry}. {INDUSTRY_PROMPTS[industry]}
Produce 5 prioritized recommendations. Each: problem, action, expected impact, timeline. Use bold titles."""
                    with st.spinner("Generating..."):
                        st.session_state.report_cache = call_ai(sys_p, get_data_context(df))
            else:
                st.markdown("""<div style='border:1px dashed #374151;border-radius:6px;padding:14px;
                    text-align:center;color:#6b7280;font-size:13px'>
                    🎯 Deep Recommendations <span class="premium-badge">PREMIUM</span>
                    <br><small>Enable Premium in sidebar</small></div>""", unsafe_allow_html=True)

        if st.session_state.report_cache:
            st.markdown("---")
            st.markdown(st.session_state.report_cache)

    # ── TAB 5: EXPORT ─────────────────────────────────────────────────────────
    with tab5:
        st.markdown('<div class="section-header">Export</div>', unsafe_allow_html=True)
        if not st.session_state.report_cache:
            st.info("Generate a report in the Reports tab first.")
        else:
            report = st.session_state.report_cache
            with st.expander("Report preview"):
                st.text(report[:800] + "..." if len(report) > 800 else report)

            if export_fmt == "Markdown (.md)":
                st.download_button("⬇️ Download Markdown", data=report,
                    file_name="insightiq_report.md", mime="text/markdown", use_container_width=True)

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
                    st.download_button("⬇️ Download Word", data=buf,
                        file_name="insightiq_report.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True)
                except ImportError:
                    st.error("pip install python-docx")

            elif export_fmt == "PDF (.pdf)":
                try:
                    st.download_button("⬇️ Download PDF", data=generate_pdf(report),
                        file_name="insightiq_report.pdf", mime="application/pdf", use_container_width=True)
                except ImportError:
                    st.error("pip install reportlab")

            st.markdown("---")
            st.download_button("⬇️ Download Dataset (CSV)",
                data=df.to_csv(index=False).encode("utf-8"),
                file_name="dataset_export.csv", mime="text/csv", use_container_width=True)

else:
    st.markdown("""
    <div style='text-align:center;padding:80px 40px;color:#374151'>
        <div style='font-size:48px;margin-bottom:16px'>◈</div>
        <div style='font-family:Syne,sans-serif;font-size:20px;color:#6b7280;margin-bottom:8px'>
            No data loaded yet</div>
        <div style='font-size:14px;color:#4b5563'>
            Upload a CSV or Excel file above, or click "Load Sample Data" to explore</div>
    </div>""", unsafe_allow_html=True)