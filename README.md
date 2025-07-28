# HCAT-CODESET-APP

This repository contains the initial scaffold for the **Codeset Automation App**.
The goal of this application is to provide a web interface for uploading and
editing multi-sheet Excel workbooks that define various codesets.

## Running the UI

The primary UI is built with [Streamlit](https://streamlit.io/). Dependencies can
be installed automatically using the helper script:

```bash
python codeset_ui_app/utils/dependency_setup.py
streamlit run codeset_ui_app/app.py
```

Once started, upload a codeset workbook (`.xlsx`) and each sheet will be
rendered in its own tab as an editable table.

A minimal [Flask](https://flask.palletsprojects.com/) entry point is also
provided if you need a traditional HTML template. Run it with:

```bash
python codeset_ui_app/flask_app.py
```

## Project Structure

```
codeset_ui_app/
├── app.py                 # Streamlit entry point
├── flask_app.py           # Optional Flask entry
├── components/
│   ├── sheet_tabs.py      # Renders sheet tabs and editable tables
│   ├── dropdown_logic.py  # (stub) dropdown extraction helpers
│   └── file_parser.py     # Workbook loading utilities
├── utils/
│   ├── export_excel.py     # (stub) workbook export helpers
│   └── dependency_setup.py # Auto installs required packages
├── assets/
│   └── styles.css         # White and purple theme
├── templates/
│   └── index.html         # Basic Flask template
requirements.txt           # Package list
```
