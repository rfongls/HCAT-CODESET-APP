from __future__ import annotations

from typing import Dict

import pandas as pd
from xml.etree.ElementTree import Element, SubElement, tostring


def _str_series(df: pd.DataFrame, col: str) -> pd.Series:
    """Return a stripped string Series for ``col`` selecting non-empty dupes."""
    series = df[col]
    if isinstance(series, pd.DataFrame):
        non_empty = series.ne("").sum()
        series = series.iloc[:, non_empty.values.argmax()]
    return series.astype(str).str.strip()


def build_transformer_xml(data: Dict[str, pd.DataFrame]) -> str:
    """Return an XML string representing ``data`` as a codeset transformer."""
    root = Element("CodesetTransformer")
    fields_el = SubElement(root, "Fields")

    for sheet, df in data.items():
        if not isinstance(df, pd.DataFrame):
            continue
        col_map = {c.strip().upper().replace(" ", "_"): c for c in df.columns}
        code_col = col_map.get("CODE")
        display_col = col_map.get("DISPLAY_VALUE") or col_map.get("DISPLAY")
        oid_col = col_map.get("OID")
        url_col = col_map.get("URL")
        if code_col is None and display_col is None:
            continue

        name = sheet
        if name.startswith("CS_"):
            name = name[3:]
        name = name.replace("_", " ").title()
        codeset_el = SubElement(fields_el, "Codeset", name=name)

        if oid_col:
            oid_val = next((v for v in _str_series(df, oid_col) if v), "")
            if oid_val:
                codeset_el.set("oid", oid_val)
        if url_col:
            url_val = next((v for v in _str_series(df, url_col) if v), "")
            if url_val:
                codeset_el.set("url", url_val)

        code_series = _str_series(df, code_col) if code_col else pd.Series([""] * len(df))
        display_series = _str_series(df, display_col) if display_col else pd.Series([""] * len(df))

        for code, display in zip(code_series, display_series):
            if not code and not display:
                continue
            text = f"{code}^{display}".strip("^")
            SubElement(codeset_el, "Value").text = text

    return tostring(root, encoding="utf-8").decode("utf-8")
