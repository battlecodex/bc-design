"""Each fixture was misjudged by an earlier audit; these pin the corrected result."""

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "audit"
sys.path.insert(0, str(ROOT / ".agents" / "skills" / "bc-design" / "scripts"))

import bc_design  # noqa: E402

EXPECTED = {
    # Comments are not copy; an em dash in JSX text or a string label still is.
    "em-dash-in-comments.tsx": set(),
    "em-dash-in-copy.tsx": {"em-dash-copy"},
    # Tailwind and GSAP motion measured against the tokens.
    "tailwind-motion-off-token.tsx": {"motion-duration-budget", "motion-easing-token"},
    "tailwind-motion-on-token.tsx": set(),
    "gsap-off-token.js": {"motion-duration-budget", "motion-easing-token"},
    "gsap-window-matchmedia.js": set(),
    # House rules from SKILL.md: glyphs, tracked capitals, focus rings, and overlays.
    "house-rule-violations.tsx": {"unicode-glyph-copy", "tracked-uppercase-label", "button-focus-ring-missing", "pure-black-overlay"},
    "house-rule-clean.tsx": set(),
    "overlay-and-caps.css": {"pure-black-overlay", "tracked-uppercase-label"},
}


class AuditFixtureTests(unittest.TestCase):
    def test_every_fixture_is_listed(self):
        self.assertEqual(sorted(path.name for path in FIXTURES.iterdir()), sorted(EXPECTED))

    def test_fixtures_report_exactly_the_expected_rules(self):
        for name, expected in EXPECTED.items():
            with self.subTest(fixture=name):
                rules = {rule_id for rule_id, _, _ in bc_design.audit_target(FIXTURES / name)}
                self.assertEqual(rules, expected)

    def test_a_global_focus_visible_rule_covers_component_buttons(self):
        button = '<button className="rounded-md px-4 py-2">Save plan</button>'
        self.assertIn("button-focus-ring-missing", {v[0] for v in bc_design.find_audit_violations(button, "a.tsx")})
        covered = bc_design.find_audit_violations(button, "a.tsx", {"global_focus_visible": True})
        self.assertNotIn("button-focus-ring-missing", {v[0] for v in covered})

    def test_scrubbed_timelines_are_not_timed(self):
        scrub = "gsap.timeline({ scrollTrigger: { scrub: true } }).to('.a', { y: 10, duration: 0.08, ease: 'none' });"
        self.assertNotIn("motion-duration-budget", {v[0] for v in bc_design.find_audit_violations(scrub, "a.js")})


if __name__ == "__main__":
    unittest.main()
