# FIFA World Cup 2026 Analytics — Interactive Streamlit Dashboard

This repository keeps the original analytics project intact and adds a Streamlit dashboard on top of it.

## Project structure

- `data/raw/` — original source datasets, including matches, events, venues, referees, lineups and prediction features.
- `data/processed/` — cleaned datasets consumed by the dashboard.
- `notebooks/` — original analysis workflow: data cleaning, EDA and feature engineering.
- `src/` — reusable data loading, feature enrichment, theme and chart helpers.
- `app.py` — Streamlit dashboard.
- `scripts/` — small maintenance helpers.

## Run locally

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

The dashboard includes:

1. Overview — tournament KPIs, goals vs xG, outcomes, latest results.
2. Matches — Match Center with xG, possession, shots, event timeline and starting XI.
3. Teams — group tables, FIFA rank, ELO and scoring output.
4. Players — contribution leaders and feature-engineered efficiency metrics.
5. Lineups & Venues — tactical positions and venue map.
6. Data & Methodology — project lineage and data-quality snapshot.

## Design principles

The dashboard does not replace the notebooks. The notebooks remain the analysis source, processed CSVs remain the primary dashboard input, and raw event/venue/referee data enrich the presentation layer.
