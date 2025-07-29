from __future__ import annotations
from typing import Dict
import pandas as pd
from openpyxl import load_workbook as _load_workbook


def load_workbook(file) -> Dict[str, pd.DataFrame]:
    """Load all sheets from an Excel workbook as data frames.

    Tries using pandas first. If that fails (often due to malformed XML
    in the workbook), it falls back to openpyxl's read-only mode. When
    all attempts fail, an empty dictionary is returned.
    """
    file.seek(0)
    try:
        # Read everything as text to avoid NaN propagation
        data = pd.read_excel(file, sheet_name=None, engine="openpyxl", dtype=str)
        for df in data.values():
            df.fillna("", inplace=True)
        return data
    except Exception:
        try:
            file.seek(0)
            wb = _load_workbook(file, data_only=True, read_only=True)
            data: Dict[str, pd.DataFrame] = {}
            for sheet in wb.sheetnames:
                ws = wb[sheet]
                rows = list(ws.values)
                if not rows:
                    data[sheet] = pd.DataFrame()
                    continue
                header, *content = rows
                df = pd.DataFrame(content, columns=header)
                df = df.astype(str).fillna("")
                data[sheet] = df
            return data
        except Exception:
            return {}
