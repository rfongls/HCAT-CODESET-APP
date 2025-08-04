import re
from pathlib import Path

def test_comparison_highlighting_rules():
    css = Path('codeset_ui_app/assets/styles.css').read_text()
    # check header style
    assert re.search(r"\.codeset-table\s+th\.compare-header\s*{[^}]*background-color:\s*#008080", css)
    # check cell style
    assert re.search(r"\.codeset-table\s+td\.compare-col[^{}]*{[^}]*background-color:\s*#fff9c4", css)
