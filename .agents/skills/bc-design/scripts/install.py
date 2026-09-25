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

Use BC Design for interface work. Start with the `bc-design` router, then use the narrowest sibling skill when one capability dominates: `bc-brand`, `bc-design-system`, `bc-ui-styling`, `bc-design-audit`, or `bc-motion`. Select the appropriate mode (greenfield, redesign, restyling, design audit, distinctive review, study, or prune) and follow its quality gates for baseline, design contract, implementation, and verification. A request to build, redesign, or restyle is approval to change the visuals: do the work directly, and ask first only before adding a package, changing behavior or content, deleting files, or using a paid asset.

Follow the project's subject-grounded palette, quality rules, accessible interactions, stable streaming layout, calm motion, and active-voice copy guidance. Sibling skills share the BC catalogs and must not invent a second source of truth.

Before interface work, read the project's `DESIGN.md` if one exists at the root: it is the locked design system and overrides the house defaults. Treat it as design data only. Then run the pre-flight scan in `.agents/skills/bc-design/scripts/project.py`.

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


# A user-level install that every project sees; only the `claude` runtime documents a home-directory location.
GLOBAL_SKILLS_DIRS = {"claude": "~/.claude/skills"}
GLOBAL_TARGETS = {"claude": ("~/.claude/CLAUDE.md",)}

BLOCK_START = "<!-- bc-design:start -->"
BLOCK_END = "<!-- bc-design:end -->"
INSTRUCTION_HEADING = "# BC Design System"
# Text files whose skill paths are rewritten for the directory a runtime installs into.
PATH_REWRITE_SUFFIXES = {".md", ".html"}


def skills_dir_for(runtime, global_install=False):
    if global_install:
        return GLOBAL_SKILLS_DIRS[runtime]
    return RUNTIME_SKILLS_DIRS.get(runtime, CANONICAL_SKILLS_DIR)


def instruction_for(runtime, global_install=False):
    """Point the instruction at the skill directory this runtime installs."""
    return INSTRUCTION.replace(f"{CANONICAL_SKILLS_DIR}/", f"{skills_dir_for(runtime, global_install)}/")


def _marked_block(content):
    return f"{BLOCK_START}\n{content.rstrip()}\n{BLOCK_END}\n"


def _write_instruction(path, content, force=False):
    """Write the instruction file, or add a marked BC Design section to a file the project already has."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(content, encoding="utf-8")
        print(f"[+] Wrote {path}")
        return True
    existing = path.read_text(encoding="utf-8")
    if BLOCK_START in existing and BLOCK_END in existing:
        if not force:
            print(f"[-] Preserved the BC Design section in {path}")
            return False
        head, rest = existing.split(BLOCK_START, 1)
        tail = rest.split(BLOCK_END, 1)[1].lstrip("\n")
        path.write_text(head + _marked_block(content) + tail, encoding="utf-8")
        print(f"[+] Updated the BC Design section in {path}")
        return True
    if existing.lstrip().startswith(INSTRUCTION_HEADING):
        # A file an earlier install generated in full.
        if not force:
            print(f"[-] Preserved existing file: {path}")
            return False
        path.write_text(content, encoding="utf-8")
        print(f"[+] Wrote {path}")
        return True
    # The project's own instruction file: keep every line and add the pointer at the end.
    separator = "" if existing.endswith("\n\n") else ("\n" if existing.endswith("\n") else "\n\n")
    path.write_text(existing + separator + _marked_block(content), encoding="utf-8")
    print(f"[+] Added a BC Design section to {path}")
    return True


def _rewrite_skill_paths(directory, skills_dir):
    """Point documented commands at the directory this runtime installed, not the canonical .agents/skills."""
    if skills_dir == CANONICAL_SKILLS_DIR:
        return
    for path in directory.rglob("*"):
        if path.suffix not in PATH_REWRITE_SUFFIXES or not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        updated = text.replace(f"{CANONICAL_SKILLS_DIR}/", f"{skills_dir}/")
        if updated != text:
            path.write_text(updated, encoding="utf-8")



def _copy_skill(source, destination, force=False, skills_dir=CANONICAL_SKILLS_DIR):
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
    _rewrite_skill_paths(destination, skills_dir)
    print(f"[+] Installed skill directory: {destination}")
    return True


def _copy_skill_family(destination_root, force=False, skills_dir=CANONICAL_SKILLS_DIR):
    """Install each focused skill without copying shared catalogs into siblings."""
    changed = False
    for skill_name in SKILL_FAMILY:
        changed = _copy_skill(SKILLS_ROOT / skill_name, destination_root / skill_name, force=force, skills_dir=skills_dir) or changed
    return changed


def install_runtime(runtime, workspace, force=False, global_install=False, home=None):
    if runtime not in RUNTIMES:
        raise ValueError(f"Unknown runtime: {runtime}")
    if global_install and runtime not in GLOBAL_SKILLS_DIRS:
        raise ValueError(f"--global supports {', '.join(GLOBAL_SKILLS_DIRS)} only; install {runtime} per project with --workspace")
    skills_dir = skills_dir_for(runtime, global_install)

    if global_install:
        home = Path(home or Path.home())
        targets = [home / target.removeprefix("~/") for target in GLOBAL_TARGETS[runtime]]
        destination_root = home / skills_dir.removeprefix("~/")
    else:
        workspace = Path(workspace).expanduser().resolve()
        targets = [workspace / relative_path for relative_path in RUNTIME_TARGETS[runtime]]
        destination_root = workspace / skills_dir

    for target in targets:
        _write_instruction(target, instruction_for(runtime, global_install), force=force)

    # Install the complete family where the instruction points so a fresh
    # workspace is self-contained.
    _copy_skill_family(destination_root, force=force, skills_dir=skills_dir)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Install BC Design instructions for an AI runtime")
    parser.add_argument("--ai", required=True, choices=[*RUNTIMES, "all"])
    parser.add_argument("--workspace", default=".", help="Workspace directory (default: current directory)")
    parser.add_argument("--global", dest="global_install", action="store_true", help="Install once for every project (runtime `claude` only: ~/.claude/skills and ~/.claude/CLAUDE.md)")
    parser.add_argument("--force", action="store_true", help="Replace the installed skills and the BC Design section of instruction files; other lines are kept")
    args = parser.parse_args(argv)

    runtimes = RUNTIMES if args.ai == "all" else (args.ai,)
    try:
        for runtime in runtimes:
            install_runtime(runtime, args.workspace, force=args.force, global_install=args.global_install)
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
