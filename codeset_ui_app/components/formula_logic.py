from __future__ import annotations

from typing import Dict
from openpyxl import load_workbook


def extract_column_formulas(file) -> Dict[str, Dict[str, str]]:
    """Return formulas for the first data row of each column per sheet."""
    file.seek(0)
    wb = load_workbook(file, data_only=False)
    formulas: Dict[str, Dict[str, str]] = {}
    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        headers = [str(cell.value) if cell.value is not None else "" for cell in ws[1]]
        sheet_formulas: Dict[str, str] = {}
        # Inspect row 2 which typically holds the first data row
        for row in ws.iter_rows(min_row=2, max_row=2, values_only=False):
            for header, cell in zip(headers, row):
                if cell.data_type == "f" and isinstance(cell.value, str):
                    sheet_formulas[header] = cell.value
            break
        formulas[sheet_name] = sheet_formulas
    return formulas
