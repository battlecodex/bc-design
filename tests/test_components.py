import csv
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".agents" / "skills" / "bc-design"
SCRIPT = SKILL / "scripts" / "components.py"
THEME = SKILL / "assets" / "components" / "shadcn-bc-theme.css"
SPEC = importlib.util.spec_from_file_location("components", SCRIPT)
components = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(components)
CONTRAST_SPEC = importlib.util.spec_from_file_location("contrast", SKILL / "scripts" / "contrast.py")
contrast = importlib.util.module_from_spec(CONTRAST_SPEC)
CONTRAST_SPEC.loader.exec_module(contrast)


def shadcn_project(root):
    (root / "package.json").write_text(json.dumps({"dependencies": {"next": "15.1.0"}}), encoding="utf-8")
    (root / "components.json").write_text(json.dumps({"style": "new-york"}), encoding="utf-8")
    ui = root / "src" / "components" / "ui"
    ui.mkdir(parents=True)
    for name in ("button", "card", "dialog"):
        (ui / f"{name}.tsx").write_text("export {}", encoding="utf-8")
    (root / "src" / "sections").mkdir()
    (root / "src" / "sections" / "Hero.tsx").write_text("export {}", encoding="utf-8")


class CatalogTests(unittest.TestCase):
    def test_every_row_is_complete(self):
        with (SKILL / "data" / "component-sources.csv").open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertGreaterEqual(len(rows), 25)
        for row in rows:
            with self.subTest(component=row["component"]):
                self.assertTrue(row["house_fit"] and row["restyle"] and row["category"])
                self.assertTrue(row["shadcn_primitive"] or row["block_sources"] or row["effect_sources"])

    def test_aliases_point_at_catalogued_components(self):
        catalog = components.load_catalog()
        self.assertEqual({target for target in components.ALIASES.values()} - set(catalog), set())


class BrainstormTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, encoding="utf-8")

    def test_options_follow_what_the_project_has(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            shadcn_project(root)
            context = components.project_context(root)
            catalog = components.load_catalog()
            hero = components.brainstorm("hero", catalog["hero"], context)
            dialog = components.brainstorm("dialog", catalog["dialog"], context)
        self.assertEqual(hero["keep_and_restyle"], ["src/sections/Hero.tsx"])
        self.assertIn("shadcnblocks", hero["new_library_blocks"])
        self.assertIn("React Bits", hero["new_library_effects"])
        self.assertIn("installed: dialog", dialog["installed_base"])
        self.assertIn("npx shadcn@latest add sheet alert-dialog after approval", dialog["installed_base"])

    def test_without_a_component_library_shadcn_is_offered_with_approval(self):
        with tempfile.TemporaryDirectory() as tempdir:
            option = components.brainstorm("tabs", components.load_catalog()["tabs"], components.project_context(Path(tempdir)))
        self.assertIn("needs approval", option["installed_base"])

    def test_cli_resolves_aliases_and_never_installs(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            shadcn_project(root)
            before = sorted(p.relative_to(root).as_posix() for p in root.rglob("*"))
            completed = self.run_cli("modal", "charts", "--workspace", tempdir)
            after = sorted(p.relative_to(root).as_posix() for p in root.rglob("*") if ".bc-design" not in p.parts)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("dialog (primitive)", completed.stdout)
        self.assertIn("chart (data)", completed.stdout)
        self.assertIn("Install or paste nothing until the user approves", completed.stdout)
        self.assertEqual(before, after)

    def test_unknown_component_is_an_error(self):
        completed = self.run_cli("spaceship")
        self.assertEqual(completed.returncode, 2)
        self.assertIn("--list", completed.stderr)


class ShadcnThemeTests(unittest.TestCase):
    def variables(self, block):
        return dict(re.findall(r"(--[\w-]+):\s*(#[0-9A-Fa-f]{6})\s*;", block))

    def blocks(self):
        text = THEME.read_text(encoding="utf-8")
        light = re.search(r":root\s*\{(.*?)\n\}", text, re.DOTALL).group(1)
        dark = re.search(r"\.dark\s*\{(.*?)\n\}", text, re.DOTALL).group(1)
        return self.variables(light), self.variables(dark)

    def test_defines_every_core_shadcn_variable_in_both_themes(self):
        required = ("--background", "--foreground", "--card", "--primary", "--primary-foreground", "--muted", "--muted-foreground", "--destructive", "--ring", "--chart-1", "--sidebar")
        light, dark = self.blocks()
        for name in required:
            with self.subTest(name=name):
                self.assertIn(name, light)
                self.assertIn(name, dark)

    def test_text_pairs_meet_wcag_aa(self):
        pairs = (("--foreground", "--background"), ("--muted-foreground", "--muted"), ("--primary-foreground", "--primary"), ("--card-foreground", "--card"))
        for label, variables in zip(("light", "dark"), self.blocks()):
            for text, surface in pairs:
                with self.subTest(theme=label, pair=text):
                    self.assertGreaterEqual(contrast.compute_contrast(variables[text], variables[surface]), 4.5)

    def test_theme_passes_the_audit(self):
        completed = subprocess.run(
            [sys.executable, str(SKILL / "scripts" / "bc_design.py"), "--audit", str(THEME)], capture_output=True, text=True, encoding="utf-8"
        )
        self.assertEqual(completed.returncode, 0, completed.stdout)


if __name__ == "__main__":
    unittest.main()
