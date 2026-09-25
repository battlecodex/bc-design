import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / ".agents" / "skills" / "bc-design" / "scripts" / "bc_design.py"


class CraftAuditTests(unittest.TestCase):
    def rules(self, source, suffix=".html"):
        with tempfile.TemporaryDirectory() as tempdir:
            target = Path(tempdir) / f"fixture{suffix}"
            target.write_text(source, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(CLI), "--audit", str(target), "--json"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
        return {finding["rule_id"] for finding in json.loads(result.stdout)["findings"]}

    def test_flags_em_dash_in_visible_copy_only(self):
        self.assertIn("em-dash-copy", self.rules("<h1>Quiet tools — for loud teams</h1>"))
        self.assertNotIn("em-dash-copy", self.rules("<script>// setup — legacy</script><h1>Quiet tools</h1>"))
        self.assertNotIn("em-dash-copy", self.rules("/* heading — note */ h1 { color: #1F1E1B; }", suffix=".css"))

    def test_allows_a_dash_used_as_a_list_marker(self):
        self.assertNotIn("em-dash-copy", self.rules("<ul><li><span>\u2014</span> Marketing</li><li>\u2014 Sales</li></ul>"))

    def test_flags_white_text_on_the_mid_tone_accent(self):
        self.assertIn("accent-fill-white-text", self.rules(".btn { background: var(--bc-accent); color: #fff; }", suffix=".css"))
        self.assertIn("accent-fill-white-text", self.rules('<a style="color: white; background: #D97757">Go</a>'))
        self.assertNotIn("accent-fill-white-text", self.rules(".btn { background: var(--bc-accent-strong); color: #fff; }", suffix=".css"))
        self.assertNotIn("accent-fill-white-text", self.rules(".dot { background: var(--bc-accent); }", suffix=".css"))

    def test_reveal_token_is_allowed_but_long_literal_durations_are_not(self):
        self.assertNotIn(
            "motion-duration-budget",
            self.rules(".reveal { transition: opacity var(--bc-duration-reveal) var(--bc-ease); }\n@media (prefers-reduced-motion: reduce) { .reveal { transition: none; } }", suffix=".css"),
        )
        self.assertIn(
            "motion-duration-budget",
            self.rules(".reveal { transition: opacity 600ms var(--bc-ease); }\n@media (prefers-reduced-motion: reduce) { .reveal { transition: none; } }", suffix=".css"),
        )
        tokens = (CLI.parents[1] / "references" / "tokens.css").read_text(encoding="utf-8")
        self.assertIn("--bc-duration-reveal: 600ms;", tokens)

    def test_every_rule_reports_under_a_review_dimension(self):
        import importlib.util

        spec = importlib.util.spec_from_file_location("bc_audit", CLI.with_name("audit.py"))
        audit = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(audit)
        self.assertEqual((set(audit.SEVERITY) | set(audit.CATEGORY)) - set(audit.DIMENSION), set())
        self.assertTrue(set(audit.DIMENSION.values()) <= set(audit.DIMENSIONS))
        dimensions_doc = (CLI.parents[1] / "references" / "design-dimensions.md").read_text(encoding="utf-8")
        for dimension in audit.DIMENSIONS:
            self.assertIn(f"**{dimension}**", dimensions_doc)

    def test_json_summary_groups_findings_by_dimension(self):
        with tempfile.TemporaryDirectory() as tempdir:
            target = Path(tempdir) / "page.html"
            target.write_text('<p>Unlock seamless flow.</p><a href="#">Docs</a>', encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(CLI), "--audit", str(target), "--json"],
                cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
            )
        summary = json.loads(result.stdout)["summary"]
        self.assertEqual(summary["by_dimension"], {"Information architecture": 1, "UX writing": 1})

    def test_flags_marketing_buzzwords(self):
        self.assertIn("buzzword-copy", self.rules("<p>Unlock seamless collaboration.</p>"))
        self.assertNotIn("buzzword-copy", self.rules("<p>Share a draft and collect comments in one place.</p>"))

    def test_flags_unverified_claims(self):
        self.assertIn("unverified-claim", self.rules("<span>SOC 2 Type II certified</span>"))
        self.assertIn("unverified-claim", self.rules("<p>10x faster builds with 99.99% uptime</p>"))
        self.assertIn("unverified-claim", self.rules("<span>HIPAA Ready</span>"))
        self.assertNotIn("unverified-claim", self.rules("<p>Builds finish in about four minutes.</p>"))

    def test_flags_dead_navigation_links(self):
        self.assertIn("dead-navigation-link", self.rules('<nav><a href="#">Pricing</a></nav>'))
        self.assertNotIn("dead-navigation-link", self.rules('<nav><a href="#pricing">Pricing</a></nav>'))

    def test_flags_removed_outline_without_focus_replacement(self):
        self.assertIn("focus-outline-removed", self.rules("input { outline: none; }", suffix=".css"))
        self.assertNotIn(
            "focus-outline-removed",
            self.rules("input { outline: none; }\ninput:focus-visible { outline: 2px solid #B35637; }", suffix=".css"),
        )

    def test_flags_gsap_without_reduced_motion_branch(self):
        self.assertIn("gsap-reduced-motion", self.rules("gsap.to('.card', { y: 0, opacity: 1 });", suffix=".js"))
        guarded = (
            "const mm = gsap.matchMedia();\n"
            "mm.add('(prefers-reduced-motion: no-preference)', () => { gsap.to('.card', { y: 0, opacity: 1 }); });\n"
        )
        self.assertNotIn("gsap-reduced-motion", self.rules(guarded, suffix=".js"))

    def test_flags_gsap_layout_property_tweens(self):
        source = "gsap.matchMedia();\ngsap.to('.panel', { height: 320, duration: 0.3 });"
        self.assertIn("gsap-layout-property", self.rules(source, suffix=".js"))
        self.assertNotIn(
            "gsap-layout-property",
            self.rules("gsap.matchMedia();\ngsap.to('.panel', { y: 12, scale: 1.02 });", suffix=".js"),
        )

    def test_bundled_motion_and_spatial_assets_pass_the_audit(self):
        assets = ROOT / ".agents" / "skills" / "bc-design" / "assets"
        completed = subprocess.run(
            [sys.executable, str(CLI), "--audit", str(assets)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(completed.returncode, 0, completed.stdout)

    def test_gsap_example_uses_reduced_motion_branch_and_capped_pixel_ratio(self):
        page = (ROOT / ".agents" / "skills" / "bc-design" / "assets" / "motion" / "gsap-atelier.html").read_text(encoding="utf-8")
        self.assertIn("./bc-motion.js", page)
        self.assertIn("gsap@3.15.0", page)
        self.assertIn("Math.min(window.devicePixelRatio, 2)", page)
        helpers = (ROOT / ".agents" / "skills" / "bc-design" / "assets" / "motion" / "bc-motion.js").read_text(encoding="utf-8")
        self.assertIn("(prefers-reduced-motion: reduce)", helpers)
        self.assertIn('"expo.out"', helpers)


if __name__ == "__main__":
    unittest.main()
