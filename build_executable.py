"""Build standalone bundles for the Codeset UI app using PyInstaller.

The script wraps the Flask app together with its templates and static assets so
end users can run it without installing Python.  The default ``auto`` bundle
mode picks an output format that matches the host platform (``onefile`` for
Windows and Linux, ``onedir`` for macOS so a ``.app`` bundle is produced).

Examples:
    python build_executable.py
    python build_executable.py --bundle-mode onedir
    python build_executable.py --bundle-mode onedir --target-arch universal2
    python build_executable.py --bundle-mode onedir --archive codeset_app-macos

The resulting build artifacts are written to the ``dist`` directory. PyInstaller
must be installed before running this script.
"""

from __future__ import annotations

import argparse
import os
import shutil
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
        choices=("auto", "onefile", "onedir"),
        default="auto",
        help=(
            "Select PyInstaller's bundling strategy. 'auto' picks the most "
            "common option for the host platform, 'onefile' produces a single "
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
    parser.add_argument(
        "--archive",
        metavar="ZIP_PATH",
        help=(
            "Optional name of a .zip file to create from the built output. This "
            "requires 'onedir' bundle mode and is convenient for distributing "
            "macOS .app bundles."
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
        "--name",
        "codeset_app",
        "--noconfirm",
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

    args.append(str(app_path))

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
            f"{target_platform} machine or trigger the GitHub Actions workflow "
            "documented in the README to build for that platform."
        )

    bundle_mode = args.bundle_mode
    if bundle_mode == "auto":
        bundle_mode = "onedir" if target_platform == "mac" else "onefile"

    pyinstaller_args = build_pyinstaller_args(
        bundle_mode, target_platform, args.target_arch
    )

    print(
        "Running PyInstaller for Codeset UI app "
        f"({target_platform}, {bundle_mode})..."
    )
    PyInstaller.__main__.run(pyinstaller_args)

    root = Path(__file__).resolve().parent
    dist_dir = root / "dist"
    output_path = describe_output(dist_dir, bundle_mode, target_platform)

    archive_path = create_archive(
        dist_dir, bundle_mode, args.archive, target_platform
    )

    if archive_path is not None:
        print(f"Archived build to {archive_path}")

    print(f"Build complete. Primary output: {output_path}")

    if bundle_mode == "onedir" and target_platform != "mac":
        print(
            "Note: onedir mode on non-macOS platforms creates a directory "
            "containing the executable rather than a .app bundle."
        )


def describe_output(dist_dir: Path, bundle_mode: str, target_platform: str) -> Path:
    """Return the expected primary build artifact path."""

    if bundle_mode == "onefile":
        name = "codeset_app.exe" if target_platform == "windows" else "codeset_app"
        return dist_dir / name

    bundle_name = "codeset_app.app" if target_platform == "mac" else "codeset_app"
    return dist_dir / bundle_name


def create_archive(
    dist_dir: Path, bundle_mode: str, archive: str | None, target_platform: str
) -> Path | None:
    """Optionally create a zip archive from the build output."""

    if not archive:
        return None

    if bundle_mode != "onedir":
        raise SystemExit("--archive can only be used with 'onedir' bundle mode")

    source = describe_output(dist_dir, bundle_mode, target_platform)
    if not source.exists():
        raise SystemExit(
            f"Expected build output at {source} but it was not created. "
            "Check the PyInstaller logs above for errors."
        )

    archive_path = Path(archive)
    if archive_path.suffix.lower() != ".zip":
        archive_path = archive_path.with_suffix(".zip")

    if not archive_path.is_absolute():
        archive_path = dist_dir / archive_path

    archive_path.parent.mkdir(parents=True, exist_ok=True)

    base_name = archive_path.with_suffix("")
    if archive_path.exists():
        archive_path.unlink()

    created = shutil.make_archive(
        str(base_name),
        "zip",
        root_dir=source.parent,
        base_dir=source.name,
    )

    return Path(created)


if __name__ == "__main__":
    main()
