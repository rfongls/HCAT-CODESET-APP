# HCAT-CODESET-APP

This repository contains the initial scaffold for the **Codeset Automation App**.
The goal of this application is to provide a web interface for uploading and
editing multi-sheet Excel workbooks that define various codesets.

## Running the UI

The application now uses [Flask](https://flask.palletsprojects.com/) for the web interface. Install the required packages and start the server with:

```bash
python codeset_ui_app/utils/dependency_setup.py
python codeset_ui_app/app.py
```

The `dependency_setup.py` helper installs all Python packages required by the
project.

Upload a codeset workbook (`.xlsx`) and each sheet will be displayed in its own tab as an editable table.


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
```

****CODEX READ HERE, THEN UPDATE READ ME****
# 📦 Codex Handoff: Codeset Automation App (Phase 1 UI Builder)

## 🧭 Objective

Build the foundational UI for the **Codeset Automation App** using Python (FLASK preferred). The purpose is to:

* Upload and parse a multi-tab Excel workbook
* Display each sheet as an editable table
* Support dynamic column headers per tab
* Respect formulas or dropdown logic in certain columns
* Use white and purple as the primary UI theme

---

## 📁 Input File

* Excel file: `(Health System) Codeset Template (Nexus Engine v4).xlsx`
* Contains 47 sheets (e.g., `CS_ADMIN_GENDER`, `CS_ORDER_STATUS`, etc.)
* Each sheet = one codeset table
* Column headers vary across sheets

---

## 🧩 Core Features to Build

### 1. **File Upload and Parsing**

* Upload `.xlsx` file
* Detect all sheets
* Read top rows of each sheet using `pandas` / `openpyxl`

### 2. **Tabbed Interface per Sheet**

* Render each sheet as a separate tab in the UI
* Display contents of each sheet using editable tables (e.g., `streamlit-aggrid`)

### 3. **Editable Table Behavior**

* Dynamic columns: load whatever columns exist in each tab
* Support:

  * Cell editing
  * Add/remove rows
  * Drag/drop row reordering

### 4. **Special Handling for Key Fields**

* `CODE`: Free text field (client-provided values)
* `DISPLAY VALUE`: Free text (expected label)
* `STANDARD_DESCRIPTION` and `MAPPED_STD_DESCRIPTION` (if present):

  * Convert to **dropdown menus** (values sourced from a reference map OR extracted from formula validation lists in Excel)

### 5. **Preserve Excel Formulas or Validation Lists**

* If formulas or dropdowns exist in the original workbook, detect them using `openpyxl`:

  * For dropdowns: extract allowed values
  * For formulas: extract or safely ignore if not needed in UI

### 6. **Export Functionality**

* Allow user to export modified codesets back into Excel
* Keep sheet names consistent
* Re-apply dropdowns if possible using `xlsxwriter` or `openpyxl`

### 7. **Theming**

* UI should follow a **white + purple** color palette
* This includes buttons, section headers, and selected rows

---

---


## ✅ Future Additions (Do Not Build Yet)

* Login system
* Repository selection
* Approval workflow
* Shared reference repository


