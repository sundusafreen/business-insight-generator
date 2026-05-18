# InsightIQ — AI Business Decision Engine

> Upload any sales or business dataset. Get instant KPIs, 
> visualisations, and an AI analyst you can ask questions 
> in plain English. Export a full business report in minutes.

**[Try it live →]([YOUR-STREAMLIT-LINK](https://business-insight-generator-iznknezr5a6nf55athdudq.streamlit.app/))**
&nbsp;&nbsp;&nbsp;&nbsp;*(No installation required — runs in your browser)*
---

## Why I built this

A sales manager shouldn't need to know Python or SQL to 
answer "which region is underperforming this quarter?" 

I built InsightIQ so that anyone — a Sales Ops lead, a 
commercial analyst, a regional manager — can upload their 
data and get real, grounded answers in under five minutes. 
No code. No dashboards to configure. Just questions and answers.

---

## What it does

Upload a CSV or Excel file and the app gives you:

- **Instant KPI summary** — row counts, revenue totals, 
  key metrics auto-detected from your columns
- **Auto-generated visualisations** — bar charts, line 
  charts, and correlation heatmaps built from your data
- **AI Analyst chat** — ask questions like 
  *"Which region is underperforming?"* or 
  *"What are the top three revenue drivers?"* 
  and get data-grounded answers
- **Structured report export** — Executive Summary, 
  Sales Performance, Risk Analysis, and Strategic 
  Recommendations, exported as Markdown, Word, or PDF

---

## Screenshots

### Dashboard Overview
<img width="1465" height="837" alt="Screenshot 2026-05-18 at 11 47 24 PM" src="https://github.com/user-attachments/assets/0115d83e-44e5-4224-806a-85813a2515c2" />

### AI Analyst in Action
<img width="1465" height="837" alt="Screenshot 2026-05-18 at 11 49 21 PM" src="https://github.com/user-attachments/assets/0425aa51-6b0b-4d9d-aba8-f77d30096a2a" />


### Report Export
<img width="1465" height="837" alt="Screenshot 2026-05-18 at 11 50 03 PM" src="https://github.com/user-attachments/assets/32ff9b71-1bb6-44d7-8cfa-367608927574" />

---

## Tech Stack

| Layer | Tool |
|---|---|
| UI Framework | Streamlit |
| LLM | Llama 3.3 70B via Groq API |
| Data Processing | Pandas |
| PDF Export | ReportLab |
| Word Export | python-docx |
| Environment | python-dotenv |

---

## Industry Modes

The AI prompt layer adapts to your context:

| Mode | Focus Areas |
|---|---|
| **SaaS** | MRR, churn rate, LTV, trial conversion |
| **Retail** | Sell-through, basket size, returns |
| **Ecommerce** | Cart abandonment, AOV, fulfilment |
| **Marketing** | CAC, ROAS, channel attribution |
| **General** | Revenue, volume, trend analysis |

---

## Getting Started (Local)

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

Create a `.env` file:
