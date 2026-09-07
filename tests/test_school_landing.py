import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "examples" / "school-spatial.html"
CLI = ROOT / ".agents" / "skills" / "bc-design" / "scripts" / "bc_design.py"


class SchoolLandingTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(PAGE.is_file(), f"Target school showcase does not exist at {PAGE}")
        self.html = PAGE.read_text(encoding="utf-8")

    def test_demo_assets_and_landmarks_exist(self):
        for marker in ('class="skip-link"', '<main', '<nav', 'id="curriculum"', 'id="faculty"', 'id="admissions"'):
            self.assertIn(marker, self.html)

    def test_demo_uses_newsreader_typography_and_accessible_states(self):
        self.assertIn('Newsreader', self.html)
        self.assertIn('Inter', self.html)
        self.assertIn('JetBrains Mono', self.html)

        # Forbidden generic filler glyphs
        for forbidden in (" · ", "↗", "↘", "⌖", "01 —", "02 —", "03 —"):
            self.assertNotIn(forbidden, self.html)

        # Accessibility and focus states
        self.assertIn("outline: 2px solid", self.html)
        self.assertIn("z-index: 30", self.html)
        self.assertIn(':focus-visible', self.html)
        self.assertIn('prefers-reduced-motion', self.html)
        self.assertIn('aria-live="polite"', self.html)

    def test_demo_enforces_spatial_webgl_safety_and_zero_overlap(self):
        # Background canvas must not block clicks
        self.assertIn("pointer-events: none", self.html)

        # Device pixel ratio capped to protect mobile GPUs
        self.assertIn("Math.min(window.devicePixelRatio", self.html)

        # Hero content column restricted so 3D open codex does not overlap typography
        self.assertIn("max-width: min(560px, 45vw)", self.html)

        # Authentic open codex object instead of astronomy space planets
        self.assertIn("Open Codex", self.html)
        self.assertNotIn("galaxy", self.html.lower())
        self.assertNotIn("spaceship", self.html.lower())

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
