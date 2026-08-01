from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "app.py",
    "requirements.txt",
    ".streamlit/config.toml",
    "src/data.py",
    "src/page.py",
    "pages/01_Overview.py",
    "pages/07_SQL_Analytics_Lab.py",
    "data/raw/teams.csv",
    "data/processed/teams_clean.csv",
    "sql/schema.sql",
    "sql/views.sql",
]

missing = [p for p in REQUIRED if not (ROOT / p).exists()]
if missing:
    raise SystemExit("Missing deploy files:\n" + "\n".join(missing))

print(f"Deployment package check passed: {len(REQUIRED)} required paths present.")
