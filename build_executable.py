"""Build standalone bundles for the Codeset UI app using PyInstaller.

The script wraps the Flask app together with its templates and static assets so
end users can run it without installing Python.  By default a single-file
executable (``--onefile``) is produced, matching the previous behaviour that
generated ``codeset_app.exe`` on Windows.

Examples:
    python build_executable.py
    python build_executable.py --bundle-mode onedir
    python build_executable.py --bundle-mode onedir --target-arch universal2

The resulting build artifacts are written to the ``dist`` directory. PyInstaller
must be installed before running this script.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Sequence

import PyInstaller.__main__


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse CLI options for configuring the PyInstaller build."""

    parser = argparse.ArgumentParser(
        description="Create distributable bundles of the Codeset UI app."
    )
    parser.add_argument(
        "--bundle-mode",
        choices=("onefile", "onedir"),
        default="onefile",
        help=(
            "Select PyInstaller's bundling strategy. 'onefile' produces a single "
            "binary (recommended for Windows), while 'onedir' creates an output "
            "directory that can contain a macOS .app bundle."
        ),
    )
    parser.add_argument(
        "--target-platform",
        choices=("auto", "windows", "mac", "linux"),
        default="auto",
        help=(
            "Platform to build for. PyInstaller does not support cross-platform "
            "compilation, so this should match the operating system you are "
            "running on."
        ),
    )
    parser.add_argument(
        "--target-arch",
        choices=("x86_64", "arm64", "universal2"),
        help=(
            "Optional architecture override for macOS builds. For example, use "
            "'universal2' when creating a bundle that runs on both Apple Silicon "
            "and Intel Macs."
        ),
    )
    return parser.parse_args(argv)


def normalise_platform(name: str) -> str:
    """Return a normalised platform label used by the build script."""

    name = name.lower()
    if name.startswith("win"):
        return "windows"
    if name in {"darwin", "mac", "macos", "osx"}:
        return "mac"
    if name.startswith("linux"):
        return "linux"
    return name


def build_pyinstaller_args(
    bundle_mode: str, target_platform: str, target_arch: str | None
) -> list[str]:
    """Construct the PyInstaller CLI invocation."""

    root = Path(__file__).resolve().parent
    app_path = root / "codeset_ui_app" / "app.py"
    assets_dir = root / "codeset_ui_app" / "assets"
    templates_dir = root / "codeset_ui_app" / "templates"

    args = [
        str(app_path),
        "--name",
        "codeset_app",
        "--add-data",
        f"{assets_dir}{os.pathsep}assets",
        "--add-data",
        f"{templates_dir}{os.pathsep}templates",
        "--hidden-import",
        "codeset_ui_app.utils.xlsx_sanitizer",
    ]

    if bundle_mode == "onefile":
        args.append("--onefile")
    else:
        args.append("--onedir")

    mac_onedir_bundle = target_platform == "mac" and bundle_mode == "onedir"

    if mac_onedir_bundle:
        # ``--windowed`` tells PyInstaller to emit a ``.app`` bundle instead of a
        # console executable when building on macOS.  This keeps the generated
        # output aligned with the README instructions so the Finder shows a
        # clickable application bundle in ``dist/codeset_app.app``.
        args.append("--windowed")

    if target_platform == "mac" and target_arch:
        args.extend(["--target-arch", target_arch])
    elif target_arch:
        raise SystemExit("--target-arch is only valid when building on macOS")

    return args


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)

    current_platform = normalise_platform(sys.platform)
    target_platform = (
        current_platform if args.target_platform == "auto" else args.target_platform
    )

    if target_platform != current_platform:
        raise SystemExit(
            "PyInstaller cannot cross-compile. Rerun this script on a "
            f"{target_platform} machine to build for that platform."
        )

    pyinstaller_args = build_pyinstaller_args(
        args.bundle_mode, target_platform, args.target_arch
    )

    print(
        "Running PyInstaller for Codeset UI app "
        f"({target_platform}, {args.bundle_mode})..."
    )
    PyInstaller.__main__.run(pyinstaller_args)


if __name__ == "__main__":
    main()
