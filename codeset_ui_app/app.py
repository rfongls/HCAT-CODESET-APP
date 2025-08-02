from __future__ import annotations
from typing import Dict, Any
from pathlib import Path
import tempfile

import pandas as pd
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from components.file_parser import load_workbook
from components.dropdown_logic import extract_dropdown_options
from components.formula_logic import (
    extract_column_formulas,
    extract_lookup_mappings,
)
from utils.export_excel import export_workbook
from openpyxl.workbook.workbook import Workbook

app = Flask(__name__, static_folder="assets", template_folder="templates")
workbook_data: Dict[str, "pd.DataFrame"] = {}
dropdown_data: Dict[str, Dict[str, list]] = {}
formula_data: Dict[str, Dict[str, str]] = {}
mapping_data: Dict[str, Dict[str, Any]] = {}
workbook_obj: Workbook | None = None
original_filename: str | None = None
workbook_path: Path | None = None
last_error: str | None = None


@app.route("/", methods=["GET", "POST"])
def index():
    global workbook_data
    global dropdown_data
    global formula_data
    global last_error
    global mapping_data
    global workbook_obj
    global original_filename
    global workbook_path
    mapping_data = {}
    if request.method == "POST" and "workbook" in request.files:
        file = request.files["workbook"]
        if file.filename:
            try:
                filename = secure_filename(file.filename)
                temp_dir = Path(tempfile.gettempdir())
                workbook_path = temp_dir / filename
                file.save(workbook_path)
                with workbook_path.open("rb") as fh:
                    workbook_data, wb = load_workbook(fh)
                workbook_obj = wb
                original_filename = filename
                dropdown_data = extract_dropdown_options(wb)
                formula_data = extract_column_formulas(wb)
                lookup_maps = extract_lookup_mappings(wb)

                for sheet, df in list(workbook_data.items()):
                    mapped_col = None
                    sub_col = None
                    std_col = None
                    std_code_col = None
                    code_col = None
                    display_col = None
                    for col in df.columns:
                        col_key = col.upper().replace(" ", "_")
                        if col_key in ["MAPPED_STANDARD_DESCRIPTION", "MAPPED_STD_DESCRIPTION"]:
                            mapped_col = col
                        if col_key in ["SUB_DEFINITION", "SUB_DEFINITION_DESCRIPTION", "SUBDEFINITION", "SUB DEFINITION"]:
                            sub_col = col
                        if col_key in ["STANDARD_DESCRIPTION", "STD_DESCRIPTION", "STANDARD_DESC"]:
                            std_col = col
                        if col_key in ["STANDARD_CODE", "STD_CODE"]:
                            std_code_col = col
                        if col_key == "CODE":
                            code_col = col
                        if col_key in ["DISPLAY_VALUE", "DISPLAY"]:
                            display_col = col

                    if std_col and mapped_col:
                        options = sorted({str(v).strip() for v in df[std_col] if str(v).strip()})
                        if options:
                            dropdown_data.setdefault(sheet, {})[mapped_col] = options

                    sheet_map = {}

                    if std_col and std_code_col:
                        std_series = df[std_col].astype(str).str.strip()
                        code_series = df[std_code_col].astype(str).str.strip()
                        mask = std_series != ""
                        sheet_map.update(
                            {
                                desc: f"{code}^{desc}"
                                for desc, code in zip(std_series[mask], code_series[mask])
                            }
                        )

                    if mapped_col and not (std_col and std_code_col) and sub_col:
                        mapped_series = df[mapped_col].astype(str).str.strip()
                        sub_series = df[sub_col].astype(str)
                        mask = mapped_series != ""
                        sheet_map.update({k: v for k, v in zip(mapped_series[mask], sub_series[mask])})

                    # Merge lookup-based mappings if available
                    lookup_sheet = lookup_maps.get(sheet, {})
                    if sub_col and sub_col in lookup_sheet:
                        sheet_map = {**lookup_sheet[sub_col], **sheet_map}

                    # populate sub_definition column dynamically from mapped description
                    if sub_col and mapped_col:
                        df[sub_col] = df[mapped_col].map(sheet_map).fillna(df[sub_col])

                    mapping_data[sheet] = {
                        "map": sheet_map,
                        "sub_col": sub_col,
                        "mapped_col": mapped_col,
                    }

                    # Preserve all rows so the full standard code list remains visible
                    if code_col and display_col and mapped_col:
                        code_series = df[code_col].astype(str).str.strip()
                        display_series = df[display_col].astype(str).str.strip()
                        blank_mask = code_series.eq("") & display_series.eq("")
                        if blank_mask.any():
                            df.loc[blank_mask, mapped_col] = ""
                            if sub_col:
                                df.loc[blank_mask, sub_col] = ""
                    workbook_data[sheet] = df
                last_error = None
            except Exception as exc:
                last_error = str(exc)
                workbook_data = {}
                dropdown_data = {}
                formula_data = {}
                mapping_data = {}

    sheet_names = list(workbook_data.keys())
    headers: Dict[str, list] = {s: df.columns.tolist() for s, df in workbook_data.items()}
    initial_sheet = sheet_names[0] if sheet_names else None
    initial_records = (
        workbook_data[initial_sheet].to_dict(orient="records") if initial_sheet else []
    )
    return render_template(
        "index.html",
        sheet_names=sheet_names,
        initial_sheet=initial_sheet,
        initial_records=initial_records,
        headers=headers,
        dropdowns=dropdown_data,
        formulas=formula_data,
        mappings=mapping_data,
        error=last_error,
        filename=original_filename,
    )


@app.route("/sheet/<sheet_name>", endpoint="sheet_data")
def sheet_data(sheet_name: str):
    df = workbook_data.get(sheet_name)
    if df is None:
        return jsonify([])
    return jsonify(df.to_dict(orient="records"))


@app.route("/export", methods=["POST"])
def export():
    """Export the in-memory workbook with updated values."""
    global workbook_obj, workbook_data, original_filename, workbook_path
    if workbook_obj is None or workbook_path is None:
        return "No workbook loaded", 400

    payload = request.get_json() or {}
    if not isinstance(payload, dict):
        return "Invalid payload", 400

    for sheet, rows in payload.items():
        if sheet in workbook_data:
            df = pd.DataFrame(rows, columns=workbook_data[sheet].columns)
            df = df.where(pd.notna(df), "")
            workbook_data[sheet] = df

    export_workbook(workbook_obj, workbook_data, workbook_path)
    filename = original_filename or workbook_path.name
    return send_file(
        workbook_path,
        as_attachment=True,
        download_name=filename,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

if __name__ == "__main__":
    app.run(debug=True)
