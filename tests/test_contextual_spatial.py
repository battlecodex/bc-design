import csv
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / ".agents" / "skills" / "bc-design" / "data" / "spatial-effects.csv"
CLI = ROOT / ".agents" / "skills" / "bc-design" / "scripts" / "bc_design.py"
SCHOOL_HTML = ROOT / "examples" / "school-spatial.html"

REQUIRED_SECTORS = {
    "Education",
    "Enterprise ERP",
    "HRM",
    "Fintech / Crypto",
    "Healthcare",
    "Pet Services",
    "SaaS",
    "AI / Chatbot",
    "E-commerce",
    "Real Estate",
    "Creative Agency",
    "Gaming",
    "Food & Restaurant",
    "Fitness",
    "Travel",
    "NFT / Web3",
    "Beauty / Spa",
    "Developer Tools",
    "Entertainment",
    "Legal",
    "Events"
}


class ContextualSpatialTests(unittest.TestCase):
    def test_catalog_contains_all_sectors(self):
        self.assertTrue(CSV_PATH.exists(), f"Catalog missing: {CSV_PATH}")
        with open(CSV_PATH, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            found_sectors = {row["Sector"].strip() for row in reader if "Sector" in row}

        missing = REQUIRED_SECTORS - found_sectors
        self.assertEqual(missing, set(), f"Missing industry sectors in spatial catalog: {missing}")

    def test_catalog_has_forbidden_gimmicks_for_all_sectors(self):
        with open(CSV_PATH, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                sector = row.get("Sector", "").strip()
                if sector in REQUIRED_SECTORS:
                    gimmick = row.get("Forbidden Gimmicks", "").strip()
                    self.assertTrue(len(gimmick) > 5, f"Sector '{sector}' must define forbidden gimmicks.")

    def test_spatial_cli_search_by_sector(self):
        queries = ["erp enterprise", "hrm talent", "veterinary pet", "legal compliance", "education codex"]
        for q in queries:
            with self.subTest(query=q):
                completed = subprocess.run(
                    [sys.executable, str(CLI), q, "--domain", "spatial"],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
                self.assertIn("Search Domain: SPATIAL", completed.stdout)
                self.assertIn("Found:", completed.stdout)

    def test_spatial_list_only_advertises_generatable_templates(self):
        expected = {
            "school-spatial",
            "erp-spatial",
            "ribbon-field",
            "predictive-arc",
            "spatial-scrollytelling",
        }
        listed = subprocess.run(
            [sys.executable, str(CLI), "--spatial", "list"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(listed.returncode, 0, listed.stdout + listed.stderr)
        advertised = set(re.findall(r"^.*?\b([a-z0-9-]+) \([^\r\n]*\) \[", listed.stdout, re.MULTILINE))
        self.assertEqual(advertised, expected)

        with tempfile.TemporaryDirectory() as output_dir:
            for preset in advertised:
                with self.subTest(preset=preset):
                    generated = subprocess.run(
                        [sys.executable, str(CLI), "--spatial", preset, "--output-dir", output_dir],
                        cwd=ROOT,
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    self.assertEqual(generated.returncode, 0, generated.stdout + generated.stderr)

    def test_school_spatial_uses_open_codex_not_astronomy(self):
        self.assertTrue(SCHOOL_HTML.exists())
        html = SCHOOL_HTML.read_text(encoding="utf-8")
        self.assertIn("Interactive 3D Open Codex", html)
        self.assertIn("createFolioTexture", html)
        self.assertIn("LIBER I", html)
        self.assertIn("PAGINA XLII", html)
        # Should not use generic astronomy planet / observatory gimmick
        self.assertNotIn("The Quadrivium Observatory", html)

    def test_spatial_aliases_resolve_correctly(self):
        sys.path.insert(0, str(ROOT / ".agents" / "skills" / "bc-design" / "scripts"))
        from spatial import SPATIAL_PRESET_ALIASES, generate_spatial_component

        aliases = ["school", "codex", "erp", "ribbon", "arc", "showcase"]
        for alias in aliases:
            with self.subTest(alias=alias):
                self.assertIn(alias, SPATIAL_PRESET_ALIASES)
                code = generate_spatial_component(alias)
                self.assertTrue(len(code) > 100)

    def test_invalid_preset_error_lists_only_runnable_generators(self):
        sys.path.insert(0, str(ROOT / ".agents" / "skills" / "bc-design" / "scripts"))
        from spatial import SPATIAL_GENERATOR_PRESETS, generate_spatial_component

        with self.assertRaises(ValueError) as ctx:
            generate_spatial_component("unsupported-preset-xyz")

        error_msg = str(ctx.exception)
        self.assertIn("Available runnable generators:", error_msg)
        for gen in SPATIAL_GENERATOR_PRESETS:
            self.assertIn(gen, error_msg)

    def test_standalone_generator_isolated_from_repo_examples(self):
        import shutil
        sys.path.insert(0, str(ROOT / ".agents" / "skills" / "bc-design" / "scripts"))

        with tempfile.TemporaryDirectory() as tempdir:
            temp_skill = Path(tempdir) / "bc-design"
            # Copy ONLY the skill folder (no examples/ or repo root)
            shutil.copytree(ROOT / ".agents" / "skills" / "bc-design", temp_skill)

            # Ensure examples/ does not exist in the isolated tree
            self.assertFalse((Path(tempdir) / "examples").exists())

            # Run python command inside isolated skill
            cli_path = temp_skill / "scripts" / "bc_design.py"
            result = subprocess.run(
                [sys.executable, str(cli_path), "--spatial", "school-spatial"],
                cwd=tempdir,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            generated_file = Path(tempdir) / "bc-school-spatial.html"
            self.assertTrue(generated_file.is_file())
            content = generated_file.read_text(encoding="utf-8")
            self.assertIn("<!DOCTYPE html>", content)
            self.assertIn("Veritas Academy", content)


if __name__ == "__main__":
    unittest.main()
