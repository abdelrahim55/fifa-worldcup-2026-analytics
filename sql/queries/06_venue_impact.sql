-- Stadium-level tournament environment profile.
SELECT
    stadium_name,
    city,
    capacity,
    elevation_meters,
    COUNT(*) AS matches,
    ROUND(AVG(total_goals), 2) AS avg_goals,
    ROUND(AVG(home_xg + away_xg), 2) AS avg_xg,
    ROUND(100.0 * AVG(high_scoring), 1) AS high_scoring_rate_pct
FROM v_match_summary
GROUP BY stadium_name, city, capacity, elevation_meters
ORDER BY avg_goals DESC, matches DESC;
