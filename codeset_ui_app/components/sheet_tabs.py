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
            gb = GridOptionsBuilder.from_dataframe(df)
            gb.configure_default_column(editable=True, resizable=True)
            grid_options = gb.build()
            AgGrid(df, gridOptions=grid_options, fit_columns_on_grid_load=True)
