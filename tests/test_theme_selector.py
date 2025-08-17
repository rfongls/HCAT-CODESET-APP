from pathlib import Path
import sys
import importlib
from openpyxl import Workbook


def setup_app(tmp_path, monkeypatch):
    samples = tmp_path / "Samples"
    repo = samples / "repo1"
    repo.mkdir(parents=True)
    wb_path = repo / "Codeset1.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.title = "Sheet1"
    ws.append(["CODE", "DISPLAY VALUE"])
    wb.save(wb_path)
    sys.path.append(str(Path(__file__).resolve().parents[1]))
    app_module = importlib.import_module("codeset_ui_app.app")
    monkeypatch.setattr(app_module, "SAMPLES_DIR", samples)
    app_module.refresh_repository_cache()
    return app_module


def test_theme_options_and_overlay(tmp_path, monkeypatch):
    app_module = setup_app(tmp_path, monkeypatch)
    client = app_module.app.test_client()
    resp = client.get("/")
    html = resp.get_data(as_text=True)
    assert 'id="menuOpenTheme"' in html
    assert 'id="themeOverlay"' in html
    themes = [
        "light-purple",
        "light-blue",
        "light-gray",
        "light-orange",
        "light-pink",
        "light-green",
        "dark-blue",
        "dark-purple",
        "dark-orange",
        "dark-green",
        "dark-pink",
    ]
    for theme in themes:
        assert f'<option value="{theme}"' in html
