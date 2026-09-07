import csv
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / ".agents" / "skills"
MIRROR = ROOT / ".bc" / "skills"
CLI = CANONICAL / "bc-design" / "scripts" / "bc_design.py"
SKILLS = (
    "bc-design",
    "bc-brand",
    "bc-design-system",
    "bc-ui-styling",
    "bc-design-audit",
    "bc-motion",
)


class ProductionReadinessTests(unittest.TestCase):
    def test_packager_derives_catalog_metrics_from_normalized_report(self):
        from scripts import package as packager

        with tempfile.TemporaryDirectory() as tempdir:
            manifest_path = Path(tempdir) / "skill.json"
            manifest_path.write_text(json.dumps({"catalogs": {"styles": 0}}), encoding="utf-8")
            updated = packager.sync_manifest_catalogs(manifest_path)
        self.assertEqual(updated["catalogs"]["styles"], 88)
        self.assertEqual(updated["catalogs"]["stackCatalogs"], 22)

    def test_release_archive_excludes_local_and_cache_artifacts(self):
        with tempfile.TemporaryDirectory() as tempdir:
            archive = Path(tempdir) / "bc-design.zip"
            subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "package.py"), "--output", str(archive)],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            with zipfile.ZipFile(archive) as bundle:
                names = bundle.namelist()
            self.assertIn("bc-design/skill.json", names)
            self.assertIn("bc-design/.agents/skills/bc-design/SKILL.md", names)
            self.assertFalse(any("__pycache__" in name or name.endswith(".pyc") for name in names))
            self.assertFalse(any(name.startswith("bc-design/design-system/") for name in names))

    def test_every_skill_has_valid_codex_ui_metadata(self):
        for name in SKILLS:
            metadata_path = CANONICAL / name / "agents" / "openai.yaml"
            self.assertTrue(metadata_path.is_file(), name)
            metadata = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))
            interface = metadata.get("interface", {})
            self.assertTrue(interface.get("display_name"), name)
            self.assertTrue(interface.get("short_description"), name)
            self.assertIn(f"${name}", interface.get("default_prompt", ""), name)

    def test_product_manifest_matches_shipped_family(self):
        manifest_path = ROOT / "skill.json"
        self.assertTrue(manifest_path.is_file())
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual("bc-design", manifest["name"])
        self.assertRegex(manifest["version"], r"^\d+\.\d+\.\d+$")
        self.assertEqual(list(SKILLS), manifest["skills"])
        self.assertEqual("MIT", manifest["license"])

    def test_readme_catalog_counts_match_bundled_data(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        expectations = {
            "styles.csv": "88",
            "colors.csv": "192",
            "typography.csv": "74",
            "charts.csv": "25",
            "ux-guidelines.csv": "119",
        }
        data = CANONICAL / "bc-design" / "data"
        for filename, advertised in expectations.items():
            with (data / filename).open(encoding="utf-8-sig", newline="") as handle:
                actual = sum(1 for _ in csv.reader(handle)) - 1
            self.assertEqual(int(advertised), actual)
            self.assertIn(advertised, readme, filename)
        stack_count = len(list((data / "stacks").glob("*.csv")))
        self.assertEqual(22, stack_count)
        self.assertIn("22", readme)

    def test_education_direction_uses_neutral_base_with_restrained_accents(self):
        result = subprocess.run(
            [sys.executable, str(CLI), "independent secondary school", "--design-system"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True,
        )
        output = result.stdout.lower()
        self.assertIn("newsreader", output)
        self.assertIn("inter", output)
        self.assertIn("neutral", output)
        self.assertNotIn("education teal", output)
        self.assertNotIn("quiet learning ground", output)

    def test_complete_skill_family_is_identical_in_bc_mirror(self):
        for name in SKILLS:
            left_root = CANONICAL / name
            right_root = MIRROR / name
            left = {
                path.relative_to(left_root): path.read_bytes()
                for path in left_root.rglob("*")
                if path.is_file() and path.suffix != ".pyc"
            }
            right = {
                path.relative_to(right_root): path.read_bytes()
                for path in right_root.rglob("*")
                if path.is_file() and path.suffix != ".pyc"
            }
            self.assertEqual(left, right, name)


if __name__ == "__main__":
    unittest.main()
