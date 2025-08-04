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

Upload a codeset workbook (`.xlsx`). After uploading, choose a sheet from the dropdown at the top of the page. Only the selected sheet's table is shown along with an **Add Row** button. A sidebar on the right shows a **Fields** panel describing which HL7 fields populate the `Code` column for the current tab (taken from comments on the workbook's `Code` header), followed by a **Requirements** panel that summarizes validation rules and an **Errors** panel that lists issues as you edit (e.g., “On tab *CS_RACE* - Code X does not have a display value”). The table spans the available width and scrolls vertically so long lists remain readable.

At startup the application scans the `Samples` directory for folders containing `Codeset*.xlsx` workbooks and caches the results. These parent folders appear in a repository dropdown so you can open an existing workbook without uploading it and subsequent visits do not rescan the filesystem.

When a sheet includes both `Mapped Standard Description` and `Sub Definition` columns, the mapped description column is rendered as a dropdown. Its options come from the sheet's `Standard Description` values and any Excel validations. Selecting a value automatically fills the corresponding `Sub Definition` cell as `code^description` when `Standard Code` and `Standard Description` columns are present.

If a `Definition` column exists in the workbook it is preserved in the export but hidden from the web interface.


If a repository workbook is already loaded, an **Import Workbook** button appears beside the export button. Choosing a file replaces the existing workbook on disk and reloads it in the interface so fresh EMR exports or offline edits can be pulled into the app without restarting. When exporting, the application writes to a temporary file and atomically replaces the original so edits overwrite the source workbook safely.

Once a workbook is loaded, a comparison form becomes available to load a second repository workbook side by side. The current repository is excluded from the comparison list. When active, the form shows the selected repository and workbook and provides a **Clear Comparison** button to remove the extra columns and return to single-workbook editing. The comparison workbook's `CODE`, `DISPLAY VALUE`, and `MAPPED_STD_DESCRIPTION` columns are inserted next to the base sheet as read-only fields with yellow cells and teal headers.

Dropdown lists are read from Excel data validations. The parser handles named ranges and cell ranges, ignoring broken references gracefully.

To try the app with mock data, copy `codeset template.xlsx` into the
`Samples` directory and upload that file from the web interface.

### Validation Rules

During export the application validates all loaded sheets and refuses to write a
workbook until issues are resolved. The checks include:

- `DISPLAY VALUE` is required whenever a `CODE` is provided and vice versa.
- If either `STANDARD_CODE` or `STANDARD_DESCRIPTION` contains a value, the
  `MAPPED_STD_DESCRIPTION` column must also be filled in.
- If `MAPPED_STD_DESCRIPTION` is populated, both `CODE` and `DISPLAY VALUE`
  must also be provided.
- Duplicate `CODE` values on a sheet are reported with the offending row
  numbers.

Errors surface in the sidebar while editing and are also returned from the
`/export` endpoint when using the JSON API.

### API Endpoints

The Flask server exposes a small JSON API alongside the HTML interface:

- `GET /workbooks/<repo>` – list `Codeset*.xlsx` files discovered in a
  repository directory.
- `GET /sheet/<sheet>` – return the current sheet's rows, including comparison
  columns when a comparison workbook is loaded.
- `POST /export` – validate and write the in-memory workbook back to disk,
  returning the updated file or validation errors.
- `POST /import` – replace the loaded workbook on disk with an uploaded file
  and reload it into the interface.

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

## Codex Utilities

Beyond the web app, the repository includes a `codex` package containing
spreadsheet definitions and additional validators. The
`codex.validators.validate_codeset_tab_logic` helper reads a codeset workbook and
checks each sheet against the rules in
`codex/spreadsheet_definitions/codex-spreadsheet-definition.md`, reporting
whether mapping is required and if expected formulas are present.

```bash
python -m codex.validators.validate_codeset_tab_logic path/to/workbook.xlsx
```

## Running Tests

After installing the dependencies, run the full test suite with:

```bash
pytest
```
