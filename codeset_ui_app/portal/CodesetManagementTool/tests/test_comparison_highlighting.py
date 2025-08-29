import re
from pathlib import Path

def test_comparison_highlighting_rules():
    css = Path('codeset_ui_app/assets/styles.css').read_text()
    # check header style
    assert re.search(r"\.codeset-table\s+th\.compare-header\s*{[^}]*background-color:\s*var\(--secondary-color\)", css)
    # check cell style
    assert re.search(r"\.codeset-table\s+td\.compare-col[^{}]*{[^}]*background-color:\s*var\(--highlight-color\)", css)
    # check repo/workbook selection highlight (primary and comparison)
    assert re.search(r"\.selected-primary,\s*\.selected-compare\s*{[^}]*background-color:\s*var\(--highlight-color\)", css)
    # sidebar colors
    assert re.search(r"#fields-box\s*{[^}]*background-color:\s*var\(--highlight-color\)", css)
    assert re.search(r"#fields-box\s*{[^}]*color:\s*var\(--text-color\)", css)
    assert re.search(r"#requirements-box\s*{[^}]*background-color:\s*var\(--secondary-color\)", css)
    assert re.search(r"#requirements-box\s*{[^}]*color:\s*var\(--text-color\)", css)
    assert re.search(r"#errors-box\s*{[^}]*color:\s*var\(--text-color\)", css)
    assert re.search(r"#fields-box\s*\.alert-heading,\s*#requirements-box\s*\.alert-heading,\s*#errors-box\s*\.alert-heading\s*{[^}]*font-weight:\s*700", css)
