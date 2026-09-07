import csv
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".agents" / "skills" / "bc-design"
CLI = SKILL / "scripts" / "bc_design.py"


class StackCatalogTests(unittest.TestCase):
    def test_every_stack_catalog_is_reachable(self):
        stacks = sorted(path.stem for path in (SKILL / "data" / "stacks").glob("*.csv"))
        self.assertEqual(22, len(stacks))
        for stack in stacks:
            with self.subTest(stack=stack):
                result = subprocess.run([sys.executable, str(CLI), "--stack", stack], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertIn(stack, result.stdout.lower())
                self.assertIn("guidance", result.stdout.lower())

    def test_unknown_stack_has_actionable_error(self):
        result = subprocess.run([sys.executable, str(CLI), "--stack", "not-a-stack"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("available", result.stdout.lower())

    def test_documented_tailwind_alias_resolves_to_html_tailwind_catalog(self):
        result = subprocess.run([sys.executable, str(CLI), "--stack", "tailwind"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("stack guidance: tailwind", result.stdout.lower())
        self.assertIn("tailwind", result.stdout.lower())


if __name__ == "__main__":
    unittest.main()
