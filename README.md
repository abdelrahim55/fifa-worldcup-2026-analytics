# ⚽ FIFA World Cup 2026 Analytics

> A football analytics project that combines data cleaning, exploratory analysis, feature engineering and an interactive Streamlit newsroom.

![Python](https://img.shields.io/badge/python-3.11%2B-1f425f.svg)
![Streamlit](https://img.shields.io/badge/streamlit-app-16c47f.svg)

## What this project does

This repository contains the **full analytical workflow**, not just the dashboard.

The project keeps the original raw datasets and analysis notebooks, preserves the processed analytical tables, and adds an interactive Streamlit dashboard with a football-focused visual design.

### Dashboard sections

| Section | What you can explore |
|---|---|
| **Overview** | Tournament KPIs, goals vs xG, outcomes, scoring distribution and latest results. |
| **Match Center** | Scorelines, xG, possession, shots, corners, event timeline and starting XI. |
| **Teams Intelligence** | FIFA rank, ELO, scoring output and group-stage tables. |
| **Player Lab** | Goals, assists, total contributions, efficiency and discipline. |
| **Squad & Venue Lab** | Starting-XI tactical mix and venue geography. |
| **Data & Methodology** | Data lineage, feature definitions and quality checks. |
| **SQL Analytics Lab** | Relational warehouse, reusable views and curated analytical SQL queries. |

## Repository structure

```text
FIFA_WorldCup_2026_Analytics/
├── app.py                         # Streamlit home / landing page
├── pages/                         # Streamlit multipage dashboard
│   ├── 01_Overview.py
│   ├── 02_Matches.py
│   ├── 03_Teams.py
│   ├── 04_Players.py
│   ├── 05_Lineups_and_Venues.py
│   ├── 06_Data_and_Methodology.py
│   └── 07_SQL_Analytics_Lab.py
├── src/                           # Reusable data, filters, UI and chart logic
│   ├── charts.py
│   ├── config.py
│   ├── data.py
│   ├── filters.py
│   ├── page.py
│   ├── theme.py
│   ├── ui.py
│   └── utils.py
├── data/
│   ├── raw/                       # Original source datasets
│   ├── processed/                 # Notebook outputs used by the app
│   └── warehouse/                 # Generated SQLite warehouse (gitignored)
├── sql/                           # Relational schema, views and analytical query library
├── notebooks/                     # Original analysis workflow
├── scripts/                       # Maintenance helpers
├── tests/                         # Smoke tests for data + analytics helpers
├── docs/                          # Architecture and original project notes
├── .github/workflows/             # GitHub Actions quality checks
├── requirements.txt               # Runtime dependencies
├── requirements-dev.txt           # Runtime + test/lint dependencies
└── run_dashboard.*                # Convenience launchers
```

## Run locally

### Windows

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

Or double-click `run_dashboard.bat` after installing the dependencies.

### macOS / Linux

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

Or:

```bash
./run_dashboard.sh
```

Then open the local Streamlit URL shown in the terminal (normally `http://localhost:8501`).

## Development checks

```bash
python -m pip install -r requirements-dev.txt
pytest -q
python -m compileall -q app.py src pages scripts tests
ruff check app.py src pages scripts tests
```

GitHub Actions runs the same quality checks on pushes and pull requests.

## Data and methodology

The analytical lineage is intentionally visible:

```text
raw data → cleaning notebook → EDA / feature engineering → processed CSVs → Streamlit dashboard
```

The dashboard reads the processed datasets as its main analytical layer and enriches them with raw event, venue and referee tables. It does not overwrite project data at runtime.

The SQL layer adds a reproducible relational warehouse generated from the same raw source files. Run `python scripts/build_sqlite_warehouse.py` to materialize it, or use the **SQL Analytics Lab** page to execute the curated query library from Streamlit.

See [docs/architecture.md](docs/architecture.md) for the architecture and [notebooks/README.md](notebooks/README.md) for the notebook workflow.

## Publishing the repository

Before making the repository public, verify that every dataset is licensed for redistribution. If any raw data source is restricted, keep it outside the public repository and document the expected local path instead.

## License

The software in this repository is released under the MIT License. Dataset licenses and third-party sources may have separate terms; check their provenance before redistribution.

## 🎥 How to present the dashboard

For a short demo, a good order is: **Overview → Filters → Match Center → Teams → Player Lab → SQL Analytics Lab → Data & Methodology**.

A simple video walkthrough is available at `docs/video_demo_script.md`.

The UI uses a dark football theme with animated elements, KPI cards, match-focused sections and a dedicated SQL page.

## Deploy to Streamlit Community Cloud

This repository is prepared for Streamlit Community Cloud.

1. Push the repository to GitHub.
2. In Streamlit Community Cloud choose **Create app**.
3. Select the GitHub repository and the `main` branch.
4. Set the app file to `app.py`.
5. Deploy.

The app uses `requirements.txt` from the repository root. The SQL warehouse is generated automatically from the source CSV files when the SQL Analytics page is first used, so the generated `.db` file does not need to be committed.

Once deployed, the app will have a public `*.streamlit.app` URL that can be shared from desktop or mobile browsers.
