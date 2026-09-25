import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / ".agents" / "skills"
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
    def test_validator_derives_catalog_metrics_including_spatial(self):
        from scripts import validate as validator

        metrics = validator.computed_catalog_metrics()
        self.assertEqual(metrics["styles"], 88)
        self.assertEqual(metrics["stackCatalogs"], 22)
        self.assertEqual(metrics["spatialEffects"], 31)
        self.assertEqual(metrics["spatialGenerators"], 5)

    def test_no_binary_archives_or_untracked_zip_files_in_repo(self):
        from scripts import validate as validator

        errors = validator.validate_prohibited_artifacts()
        self.assertEqual(errors, [])

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

    def test_manifest_spatial_contract_matches_runtime(self):
        from scripts import validate as validator
        from spatial import SPATIAL_GENERATOR_PRESETS, SPATIAL_PRESET_ALIASES

        manifest = json.loads((ROOT / "skill.json").read_text(encoding="utf-8"))
        spatial = manifest["spatial"]
        self.assertEqual(list(SPATIAL_GENERATOR_PRESETS), spatial["generators"])
        self.assertEqual(SPATIAL_PRESET_ALIASES, spatial["aliases"])
        self.assertEqual(len(SPATIAL_GENERATOR_PRESETS), manifest["catalogs"]["spatialGenerators"])
        self.assertEqual(validator.computed_catalog_metrics()["spatialEffects"], spatial["effectsCount"])

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



    def test_validator_detects_nested_zip_artifacts(self):
        from scripts import validate as validator

        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            (root / "examples" / "nested").mkdir(parents=True)
            (root / "examples" / "nested" / "backup.zip").write_bytes(b"not a release")
            original_root = validator.ROOT
            try:
                validator.ROOT = root
                self.assertTrue(validator.validate_prohibited_artifacts())
            finally:
                validator.ROOT = original_root


if __name__ == "__main__":
    unittest.main()
