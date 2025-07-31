from __future__ import annotations
from typing import Dict, Tuple
import pandas as pd
from openpyxl import load_workbook as _load_workbook
from openpyxl.workbook.workbook import Workbook


def load_workbook(file) -> Tuple[Dict[str, pd.DataFrame], Workbook]:
    """Load all sheets from an Excel workbook as data frames and return
    the underlying openpyxl workbook.

    The file is parsed only once using :mod:`openpyxl` to avoid repeated
    reads for dropdown extraction and formula inspection. All cells are
    converted to strings and empty columns are removed.
    """
    file.seek(0)
    wb = _load_workbook(file, data_only=False)

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
        df.dropna(axis=1, how="all", inplace=True)
        empty_cols = [c for c in df.columns if not c or str(c).startswith("Unnamed")]
        df.drop(columns=empty_cols, inplace=True, errors="ignore")
        data[sheet] = df

    return data, wb
