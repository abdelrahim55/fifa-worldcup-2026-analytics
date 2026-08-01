from __future__ import annotations

import pandas as pd


def fmt_num(value: float | None) -> str:
    if value is None or pd.isna(value):
        return "—"
    return f"{value:,.0f}"


def fmt_pct(value: float | None) -> str:
    if value is None or pd.isna(value):
        return "—"
    return f"{value:.1%}"


def money(value: float | None) -> str:
    if value is None or pd.isna(value):
        return "—"
    if value >= 1e9:
        return f"€{value / 1e9:.1f}B"
    if value >= 1e6:
        return f"€{value / 1e6:.1f}M"
    if value >= 1e3:
        return f"€{value / 1e3:.0f}K"
    return f"€{value:,.0f}"


def team_logo(team_name: str) -> str:
    initials = "".join(word[0] for word in str(team_name).split()[:2]).upper()
    return initials[:3]


def make_standings(matches: pd.DataFrame, teams: pd.DataFrame, stage: str = "Group Stage") -> pd.DataFrame:
    match_frame = matches[matches["stage_name"] == stage].copy()
    rows: list[list[object]] = []

    for _, team in teams.iterrows():
        home = match_frame[match_frame["home_team_id"] == team.team_id]
        away = match_frame[match_frame["away_team_id"] == team.team_id]
        goals_for = home["home_score"].sum() + away["away_score"].sum()
        goals_against = home["away_score"].sum() + away["home_score"].sum()
        wins = (
            (home["home_score"] > home["away_score"]).sum()
            + (away["away_score"] > away["home_score"]).sum()
        )
        draws = (
            (home["home_score"] == home["away_score"]).sum()
            + (away["away_score"] == away["home_score"]).sum()
        )
        played = len(home) + len(away)
        rows.append(
            [
                team.team_id,
                team.team_name,
                team.group_letter,
                played,
                wins,
                draws,
                played - wins - draws,
                goals_for,
                goals_against,
                goals_for - goals_against,
                wins * 3 + draws,
                team.fifa_ranking_pre_tournament,
                team.elo_rating,
            ]
        )

    return pd.DataFrame(
        rows,
        columns=[
            "team_id",
            "Team",
            "Group",
            "MP",
            "W",
            "D",
            "L",
            "GF",
            "GA",
            "GD",
            "Pts",
            "FIFA Rank",
            "ELO",
        ],
    ).sort_values(["Group", "Pts", "GD", "GF"], ascending=[True, False, False, False])
