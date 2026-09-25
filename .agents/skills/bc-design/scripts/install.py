#!/usr/bin/env python3
"""Install the BC Design skill into supported assistant runtimes."""

import argparse
import shutil
from pathlib import Path
import uuid


SKILL_ROOT = Path(__file__).resolve().parent.parent
SKILLS_ROOT = SKILL_ROOT.parent
SKILL_FAMILY = (
    "bc-design",
    "bc-brand",
    "bc-design-system",
    "bc-ui-styling",
    "bc-design-audit",
    "bc-motion",
)
RUNTIMES = (
    "claude",
    "codex",
    "antigravity",
    "kiro",
)

INSTRUCTION = """# BC Design System

Use BC Design for interface work. Start with the `bc-design` router, then use the narrowest sibling skill when one capability dominates: `bc-brand`, `bc-design-system`, `bc-ui-styling`, `bc-design-audit`, or `bc-motion`. Select the appropriate mode (greenfield, redesign, restyling, design audit, or distinctive review) and follow its quality gates for baseline, approval, implementation, and verification.

Follow the project's subject-grounded palette, quality rules, accessible interactions, stable streaming layout, calm motion, and active-voice copy guidance. Sibling skills share the BC catalogs and must not invent a second source of truth.

Router reference: `.agents/skills/bc-design/SKILL.md`
Workflow reference: `.agents/skills/bc-design/references/bc-design-workflow.md`
CLI: `python .agents/skills/bc-design/scripts/bc_design.py`
"""

CANONICAL_SKILLS_DIR = ".agents/skills"

# Runtimes that discover skills natively outside the shared .agents directory.
RUNTIME_SKILLS_DIRS = {
    "claude": ".claude/skills",
    "kiro": ".kiro/skills",
}

RUNTIME_TARGETS = {
    "claude": ("CLAUDE.md",),
    "codex": ("AGENTS.md",),
    "antigravity": ("GEMINI.md",),
    "kiro": (".kiro/steering/bc-design.md",),
}


def skills_dir_for(runtime):
    return RUNTIME_SKILLS_DIRS.get(runtime, CANONICAL_SKILLS_DIR)


def instruction_for(runtime):
    """Point the instruction at the skill directory this runtime installs."""
    return INSTRUCTION.replace(f"{CANONICAL_SKILLS_DIR}/", f"{skills_dir_for(runtime)}/")


def _write_text(path, content, force=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        print(f"[-] Preserved existing file: {path}")
        return False
    path.write_text(content, encoding="utf-8")
    print(f"[+] Wrote {path}")
    return True



def _copy_skill(source, destination, force=False):
    source = source.resolve()
    destination = destination.resolve()
    if destination == source:
        print(f"[-] Canonical skill directory already in place: {destination}")
        return False
    if destination.exists() and not force:
        print(f"[-] Preserved existing skill directory: {destination}")
        return False
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        staging = destination.parent / f".{destination.name}.install-{uuid.uuid4().hex}"
        backup = destination.parent / f".{destination.name}.backup-{uuid.uuid4().hex}"
        try:
            shutil.copytree(source, staging)
            destination.replace(backup)
            staging.replace(destination)
        except Exception:
            if not destination.exists() and backup.exists():
                backup.replace(destination)
            raise
        finally:
            if staging.exists():
                shutil.rmtree(staging)
            if backup.exists():
                shutil.rmtree(backup)
    else:
        shutil.copytree(source, destination)
    print(f"[+] Installed skill directory: {destination}")
    return True


def _copy_skill_family(destination_root, force=False):
    """Install each focused skill without copying shared catalogs into siblings."""
    changed = False
    for skill_name in SKILL_FAMILY:
        changed = _copy_skill(SKILLS_ROOT / skill_name, destination_root / skill_name, force=force) or changed
    return changed


def install_runtime(runtime, workspace, force=False):
    workspace = Path(workspace).expanduser().resolve()
    if runtime not in RUNTIMES:
        raise ValueError(f"Unknown runtime: {runtime}")

    for relative_path in RUNTIME_TARGETS[runtime]:
        _write_text(workspace / relative_path, instruction_for(runtime), force=force)

    # Install the complete family where the instruction points so a fresh
    # workspace is self-contained.
    _copy_skill_family(workspace / skills_dir_for(runtime), force=force)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Install BC Design instructions for an AI runtime")
    parser.add_argument("--ai", required=True, choices=[*RUNTIMES, "all"])
    parser.add_argument("--workspace", default=".", help="Workspace directory (default: current directory)")
    parser.add_argument("--force", action="store_true", help="Overwrite generated files and merge the skill directory")
    args = parser.parse_args(argv)

    runtimes = RUNTIMES if args.ai == "all" else (args.ai,)
    try:
        for runtime in runtimes:
            install_runtime(runtime, args.workspace, force=args.force)
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
