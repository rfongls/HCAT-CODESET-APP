from __future__ import annotations
from typing import Dict, Any
import pandas as pd
from flask import Flask, render_template, request
from components.file_parser import load_workbook
from components.dropdown_logic import extract_dropdown_options
from components.formula_logic import (
    extract_column_formulas,
    extract_lookup_mappings,
)

app = Flask(__name__, static_folder="assets", template_folder="templates")
workbook_data: Dict[str, "pd.DataFrame"] = {}
dropdown_data: Dict[str, Dict[str, list]] = {}
formula_data: Dict[str, Dict[str, str]] = {}
mapping_data: Dict[str, Dict[str, Any]] = {}
last_error: str | None = None


@app.route("/", methods=["GET", "POST"])
def index():
    global workbook_data
    global dropdown_data
    global formula_data
    global last_error
    global mapping_data
    mapping_data = {}

    if request.method == "POST" and "workbook" in request.files:
        file = request.files["workbook"]
        if file.filename:
            try:
                workbook_data = load_workbook(file)
                dropdown_data = extract_dropdown_options(file)
                formula_data = extract_column_formulas(file)
                lookup_maps = extract_lookup_mappings(file)

                for sheet, df in workbook_data.items():
                    mapped_col = None
                    sub_col = None
                    std_col = None

                    for col in df.columns:
                        col_key = col.upper().replace(" ", "_")
                        if col_key in ["MAPPED_STANDARD_DESCRIPTION", "MAPPED_STD_DESCRIPTION"]:
                            mapped_col = col
                        if col_key in ["SUB_DEFINITION", "SUB_DEFINITION_DESCRIPTION"]:
                            sub_col = col
                        if col_key in ["STANDARD_DESCRIPTION", "STD_DESCRIPTION", "STANDARD_DESC"]:
                            std_col = col
                    if std_col and mapped_col:
                        options = sorted({str(v) for v in df[std_col].dropna() if str(v).strip()})
                        dropdown_data.setdefault(sheet, {})[mapped_col] = options
                    sheet_map = {}
                    if mapped_col and sub_col:
                        for _, row in df[[mapped_col, sub_col]].dropna().iterrows():
                            sheet_map[str(row[mapped_col])] = str(row[sub_col])
                    # Merge lookup-based mappings if available
                    lookup_sheet = lookup_maps.get(sheet, {})
                    if sub_col and sub_col in lookup_sheet:
                        sheet_map = {**lookup_sheet[sub_col], **sheet_map}

                    mapping_data[sheet] = {
                        "map": sheet_map,
                        "sub_col": sub_col,
                        "mapped_col": mapped_col,
                    }

                last_error = None
            except Exception as exc:
                last_error = str(exc)
                workbook_data = {}
                dropdown_data = {}
                formula_data = {}
                mapping_data = {}
    workbook_headers: Dict[str, list] = {s: df.columns.tolist() for s, df in workbook_data.items()}
    workbook_records: Dict[str, list] = {s: df.to_dict(orient="records") for s, df in workbook_data.items()}
    return render_template(
        "index.html",
        workbook=workbook_records,
        headers=workbook_headers,
        dropdowns=dropdown_data,
        formulas=formula_data,
        mappings=mapping_data,
        error=last_error,
    )

if __name__ == "__main__":
    app.run(debug=True)
