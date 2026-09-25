#!/usr/bin/env python3
"""BC Design Repository & Skill Integrity Validator.

Zero external dependencies (pure Python standard library).
Validates:
1. Catalog alignment and normalized counts against skill.json.
2. Complete byte-for-byte parity between .agents/skills/ and .bc/skills/.
3. Presence and integrity of internal spatial assets and runnable generators.
4. Non-existence of binary ZIP archives, caches, or machine-specific paths.
5. Runtime instruction files in adapters/ and the root match install.py output.
6. Upstream notices ship inside the installed skill directory.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / ".agents" / "skills" / "bc-design"
sys.path.insert(0, str(SKILL_DIR / "scripts"))
from normalize_catalog import build_report  # noqa: E402
sys.path.insert(0, str(ROOT / "scripts"))
import sync_adapters  # noqa: E402
from spatial import SPATIAL_GENERATOR_PRESETS, SPATIAL_PRESET_ALIASES  # noqa: E402

EXCLUDED_SUFFIXES = {".pyc", ".pyo"}
EXCLUDED_PARTS = {"__pycache__", ".git", ".pytest_cache"}
CACHE_DIR_NAMES = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".tox"}


def computed_catalog_metrics(report=None) -> dict[str, int]:
    """Derive public catalog totals from normalized source data and spatial CSV."""
    report = report or build_report()
    data = SKILL_DIR / "data"

    # Count rows in spatial-effects.csv
    spatial_csv = data / "spatial-effects.csv"
    spatial_count = 0
    if spatial_csv.is_file():
        with spatial_csv.open(encoding="utf-8-sig", newline="") as handle:
            spatial_count = sum(1 for _ in csv.DictReader(handle))

    # Keep the manifest count tied to the actual dispatcher contract.
    spatial_generators_count = len(SPATIAL_GENERATOR_PRESETS)

    return {
        "styles": sum(report["files"].get("styles.csv", {}).values()),
        "palettes": sum(report["files"].get("colors.csv", {}).values()),
        "typographyPairings": sum(report["files"].get("typography.csv", {}).values()),
        "uxGuidelines": sum(report["files"].get("ux-guidelines.csv", {}).values()),
        "charts": sum(report["files"].get("charts.csv", {}).values()),
        "motionGuidance": sum(report["files"].get("motion.csv", {}).values()),
        "spatialEffects": spatial_count,
        "spatialGenerators": spatial_generators_count,
        "stackCatalogs": len(list((data / "stacks").glob("*.csv"))),
        "focusedStackGuides": len(list((SKILL_DIR / "stacks").glob("*.md"))),
    }


def validate_manifest(fix: bool = False) -> list[str]:
    """Validate skill.json version and catalog counts."""
    errors: list[str] = []
    manifest_path = ROOT / "skill.json"
    if not manifest_path.is_file():
        return ["skill.json not found in repository root"]

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("version") != "1.1.0":
        errors.append(f"skill.json version expected '1.1.0', found '{manifest.get('version')}'")

    expected_catalogs = computed_catalog_metrics()
    current_catalogs = manifest.get("catalogs", {})
    if current_catalogs != expected_catalogs:
        if fix:
            manifest["catalogs"] = expected_catalogs
            manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        else:
            diff = {k: (current_catalogs.get(k), expected_catalogs.get(k)) for k in expected_catalogs if current_catalogs.get(k) != expected_catalogs.get(k)}
            errors.append(f"skill.json catalog metrics mismatch: {diff}")

    spatial_meta = manifest.get("spatial", {})
    expected_effects = expected_catalogs["spatialEffects"]
    if spatial_meta.get("effectsCount") != expected_effects:
        errors.append(
            f"skill.json spatial.effectsCount expected {expected_effects}, "
            f"found {spatial_meta.get('effectsCount')}"
        )
    if spatial_meta.get("generators") != list(SPATIAL_GENERATOR_PRESETS):
        errors.append(
            "skill.json spatial.generators does not match the runtime generator contract: "
            f"expected {list(SPATIAL_GENERATOR_PRESETS)}, found {spatial_meta.get('generators')}"
        )
    if spatial_meta.get("aliases") != SPATIAL_PRESET_ALIASES:
        errors.append("skill.json spatial.aliases does not match the runtime alias contract")

    return errors


def validate_mirror_parity() -> list[str]:
    """Verify byte-for-byte parity between .agents/skills/ and .bc/skills/."""
    errors: list[str] = []
    canonical = ROOT / ".agents" / "skills"
    mirror = ROOT / ".bc" / "skills"

    def files_under(base: Path) -> dict[Path, Path]:
        if not base.is_dir():
            return {}
        result = {}
        for path in base.rglob("*"):
            if not path.is_file():
                continue
            if any(part in EXCLUDED_PARTS for part in path.parts) or path.suffix in EXCLUDED_SUFFIXES:
                continue
            result[path.relative_to(base)] = path
        return result

    canonical_files = files_under(canonical)
    mirror_files = files_under(mirror)
    for relative in sorted(canonical_files.keys() | mirror_files.keys()):
        left = canonical_files.get(relative)
        right = mirror_files.get(relative)
        if left is None:
            errors.append(f"Extra mirror file: .bc/skills/{relative}")
        elif right is None:
            errors.append(f"Missing mirror file: .bc/skills/{relative}")
        elif left.read_bytes() != right.read_bytes():
            errors.append(f"Mirror drift detected: {relative}")

    return errors


def validate_prohibited_artifacts() -> list[str]:
    """Verify no ZIP archives or cache directories exist in the working tree."""
    errors: list[str] = []
    if not ROOT.is_dir():
        return [f"Repository root not found: {ROOT}"]
    def is_gitignored(path: Path) -> bool:
        """Treat generated caches as clean when the repository ignores them."""
        try:
            relative = path.relative_to(ROOT).as_posix()
            result = subprocess.run(
                ["git", "check-ignore", "--quiet", "--no-index", "--", relative],
                cwd=ROOT,
                capture_output=True,
                check=False,
            )
            return result.returncode == 0
        except (OSError, ValueError):
            return False

    for path in ROOT.rglob("*"):
        if ".git" in path.parts:
            continue
        if path.is_dir() and path.name in CACHE_DIR_NAMES:
            if not is_gitignored(path):
                errors.append(f"Prohibited cache directory found: {path.relative_to(ROOT)}")
        elif path.is_file() and path.suffix.lower() == ".zip":
            errors.append(f"Prohibited ZIP archive found: {path.relative_to(ROOT)}")
    return errors


def validate_spatial_assets() -> list[str]:
    """Verify standalone spatial asset templates exist inside the skill directory."""
    errors: list[str] = []
    asset_roots = (
        SKILL_DIR / "assets" / "spatial",
        ROOT / ".bc" / "skills" / "bc-design" / "assets" / "spatial",
    )
    required_assets = ["school-codex.html", "spatial-showcase.html"]
    for assets_dir in asset_roots:
        for name in required_assets:
            target = assets_dir / name
            if not target.is_file():
                errors.append(f"Required spatial generator asset missing: {target}")
    return errors


def validate_third_party_notices() -> list[str]:
    """Verify the MIT notices for bundled upstream material travel with installs."""
    notices = SKILL_DIR / "THIRD_PARTY_NOTICES.md"
    if not notices.is_file():
        return [f"Third-party notices missing from skill directory: {notices.relative_to(ROOT)}"]
    text = notices.read_text(encoding="utf-8")
    required = ("Copyright (c) 2024 Next Level Builder", "Copyright (c) 2026 Meng To")
    return [f"Third-party notices missing '{notice}'" for notice in required if notice not in text]


def validate_brand_and_clean_paths() -> list[str]:
    """Verify no banned legacy brand strings or local machine paths exist in public skill files."""
    errors: list[str] = []
    banned_tokens = ("claude design", "anthropic design", "superpowers")
    check_dirs = [ROOT / ".agents" / "skills", ROOT / "examples"]

    for base in check_dirs:
        for file in base.rglob("*"):
            if not file.is_file() or file.suffix in EXCLUDED_SUFFIXES or any(p in EXCLUDED_PARTS for p in file.parts):
                continue
            if file.name.endswith(".csv") or file.name.endswith(".png") or file.name.endswith(".jpg"):
                continue
            try:
                content = file.read_text(encoding="utf-8", errors="ignore").lower()
            except Exception:
                continue
            for banned in banned_tokens:
                if banned in content:
                    errors.append(f"Banned brand token '{banned}' found in {file.relative_to(ROOT)}")
            if "c:\\users\\ahmad" in content or "c:/users/ahmad" in content:
                errors.append(f"Local machine path found in {file.relative_to(ROOT)}")

    return errors


def validate_all(fix: bool = False) -> list[str]:
    """Run full suite of repository integrity checks."""
    errors: list[str] = []
    report = build_report()
    if report["errors"]:
        errors.extend(report["errors"])
    if report["totals"].get("unclassified", 0):
        errors.append(f"Unclassified catalog entries detected: {report['totals']['unclassified']}")

    errors.extend(validate_manifest(fix=fix))
    errors.extend(validate_mirror_parity())
    errors.extend(validate_prohibited_artifacts())
    errors.extend(validate_spatial_assets())
    errors.extend(validate_brand_and_clean_paths())
    errors.extend(sync_adapters.check())
    errors.extend(validate_third_party_notices())
    return errors


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Validate BC Design repository and skill integrity")
    parser.add_argument("--fix-manifest", action="store_true", help="Auto-update skill.json catalog counts from normalized sources")
    args = parser.parse_args(argv)

    errors = validate_all(fix=args.fix_manifest)
    if errors:
        print(f"VALIDATION FAILED ({len(errors)} error(s)):")
        for err in errors:
            print(f"  - {err}")
        return 1

    metrics = computed_catalog_metrics()
    print("VALIDATION SUCCESS: Repository, mirror parity, catalogs, and assets are in full compliance.")
    print(f"Catalogs: {metrics}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
