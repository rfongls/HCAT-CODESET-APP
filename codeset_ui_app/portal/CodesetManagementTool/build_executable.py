"""Build a standalone executable for the Codeset UI app using PyInstaller.

This script bundles the Flask app and its templates/assets into a single
executable so end users do not need to install Python or view the source code.

Usage:
    python build_executable.py

The resulting executable will be placed in the ``dist`` directory. PyInstaller
must be installed before running this script.
"""

from __future__ import annotations

import os
from pathlib import Path
import PyInstaller.__main__


def main() -> None:
    root = Path(__file__).resolve().parent
    app_path = root / "codeset_ui_app" / "app.py"
    assets_dir = root / "codeset_ui_app" / "assets"
    templates_dir = root / "codeset_ui_app" / "templates"

    PyInstaller.__main__.run([
        str(app_path),
        "--onefile",
        "--name",
        "codeset_app",
        "--add-data",
        f"{assets_dir}{os.pathsep}codeset_ui_app/assets",
        "--add-data",
        f"{templates_dir}{os.pathsep}codeset_ui_app/templates",
    ])


if __name__ == "__main__":
    main()
