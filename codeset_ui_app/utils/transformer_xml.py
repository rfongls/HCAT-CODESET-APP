from __future__ import annotations
from typing import Dict, List
import pandas as pd
from xml.sax.saxutils import quoteattr


def _str_series(df: pd.DataFrame, col: str) -> pd.Series:
    """Return a stripped string Series for ``col`` using the first column if duplicated."""
    series = df[col]
    if isinstance(series, pd.DataFrame):
        series = series.iloc[:, 0]
    return series.astype(str).str.strip()


# Static field configuration copied from the generic transformer template.  The
# application does not derive these from the workbook; every exported
# transformer should include this same set of ``Field`` definitions.
DEFAULT_FIELDS: List[dict] = [
    {"Name": "PID:8", "Codeset": "CS_ADMIN_GENDER", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Gender"},
    {"Name": "PID:10", "Codeset": "CS_RACE", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Race"},
    {"Name": "PID:15", "Codeset": "CS_LANGUAGE", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Language"},
    {"Name": "PID:16", "Codeset": "CS_MARITAL_STATUS", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Marital Status"},
    {"Name": "PID:17", "Codeset": "CS_RELIGION", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Religion"},
    {"Name": "PID:22", "Codeset": "CS_ETHNIC_GROUP", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Ethnic Group"},
    {"Name": "PID:26", "Codeset": "CS_CITIZENSHIP", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Citizenship"},
    {"Name": "PID:28", "Codeset": "CS_NATIONALITY", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Nationality"},
    {"Name": "PD1:5", "Codeset": "CS_STUDENT", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Student Indicator"},
    {"Name": "PD1:7", "Codeset": "CS_LIVING_WILL", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Living Will"},
    {"Name": "PD1:12", "Codeset": "CS_PROTECTION_IND", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Protection Indicator"},
    {"Name": "NK1:3", "Codeset": "CS_REL_TO_PERSON", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Next of Kin Relationship to Patient"},
    {"Name": "NK1:14", "Codeset": "CS_MARITAL_STATUS", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Marital Status"},
    {"Name": "NK1:15", "Codeset": "CS_ADMIN_GENDER", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Gender"},
    {"Name": "NK1:19", "Codeset": "CS_CITIZENSHIP", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Citizenship"},
    {"Name": "NK1:20", "Codeset": "CS_LANGUAGE", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Primary Language"},
    {"Name": "NK1:23", "Codeset": "CS_PROTECTION_IND", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Protection Indicator"},
    {"Name": "NK1:24", "Codeset": "CS_STUDENT", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Student Indicator"},
    {"Name": "NK1:27", "Codeset": "CS_NATIONALITY", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Nationality"},
    {"Name": "NK1:35", "Codeset": "CS_RACE", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Race"},
    {"Name": "PV1:2", "Codeset": "CS_ENCOUNTER_CLASS", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Patient Class"},
    {"Name": "PV1:4", "Codeset": "CS_ADMIT_TYPE", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Admission Type"},
    {"Name": "PV1:10", "Codeset": "CS_ADMIT_SERVICE", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Hospital Service"},
    {"Name": "PV1:14", "Codeset": "CS_ADMIT_SOURCE", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Admission Source"},
    {"Name": "PV1:16", "Codeset": "CS_VIP_IND", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "VIP Indicator"},
    {"Name": "PV1:18", "Codeset": "CS_ENCOUNTER_TYPE", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Patient Type"},
    {"Name": "PV1:20", "Codeset": "CS_FINANCIAL_CLASS", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Financial Class"},
    {"Name": "PV1:36", "Codeset": "CS_DISCHARGE_DISPOSITION", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Discharge Disposition"},
    {"Name": "PV1:39", "Codeset": "CS_SERVICING_FACILITY", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Servicing Facility"},
    {"Name": "PV2:2", "Codeset": "CS_ACCOMODATION", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Accommodation Code"},
    {"Name": "PV2:22", "Codeset": "CS_PROTECTION_IND", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Visit Protection Indicator"},
    {"Name": "AL1:2", "Codeset": "CS_ALLERGEN_TYPE_CODE", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Allergen Type Code"},
    {"Name": "AL1:4", "Codeset": "CS_ALLERGY_SEVERITY_CODE", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Allergy Severity"},
    {"Name": "AL1:5", "Codeset": "CS_ALLERGY_REACTION_CODE", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Allergy Reaction"},
    {"Name": "IAM:2", "Codeset": "CS_ALLERGEN_TYPE_CODE", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Allergen Type Code"},
    {"Name": "IAM:4", "Codeset": "CS_ALLERGY_SEVERITY_CODE", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Allergy Severity"},
    {"Name": "IAM:5", "Codeset": "CS_ALLERGY_REACTION_CODE", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Allergy Reaction"},
    {"Name": "DG1:2", "Codeset": "CS_DIAGNOSIS_CODE_METHOD", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Diagnosis Coding Method"},
    {"Name": "DG1:6", "Codeset": "CS_DIAGNOSIS_TYPE", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Diagnosis Type"},
    {"Name": "DG1:18", "Codeset": "CS_PROTECCTION_IND", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Confidential Indicator"},
    {"Name": "GT1:9", "Codeset": "CS_ADMIN_GENDER", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Gender"},
    {"Name": "GT1:11", "Codeset": "CS_REL_TO_PERSON", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Guarantor Relationship"},
    {"Name": "GT1:30", "Codeset": "CS_MARITAL_STATUS", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Marital Status Code"},
    {"Name": "GT1:35", "Codeset": "CS_CITIZENSHIP", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Citizenship"},
    {"Name": "GT1:36", "Codeset": "CS_LANGUAGE", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Language"},
    {"Name": "GT1:39", "Codeset": "CS_PROTECTION_IND", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Protection Indicator"},
    {"Name": "GT1:40", "Codeset": "CS_STUDENT", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Student Indicator"},
    {"Name": "GT1:41", "Codeset": "CS_RELIGION", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Religion"},
    {"Name": "GT1:43", "Codeset": "CS_NATIONALITY", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Nationality"},
    {"Name": "GT1:55", "Codeset": "CS_RACE", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Race"},
    {"Name": "IN1:17", "Codeset": "CS_REL_TO_PERSON", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Relationship To Patient"},
    {"Name": "IN1:43", "Codeset": "CS_ADMIN_GENDER", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Gender"},
    {"Name": "IN2:33", "Codeset": "CS_CITIZENSHIP", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Citizenship"},
    {"Name": "IN2:34", "Codeset": "CS_LANGUAGE", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Language"},
    {"Name": "IN2:37", "Codeset": "CS_PROTECTION_IND", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Protection Indicator"},
    {"Name": "IN2:38", "Codeset": "CS_STUDENT", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Student Indicator"},
    {"Name": "IN2:39", "Codeset": "CS_RELIGION", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Religion"},
    {"Name": "IN2:41", "Codeset": "CS_NATIONALITY", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Nationality"},
    {"Name": "IN2:42", "Codeset": "CS_ETHNIC_GROUP", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Ethnic Group"},
    {"Name": "IN2:43", "Codeset": "CS_MARITAL_STATUS", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Marital Status"},
    {"Name": "ACC:2", "Codeset": "CS_ACCIDENT_CODE", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Accident Code"},
    {"Name": "ORC:28", "Codeset": "CS_CONFIDENTIALITY_CODE", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Confidential Code"},
    {"Name": "OBR:5", "Codeset": "CS_ORDERING_PRIORITY", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Priority"},
    {"Name": "PR1:6", "Codeset": "CS_PROCEDURE_FUNCTIONAL_TYPE", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Procedure Type"},
    {"Name": "PR1:3.3", "Codeset": "CS_PROCEDURE_CODING_SYSTEM", "OutputType": "DisplayOnly", "Enabled": "True", "Description": "Procedure Coding System"},
    {"Name": "OBR:15.1", "Codeset": "CS_SPECIMEN_TYPE_CODE", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Specimen Type Code"},
    {"Name": "OBR:15.3", "Codeset": "CS_SPECIMEN_COLLECTION_METHOD", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Specimen Collection Method"},
    {"Name": "OBR:15.4", "Codeset": "CS_SPECIMEN_BODY_SITE_CODE", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Specimen Body Site"},
    {"Name": "OBR:24", "Codeset": "CS_DIAGNOSTIC_SERVICE_SECTION", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Diagnostic Service Section"},
    {"Name": "OBR:25", "Codeset": "CS_RESULT_STATUS", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Result Status"},
    {"Name": "OBR:27.6", "Codeset": "CS_ORDERING_PRIORITY", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Priority"},
    {"Name": "OBX:8", "Codeset": "CS_ABNORMAL_FLAG", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Abnormal Flag"},
    {"Name": "OBX:11", "Codeset": "CS_RESULT_STATUS", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Result Status"},
    {"Name": "TXA:2.3.2", "Codeset": "CS_DIAGNOSTIC_SERVICE_SECTION", "OutputType": "DisplayOnly", "Enabled": "True", "Description": "Diagnostic Service Section"},
    {"Name": "TXA:17", "Codeset": "CS_COMPLETION_STATUS", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Completion Status"},
    {"Name": "TXA:18", "Codeset": "CS_CONFIDENTIALITY_CODE", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Confidentiality Status"},
    {"Name": "TXA:19", "Codeset": "CS_AVAILABILITY_STATUS", "OutputType": "LocalCodeFirst", "Enabled": "True", "Description": "Availability Status"},
]


def build_transformer_xml(
    data: Dict[str, pd.DataFrame],
    freetext: Dict[str, bool] | None = None,
) -> str:
    """Return an indented XML string representing ``data`` as a codeset transformer.

    Parameters
    ----------
    data:
        Mapping of sheet name to DataFrame representing the codeset workbook.
    freetext:
        Optional mapping of codeset name to a boolean indicating whether the
        field should allow free text (``True`` disables the field in the
        transformer ``Fields`` section).
    """

    free_map = {k: v for k, v in (freetext or {}).items() if v}

    # Build fields data with optional free text overrides
    field_dicts: List[dict] = []
    for f in DEFAULT_FIELDS:
        attrs = f.copy()
        if free_map.get(attrs["Codeset"]):
            attrs["Enabled"] = "False"
        field_dicts.append(attrs)

    # Determine column widths for field attributes to align output
    field_order = ["Name", "Codeset", "OutputType", "Enabled", "Description"]
    field_attr_strings = [
        [f"{k}={quoteattr(d[k])}" for k in field_order]
        for d in field_dicts
    ]
    field_widths = [
        max(len(attrs[i]) for attrs in field_attr_strings) + 2
        for i in range(len(field_order) - 1)
    ]

    field_lines: List[str] = []
    for attrs in field_attr_strings:
        parts = [attrs[0].ljust(field_widths[0])]
        for i in range(1, len(field_order) - 1):
            parts.append(attrs[i].ljust(field_widths[i]))
        parts.append(attrs[-1])
        field_lines.append("    <Field " + "".join(parts).rstrip() + " />")

    # Collect codeset information from workbook data
    codesets: List[dict] = []
    for sheet, df in data.items():
        if not isinstance(df, pd.DataFrame):
            continue
        col_map = {c.strip().upper().replace(" ", "_"): c for c in df.columns}
        code_col = col_map.get("CODE")
        display_col = col_map.get("DISPLAY_VALUE") or col_map.get("DISPLAY")
        std_code_col = (
            col_map.get("MAPPED_STANDARD_CODE")
            or col_map.get("MAPPED_STD_CODE")
            or col_map.get("STANDARD_CODE")
            or col_map.get("STD_CODE")
        )
        std_display_col = (
            col_map.get("MAPPED_STD_DESCRIPTION")
            or col_map.get("MAPPED_STANDARD_DESCRIPTION")
            or col_map.get("STANDARD_DESCRIPTION")
            or col_map.get("STD_DESCRIPTION")
            or col_map.get("MAPPED_STD_DESC")
        )
        oid_col = col_map.get("OID")
        url_col = col_map.get("URL")
        if code_col is None and display_col is None and std_code_col is None and std_display_col is None:
            continue

        codeset_info: dict = {"Name": sheet, "Codes": []}

        if oid_col:
            oid_val = next((v for v in _str_series(df, oid_col) if v), "")
            if oid_val:
                codeset_info["Oid"] = oid_val
        if url_col:
            url_val = next((v for v in _str_series(df, url_col) if v), "")
            if url_val:
                codeset_info["Url"] = url_val

        code_series = _str_series(df, code_col) if code_col else pd.Series([""] * len(df))
        display_series = _str_series(df, display_col) if display_col else pd.Series([""] * len(df))
        std_code_series = _str_series(df, std_code_col) if std_code_col else pd.Series([""] * len(df))
        std_display_series = _str_series(df, std_display_col) if std_display_col else pd.Series([""] * len(df))

        seen = set()
        for lc, ld, sc, sd in zip(code_series, display_series, std_code_series, std_display_series):
            lc = (lc or "").strip()
            ld = (ld or "").strip()
            if not lc or not ld:
                continue
            sc = (sc or "").strip()
            sd = (sd or "").strip()
            key = (lc, ld, sc, sd)
            if key in seen:
                continue
            seen.add(key)
            code_attrs = {"LocalCode": lc, "LocalDisplay": ld, "StandardCode": sc, "StandardDisplay": sd}
            codeset_info["Codes"].append(code_attrs)

        codesets.append(codeset_info)

    # Build codeset XML lines with column widths calculated per codeset to
    # avoid excessive gaps between attributes when one codeset contains very
    # long values.
    code_order = ["LocalCode", "LocalDisplay", "StandardCode", "StandardDisplay"]
    codeset_lines: List[str] = []
    for cs in codesets:
        header = f"    <Codeset Name={quoteattr(cs['Name'])}"
        if cs.get("Oid"):
            header += f" Oid={quoteattr(cs['Oid'])}"
        if cs.get("Url"):
            header += f" Url={quoteattr(cs['Url'])}"
        header += ">"
        codeset_lines.append(header)
        code_attr_strings = [
            [f"{k}={quoteattr(c[k])}" if c.get(k) else "" for k in code_order]
            for c in cs["Codes"]
        ]
        code_widths = [
            max((len(attrs[i]) for attrs in code_attr_strings if attrs[i]), default=0) + 2
            for i in range(len(code_order) - 1)
        ]

        for attrs in code_attr_strings:
            parts = [attrs[0].ljust(code_widths[0])]
            for i in range(1, len(code_order) - 1):
                parts.append(attrs[i].ljust(code_widths[i]))
            parts.append(attrs[-1])
            codeset_lines.append("      <Code " + "".join(parts).rstrip() + " />")

        codeset_lines.append("    </Codeset>")

    lines = [
        "<?xml version=\"1.0\" ?>",
        "<Configuration>",
        "  <Fields>",
        *field_lines,
        "  </Fields>",
        "  <Codesets>",
        *codeset_lines,
        "  </Codesets>",
        "</Configuration>",
    ]

    return "\r\n".join(lines) + "\r\n"

