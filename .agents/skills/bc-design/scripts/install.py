#!/usr/bin/env python3
"""Install the BC Design skill into supported assistant runtimes."""

import argparse
import json
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
    "bc",
    "cursor",
    "windsurf",
    "antigravity",
    "copilot",
    "kiro",
    "codex",
    "qoder",
    "vscode",
)

INSTRUCTION = """# BC Design System

Use BC Design for interface work. Start with the `bc-design` router, then use the narrowest sibling skill when one capability dominates: `bc-brand`, `bc-design-system`, `bc-ui-styling`, `bc-design-audit`, or `bc-motion`. Select the appropriate mode (greenfield, redesign, restyling, design audit, or distinctive review) and follow its quality gates for baseline, approval, implementation, and verification.

Follow the project's subject-grounded palette, quality rules, accessible interactions, stable streaming layout, calm motion, and active-voice copy guidance. Sibling skills share the BC catalogs and must not invent a second source of truth.

Router reference: `.agents/skills/bc-design/SKILL.md`
Workflow reference: `.agents/skills/bc-design/references/bc-design-workflow.md`
CLI: `python .agents/skills/bc-design/scripts/bc_design.py`
"""

BC_INSTRUCTION = INSTRUCTION.replace(
    ".agents/skills/bc-design",
    ".bc/skills/bc-design",
)

RUNTIME_TARGETS = {
    "bc": ("BC.md",),
    "cursor": (".cursor/rules/bc-design.mdc", ".cursorrules"),
    "windsurf": (".windsurfrules",),
    "antigravity": ("GEMINI.md",),
    "copilot": (".github/copilot-instructions.md",),
    "kiro": (".kiro/rules/bc-design.md",),
    "codex": ("AGENTS.md",),
    "qoder": (".qoder/rules/bc-design.md",),
    "vscode": (".vscode/settings.json", ".github/copilot-instructions.md"),
}


def _write_text(path, content, force=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        print(f"[-] Preserved existing file: {path}")
        return False
    path.write_text(content, encoding="utf-8")
    print(f"[+] Wrote {path}")
    return True


def _write_vscode_settings(path, force=False):
    settings = {}
    if path.exists():
        try:
            settings = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            if not force:
                raise ValueError(f"Existing VS Code settings are not valid JSON: {path}") from exc
            settings = {}
    if not isinstance(settings, dict):
        raise ValueError(f"Existing VS Code settings must be a JSON object: {path}")
    settings.setdefault(
        "bcDesign.instructions",
        "Use .agents/skills/bc-design/SKILL.md for interface guidance.",
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        print(f"[-] Preserved existing file: {path}")
        return False
    path.write_text(json.dumps(settings, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
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
        destination = workspace / relative_path
        if relative_path == ".vscode/settings.json":
            _write_vscode_settings(destination, force=force)
        else:
            instruction = BC_INSTRUCTION if runtime == "bc" else INSTRUCTION
            _write_text(destination, instruction, force=force)

    if runtime == "bc":
        _copy_skill_family(workspace / ".bc" / "skills", force=force)
    else:
        # Every non-BC instruction points at the workspace .agents router.
        # Install the complete family so a fresh workspace is self-contained.
        _copy_skill_family(workspace / ".agents" / "skills", force=force)


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
