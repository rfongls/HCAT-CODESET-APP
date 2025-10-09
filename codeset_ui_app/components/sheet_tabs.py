from __future__ import annotations

from typing import Dict

import pandas as pd
import streamlit as st
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder


def render_sheet_tabs(workbook: Dict[str, pd.DataFrame]) -> None:
    """Render each workbook sheet in a separate tab with editable table."""
    sheet_names = list(workbook.keys())
    tabs = st.tabs(sheet_names)

    lock_key = "workbook_protected"
    if lock_key not in st.session_state:
        st.session_state[lock_key] = False

    for idx, (sheet, df) in enumerate(workbook.items()):
        with tabs[idx]:
            st.subheader(sheet)

            free_key = f"{sheet}_freetext"
            if free_key not in st.session_state:
                st.session_state[free_key] = False

            icon = "🔒" if st.session_state[lock_key] else "🔓"
            status_text = (
                "Workbook Protected"
                if st.session_state[lock_key]
                else "Workbook Unprotected"
            )

            if st.button(icon, key=f"{sheet}_lock"):
                st.session_state[lock_key] = not st.session_state[lock_key]
                icon = "🔒" if st.session_state[lock_key] else "🔓"
                status_text = (
                    "Workbook Protected"
                    if st.session_state[lock_key]
                    else "Workbook Unprotected"
                )

            bg_color = "#42b0f5" if st.session_state[lock_key] else "#fff"
            style = (
                "background-color:{bg}; border:1px solid #42b0f5; color:#000; "
                "padding:2px 4px; border-radius:4px;"
            ).format(bg=bg_color)
            st.markdown(
                f"<span style='{style}'>{icon}</span> <span style='margin-left:0.5rem'>{status_text}</span>",
                unsafe_allow_html=True,
            )

            gb = GridOptionsBuilder.from_dataframe(df)
            gb.configure_default_column(editable=not st.session_state[lock_key], resizable=True)
            grid_options = gb.build()
            AgGrid(df, gridOptions=grid_options, fit_columns_on_grid_load=True)
