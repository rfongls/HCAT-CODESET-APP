from __future__ import annotations
from typing import Dict, List, Any
import pandas as pd


def _norm(val: Any) -> str:
    if val is None:
        return ""
    return str(val).strip()


def validate_workbook(sheets: Dict[str, pd.DataFrame], mapping: Dict[str, Dict[str, Any]]) -> List[str]:
    """Return a list of validation error messages for the workbook."""
    errors: List[str] = []
    for sheet, df in sheets.items():
        info = mapping.get(sheet, {})
        code_col = info.get("code_col")
        display_col = info.get("display_col")
        mapped_col = info.get("mapped_col")
        std_col = info.get("std_col")
        std_code_col = info.get("std_code_col")
        # Skip if no dataframe
        if df is None or df.empty:
            continue
        # Duplicate codes
        if code_col and code_col in df.columns:
            codes = df[code_col].astype(str).str.strip()
            dup_vals = codes[codes != ""].value_counts()
            dup_vals = dup_vals[dup_vals > 1]
            for code_val in dup_vals.index:
                rows = [str(i + 2) for i, v in codes.items() if v == code_val]
                errors.append(f"{sheet} rows {', '.join(rows)} have duplicate CODE '{code_val}'")
        # Row-wise validations
        for idx, row in df.iterrows():
            row_num = idx + 2  # account for header row
            code = _norm(row.get(code_col)) if code_col else ""
            display = _norm(row.get(display_col)) if display_col else ""
            mapped = _norm(row.get(mapped_col)) if mapped_col else ""
            std_code = _norm(row.get(std_code_col)) if std_code_col else ""
            std_desc = _norm(row.get(std_col)) if std_col else ""
            if code and not display:
                errors.append(f"{sheet} row {row_num}: DISPLAY VALUE required when CODE is provided")
            if display and not code:
                errors.append(f"{sheet} row {row_num}: CODE required when DISPLAY VALUE is provided")

            if (code or display) and (std_code or std_desc) and not mapped:
                errors.append(
                    f"{sheet} row {row_num}: MAPPED_STD_DESCRIPTION required when standard code/description present"
                )
    return errors
