#!/usr/bin/env python3
"""Regenerate runtime instruction files from the canonical BC Design installer.

The installer is the single source of truth for what each runtime receives.
This script writes that output to two places so neither can drift:

- ``adapters/<runtime>/``: a preview of a fresh install for each runtime.
- the repository root: this repository's own instruction files, which point at
  the canonical ``.agents/skills`` family (``BC.md`` points at ``.bc/skills``).

Run with ``--check`` to report drift without writing, as the validator does.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
ADAPTERS_DIR = ROOT / "adapters"
sys.path.insert(0, str(ROOT / ".agents" / "skills" / "bc-design" / "scripts"))
import install  # noqa: E402


def expected_adapter_files() -> dict[Path, str]:
    files = {}
    for runtime in install.RUNTIMES:
        for relative_path in install.RUNTIME_TARGETS[runtime]:
            files[ADAPTERS_DIR / runtime / relative_path] = install.render_target(runtime, relative_path)
    return files


def expected_root_files() -> dict[Path, str]:
    # The repository keeps its own editor settings, so only instruction files
    # are managed at the root.
    files = {}
    for runtime in install.RUNTIMES:
        instruction = install.instruction_for(runtime) if runtime == "bc" else install.INSTRUCTION
        for relative_path in install.RUNTIME_TARGETS[runtime]:
            if relative_path != install.VSCODE_SETTINGS:
                files[ROOT / relative_path] = instruction
    return files


def stale_adapter_files(expected: dict[Path, str]) -> list[Path]:
    if not ADAPTERS_DIR.is_dir():
        return []
    return sorted(path for path in ADAPTERS_DIR.rglob("*") if path.is_file() and path not in expected)


def check() -> list[str]:
    errors = []
    expected = {**expected_adapter_files(), **expected_root_files()}
    for path, content in sorted(expected.items()):
        relative = path.relative_to(ROOT).as_posix()
        if not path.is_file():
            errors.append(f"Missing generated instruction file: {relative}")
        elif path.read_text(encoding="utf-8") != content:
            errors.append(f"Generated instruction file drifted from install.py: {relative}")
    for path in stale_adapter_files(expected):
        errors.append(f"Stale adapter file not produced by install.py: {path.relative_to(ROOT).as_posix()}")
    return errors


def sync() -> None:
    expected = {**expected_adapter_files(), **expected_root_files()}
    for path in stale_adapter_files(expected):
        path.unlink()
        print(f"[-] Removed {path.relative_to(ROOT).as_posix()}")
    for path in sorted(ADAPTERS_DIR.rglob("*"), reverse=True):
        if path.is_dir() and not any(path.iterdir()):
            path.rmdir()
    for path, content in sorted(expected.items()):
        if path.is_file() and path.read_text(encoding="utf-8") == content:
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        # Write LF endings on every platform so the check stays byte-stable.
        path.write_text(content, encoding="utf-8", newline="\n")
        print(f"[+] Wrote {path.relative_to(ROOT).as_posix()}")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="Report drift without writing files")
    args = parser.parse_args(argv)
    if args.check:
        errors = check()
        for error in errors:
            print(f"[x] {error}")
        return 1 if errors else 0
    sync()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
