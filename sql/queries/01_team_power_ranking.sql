-- Team power ranking: tournament output balanced with underlying xG and possession.
WITH ranked AS (
    SELECT
        team_name,
        fifa_code,
        matches_played,
        wins,
        draws,
        losses,
        points,
        goal_difference,
        xg_for,
        xg_against,
        avg_possession,
        goals_vs_xg,
        RANK() OVER (ORDER BY points DESC, goal_difference DESC, xg_for DESC) AS table_rank,
        ROUND(
            0.45 * points
            + 0.20 * goal_difference
            + 0.20 * (xg_for - xg_against)
            + 0.15 * (avg_possession / 10.0),
            2
        ) AS power_score
    FROM v_team_tournament_summary
)
SELECT *
FROM ranked
ORDER BY power_score DESC, table_rank;
