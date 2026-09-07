#!/usr/bin/env python3
"""Repository entry point for the canonical BC Design CLI."""

from pathlib import Path
import runpy


CLI_PATH = Path(__file__).resolve().parent.parent / ".agents" / "skills" / "bc-design" / "scripts" / "bc_design.py"


if __name__ == "__main__":
    runpy.run_path(str(CLI_PATH), run_name="__main__")
