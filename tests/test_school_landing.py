import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "examples" / "school-cakrawala"
CLI = ROOT / ".agents" / "skills" / "bc-design" / "scripts" / "bc_design.py"


class SchoolLandingTests(unittest.TestCase):
    def test_demo_assets_and_landmarks_exist(self):
        html = (PAGE / "index.html").read_text(encoding="utf-8")
        self.assertTrue((PAGE / "styles.css").exists())
        self.assertTrue((PAGE / "script.js").exists())
        for marker in ('lang="id"', 'class="skip-link"', '<main', '<nav', 'id="kunjungan"', 'data-visit-form'):
            self.assertIn(marker, html)

    def test_demo_uses_newsreader_typography_and_accessible_states(self):
        css = (PAGE / "styles.css").read_text(encoding="utf-8")
        js = (PAGE / "script.js").read_text(encoding="utf-8")
        html = (PAGE / "index.html").read_text(encoding="utf-8")
        self.assertIn('--serif: "Newsreader", Georgia, serif;', css)
        self.assertNotIn("BCSerif", css)
        self.assertNotIn('@font-face', css)
        for forbidden in (" · ", "↗", "↘", "⌖", "01 —", "02 —", "03 —"):
            self.assertNotIn(forbidden, html)
        self.assertIn("outline: 2px solid", css)
        self.assertIn("z-index: 30", css)
        self.assertIn(':focus-visible', css)
        self.assertIn('@media (prefers-reduced-motion: reduce)', css)
        self.assertIn('reportValidity()', js)
        self.assertIn('aria-live="polite"', (PAGE / "index.html").read_text(encoding="utf-8"))

    def test_demo_has_no_generic_card_or_gradient_shortcuts(self):
        combined = "\n".join(path.read_text(encoding="utf-8") for path in PAGE.glob("*"))
        self.assertNotIn("rounded-xl p-6", combined)
        self.assertNotIn("linear-gradient", combined)
        self.assertNotIn("background: #FFFFFF", combined)

    def test_demo_passes_bc_design_source_audit(self):
        completed = subprocess.run(
            [sys.executable, str(CLI), "--audit", str(PAGE)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("AUDIT PASS", completed.stdout)


if __name__ == "__main__":
    unittest.main()
