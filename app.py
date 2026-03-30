import os
import pandas as pd
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="Business Insight Generator", page_icon="📊", layout="wide")
st.title("📊 AI Business Insight Generator")
st.markdown("Upload CSV files and generate instant AI-powered business reports.")

# ── Sidebar ────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Report Settings")
    report_type = st.selectbox("Report Type", [
        "Executive Summary", "Sales Performance",
        "Trend Analysis", "Strategic Recommendations"
    ])
    custom_focus = st.text_input("Custom Focus (optional)",
        placeholder="e.g. Focus on regional gaps")
    st.divider()
    st.caption("Powered by Groq + Llama 3.3")

# ── File Upload ────────────────────────────────────────────
uploaded_files = st.file_uploader(
    "Upload one or more CSV files",
    type=["csv"],
    accept_multiple_files=True
)

if uploaded_files:
    if len(uploaded_files) > 1:
        selected_name = st.selectbox(
            "Select file to analyse",
            [f.name for f in uploaded_files]
        )
        uploaded_file = next(f for f in uploaded_files if f.name == selected_name)
    else:
        uploaded_file = uploaded_files[0]

    df = pd.read_csv(uploaded_file)
    st.success(f"✅ Loaded **{uploaded_file.name}** — {df.shape[0]} rows, {df.shape[1]} columns")

    # ── Metrics ────────────────────────────────────────────
    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Numeric Columns", len(df.select_dtypes(include='number').columns))

    st.subheader("📋 Data Preview")
    st.dataframe(df.head(10), use_container_width=True)

    # ── Charts ─────────────────────────────────────────────
    st.subheader("📈 Data Visualizations")
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    date_col = next((c for c in df.columns if 'date' in c.lower()), None)

    if numeric_cols:
        tab1, tab2, tab3 = st.tabs(["📊 Bar Chart", "📉 Line Chart", "🔥 Correlation"])

        with tab1:
            col_choice = st.selectbox("Select column", numeric_cols, key="bar")
            group_col = st.selectbox("Group by",
                [c for c in df.columns if df[c].nunique() < 20], key="bar_group")
            chart_data = df.groupby(group_col)[col_choice].sum().reset_index()
            st.bar_chart(chart_data.set_index(group_col))

        with tab2:
            col_choice2 = st.selectbox("Select column", numeric_cols, key="line")
            if date_col:
                st.line_chart(df.set_index(date_col)[col_choice2])
            else:
                st.line_chart(df[col_choice2])

        with tab3:
            st.dataframe(df[numeric_cols].corr().round(2), use_container_width=True)

    st.divider()

    # ── Generate ───────────────────────────────────────────
    if st.button("🚀 Generate Report", type="primary", use_container_width=True):
        with st.spinner("Analysing data and generating report..."):
            prompt = f"""You are an elite business intelligence analyst.
Generate a {report_type} report using this exact structure:
## {report_type} Report
### 📊 Data Overview
### 🔍 Key Findings
### 📈 Trend Analysis
### ⚠️ Risk Signals
### ✅ Strategic Recommendations
### 💡 Executive Takeaway
Use real numbers. Be specific and concise.
Statistics:
{df.describe().round(1).to_string()}
{f'Additional focus: {custom_focus}' if custom_focus else ''}"""

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are an elite business intelligence analyst."},
                    {"role": "user", "content": prompt}
                ]
            )
            report = response.choices[0].message.content

        st.subheader("📄 Generated Report")
        st.markdown(report)
        st.divider()
        st.download_button(
            label="⬇️ Download Report (.md)",
            data=report,
            file_name="business_report.md",
            mime="text/markdown",
            use_container_width=True
        )

else:
    st.info("👆 Upload one or more CSV files to get started.")