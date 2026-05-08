# InsightIQ — AI Business Decision Engine

A Streamlit web app that lets you upload any business dataset, explore it visually, and ask an AI analyst questions about it in plain English. Built with Groq's Llama 3.3 70B model.

---

## What it does

You upload a CSV or Excel file. The app gives you an instant KPI summary, bar charts, line charts, and a correlation matrix — no code required. Then you can open the AI Analyst tab and ask questions like *"Which region is underperforming?"* or *"What are the top three revenue drivers?"* and get specific, data-grounded answers.

When you're done, you can generate a full business report (Executive Summary, Sales Performance, Risk Analysis, and more) and export it as Markdown, Word, or PDF.

---

## Features

- **AI chat analyst** — powered by Groq + Llama 3.3 70B, with full dataset context passed on every query
- **Auto visualisations** — bar charts, line charts, and correlation heatmaps built from your actual columns
- **Report generator** — structured reports with KPIs, findings, risk signals, and strategic recommendations
- **Export options** — Markdown, Word (.docx), and PDF via ReportLab
- **Industry modes** — General, Ecommerce, SaaS, Retail, Marketing (each tunes the AI's analysis focus)
- **Sample dataset** — built-in sales data so you can try it immediately without uploading anything

---

## Tech stack

| Layer | Tool |
|---|---|
| UI framework | Streamlit |
| LLM | Llama 3.3 70B via Groq API |
| Data processing | Pandas |
| PDF export | ReportLab |
| Word export | python-docx |
| Env management | python-dotenv |

---

## Getting started

**1. Clone the repo**
```bash
git clone https://github.com/sundusafreen/business-insight-generator.git
cd business-insight-generator
```

**2. Install dependencies**
```bash
pip install streamlit groq pandas python-dotenv reportlab python-docx openpyxl
```

**3. Add your Groq API key**

Create a `.env` file in the root folder:
```
GROQ_API_KEY=your_key_here
```
Get a free key at [console.groq.com](https://console.groq.com)

**4. Run the app**
```bash
streamlit run app.py
```

---

## How to use it

1. Upload a CSV or Excel file — or click **Load Sample Dataset** to start immediately
2. Check the **Overview** tab for a data summary and schema
3. Go to **Insights** to explore charts
4. Open **AI Analyst** and ask questions about your data
5. Head to **Reports** to generate a structured business report
6. Download your report from the **Export** tab

---

## Project context

Built as part of my MSc in Business Analytics at Trinity College Dublin. The goal was to make business data analysis accessible without requiring SQL or Python knowledge — something a sales manager or operations lead could pick up in five minutes and get real answers from.

The AI prompt layer is designed around industry-specific analysis modes, so the model's output is grounded in what actually matters for each context (e.g. for SaaS it focuses on MRR, churn, and LTV; for Retail it focuses on sell-through and basket size).

---

## Author

**Sundus Afreen** — MSc Business Analytics, Trinity College Dublin  
[LinkedIn](https://linkedin.com/in/sundusafreen) · [GitHub](https://github.com/sundusafreen)
