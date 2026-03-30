import os
import time
import pandas as pd
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ── 1. Load Data ───────────────────────────────────────────
def load_data(csv_path):
    df = pd.read_csv(csv_path)
    print(f"✅ Loaded {len(df)} rows and {len(df.columns)} columns")
    print(f"   Columns: {list(df.columns)}\n")
    return df

# ── 2. Generate Report ─────────────────────────────────────
def generate_report(df, report_type="executive summary", custom_focus=""):
    print(f"⏳ Generating {report_type} report...")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are an elite business intelligence analyst. Structure reports with: Data Overview, Key Findings, Trend Analysis, Risk Signals, Recommendations, Executive Takeaway."
            },
            {
                "role": "user",
                "content": f"""Generate a {report_type} report.
Stats:
{df.describe().round(1).to_string()}
{f'Focus: {custom_focus}' if custom_focus else ''}"""
            }
        ]
    )
    return response.choices[0].message.content

# ── 3. Save Report ─────────────────────────────────────────
def save_report(report, filename="report_output.md"):
    with open(filename, "w") as f:
        f.write(report)
    print(f"✅ Report saved to {filename}")

# ── 4. Run ─────────────────────────────────────────────────
if __name__ == "__main__":
    CSV_FILE    = "data.csv"
    REPORT_TYPE = "executive summary"
    FOCUS       = "Focus on regional performance gaps"

    df     = load_data(CSV_FILE)
    report = generate_report(df, REPORT_TYPE, FOCUS)

    print("\n" + "="*60)
    print(report)
    print("="*60 + "\n")

    save_report(report)