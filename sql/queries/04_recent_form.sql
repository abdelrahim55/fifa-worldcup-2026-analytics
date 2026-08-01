-- Last five results per team using window functions.
WITH numbered AS (
    SELECT
        team_name,
        date,
        match_id,
        result,
        points,
        ROW_NUMBER() OVER (PARTITION BY team_id ORDER BY date DESC, match_id DESC) AS recency_rank
    FROM v_team_form
), ordered AS (
    SELECT team_name, result, points, recency_rank
    FROM numbered
    WHERE recency_rank <= 5
    ORDER BY team_name, recency_rank DESC
)
SELECT
    team_name,
    GROUP_CONCAT(result, ' ') AS last_five_form,
    SUM(points) AS last_five_points
FROM ordered
GROUP BY team_name
ORDER BY last_five_points DESC, team_name;
