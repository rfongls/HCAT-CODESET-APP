from pathlib import Path

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
