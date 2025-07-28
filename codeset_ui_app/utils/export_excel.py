"""Helper functions for exporting workbooks back to Excel."""

from __future__ import annotations

from typing import Dict

import pandas as pd


def export_workbook(workbook: Dict[str, pd.DataFrame], path: str) -> None:
    """Stub implementation for saving workbook to disk."""
    with pd.ExcelWriter(path, engine="xlsxwriter") as writer:
        for sheet, df in workbook.items():
            df.to_excel(writer, sheet_name=sheet, index=False)
