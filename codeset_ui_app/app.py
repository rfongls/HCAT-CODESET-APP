from __future__ import annotations

from typing import Dict

import pandas as pd
from flask import Flask, render_template, request

from components.file_parser import load_workbook
from utils.dependency_setup import ensure_installed

ensure_installed()

app = Flask(__name__, static_folder="assets", template_folder="templates")
workbook_data: Dict[str, "pd.DataFrame"] = {}
last_error: str | None = None


@app.route("/", methods=["GET", "POST"])
def index():
    global workbook_data
    global last_error
    if request.method == "POST" and "workbook" in request.files:
        file = request.files["workbook"]
        if file.filename:
            try:
                workbook_data = load_workbook(file)
                last_error = None
            except Exception as exc:
                last_error = str(exc)
                workbook_data = {}
    return render_template("index.html", workbook=workbook_data, error=last_error)


if __name__ == "__main__":
    app.run(debug=True)
