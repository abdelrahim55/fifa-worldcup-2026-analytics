-- Referee discipline profile: stated average vs observed event cards.
SELECT
    name AS referee,
    country,
    avg_cards_per_game AS listed_cards_per_game,
    matches_with_events,
    yellow_cards,
    red_cards,
    total_cards,
    observed_cards_per_game,
    ROUND(observed_cards_per_game - avg_cards_per_game, 2) AS card_rate_delta
FROM v_referee_profile
ORDER BY observed_cards_per_game DESC, total_cards DESC;
