#!/usr/bin/env python3
"""Brainstorm where each component should come from, then let the user choose.

For every component in scope this prints three kinds of option, tailored to
what the project already has:

    A. Keep and restyle   the project's own implementation, if one exists
    B. Installed base     a primitive from the component library the project
                          already uses (shadcn/ui and similar), or the shadcn
                          primitive that would be added
    C. New library        candidate sources from newer libraries (blocks from
                          shadcnblocks, ReUI, 21st.dev, and others; effects
                          from React Bits and others) to offer as an upgrade

It never installs anything. Present the options, recommend one per
component, and install or paste only what the user approves. Library
contents change, so confirm a candidate exists and read its license before
proposing it as final.

Standard library only.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from project import _walk_files, scan_project  # noqa: E402

CATALOG = HERE.parent / "data" / "component-sources.csv"
COMPONENT_SUFFIXES = {".tsx", ".jsx", ".vue", ".svelte", ".astro", ".html"}
ALIASES = {
    "nav": "navbar", "header": "navbar", "features": "feature-list", "feature": "feature-list",
    "plans": "pricing", "testimonial": "testimonials", "logos": "logo-cloud", "numbers": "stats",
    "modal": "dialog", "drawer": "dialog", "menu": "dropdown-menu", "command": "command-palette",
    "charts": "chart", "graph": "chart", "notification": "toast", "empty": "empty-state",
    "3d": "3d-scene", "spatial": "3d-scene", "icon": "icons", "blog": "blog-cards", "grid": "bento",
}


def load_catalog():
    with CATALOG.open(encoding="utf-8", newline="") as handle:
        return {row["component"]: row for row in csv.DictReader(handle)}


def _split(value):
    return [item.strip() for item in value.split(";") if item.strip()]


def project_context(root):
    """What the project already has: libraries, shadcn files, and its own component files."""
    root = Path(root).resolve()
    findings = scan_project(root)
    shadcn = (root / "components.json").is_file()
    shadcn_files, own_files = set(), []
    for path in _walk_files(root):
        if path.suffix not in COMPONENT_SUFFIXES:
            continue
        if path.parent.name == "ui" and path.parent.parent.name == "components":
            shadcn_files.add(path.stem)
        else:
            own_files.append(path.relative_to(root).as_posix())
    other_libraries = [item for item in findings["components"] if not item.startswith("shadcn/ui")]
    return {"shadcn": shadcn, "shadcn_files": shadcn_files, "own_files": own_files, "libraries": other_libraries}


def _own_matches(component, own_files):
    words = {component, *(alias for alias, target in ALIASES.items() if target == component)}
    words |= {part for part in component.split("-") if len(part) > 3}
    matches = [rel for rel in own_files if any(word in Path(rel).stem.lower() for word in words)]
    return matches[:3]


def brainstorm(component, row, context):
    primitives = _split(row["shadcn_primitive"])
    if primitives and context["shadcn"]:
        installed = [p for p in primitives if p in context["shadcn_files"]]
        missing = [p for p in primitives if p not in context["shadcn_files"]]
        base = "shadcn/ui " + ", ".join(primitives)
        base += f" (installed: {', '.join(installed) or 'none'}"
        base += f"; add with npx shadcn@latest add {' '.join(missing)} after approval)" if missing else ")"
    elif primitives and context["libraries"]:
        base = f"The equivalent of shadcn {', '.join(primitives)} from the installed library: {'; '.join(context['libraries'])}"
    elif primitives:
        base = f"shadcn/ui {', '.join(primitives)} (adds shadcn/ui to the project; needs approval)"
    else:
        base = "No primitive; compose it from the project's layout and typography"
    return {
        "component": component,
        "category": row["category"],
        "keep_and_restyle": _own_matches(component, context["own_files"]),
        "installed_base": base,
        "new_library_blocks": _split(row["block_sources"]),
        "new_library_effects": _split(row["effect_sources"]),
        "house_fit": row["house_fit"],
        "restyle": row["restyle"],
    }


def format_brainstorm(options):
    lines = []
    for option in options:
        lines.append(f"{option['component']} ({option['category']})")
        keep = ", ".join(option["keep_and_restyle"]) or "no existing implementation found"
        lines.append(f"  A. Keep and restyle: {keep}")
        lines.append(f"  B. Installed base: {option['installed_base']}")
        sources = []
        if option["new_library_blocks"]:
            sources.append("blocks from " + ", ".join(option["new_library_blocks"]))
        if option["new_library_effects"]:
            sources.append("effects from " + ", ".join(option["new_library_effects"]))
        lines.append(f"  C. New library: {'; '.join(sources) if sources else 'none catalogued'}")
        lines.append(f"  House fit: {option['house_fit']}")
        lines.append(f"  Restyle: {option['restyle']}")
        lines.append("")
    lines.append(
        "Offer these options to the user with one recommendation per component. Confirm a candidate exists and read its "
        "license before proposing it as final. Install or paste nothing until the user approves; then restyle to BC tokens, "
        "audit, and run render_check.py."
    )
    return "\n".join(lines)


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Brainstorm component sources: keep, installed base, or a new library")
    parser.add_argument("components", nargs="*", help="Component types, for example: hero pricing chart navbar")
    parser.add_argument("--all", action="store_true", help="Brainstorm every catalogued component")
    parser.add_argument("--list", action="store_true", help="List catalogued component types")
    parser.add_argument("--workspace", default=".", help="Project root (default: current directory)")
    parser.add_argument("--json", action="store_true", help="Print options as JSON")
    args = parser.parse_args(argv)

    catalog = load_catalog()
    if args.list:
        for name, row in catalog.items():
            print(f"{name} ({row['category']})")
        return 0
    names = list(catalog) if args.all else [ALIASES.get(name.lower(), name.lower()) for name in args.components]
    if not names:
        parser.error("name at least one component, or use --all or --list")
    unknown = [name for name in names if name not in catalog]
    if unknown:
        print(f"Error: unknown component(s): {', '.join(unknown)}. Run with --list to see the catalogue.", file=sys.stderr)
        return 2
    root = Path(args.workspace)
    if not root.is_dir():
        print(f"Error: workspace not found: {root}", file=sys.stderr)
        return 2
    context = project_context(root)
    options = [brainstorm(name, catalog[name], context) for name in dict.fromkeys(names)]
    print(json.dumps(options, indent=2) if args.json else format_brainstorm(options))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
