from pathlib import Path
import sys
import importlib
from openpyxl import Workbook
from openpyxl.comments import Comment


def setup_app(tmp_path, monkeypatch):
    samples = tmp_path / "Samples"
    repo1 = samples / "repo1"
    repo1.mkdir(parents=True)
    wb_path = repo1 / "Codeset1.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.title = "CS_ABNORMAL_FLAG"
    ws.append(["CODE", "DISPLAY VALUE"])
    ws["A1"].comment = Comment("This tab applies to the field OBX:8", "author")
    wb.save(wb_path)
    sys.path.append(str(Path(__file__).resolve().parents[1]))
    app_module = importlib.import_module("codeset_ui_app.app")
    monkeypatch.setattr(app_module, "SAMPLES_DIR", samples)
    app_module.refresh_repository_cache()
    return app_module, repo1.name, wb_path.name


def test_field_comment_display(tmp_path, monkeypatch):
    app_module, repo, wb_name = setup_app(tmp_path, monkeypatch)
    client = app_module.app.test_client()
    resp = client.post("/", data={"repo": repo, "workbook_name": wb_name})
    html = resp.get_data(as_text=True)
    assert "Fields" in html
    assert "OBX:8" in html

