from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_sql_assets_exist() -> None:
    assert (ROOT / "sql/schema.sql").exists()
    assert (ROOT / "sql/views.sql").exists()
    assert len(list((ROOT / "sql/queries").glob("*.sql"))) >= 8


def test_sql_schema_has_core_tables() -> None:
    schema = (ROOT / "sql/schema.sql").read_text(encoding="utf-8")
    for name in ["dim_team", "dim_player", "fact_match", "fact_event", "fact_lineup"]:
        assert f"CREATE TABLE {name}" in schema
