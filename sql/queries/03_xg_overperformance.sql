-- Which teams finish furthest above / below their xG?
SELECT
    team_name,
    matches_played,
    goals_for,
    xg_for,
    goals_vs_xg,
    ROUND(goals_vs_xg / NULLIF(matches_played, 0), 3) AS goals_above_xg_per_match,
    RANK() OVER (ORDER BY goals_vs_xg DESC) AS overperformance_rank
FROM v_team_tournament_summary
ORDER BY overperformance_rank;
