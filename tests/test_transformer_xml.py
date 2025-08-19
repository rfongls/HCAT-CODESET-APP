from pathlib import Path
import xml.etree.ElementTree as ET
import importlib

from codeset_ui_app.components.file_parser import load_workbook
from codeset_ui_app.utils.transformer_xml import build_transformer_xml
from codeset_ui_app.app import app, _load_workbook_path


def test_build_transformer_xml_generates_codeset():
    path = Path('Samples/Generic Codeset V4/(Health System) Codeset Template (Nexus Engine v4) (1).xlsx')
    with path.open('rb') as fh:
        data, _ = load_workbook(fh)
    xml_str = build_transformer_xml(data)
    root = ET.fromstring(xml_str)
    cs = root.find("./Fields/Codesets/Codeset[@Name='Diagnostic Service Section']")
    assert cs is not None
    assert cs.get('OID') == '2.16.840.1.114222.4.11.922'
    assert cs.get('URL') == 'PHIN VADS (CDC)'
    values = [v.text for v in cs.findall('Code')]
    assert 'CARD^CARDIOLOGY' in values
    # Ensure output is indented with each code on its own line
    assert '\n    <Codesets>' in xml_str
    assert '\n      <Codeset' in xml_str
    assert '\n        <Code>' in xml_str


def test_export_transformer_endpoint(tmp_path):
    path = Path('Samples/Generic Codeset V4/(Health System) Codeset Template (Nexus Engine v4) (1).xlsx')
    _load_workbook_path(path, path.name)
    with app.test_client() as c:
        resp = c.get('/transformer')
        assert resp.status_code == 200
        root = ET.fromstring(resp.data)
        assert root.find("./Fields/Codesets/Codeset[@Name='Diagnostic Service Section']") is not None
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
