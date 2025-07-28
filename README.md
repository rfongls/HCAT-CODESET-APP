# HCAT-CODESET-APP

This repository contains the initial scaffold for the **Codeset Automation App**.
The goal of this application is to provide a web interface for uploading and
editing multi-sheet Excel workbooks that define various codesets.

## Running the UI

The UI is built with [Streamlit](https://streamlit.io/). To run it locally:

```bash
pip install streamlit pandas openpyxl xlsxwriter streamlit-aggrid
streamlit run codeset_ui_app/app.py
```

Once started, upload a codeset workbook (``.xlsx``) and each sheet will be
rendered in its own tab as an editable table.

## Project Structure

```
codeset_ui_app/
├── app.py                 # Streamlit entry point
├── components/
│   ├── sheet_tabs.py      # Renders sheet tabs and editable tables
│   ├── dropdown_logic.py  # (stub) dropdown extraction helpers
│   └── file_parser.py     # Workbook loading utilities
├── utils/
│   └── export_excel.py    # (stub) workbook export helpers
├── assets/
│   └── styles.css         # White and purple theme
```
