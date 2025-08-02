from pathlib import Path
import sys
import importlib
from openpyxl import Workbook


def setup_app(tmp_path, monkeypatch):
    samples = tmp_path / "Samples"
    repo = samples / "repo1"
    repo.mkdir(parents=True)
    wb_path = repo / "CodesetSample.xlsx"

    wb = Workbook()
    ws = wb.active
    ws.title = "Sheet1"
    ws.append(["CODE", "DISPLAY VALUE"])
    wb.save(wb_path)
    sys.path.append(str(Path(__file__).resolve().parents[1]))
    app_module = importlib.import_module("codeset_ui_app.app")
    monkeypatch.setattr(app_module, "SAMPLES_DIR", samples)
    return app_module, repo.name, wb_path.name


def test_workbooks_endpoint(tmp_path, monkeypatch):
    app_module, repo, fname = setup_app(tmp_path, monkeypatch)
    client = app_module.app.test_client()
    resp = client.get(f"/workbooks/{repo}")
    assert resp.status_code == 200
    assert fname in resp.get_json()


def test_load_workbook_via_repo(tmp_path, monkeypatch):
    app_module, repo, fname = setup_app(tmp_path, monkeypatch)
    client = app_module.app.test_client()
    resp = client.post("/", data={"repo": repo, "workbook_name": fname})
    assert resp.status_code == 200
    assert bytes(f"<option value=\"{fname}\" selected>", "utf-8") in resp.data

def test_repository_list(tmp_path, monkeypatch):
    app_module, repo, fname = setup_app(tmp_path, monkeypatch)
    client = app_module.app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
    assert f'<option value="{repo}"' in resp.get_data(as_text=True)

