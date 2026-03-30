import os
import io
import re
import pandas as pd
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="Business Insight Generator", page_icon="📊", layout="wide")
st.title("📊 AI Business Insight Generator")
st.markdown("Upload CSV or Excel files and generate instant AI-powered business reports.")

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
    export_format = st.radio("Download Format", ["Markdown (.md)", "Word (.docx)", "PDF (.pdf)"])
    st.divider()
    st.caption("Powered by Groq + Llama 3.3")

# ── File Upload ────────────────────────────────────────────
uploaded_files = st.file_uploader(
    "Upload one or more CSV or Excel files",
    type=["csv", "xlsx", "xls"],
    accept_multiple_files=True
)

def read_file(f):
    if f.name.endswith(".csv"):
        return pd.read_csv(f)
    return pd.read_excel(f)

def clean_text(text):
    return re.sub(r'[^\x00-\x7F]+', '', text).strip()

if uploaded_files:
    if len(uploaded_files) > 1:
        selected_name = st.selectbox("Select file to analyse", [f.name for f in uploaded_files])
        uploaded_file = next(f for f in uploaded_files if f.name == selected_name)
    else:
        uploaded_file = uploaded_files[0]

    df = read_file(uploaded_file)
    st.success(f"✅ Loaded **{uploaded_file.name}** — {df.shape[0]} rows, {df.shape[1]} columns")

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
### Data Overview
### Key Findings
### Trend Analysis
### Risk Signals
### Strategic Recommendations
### Executive Takeaway

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

        # ── Markdown ───────────────────────────────────────
        if export_format == "Markdown (.md)":
            st.download_button(
                label="⬇️ Download as Markdown",
                data=report,
                file_name="business_report.md",
                mime="text/markdown",
                use_container_width=True
            )

        # ── Word ───────────────────────────────────────────
        elif export_format == "Word (.docx)":
            try:
                from docx import Document
                doc = Document()
                doc.add_heading("Business Insight Report", 0)
                for line in report.split("\n"):
                    line = line.strip()
                    if not line:
                        continue
                    if line.startswith("## "):
                        doc.add_heading(line[3:], level=1)
                    elif line.startswith("### "):
                        doc.add_heading(line[4:], level=2)
                    elif line.startswith("- ") or line.startswith("* "):
                        doc.add_paragraph(line[2:], style="List Bullet")
                    else:
                        doc.add_paragraph(line)
                buf = io.BytesIO()
                doc.save(buf)
                buf.seek(0)
                st.download_button(
                    label="⬇️ Download as Word",
                    data=buf,
                    file_name="business_report.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
            except ImportError:
                st.error("Run: pip install python-docx")

        # ── PDF ────────────────────────────────────────────
        elif export_format == "PDF (.pdf)":
            try:
                from fpdf import FPDF
                pdf = FPDF()
                pdf.add_page()
                pdf.set_margins(15, 15, 15)

                for line in report.split("\n"):
                    line = line.strip()
                    if not line:
                        pdf.ln(3)
                        continue
                    if line.startswith("## "):
                        pdf.set_font("Helvetica", "B", 16)
                        pdf.multi_cell(0, 10, clean_text(line[3:]))
                    elif line.startswith("### "):
                        pdf.set_font("Helvetica", "B", 13)
                        pdf.multi_cell(0, 8, clean_text(line[4:]))
                    elif line.startswith("- ") or line.startswith("* "):
                        pdf.set_font("Helvetica", size=11)
                        pdf.multi_cell(0, 7, "- " + clean_text(line[2:]))
                    else:
                        pdf.set_font("Helvetica", size=11)
                        pdf.multi_cell(0, 7, clean_text(line))

                buf = io.BytesIO(pdf.output())
                st.download_button(
                    label="⬇️ Download as PDF",
                    data=buf,
                    file_name="business_report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except ImportError:
                st.error("Run: pip install fpdf2")

else:
    st.info("👆 Upload a CSV or Excel file to get started.")