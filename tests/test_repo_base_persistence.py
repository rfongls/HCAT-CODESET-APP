from pathlib import Path
import sys
import importlib
from openpyxl import Workbook


def test_repository_folder_persisted(tmp_path, monkeypatch):
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
    config = tmp_path / "repo_base.txt"
    monkeypatch.setattr(app_module, "CONFIG_FILE", config)
    monkeypatch.setattr(app_module, "SAMPLES_DIR", None)
    app_module.refresh_repository_cache()

    client = app_module.app.test_client()
    client.post("/", data={"repo_base": str(samples), "save_repo_base": "1"})
    assert config.read_text().strip() == str(samples)

    # simulate restart
    monkeypatch.setattr(app_module, "SAMPLES_DIR", None)
    app_module.refresh_repository_cache()
    app_module.load_repository_base()
    assert app_module.SAMPLES_DIR == samples
    assert str(repo.relative_to(samples)) in app_module.REPOSITORY_CACHE
