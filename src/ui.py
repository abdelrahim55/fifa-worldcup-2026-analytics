from __future__ import annotations

import streamlit as st

from src.filters import FilterState


def render_site_nav(active: str | None = None) -> None:
    st.markdown('<div class="site-nav"><div class="nav-brand"><div class="nav-ball">⚽</div><div><div class="nav-brand__name">WORLD CUP 26</div><div class="nav-brand__tag">Football intelligence newsroom</div></div></div><div class="nav-spacer"></div></div>', unsafe_allow_html=True)
    cols = st.columns([1,1,1.05,1,1.15,1.25,1.18], gap="small")
    links = [
        ("🏠 Overview", "app.py", "Overview"),
        ("⚡ Matches", "pages/02_Matches.py", "Matches"),
        ("🛡 Teams", "pages/03_Teams.py", "Teams"),
        ("★ Players", "pages/04_Players.py", "Players"),
        ("◈ Squads", "pages/05_Lineups_and_Venues.py", "Lineups & Venues"),
        ("⌘ SQL Lab", "pages/07_SQL_Analytics_Lab.py", "SQL"),
        ("◎ Methodology", "pages/06_Data_and_Methodology.py", "Data & Methodology"),
    ]
    for col, (label, path, name) in zip(cols, links):
        with col:
            st.markdown('<div class="nav-link-wrap">', unsafe_allow_html=True)
            st.page_link(path, label=label)
            st.markdown('</div>', unsafe_allow_html=True)


def render_ticker() -> None:
    items = [
        "TOURNAMENT PULSE <b>LIVE FILTERS</b>",
        "MATCH INTELLIGENCE <b>xG • SHOTS • POSSESSION</b>",
        "TEAM POWER <b>FIFA RANK • ELO • FORM</b>",
        "PLAYER LAB <b>GOALS • ASSISTS • IMPACT</b>",
        "SQL ANALYTICS <b>CTEs • WINDOWS • RANKING</b>",
        "DATA LINEAGE <b>RAW → CLEAN → FEATURES → APP</b>",
    ]
    sequence = "".join(f'<span class="ticker__item"><span class="dot"></span>{x}</span>' for x in items)
    st.markdown(f'<div class="ticker"><div class="ticker__track">{sequence}{sequence}</div></div>', unsafe_allow_html=True)


def render_brand_header(eyebrow: str, title: str, subtitle: str, meta: list[str] | None = None) -> None:
    meta = meta or ["Interactive", "Notebook-backed", "SQL-enabled"]
    pills = "".join(f'<span class="hero-pill">{x}</span>' for x in meta)
    st.markdown(
        f'''
        <div class="hero hero--newsroom">
          <div class="hero__topline"><span class="live-dot"></span>{eyebrow}</div>
          <h1>{title}</h1>
          <p>{subtitle}</p>
          <div class="hero__meta">{pills}</div>
          <div class="hero__shape hero__shape--one"></div>
          <div class="hero__shape hero__shape--two"></div>
          <div class="hero__shape hero__shape--grid"></div>
        </div>
        ''',
        unsafe_allow_html=True,
    )


def page_intro(title: str, what: str, how: str) -> None:
    st.markdown(
        f'''
        <div class="page-intro">
          <div class="page-intro__main">
            <div class="page-intro__eyebrow">WHAT YOU ARE SEEING</div>
            <div class="page-intro__title">{title}</div>
            <div class="page-intro__text">{what}</div>
          </div>
          <div class="page-intro__how"><strong>HOW TO READ IT</strong><p>{how}</p></div>
        </div>
        ''',
        unsafe_allow_html=True,
    )


def explain_card(title: str, text: str, items: list[tuple[str, str]]) -> None:
    body = "".join(f'<div class="explain-card__item"><b>{k}</b><span>{v}</span></div>' for k, v in items)
    st.markdown(
        f'''
        <div class="explain-card">
          <div class="explain-card__kicker">ANALYST NOTE</div>
          <div class="explain-card__title">{title}</div>
          <div class="explain-card__text">{text}</div>
          <div class="explain-card__grid">{body}</div>
        </div>
        ''', unsafe_allow_html=True,
    )


def section_heading(title: str, subtitle: str | None = None) -> None:
    subtitle_html = f'<div class="section-subtitle">{subtitle}</div>' if subtitle else ""
    st.markdown(f'<div class="section-title">{title}</div>{subtitle_html}', unsafe_allow_html=True)


def kpi_card(label: str, value: str, note: str, tone: str = "green") -> str:
    return (
        f'<div class="kpi kpi--{tone}"><div class="kpi__label">{label}</div>'
        f'<div class="kpi__value">{value}</div><div class="kpi__note">{note}</div></div>'
    )


def render_filter_summary(state: FilterState) -> None:
    active = []
    if state.confederations:
        active.append("Confederation")
    if state.stages:
        active.append("Stage")
    if state.teams:
        active.append("Teams")
    label = " • ".join(active) if active else "All tournament data"
    st.markdown(
        f'<div class="filter-strip"><span class="filter-strip__label">FILTERS</span>'
        f'<span>{label}</span><span class="filter-strip__dates">{state.start_date:%d %b %Y} → {state.end_date:%d %b %Y}</span></div>',
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    st.markdown(
        '<div class="footer"><span><b>WORLD CUP 26 ANALYTICS</b> · data + EDA + feature engineering + SQL</span><span>Streamlit presentation layer</span></div>',
        unsafe_allow_html=True,
    )
