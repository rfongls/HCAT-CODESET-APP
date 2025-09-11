from pathlib import Path
import xml.etree.ElementTree as ET
import importlib
import json
import re
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
    assert '\n  <Fields>' in normalized
    assert '\n  <Codesets>' in normalized
    assert '\n    <Codeset' in normalized
    assert '\n      <Code ' in normalized


def test_build_transformer_xml_disables_freetext():
    path = Path('Samples/Generic Codeset V4/(Health System) Codeset Template (Nexus Engine v4) (1).xlsx')
    with path.open('rb') as fh:
        data, _ = load_workbook(fh)
    xml_str = build_transformer_xml(data, {'CS_RACE': True})
    root = ET.fromstring(xml_str)
    field = root.find("./Fields/Field[@Codeset='CS_RACE']")
    assert field is not None and field.get('Enabled') == 'False'
    other = root.find("./Fields/Field[@Codeset='CS_LANGUAGE']")
    assert other is not None and other.get('Enabled') == 'True'


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


def test_export_transformer_respects_freetext(tmp_path):
    path = Path('Samples/Generic Codeset V4/(Health System) Codeset Template (Nexus Engine v4) (1).xlsx')
    _load_workbook_path(path, path.name)
    with app.test_client() as c:
        resp = c.get('/transformer', query_string={'freetext': json.dumps({'CS_RACE': True})})
        assert resp.status_code == 200
        root = ET.fromstring(resp.data)
        field = root.find("./Fields/Field[@Codeset='CS_RACE']")
        assert field is not None and field.get('Enabled') == 'False'
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
    

def test_alignment_of_fields_and_codes():
    path = Path('Samples/Generic Codeset V4/(Health System) Codeset Template (Nexus Engine v4) (1).xlsx')
    with path.open('rb') as fh:
        data, _ = load_workbook(fh)
    xml_str = build_transformer_xml(data)
    lines = xml_str.split('\r\n')

    field_lines = [l for l in lines if l.strip().startswith('<Field ')]
    assert len({l.index('Codeset=') for l in field_lines}) == 1
    assert len({l.index('OutputType=') for l in field_lines}) == 1
    assert len({l.index('Enabled=') for l in field_lines}) == 1
    assert len({l.index('Description=') for l in field_lines}) == 1

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
