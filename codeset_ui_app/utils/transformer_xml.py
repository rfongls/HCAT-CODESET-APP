from __future__ import annotations
from typing import Dict, List
import pandas as pd
from xml.sax.saxutils import quoteattr


def _str_series(df: pd.DataFrame, col: str) -> pd.Series:
    """Return a stripped string Series for ``col`` using the first column if duplicated."""
    series = df[col]
    if isinstance(series, pd.DataFrame):
        series = series.iloc[:, 0]
    # ``astype(str)`` turns ``NaN`` into the literal string "nan" which later
    # appears as a legitimate value.  Replace these with empty strings so rows
    # with missing data can be dropped cleanly during processing.
    return series.astype(str).replace("nan", "").str.strip()


def _split_code_display(text: str) -> tuple[str, str]:
    """Return a code/description pair from ``text``.

    The workbook sometimes stores combined values like ``"X^Desc"`` or
    ``"X-Desc"``.  Hyphen splits are only considered a separator when the code
    portion contains no spaces; otherwise the entire value is treated as the
    description (e.g. ``"HIPAA OPT-OUT"``).
    """

    text = text.strip()
    if "^" in text:
        left, right = text.split("^", 1)
        return left.strip(), right.strip()
    if "-" in text:
        left, right = text.split("-", 1)
        if " " not in left.strip() and " " in right.strip():
            return left.strip(), right.strip()
    return "", text.strip()

def build_transformer_xml(
    data: Dict[str, pd.DataFrame],
    freetext: Dict[str, bool] | None = None,
) -> str:
    """Return an indented XML string representing ``data`` as a codeset transformer.

    Parameters
    ----------
    data:
        Mapping of sheet name to DataFrame representing the codeset workbook.
    freetext:
        Optional mapping of codeset name to a boolean indicating whether the
        field should allow free text.  The argument is retained for backwards
        compatibility but is currently ignored because the generated
        transformers omit the ``Fields`` section.
    """

    # Collect codeset information from workbook data
    codesets: List[dict] = []
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
        mapped_sd_col = (
            col_map.get("MAPPED_STD_DESCRIPTION")
            or col_map.get("MAPPED_STANDARD_DESCRIPTION")
            or col_map.get("MAPPED_STD_DESC")
        )
        std_desc_col = (
            col_map.get("STANDARD_DESCRIPTION")
            or col_map.get("STD_DESCRIPTION")
        )
        subdef_col = col_map.get("SUBDEFINITION") or col_map.get("SUBSECTION")
        oid_col = col_map.get("OID")
        url_col = col_map.get("URL")
        if (
            code_col is None
            and display_col is None
            and std_code_col is None
            and mapped_sd_col is None
            and std_desc_col is None
        ):
            continue

        codeset_info: dict = {"Name": sheet, "Codes": []}

        if oid_col:
            oid_val = next((v for v in _str_series(df, oid_col) if v), "")
            if oid_val:
                codeset_info["Oid"] = oid_val
        if url_col:
            url_val = next((v for v in _str_series(df, url_col) if v), "")
            if url_val:
                codeset_info["Url"] = url_val

        code_series = _str_series(df, code_col) if code_col else pd.Series([""] * len(df))
        display_series = _str_series(df, display_col) if display_col else pd.Series([""] * len(df))
        std_code_series = _str_series(df, std_code_col) if std_code_col else pd.Series([""] * len(df))
        mapped_sd_series = _str_series(df, mapped_sd_col) if mapped_sd_col else pd.Series([""] * len(df))
        std_desc_series = _str_series(df, std_desc_col) if std_desc_col else pd.Series([""] * len(df))
        subdef_series = _str_series(df, subdef_col) if subdef_col else pd.Series([""] * len(df))
        def_col = col_map.get("DEFINITION")
        def_series = _str_series(df, def_col) if def_col else pd.Series([""] * len(df))

        code_map: Dict[tuple[str, str], dict] = {}
        code_order_keys: List[tuple[str, str]] = []
        has_mapped_col = mapped_sd_col is not None
        has_subdef_col = subdef_col is not None

        for lc, ld, sc, mapped_sd, std_desc, subdef, definition in zip(
            code_series,
            display_series,
            std_code_series,
            mapped_sd_series,
            std_desc_series,
            subdef_series,
            def_series,
        ):
            lc = (lc or "").strip()
            ld = (ld or "").strip()
            if not lc or not ld:
                continue
            sc = (sc or "").strip()
            mapped_sd = (mapped_sd or "").strip()
            std_desc = (std_desc or "").strip()
            subdef = (subdef or "").strip()
            definition = (definition or "").strip()
            mapping_selected = False
            if mapped_sd:
                mapping_selected = True
            elif subdef:
                mapping_selected = True
            elif not (has_mapped_col or has_subdef_col):
                mapping_selected = bool(definition)
            sd = ""
            final_sc = ""
            mapped_code = ""
            def_code = ""
            def_desc = ""
            if mapping_selected:
                if mapped_sd:
                    mapped_code, sd = _split_code_display(mapped_sd)
                if not sd and std_desc:
                    sd = std_desc
                if definition:
                    def_code, def_desc = _split_code_display(definition)
                    if not sd:
                        sd = def_desc
                if sd and std_desc == sd and sc:
                    final_sc = sc
                elif sd and def_desc == sd and def_code:
                    final_sc = def_code
                elif mapped_code:
                    final_sc = mapped_code
                elif def_code:
                    final_sc = def_code
                elif sc and not std_desc:
                    final_sc = sc
                if (not final_sc or not sd) and subdef:
                    sc2, sd2 = _split_code_display(subdef)
                    if sd2 and not sd:
                        sd = sd2
                    if sd2 == sd and sc2:
                        final_sc = sc2
                    elif not final_sc and sc2:
                        final_sc = sc2
                if sd and not final_sc:
                    matches = std_desc_series[std_desc_series == sd]
                    if not matches.empty:
                        idx = matches.index[0]
                        sc_lookup = std_code_series.iloc[idx].strip()
                        if sc_lookup:
                            final_sc = sc_lookup
            key = (lc, ld)
            if key in code_map:
                existing = code_map[key]
                if final_sc and not existing.get("StandardCode"):
                    existing["StandardCode"] = final_sc
                if sd and not existing.get("StandardDisplay"):
                    existing["StandardDisplay"] = sd
            else:
                code_map[key] = {
                    "LocalCode": lc,
                    "LocalDisplay": ld,
                    "StandardCode": final_sc,
                    "StandardDisplay": sd,
                }
                code_order_keys.append(key)
        codeset_info["Codes"].extend(code_map[k] for k in code_order_keys)
        codesets.append(codeset_info)

    # Build codeset XML lines with column widths calculated per codeset to
    # avoid excessive gaps between attributes when one codeset contains very
    # long values.
    code_order = ["LocalCode", "LocalDisplay", "StandardCode", "StandardDisplay"]
    codeset_lines: List[str] = []
    for cs in codesets:
        header = f"    <Codeset Name={quoteattr(cs['Name'])}"
        if cs.get("Oid"):
            header += f" Oid={quoteattr(cs['Oid'])}"
        if cs.get("Url"):
            header += f" Url={quoteattr(cs['Url'])}"

        if not cs["Codes"]:
            codeset_lines.append(header + " />")
            continue

        header += ">"
        codeset_lines.append(header)
        code_attr_strings = [
            [f"{k}={quoteattr(c[k])}" if c.get(k) else "" for k in code_order]
            for c in cs["Codes"]
        ]
        code_widths = [
            max((len(attrs[i]) for attrs in code_attr_strings if attrs[i]), default=0) + 2
            for i in range(len(code_order) - 1)
        ]

        for attrs in code_attr_strings:
            parts = [attrs[0].ljust(code_widths[0])]
            for i in range(1, len(code_order) - 1):
                parts.append(attrs[i].ljust(code_widths[i]))
            parts.append(attrs[-1])
            codeset_lines.append("      <Code " + "".join(parts).rstrip() + " />")

        codeset_lines.append("    </Codeset>")

    lines = [
        "<Configuration>",
        "  <Codesets>",
        *codeset_lines,
        "  </Codesets>",
        "</Configuration>",
    ]

    return "\r\n".join(lines) + "\r\n"

