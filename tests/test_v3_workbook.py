from pathlib import Path
import importlib

from codeset_ui_app.components.file_parser import load_workbook
from codex.validators.validate_codeset_tab_logic import validate_codeset_tab_logic

SAMPLE_V3 = Path(__file__).resolve().parents[1] / "Samples" / "Generic Codeset V3" / "(Repository) CHR Codeset.xlsx"


def test_file_parser_handles_v3_workbook():
    with SAMPLE_V3.open('rb') as fh:
        data, wb = load_workbook(fh)
    assert 'CS_GENDER' in data
    assert 'CS_GENDER' in wb.sheetnames


def test_validator_handles_v3_workbook():
    results = validate_codeset_tab_logic(SAMPLE_V3)
    assert any(r["sheet_name"] == "CS_GENDER" for r in results)


def test_definition_column_used_for_mapping_v3_workbook():
    app_module = importlib.import_module("codeset_ui_app.app")
    app_module._load_workbook_path(SAMPLE_V3, SAMPLE_V3.name)
    info = app_module.mapping_data["CS_DIAGNOSTIC_SERVICE_SECTION"]
    assert info["mapped_col"] == "DEFINITION"
    opts = app_module.dropdown_data["CS_DIAGNOSTIC_SERVICE_SECTION"]["DEFINITION"]
    assert "CARDIOLOGY" in opts
    assert info["map"]["CARDIOLOGY"] == "CARDIOLOGY^CARDIOLOGY"
    # cleanup global state
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


def test_v3_sheet_data_contains_values():
    app_module = importlib.import_module("codeset_ui_app.app")
    app_module._load_workbook_path(SAMPLE_V3, SAMPLE_V3.name)
    client = app_module.app.test_client()
    resp = client.get("/sheet/CS_DIAGNOSTIC_SERVICE_SECTION")
    assert resp.status_code == 200
    rows = resp.get_json()
    assert rows and rows[0]["CODE"] and rows[0]["DISPLAY VALUE"] and rows[0]["DEFINITION"]
    # cleanup
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

