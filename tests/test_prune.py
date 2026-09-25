import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".agents" / "skills" / "bc-design" / "scripts" / "prune.py"
SPEC = importlib.util.spec_from_file_location("prune", SCRIPT)
prune = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(prune)


def write(root, relative, text=""):
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def fixture(root):
    write(root, "package.json", json.dumps({"dependencies": {"react": "19.0.0", "gsap": "3.15.0", "framer-motion": "11.0.0", "@fontsource/inter": "5.0.0"}}, indent=2))
    write(root, "src/app.css", "\n".join([
        ":root {",
        "  --text-ink: #141413;",
        "  --bg-canvas: #FAF9F5;",
        "  --unused-gap: 12px;",
        "}",
        ".card { color: var(--text-ink); }",
        ".legacy-banner { color: #141413; }",
        ".btn-primary { background: #FAF8F5; }",
        ".btn-ghost { background: #FAF7F4; }",
        "h1 { font-family: \"Newsreader\", serif; }",
    ]))
    write(root, "index.html", '<link href="https://fonts.googleapis.com/css2?family=Newsreader:opsz@6..72&family=Playfair+Display&display=swap" rel="stylesheet">\n<div class="card"><img src="/img/hero.png" alt="Hero"></div>\n')
    write(root, "src/app.js", 'import gsap from "gsap";\nconst variant = "primary";\nel.className = `btn-${variant}`;\n')
    for asset in ("public/img/hero.png", "public/img/old-logo.svg", "public/favicon.ico"):
        write(root, asset)


class PruneTests(unittest.TestCase):
    def analyze(self, **kwargs):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            fixture(root)
            return {(f["kind"], f["subject"]): f for f in prune.analyze(root, **kwargs)}

    def test_finds_each_kind_of_unused_design_code(self):
        found = self.analyze()
        self.assertIn(("unused-token", "--unused-gap"), found)
        self.assertIn(("unused-package", "framer-motion"), found)
        self.assertIn(("unused-font", "Playfair Display"), found)
        self.assertIn(("unused-font", "Inter"), found)
        self.assertIn(("unused-asset", "public/img/old-logo.svg"), found)
        self.assertIn(("unused-class", ".legacy-banner"), found)
        self.assertIn(("hardcoded-token-color", "#141413"), found)

    def test_does_not_flag_what_is_used(self):
        found = self.analyze()
        subjects = {subject for _, subject in found}
        for used in ("--text-ink", "gsap", "Newsreader", "public/img/hero.png", ".card"):
            self.assertNotIn(used, subjects)

    def test_skips_conventional_assets(self):
        self.assertNotIn(("unused-asset", "public/favicon.ico"), self.analyze())

    def test_dynamic_class_names_lower_confidence(self):
        found = self.analyze()
        self.assertEqual(found[("unused-class", ".btn-ghost")]["confidence"], "low")
        self.assertEqual(found[("unused-class", ".legacy-banner")]["confidence"], "medium")

    def test_token_suggestion_matches_the_property_role(self):
        finding = self.analyze()[("hardcoded-token-color", "#141413")]
        self.assertEqual(finding["confidence"], "high")
        self.assertIn("var(--text-ink)", finding["action"])

    def test_groups_near_duplicate_raw_colors(self):
        finding = next(f for (kind, _), f in self.analyze().items() if kind == "near-duplicate-color")
        self.assertIn("#FAF8F5", finding["subject"])
        self.assertIn("#FAF7F4", finding["subject"])

    def test_keep_treats_a_file_as_public_api(self):
        found = self.analyze(keep=("src/app.css",))
        self.assertNotIn(("unused-token", "--unused-gap"), found)
        self.assertNotIn(("unused-class", ".legacy-banner"), found)

    def test_findings_are_numbered_by_confidence(self):
        findings = sorted(self.analyze().values(), key=lambda f: f["number"])
        order = [prune.CONFIDENCE_ORDER[f["confidence"]] for f in findings]
        self.assertEqual(order, sorted(order))
        self.assertEqual([f["number"] for f in findings], list(range(1, len(findings) + 1)))

    def test_cli_reports_without_changing_files(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            fixture(root)
            before = {p: p.read_bytes() for p in root.rglob("*") if p.is_file()}
            completed = subprocess.run(
                [sys.executable, str(SCRIPT), "--workspace", tempdir],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            after = {p: p.read_bytes() for p in root.rglob("*") if p.is_file() and ".bc-design" not in p.parts}
            report = json.loads((root / ".bc-design" / "prune-report.json").read_text(encoding="utf-8"))
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("Nothing was changed", completed.stdout)
        self.assertEqual(before, after)
        self.assertTrue(report["findings"])


if __name__ == "__main__":
    unittest.main()
