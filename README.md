# ◈ InsightIQ — AI Business Analyst

> Turn raw data into boardroom-ready insights in seconds. No SQL. No Python. Just answers.

![Python](https://img.shields.io/badge/Python-3.10+-3B82F6?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-10B981?style=flat-square)
![Status](https://img.shields.io/badge/Status-Live-10B981?style=flat-square)

---

## What is InsightIQ?

InsightIQ is a production-grade AI business intelligence tool built with Streamlit. Upload any CSV or Excel file and instantly get KPI dashboards, interactive charts, AI-generated reports, and sentiment analysis — all from a clean, modern interface that feels like a real SaaS product.

It supports three AI providers out of the box. Users bring their own API key — zero hosting cost for you.

**Live demo →** [business-insight-generator-iznknezr5a6nf55athdudq.streamlit.app](https://business-insight-generator-iznknezr5a6nf55athdudq.streamlit.app)

---

## Features

### Core
- **CSV & Excel upload** — drag and drop any business dataset
- **KPI Dashboard** — auto-generated metric cards: rows, columns, completeness, missing values
- **Interactive Charts** — bar charts, line charts, correlation heatmap with dynamic column selection
- **AI Chat Assistant** — ask anything about your data in plain English, with full conversation memory
- **Report Generator** — structured AI reports with charts auto-embedded per section
- **Sentiment Analysis** — auto-detects text review columns or numeric score columns and runs full sentiment breakdown

### Export
- **Markdown** — structured report with table of contents, section icons, ready for Notion or GitHub
- **Word (.docx)** — professional document with branded cover page, color-coded section headers
- **PDF (.pdf)** — polished report with dark cover, numbered section cards, branded header/footer
- **CSV** — export the analysed dataset directly

### AI Providers (Bring Your Own Key)
| Provider | Model | Cost |
|---|---|---|
| ⚡ Groq | Llama 3.3 70B | Free tier |
| 🤖 OpenAI | GPT-4o Mini | Pay-per-use |
| ✨ Gemini | Gemini 2.0 Flash | Free tier |

The app auto-detects which provider from your key prefix — no dropdown needed.

### UX
- Smooth onboarding screen before any key is entered
- Provider auto-detection with verify button
- Pro Mode toggle to unlock Deep Recommendations
- Keys stored in browser session only — never saved, never logged

---

## Screenshots

| Onboarding | Dashboard | AI Chat |
|---|---|---|
| Clean provider setup screen | KPI cards + pill-style tabs | ChatGPT-style bubbles |

| Sentiment Analysis | Report with Charts | PDF Export |
|---|---|---|
| Distribution bar + themes | Sections with inline charts | Branded cover + section cards |

---

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/sundusafreen/business-insight-generator.git
cd business-insight-generator
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate       # Mac/Linux
venv\Scripts\activate          # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Get a free API key

Pick any one provider:

- **Groq (recommended)** → [console.groq.com/keys](https://console.groq.com/keys) — free, fastest
- **Gemini** → [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey) — free tier
- **OpenAI** → [platform.openai.com/api-keys](https://platform.openai.com/api-keys) — pay-per-use

### 5. Run the app
```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501), paste your API key in the sidebar, and upload a dataset.

---

## Deployment (Streamlit Cloud)

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your repo
3. Set `app.py` as the main file
4. Deploy — no secrets needed (users bring their own keys)

> Your app URL will look like: `your-repo-name.streamlit.app`

---

## Project Structure

```
business-insight-generator/
├── app.py                  # Main application — all features in one file
├── requirements.txt        # Python dependencies
├── data.csv                # Sample sales dataset
└── README.md
```

---

## Dependencies

```
streamlit           # Web UI framework
pandas              # Data loading and manipulation
groq                # Groq API client (Llama 3.3)
openai              # OpenAI API client (GPT-4o Mini)
google-generativeai # Gemini API client
python-dotenv       # Environment variable loading
python-docx         # Word document export
reportlab           # PDF export
openpyxl            # Excel file support
matplotlib          # Chart rendering (correlation heatmap)
```

---

## How to Update Your Code

Every time you make a change to `app.py`:

```bash
git add .
git commit -m "describe what you changed"
git push
```

Streamlit Cloud auto-redeploys within ~1 minute.

---

## How It Works

```
User uploads CSV/Excel
        ↓
Auto KPI generation + schema detection
        ↓
Sentiment data detected? → Show Sentiment tab
        ↓
User asks question → AI receives dataset context + conversation history
        ↓
User generates report → AI returns structured sections
        ↓
Charts auto-inserted after each relevant section
        ↓
Export as Markdown / Word / PDF
```

---

## Roadmap

- [ ] Multi-file comparison reports
- [ ] Scheduled report delivery via email
- [ ] Custom branding (logo, company name)
- [ ] Database connectors (PostgreSQL, BigQuery)
- [ ] Save and load past reports

---

## Built With

- [Streamlit](https://streamlit.io) — UI framework
- [Groq](https://groq.com) — Ultra-fast LLM inference
- [Llama 3.3 70B](https://ai.meta.com/blog/meta-llama-3/) — Meta's open-source LLM
- [ReportLab](https://www.reportlab.com) — PDF generation
- [python-docx](https://python-docx.readthedocs.io) — Word document generation

---

## License

MIT License — free to use, modify, and distribute.

---

## Author

**Sundus Afreen**
- GitHub: [@sundusafreen](https://github.com/sundusafreen)

---

*Built as part of an AI engineering portfolio project — from zero to production in one session.*# InsightIQ — AI Business Decision Engine

> Upload any sales or business dataset. Get instant KPIs, 
> visualisations, and an AI analyst you can ask questions 
> in plain English. Export a full business report in minutes.

**[Try it live](https://business-insight-generator-iznknezr5a6nf55athdudq.streamlit.app/)**
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
GROQ_API_KEY=your_key_here

Get a free key at [console.groq.com](https://console.groq.com)

**Disclaimer:** "The live demo uses Groq's free API tier — if you hit a rate limit, try again in a minute or run locally with your own key." 

**4. Run**
```bash
streamlit run app.py
```

---

## Project Context

Built during my MSc in Business Analytics at Trinity College 
Dublin. The core design question was: *how do you make 
commercial data analysis accessible to the people who 
actually make the decisions — not just the people who 
write the queries?*

The industry mode system came from noticing that a retail 
analyst and a SaaS analyst care about completely different 
metrics. Rather than one generic AI prompt, InsightIQ 
switches the analytical lens based on your business context.

---

## Author

**Sundus Afreen**  
MSc Business Analytics — Trinity College Dublin  
AI & Analytics Consulting — EY Ireland  
[LinkedIn](https://www.linkedin.com/in/sundusafreen21/) · 
[Portfolio](https://sa-personall-portfolio.netlify.app/)
