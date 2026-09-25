import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".agents" / "skills" / "bc-design"
POLICY = SKILL / "data" / "bc-alignment-policy.json"
sys.path.insert(0, str(SKILL / "scripts"))


class CatalogAlignmentTests(unittest.TestCase):
    def test_policy_schema(self):
        self.assertTrue(POLICY.is_file())
        policy = json.loads(POLICY.read_text(encoding="utf-8"))
        self.assertEqual(1, policy["schemaVersion"])
        self.assertEqual(
            ["core", "compatible", "conditional", "excluded"],
            policy["statuses"],
        )
        self.assertGreaterEqual(len(policy["coreTraits"]), 5)
        self.assertGreaterEqual(len(policy["conflictTraits"]), 5)
        self.assertTrue(policy["explicitRequestSignals"])
        self.assertIn("contrast", policy["qualityGates"])

    def test_alignment_module_classifies_representative_entries(self):
        from alignment import classify_entry

        self.assertEqual("core", classify_entry("style", {"Style Category": "Editorial Minimalism", "Keywords": "serif neutral spacious"}).status)
        self.assertEqual("compatible", classify_entry("style", {"Style Category": "Utility Dashboard", "Keywords": "structured practical"}).status)
        self.assertEqual("conditional", classify_entry("style", {"Style Category": "Claymorphism", "Keywords": "3d bubbly spring"}).status)
        self.assertEqual("excluded", classify_entry("style", {"Style Category": "Neon Glassmorphism", "Keywords": "neon gradient low contrast"}).status)

    def test_chart_search_reads_secondary_options(self):
        from core import search_domain

        result = search_domain("chart", "area chart")
        self.assertTrue(result["results"])

    def test_explicit_request_unlocks_conditional_but_not_excluded_quality(self):
        from alignment import classify_entry, explicit_direction_requested

        row = {"Style Category": "Claymorphism", "Keywords": "3d bubbly spring"}
        self.assertFalse(explicit_direction_requested("build an editorial school site", row))
        self.assertTrue(explicit_direction_requested("use claymorphism for a playful mobile game", row))
        self.assertEqual("conditional", classify_entry("style", row, explicit=True).status)
        bad = {"Style Category": "Neon Glassmorphism", "Keywords": "neon gradient low contrast"}
        self.assertEqual("excluded", classify_entry("style", bad, explicit=True).status)

    def test_normalize_catalog_check_reports_complete_status_coverage(self):
        command = [
            sys.executable,
            str(SKILL / "scripts" / "normalize_catalog.py"),
            "--check",
        ]
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("unclassified=0", result.stdout)

    def test_automatic_search_excludes_conditional_and_excluded_rows(self):
        from core import search_domain

        result = search_domain("style", "neon glassmorphism", max_results=20)
        self.assertEqual([], result["results"])

    def test_explicit_search_can_return_conditional_style_with_reason(self):
        from core import search_domain

        result = search_domain("style", "use claymorphism", max_results=20, selection_mode="explicit")
        self.assertTrue(result["results"])
        self.assertTrue(any(item["alignment"]["status"] == "conditional" for item in result["results"]))

    def test_cli_explicit_style_request_surfaces_conditional_entry(self):
        result = subprocess.run(
            [sys.executable, str(SKILL / "scripts" / "bc_design.py"), "use claymorphism", "--domain", "style"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("conditional", result.stdout.lower())

    def test_automatic_design_generator_does_not_select_conditional_visual_styles(self):
        from bc_design import generate_design_system

        for query in ("health clinic", "general interface"):
            card, _ = generate_design_system(query)
            self.assertNotIn("Warm Editorial Glass", card)
            self.assertNotIn("BC Design Bento Grid", card)

    def test_prompt_matrix_preserves_alignment_invariants(self):
        matrix = json.loads((ROOT / "tests" / "fixtures" / "prompts" / "catalog-alignment.json").read_text(encoding="utf-8"))
        for case in matrix:
            if case.get("mode") == "audit":
                continue
            args = [sys.executable, str(SKILL / "scripts" / "bc_design.py"), case["query"]]
            if case.get("domain"):
                args.extend(["--domain", case["domain"]])
            result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(0, result.returncode, case["name"])
            for expected in case.get("must_include", []):
                self.assertIn(expected.lower(), result.stdout.lower(), case["name"])
            for forbidden in case.get("must_exclude", []):
                self.assertNotIn(forbidden.lower(), result.stdout.lower(), case["name"])


if __name__ == "__main__":
    unittest.main()
