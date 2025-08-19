from pathlib import Path
import xml.etree.ElementTree as ET

from codeset_ui_app.components.file_parser import load_workbook
from codeset_ui_app.utils.transformer_xml import build_transformer_xml


def test_build_transformer_xml_generates_codeset():
    path = Path('Samples/Generic Codeset V4/(Health System) Codeset Template (Nexus Engine v4) (1).xlsx')
    with path.open('rb') as fh:
        data, _ = load_workbook(fh)
    xml_str = build_transformer_xml(data)
    root = ET.fromstring(xml_str)
    cs = root.find("./Fields/Codeset[@name='Diagnostic Service Section']")
    assert cs is not None
    assert cs.get('oid') == '2.16.840.1.114222.4.11.922'
    assert cs.get('url') == 'PHIN VADS (CDC)'
    values = [v.text for v in cs.findall('Value')]
    assert 'CARD^CARDIOLOGY' in values
