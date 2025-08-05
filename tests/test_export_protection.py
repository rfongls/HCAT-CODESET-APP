"""Tests for sheet protection during export."""

import pandas as pd
from openpyxl import Workbook, load_workbook

from codeset_ui_app.utils.export_excel import export_workbook


def test_export_workbook_protects_sheet(tmp_path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Sheet1"
    ws.append(["CODE"])

    df = pd.DataFrame([{"CODE": "A"}])
    out = tmp_path / "out.xlsx"

    export_workbook(wb, {"Sheet1": df}, out, {"Sheet1": True})

    saved = load_workbook(out)
    assert saved["Sheet1"].protection.sheet is True

