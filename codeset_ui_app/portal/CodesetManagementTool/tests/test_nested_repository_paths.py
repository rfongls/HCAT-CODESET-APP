from pathlib import Path
import sys
import importlib
from openpyxl import Workbook
from urllib.parse import quote


def test_nested_repository_scanning(tmp_path, monkeypatch):
    samples = tmp_path / "Samples"
    repo = samples / "CA" / "V7" / "QA" / "InterfacePackage" / "FortHealthcareRepository"
    codeset_dir = repo / "Database" / "CDR" / "Codesets"
    codeset_dir.mkdir(parents=True)
    wb_path = codeset_dir / "NestedCodeset.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.title = "Sheet1"
    ws.append(["CODE", "DISPLAY VALUE"])
    wb.save(wb_path)

    sys.path.append(str(Path(__file__).resolve().parents[1]))
    app_module = importlib.import_module("codeset_ui_app.app")
    monkeypatch.setattr(app_module, "SAMPLES_DIR", samples)
    app_module.refresh_repository_cache()

    repo_key = str(repo.relative_to(samples))
    rel_wb = str(wb_path.relative_to(repo))

    # ensure discovery stores repo by relative path and returns unique workbook
    client = app_module.app.test_client()
    resp = client.get(f"/workbooks/{quote(repo_key, safe='')}")
    assert resp.status_code == 200
    assert resp.get_json() == [rel_wb]

    # ensure workbook can be loaded without repository errors
    resp = client.post("/", data={"repo": repo_key, "workbook_name": rel_wb})
    assert resp.status_code == 200
    assert b"Repository not found" not in resp.data
