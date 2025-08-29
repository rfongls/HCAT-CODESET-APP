from pathlib import Path
import sys
import importlib
import re
from openpyxl import Workbook


def setup_app(tmp_path, monkeypatch):
    samples = tmp_path / "Samples"
    repo1 = samples / "repo1Repository"
    repo2 = samples / "repo2Repository"
    repo1.mkdir(parents=True)
    repo2.mkdir(parents=True)
    wb1_path = repo1 / "Codeset1.xlsx"
    wb2_path = repo2 / "Codeset2.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.title = "Sheet1"
    ws.append(["CODE", "DISPLAY VALUE"])
    wb.save(wb1_path)
    wb.save(wb2_path)
    sys.path.append(str(Path(__file__).resolve().parents[1]))
    app_module = importlib.import_module("codeset_ui_app.app")
    monkeypatch.setattr(app_module, "SAMPLES_DIR", samples)
    app_module.refresh_repository_cache()
    return app_module, repo1.name, wb1_path.name, repo2.name, wb2_path.name


def test_compare_form_visibility_and_repo_exclusion(tmp_path, monkeypatch):
    app_module, repo1, wb1, repo2, _ = setup_app(tmp_path, monkeypatch)
    client = app_module.app.test_client()

    resp = client.get("/")
    html = resp.get_data(as_text=True)
    assert 'name="compare_repo"' not in html

    resp = client.post("/", data={"repo": repo1, "workbook_name": wb1})
    html = resp.get_data(as_text=True)
    assert 'name="compare_repo"' in html
    assert re.search(r'<div id="compare-card-modal"[^>]*class="[^"]*d-none', html)
    match = re.search(r'<select name="compare_repo"[^>]*>(.*?)</select>', html, re.DOTALL)
    assert match is not None
    select_html = match.group(1)
    assert f'<option value="{repo1}"' not in select_html
    assert f'<option value="{repo2}"' in select_html


def test_compare_selection_and_clear_button(tmp_path, monkeypatch):
    app_module, repo1, wb1, repo2, wb2 = setup_app(tmp_path, monkeypatch)
    client = app_module.app.test_client()

    client.post("/", data={"repo": repo1, "workbook_name": wb1})
    resp = client.post("/", data={"compare_repo": repo2, "compare_workbook_name": wb2})
    html = resp.get_data(as_text=True)

    assert f'<option value="{repo2}" selected>' in html
    assert f'<option value="{wb2}" selected>' in html
    assert 'Clear Comparison' in html
    assert 'name="end_compare"' in html

    resp = client.post("/", data={"end_compare": "1"})
    html = resp.get_data(as_text=True)
    assert re.search(r'<div id="compare-card-modal"[^>]*class="[^"]*d-none', html)
