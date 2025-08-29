from pathlib import Path
import sys
import importlib
from openpyxl import Workbook

def setup_app(tmp_path, monkeypatch):
    samples = tmp_path / "Samples"
    repo = samples / "repo1Repository"
    repo.mkdir(parents=True)
    wb1_path = repo / "Codeset1.xlsx"
    wb2_path = repo / "Codeset2.xlsx"
    wb1 = Workbook()
    ws1 = wb1.active
    ws1.title = "Sheet1"
    ws1.append(["CODE", "DISPLAY VALUE", "MAPPED_STD_DESCRIPTION"])
    ws1.append(["A", "Alpha", "Desc1"])
    wb1.save(wb1_path)
    wb2 = Workbook()
    ws2 = wb2.active
    ws2.title = "Sheet1"
    ws2.append(["CODE", "DISPLAY VALUE", "MAPPED_STD_DESCRIPTION"])
    ws2.append(["B", "Beta", "Desc2"])
    wb2.save(wb2_path)
    sys.path.append(str(Path(__file__).resolve().parents[1]))
    app_module = importlib.import_module("codeset_ui_app.app")
    monkeypatch.setattr(app_module, "SAMPLES_DIR", samples)
    app_module.refresh_repository_cache()
    return app_module, repo.name, wb1_path.name, wb2_path.name


def test_comparison_columns(tmp_path, monkeypatch):
    app_module, repo, main_wb, cmp_wb = setup_app(tmp_path, monkeypatch)
    client = app_module.app.test_client()
    client.post("/", data={"repo": repo, "workbook_name": main_wb})
    client.post("/", data={"compare_repo": repo, "compare_workbook_name": cmp_wb})
    resp = client.get("/sheet/Sheet1")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "CODE_COMPARE" in data[0]
    assert data[0]["CODE_COMPARE"] == "B"
    assert data[0]["DISPLAY_VALUE_COMPARE"] == "Beta"
    client.post("/", data={"end_compare": "1"})
    resp = client.get("/sheet/Sheet1")
    data = resp.get_json()
    assert "CODE_COMPARE" not in data[0]
