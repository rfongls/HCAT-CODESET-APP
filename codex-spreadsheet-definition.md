# 📘 Codex Reference: Nexus Engine Codeset Template Workbook

Workbook: **(Health System) Codeset Template (Nexus Engine v4)**

Purpose: Define, normalize, and optionally map facility codes to national standards using a structured UI.

---

## Field Summary

| Column Name                | Description |
|---------------------------|-------------|
| `CODE`                    | Local/internal code value |
| `DISPLAY VALUE`           | Human-friendly label |
| `STANDARD_CODE`           | Optional: industry-aligned code (e.g., SNOMED, HL7) |
| `STANDARD_DESCRIPTION`    | Optional: official label for standard code |
| `MAPPED_STD_DESCRIPTION`  | Dropdown-enabled field where user selects a mapped description |
| (Formula Column)          | Generates a concatenated string (e.g., `UNK^UNKNOWN`) based on mapped description |

---

## Mapping Behavior Logic

### Mapping **is required** if:
- `STANDARD_CODE` column exists **and contains data**
- `STANDARD_DESCRIPTION` column exists **and contains data**
- `MAPPED_STD_DESCRIPTION` standard_code and standard_description is populated with anything except for NA.

### Mapping **is NOT required** if:
- `STANDARD_CODE` or `STANDARD_DESCRIPTION` columns are entirely blank (even if headers exist)

---

## Formula Logic (If Present)
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

## Sheet-Level Mapping & Formula Summary

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

## Codex Development Guidelines

### 1. Conditional UI Enforcement
Only enforce `MAPPED_STD_DESCRIPTION` selection **if mapping is required** for that tab.
Rows that lack values in both `CODE` and `DISPLAY VALUE` remain visible so users can review all available `STANDARD_CODE` and `STANDARD_DESCRIPTION` values. Their `MAPPED_STD_DESCRIPTION` and `SUB_DEFINITION` fields start blank and only populate after a mapping is chosen.

### 1.1 Validation Rules

- `CODE` and `DISPLAY VALUE` operate as a pair. If one is populated the other is required.
- If `CODE` or `DISPLAY VALUE` is populated and the row has a `STANDARD_CODE` or `STANDARD_DESCRIPTION`, `MAPPED_STD_DESCRIPTION` must also be selected.
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

### 7. Codeset Field References

| Field | Description | Code Set Name | HL7 2.3+ Data Type | Code Set NBR |
|-------|-------------|---------------|-------------------|--------------|
| PID:8 | Gender | CS_GENDER | IS | 10 |
| PID:10 | Race | CS_RACE | CE | 40 |
| PID:15 | Language | CS_LANGUAGE | CE | 380 |
| PID:16 | Marital Status | CS_MARITAL_STATUS | CE | 60 |
| PID:17 | Religion | CS_RELIGION | CE | 70 |
| PID:11.3 | Patient Address City | No Translation | ST | 50 |
| PID:22 | Ethnic Group | CS_ETHNIC_GROUP | ST | 710 |
| PID:23.3 | Birth Place | No Translation | ST | 50 |
| PID:26 | Citizenship | CS_CITIZENSHIP | ST | ??? |
| PID:28 | Nationality | CS_NATIONALITY | CE | 1080 |

> **Note:** PID:26 is not supported for Translation. It works for other fields for that tab, just not that one specific field.

## PD1 Segment - Additional Patient Demographic

| Field | Description | Code Set Name | HL7 2.3+ Data Type | Code Set NBR |
|-------|-------------|---------------|-------------------|--------------|
| PD1:5 | Student Indicator | CS_STUDENT | IS | 180 |
| PD1:7 | Living Will | CS_LIVING_WILL | IS | 170 |
| PD1:11 | Publicity Code | CS_PUBLICITY | CE | 510 |
| PD1:12 | Protection Indicator | CS_PROTECTION_IND | ID | 190 |

## NK1 Segment - Next of Kin

| Field | Description | Code Set Name | HL7 2.3+ Data Type | Code Set NBR |
|-------|-------------|---------------|-------------------|--------------|
| NK1:3 | Next of Kin Relationship to Patient | CS_REL_TO_PERSON | CE | 280 |
| NK1:14 | Marital Status | CS_MARITAL_STATUS | ST | 60 |
| NK1:15 | Gender | CS_GENDER | IS | 10 |
| NK1:20 | Primary Language | CS_LANGUAGE | CE | 380 |
| NK1:22 | Publicity Code | CS_PUBLICITY | CE | 510 |
| NK1:23 | Protection Indicator | CS_PROTECTION_IND | ID | 190 |
| NK1:24 | Student Indicator | CD_STUDENT | ID | 180 |
| NK1:27 | Nationality | CS_NATIONALITY | CE | 1080 |
| NK1:28 | Ethnic Group | CS_ETHNIC_GROUP | CE | 710 |
| NK1:32.3 | Contact Person's Address City | No Translation | ST | 50 |
| NK1:39 | VIP Indicator | CS_VIP_IND | IS | 250 |

> **Note:** This list intentionally excludes NK1:19 and NK1:35, which are not translated by the Translator module.

## PV1 Segment - Patient Visit

| Field | Description | Code Set Name | HL7 2.3+ Data Type | Code Set NBR |
|-------|-------------|---------------|-------------------|--------------|
| PV1:2 | Patient Class | CS_ENCOUNTER_CLASS | IS | 80 |
| PV1:4 | Admission Type | CS_ADMIT_TYPE | IS | 100 |
| PV1:10 | Hospital Service | CS_ADMIT_SERVICE | IS | 110 |
| PV1:14 | Admission Source | CS_ADMIT_SOURCE | IS | 120 |
| PV1:16 | VIP Indicator | CS_VIP_IND | IS | 250 |
| PV1:18 | Patient Type | CS_ENCOUNTER_TYPE | IS | 130 |
| PV1:20 | Financial Class | CS_FINANCIAL_CLASS | FC | 140 |
| PV1:36 | Discharge Disposition | CS_DISCHARGE_DISPOSITION | IS | 740 |
| PV1:39 | Servicing Facility | CS_SERVICING_FACILITY | IS | 150 |

## PV2 Segment - Additional Patient Visit Information

| Field | Description | Code Set Name | HL7 2.3+ Data Type | Code Set NBR |
|-------|-------------|---------------|-------------------|--------------|
| PV2:2 | Accommodation Code | CS_ACCOMODATION | CE | 700 |
| PV2:21 | Visit Publicity Code | No Translation | IS | 510 |
| PV2:22 | Visit Protection Indicator | CS_PROTECTION_IND | ID | 190 |

## AL1 Segment - Allergies

| Field | Description | Code Set Name | HL7 2.3+ Data Type | Code Set NBR |
|-------|-------------|---------------|-------------------|--------------|
| AL1:4 | Allergy Severity | CS_ALLERGY_SEVERITY_CODE | CE | 1060 |
| AL1:5 | Allergy Reaction | CS_ALLERGY_REACTION_CODE | ST | 1070 |

## DG1 Segment - Diagnosis

| Field | Description | Code Set Name | HL7 2.3+ Data Type | Code Set NBR |
|-------|-------------|---------------|-------------------|--------------|
| DG1:2 | Diagnosis Coding Method | CS_DIAGNOSIS_CODE_METHOD | ID | 210 |
| DG1:6 | Diagnosis Type | CS_DIAGNOSIS_TYPE | IS | 200 |
| DG1:18 | Confidential Indicator | CS_PROTECTION_IND | ID | 190 |

## GT1 Segment - Guarantor

| Field | Description | Code Set Name | HL7 2.3+ Data Type | Code Set NBR |
|-------|-------------|---------------|-------------------|--------------|
| G1:5.3 | Guarantor Address City | No Translation | ST | 50 |
| GT1:9 | Gender | CS_GENDER | IS | 10 |
| GT1:11 | Guarantor Relationship | CS_REL_TO_PERSON | CE | 280 |
| GT1:17.3 | Guarantor Employer Address City | No Translation | ST | 50 |
| GT1:30 | Marital Status Code | CS_MARITAL_STATUS | CE | 60 |
| GT1:36 | Language | CS_LANGUAGE | CE | 380 |
| GT1:38 | Publicity Code | CS_PUBLICITY | CE | 510 |
| GT1:39 | Protection Indicator | CS_PROTECTION_IND | ID | 190 |
| GT1:41 | Religion | CS_RELIGION | CE | 70 |
| GT1:43 | Nationality | CS_NATIONALITY | CE | 1080 |
| GT1:44 | Ethnic Group | CS_ETHNIC_GROUP | CE | 710 |
| GT1:55 | Race | CS_RACE | CE | 40 |
| GT1:57 | VIP Indicator | CS_VIP_IND | IS | 250 |

> **Note:** This list intentionally excludes GT1:35 and GT1:40, which are not translated by the Translator module.

## IN1 Segment - Insurance

| Field | Description | Code Set Name | HL7 2.3+ Data Type | Code Set NBR |
|-------|-------------|---------------|-------------------|--------------|
| IN1:5.3 | Insurance Company City | No Translation | ST | 50 |
| IN1:15 | Plan Type | No Translation | IS | 300 |
| IN1:17 | Relationship To Patient | CS_REL_TO_PERSON | CE | 280 |
| IN1:19.3 | Insured's Address City | No Translation | ST | 50 |
| IN1:43 | Gender | CS_GENDER | IS | 10 |
| IN1:44.3 | Insured's Employer City | No Translation | ST | 50 |
| IN1:45 | Verification Status | No Translation | ST | 310 |
| IN1:53 | VIP Indicator | CS_VIP_IND | IS | 250 |

## IN2 Segment - Additional Insurance Information

| Field | Description | Code Set Name | HL7 2.3+ Data Type | Code Set NBR |
|-------|-------------|---------------|-------------------|--------------|
| IN2:33 | Citizenship | CS_CITIZENSHIP | CE | ??? |
| IN2:34 | Primary Language | CS_LANGUAGE | CE | 380 |
| IN2:36 | Publicity Code | CS_PUBLICITY | CE | 510 |
| IN2:37 | Protection Indicator | CS_PROTECTION_IND | ID | 190 |
| IN2:38 | Student Indicator | CS_STUDENT | IS | 180 |
| IN2:39 | Religion | CS_RELIGION | CE | 70 |
| IN2:41 | Nationality | CS_NATIONALITY | CE | 1080 |
| IN2:42 | Ethnic Group | CS_ETHNIC_GROUP | CE | 710 |
| IN2:43 | Marital Status | CS_MARITAL_STATUS | CE | 60 |
| IN2:71 | Race | CS_RACE | CE | 40 |

## ACC Segment - Accident Information

| Field | Description | Code Set Name | HL7 2.3+ Data Type | Code Set NBR |
|-------|-------------|---------------|-------------------|--------------|
| ACC:2 | Accident Code | CS_ACCIDENT_CODE | CE | 720 |
| ACC:4 | Auto Accident State | No Translation | CE | 200 |

## ORC Segment - Common Order

| Field | Description | Code Set Name | HL7 2.3+ Data Type | Code Set NBR |
|-------|-------------|---------------|-------------------|--------------|
| ORC:1 | Order Control | No Translation | ID | 490 |
| ORC:2.2 | Placer Order Number | No Translation | EI | 830 |
| ORC:5 | Order Status | No Translation | ID | 490 |
| ORC:7.6 | Quantity/Timing | No Translation | TQ | 730 |
| ORC:17 | Entering Organization | No Translation | CE | 560 |
| ORC:28 | Confidential Code | CS_CONFIDENTIALITY_CODE | CE | 970 |

## OBR Segment - Observation Request

| Field | Description | Code Set Name | HL7 2.3+ Data Type | Code Set NBR |
|-------|-------------|---------------|-------------------|--------------|
| OBR:15.1 | Specimen Type Code | CS_SPECIMENT_TYPE_CODE | CE | 840 |
| OBR:15.4 | Body Site | No Translation | CE | 850 |
| OBR:24 | Diagnostic Service Sec. ID | CS_DIAGNOSTIC_SERVICE_SECTION | ID | 560 |
| OBR:25 | Result Status | CS_RESULT_STATUS | ID | 470 |
| OBR:27.6 | Priority | CS_ORDERING_PRIORITY | ID | 730 |

## TXA Segment - Document Notification

| Field | Description | Code Set Name | HL7 2.3+ Data Type | Code Set NBR |
|-------|-------------|---------------|-------------------|--------------|
| TXA:2.3.2 | Diagnostic Service Sec. ID | CS_DIAGNOSTIC_SERVICE_SECTION | ID | 560 |
| TXA:17 | Completion Status | CS_COMPLETION_STATUS | ID | 1090 |
| TXA:18 | Confidentiality Status | CS_CONFIDENTIALITY_CODE | ID | 970 |
| TXA:19 | Availability Status | CS_AVAILABILITY_STATUS | ID | 1000 |

## OBX Segment - Observation

| Field | Description | Code Set Name | HL7 2.3+ Data Type | Code Set NBR |
|-------|-------------|---------------|-------------------|--------------|
| OBX:2 | Value Type | No Translation | ID | 400 |
| OBX:8 | Abnormal Flag | CS_ABNORMAL_FLAG | IS | 480 |
| OBX:11 | Result Status | CS_RESULT_STATUS | ID | 470 |

## NTE Segment - Comments

| Field | Description | Code Set Name | HL7 2.3+ Data Type | Code Set NBR |
|-------|-------------|---------------|-------------------|--------------|
| NTE:2 | Source Of Comment | No Translation | ID | 460 |
