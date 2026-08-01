-- Players who started most often and the team's scoring points while they started.
WITH starts AS (
    SELECT
        l.player_id,
        COUNT(*) AS starts,
        AVG(l.minutes_played) AS avg_minutes
    FROM fact_lineup l
    WHERE l.is_starting_xi = 1
    GROUP BY l.player_id
), player AS (
    SELECT
        p.player_id,
        p.player_name,
        t.team_name,
        ps.matches_played,
        ps.goals,
        ps.assists,
        s.starts,
        ROUND(s.avg_minutes, 1) AS avg_start_minutes
    FROM starts s
    JOIN dim_player p ON p.player_id = s.player_id
    JOIN dim_team t ON t.team_id = p.team_id
    LEFT JOIN fact_player_stats ps ON ps.player_id = p.player_id
)
SELECT *
FROM player
ORDER BY starts DESC, goals DESC, assists DESC
LIMIT 30;
