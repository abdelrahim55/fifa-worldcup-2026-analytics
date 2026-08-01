-- Reusable analytical views for the World Cup warehouse.

DROP VIEW IF EXISTS v_match_summary;
CREATE VIEW v_match_summary AS
SELECT
    m.match_id,
    m.date,
    m.kickoff_time_utc,
    s.stage_name,
    s.is_knockout,
    ht.team_name AS home_team,
    ht.fifa_code AS home_code,
    at.team_name AS away_team,
    at.fifa_code AS away_code,
    ht.confederation AS home_confederation,
    at.confederation AS away_confederation,
    m.home_score,
    m.away_score,
    m.home_xg,
    m.away_xg,
    ROUND(m.home_xg - m.away_xg, 2) AS xg_delta,
    m.status,
    m.result_type,
    v.stadium_name,
    v.city,
    v.country AS venue_country,
    v.capacity,
    v.elevation_meters,
    r.name AS referee,
    r.country AS referee_country,
    r.avg_cards_per_game,
    CASE
        WHEN m.home_score > m.away_score THEN 'Home Win'
        WHEN m.home_score < m.away_score THEN 'Away Win'
        ELSE 'Draw'
    END AS match_result,
    (m.home_score + m.away_score) AS total_goals,
    CASE WHEN m.home_score + m.away_score >= 3 THEN 1 ELSE 0 END AS high_scoring,
    CASE WHEN m.home_score > 0 AND m.away_score > 0 THEN 1 ELSE 0 END AS both_teams_scored
FROM fact_match m
JOIN dim_team ht ON ht.team_id = m.home_team_id
JOIN dim_team at ON at.team_id = m.away_team_id
LEFT JOIN dim_stage s ON s.stage_id = m.stage_id
LEFT JOIN dim_venue v ON v.venue_id = m.venue_id
LEFT JOIN dim_referee r ON r.referee_id = m.referee_id;

DROP VIEW IF EXISTS v_team_match_long;
CREATE VIEW v_team_match_long AS
SELECT
    m.match_id,
    m.date,
    s.stage_name,
    s.is_knockout,
    m.home_team_id AS team_id,
    m.away_team_id AS opponent_id,
    'HOME' AS venue_side,
    m.home_score AS goals_for,
    m.away_score AS goals_against,
    m.home_xg AS xg_for,
    m.away_xg AS xg_against,
    CASE WHEN m.home_score > m.away_score THEN 3 WHEN m.home_score = m.away_score THEN 1 ELSE 0 END AS points,
    CASE WHEN m.home_score > m.away_score THEN 'W' WHEN m.home_score = m.away_score THEN 'D' ELSE 'L' END AS result,
    ts.possession_pct,
    ts.total_shots,
    ts.shots_on_target,
    ts.corners,
    ts.fouls,
    ts.offsides,
    ts.saves
FROM fact_match m
JOIN dim_stage s ON s.stage_id = m.stage_id
LEFT JOIN fact_team_match_stats ts ON ts.match_id = m.match_id AND ts.team_id = m.home_team_id
UNION ALL
SELECT
    m.match_id,
    m.date,
    s.stage_name,
    s.is_knockout,
    m.away_team_id,
    m.home_team_id,
    'AWAY',
    m.away_score,
    m.home_score,
    m.away_xg,
    m.home_xg,
    CASE WHEN m.away_score > m.home_score THEN 3 WHEN m.home_score = m.away_score THEN 1 ELSE 0 END,
    CASE WHEN m.away_score > m.home_score THEN 'W' WHEN m.home_score = m.away_score THEN 'D' ELSE 'L' END,
    ts.possession_pct,
    ts.total_shots,
    ts.shots_on_target,
    ts.corners,
    ts.fouls,
    ts.offsides,
    ts.saves
FROM fact_match m
JOIN dim_stage s ON s.stage_id = m.stage_id
LEFT JOIN fact_team_match_stats ts ON ts.match_id = m.match_id AND ts.team_id = m.away_team_id;

DROP VIEW IF EXISTS v_team_tournament_summary;
CREATE VIEW v_team_tournament_summary AS
SELECT
    t.team_id,
    t.team_name,
    t.fifa_code,
    t.group_letter,
    t.confederation,
    t.fifa_ranking_pre_tournament,
    t.elo_rating,
    t.manager_name,
    COUNT(*) AS matches_played,
    SUM(CASE WHEN tm.result = 'W' THEN 1 ELSE 0 END) AS wins,
    SUM(CASE WHEN tm.result = 'D' THEN 1 ELSE 0 END) AS draws,
    SUM(CASE WHEN tm.result = 'L' THEN 1 ELSE 0 END) AS losses,
    SUM(tm.points) AS points,
    SUM(tm.goals_for) AS goals_for,
    SUM(tm.goals_against) AS goals_against,
    SUM(tm.goals_for - tm.goals_against) AS goal_difference,
    ROUND(SUM(tm.xg_for), 2) AS xg_for,
    ROUND(SUM(tm.xg_against), 2) AS xg_against,
    ROUND(AVG(tm.possession_pct), 1) AS avg_possession,
    ROUND(AVG(tm.total_shots), 1) AS avg_shots,
    ROUND(AVG(tm.shots_on_target), 1) AS avg_shots_on_target,
    ROUND(AVG(tm.corners), 1) AS avg_corners,
    ROUND(AVG(tm.fouls), 1) AS avg_fouls,
    ROUND(SUM(tm.goals_for) - SUM(tm.xg_for), 2) AS goals_vs_xg
FROM v_team_match_long tm
JOIN dim_team t ON t.team_id = tm.team_id
GROUP BY t.team_id, t.team_name, t.fifa_code, t.group_letter, t.confederation,
         t.fifa_ranking_pre_tournament, t.elo_rating, t.manager_name;

DROP VIEW IF EXISTS v_player_impact;
CREATE VIEW v_player_impact AS
SELECT
    ps.player_id,
    ps.player_name,
    t.team_name,
    t.confederation,
    ps.position,
    p.market_value_eur,
    p.caps,
    ps.matches_played,
    ps.matches_started,
    ps.minutes_played,
    COALESCE(ps.goals, 0) AS goals,
    COALESCE(ps.assists, 0) AS assists,
    COALESCE(ps.goals, 0) + COALESCE(ps.assists, 0) AS contributions,
    ps.shots,
    ps.shots_on_target,
    ps.yellow_cards,
    ps.red_cards,
    ps.clean_sheets,
    ps.saves,
    ps.goals_conceded,
    ps.average_rating,
    ROUND(CAST(COALESCE(ps.goals, 0) AS REAL) / NULLIF(ps.matches_played, 0), 3) AS goals_per_match,
    ROUND(CAST(COALESCE(ps.assists, 0) AS REAL) / NULLIF(ps.matches_played, 0), 3) AS assists_per_match,
    ROUND(CAST(COALESCE(ps.goals, 0) + COALESCE(ps.assists, 0) AS REAL) / NULLIF(ps.matches_played, 0), 3) AS contribution_per_match,
    ROUND(CAST(ps.minutes_played AS REAL) / NULLIF(ps.goals, 0), 1) AS minutes_per_goal,
    ROUND(CAST(ps.minutes_played AS REAL) / NULLIF(COALESCE(ps.goals, 0) + COALESCE(ps.assists, 0), 0), 1) AS minutes_per_contribution,
    ROUND(COALESCE(ps.yellow_cards, 0) + 2.0 * COALESCE(ps.red_cards, 0), 2) AS discipline_score
FROM fact_player_stats ps
JOIN dim_player p ON p.player_id = ps.player_id
JOIN dim_team t ON t.team_id = ps.team_id;

DROP VIEW IF EXISTS v_team_form;
CREATE VIEW v_team_form AS
WITH ordered AS (
    SELECT
        tm.*,
        t.team_name,
        ROW_NUMBER() OVER (PARTITION BY tm.team_id ORDER BY tm.date, tm.match_id) AS match_seq,
        LAG(tm.result) OVER (PARTITION BY tm.team_id ORDER BY tm.date, tm.match_id) AS previous_result
    FROM v_team_match_long tm
    JOIN dim_team t ON t.team_id = tm.team_id
)
SELECT *
FROM ordered;

DROP VIEW IF EXISTS v_referee_profile;
CREATE VIEW v_referee_profile AS
SELECT
    r.referee_id,
    r.name,
    r.country,
    r.avg_cards_per_game,
    COUNT(DISTINCT e.match_id) AS matches_with_events,
    SUM(CASE WHEN LOWER(e.event_type) = 'yellow card' THEN 1 ELSE 0 END) AS yellow_cards,
    SUM(CASE WHEN LOWER(e.event_type) = 'red card' THEN 1 ELSE 0 END) AS red_cards,
    SUM(CASE WHEN LOWER(e.event_type) IN ('yellow card', 'red card') THEN 1 ELSE 0 END) AS total_cards,
    ROUND(
        CAST(SUM(CASE WHEN LOWER(e.event_type) IN ('yellow card', 'red card') THEN 1 ELSE 0 END) AS REAL)
        / NULLIF(COUNT(DISTINCT e.match_id), 0),
        2
    ) AS observed_cards_per_game
FROM dim_referee r
LEFT JOIN fact_match m ON m.referee_id = r.referee_id
LEFT JOIN fact_event e ON e.match_id = m.match_id
GROUP BY r.referee_id, r.name, r.country, r.avg_cards_per_game;

DROP VIEW IF EXISTS v_match_event_timeline;
CREATE VIEW v_match_event_timeline AS
SELECT
    e.event_id,
    e.match_id,
    e.minute,
    e.event_type,
    t.team_name,
    p.player_name,
    m.date,
    ht.team_name AS home_team,
    at.team_name AS away_team
FROM fact_event e
LEFT JOIN dim_team t ON t.team_id = e.team_id
LEFT JOIN dim_player p ON p.player_id = e.player_id
JOIN fact_match m ON m.match_id = e.match_id
JOIN dim_team ht ON ht.team_id = m.home_team_id
JOIN dim_team at ON at.team_id = m.away_team_id;
