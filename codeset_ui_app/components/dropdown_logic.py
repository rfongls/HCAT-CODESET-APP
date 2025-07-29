"""Utilities for extracting and handling dropdown validations."""

from __future__ import annotations

from typing import Dict, List

from openpyxl import load_workbook
from openpyxl.utils import range_boundaries


def _parse_formula(formula: str, wb) -> List[str]:
    """Return a list of options from a data-validation formula."""
    if not formula:
        return []
    formula = formula.lstrip("=")
    # Quoted comma-separated list
    if formula.startswith('"') and formula.endswith('"'):
        return [v.strip() for v in formula.strip('"').split(',') if v.strip()]
    # Range reference, e.g. Sheet1!$A$1:$A$5
    if "!" in formula:
        sheet_name, cell_range = formula.split("!", 1)
        sheet = wb[sheet_name]
    else:
        # Current sheet range
        cell_range = formula
        sheet = wb.active
    min_col, min_row, max_col, max_row = range_boundaries(cell_range)
    values: List[str] = []
    for row in range(min_row, max_row + 1):
        for col in range(min_col, max_col + 1):
            value = sheet.cell(row=row, column=col).value
            if value is not None:
                values.append(str(value))
    return values


def extract_dropdown_options(file) -> Dict[str, Dict[str, List[str]]]:
    """Extract dropdown validation options per sheet and column.

    Parameters
    ----------
    file: path or file-like object
        The Excel workbook to inspect.

    Returns
    -------
    Dict[str, Dict[str, List[str]]]
        Mapping of sheet names to columns and their list of allowed values.
    """
    file.seek(0)
    wb = load_workbook(file, data_only=True)
    dropdowns: Dict[str, Dict[str, List[str]]] = {}
    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        sheet_opts: Dict[str, List[str]] = {}
        headers = {cell.column: str(cell.value) for cell in ws[1]}
        if ws.data_validations is None:
            dropdowns[sheet_name] = sheet_opts
            continue
        for dv in ws.data_validations.dataValidation:
            if dv.type != "list":
                continue
            options = _parse_formula(dv.formula1, wb)
            for rng in dv.cells.ranges:
                min_col, min_row, max_col, max_row = range_boundaries(str(rng))
                # assume validation applies to entire column below header
                if min_row <= 2:
                    for col in range(min_col, max_col + 1):
                        header = headers.get(col)
                        if header:
                            sheet_opts.setdefault(header, options)
        dropdowns[sheet_name] = sheet_opts
    return dropdowns
