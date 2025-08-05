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
    for idx, (sheet, df) in enumerate(workbook.items()):
        with tabs[idx]:
            st.subheader(sheet)

            lock_key = f"{sheet}_protected"
            if lock_key not in st.session_state:
                st.session_state[lock_key] = False

            icon = "🔒" if st.session_state[lock_key] else "🔓"
            color = "red" if st.session_state[lock_key] else "green"
            status_text = "Sheet Protected" if st.session_state[lock_key] else "Sheet Unprotected"

            if st.button(icon, key=f"{sheet}_lock"):
                st.session_state[lock_key] = not st.session_state[lock_key]
                icon = "🔒" if st.session_state[lock_key] else "🔓"
                color = "red" if st.session_state[lock_key] else "green"
                status_text = (
                    "Sheet Protected" if st.session_state[lock_key] else "Sheet Unprotected"
                )

            st.markdown(
                f"<span style='color:{color}'>{icon} {status_text}</span>",
                unsafe_allow_html=True,
            )

            gb = GridOptionsBuilder.from_dataframe(df)
            gb.configure_default_column(editable=not st.session_state[lock_key], resizable=True)
            grid_options = gb.build()
            AgGrid(df, gridOptions=grid_options, fit_columns_on_grid_load=True)
