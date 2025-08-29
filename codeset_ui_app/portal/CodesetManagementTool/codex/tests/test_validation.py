from pathlib import Path

from codex.validators.validate_codeset_tab_logic import validate_codeset_tab_logic


def test_validate_codeset_tab_logic():
    sample = Path(__file__).resolve().parents[2] / "codeset_ui_app" / "samples" / "Codeset Template.xlsx"
    results = validate_codeset_tab_logic(sample)
    assert isinstance(results, list)
    assert results, "No sheets found"
    assert all("sheet_name" in r for r in results)
