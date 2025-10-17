from __future__ import annotations
from typing import Dict, List, Any, Iterable
import pandas as pd


_PLACEHOLDER_VALUES = {"NA", "N/A"}


def _format_error(sheet: str, row: int | str, detail: str) -> str:
    """Return a standardized validation message."""

    if isinstance(row, int):
        row_label = f"row {row}"
    else:
        row_label = str(row)
    return f"{sheet} {row_label}: {detail}"


def _label(name: str | None, fallback: str) -> str:
    """Return a normalized column label for error messaging."""

    if not name:
        return fallback
    return str(name).strip()


def _norm(val: Any) -> str:
    if val is None:
        return ""
    return str(val).strip()


def _empty_if_placeholder(val: str) -> str:
    if val and val.upper() in _PLACEHOLDER_VALUES:
        return ""
    return val


def validate_workbook(
    sheets: Dict[str, pd.DataFrame],
    mapping: Dict[str, Dict[str, Any]],
    skip_mapped_requirement_sheets: Iterable[str] | None = None,
) -> List[str]:
    """Return a list of validation error messages for the workbook."""
    errors: List[str] = []
    skip_mapped_requirement = set(skip_mapped_requirement_sheets or [])
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
        code_label = _label(code_col, "CODE")
        display_label = _label(display_col, "DISPLAY VALUE")
        mapped_label = _label(mapped_col, "MAPPED_STD_DESCRIPTION")

        if code_col and code_col in df.columns:
            codes = df[code_col].astype(str).str.strip()
            dup_vals = codes[codes != ""].value_counts()
            dup_vals = dup_vals[dup_vals > 1]
            for code_val in dup_vals.index:
                dup_rows = [i + 2 for i, v in codes.items() if v == code_val]
                for row_num in dup_rows:
                    others = [str(r) for r in dup_rows if r != row_num]
                    if not others:
                        continue
                    others_list = ", ".join(others)
                    if len(others) == 1:
                        detail = (
                            f"duplicate {code_label} '{code_val}' duplicates row {others_list}"
                        )
                    else:
                        detail = (
                            f"duplicate {code_label} '{code_val}' duplicates rows {others_list}"
                        )
                    errors.append(_format_error(sheet, row_num, detail))
        # Row-wise validations
        for idx, row in df.iterrows():
            row_num = idx + 2  # account for header row
            code = _norm(row.get(code_col)) if code_col else ""
            display = _norm(row.get(display_col)) if display_col else ""
            mapped = _norm(row.get(mapped_col)) if mapped_col else ""
            std_code = _empty_if_placeholder(_norm(row.get(std_code_col))) if std_code_col else ""
            std_desc = _empty_if_placeholder(_norm(row.get(std_col))) if std_col else ""
            if code and not display:
                errors.append(
                    _format_error(
                        sheet,
                        row_num,
                        f"{display_label} required when {code_label} is provided",
                    )
                )
            if display and not code:
                errors.append(
                    _format_error(
                        sheet,
                        row_num,
                        f"{code_label} required when {display_label} is provided",
                    )
                )
            if (
                sheet not in skip_mapped_requirement
                and (code or display)
                and (std_code or std_desc)
                and not mapped
            ):
                detail = (
                    f"{mapped_label} required when STANDARD_CODE/STANDARD_DESCRIPTION is provided"
                )
                errors.append(_format_error(sheet, row_num, detail))
            if mapped and not code:
                errors.append(
                    _format_error(
                        sheet,
                        row_num,
                        f"{code_label} required when {mapped_label} is provided",
                    )
                )
            if mapped and not display:
                errors.append(
                    _format_error(
                        sheet,
                        row_num,
                        f"{display_label} required when {mapped_label} is provided",
                    )
                )
    return errors
