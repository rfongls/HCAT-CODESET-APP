from pathlib import Path
import sys
import importlib


def test_close_buttons_render(tmp_path, monkeypatch):
    sys.path.append(str(Path(__file__).resolve().parents[1]))
    app_module = importlib.import_module("codeset_ui_app.app")
    monkeypatch.setattr(app_module, "CONFIG_FILE", tmp_path / "repo_base.txt")
    monkeypatch.setattr(app_module, "SAMPLES_DIR", None)
    app_module.refresh_repository_cache()

    client = app_module.app.test_client()
    resp = client.get("/")
    text = resp.get_data(as_text=True)

    assert '<button id="overlayClose" type="button" class="btn btn-danger text-white fs-4" aria-label="Close">&times;</button>' in text
    assert '<button id="themeOverlayClose" type="button" class="btn btn-danger text-white fs-4" aria-label="Close">&times;</button>' in text

    css = (Path(__file__).resolve().parents[1] / "codeset_ui_app/assets/styles.css").read_text()
    assert ".overlay-header .btn-danger" in css
    assert "box-shadow" in css

