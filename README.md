# HCAT-CODESET-APP

This repository contains the initial scaffold for the **Codeset Automation App**.
The goal of this application is to provide a web interface for uploading and
editing multi-sheet Excel workbooks that define various codesets.

## Running the UI

The application uses [Flask](https://flask.palletsprojects.com/) for the web interface and [Bootstrap 5](https://getbootstrap.com/) for responsive styling. Install dependencies from `requirements.txt` and start the server with:

```bash
pip install -r requirements.txt
python codeset_ui_app/app.py
```

You can also run `utils/dependency_setup.py` to install the packages individually when network access is available.

Upload a codeset workbook (`.xlsx`). After uploading, choose a sheet from the dropdown at the top of the page. Only the selected sheet's table is shown along with an **Add Row** button. Any dropdown validations detected in the workbook are listed below the table along with formulas discovered in the first data row.

The application also scans the `Samples` directory for folders containing `Codeset*.xlsx` workbooks. These parent folders appear in a repository dropdown so you can open an existing workbook without uploading it.

When a sheet includes both `Mapped Standard Description` and `Sub Definition` columns, the mapped description column is rendered as a dropdown. Its options come from the sheet's `Standard Description` values and any Excel validations. Selecting a value automatically fills the corresponding `Sub Definition` cell. If the workbook uses simple `VLOOKUP` formulas to populate the sub definition, those lookup tables are read and used for this automatic fill behavior. When `Standard Code` and `Standard Definition` columns are present the sub-definition is derived from them as `code^definition` whenever a mapped description is selected.



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
│   └── dependency_setup.py # Optional helper to install packages
├── assets/
│   └── styles.css         # White and purple theme
├── templates/
│   └── index.html         # Basic Flask template
requirements.txt           # Package list
Samples/
    README.md              # Location for `codeset template.xlsx`
```
