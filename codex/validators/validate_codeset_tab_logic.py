from __future__ import annotations

from pathlib import Path
from typing import Dict, Any, List

import pandas as pd
from openpyxl import load_workbook

DEFAULT_DEFINITION = Path(__file__).resolve().parents[1] / "spreadsheet_definitions" / "codex-spreadsheet-definition.md"


def _parse_definition_table(path: Path = DEFAULT_DEFINITION) -> Dict[str, Dict[str, bool]]:
    """Parse sheet-level rules from the markdown table."""
    rules: Dict[str, Dict[str, bool]] = {}
    if not path.exists():
        return rules
    for line in path.read_text().splitlines():
        if line.startswith("| CS_"):
            parts = [p.strip() for p in line.strip().strip("|").split("|")]
            if len(parts) >= 5:
                sheet = parts[0]
                req_map = parts[3].startswith("✅")
                has_formula = parts[4].startswith("✅")
                rules[sheet] = {
                    "requires_mapping": req_map,
                    "has_formula": has_formula,
                }
    return rules


def validate_codeset_tab_logic(workbook_path: str | Path,
                               definition_path: Path | None = None) -> List[Dict[str, Any]]:
    """Validate mapping logic for each sheet in a workbook."""
    definition_path = definition_path or DEFAULT_DEFINITION
    rules = _parse_definition_table(definition_path)

    xls = pd.ExcelFile(workbook_path, engine="openpyxl")
    wb = load_workbook(workbook_path, data_only=False)

    results: List[Dict[str, Any]] = []
    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet, dtype=str).fillna("")
        ws = wb[sheet]

        cols = [c.upper().replace(" ", "_") for c in df.columns]
        std_code_col = None
        std_desc_col = None
        mapped_col = None
        code_col = None
        display_col = None
        for col, key in zip(df.columns, cols):
            if key == "STANDARD_CODE":
                std_code_col = col
            if key == "STANDARD_DESCRIPTION":
                std_desc_col = col
            if key in ["MAPPED_STD_DESCRIPTION", "MAPPED_STANDARD_DESCRIPTION"]:
                mapped_col = col
            if key == "CODE":
                code_col = col
            if key in ["DISPLAY_VALUE", "DISPLAY"]:
                display_col = col

        if code_col and display_col:
            mask = df[code_col].str.strip().ne("") | df[display_col].str.strip().ne("")
            df = df[mask]

        std_code_has = bool(std_code_col and df[std_code_col].str.strip().any())
        std_desc_has = bool(std_desc_col and df[std_desc_col].str.strip().any())
        requires_mapping = std_code_has and std_desc_has and mapped_col is not None

        missing = 0
        if requires_mapping and mapped_col:
            missing = int(df[mapped_col].str.strip().eq("").sum())

        sheet_rules = rules.get(sheet, {})
        formula_issues: List[str] = []
        if sheet_rules.get("has_formula"):
            cell = ws.cell(row=2, column=4)
            if cell.data_type != "f":
                formula_issues.append("Missing formula in D2")

        results.append({
            "sheet_name": sheet,
            "requires_mapping": requires_mapping,
            "missing_mapped_std_descriptions": missing,
            "formula_issues": formula_issues,
        })
    return results
