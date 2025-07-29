# HCAT-CODESET-APP

This repository contains the initial scaffold for the **Codeset Automation App**.
The goal of this application is to provide a web interface for uploading and
editing multi-sheet Excel workbooks that define various codesets.

## Running the UI

The application uses [Flask](https://flask.palletsprojects.com/) for the web interface. Dependencies are installed automatically **before** the rest of the app imports, or you can run the helper script manually. Start the server with:

```bash
python codeset_ui_app/app.py
```

The `dependency_setup.py` helper installs all Python packages required by the project and is invoked automatically by `app.py` on startup.

Upload a codeset workbook (`.xlsx`). Use the search box to type a sheet name or pick one from the suggestions to view its table. Any dropdown validations detected in the workbook are listed below the table, along with formulas discovered in the first data row of each sheet for reference.
When a sheet includes both `Mapped Standard Description` and `Sub Definition` columns, the table shows a dropdown for the mapped description. Changing it automatically fills the corresponding `Sub Definition` cell using mappings detected in the workbook.


Dropdown lists are read from Excel data validations. The parser handles named ranges and cell ranges, ignoring broken references gracefully.

To try the app with mock data, copy `codeset template.xlsx` into the
`Samples` directory and upload that file from the web interface.


## Project Structure

```
codeset_ui_app/
├── app.py                 # Flask entry point
├── components/
│   ├── dropdown_logic.py  # Extract dropdown validations from Excel
│   ├── file_parser.py     # Workbook loading utilities
│   └── formula_logic.py   # Parse example formulas
├── utils/
│   ├── export_excel.py    # (stub) workbook export helpers
│   └── dependency_setup.py # Auto installs required packages
├── assets/
│   └── styles.css         # White and purple theme
├── templates/
│   └── index.html         # Basic Flask template
requirements.txt           # Package list
Samples/
    README.md              # Location for `codeset template.xlsx`
```
