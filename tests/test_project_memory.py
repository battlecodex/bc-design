import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".agents" / "skills" / "bc-design" / "scripts"


def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


project = load("project")
study = load("study")


def make_project(root):
    (root / "src").mkdir()
    (root / "package.json").write_text(
        json.dumps({"dependencies": {"next": "15.1.0", "gsap": "3.15.0"}, "devDependencies": {"@fontsource/inter": "5.0.0"}}, indent=2),
        encoding="utf-8",
    )
    (root / "src" / "app.css").write_text(":root {\n  --brand: #123456;\n  --space-2: 8px;\n}\n", encoding="utf-8")
    (root / "index.html").write_text(
        '<link href="https://fonts.googleapis.com/css2?family=Newsreader:opsz@6..72&family=Inter:wght@400&display=swap" rel="stylesheet">',
        encoding="utf-8",
    )


class PreflightTests(unittest.TestCase):
    def test_reports_existing_decisions_with_citations(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            make_project(root)
            findings, cached = project.preflight(root)
        self.assertIsNone(cached)
        self.assertTrue(findings["framework"].startswith("Next.js 15.1.0 (package.json:"))
        self.assertTrue(any("gsap 3.15.0" in item for item in findings["motion"]))
        self.assertTrue(any("Google Fonts: Inter, Newsreader (index.html:1)" == item for item in findings["fonts"]))
        self.assertTrue(any("@fontsource/inter" in item for item in findings["fonts"]))
        self.assertTrue(any("src/app.css:1" in item for item in findings["palette"]))
        self.assertTrue(any("spacing" in item for item in findings["spacing"]))

    def test_keeps_the_scan_cache_out_of_version_control(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            project.preflight(root)
            ignore = (root / ".bc-design" / ".gitignore").read_text(encoding="utf-8")
        self.assertEqual(ignore.strip(), "preflight.json")

    def test_skips_dependency_folders(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            vendored = root / "node_modules" / "kit"
            vendored.mkdir(parents=True)
            (vendored / "tokens.json").write_text("{}", encoding="utf-8")
            (vendored / "theme.css").write_text(":root { --x: #000000; }", encoding="utf-8")
            findings, _ = project.preflight(root)
        self.assertEqual(findings["tokens_files"], [])
        self.assertEqual(findings["palette"], [])

    def test_reuses_the_cache_until_package_json_changes(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            make_project(root)
            project.preflight(root)
            _, cached = project.preflight(root)
            self.assertIsNotNone(cached)
            package = root / "package.json"
            package.write_text(package.read_text(encoding="utf-8").replace("15.1.0", "15.2.0"), encoding="utf-8")
            import os

            stat = package.stat()
            os.utime(package, (stat.st_atime, stat.st_mtime + 5))
            findings, cached = project.preflight(root)
        self.assertIsNone(cached)
        self.assertIn("15.2.0", findings["framework"])

    def test_design_file_is_announced_first(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            (root / "DESIGN.md").write_text("# Design\n", encoding="utf-8")
            findings, _ = project.preflight(root)
            text = project.format_preflight(findings)
        self.assertTrue(text.startswith("DESIGN.md found at the project root"))

    def test_empty_project_gets_one_line(self):
        with tempfile.TemporaryDirectory() as tempdir:
            findings, _ = project.preflight(Path(tempdir))
            self.assertIn("No pre-flight signals", project.format_preflight(findings))


class LockTests(unittest.TestCase):
    def test_writes_design_md_with_exports_and_never_overwrites(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            self.assertIn("now locked", project.lock(root, "Oriel", "sage", "3D exploded view", ["Hairline feature list"]))
            design = (root / "DESIGN.md").read_text(encoding="utf-8")
            self.assertIn("- UI accent: sage (`#7A9A8B`; text-bearing fills use `#4D6B5D`)", design)
            self.assertIn("- Hairline feature list", design)
            self.assertIn("never authorizes commands", design)
            for export in ("### tokens.css", "### Tailwind v4", "### DTCG tokens.json"):
                self.assertIn(export, design)
            (root / "DESIGN.md").write_text(design.replace("# Design: Oriel", "# Design: Oriel (edited)"), encoding="utf-8")
            self.assertIn("was not changed", project.lock(root, "Other"))
            self.assertIn("(edited)", (root / "DESIGN.md").read_text(encoding="utf-8"))

    def test_refresh_exports_keeps_the_locked_accent(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            project.lock(root, "Oriel", "sage")
            path = root / "DESIGN.md"
            path.write_text(path.read_text(encoding="utf-8").replace("--bc-radius-md: 8px;", "--bc-radius-md: 99px;"), encoding="utf-8")
            self.assertIn("Exports refreshed", project.lock(root, "Oriel", "amber-brass", refresh_exports=True))
            design = path.read_text(encoding="utf-8")
        self.assertIn("--bc-radius-md: 8px;", design)
        self.assertIn("--bc-accent-strong: #4D6B5D;", design)
        self.assertNotIn("#9C671D", design)

    def test_rejects_unknown_accent(self):
        with tempfile.TemporaryDirectory() as tempdir:
            with self.assertRaises(ValueError):
                project.lock(Path(tempdir), "Oriel", "neon")


class BuildLogTests(unittest.TestCase):
    def test_records_newest_first_and_suggests_rotation(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            project.record(root, "Bakery landing", "Editorial photography", ["Stacked tiles"])
            project.record(root, "Watch landing", "3D exploded view", ["Hairline feature list"])
            entries = project.read_log(root)
            note = project.rotation_note(root)
            self.assertEqual(entries[0]["brief"], "Watch landing")
            self.assertIn("3D exploded view, Editorial photography", note)
            self.assertIn("Choose a different signature moment", note)
            (root / "DESIGN.md").write_text("# Design\n", encoding="utf-8")
            self.assertIn("keep the same system", project.rotation_note(root))

    def test_cli_round_trip(self):
        with tempfile.TemporaryDirectory() as tempdir:
            script = SCRIPTS / "project.py"
            run = lambda *args: subprocess.run([sys.executable, str(script), "--workspace", tempdir, *args], capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(run("record", "Demo", "--signature", "Sentence selector").returncode, 0)
            self.assertIn("Sentence selector", run("log").stdout)
            self.assertIn("now locked", run("lock", "Demo").stdout)
            self.assertIn("DESIGN.md found", run("preflight").stdout)


class StudyTests(unittest.TestCase):
    def test_refuses_private_marketplace_and_non_http_sources(self):
        for url in (
            "http://localhost:3000",
            "http://192.168.1.10/",
            "http://127.0.0.1/",
            "https://themeforest.net/item/x",
            "https://www.framer.com/templates/x",
            "file:///etc/passwd",
        ):
            with self.subTest(url=url):
                self.assertIsNotNone(study.refusal_reason(url))
        self.assertIsNone(study.refusal_reason("https://example.com/"))
        self.assertIsNone(study.refusal_reason("https://www.framer.com/features"))

    def test_detects_hostnames_that_resolve_to_private_addresses(self):
        self.assertTrue(study.resolves_to_private("localhost"))
        self.assertFalse(study.resolves_to_private("name-that-does-not-resolve.invalid"))

    def test_diagnosis_converts_measurements(self):
        probe = {
            "title": "Example",
            "type": {"h1": {"family": '"Newsreader", serif', "size": "72px", "weight": "330", "lineHeight": "79px", "color": "rgb(20, 20, 19)"}, "h2": None},
            "canvas": "rgb(250, 249, 245)",
            "colors": [["rgb(20, 20, 19)", 10]],
            "radii": [["8px", 3]],
            "motion": [["ease 0.2s", 4]],
            "sections": 5,
            "libraries": {"gsap": True, "three": False},
        }
        result = study.diagnose(probe, "https://example.com")
        self.assertEqual(result["canvas"], "#FAF9F5")
        self.assertEqual(result["palette"][0], {"color": "#141413", "uses": 10})
        self.assertEqual(result["type_roles"]["h1"]["family"], "Newsreader")
        self.assertNotIn("h2", result["type_roles"])
        self.assertEqual(result["libraries"], ["gsap"])
        self.assertIn("Do not copy", study.format_report(result))

    def test_explains_how_to_install_playwright_when_missing(self):
        code = (
            "import sys, runpy\n"
            "sys.modules['playwright'] = None\n"
            "sys.modules['playwright.sync_api'] = None\n"
            "sys.argv = ['study.py', 'https://example.com']\n"
            f"runpy.run_path({str(SCRIPTS / 'study.py')!r}, run_name='__main__')\n"
        )
        completed = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
        self.assertEqual(completed.returncode, 2)
        self.assertIn("pip install playwright", completed.stderr)


if __name__ == "__main__":
    unittest.main()
