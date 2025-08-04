import re
from pathlib import Path

def test_comparison_highlighting_rules():
    css = Path('codeset_ui_app/assets/styles.css').read_text()
    # check header style
    assert re.search(r"\.codeset-table\s+th\.compare-header\s*{[^}]*background-color:\s*#42b0f5", css)
    # check cell style
    assert re.search(r"\.codeset-table\s+td\.compare-col[^{}]*{[^}]*background-color:\s*#fff9c4", css)
    # check repo/workbook selection highlight
    assert re.search(r"\.selected-primary\s*{[^}]*background-color:\s*#fff9c4", css)
    # check comparison selection highlight
    assert re.search(r"\.selected-compare\s*{[^}]*background-color:\s*#ffd4c4", css)
    # sidebar colors
    assert re.search(r"#fields-box\s*{[^}]*background-color:\s*#fff9c4", css)
    assert re.search(r"#requirements-box\s*{[^}]*background-color:\s*#42b0f5", css)
