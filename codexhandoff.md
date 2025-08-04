Certainly. Here's a full Codex handoff instruction for referencing the workbook, validating mapping logic, and ensuring that all logic derives from the authoritative markdown file: `codex-spreadsheet-definition.md`.

---

## 🧩 Codex Integration Handoff: Codeset Template Validation & Agent Reference

### 🔗 Source Files

* **Spreadsheet to Process:**
  `codeset_ui_app/samples/Codeset Template.xlsx`

* **Reference Definition File:**
  `codex-spreadsheet-definition.md`

This markdown file contains authoritative rules regarding:

* Which tabs require mapped standard descriptions.
* The presence and structure of formulas.
* Conditional enforcement based on actual data (not just headers).

---

### ✅ Objective

Create the following components in Codex:

---

### 1. **Validation Node: `validate_codeset_tab_logic`**

This node performs sheet-level validation logic as defined in `codex-spreadsheet-definition.md`.

#### Responsibilities:

* Open `Codeset Template.xlsx` using `pandas` or `openpyxl`.
* For each sheet:

  * Confirm if `STANDARD_CODE` and `STANDARD_DESCRIPTION` columns exist and contain data.
  * If both exist and contain values, ensure `MAPPED_STD_DESCRIPTION` is not null.
  * If formulas are present (column `D`), confirm the formula output matches the logic in the markdown spec (e.g., `UNK^UNKNOWN`, etc).

#### Output:

```json
{
  "sheet_name": "CS_RACE",
  "requires_mapping": true,
  "missing_mapped_std_descriptions": 2,
  "formula_issues": []
}
```

---

### 2. **Reference Agent: `codeset_context_agent`**

This is a persistent agent (or knowledge reference) for any logic or UI behavior referencing the codeset UI or imported Excel workbooks.

#### Behavior:

* On interaction with `codeset_ui_app/samples/Codeset Template.xlsx`, it:

  * Loads and references `codex-spreadsheet-definition.md` as a grounding document.
  * Injects context from that file before prompting the user for any new mapping action.
  * Uses the file to inform dropdown population, enforcement logic, and validation criteria.

#### Notes:

* If a new codeset template is added, this agent should confirm if a corresponding `.md` definition exists and validate it first.
* This agent acts as a **single source of truth** for how `MAPPED_STD_DESCRIPTION` and formulas behave in the UI.
* When a mapped description is chosen, the agent ensures the `SUB_DEFINITION` cell contains `STANDARD_CODE^STANDARD_DESCRIPTION`.
  The workbook may label this column as either `SUB_DEFINITION` or `SUBDEFINITION`.
* `SUB_DEFINITION` is read-only and auto-populated. `MAPPED_STD_DESCRIPTION` pulls its options from `STANDARD_DESCRIPTION`, and selecting a value automatically fills the `SUB_DEFINITION` cell with the code and description pair.
* Rows lacking entries for both `CODE` and `DISPLAY VALUE` remain visible so the full list of `STANDARD_CODE` and `STANDARD_DESCRIPTION` values is viewable; their `MAPPED_STD_DESCRIPTION` and `SUB_DEFINITION` cells start blank until a value is chosen.
* The application parses the workbook once and renders only the requested sheet, fetching other tabs on demand to avoid UI hangs on large files.
* Tables stretch to their natural width and include a vertical scrollbar so long sheets remain readable without shrinking columns.
* Empty columns are preserved during parsing so each sheet's expected headers remain available even when no data exists for a column.
* A dedicated export routine writes changes to a temporary file and atomically replaces the original workbook on disk, retaining the original name and formatting while also returning it for download if needed.
* An import endpoint lets users replace the currently loaded workbook with a new file so EMR exports or offline edits can be pulled in without restarting the session.
* The web UI scans the `Samples` directory for folders containing `Codeset*.xlsx` files and offers those parent folders as repositories so users can choose an existing workbook instead of uploading.
* A comparison mode lets a second workbook be loaded from a repository. Its `CODE`, `DISPLAY VALUE`, and `MAPPED_STD_DESCRIPTION` columns appear read-only alongside the active workbook. Users can end the comparison to remove the extra columns.
* Repository and workbook listings are cached when the server starts, allowing users to immediately select a repository without waiting for a filesystem scan.
* The interface shows a sidebar that lists validation errors in real time, referencing the sheet and row for issues such as missing code/display pairs, required mappings, or duplicate codes. When no errors exist it displays guidance, e.g., "If CODE is populated, Display Value must be populated".


---

### 🧪 Optional Test Task

Include a test routine in `tests/test_validation.py` that:

* Loads the `Codeset Template.xlsx`
* Applies `validate_codeset_tab_logic`
* Confirms all sheets expected to require mappings do so
* Fails gracefully on sheets that omit standard fields (and ensures no enforcement applied)

---

### 📂 Folder Integration

Suggested layout:

```
codex/
├── spreadsheet_definitions/
│   └── codex-spreadsheet-definition.md
├── validators/
│   └── validate_codeset_tab_logic.py
├── agents/
│   └── codeset_context_agent.py
└── tests/
    └── test_validation.py
```

Let me know if you’d like scaffold code for the validator or agent setup.
