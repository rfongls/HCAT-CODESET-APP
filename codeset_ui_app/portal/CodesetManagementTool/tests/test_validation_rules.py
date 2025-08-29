import pandas as pd
from codeset_ui_app.validators import validate_workbook


def test_validation_rules():
    df = pd.DataFrame([
        {
            "CODE": "A",
            "DISPLAY VALUE": "",
            "STANDARD_CODE": "1",
            "STANDARD_DESCRIPTION": "One",
            "MAPPED_STD_DESCRIPTION": "",
        },
        {
            "CODE": "",
            "DISPLAY VALUE": "Beta",
            "STANDARD_CODE": "",
            "STANDARD_DESCRIPTION": "",
            "MAPPED_STD_DESCRIPTION": "",
        },
        {
            "CODE": "A",
            "DISPLAY VALUE": "Alpha",
            "STANDARD_CODE": "2",
            "STANDARD_DESCRIPTION": "Two",
            "MAPPED_STD_DESCRIPTION": "Two",
        },
        {
            "CODE": "",
            "DISPLAY VALUE": "",
            "STANDARD_CODE": "3",
            "STANDARD_DESCRIPTION": "Three",
            "MAPPED_STD_DESCRIPTION": "",
        },
        {
            "CODE": "",
            "DISPLAY VALUE": "",
            "STANDARD_CODE": "",
            "STANDARD_DESCRIPTION": "",
            "MAPPED_STD_DESCRIPTION": "Mapped Only",
        },
    ])
    sheets = {"Sheet1": df}
    mapping = {
        "Sheet1": {
            "code_col": "CODE",
            "display_col": "DISPLAY VALUE",
            "mapped_col": "MAPPED_STD_DESCRIPTION",
            "std_col": "STANDARD_DESCRIPTION",
            "std_code_col": "STANDARD_CODE",
        }
    }
    errors = validate_workbook(sheets, mapping)
    assert any("DISPLAY VALUE required" in e for e in errors)
    assert any("CODE required" in e for e in errors)
    mapping_errors = [e for e in errors if "MAPPED_STD_DESCRIPTION required" in e]
    assert len(mapping_errors) == 1
    assert any("CODE required when MAPPED_STD_DESCRIPTION is provided" in e for e in errors)
    assert any("DISPLAY VALUE required when MAPPED_STD_DESCRIPTION is provided" in e for e in errors)
    assert any("duplicate CODE" in e for e in errors)


def test_validation_rules_mapped_std_code():
    df = pd.DataFrame([
        {
            "CODE": "A",
            "DISPLAY VALUE": "Alpha",
            "STANDARD_CODE": "1",
            "STANDARD_DESCRIPTION": "One",
            "MAPPED_STD_CODE": "",
        },
        {
            "CODE": "",
            "DISPLAY VALUE": "",
            "STANDARD_CODE": "2",
            "STANDARD_DESCRIPTION": "Two",
            "MAPPED_STD_CODE": "2",
        },
    ])
    sheets = {"Sheet1": df}
    mapping = {
        "Sheet1": {
            "code_col": "CODE",
            "display_col": "DISPLAY VALUE",
            "mapped_col": "MAPPED_STD_CODE",
            "std_col": "STANDARD_DESCRIPTION",
            "std_code_col": "STANDARD_CODE",
        }
    }
    errors = validate_workbook(sheets, mapping)
    assert any("MAPPED_STD_CODE required" in e for e in errors)
    assert any("CODE required when MAPPED_STD_CODE is provided" in e for e in errors)
    assert any("DISPLAY VALUE required when MAPPED_STD_CODE is provided" in e for e in errors)
