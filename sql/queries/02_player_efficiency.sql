-- Player efficiency: contribution per 90 with a minutes floor.
WITH eligible AS (
    SELECT
        player_name,
        team_name,
        position,
        minutes_played,
        goals,
        assists,
        contributions,
        market_value_eur,
        average_rating,
        ROUND(90.0 * contributions / NULLIF(minutes_played, 0), 3) AS contributions_per_90,
        ROUND(90.0 * goals / NULLIF(minutes_played, 0), 3) AS goals_per_90
    FROM v_player_impact
    WHERE minutes_played >= 180
), ranked AS (
    SELECT *,
           RANK() OVER (ORDER BY contributions_per_90 DESC) AS efficiency_rank
    FROM eligible
)
SELECT *
FROM ranked
ORDER BY efficiency_rank
LIMIT 25;
