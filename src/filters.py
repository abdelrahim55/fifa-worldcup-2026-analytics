from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any

import pandas as pd
import streamlit as st


@dataclass(frozen=True)
class FilterState:
    confederations: tuple[str, ...]
    stages: tuple[str, ...]
    teams: tuple[str, ...]
    start_date: date
    end_date: date


def _options(df: pd.DataFrame, column: str) -> list[str]:
    return sorted(df[column].dropna().astype(str).unique().tolist())


def _normalize_date_input(value: Any, minimum: date, maximum: date) -> tuple[date, date]:
    if isinstance(value, (list, tuple)):
        if len(value) >= 2:
            start, end = value[0], value[1]
        elif len(value) == 1:
            start = end = value[0]
        else:
            start, end = minimum, maximum
    else:
        start = end = value or minimum

    start = start or minimum
    end = end or maximum
    if start > end:
        start, end = end, start
    return start, end


def render_global_filters(data: dict[str, pd.DataFrame]) -> FilterState:
    teams = data["teams"]
    matches = data["matches_enriched"]

    with st.sidebar:
        st.markdown('<div class="brand-lockup"><div class="brand-ball">⚽</div><div><div class="brand-name">WORLD CUP 26</div><div class="brand-tag">Analytics newsroom</div></div></div>', unsafe_allow_html=True)
        st.divider()

        confederations = st.multiselect(
            "Confederation",
            _options(teams, "confederation"),
            key="filter_confederations",
        )
        stages = st.multiselect(
            "Stage",
            _options(matches, "stage_name"),
            key="filter_stages",
        )
        selected_teams = st.multiselect(
            "Teams",
            _options(teams, "team_name"),
            key="filter_teams",
        )

        minimum = matches["date"].min().date()
        maximum = matches["date"].max().date()
        raw_dates = st.date_input(
            "Date range",
            value=(minimum, maximum),
            min_value=minimum,
            max_value=maximum,
            key="filter_dates",
        )
        start_date, end_date = _normalize_date_input(raw_dates, minimum, maximum)

        st.divider()
        st.caption("Tip: every page respects the active filters.")

    return FilterState(
        confederations=tuple(confederations),
        stages=tuple(stages),
        teams=tuple(selected_teams),
        start_date=start_date,
        end_date=end_date,
    )


def filter_data(data: dict[str, pd.DataFrame], state: FilterState) -> dict[str, pd.DataFrame]:
    teams = data["teams"].copy()
    matches = data["matches_enriched"].copy()
    players = data["players_enriched"].copy()
    team_stats = data["team_stats_enriched"].copy()

    active_team_ids = set(teams["team_id"])
    if state.confederations:
        active_team_ids &= set(
            teams.loc[teams["confederation"].isin(state.confederations), "team_id"]
        )
    if state.teams:
        active_team_ids &= set(
            teams.loc[teams["team_name"].isin(state.teams), "team_id"]
        )

    mask = matches["home_team_id"].isin(active_team_ids) | matches["away_team_id"].isin(active_team_ids)
    if state.confederations or state.teams:
        matches = matches.loc[mask]

    if state.stages:
        matches = matches[matches["stage_name"].isin(state.stages)]

    matches = matches[
        (matches["date"].dt.date >= state.start_date)
        & (matches["date"].dt.date <= state.end_date)
    ]

    if state.teams:
        matches = matches[
            matches["home_team"].isin(state.teams) | matches["away_team"].isin(state.teams)
        ]
        players = players[players["team_name"].isin(state.teams)]
        team_stats = team_stats[team_stats["team_name"].isin(state.teams)]
    elif state.confederations:
        team_stats = team_stats[team_stats["team_id"].isin(active_team_ids)]
        players = players[players["team_id"].isin(active_team_ids)]

    return {
        **data,
        "teams_filtered": teams[teams["team_id"].isin(active_team_ids)].copy()
        if (state.confederations or state.teams)
        else teams,
        "matches_filtered": matches,
        "players_filtered": players,
        "team_stats_filtered": team_stats,
    }
