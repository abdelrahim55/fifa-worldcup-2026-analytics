from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
WAREHOUSE = DATA / "warehouse" / "worldcup_analytics.db"
SQL_DIR = ROOT / "sql"

TABLE_MAP = {
    "dim_team": DATA / "raw" / "teams.csv",
    "dim_player": DATA / "raw" / "squads_and_players.csv",
    "dim_stage": DATA / "raw" / "tournament_stages.csv",
    "dim_venue": DATA / "raw" / "venues.csv",
    "dim_referee": DATA / "raw" / "referees.csv",
    "fact_match": DATA / "raw" / "matches.csv",
    "fact_player_stats": DATA / "raw" / "player_stats.csv",
    "fact_team_match_stats": DATA / "raw" / "match_team_stats.csv",
    "fact_lineup": DATA / "raw" / "match_lineups.csv",
    "fact_event": DATA / "raw" / "match_events.csv",
}


def execute_script(connection: sqlite3.Connection, path: Path) -> None:
    connection.executescript(path.read_text(encoding="utf-8"))


def normalize(df: pd.DataFrame) -> pd.DataFrame:
    # SQLite handles NULL more predictably when pandas NaN is converted to None.
    return df.astype(object).where(pd.notna(df), None)


def build() -> Path:
    WAREHOUSE.parent.mkdir(parents=True, exist_ok=True)
    if WAREHOUSE.exists():
        WAREHOUSE.unlink()

    with sqlite3.connect(WAREHOUSE) as conn:
        execute_script(conn, SQL_DIR / "schema.sql")

        for table, path in TABLE_MAP.items():
            if not path.exists():
                raise FileNotFoundError(f"Missing source CSV: {path}")
            df = normalize(pd.read_csv(path))
            if table == "dim_stage" and "is_knockout" in df.columns:
                df["is_knockout"] = df["is_knockout"].astype(int)
            if table == "dim_player" and "goals" in df.columns:
                df = df.rename(columns={"goals": "goals_career"})
            if table == "fact_match" and "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
            df.to_sql(table, conn, if_exists="append", index=False)

        execute_script(conn, SQL_DIR / "views.sql")
        conn.execute("ANALYZE;")
        conn.commit()

    return WAREHOUSE


if __name__ == "__main__":
    path = build()
    print(f"Built SQL warehouse: {path}")
