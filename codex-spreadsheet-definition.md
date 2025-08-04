# 📘 Codex Reference: Nexus Engine Codeset Template Workbook

Workbook: **(Health System) Codeset Template (Nexus Engine v4)**

Purpose: Define, normalize, and optionally map facility codes to national standards using a structured UI.

---

## 🔍 Field Summary

| Column Name                | Description |
|---------------------------|-------------|
| `CODE`                    | Local/internal code value |
| `DISPLAY VALUE`           | Human-friendly label |
| `STANDARD_CODE`           | Optional: industry-aligned code (e.g., SNOMED, HL7) |
| `STANDARD_DESCRIPTION`    | Optional: official label for standard code |
| `MAPPED_STD_DESCRIPTION`  | Dropdown-enabled field where user selects a mapped description |
| (Formula Column)          | Generates a concatenated string (e.g., `UNK^UNKNOWN`) based on mapped description |

---

## 🔁 Mapping Behavior Logic

### Mapping **is required** if:
- `STANDARD_CODE` column exists **and contains data**
- `STANDARD_DESCRIPTION` column exists **and contains data**
- `MAPPED_STD_DESCRIPTION` column exists

### Mapping **is NOT required** if:
- `STANDARD_CODE` or `STANDARD_DESCRIPTION` columns are entirely blank (even if headers exist)

---

## 🧮 Formula Logic (If Present)
Formulas, when present, are generally embedded in column `D` and follow a structure like:

```excel
=IFERROR(
  IF(F2="Unknown", "UNK^UNKNOWN",
    IF(F2="Other", "OTH^OTHER",
      IF(F2="Refused", "ASKU^ASKED BUT UNKNOWN", "")
    )
  ),
"")
```

---

## ✅ Sheet-Level Mapping & Formula Summary

| Sheet Name | Has `STANDARD_CODE` Data | Has `STANDARD_DESCRIPTION` Data | Requires Mapping Logic | Has Formula | Sample Formula |
|------------|---------------------------|----------------------------------|--------------------------|--------------|----------------|
| CS_ABNORMAL_FLAG | ✅ | ✅ | ✅ | ✅ | D2: =IFERROR(IF(F2="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F2,J:J,0)),"^",VLOOKUP(F2,J:J,1,FALSE)))),""); D3: =IFERROR(IF(F3="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F3,J:J,0)),"^",VLOOKUP(F3,J:J,1,FALSE)))),"") |
| CS_ACCIDENT_CODE | ✅ | ✅ | ✅ | ✅ | D2: =IFERROR(IF(F2="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F2,J:J,0)),"^",VLOOKUP(F2,J:J,1,FALSE)))),""); D3: =IFERROR(IF(F3="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F3,J:J,0)),"^",VLOOKUP(F3,J:J,1,FALSE)))),"") |
| CS_ACCOMMODATION | ✅ | ✅ | ✅ | ✅ | D2: =IFERROR(IF(F2="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F2,J:J,0)),"^",VLOOKUP(F2,J:J,1,FALSE)))),""); D3: =IFERROR(IF(F3="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F3,J:J,0)),"^",VLOOKUP(F3,J:J,1,FALSE)))),"") |
| CS_ADMIN_GENDER | ✅ | ✅ | ✅ | ✅ | D2: =IFERROR(IF(F2="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F2,J:J,0)),"^",VLOOKUP(F2,J:J,1,FALSE)))),""); D3: =IFERROR(IF(F3="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F3,J:J,0)),"^",VLOOKUP(F3,J:J,1,FALSE)))),"") |
| CS_ADMIT_SERVICE | ✅ | ✅ | ✅ | ✅ | D2: =IFERROR(IF(F2="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F2,J:J,0)),"^",VLOOKUP(F2,J:J,1,FALSE)))),""); D3: =IFERROR(IF(F3="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F3,J:J,0)),"^",VLOOKUP(F3,J:J,1,FALSE)))),"") |
| CS_ADMIT_SOURCE | ❌ | ❌ | ❌ | ✅ | C2: =IFERROR(IF(E2="Unknown","UNK^UNKNOWN",(CONCATENATE(VLOOKUP(E2,I:J,2,FALSE),"^",VLOOKUP(E2,I:J,1,FALSE)))),""); D2: =IFERROR(IF(F2="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F2,J:J,0)),"^",VLOOKUP(F2,J:J,1,FALSE)))),"") |
| CS_ADMIT_TYPE | ✅ | ✅ | ✅ | ✅ | D2: =IFERROR(IF(F2="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F2,J:J,0)),"^",VLOOKUP(F2,J:J,1,FALSE)))),""); D3: =IFERROR(IF(F3="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F3,J:J,0)),"^",VLOOKUP(F3,J:J,1,FALSE)))),"") |
| CS_ALLERGEN_TYPE_CODE | ❌ | ❌ | ❌ | ✅ | D2: =IFERROR(IF(F2="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F2,J:J,0)),"^",VLOOKUP(F2,J:J,1,FALSE)))),""); D3: =IFERROR(IF(F3="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F3,J:J,0)),"^",VLOOKUP(F3,J:J,1,FALSE)))),"") |
| CS_ALLERGY_REACTION_CODE | ❌ | ❌ | ❌ | ✅ | D2: =IFERROR(IF(F2="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F2,J:J,0)),"^",VLOOKUP(F2,J:J,1,FALSE)))),""); D3: =IFERROR(IF(F3="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F3,J:J,0)),"^",VLOOKUP(F3,J:J,1,FALSE)))),"") |
| CS_ALLERGY_SEVERITY_CODE | ✅ | ✅ | ✅ | ✅ | D2: =IFERROR(IF(F2="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F2,J:J,0)),"^",VLOOKUP(F2,J:J,1,FALSE)))),""); D3: =IFERROR(IF(F3="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F3,J:J,0)),"^",VLOOKUP(F3,J:J,1,FALSE)))),"") |
| CS_AVAILABILITY_STATUS | ✅ | ✅ | ✅ | ✅ | D2: =IFERROR(IF(F2="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F2,J:J,0)),"^",VLOOKUP(F2,J:J,1,FALSE)))),""); D3: =IFERROR(IF(F3="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F3,J:J,0)),"^",VLOOKUP(F3,J:J,1,FALSE)))),"") |
| CS_CITIZENSHIP | ❌ | ❌ | ❌ | ✅ | D2: =IFERROR(IF(F2="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F2,J:J,0)),"^",VLOOKUP(F2,J:J,1,FALSE)))),""); D3: =IFERROR(IF(F3="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F3,J:J,0)),"^",VLOOKUP(F3,J:J,1,FALSE)))),"") |
| CS_COMPLETION_STATUS | ✅ | ✅ | ✅ | ✅ | D2: =IFERROR(IF(F2="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F2,J:J,0)),"^",VLOOKUP(F2,J:J,1,FALSE)))),""); D3: =IFERROR(IF(F3="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F3,J:J,0)),"^",VLOOKUP(F3,J:J,1,FALSE)))),"") |
| CS_CONFIDENTIALITY_CODE | ✅ | ✅ | ✅ | ✅ | D2: =IFERROR(IF(F2="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F2,J:J,0)),"^",VLOOKUP(F2,J:J,1,FALSE)))),""); D3: =IFERROR(IF(F3="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F3,J:J,0)),"^",VLOOKUP(F3,J:J,1,FALSE)))),"") |
| CS_DIAGNOSIS_CODE_METHOD | ❌ | ❌ | ❌ | ✅ | D2: =IFERROR(IF(F2="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F2,J:J,0)),"^",VLOOKUP(F2,J:J,1,FALSE)))),""); D3: =IFERROR(IF(F3="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F3,J:J,0)),"^",VLOOKUP(F3,J:J,1,FALSE)))),"") |
| CS_DIAGNOSIS_TYPE | ✅ | ✅ | ✅ | ✅ | D2: =IFERROR(IF(F2="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F2,J:J,0)),"^",VLOOKUP(F2,J:J,1,FALSE)))),""); D3: =IFERROR(IF(F3="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F3,J:J,0)),"^",VLOOKUP(F3,J:J,1,FALSE)))),"") |
| CS_DIAGNOSTIC_SERVICE_SECTION | ❌ | ❌ | ❌ | ✅ | D2: =IFERROR(IF(F2="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F2,J:J,0)),"^",VLOOKUP(F2,J:J,1,FALSE)))),""); D3: =IFERROR(IF(F3="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F3,J:J,0)),"^",VLOOKUP(F3,J:J,1,FALSE)))),"") |
| CS_DISCHARGE_DISPOSITION | ✅ | ✅ | ✅ | ✅ | D2: =IFERROR(IF(F2="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F2,J:J,0)),"^",VLOOKUP(F2,J:J,1,FALSE)))),""); D3: =IFERROR(IF(F3="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F3,J:J,0)),"^",VLOOKUP(F3,J:J,1,FALSE)))),"") |
| CS_ENCOUNTER_CLASS | ✅ | ✅ | ✅ | ✅ | D2: =IFERROR(IF(F2="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F2,J:J,0)),"^",VLOOKUP(F2,J:J,1,FALSE)))),""); D3: =IFERROR(IF(F3="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F3,J:J,0)),"^",VLOOKUP(F3,J:J,1,FALSE)))),"") |
| CS_ENCOUNTER_TYPE | ❌ | ❌ | ❌ | ✅ | D2: =IFERROR(IF(F2="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F2,J:J,0)),"^",VLOOKUP(F2,J:J,1,FALSE)))),""); D3: =IFERROR(IF(F3="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F3,J:J,0)),"^",VLOOKUP(F3,J:J,1,FALSE)))),"") |
| CS_ETHNIC_GROUP | ✅ | ✅ | ✅ | ✅ | D2: =IFERROR(IF(F2="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F2,J:J,0)),"^",VLOOKUP(F2,J:J,1,FALSE)))),""); D3: =IFERROR(IF(F3="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F3,J:J,0)),"^",VLOOKUP(F3,J:J,1,FALSE)))),"") |
| CS_FINANCIAL_CLASS | ❌ | ❌ | ❌ | ✅ | D2: =IFERROR(IF(F2="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F2,J:J,0)),"^",VLOOKUP(F2,J:J,1,FALSE)))),""); D3: =IFERROR(IF(F3="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F3,J:J,0)),"^",VLOOKUP(F3,J:J,1,FALSE)))),"") |
| CS_FREQUENCY | ❌ | ❌ | ❌ | ✅ | D2: =IFERROR(IF(F2="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F2,J:J,0)),"^",VLOOKUP(F2,J:J,1,FALSE)))),""); D3: =IFERROR(IF(F3="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F3,J:J,0)),"^",VLOOKUP(F3,J:J,1,FALSE)))),"") |
| CS_LANGUAGE | ✅ | ✅ | ✅ | ✅ | D2: =IFERROR(IF(F2="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F2,J:J,0)),"^",VLOOKUP(F2,J:J,1,FALSE)))),""); D3: =IFERROR(IF(F3="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F3,J:J,0)),"^",VLOOKUP(F3,J:J,1,FALSE)))),"") |
| CS_LIVING_WILL | ✅ | ✅ | ✅ | ✅ | D2: =IFERROR(IF(F2="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F2,J:J,0)),"^",VLOOKUP(F2,J:J,1,FALSE)))),""); D3: =IFERROR(IF(F3="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F3,J:J,0)),"^",VLOOKUP(F3,J:J,1,FALSE)))),"") |
| CS_MARITAL_STATUS | ✅ | ✅ | ✅ | ✅ | D2: =IFERROR(IF(F2="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F2,J:J,0)),"^",VLOOKUP(F2,J:J,1,FALSE)))),""); D3: =IFERROR(IF(F3="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F3,J:J,0)),"^",VLOOKUP(F3,J:J,1,FALSE)))),"") |
| CS_NATIONALITY | ❌ | ❌ | ❌ | ✅ | D2: =IFERROR(IF(F2="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F2,J:J,0)),"^",VLOOKUP(F2,J:J,1,FALSE)))),""); D3: =IFERROR(IF(F3="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F3,J:J,0)),"^",VLOOKUP(F3,J:J,1,FALSE)))),"") |
| CS_ORDERING_PRIORITY | ✅ | ✅ | ✅ | ✅ | D2: =IFERROR(IF(F2="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F2,J:J,0)),"^",VLOOKUP(F2,J:J,1,FALSE)))),""); D3: =IFERROR(IF(F3="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F3,J:J,0)),"^",VLOOKUP(F3,J:J,1,FALSE)))),"") |
| CS_ORDER_STATUS | ✅ | ✅ | ✅ | ✅ | D2: =IFERROR(IF(F2="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F2,J:J,0)),"^",VLOOKUP(F2,J:J,1,FALSE)))),""); D3: =IFERROR(IF(F3="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F3,J:J,0)),"^",VLOOKUP(F3,J:J,1,FALSE)))),"") |
| CS_PROCEDURE_CODING_SYSTEM | ❌ | ❌ | ❌ | ✅ | D2: =IFERROR(IF(F2="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F2,J:J,0)),"^",VLOOKUP(F2,J:K,1,FALSE)))),""); D3: =IFERROR(IF(F3="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F3,J:J,0)),"^",VLOOKUP(F3,J:K,1,FALSE)))),"") |
| CS_PROCEDURE_FUNCTIONAL_TYPE | ✅ | ✅ | ✅ | ✅ | D2: =IFERROR(IF(F2="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F2,J:J,0)),"^",VLOOKUP(F2,J:J,1,FALSE)))),""); D3: =IFERROR(IF(F3="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F3,J:J,0)),"^",VLOOKUP(F3,J:J,1,FALSE)))),"") |
| CS_PROTECTION_IND | ✅ | ✅ | ✅ | ✅ | D2: =IFERROR(IF(F2="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F2,J:J,0)),"^",VLOOKUP(F2,J:J,1,FALSE)))),""); D3: =IFERROR(IF(F3="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F3,J:J,0)),"^",VLOOKUP(F3,J:J,1,FALSE)))),"") |
| CS_RACE | ✅ | ❌ | ❌ | ✅ | D2: =IFERROR(IF(F2="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F2,J:J,0)),"^",VLOOKUP(F2,J:J,1,FALSE)))),""); D3: =IFERROR(IF(F3="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F3,J:J,0)),"^",VLOOKUP(F3,J:J,1,FALSE)))),"") |
| CS_REL_TO_PERSON | ✅ | ✅ | ✅ | ✅ | D2: =IFERROR(IF(F2="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F2,J:J,0)),"^",VLOOKUP(F2,J:J,1,FALSE)))),""); D3: =IFERROR(IF(F3="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F3,J:J,0)),"^",VLOOKUP(F3,J:J,1,FALSE)))),"") |
| CS_RELIGION | ✅ | ✅ | ✅ | ✅ | D2: =IFERROR(IF(F2="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F2,J:J,0)),"^",VLOOKUP(F2,J:J,1,FALSE)))),""); D3: =IFERROR(IF(F3="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F3,J:J,0)),"^",VLOOKUP(F3,J:J,1,FALSE)))),"") |
| CS_RESULT_STATUS | ✅ | ✅ | ❌ | ✅ | D2: =IFERROR(IF(F2="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F2,J:J,0)),"^",VLOOKUP(F2,J:J,1,FALSE)))),""); D3: =IFERROR(IF(F3="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F3,J:J,0)),"^",VLOOKUP(F3,J:J,1,FALSE)))),"") |
| CS_RX_COMPONENT_TYPE | ✅ | ✅ | ❌ | ✅ | D2: =IFERROR(IF(F2="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F2,J:J,0)),"^",VLOOKUP(F2,J:J,1,FALSE)))),""); D3: =IFERROR(IF(F3="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F3,J:J,0)),"^",VLOOKUP(F3,J:J,1,FALSE)))),"") |
| CS_RX_ROUTE | ❌ | ❌ | ❌ | ✅ | D2: =IFERROR(IF(F2="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F2,J:J,0)),"^",VLOOKUP(F2,J:J,1,FALSE)))),""); D3: =IFERROR(IF(F3="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F3,J:J,0)),"^",VLOOKUP(F3,J:J,1,FALSE)))),"") |
| CS_SERVICING_FACILITY | ❌ | ❌ | ❌ | ✅ | D2: =IFERROR(IF(F2="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F2,J:J,0)),"^",VLOOKUP(F2,J:J,1,FALSE)))),""); D3: =IFERROR(IF(F3="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F3,J:J,0)),"^",VLOOKUP(F3,J:J,1,FALSE)))),"") |
| CS_SPECIMEN_BODY_SITE_CODE | ❌ | ❌ | ❌ | ✅ | D2: =IFERROR(IF(F2="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F2,J:J,0)),"^",VLOOKUP(F2,J:J,1,FALSE)))),""); D3: =IFERROR(IF(F3="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F3,J:J,0)),"^",VLOOKUP(F3,J:J,1,FALSE)))),"") |
| CS_SPECIMEN_TYPE_CODE | ❌ | ❌ | ❌ | ✅ | D2: =IFERROR(IF(F2="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F2,J:J,0)),"^",VLOOKUP(F2,J:J,1,FALSE)))),""); D3: =IFERROR(IF(F3="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F3,J:J,0)),"^",VLOOKUP(F3,J:J,1,FALSE)))),"") |
| CS_SPECIMEN_COLLECTION_METHOD | ❌ | ❌ | ❌ | ✅ | D2: =IFERROR(IF(F2="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F2,J:J,0)),"^",VLOOKUP(F2,J:J,1,FALSE)))),""); D3: =IFERROR(IF(F3="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F3,J:J,0)),"^",VLOOKUP(F3,J:J,1,FALSE)))),"") |
| CS_STUDENT | ✅ | ✅ | ✅ | ✅ | D2: =IFERROR(IF(F2="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F2,J:J,0)),"^",VLOOKUP(F2,J:J,1,FALSE)))),""); D3: =IFERROR(IF(F3="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F3,J:J,0)),"^",VLOOKUP(F3,J:J,1,FALSE)))),"") |
| CS_VIP_IND | ✅ | ✅ | ✅ | ✅ | D2: =IFERROR(IF(F2="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F2,J:J,0)),"^",VLOOKUP(F2,J:J,1,FALSE)))),""); D3: =IFERROR(IF(F3="Unknown","UNK^UNKNOWN",(CONCATENATE(INDEX(I:I,MATCH(F3,J:J,0)),"^",VLOOKUP(F3,J:J,1,FALSE)))),"") |

---

## 🧩 Codex Development Guidelines

### 1. Conditional UI Enforcement
Only enforce `MAPPED_STD_DESCRIPTION` selection **if mapping is required** for that tab.
Rows that lack values in both `CODE` and `DISPLAY VALUE` remain visible so users can review all available `STANDARD_CODE` and `STANDARD_DESCRIPTION` values. Their `MAPPED_STD_DESCRIPTION` and `SUB_DEFINITION` fields start blank and only populate after a mapping is chosen.

### 1.1 Validation Rules

- `CODE` and `DISPLAY VALUE` operate as a pair. If one is populated the other is required.
- When either `STANDARD_CODE` or `STANDARD_DESCRIPTION` has a value, `MAPPED_STD_DESCRIPTION` must be selected.
- Codes within a single tab must be unique.
- Validation errors are surfaced in the right‑hand sidebar with sheet and row references.

### 2. Formula Replication
Recreate the Excel logic within your backend/frontend to compute a `CODE^DESC` combo string when a mapped value is selected.
When the user picks a value in `MAPPED_STD_DESCRIPTION`, the corresponding `SUB_DEFINITION` field should be set to `STANDARD_CODE^STANDARD_DESCRIPTION` for that row.

The "sub definition" column may appear as either `SUB_DEFINITION` or `SUBDEFINITION` in the workbook headers.
`SUB_DEFINITION` itself is not a dropdown. Options for `MAPPED_STD_DESCRIPTION` come from the `STANDARD_DESCRIPTION` column, and the selected value dynamically fills the `SUB_DEFINITION` cell with `STANDARD_CODE^STANDARD_DESCRIPTION`.

### 3. Skip Tabs with No Mapping Data
If `STANDARD_CODE` or `STANDARD_DESCRIPTION` is blank across all rows, the mapping field is **not required**. Codex should skip enforcement and formula computation for that tab.

### 4. Maintain Column Order and Naming
Avoid renaming or reordering columns to preserve downstream interoperability. Columns
are retained even when completely blank so that all expected fields remain
available for data entry.

### 5. UI Loading Efficiency
The workbook is parsed once on upload and the web interface renders one sheet at a time, fetching data for other sheets only when selected. This prevents the page from hanging on large workbooks.

### 6. Workbook Export
After mappings are applied, the application can write the updated values back to the uploaded workbook while preserving the original file name and Excel formatting.
