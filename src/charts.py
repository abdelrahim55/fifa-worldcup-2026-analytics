from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

GREEN = "#16b967"
DARK = "#0d1826"
CYAN = "#4fdcff"
RED = "#ff4f61"
GOLD = "#f5c451"
BLUE = "#4b7dff"
MINT = "#bfe9d5"
GREY = "#8090a0"


def base(fig: go.Figure, height: int | None = None) -> go.Figure:
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0)",
        margin={"l": 8, "r": 8, "t": 52, "b": 12},
        font={"family": "Inter", "color": DARK, "size": 11},
        hoverlabel={"bgcolor": DARK, "font_color": "white"},
        title={"font": {"size": 16, "family": "Barlow Condensed", "color": DARK}, "x": 0, "xanchor": "left"},
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "left", "x": 0, "font": {"size": 9}},
        xaxis={"showgrid": True, "gridcolor": "#eef2f5", "zeroline": False},
        yaxis={"showgrid": True, "gridcolor": "#eef2f5", "zeroline": False},
    )
    if height:
        fig.update_layout(height=height)
    return fig


def empty(title: str, message: str = "No data for the current filters.") -> go.Figure:
    fig = go.Figure()
    fig.update_layout(
        title=title,
        annotations=[{"text": message, "x": .5, "y": .5, "xref": "paper", "yref": "paper", "showarrow": False, "font": {"size": 12, "color": GREY}}],
        xaxis={"visible": False},
        yaxis={"visible": False},
    )
    return base(fig)


def goals_xg(matches: pd.DataFrame) -> go.Figure:
    if matches.empty:
        return empty("Goals vs xG trend")
    frame = matches.sort_values("date")
    long = pd.DataFrame({"date": frame["date"], "Goals": frame.home_score + frame.away_score, "xG": frame.home_xg + frame.away_xg}).melt("date", var_name="Metric", value_name="Value")
    return base(px.line(long, x="date", y="Value", color="Metric", markers=True, title="Goals vs xG trend", color_discrete_sequence=[GREEN, DARK]))


def confederations(teams: pd.DataFrame) -> go.Figure:
    if teams.empty:
        return empty("Tournament field by confederation")
    counts = teams.confederation.value_counts().reset_index()
    counts.columns = ["Confederation", "Teams"]
    return base(px.bar(counts, x="Teams", y="Confederation", orientation="h", title="Tournament field by confederation", text="Teams", color="Confederation", color_discrete_sequence=[GREEN, CYAN, BLUE, GOLD, RED, DARK]))


def results_donut(matches: pd.DataFrame) -> go.Figure:
    if matches.empty:
        return empty("Match outcomes")
    counts = matches.match_result.value_counts().rename_axis("Result").reset_index(name="Matches")
    return base(px.pie(counts, names="Result", values="Matches", hole=.67, title="Match outcomes", color_discrete_sequence=[GREEN, RED, GOLD]))


def goals_distribution(matches: pd.DataFrame) -> go.Figure:
    if matches.empty:
        return empty("Goals per match")
    bins = int(matches.total_goals.max() + 1) if len(matches) else 1
    return base(px.histogram(matches, x="total_goals", nbins=bins, title="Goals per match", text_auto=True, color_discrete_sequence=[DARK]))


def team_rankings(teams: pd.DataFrame) -> go.Figure:
    if teams.empty:
        return empty("Best pre-tournament FIFA ranks")
    top = teams.sort_values("fifa_ranking_pre_tournament").head(12).sort_values("fifa_ranking_pre_tournament", ascending=True)
    return base(px.bar(top, x="fifa_ranking_pre_tournament", y="team_name", orientation="h", title="Best pre-tournament FIFA ranks", text="fifa_ranking_pre_tournament", color_discrete_sequence=[GREEN]))


def team_scatter(team_view: pd.DataFrame) -> go.Figure:
    if team_view.empty:
        return empty("ELO vs scoring output")
    fig = px.scatter(team_view, x="elo_rating", y="goals_per_match", size="matches_played", color="confederation", hover_name="team_name", text="fifa_code", title="ELO vs scoring output", color_discrete_sequence=[GREEN, CYAN, BLUE, GOLD, RED, DARK])
    fig.update_traces(textposition="top center", marker={"line": {"width": 1, "color": "white"}})
    return base(fig)


def player_scatter(players: pd.DataFrame) -> go.Figure:
    if players.empty:
        return empty("Goals vs assists — player impact")
    return base(px.scatter(players, x="assists", y="goals", size="minutes_played", color="position", hover_name="player_name", hover_data=["team_name", "contribution_per_match"], title="Goals vs assists — player impact", color_discrete_sequence=[GREEN, CYAN, GOLD, RED, BLUE]))


def xg_match(match: object) -> go.Figure:
    categories = ["Goals", "xG", "Shots", "Shots on target", "Possession %", "Corners"]
    home_values = [match.home_score, match.home_xg, match.home_shots, match.home_sot, match.home_poss, match.home_corners]
    away_values = [match.away_score, match.away_xg, match.away_shots, match.away_sot, match.away_poss, match.away_corners]
    fig = go.Figure([
        go.Bar(name=match.home_team, x=categories, y=home_values, marker_color=GREEN, marker_line_color="white", marker_line_width=0.8),
        go.Bar(name=match.away_team, x=categories, y=away_values, marker_color=DARK, marker_line_color="white", marker_line_width=0.8),
    ])
    fig.update_layout(barmode="group", title="Match performance comparison")
    return base(fig)


def event_timeline(events: pd.DataFrame) -> go.Figure:
    if events.empty:
        return empty("Match event timeline")
    frame = events.copy(); frame["count"] = 1
    return base(px.scatter(frame, x="minute_num", y="team_name", color="event_type", size="count", hover_name="player_name", title="Match event timeline", symbol="event_type", color_discrete_sequence=[GREEN, RED, CYAN, GOLD, BLUE, DARK]))


def formation(lineups: pd.DataFrame, players: pd.DataFrame, team_id: int) -> go.Figure:
    frame = lineups[(lineups.team_id == team_id) & (lineups.is_starting_xi == 1)].merge(players[["player_id", "player_name"]], on="player_id", how="left")
    if frame.empty:
        return empty("Starting XI by tactical position")
    positions = frame.tactical_position.value_counts().reindex(["GK", "DEF", "MID", "FWD"]).fillna(0).reset_index()
    positions.columns = ["Position", "Players"]
    return base(px.bar(positions, x="Position", y="Players", title="Starting XI by tactical position", text="Players", color="Position", color_discrete_sequence=[GOLD, BLUE, CYAN, GREEN]))


def venue_map(venues: pd.DataFrame) -> go.Figure:
    if venues.empty:
        return empty("Tournament venues")
    fig = px.scatter_map(venues, lat="latitude", lon="longitude", hover_name="stadium_name", hover_data=["city", "country", "capacity", "elevation_meters"], size="capacity", zoom=2.8, height=500, title="Tournament venues")
    fig.update_traces(marker={"color": GREEN})
    fig.update_layout(map_style="carto-positron")
    return fig
