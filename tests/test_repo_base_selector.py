from pathlib import Path
import sys
import importlib
from openpyxl import Workbook


def test_repository_folder_selection(tmp_path, monkeypatch):
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
    monkeypatch.setattr(app_module, "CONFIG_FILE", tmp_path / "repo_base.txt")
    monkeypatch.setattr(app_module, "SAMPLES_DIR", None)
    app_module.refresh_repository_cache()

    client = app_module.app.test_client()
    resp = client.get("/")
    text = resp.get_data(as_text=True)
    assert "Select repository folder" in text
    assert "js-repo-browse" in text
    assert "js-repo-save" in text
    assert 'name="repo_base"' in text
    assert 'class="form-control selected-primary js-repo-base"' in text
    assert 'placeholder="Enter folder path"' in text
    assert '<button type="submit" class="btn btn-primary w-100 js-repo-load" disabled>' in text
    assert 'repo-base-picker' not in text
    assert f"<option value=\"{repo.name}\"" not in text

    resp = client.post("/", data={"repo_base": str(samples)})
    text2 = resp.get_data(as_text=True)
    assert f"<option value=\"{repo.name}\"" in text2
    assert 'class="form-control selected-primary js-repo-base"' in text2
