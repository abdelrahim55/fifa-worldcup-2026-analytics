# Architecture

```text
                         ┌─────────────────────────────┐
                         │        data/raw/*.csv       │
                         └─────────────┬───────────────┘
                                       │
                                       ▼
                         ┌─────────────────────────────┐
                         │      notebooks/*.ipynb      │
                         │ cleaning → EDA → features   │
                         └─────────────┬───────────────┘
                                       │
                                       ▼
                    ┌──────────────────────────────────────┐
                    │       data/processed/*.csv            │
                    │   dashboard-ready analytical layer    │
                    └──────────────────┬───────────────────┘
                                       │
                                       ▼
              ┌─────────────────────────────────────────────────┐
              │              Streamlit presentation              │
              │ app.py + pages/* + src/data.py + src/charts.py  │
              └─────────────────────────────────────────────────┘
```

## Design rules

1. **Notebooks own the analysis history.** Feature definitions should be traceable to the notebook workflow.
2. **Processed CSVs are the dashboard's primary input.** Raw event/venue/referee tables are used for enrichment.
3. **UI code is separated from data logic.** `src/` contains reusable modules; `pages/` contains page-specific presentation.
4. **The application is read-only at runtime.** It loads data and computes in-memory enrichments without rewriting project datasets.
5. **Quality checks run in CI.** Python compilation, tests and Ruff linting are part of the GitHub workflow.

## SQL warehouse layer

The repository now includes a reproducible SQLite warehouse between the source CSV layer and the optional SQL Analytics Lab in Streamlit.

```text
Raw CSVs -> SQLite schema -> reusable SQL views -> curated analytical queries -> Streamlit SQL Analytics Lab
```

The warehouse is deliberately generated, not committed, so the project remains transparent and reproducible.

## Presentation layer

The Streamlit interface is intentionally styled like a football newsroom rather than a default BI dashboard. The visual language uses a dark navy editorial palette with green/cyan highlights, animated hero shapes, a live ticker, card hover states and a clear “what am I looking at / how to read it” explainer block on major pages.

For a recorded demo, follow `docs/video_demo_script.md`.
