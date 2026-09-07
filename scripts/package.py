#!/usr/bin/env python3
"""Build a deterministic BC Design source distribution."""

import argparse
import json
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / ".agents" / "skills" / "bc-design" / "scripts"))
from normalize_catalog import build_report


EXCLUDED_DIRS = {".git", "__pycache__", ".pytest_cache", "dist", "design-system", "docs"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}
EXCLUDED_NAMES = {"full-test.log"}


def iter_release_files():
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT)
        if any(part in EXCLUDED_DIRS for part in relative.parts):
            continue
        if path.name in EXCLUDED_NAMES:
            continue
        if path.suffix.lower() in EXCLUDED_SUFFIXES:
            continue
        yield path, relative


def build_archive(output):
    preflight()
    manifest = json.loads((ROOT / "skill.json").read_text(encoding="utf-8"))
    output = Path(output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    prefix = "bc-design"
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path, relative in iter_release_files():
            info = zipfile.ZipInfo(f"{prefix}/{relative.as_posix()}")
            info.date_time = (2026, 1, 1, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes())
    return output, manifest["version"]


def computed_catalog_metrics(report=None):
    """Derive public catalog totals from the normalized source data."""
    report = report or build_report()
    data = ROOT / ".agents" / "skills" / "bc-design" / "data"
    return {
        "styles": sum(report["files"].get("styles.csv", {}).values()),
        "palettes": sum(report["files"].get("colors.csv", {}).values()),
        "typographyPairings": sum(report["files"].get("typography.csv", {}).values()),
        "uxGuidelines": sum(report["files"].get("ux-guidelines.csv", {}).values()),
        "charts": sum(report["files"].get("charts.csv", {}).values()),
        "motionGuidance": sum(report["files"].get("motion.csv", {}).values()),
        "stackCatalogs": len(list((data / "stacks").glob("*.csv"))),
        "focusedStackGuides": len(list((ROOT / ".agents" / "skills" / "bc-design" / "stacks").glob("*.md"))),
    }


def sync_manifest_catalogs(manifest_path=None, report=None):
    """Update manifest catalog totals from normalized data and return it."""
    manifest_path = Path(manifest_path or ROOT / "skill.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected = computed_catalog_metrics(report)
    if manifest.get("catalogs") != expected:
        manifest["catalogs"] = expected
        manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return manifest


def preflight():
    """Reject releases with stale alignment metrics or a drifting BC mirror."""
    report = build_report()
    if report["errors"] or report["totals"].get("unclassified", 0):
        raise ValueError("catalog alignment preflight failed")
    manifest_path = ROOT / "skill.json"
    manifest = sync_manifest_catalogs(manifest_path, report)
    expected = computed_catalog_metrics(report)
    if manifest.get("catalogs") != expected:
        raise ValueError(f"skill.json catalog metrics are stale: expected {expected}")
    canonical = ROOT / ".agents" / "skills"
    mirror = ROOT / ".bc" / "skills"
    for left in sorted(path for path in canonical.rglob("*") if path.is_file() and path.suffix not in EXCLUDED_SUFFIXES):
        relative = left.relative_to(canonical)
        right = mirror / relative
        if not right.is_file() or left.read_bytes() != right.read_bytes():
            raise ValueError(f"skill mirror drift: {relative}")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Build a clean BC Design release archive")
    parser.add_argument("--output", help="Archive path; defaults to dist/bc-design-VERSION.zip")
    args = parser.parse_args(argv)
    manifest = json.loads((ROOT / "skill.json").read_text(encoding="utf-8"))
    output = args.output or ROOT / "dist" / f"bc-design-{manifest['version']}.zip"
    archive, version = build_archive(output)
    print(f"Built BC Design {version}: {archive}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
