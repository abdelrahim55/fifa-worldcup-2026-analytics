-- Does controlling possession correlate with points and wins?
WITH buckets AS (
    SELECT
        CASE
            WHEN possession_pct < 45 THEN 'Below 45%'
            WHEN possession_pct < 55 THEN '45-54%'
            WHEN possession_pct < 65 THEN '55-64%'
            ELSE '65%+'
        END AS possession_bucket,
        points,
        result,
        goals_for,
        goals_against
    FROM v_team_match_long
    WHERE possession_pct IS NOT NULL
)
SELECT
    possession_bucket,
    COUNT(*) AS team_match_samples,
    ROUND(AVG(points), 2) AS avg_points,
    ROUND(100.0 * AVG(CASE WHEN result = 'W' THEN 1.0 ELSE 0.0 END), 1) AS win_rate_pct,
    ROUND(AVG(goals_for), 2) AS avg_goals_for,
    ROUND(AVG(goals_against), 2) AS avg_goals_against
FROM buckets
GROUP BY possession_bucket
ORDER BY CASE possession_bucket
    WHEN 'Below 45%' THEN 1 WHEN '45-54%' THEN 2 WHEN '55-64%' THEN 3 ELSE 4 END;
