-- FIFA World Cup Analytics | SQLite warehouse schema
-- The warehouse is rebuilt from the CSV source layer by scripts/build_sqlite_warehouse.py.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS fact_event;
DROP TABLE IF EXISTS fact_lineup;
DROP TABLE IF EXISTS fact_team_match_stats;
DROP TABLE IF EXISTS fact_player_stats;
DROP TABLE IF EXISTS fact_match;
DROP TABLE IF EXISTS dim_player;
DROP TABLE IF EXISTS dim_team;
DROP TABLE IF EXISTS dim_stage;
DROP TABLE IF EXISTS dim_venue;
DROP TABLE IF EXISTS dim_referee;

CREATE TABLE dim_team (
    team_id INTEGER PRIMARY KEY,
    team_name TEXT NOT NULL,
    fifa_code TEXT NOT NULL,
    group_letter TEXT,
    confederation TEXT,
    fifa_ranking_pre_tournament INTEGER,
    elo_rating REAL,
    manager_name TEXT
);

CREATE TABLE dim_player (
    player_id INTEGER PRIMARY KEY,
    team_id INTEGER NOT NULL,
    player_name TEXT NOT NULL,
    position TEXT,
    club_team TEXT,
    market_value_eur REAL,
    caps INTEGER,
    date_of_birth TEXT,
    height_cm REAL,
    goals_career INTEGER,
    FOREIGN KEY (team_id) REFERENCES dim_team(team_id)
);

CREATE TABLE dim_stage (
    stage_id INTEGER PRIMARY KEY,
    stage_name TEXT NOT NULL,
    is_knockout INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE dim_venue (
    venue_id INTEGER PRIMARY KEY,
    stadium_name TEXT NOT NULL,
    city TEXT,
    country TEXT,
    capacity INTEGER,
    latitude REAL,
    longitude REAL,
    elevation_meters REAL
);

CREATE TABLE dim_referee (
    referee_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    country TEXT,
    avg_cards_per_game REAL
);

CREATE TABLE fact_match (
    match_id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,
    kickoff_time_utc TEXT,
    stage_id INTEGER,
    venue_id INTEGER,
    home_team_id INTEGER NOT NULL,
    away_team_id INTEGER NOT NULL,
    home_score INTEGER,
    away_score INTEGER,
    home_penalty_score INTEGER,
    away_penalty_score INTEGER,
    status TEXT,
    result_type TEXT,
    home_xg REAL,
    away_xg REAL,
    referee_id INTEGER,
    player_of_the_match_id INTEGER,
    FOREIGN KEY (stage_id) REFERENCES dim_stage(stage_id),
    FOREIGN KEY (venue_id) REFERENCES dim_venue(venue_id),
    FOREIGN KEY (home_team_id) REFERENCES dim_team(team_id),
    FOREIGN KEY (away_team_id) REFERENCES dim_team(team_id),
    FOREIGN KEY (referee_id) REFERENCES dim_referee(referee_id)
);

CREATE TABLE fact_player_stats (
    player_id INTEGER PRIMARY KEY,
    player_name TEXT NOT NULL,
    team_id INTEGER NOT NULL,
    position TEXT,
    matches_played INTEGER,
    matches_started INTEGER,
    minutes_played INTEGER,
    goals INTEGER,
    assists INTEGER,
    shots REAL,
    shots_on_target REAL,
    yellow_cards INTEGER,
    red_cards INTEGER,
    penalty_goals INTEGER,
    own_goals INTEGER,
    clean_sheets REAL,
    saves REAL,
    goals_conceded REAL,
    average_rating REAL,
    data_source TEXT,
    last_verified TEXT,
    FOREIGN KEY (player_id) REFERENCES dim_player(player_id),
    FOREIGN KEY (team_id) REFERENCES dim_team(team_id)
);

CREATE TABLE fact_team_match_stats (
    match_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    possession_pct REAL,
    total_shots INTEGER,
    shots_on_target INTEGER,
    corners INTEGER,
    fouls INTEGER,
    offsides INTEGER,
    saves INTEGER,
    player_of_the_match TEXT,
    data_source TEXT,
    last_updated TEXT,
    PRIMARY KEY (match_id, team_id),
    FOREIGN KEY (match_id) REFERENCES fact_match(match_id),
    FOREIGN KEY (team_id) REFERENCES dim_team(team_id)
);

CREATE TABLE fact_lineup (
    lineup_id INTEGER PRIMARY KEY,
    match_id INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    is_starting_xi INTEGER NOT NULL DEFAULT 0,
    tactical_position TEXT,
    minutes_played INTEGER,
    FOREIGN KEY (match_id) REFERENCES fact_match(match_id),
    FOREIGN KEY (player_id) REFERENCES dim_player(player_id),
    FOREIGN KEY (team_id) REFERENCES dim_team(team_id)
);

CREATE TABLE fact_event (
    event_id INTEGER PRIMARY KEY,
    match_id INTEGER NOT NULL,
    minute TEXT,
    event_type TEXT,
    team_id INTEGER,
    player_id INTEGER,
    FOREIGN KEY (match_id) REFERENCES fact_match(match_id),
    FOREIGN KEY (team_id) REFERENCES dim_team(team_id),
    FOREIGN KEY (player_id) REFERENCES dim_player(player_id)
);

CREATE INDEX idx_fact_match_date ON fact_match(date);
CREATE INDEX idx_fact_match_home_team ON fact_match(home_team_id);
CREATE INDEX idx_fact_match_away_team ON fact_match(away_team_id);
CREATE INDEX idx_team_match_team ON fact_team_match_stats(team_id);
CREATE INDEX idx_team_match_match ON fact_team_match_stats(match_id);
CREATE INDEX idx_lineup_player ON fact_lineup(player_id);
CREATE INDEX idx_event_match ON fact_event(match_id);
CREATE INDEX idx_event_type ON fact_event(event_type);
