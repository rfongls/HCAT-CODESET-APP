from pathlib import Path
import sys
import importlib
from openpyxl import Workbook


def setup_app(tmp_path, monkeypatch):
    samples = tmp_path / "Samples"
    repo = samples / "repo1Repository"
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
    app_module.refresh_repository_cache()
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


def test_import_updates_overwrites_file(tmp_path, monkeypatch):
    app_module, repo, fname = setup_app(tmp_path, monkeypatch)
    client = app_module.app.test_client()

    # load existing workbook via repo selection
    resp = client.post("/", data={"repo": repo, "workbook_name": fname})
    assert resp.status_code == 200

    from openpyxl import Workbook, load_workbook as xl_load
    import io

    wb = Workbook()
    ws = wb.active
    ws.title = "Sheet1"
    ws.append(["CODE", "DISPLAY VALUE"])
    ws.append(["A", "Alpha"])
    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)

    resp = client.post(
        "/import",
        data={"workbook": (buf, fname)},
        content_type="multipart/form-data",
    )
    assert resp.status_code == 200

    # ensure file on disk was replaced
    wb2 = xl_load(tmp_path / "Samples" / repo / fname)
    ws2 = wb2["Sheet1"]
    assert ws2.max_row == 2
    assert ws2["A2"].value == "A"

    # ensure in-memory data updated
    resp = client.get("/sheet/Sheet1")
    assert resp.get_json()[0]["CODE"] == "A"


def test_export_overwrites_original_file(tmp_path, monkeypatch):
    app_module, repo, fname = setup_app(tmp_path, monkeypatch)
    client = app_module.app.test_client()

    # load workbook and then export with new row
    resp = client.post("/", data={"repo": repo, "workbook_name": fname})
    assert resp.status_code == 200

    payload = {"Sheet1": [{"CODE": "B", "DISPLAY VALUE": "Beta"}]}
    resp = client.post("/export", json=payload)
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"
    assert resp.headers.get("Content-Disposition") is None

    from openpyxl import load_workbook as xl_load

    wb2 = xl_load(tmp_path / "Samples" / repo / fname)
    ws2 = wb2["Sheet1"]
    assert ws2.max_row == 2
    assert ws2["A2"].value == "B"
