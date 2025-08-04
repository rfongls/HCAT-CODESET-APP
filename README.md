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

The development server runs with the Flask reloader disabled to avoid an
initial connection reset when loading workbooks. You can also run
`utils/dependency_setup.py` to install the packages individually when network
access is available.

Upload a codeset workbook (`.xlsx`). After uploading, choose a sheet from the dropdown at the top of the page. Only the selected sheet's table is shown along with an **Add Row** button. A sidebar on the right displays guidance such as "If CODE is populated, Display Value must be populated" and will later surface validation results. The table spans the available width and scrolls vertically so long lists remain readable.

At startup the application scans the `Samples` directory for folders containing `Codeset*.xlsx` workbooks and caches the results. These parent folders appear in a repository dropdown so you can open an existing workbook without uploading it and subsequent visits do not rescan the filesystem.

When a sheet includes both `Mapped Standard Description` and `Sub Definition` columns, the mapped description column is rendered as a dropdown. Its options come from the sheet's `Standard Description` values and any Excel validations. Selecting a value automatically fills the corresponding `Sub Definition` cell as `code^description` when `Standard Code` and `Standard Description` columns are present.

If a repository workbook is already loaded, an **Import Workbook** button appears beside the export button. Choosing a file replaces the existing workbook on disk and reloads it in the interface so fresh EMR exports or offline edits can be pulled into the app without restarting. When exporting, the application writes to a temporary file and atomically replaces the original so edits overwrite the source workbook safely.

Once a workbook is loaded, a **Load Comparison** form becomes available to load a second repository workbook side by side. The current repository is excluded from the comparison list. The comparison workbook's `CODE`, `DISPLAY VALUE`, and `MAPPED_STD_DESCRIPTION` columns are inserted next to the base sheet as read-only fields with yellow cells and teal headers. Use **End Comparison** to remove these extra columns and return to single-workbook editing.

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
