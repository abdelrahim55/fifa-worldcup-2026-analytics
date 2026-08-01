from __future__ import annotations

import streamlit as st

from src.config import APP_ICON, APP_TITLE
from src.data import load_data
from src.filters import render_global_filters
from src.theme import apply_theme
from src.ui import render_brand_header, render_footer, render_site_nav, render_ticker

st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout="wide", initial_sidebar_state="collapsed")
apply_theme()
render_site_nav("Overview")
render_ticker()

data = load_data()
render_global_filters(data)

render_brand_header(
    "WORLD CUP 26 • FOOTBALL INTELLIGENCE",
    "World Cup analytics, match by match.",
    "An interactive dashboard built from the project's cleaning, EDA, feature-engineering and SQL work.",
    ["Interactive newsroom", "Notebook-backed", "SQL warehouse"],
)

st.markdown(
    '''
    <div class="home-grid">
      <div class="feature-card feature-card--wide">
        <span class="feature-kicker">START HERE</span>
        <h3>Overview</h3>
        <p>Read the tournament pulse first: goals, xG, results, scoring trends, confederations and the latest scorelines.</p>
        <div class="feature-arrow">→</div>
      </div>
      <div class="feature-card"><span class="feature-kicker">MATCHDAY</span><h3>Match Center</h3><p>Pick a match and explain the score using xG, possession, shots, corners and event timelines.</p><div class="feature-arrow">→</div></div>
      <div class="feature-card"><span class="feature-kicker">TEAMS</span><h3>Teams Intelligence</h3><p>Compare FIFA ranking, ELO, goal production and group-stage standings to understand team strength.</p><div class="feature-arrow">→</div></div>
      <div class="feature-card"><span class="feature-kicker">PLAYERS</span><h3>Player Lab</h3><p>Find the players driving results through goals, assists, contribution rate and efficiency metrics.</p><div class="feature-arrow">→</div></div>
      <div class="feature-card"><span class="feature-kicker">SQL</span><h3>Analytics Lab</h3><p>Explore the warehouse and SQL queries using CTEs, window functions, ranking and reusable views.</p><div class="feature-arrow">→</div></div>
      <div class="feature-card"><span class="feature-kicker">METHOD</span><h3>Data & Methodology</h3><p>See how the raw CSVs move through cleaning, EDA and feature engineering before they reach the dashboard.</p><div class="feature-arrow">→</div></div>
    </div>
    ''', unsafe_allow_html=True
)

st.markdown('<div class="section-title">Project snapshot</div><div class="section-subtitle">These are the objects the dashboard can explain — not just decorative counters.</div>', unsafe_allow_html=True)
cols = st.columns(4)
summary = [
    ("Teams", len(data["teams"]), "competition field"),
    ("Matches", len(data["matches"]), "cleaned match records"),
    ("Players", len(data["players_enriched"]), "feature-engineered player rows"),
    ("Events", len(data["events_enriched"]), "event layer records"),
]
for col, (label, value, note) in zip(cols, summary):
    with col:
        st.markdown(f'<div class="mini-stat"><div class="mini-stat__value">{value:,}</div><div class="mini-stat__label">{label}</div><div class="mini-stat__note">{note}</div></div>', unsafe_allow_html=True)

st.markdown('<div class="page-intro" style="margin-top:15px;"><div class="page-intro__main"><div class="page-intro__eyebrow">VIDEO WALKTHROUGH</div><div class="page-intro__title">A practical route through the dashboard.</div><div class="page-intro__text">Start with Overview, apply a team filter, open a match in Match Center, then look at Teams, Players and the SQL page. The full walkthrough is in docs/video_demo_script.md.</div></div><div class="page-intro__how"><strong>SUGGESTED ORDER</strong><p>Overview → Filters → Match Center → Teams → Players → SQL → Methodology.</p></div></div>', unsafe_allow_html=True)
render_footer()
