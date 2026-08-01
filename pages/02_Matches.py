from __future__ import annotations

import pandas as pd
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

data, _ = bootstrap("Matches")
fm = data["matches_filtered"]
teams = data["teams"]
events = data["events_enriched"]
team_stats = data["team_stats_enriched"]
players = data["players_enriched"]

render_brand_header("MATCHDAY • DEEP DIVE", "Every match has more detail than the final score.", "Move from the headline score into xG, possession, shots, corners, referee context, events and the starting XI.", ["Match Center", "Event timeline", "Lineups"])
page_intro("Match Center", "This page answers why a match looked the way it did. The final score is the headline; the comparison chart and event timeline explain the process behind it.", "Pick a match, scan the score and ranking context, compare the performance bars, then scroll to events and the starting XI.")
explain_card("How to interpret the match comparison", "Goals are outcomes. xG is chance quality. Shots and shots on target show volume and accuracy, while possession and corners describe control and territorial pressure.", [("xG", "Expected goals — estimated scoring quality of chances."), ("Possession", "Share of ball control in the match stats layer."), ("Events", "Recorded match events joined to players and teams.")])

if fm.empty:
    st.warning("No matches match the active filters.")
    st.stop()

options = fm.sort_values("date", ascending=False).match_id.tolist()
pick = st.selectbox("Select match", options, format_func=lambda match_id: f"#{match_id} • {fm.loc[fm.match_id.eq(match_id), 'home_team'].iloc[0]} vs {fm.loc[fm.match_id.eq(match_id), 'away_team'].iloc[0]}")
row = fm[fm.match_id.eq(pick)].iloc[0]
team_rows = team_stats[team_stats.match_id.eq(pick)]
home_stats = team_rows[team_rows.team_id.eq(row.home_team_id)].iloc[0]
away_stats = team_rows[team_rows.team_id.eq(row.away_team_id)].iloc[0]
home_rank = int(teams.loc[teams.team_id.eq(row.home_team_id), "fifa_ranking_pre_tournament"].iloc[0])
away_rank = int(teams.loc[teams.team_id.eq(row.away_team_id), "fifa_ranking_pre_tournament"].iloc[0])

st.markdown(f'''<div class="match-card" style="margin-bottom:15px;"><div class="muted">{row.stage_name} • {row.date:%A, %d %B %Y} • {row.stadium_name}</div><div style="display:flex;justify-content:space-between;align-items:center;padding:17px 0;gap:24px;"><div><div class="team">{row.home_team}</div><div class="muted">FIFA #{home_rank}</div></div><div style="text-align:center"><div class="score">{row.home_score} — {row.away_score}</div><span class="badge" style="margin-top:7px">{row.result_type}</span></div><div style="text-align:right"><div class="team">{row.away_team}</div><div class="muted">FIFA #{away_rank}</div></div></div><span class="badge badge--dark">Referee: {row['name']} • Avg cards {row.avg_cards_per_game}</span></div>''', unsafe_allow_html=True)

match_object = type("MatchSummary", (), {})()
for key, value in {"home_team": row.home_team, "away_team": row.away_team, "home_score": row.home_score, "away_score": row.away_score, "home_xg": row.home_xg, "away_xg": row.away_xg, "home_shots": home_stats.total_shots, "away_shots": away_stats.total_shots, "home_sot": home_stats.shots_on_target, "away_sot": away_stats.shots_on_target, "home_poss": home_stats.possession_pct, "away_poss": away_stats.possession_pct, "home_corners": home_stats.corners, "away_corners": away_stats.corners}.items():
    setattr(match_object, key, value)

st.plotly_chart(charts.xg_match(match_object), use_container_width=True, config={"displayModeBar": False})

event_frame = events[events.match_id.eq(pick)].copy()
event_frame["minute_num"] = pd.to_numeric(event_frame.minute.astype(str).str.extract(r"(\d+)")[0], errors="coerce").fillna(0)
st.plotly_chart(charts.event_timeline(event_frame), use_container_width=True, config={"displayModeBar": False})

section_heading("Starting XI", "Lineup records show who started, their tactical position and minutes played.")
lineup = data["lineups"][data["lineups"].match_id.eq(pick)].merge(players[["player_id", "player_name"]], on="player_id", how="left")
left, right = st.columns(2)
with left:
    st.markdown(f"**{row.home_team}**")
    st.dataframe(lineup[(lineup.team_id == row.home_team_id) & (lineup.is_starting_xi == 1)][["player_name", "tactical_position", "minutes_played"]], hide_index=True, use_container_width=True)
with right:
    st.markdown(f"**{row.away_team}**")
    st.dataframe(lineup[(lineup.team_id == row.away_team_id) & (lineup.is_starting_xi == 1)][["player_name", "tactical_position", "minutes_played"]], hide_index=True, use_container_width=True)

render_footer()
