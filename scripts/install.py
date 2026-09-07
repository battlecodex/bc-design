#!/usr/bin/env python3
"""Repository entry point for the canonical BC Design installer."""

from pathlib import Path
import runpy
import sys


INSTALLER_PATH = Path(__file__).resolve().parent.parent / ".agents" / "skills" / "bc-design" / "scripts" / "install.py"


def main():
    # Keep the historical repository-level option while delegating behavior to
    # the canonical installer, whose public option is --workspace.
    args = ["--workspace" if arg == "--target-dir" else arg for arg in sys.argv[1:]]
    sys.argv = [str(INSTALLER_PATH), *args]
    runpy.run_path(str(INSTALLER_PATH), run_name="__main__")


if __name__ == "__main__":
    main()
