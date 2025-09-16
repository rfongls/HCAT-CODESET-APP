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

On Windows, a convenience script `run-ui.bat` is included at the project root. Double‑clicking it starts the Flask server and opens your default browser to the app.

The development server runs with the Flask reloader disabled to avoid an
initial connection reset when loading workbooks. You can also run
`utils/dependency_setup.py` to install the packages individually when network
access is available.

Upload a codeset workbook (`.xlsx`). After uploading, choose a sheet from the dropdown at the top of the page. Only the selected sheet's table is shown along with an **Add Row** button. A sidebar on the right shows a **Codeset References** panel that lists the HL7 field location, a description, expected data type, and NBR table number for the current tab (sourced from the `codex-spreadsheet-definition.md` reference file). This is followed by a **Requirements** panel summarizing validation rules and an **Errors** panel that lists issues as you edit (e.g., “On tab *CS_RACE* - Code X does not have a display value”). You can download these messages as a CSV via the **Download Error Report** button beneath the panel. The table spans the available width and scrolls vertically so long lists remain readable.

Click **Export Workbook** to persist your edits back to the original file in its repository without triggering a download prompt.

At startup the application scans the `Samples` directory for folders containing `Codeset*.xlsx` workbooks and caches the results. These parent folders appear in a repository dropdown so you can open an existing workbook without uploading it and subsequent visits do not rescan the filesystem.

When a sheet includes both `Mapped Standard Description` and `Sub Definition` columns, the mapped description column is rendered as a dropdown. Its options come from the sheet's `Standard Description` values and any Excel validations. Selecting a value automatically fills the corresponding `Sub Definition` cell as `code^description` when `Standard Code` and `Standard Description` columns are present.

If a `Definition` column exists in the workbook it is preserved in the export but hidden from the web interface.


If a repository workbook is already loaded, an **Import Workbook** button appears beside the export button. Choosing a file replaces the existing workbook on disk and reloads it in the interface so fresh EMR exports or offline edits can be pulled into the app without restarting. When exporting, the application writes to a temporary file and atomically replaces the original so edits overwrite the source workbook safely without prompting a download; the updated file is stored in the same repository directory.

Once a workbook is loaded, a **Compare** button appears next to the **Load Workbook** control. Clicking it reveals a form for loading a second repository workbook side by side. The current repository is excluded from the comparison list. When a comparison is active, the form displays the chosen repository and workbook along with a **Clear Comparison** button to return to single-workbook editing. The comparison workbook's `CODE`, `DISPLAY VALUE`, and `MAPPED_STD_DESCRIPTION` columns are inserted next to the base sheet as read-only fields with yellow cells and teal headers.
The selected repository and workbook fields—both primary and comparison—are highlighted in yellow so current choices are easy to spot.

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
- `POST /export` – validate and overwrite the in-memory workbook on disk,
  returning a JSON status or validation errors.
- `POST /export_errors` – run validation and return a CSV file listing all
  detected errors for the provided workbook data.
- `POST /import` – replace the loaded workbook on disk with an uploaded file
  and reload it into the interface.

## Project Structure

The repository is organized into the following directories:

```
HCAT-CODESET-APP/
├── codeset_ui_app/               # Flask-based web interface for editing workbooks
│   ├── app.py                    # Application entry point
│   ├── assets/                   # Static CSS and other assets
│   ├── components/               # Excel parsing and dropdown logic helpers
│   ├── samples/                  # Example workbook used in demos
│   ├── templates/                # HTML templates
│   └── utils/                    # Export helpers and dependency scripts
├── codex/                        # Reusable spreadsheet definitions and validators
│   ├── agents/                   # Experimental agent utilities
│   ├── spreadsheet_definitions/  # Markdown spec for codeset columns
│   ├── validators/               # Workbook validation logic
│   └── tests/                    # Unit tests for the codex package
├── Samples/                      # Sample repositories of Codeset workbooks
├── tests/                        # Pytest suite covering the Flask interface
├── codex-spreadsheet-definition.md # Central codex reference document
├── codexhandoff.md               # Notes for handing off the codex module
├── enhancements.md               # Ideas and future enhancements
├── project-proposal.md           # Original project planning document
└── requirements.txt              # Python dependencies
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

## Packaging with PyInstaller

To distribute the application without requiring Python, you can bundle it with [PyInstaller](https://pyinstaller.org/). The `build_executable.py` helper now picks a sensible default bundle for the current operating system and exposes switches for the less common cases.

### Install the build dependencies

```bash
pip install -r requirements.txt pyinstaller
```

### Build with the helper script

Run the build script without arguments from a terminal in the project root:

```bash
python build_executable.py
```

The default `--bundle-mode auto` chooses the most typical output for the host platform:

- **Windows / Linux:** single-file executable at `dist/codeset_app.exe` (Windows) or `dist/codeset_app` (Linux).
- **macOS:** Finder-ready `.app` bundle at `dist/codeset_app.app`.

The bundle already includes the templates, static assets, and hidden imports (such as `codeset_ui_app.utils.xlsx_sanitizer`) that PyInstaller needs to discover manually.

Use `--bundle-mode onefile` or `--bundle-mode onedir` to override the default. When you request `onedir` on macOS the helper automatically adds PyInstaller's `--windowed` option so the output is a clickable `.app` bundle instead of a console binary. On Windows or Linux, `onedir` produces a folder containing the platform-native executable.

### macOS-specific options

Run the script on a macOS machine; PyInstaller cannot cross-compile for macOS. Optional arguments tailor the bundle further:

```bash
# Create a universal binary for macOS 11+
python build_executable.py --bundle-mode onedir --target-arch universal2

# Zip the generated .app bundle for easier sharing
python build_executable.py --bundle-mode onedir --archive codeset_app-macos
```

Launch the `.app` via Finder or with `open dist/codeset_app.app`. If you need logs, run the binary nested inside the bundle:

```bash
./dist/codeset_app.app/Contents/MacOS/codeset_app
```

### No Mac? Build on GitHub Actions

GitHub-hosted macOS runners can build the `.app` bundle for you—no self-hosted hardware required. The repository includes a manual workflow that runs `build_executable.py` remotely:

1. Push your branch to GitHub and ensure Actions are enabled for the repository.
2. In the **Actions** tab, trigger **Build macOS App Bundle**.
3. Accept the default architecture of **auto** or choose a specific option such as `universal2` when you need both Apple Silicon and Intel binaries.
4. Download the `codeset_app-macos.zip` artifact once the workflow finishes and extract it locally to retrieve the `.app` bundle.

Prefer the command line? Install the [GitHub CLI](https://cli.github.com/) and run:

```bash
gh workflow run "Build macOS App Bundle" --field target_arch=auto
```

Replace `auto` with a specific architecture when needed. After the workflow completes, use `gh run download` (or revisit the Actions tab) to fetch the `codeset_app-macos.zip` artifact. If your organisation disables GitHub-hosted macOS runners you will need to supply a Mac (locally or as a self-hosted runner) to build the bundle.

### Running PyInstaller manually

You can still invoke PyInstaller directly when you need finer control:

```bash
pyinstaller codeset_ui_app/app.py --onefile --name codeset_app ^
 --add-data "codeset_ui_app/assets;assets" ^
 --add-data "codeset_ui_app/templates;templates" ^
 --hidden-import codeset_ui_app.utils.xlsx_sanitizer
```

Adjust the `^` line continuations for your shell if not using `cmd.exe` and
replace the semicolons with colons on macOS or Linux. When building on macOS and
you want a `.app` bundle, add `--windowed` and drop `--onefile` so PyInstaller
creates `dist/codeset_app.app` instead of a single console executable.

Double-clicking the resulting executable launches the Flask app just like `python app.py`.
