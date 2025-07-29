from __future__ import annotations

from typing import Dict

import pandas as pd
from flask import Flask, render_template, request

from components.file_parser import load_workbook

app = Flask(__name__, static_folder="assets", template_folder="templates")
workbook_data: Dict[str, "pd.DataFrame"] = {}


@app.route("/", methods=["GET", "POST"])
def index():
    global workbook_data
    if request.method == "POST" and "workbook" in request.files:
        file = request.files["workbook"]
        if file.filename:
            workbook_data = load_workbook(file)
    return render_template("index.html", workbook=workbook_data)


if __name__ == "__main__":
    app.run(debug=True)
