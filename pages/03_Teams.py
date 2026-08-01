from __future__ import annotations

import pandas as pd
import streamlit as st

from src import charts
from src.page import bootstrap
from src.ui import explain_card, page_intro, render_brand_header, render_footer, section_heading
from src.utils import make_standings


data, _ = bootstrap("Teams")
fm = data["matches_filtered"]
teams = data["teams_filtered"]

render_brand_header("TEAM INTELLIGENCE • STRENGTH & FORM", "Find the teams behind the headlines.", "Blend pre-tournament pedigree with observed scoring output and group-stage performance to see which teams look strongest.", ["FIFA rank", "ELO", "Form"])
page_intro("Teams Intelligence", "This page is for questions like: who entered the tournament highly rated, who is actually producing goals, and what does the group table say about performance?", "Use the left chart for ranking pedigree, the scatter for the ELO/scoring relationship, then read the group tables for points, goal difference and record.")
explain_card("Why use both FIFA rank and ELO?", "They are different signals. FIFA rank is a pre-tournament external ranking; ELO is a rating of relative strength. The dashboard pairs them with observed goals so you can compare expectations with output.", [("FIFA rank", "Lower number means a stronger pre-tournament position."), ("ELO", "Relative strength score from the project data."), ("Goals / match", "Observed scoring production in the filtered matches.")])

performance: list[list[object]] = []
for _, team in teams.iterrows():
    matches = fm[(fm.home_team_id == team.team_id) | (fm.away_team_id == team.team_id)]
    goals_for = matches.loc[matches.home_team_id == team.team_id, "home_score"].sum() + matches.loc[matches.away_team_id == team.team_id, "away_score"].sum()
    performance.append([team.team_id, team.team_name, team.fifa_code, team.confederation, team.fifa_ranking_pre_tournament, team.elo_rating, goals_for, len(matches), goals_for / len(matches) if len(matches) else 0])

team_view = pd.DataFrame(performance, columns=["team_id", "team_name", "fifa_code", "confederation", "fifa_rank", "elo_rating", "goals", "matches_played", "goals_per_match"])

left, right = st.columns(2)
with left: st.plotly_chart(charts.team_rankings(teams), use_container_width=True, config={"displayModeBar": False})
with right: st.plotly_chart(charts.team_scatter(team_view), use_container_width=True, config={"displayModeBar": False})

section_heading("Group Stage table", "Points, wins, draws, losses and goal difference calculated from the cleaned match records.")
standings = make_standings(fm, teams, "Group Stage")
if standings.empty:
    st.info("No group-stage rows under the active filters.")
else:
    for group in sorted(standings.Group.unique()):
        st.markdown(f"**Group {group}**")
        st.dataframe(standings[standings.Group == group][["Team", "MP", "W", "D", "L", "GF", "GA", "GD", "Pts", "FIFA Rank", "ELO"]], hide_index=True, use_container_width=True)

render_footer()
