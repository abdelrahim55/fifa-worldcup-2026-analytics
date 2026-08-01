# SQL Analytics Layer

The project includes a lightweight **SQLite analytical warehouse** so the repository demonstrates a real SQL workflow in addition to Python/Streamlit.

## Why SQL is here

The SQL layer turns the CSV collection into a relational model with clear dimensions and facts, reusable analytical views, window functions, CTEs, ranking, and an auditable query library. The Streamlit dashboard remains the presentation layer; SQL is the analytical warehouse layer.

## Structure

```text
sql/
├── schema.sql
├── views.sql
├── queries/
│   ├── 01_team_power_ranking.sql
│   ├── 02_player_efficiency.sql
│   ├── 03_xg_overperformance.sql
│   ├── 04_recent_form.sql
│   ├── 05_possession_vs_results.sql
│   ├── 06_venue_impact.sql
│   ├── 07_referee_discipline.sql
│   └── 08_starting_xi_impact.sql
└── README.md
```

## Warehouse model

**Dimensions:** `dim_team`, `dim_player`, `dim_stage`, `dim_venue`, `dim_referee`

**Facts:** `fact_match`, `fact_player_stats`, `fact_team_match_stats`, `fact_lineup`, `fact_event`

**Analytical views:** `v_match_summary`, `v_team_match_long`, `v_team_tournament_summary`, `v_player_impact`, `v_team_form`, `v_referee_profile`, `v_match_event_timeline`

## Build the database

From the repository root:

```bash
python scripts/build_sqlite_warehouse.py
```

This creates:

```text
data/warehouse/worldcup_analytics.db
```

The generated database is intentionally gitignored because it can be reproduced from source CSVs.

## Open the warehouse manually

SQLite CLI:

```bash
sqlite3 data/warehouse/worldcup_analytics.db
```

Then:

```sql
SELECT * FROM v_team_tournament_summary ORDER BY points DESC LIMIT 10;
```

## Streamlit

The `SQL Analytics Lab` page runs the curated SQL query library against the same warehouse and exposes the query text for inspection and reuse.
