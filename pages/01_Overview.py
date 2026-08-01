from __future__ import annotations

import streamlit as st

from src import charts
from src.page import bootstrap
from src.ui import (
    explain_card,
    kpi_card,
    page_intro,
    render_brand_header,
    render_footer,
    section_heading,
)
from src.utils import fmt_num

data, filters = bootstrap("Overview")
fm = data["matches_filtered"]
fp = data["players_filtered"]
teams = data["teams_filtered"]

render_brand_header(
    "TOURNAMENT PULSE • THE FRONT PAGE",
    "Read the World Cup like a sports desk.",
    "This is the executive view: the fastest way to understand scoring, chance quality, outcomes and who is driving the tournament narrative.",
    ["Start here", "Global filters", "Live calculations"],
)
page_intro(
    "Overview",
    "Use this page to answer: how much football are we seeing, how are goals comparing with chance quality (xG), what types of results dominate, and which teams/players deserve a deeper look?",
    "Read the KPI row first, then use the two charts to spot a trend. Finish with the latest results and open Match Center when one scoreline catches your eye.",
)
explain_card(
    "What do the headline numbers mean?",
    "The KPI cards are recalculated from the active filters, so the values update when you change the competition, stage, team or date range.",
    [("Goals", "Total home + away goals across filtered matches."), ("xG", "Expected-goal estimate summed across both teams."), ("Top scorer", "Leader by recorded goals in the filtered player layer.")],
)

goals = int(fm.total_goals.sum()) if len(fm) else 0
avg_goals = float(fm.total_goals.mean()) if len(fm) else 0
avg_xg = float((fm.home_xg + fm.away_xg).mean()) if len(fm) else 0
top_scorer = fp.sort_values(["goals", "assists"], ascending=False).iloc[0].player_name if len(fp) else "—"
cols = st.columns(4)
for col, html in zip(cols, [
    kpi_card("Matches", fmt_num(len(fm)), f"of {len(data['matches']):,} tournament records"),
    kpi_card("Goals", fmt_num(goals), f"{avg_goals:.2f} per match"),
    kpi_card("Avg xG / match", f"{avg_xg:.2f}", "chance quality estimate"),
    kpi_card("Top scorer", str(top_scorer), "recorded goals", "dark"),
]):
    with col: st.markdown(html, unsafe_allow_html=True)

left, right = st.columns([1.6, 1])
with left: st.plotly_chart(charts.goals_xg(fm), use_container_width=True, config={"displayModeBar": False})
with right: st.plotly_chart(charts.results_donut(fm), use_container_width=True, config={"displayModeBar": False})

left, right = st.columns(2)
with left: st.plotly_chart(charts.goals_distribution(fm), use_container_width=True, config={"displayModeBar": False})
with right: st.plotly_chart(charts.confederations(teams), use_container_width=True, config={"displayModeBar": False})

section_heading("Latest results", "Use these as the bridge from the tournament overview into Match Center.")
if fm.empty:
    st.warning("No matches match the active filters.")
else:
    for _, row in fm.sort_values("date", ascending=False).head(6).iterrows():
        st.markdown(f'''<div class="match-card" style="margin-bottom:9px;"><div style="display:flex;justify-content:space-between;align-items:center;gap:20px;"><div><div class="team">{row.home_team} <span class="muted">vs</span> {row.away_team}</div><div class="muted">{row.stage_name} • {row.date:%d %b %Y} • {row.stadium_name}</div></div><div class="score">{row.home_score} — {row.away_score}</div><span class="badge">{row.result_type}</span></div></div>''', unsafe_allow_html=True)

render_footer()
