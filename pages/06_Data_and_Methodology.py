from __future__ import annotations

import pandas as pd
import streamlit as st

from src.page import bootstrap
from src.ui import explain_card, page_intro, render_brand_header, render_footer, section_heading


data, _ = bootstrap("Data & Methodology")

render_brand_header("DATA • METHODOLOGY • LINEAGE", "Every number has a trail back to the source.", "This page explains what feeds the dashboard, what is calculated in the notebooks, what is enriched at runtime and where SQL fits into the architecture.", ["Traceable", "Notebook-backed", "SQL warehouse"])
page_intro("Data & Methodology", "This page documents the data flow and the calculations used by the dashboard. Raw files, cleaned outputs, feature engineering and SQL are listed here.", "Start with the pipeline, then review the dataset sizes and finish with the SQL Analytics Lab.")
explain_card("The project pipeline", "The dashboard sits on top of the original analysis workflow and does not replace the notebooks. Processed CSVs provide the main tables, while selected raw tables add event, venue and referee context.", [("Raw", "Original CSV sources such as matches, events, venues and referees."), ("Notebooks", "Cleaning, EDA and feature-engineering workflow."), ("App + SQL", "Streamlit presentation plus a rebuildable analytical warehouse.")])

section_heading("Project lineage", "How the data moves through the project.")
st.markdown('''<div class="card" style="padding:22px;margin-bottom:15px;text-align:center;"><span class="badge">RAW</span><span style="margin:0 9px;color:#9aa9a3">→</span><span class="badge">CLEANED</span><span style="margin:0 9px;color:#9aa9a3">→</span><span class="badge">FEATURES</span><span style="margin:0 9px;color:#9aa9a3">→</span><span class="badge">SQL WAREHOUSE</span><span style="margin:0 9px;color:#9aa9a3">→</span><span class="badge">STREAMLIT</span><p style="margin:15px 0 0;color:#70817a;font-size:11px;line-height:1.7">The notebooks remain part of the repository. The processed outputs are consumed by the app, while the SQL layer rebuilds from source CSVs so the database is an explicit engineering artifact rather than a hidden binary dependency.</p></div>''', unsafe_allow_html=True)

left, middle, right = st.columns(3)
with left:
    st.markdown("### Notebooks")
    st.write("`01_Data_cleaning.ipynb` · `03_EDA.ipynb` · `03_Feature_Engineering.ipynb`")
with middle:
    st.markdown("### Processed layer")
    st.write(f"{len(data['teams']):,} teams · {len(data['matches']):,} matches · {len(data['players_enriched']):,} players · {len(data['lineups']):,} lineup rows")
with right:
    st.markdown("### Enrichment layer")
    st.write(f"{len(data['events_enriched']):,} events · {len(data['venues']):,} venues · {len(data['referees']):,} referees")

section_heading("Feature engineering carried into the dashboard")
st.markdown('''<div class="card"><p><b>Player:</b> total contributions, goals/assists per match, contribution per match, discipline score, minutes per goal/contribution and clean-sheet rate.</p><p><b>Match:</b> total goals, goal difference, result type, high-scoring flag, clean-sheet flag and both-teams-scored flag.</p><p style="margin-bottom:0"><b>Team-match:</b> shot accuracy, shots off target, save rate, fouls/corners/offsides per shot and aggressive play index.</p></div>''', unsafe_allow_html=True)

section_heading("Data quality snapshot", "Row counts across the tables currently used by the application.")
quality = pd.DataFrame({"Dataset":["teams","matches","players","lineups","team_match_stats","events","venues","referees"],"Rows":[len(data["teams"]),len(data["matches"]),len(data["players_enriched"]),len(data["lineups"]),len(data["team_stats_enriched"]),len(data["events_enriched"]),len(data["venues"]),len(data["referees"])]})
st.dataframe(quality, hide_index=True, use_container_width=True)

st.markdown('<div class="card" style="margin-top:15px"><b>Note:</b> “Every headline KPI is traceable to a dataset, and every derived metric is documented in the notebook/feature-engineering layer or the SQL views.”</div>', unsafe_allow_html=True)
render_footer()
