from __future__ import annotations

import streamlit as st

from src import charts
from src.page import bootstrap
from src.ui import (
    explain_card,
    page_intro,
    render_brand_header,
    render_footer,
    section_heading,
)

data, _ = bootstrap("Players")
players = data["players_filtered"]

render_brand_header("PLAYER LAB • IMPACT METRICS", "Meet the players driving the numbers.", "Use contribution, efficiency, minutes and discipline metrics to move beyond raw goal totals.", ["Goals + assists", "Efficiency", "Discipline"])
page_intro("Player Lab", "This page ranks players by output and efficiency. It looks at both total production and rate-based measures such as contributions per match.", "Search a player, scan the contribution leaderboard, then compare goals and assists visually. Use the efficiency tables as a sanity check for rate-based performance.")
explain_card("What is contribution per match?", "It is a project-derived rate: total goals + assists divided by matches played. Rates are easier to compare than raw totals when players have different game counts.", [("Contributions", "Goals + assists."), ("Per match", "Contribution total divided by matches played."), ("Minutes / goal", "Minutes played divided by goals, for scorers.")])

query = st.text_input("Search player", placeholder="Type a player name…")
player_frame = players[players.player_name.str.contains(query, case=False, na=False)] if query else players.copy()

section_heading("Contribution leaderboard", "The main ranking: goals + assists, with minutes and project-derived rates alongside it.")
left, right = st.columns([1.4, 1])
with left:
    top = player_frame.sort_values(["total_contributions", "goals", "assists"], ascending=False).head(15)
    st.dataframe(top[["player_name", "team_name", "position", "matches_played", "minutes_played", "goals", "assists", "total_contributions", "contribution_per_match", "yellow_cards", "red_cards"]], hide_index=True, use_container_width=True)
with right:
    st.plotly_chart(charts.player_scatter(player_frame.head(300)), use_container_width=True, config={"displayModeBar": False})

section_heading("Efficiency leaders", "A 180-minute minimum is used here so tiny samples do not dominate the rate leaderboards.")
cols = st.columns(3)
with cols[0]: st.dataframe(player_frame[player_frame.minutes_played >= 180].sort_values("goals_per_match", ascending=False).head(10)[["player_name", "team_name", "goals_per_match"]], hide_index=True, use_container_width=True)
with cols[1]: st.dataframe(player_frame[player_frame.minutes_played >= 180].sort_values("assists_per_match", ascending=False).head(10)[["player_name", "team_name", "assists_per_match"]], hide_index=True, use_container_width=True)
with cols[2]: st.dataframe(player_frame[player_frame.minutes_played >= 180].sort_values("clean_sheet_rate", ascending=False).head(10)[["player_name", "team_name", "clean_sheet_rate"]], hide_index=True, use_container_width=True)

render_footer()
