from __future__ import annotations

from typing import List

from flask import Flask, render_template, request

from components.file_parser import load_workbook

app = Flask(__name__, static_folder="assets", template_folder="templates")


@app.route("/", methods=["GET", "POST"])
def index():
    sheet_names: List[str] = []
    if request.method == "POST" and "workbook" in request.files:
        file = request.files["workbook"]
        if file.filename:
            workbook = load_workbook(file)
            sheet_names = list(workbook.keys())
    return render_template("index.html", sheet_names=sheet_names)


if __name__ == "__main__":
    app.run(debug=True)
