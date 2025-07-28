"""Automatically install required packages if they are missing."""
from __future__ import annotations

import subprocess
import sys
from importlib import util

REQUIRED_PACKAGES = [
    "streamlit",
    "pandas",
    "openpyxl",
    "xlsxwriter",
    "streamlit-aggrid",
    "flask",
]


def ensure_installed() -> None:
    """Install any missing packages at runtime."""
    for package in REQUIRED_PACKAGES:
        if util.find_spec(package) is None:
            subprocess.check_call([
                sys.executable,
                "-m",
                "pip",
                "install",
                package,
            ])


if __name__ == "__main__":
    ensure_installed()
