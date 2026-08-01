from __future__ import annotations

import streamlit as st

from src import charts
from src.page import bootstrap
from src.ui import explain_card, page_intro, render_brand_header, render_footer, section_heading


data, _ = bootstrap("Lineups & Venues")
teams = data["teams_filtered"]
players = data["players_enriched"]
lineups = data["lineups"]
venues = data["venues"]

render_brand_header("SQUADS & VENUES • TOURNAMENT FOOTPRINT", "See how the competition is assembled.", "Inspect starting-XI patterns, tactical positions and the physical footprint of the venues hosting the tournament.", ["Starting XI", "Tactical mix", "Venue map"])
page_intro("Squads & Venues", "This section combines squad composition with venue context. It is intentionally different from the result pages: it explains who is on the pitch and where the competition is being played.", "Start with a team, inspect the tactical mix, then switch to Venues to explore stadium location, capacity and elevation.")
explain_card("What is a tactical position?", "The lineup data maps each player to a broad tactical bucket — goalkeeper, defender, midfielder or forward — so the dashboard can summarize the shape of a starting XI without pretending to reconstruct every formation detail.", [("Starting XI", "Players marked as starting in the lineup dataset."), ("Minutes", "Recorded minutes played."), ("Venue capacity", "Reported stadium capacity from raw venue data.")])

lineup_tab, venue_tab = st.tabs(["Lineups", "Venues"])
with lineup_tab:
    section_heading("Formation explorer", "Select a team to inspect its starting-XI tactical mix.")
    if teams.empty:
        st.info("No teams match the active filters.")
    else:
        team_pick = st.selectbox("Team", teams.team_name.sort_values().tolist())
        team_id = int(teams.loc[teams.team_name.eq(team_pick), "team_id"].iloc[0])
        lineup_frame = lineups[lineups.team_id.eq(team_id)]
        st.plotly_chart(charts.formation(lineup_frame, players, team_id), use_container_width=True, config={"displayModeBar": False})
        joined = lineup_frame.merge(players[["player_id", "player_name", "position"]], on="player_id", how="left")
        st.dataframe(joined[["match_id", "player_name", "position", "tactical_position", "is_starting_xi", "minutes_played"]].sort_values(["match_id", "is_starting_xi"], ascending=[True, False]), hide_index=True, use_container_width=True)
with venue_tab:
    section_heading("Venue map", "Location, capacity and elevation from the raw venue dataset.")
    st.plotly_chart(charts.venue_map(venues), use_container_width=True, config={"displayModeBar": False})
    st.dataframe(venues.rename(columns={"stadium_name":"Stadium", "city":"City", "country":"Country", "capacity":"Capacity", "elevation_meters":"Elevation (m)"}), hide_index=True, use_container_width=True)

render_footer()
