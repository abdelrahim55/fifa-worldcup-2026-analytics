from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
WAREHOUSE = ROOT / "data" / "warehouse" / "worldcup_analytics.db"
SQL_DIR = ROOT / "sql"


def _build_database() -> None:
    from scripts.build_sqlite_warehouse import build

    build()


@st.cache_resource(show_spinner="Preparing SQL warehouse…")
def get_connection() -> sqlite3.Connection:
    if not WAREHOUSE.exists():
        _build_database()
    connection = sqlite3.connect(WAREHOUSE, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    return connection


def run_sql(query: str) -> pd.DataFrame:
    connection = get_connection()
    return pd.read_sql_query(query, connection)


def list_queries() -> dict[str, Path]:
    return {
        path.stem: path
        for path in sorted((SQL_DIR / "queries").glob("*.sql"))
    }


def load_query(name: str) -> str:
    queries = list_queries()
    if name not in queries:
        raise KeyError(f"Unknown SQL query: {name}")
    return queries[name].read_text(encoding="utf-8")
