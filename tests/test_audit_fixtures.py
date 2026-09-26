"""Each fixture was misjudged by an earlier audit; these pin the corrected result."""

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "audit"
sys.path.insert(0, str(ROOT / ".agents" / "skills" / "bc-design" / "scripts"))

import audit  # noqa: E402
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
    # One finding per offending line, overshooting curves, arbitrary black overlays, and arrow glyphs.
    "per-line-findings.tsx": {"button-focus-ring-missing", "gsap-reduced-motion", "motion-duration-budget", "motion-easing-token"},
    "overshoot-bezier.css": {"motion-easing-token"},
    "overshoot-bezier.tsx": {"motion-easing-token"},
    "black-arbitrary-overlay.tsx": {"pure-black-overlay"},
    "glyph-arrows.tsx": {"unicode-glyph-copy"},
    "regression-all.tsx": {"em-dash-copy", "motion-duration-budget", "motion-easing-token", "pure-black-overlay", "unicode-glyph-copy"},
}

# Exact (rule, line) pairs: a per-file dedupe or a loosened pattern fails these loudly.
EXPECTED_LINES = {
    "per-line-findings.tsx": {
        ("gsap-reduced-motion", 3),
        ("motion-duration-budget", 3),
        ("motion-easing-token", 3),
        ("motion-duration-budget", 4),
        ("button-focus-ring-missing", 4),
    },
    "overshoot-bezier.css": {("motion-easing-token", 2)},
    "overshoot-bezier.tsx": {("motion-easing-token", 4)},
    "black-arbitrary-overlay.tsx": {("pure-black-overlay", line) for line in (4, 5, 6, 7, 8)},
    "glyph-arrows.tsx": {("unicode-glyph-copy", 6), ("unicode-glyph-copy", 7)},
    "regression-all.tsx": {
        ("motion-duration-budget", 10),
        ("motion-easing-token", 10),
        ("em-dash-copy", 14),
        ("motion-duration-budget", 15),
        ("motion-easing-token", 16),
        ("pure-black-overlay", 18),
        ("pure-black-overlay", 19),
        ("unicode-glyph-copy", 20),
    },
}


class AuditFixtureTests(unittest.TestCase):
    def test_every_fixture_is_listed(self):
        self.assertEqual(sorted(path.name for path in FIXTURES.iterdir()), sorted(EXPECTED))

    def test_fixtures_report_exactly_the_expected_rules(self):
        for name, expected in EXPECTED.items():
            with self.subTest(fixture=name):
                rules = {rule_id for rule_id, _, _ in bc_design.audit_target(FIXTURES / name)}
                self.assertEqual(rules, expected)

    def test_fixtures_report_exactly_the_expected_lines(self):
        for name, expected in EXPECTED_LINES.items():
            with self.subTest(fixture=name):
                findings = audit.build_audit_findings(FIXTURES / name)
                pairs = [(finding["rule_id"], finding["line"]) for finding in findings]
                self.assertEqual(len(pairs), len(set(pairs)), "a (rule, line) pair was reported twice")
                self.assertEqual(set(pairs), expected)

    def test_glyph_findings_name_every_glyph_on_the_line(self):
        findings = audit.build_audit_findings(FIXTURES / "glyph-arrows.tsx")
        messages = {finding["line"]: finding["message"] for finding in findings}
        self.assertIn("'✓', '→', '★'", messages[6])
        self.assertIn("'↗'", messages[7])

    def test_calm_curves_pass_and_overshooting_curves_fail(self):
        self.assertTrue(bc_design._easing_value_ok("transform 200ms cubic-bezier(0.16, 1, 0.3, 1)"))
        self.assertFalse(bc_design._easing_value_ok("all .2s cubic-bezier(.68,-.55,.27,1.55)"))
        self.assertTrue(bc_design._overshoots("cubic-bezier(0.68,-0.6,0.32,1.6)"))
        self.assertFalse(bc_design._overshoots("cubic-bezier(0.4_0_0.2_1)"))

    def test_findings_are_capped_per_rule_and_file(self):
        import tempfile

        rows = "\n".join(f'    <div className="duration-700">Row {index}</div>' for index in range(25))
        with tempfile.TemporaryDirectory() as tempdir:
            target = Path(tempdir) / "rows.tsx"
            target.write_text(f"export const Rows = () => (\n  <>\n{rows}\n  </>\n);\n", encoding="utf-8")
            findings = audit.build_audit_findings(target)
        durations = [finding for finding in findings if finding["rule_id"] == "motion-duration-budget"]
        self.assertEqual(len(durations), audit.MAX_FINDINGS_PER_RULE_AND_FILE)
        self.assertEqual([finding["line"] for finding in durations], list(range(3, 23)))
        self.assertTrue(durations[-1]["message"].endswith("(+5 more in this file)"))
        self.assertNotIn("more in this file", durations[0]["message"])

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
