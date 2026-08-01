from __future__ import annotations

import streamlit as st

from src.config import APP_ICON, APP_TITLE
from src.data import load_data
from src.filters import FilterState, filter_data, render_global_filters
from src.theme import apply_theme
from src.ui import render_filter_summary, render_site_nav, render_ticker


def bootstrap(active: str | None = None) -> tuple[dict, FilterState]:
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=APP_ICON,
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    apply_theme()
    render_site_nav(active)
    render_ticker()
    data = load_data()
    filters = render_global_filters(data)
    render_filter_summary(filters)
    return filter_data(data, filters), filters
