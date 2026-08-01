from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


@st.cache_data(show_spinner=False)
def _read_csv(path: Path, **kwargs: object) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing dataset: {path}")
    return pd.read_csv(path, **kwargs)


@st.cache_data(show_spinner="Loading project datasets…")
def load_data() -> dict[str, pd.DataFrame]:
    """Load processed dashboard datasets and raw enrichment tables."""
    data = {
        "teams": _read_csv(DATA / "processed/teams_clean.csv"),
        "matches": _read_csv(DATA / "processed/matches_clean.csv", parse_dates=["date"]),
        "players": _read_csv(DATA / "processed/player_stats_clean.csv"),
        "squads": _read_csv(DATA / "processed/squads_and_players_clean.csv", parse_dates=["date_of_birth"]),
        "lineups": _read_csv(DATA / "processed/lineups_clean.csv"),
        "team_stats": _read_csv(DATA / "processed/team_match_stats_clean.csv"),
        "events": _read_csv(DATA / "raw/match_events.csv"),
        "stages": _read_csv(DATA / "raw/tournament_stages.csv"),
        "venues": _read_csv(DATA / "raw/venues.csv"),
        "referees": _read_csv(DATA / "raw/referees.csv"),
        "detailed_matches": _read_csv(DATA / "raw/matches_detailed.csv", parse_dates=["date"]),
        "prediction_features": _read_csv(DATA / "raw/match_prediction_features.csv", parse_dates=["date"]),
    }
    return enrich(data)


def enrich(data: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    teams = data["teams"]
    matches = data["matches"]
    players = data["players"]
    squads = data["squads"]
    data["lineups"]
    team_stats = data["team_stats"]
    events = data["events"]
    stages = data["stages"]
    venues = data["venues"]
    referees = data["referees"]

    team_names = teams.set_index("team_id")["team_name"].to_dict()

    enriched_matches = matches.copy()
    enriched_matches["home_team"] = enriched_matches["home_team_id"].map(team_names)
    enriched_matches["away_team"] = enriched_matches["away_team_id"].map(team_names)
    enriched_matches["total_goals"] = enriched_matches["home_score"] + enriched_matches["away_score"]
    enriched_matches["goal_difference"] = (
        enriched_matches["home_score"] - enriched_matches["away_score"]
    ).abs()
    enriched_matches["match_result"] = np.select(
        [
            enriched_matches["home_score"] > enriched_matches["away_score"],
            enriched_matches["home_score"] < enriched_matches["away_score"],
        ],
        ["Home Win", "Away Win"],
        default="Draw",
    )
    enriched_matches["high_scoring_match"] = enriched_matches["total_goals"] >= 3
    enriched_matches["clean_sheet_match"] = (
        (enriched_matches["home_score"] == 0) | (enriched_matches["away_score"] == 0)
    )
    enriched_matches["both_teams_scored"] = (
        (enriched_matches["home_score"] > 0) & (enriched_matches["away_score"] > 0)
    )
    enriched_matches = (
        enriched_matches.merge(stages, on="stage_id", how="left")
        .merge(venues, on="venue_id", how="left", suffixes=("", "_venue"))
        .merge(referees, on="referee_id", how="left", suffixes=("", "_ref"))
    )
    data["matches_enriched"] = enriched_matches

    enriched_players = players.merge(
        squads.drop(columns=["team_id", "player_name", "position", "goals"], errors="ignore"),
        on="player_id",
        how="left",
        suffixes=("", "_squad"),
    )
    enriched_players["total_contributions"] = (
        enriched_players["goals"].fillna(0) + enriched_players["assists"].fillna(0)
    )
    enriched_players["goals_per_match"] = np.where(
        enriched_players["matches_played"] > 0,
        enriched_players["goals"] / enriched_players["matches_played"],
        0,
    )
    enriched_players["assists_per_match"] = np.where(
        enriched_players["matches_played"] > 0,
        enriched_players["assists"] / enriched_players["matches_played"],
        0,
    )
    enriched_players["contribution_per_match"] = np.where(
        enriched_players["matches_played"] > 0,
        enriched_players["total_contributions"] / enriched_players["matches_played"],
        0,
    )
    enriched_players["total_cards"] = (
        enriched_players["yellow_cards"].fillna(0) + enriched_players["red_cards"].fillna(0)
    )
    enriched_players["discipline_score"] = (
        enriched_players["yellow_cards"].fillna(0)
        + 2 * enriched_players["red_cards"].fillna(0)
    )
    enriched_players["minutes_per_goal"] = np.where(
        enriched_players["goals"] > 0,
        enriched_players["minutes_played"] / enriched_players["goals"],
        np.nan,
    )
    enriched_players["minutes_per_contribution"] = np.where(
        enriched_players["total_contributions"] > 0,
        enriched_players["minutes_played"] / enriched_players["total_contributions"],
        np.nan,
    )
    enriched_players["clean_sheet_rate"] = np.where(
        enriched_players["matches_played"] > 0,
        enriched_players["clean_sheets"] / enriched_players["matches_played"],
        np.nan,
    )
    enriched_players["team_name"] = enriched_players["team_id"].map(team_names)
    data["players_enriched"] = enriched_players

    enriched_team_stats = team_stats.copy()
    enriched_team_stats["shot_accuracy"] = np.where(
        enriched_team_stats["total_shots"] > 0,
        enriched_team_stats["shots_on_target"] / enriched_team_stats["total_shots"],
        0,
    )
    enriched_team_stats["shots_off_target"] = (
        enriched_team_stats["total_shots"] - enriched_team_stats["shots_on_target"]
    )
    enriched_team_stats["save_rate"] = np.where(
        enriched_team_stats["shots_on_target"] > 0,
        enriched_team_stats["saves"] / enriched_team_stats["shots_on_target"],
        0,
    )
    enriched_team_stats["fouls_per_shot"] = np.where(
        enriched_team_stats["total_shots"] > 0,
        enriched_team_stats["fouls"] / enriched_team_stats["total_shots"],
        0,
    )
    enriched_team_stats["corners_per_shot"] = np.where(
        enriched_team_stats["total_shots"] > 0,
        enriched_team_stats["corners"] / enriched_team_stats["total_shots"],
        0,
    )
    enriched_team_stats["offsides_per_shot"] = np.where(
        enriched_team_stats["total_shots"] > 0,
        enriched_team_stats["offsides"] / enriched_team_stats["total_shots"],
        0,
    )
    enriched_team_stats["aggressive_play_index"] = (
        enriched_team_stats["fouls"] + enriched_team_stats["offsides"]
    )
    enriched_team_stats["team_name"] = enriched_team_stats["team_id"].map(team_names)
    data["team_stats_enriched"] = enriched_team_stats

    data["events_enriched"] = (
        events.merge(players[["player_id", "player_name"]], on="player_id", how="left")
        .merge(teams[["team_id", "team_name"]], on="team_id", how="left")
    )

    return data
