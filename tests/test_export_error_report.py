import sys
from pathlib import Path
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
    ws.append([
        "CODE",
        "DISPLAY VALUE",
        "STANDARD_CODE",
        "STANDARD_DESCRIPTION",
        "MAPPED_STD_DESCRIPTION",
    ])
    wb.save(wb_path)
    sys.path.append(str(Path(__file__).resolve().parents[1]))
    app_module = importlib.import_module("codeset_ui_app.app")
    monkeypatch.setattr(app_module, "SAMPLES_DIR", samples)
    app_module.refresh_repository_cache()
    return app_module, repo.name, wb_path.name

def test_export_error_report_contains_validation_messages(tmp_path, monkeypatch):
    app_module, repo, fname = setup_app(tmp_path, monkeypatch)
    client = app_module.app.test_client()
    resp = client.post("/", data={"repo": repo, "workbook_name": fname})
    assert resp.status_code == 200

    payload = {
        "Sheet1": [
            {
                "CODE": "A",
                "DISPLAY VALUE": "",
                "STANDARD_CODE": "1",
                "STANDARD_DESCRIPTION": "One",
                "MAPPED_STD_DESCRIPTION": "",
            }
        ]
    }
    resp = client.post("/export_errors", json=payload)
    assert resp.status_code == 200
    text = resp.data.decode()
    assert "Sheet1 row 2: DISPLAY VALUE required when CODE is provided" in text
