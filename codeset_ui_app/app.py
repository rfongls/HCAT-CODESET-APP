from __future__ import annotations
from typing import Dict
from utils.dependency_setup import ensure_installed

ensure_installed()

import pandas as pd
from flask import Flask, render_template, request
from components.file_parser import load_workbook
from components.dropdown_logic import extract_dropdown_options
from components.formula_logic import extract_column_formulas

app = Flask(__name__, static_folder="assets", template_folder="templates")
workbook_data: Dict[str, "pd.DataFrame"] = {}
dropdown_data: Dict[str, Dict[str, list]] = {}
formula_data: Dict[str, Dict[str, str]] = {}

last_error: str | None = None


@app.route("/", methods=["GET", "POST"])
def index():
    global workbook_data
    global dropdown_data
    global formula_data
    global last_error
    if request.method == "POST" and "workbook" in request.files:
        file = request.files["workbook"]
        if file.filename:
            try:
                workbook_data = load_workbook(file)
                dropdown_data = extract_dropdown_options(file)
                formula_data = extract_column_formulas(file)
                last_error = None
            except Exception as exc:
                last_error = str(exc)
                workbook_data = {}
                dropdown_data = {}
                formula_data = {}

    return render_template(
        "index.html",
        workbook=workbook_data,
        dropdowns=dropdown_data,
        formulas=formula_data,
        error=last_error,
    )

if __name__ == "__main__":
    app.run(debug=True)
