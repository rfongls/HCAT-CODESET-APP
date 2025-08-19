from __future__ import annotations

from typing import Dict

import pandas as pd
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom


def _str_series(df: pd.DataFrame, col: str) -> pd.Series:
    """Return a stripped string Series for ``col`` selecting non-empty dupes."""
    series = df[col]
    if isinstance(series, pd.DataFrame):
        non_empty = series.ne("").sum()
        series = series.iloc[:, non_empty.values.argmax()]
    return series.astype(str).str.strip()


def build_transformer_xml(data: Dict[str, pd.DataFrame]) -> str:
    """Return an indented XML string representing ``data`` as a codeset transformer."""
    root = Element("Configuration")
    fields_el = SubElement(root, "Fields")

    for sheet, df in data.items():
        if not isinstance(df, pd.DataFrame):
            continue
        col_map = {c.strip().upper().replace(" ", "_"): c for c in df.columns}
        code_col = col_map.get("CODE")
        display_col = col_map.get("DISPLAY_VALUE") or col_map.get("DISPLAY")
        std_code_col = (
            col_map.get("MAPPED_STANDARD_CODE")
            or col_map.get("MAPPED_STD_CODE")
            or col_map.get("STANDARD_CODE")
            or col_map.get("STD_CODE")
        )
        std_display_col = (
            col_map.get("MAPPED_STD_DESCRIPTION")
            or col_map.get("MAPPED_STANDARD_DESCRIPTION")
            or col_map.get("STANDARD_DESCRIPTION")
            or col_map.get("STD_DESCRIPTION")
            or col_map.get("MAPPED_STD_DESC")
        )
        oid_col = col_map.get("OID")
        url_col = col_map.get("URL")
        if code_col is None and display_col is None:
            continue

        name = sheet
        if name.startswith("CS_"):
            name = name[3:]
        name = name.replace("_", " ").title()

        field_el = SubElement(fields_el, "Field", Name=name)
        codesets_el = SubElement(field_el, "Codesets")
        codeset_el = SubElement(codesets_el, "Codeset", Name=name)

        if oid_col:
            oid_val = next((v for v in _str_series(df, oid_col) if v), "")
            if oid_val:
                codeset_el.set("OID", oid_val)
        if url_col:
            url_val = next((v for v in _str_series(df, url_col) if v), "")
            if url_val:
                codeset_el.set("URL", url_val)

        code_series = _str_series(df, code_col) if code_col else pd.Series([""] * len(df))
        display_series = _str_series(df, display_col) if display_col else pd.Series([""] * len(df))
        std_code_series = (
            _str_series(df, std_code_col) if std_code_col else code_series
        )
        std_display_series = (
            _str_series(df, std_display_col) if std_display_col else display_series
        )

        for lc, ld, sc, sd in zip(
            code_series, display_series, std_code_series, std_display_series
        ):
            if not any([lc, ld, sc, sd]):
                continue
            attrib = {}
            if lc:
                attrib["LocalCode"] = lc
            if ld:
                attrib["LocalDisplay"] = ld
            if sc:
                attrib["StandardCode"] = sc
            if sd:
                attrib["StandardDisplay"] = sd
            SubElement(codeset_el, "Code", attrib)

    xml_bytes = tostring(root, encoding="utf-8")
    # Pretty-print with CRLF newlines so Windows editors show each tag on its own line
    return minidom.parseString(xml_bytes).toprettyxml(indent="  ", newl="\r\n")
