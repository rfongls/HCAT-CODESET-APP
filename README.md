# HCAT-CODESET-APP

This repository contains the initial scaffold for the **Codeset Automation App**.
The goal of this application is to provide a web interface for uploading and
editing multi-sheet Excel workbooks that define various codesets.

## Running the UI

The application uses [Flask](https://flask.palletsprojects.com/) for the web interface. Dependencies are installed automatically when the app starts, or you can run the helper script manually. Start the server with:

```bash
python codeset_ui_app/app.py
```

The `dependency_setup.py` helper installs all Python packages required by the project and is invoked automatically by `app.py` on startup.

Upload a codeset workbook (`.xlsx`) and each sheet will be displayed in its own tab as an editable table.

The repository also includes a `Samples` directory. Place the sample workbook
`codeset template.xlsx` in this folder if you would like to experiment with the
app using mock data.


## Project Structure

```
codeset_ui_app/
├── app.py                 # Flask entry point
├── components/
│   ├── dropdown_logic.py  # (stub) dropdown extraction helpers
│   └── file_parser.py     # Workbook loading utilities
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
