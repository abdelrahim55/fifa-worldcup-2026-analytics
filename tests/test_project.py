from __future__ import annotations

import pandas as pd

from src.data import load_data
from src.utils import make_standings


def test_project_data_loads() -> None:
    data = load_data()
    assert len(data["teams"]) == 48
    assert len(data["matches"]) > 0
    assert len(data["players_enriched"]) > 0
    assert len(data["events_enriched"]) > 0


def test_match_enrichment_has_expected_columns() -> None:
    data = load_data()
    expected = {
        "home_team",
        "away_team",
        "total_goals",
        "match_result",
        "high_scoring_match",
        "clean_sheet_match",
        "both_teams_scored",
    }
    assert expected.issubset(data["matches_enriched"].columns)


def test_standings_schema() -> None:
    data = load_data()
    standings = make_standings(data["matches_enriched"], data["teams"])
    assert isinstance(standings, pd.DataFrame)
    assert {"Team", "Pts", "GD", "FIFA Rank", "ELO"}.issubset(standings.columns)
