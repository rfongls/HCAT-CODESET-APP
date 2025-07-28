from __future__ import annotations

from typing import Dict

import pandas as pd


def load_workbook(file) -> Dict[str, pd.DataFrame]:
    """Load all sheets from an Excel workbook as data frames."""
    return pd.read_excel(file, sheet_name=None, engine="openpyxl")
