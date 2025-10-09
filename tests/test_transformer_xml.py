from pathlib import Path
import xml.etree.ElementTree as ET
import importlib
import json
import re
from typing import List
import pytest
import pandas as pd
from codeset_ui_app.components.file_parser import load_workbook
from codeset_ui_app.utils.transformer_xml import build_transformer_xml
from codeset_ui_app.app import app, _load_workbook_path


def test_build_transformer_xml_generates_codeset():
    path = Path('Samples/Generic Codeset V4/(Health System) Codeset Template (Nexus Engine v4) (1).xlsx')
    with path.open('rb') as fh:
        data, _ = load_workbook(fh)
    xml_str = build_transformer_xml(data)
    root = ET.fromstring(xml_str)
    cs = root.find("./Codesets/Codeset[@Name='CS_DIAGNOSTIC_SERVICE_SECTION']")
    assert cs is not None
    assert cs.get('Oid') == '2.16.840.1.114222.4.11.922'
    assert cs.get('Url') == 'PHIN VADS (CDC)'
    codes = cs.findall('Code')
    assert any(
        c.get('LocalCode') == 'CARD'
        and c.get('LocalDisplay') == 'CARDIOLOGY'
        and c.get('StandardCode') == 'CARD'
        and c.get('StandardDisplay') == 'CARDIOLOGY'
        for c in codes
    )
    # Ensure output is indented with each code on its own line
    normalized = xml_str.replace('\r\n', '\n')
    assert '\n  <Codesets>' in normalized
    assert '\n    <Codeset' in normalized
    assert '\n      <Code ' in normalized


def test_build_transformer_xml_ignores_freetext():
    path = Path('Samples/Generic Codeset V4/(Health System) Codeset Template (Nexus Engine v4) (1).xlsx')
    with path.open('rb') as fh:
        data, _ = load_workbook(fh)
    xml_str = build_transformer_xml(data, {'CS_RACE': True})
    root = ET.fromstring(xml_str)
    assert root.find('./Fields') is None
    cs = root.find("./Codesets/Codeset[@Name='CS_RACE']")
    assert cs is not None


def test_export_transformer_endpoint(tmp_path):
    path = Path('Samples/Generic Codeset V4/(Health System) Codeset Template (Nexus Engine v4) (1).xlsx')
    _load_workbook_path(path, path.name)
    with app.test_client() as c:
        resp = c.get('/transformer')
        assert resp.status_code == 200
        root = ET.fromstring(resp.data)
        assert root.find("./Codesets/Codeset[@Name='CS_DIAGNOSTIC_SERVICE_SECTION']") is not None
    # cleanup global state
    app_module = importlib.import_module("codeset_ui_app.app")
    app_module.workbook_data.clear()
    app_module.dropdown_data.clear()
    app_module.mapping_data.clear()
    app_module.field_notes.clear()
    app_module.workbook_obj = None
    app_module.original_filename = None
    app_module.workbook_path = None
    app_module.last_error = None
    app_module.comparison_data.clear()
    app_module.comparison_path = None


def test_export_transformer_ignores_freetext(tmp_path):
    path = Path('Samples/Generic Codeset V4/(Health System) Codeset Template (Nexus Engine v4) (1).xlsx')
    _load_workbook_path(path, path.name)
    with app.test_client() as c:
        resp = c.get('/transformer', query_string={'freetext': json.dumps({'CS_RACE': True})})
        assert resp.status_code == 200
        root = ET.fromstring(resp.data)
        assert root.find('./Fields') is None
        assert root.find("./Codesets/Codeset[@Name='CS_RACE']") is not None
    app_module = importlib.import_module("codeset_ui_app.app")
    app_module.workbook_data.clear()
    app_module.dropdown_data.clear()
    app_module.mapping_data.clear()
    app_module.field_notes.clear()
    app_module.workbook_obj = None
    app_module.original_filename = None
    app_module.workbook_path = None
    app_module.last_error = None
    app_module.comparison_data.clear()
    app_module.comparison_path = None


def test_export_transformer_rejects_validation_errors():
    app_module = importlib.import_module("codeset_ui_app.app")
    app_module.workbook_data = {
        "CS_DUP": pd.DataFrame(
            {
                "CODE": ["A", "A"],
                "DISPLAY VALUE": ["Alpha", "Alpha"],
                "MAPPED_STD_DESCRIPTION": ["", ""],
                "STANDARD_CODE": ["", ""],
                "STANDARD_DESCRIPTION": ["", ""],
            }
        )
    }
    app_module.mapping_data = {
        "CS_DUP": {
            "code_col": "CODE",
            "display_col": "DISPLAY VALUE",
            "mapped_col": "MAPPED_STD_DESCRIPTION",
            "std_col": "STANDARD_DESCRIPTION",
            "std_code_col": "STANDARD_CODE",
        }
    }
    with app.test_client() as c:
        resp = c.get('/transformer')
        assert resp.status_code == 400
        data = resp.get_json()
        assert data is not None and data.get('errors')
        assert any('duplicates row' in e for e in data['errors'])
    app_module.workbook_data.clear()
    app_module.mapping_data.clear()


def test_alignment_of_codes():
    path = Path('Samples/Generic Codeset V4/(Health System) Codeset Template (Nexus Engine v4) (1).xlsx')
    with path.open('rb') as fh:
        data, _ = load_workbook(fh)
    xml_str = build_transformer_xml(data)
    lines = xml_str.split('\r\n')

    # Ensure code attribute columns are consistent within each codeset
    codeset_code_lines: List[List[str]] = []
    current: List[str] | None = None
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('<Codeset '):
            current = []
            codeset_code_lines.append(current)
        elif stripped.startswith('<Code '):
            if current is not None:
                current.append(line)
        elif stripped.startswith('</Codeset>'):
            current = None

    for cls in codeset_code_lines:
        if not cls:
            continue
        if any('LocalDisplay=' in l for l in cls):
            assert len({l.index('LocalDisplay=') for l in cls if 'LocalDisplay=' in l}) == 1
        if any('StandardCode=' in l for l in cls):
            assert len({l.index('StandardCode=') for l in cls if 'StandardCode=' in l}) == 1
        if any('StandardDisplay=' in l for l in cls):
            assert len({l.index('StandardDisplay=') for l in cls if 'StandardDisplay=' in l}) == 1


def test_duplicate_codes_raise_error():
    df = pd.DataFrame(
        {
            "Code": ["UNK", "UNK"],
            "Display": ["Unknown", "Unknown"],
            "Standard Code": ["", "UNK"],
            "Standard Description": ["", "Unknown"],
        }
    )
    with pytest.raises(ValueError) as exc:
        build_transformer_xml({"CS_ADMIN_GENDER": df})
    assert "duplicate CODE" in str(exc.value)


def test_blank_mapping_columns_do_not_generate_standard_fields():
    df = pd.DataFrame(
        {
            "Code": ["IND"],
            "Display Value": ["Industrial"],
            "Mapped_STD_DESCRIPTION": [""],
            "Subdefinition": [""],
            "Standard Code": ["ALL"],
            "Standard Description": ["Allergy Clinic"],
        }
    )
    xml_str = build_transformer_xml({"CS_ADMIT_SERVICE": df})
    root = ET.fromstring(xml_str)
    code = root.find("./Codesets/Codeset[@Name='CS_ADMIT_SERVICE']/Code")
    assert code is not None
    assert code.get("LocalCode") == "IND"
    assert code.get("LocalDisplay") == "Industrial"
    assert code.get("StandardCode") is None
    assert code.get("StandardDisplay") is None


def test_extra_tabs_without_mapping_are_ignored():
    df = pd.DataFrame(
        {
            "Code": ["M"],
            "Display": ["Male"],
            "Standard Code": ["M"],
            "Standard Description": ["Male"],
        }
    )
    extra = pd.DataFrame({"Notes": ["Keep"], "Owner": ["Team"]})
    xml_str = build_transformer_xml({"CS_ADMIN_GENDER": df, "README": extra})
    root = ET.fromstring(xml_str)
    codeset = root.find("./Codesets/Codeset[@Name='CS_ADMIN_GENDER']")
    assert codeset is not None
    assert root.find("./Codesets/Codeset[@Name='README']") is None


def test_definition_values_without_mapping_are_ignored():
    df = pd.DataFrame(
        {
            "Code": ["IND"],
            "Display Value": ["Industrial"],
            "Mapped_STD_DESCRIPTION": [""],
            "Subdefinition": [""],
            "Definition": ["ALL^Allergy Clinic"],
            "Standard Code": ["ALL"],
            "Standard Description": ["Allergy Clinic"],
        }
    )
    xml_str = build_transformer_xml({"CS_ADMIT_SERVICE": df})
    root = ET.fromstring(xml_str)
    code = root.find("./Codesets/Codeset[@Name='CS_ADMIT_SERVICE']/Code")
    assert code is not None
    assert code.get("StandardCode") is None
    assert code.get("StandardDisplay") is None


def test_definition_used_when_mapping_columns_absent():
    df = pd.DataFrame(
        {
            "Code": ["IND"],
            "Display": ["Industrial"],
            "Definition": ["ALL^Allergy Clinic"],
            "Standard Code": ["ALL"],
            "Standard Description": ["Allergy Clinic"],
        }
    )
    xml_str = build_transformer_xml({"CS_ADMIT_SERVICE": df})
    root = ET.fromstring(xml_str)
    code = root.find("./Codesets/Codeset[@Name='CS_ADMIT_SERVICE']/Code")
    assert code is not None
    assert code.get("StandardCode") == "ALL"
    assert code.get("StandardDisplay") == "Allergy Clinic"


def test_subdefinition_fills_missing_standard_fields():
    df = pd.DataFrame(
        {
            "Code": ["UNK"],
            "Display": ["Unknown"],
            "Subdefinition": ["UNK^Unknown"],
            "Standard Code": [""],
            "Standard Description": [""],
        }
    )
    xml_str = build_transformer_xml({"CS_ADMIN_GENDER": df})
    root = ET.fromstring(xml_str)
    code = root.find("./Codesets/Codeset[@Name='CS_ADMIN_GENDER']/Code")
    assert code is not None
    assert code.get("StandardCode") == "UNK"
    assert code.get("StandardDisplay") == "Unknown"


def test_mapped_std_description_preference():
    df = pd.DataFrame(
        {
            "Code": ["UNKNOWN", "01", "06"],
            "Display Value": ["Unknown", "Accident/Medical Coverage", "Crime Victim"],
            "Mapped_STD_DESCRIPTION": [
                "U^Unknown accident nature",
                "U^Unknown accident nature",
                "C^Assault and battery",
            ],
            "Standard Code": ["P", "T", "X"],
            "Standard Description": [
                "Accident on public road",
                "Occupational accident",
                "Assault and battery",
            ],
        }
    )
    xml_str = build_transformer_xml({"CS_ACCIDENT_CODE": df})
    root = ET.fromstring(xml_str)
    codes = root.findall("./Codesets/Codeset[@Name='CS_ACCIDENT_CODE']/Code")
    assert len(codes) == 3
    assert codes[0].get("StandardCode") == "U"
    assert codes[1].get("StandardCode") == "U"
    # Description matches for third row so explicit Standard Code is preferred
    assert codes[2].get("StandardCode") == "X"


def test_definition_overrides_mismatched_standard_code():
    df = pd.DataFrame(
        {
            "Code": ["UNKNOWN", "01"],
            "Display Value": ["Unknown", "Accident/Medical Coverage"],
            "Definition": ["U^Unknown accident nature", "U^Unknown accident nature"],
            "Mapped_STD_DESCRIPTION": ["Unknown accident nature", "Unknown accident nature"],
            "Standard Code": ["P", "T"],
            "Standard Description": ["Accident on public road", "Occupational accident"],
        }
    )
    xml_str = build_transformer_xml({"CS_ACCIDENT_CODE": df})
    root = ET.fromstring(xml_str)
    codes = root.findall("./Codesets/Codeset[@Name='CS_ACCIDENT_CODE']/Code")
    assert len(codes) == 2
    assert codes[0].get("StandardCode") == "U"
    assert codes[1].get("StandardCode") == "U"


def test_mapped_std_description_with_hyphen():
    df = pd.DataFrame(
        {
            "Code": ["OO"],
            "Display": ["HIPAA OPT-OUT"],
            "Mapped_STD_DESCRIPTION": ["HIPAA OPT-OUT"],
            "Standard Code": ["OO"],
            "Standard Description": ["HIPAA OPT-OUT"],
        }
    )
    xml_str = build_transformer_xml({"CS_PROTECTION_IND": df})
    root = ET.fromstring(xml_str)
    code = root.find("./Codesets/Codeset[@Name='CS_PROTECTION_IND']/Code")
    assert code is not None
    assert code.get("StandardCode") == "OO"
    assert code.get("StandardDisplay") == "HIPAA OPT-OUT"


def test_hyphenated_standard_code_not_split():
    df = pd.DataFrame(
        {
            "Code": ["I9"],
            "Display Value": ["ICD-9"],
            "Mapped_STD_DESCRIPTION": ["ICD-9"],
            "Standard Code": ["ICD-9"],
            "Standard Description": ["ICD-9"],
        }
    )
    xml_str = build_transformer_xml({"CS_DIAGNOSIS_CODE_METHOD": df})
    root = ET.fromstring(xml_str)
    code = root.find("./Codesets/Codeset[@Name='CS_DIAGNOSIS_CODE_METHOD']/Code")
    assert code is not None
    assert code.get("StandardCode") == "ICD-9"
    assert code.get("StandardDisplay") == "ICD-9"


def test_codeset_without_codes_self_closes():
    df = pd.DataFrame(
        {
            "Code": [""],
            "Display": [""],
            "OID": ["No OID"],
            "URL": ["http://example.com"],
        }
    )
    xml_str = build_transformer_xml({"CS_EMPTY": df})
    root = ET.fromstring(xml_str)
    cs = root.find("./Codesets/Codeset[@Name='CS_EMPTY']")
    assert cs is not None
    assert list(cs) == []


def test_no_xml_declaration():
    df = pd.DataFrame({"Code": ["A"], "Display": ["Alpha"]})
    xml_str = build_transformer_xml({"CS_ALPHA": df})
    assert not xml_str.lstrip().startswith("<?xml")
    

def test_mismatched_standard_code_uses_subdefinition_lookup():
    df = pd.DataFrame(
        {
            "Code": ["UNK"],
            "Display": ["Unknown"],
            "Mapped_STD_DESCRIPTION": ["Unknown"],
            "Subdefinition": ["UNK^Unknown"],
            "Standard Code": ["126485001"],
            "Standard Description": ["Hives"],
        }
    )
    xml_str = build_transformer_xml({"CS_ALLERGY_REACTION_CODE": df})
    root = ET.fromstring(xml_str)
    code = root.find("./Codesets/Codeset[@Name='CS_ALLERGY_REACTION_CODE']/Code")
    assert code is not None
    assert code.get("StandardCode") == "UNK"
    assert code.get("StandardDisplay") == "Unknown"
