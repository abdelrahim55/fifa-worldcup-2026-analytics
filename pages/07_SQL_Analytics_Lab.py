from __future__ import annotations

import streamlit as st

from src.page import bootstrap
from src.sql import WAREHOUSE, list_queries, load_query, run_sql
from src.ui import explain_card, page_intro, render_brand_header, render_footer, section_heading

bootstrap("SQL")

render_brand_header("SQL • ANALYTICS ENGINE", "The dashboard's analytical engine is queryable.", "This page contains the SQLite warehouse, reusable views and the main analytical SQL queries.", ["Warehouse", "CTEs", "Window functions"])
page_intro("SQL Analytics Lab", "Use this page to inspect the SQL used by the project. Each query is stored in the repository, executed against the warehouse and shown with its result.", "Pick a query, read through the SQL, run it and compare the result with the dashboard metrics.")
explain_card("What makes this SQL layer strong?", "The warehouse separates dimensions from facts, the views standardize reusable summaries, and the query library demonstrates analytical SQL rather than simple SELECT statements.", [("CTEs", "Break complex logic into readable stages."), ("Windows", "Rank teams/players without losing row-level detail."), ("Views", "Create reusable business-ready analytical tables.")])

queries = list_queries()
if not WAREHOUSE.exists():
    st.info("The SQLite warehouse is generated from the source CSVs the first time a query is executed.")

labels = {"01_team_power_ranking":"Team Power Ranking","02_player_efficiency":"Player Efficiency","03_xg_overperformance":"xG Overperformance","04_recent_form":"Recent Form","05_possession_vs_results":"Possession vs Results","06_venue_impact":"Venue Impact","07_referee_discipline":"Referee Discipline","08_starting_xi_impact":"Starting XI Impact"}
left, right = st.columns([.95, 1.7])
with left:
    section_heading("Query library", "Curated questions that look like actual analyst requests.")
    selected = st.selectbox("Analytics question", list(queries), format_func=lambda x: labels.get(x, x.replace("_", " ").title()))
    st.markdown('<div class="card" style="margin-top:10px"><b>Why this matters:</b><p style="font-size:10px;color:#74818f;line-height:1.6;margin:6px 0 0">Open this page after the main dashboard to show how the same data can be queried from the relational model.</p></div>', unsafe_allow_html=True)
with right:
    section_heading("SQL", "The exact query lives in `sql/queries/` and is therefore reviewable on GitHub.")
    query = load_query(selected)
    st.code(query, language="sql")

if st.button("Run selected query", type="primary", use_container_width=True):
    try:
        result = run_sql(query)
        section_heading("Result", f"{len(result):,} rows returned from the SQL warehouse.")
        st.dataframe(result, hide_index=True, use_container_width=True)
    except Exception as exc:
        st.error(f"SQL execution failed: {exc}")

st.markdown('''<div class="card" style="margin-top:16px"><b>Warehouse design</b><p style="font-size:10px;color:#74818f;line-height:1.6;margin:7px 0 0"><b>Dimensions:</b> teams, players, stages, venues, referees. <b>Facts:</b> matches, player stats, team-match stats, lineups, events. <b>Analytics:</b> reusable views + CTEs + window functions + ranking + statistical comparisons.</p></div>''', unsafe_allow_html=True)
render_footer()
