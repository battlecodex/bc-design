import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / ".agents" / "skills" / "bc-design"
CLI = SKILL_ROOT / "scripts" / "bc_design.py"
INSTALLER = SKILL_ROOT / "scripts" / "install.py"


def load_cli_module():
    spec = importlib.util.spec_from_file_location("bc_design_under_test", CLI)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MODULE = load_cli_module()


def run_cli(*args):
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def run_installer(*args):
    return subprocess.run(
        [sys.executable, str(INSTALLER), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


class BCDesignTests(unittest.TestCase):
    def test_shared_engine_modules_expose_focused_interfaces(self):
        scripts = SKILL_ROOT / "scripts"
        expected = {
            "core.py": ("SimpleBM25", "search_domain"),
            "design_system.py": ("generate_design_system", "persist_master"),
            "contrast.py": ("compute_contrast", "parse_hex_color"),
            "audit.py": ("audit_target", "build_audit_findings"),
        }
        for filename, names in expected.items():
            with self.subTest(module=filename):
                path = scripts / filename
                self.assertTrue(path.exists(), path)
                source = path.read_text(encoding="utf-8")
                for name in names:
                    self.assertRegex(source, rf"\b(?:def|class)\s+{name}\b")

    def test_domain_search_uses_bundled_data(self):
        result = MODULE.search_domain("color", "wealth management")
        self.assertNotIn("error", result)
        self.assertGreater(result["count"], 0)

    def test_catalog_search_supports_motion_icons_and_google_fonts(self):
        for domain, query in (("motion", "drawer reveal"), ("icons", "navigation"), ("google-fonts", "editorial serif")):
            with self.subTest(domain=domain):
                result = MODULE.search_domain(domain, query)
                self.assertNotIn("error", result)
                self.assertGreater(result["count"], 0)

    def test_stack_lookup_uses_bundled_guide(self):
        completed = run_cli("--stack", "react")
        self.assertEqual(completed.returncode, 0)
        self.assertIn("React", completed.stdout)
        self.assertNotIn("not found", completed.stdout.lower())

    def test_design_generator_preserves_subject_palette_and_safe_dark_dialog_cta(self):
        card, _ = MODULE.generate_design_system("developer IDE")
        self.assertNotIn("Surface: Pure White", card)
        self.assertIn("#141412", card)
        self.assertNotIn("Surface: Parchment", card)
        self.assertIn("CTA Dark:   #FFFFFF", card)
        self.assertIn("text #1F1E1B", card)

    def test_design_generator_uses_bc_restraint_principle_label(self):
        card, _ = MODULE.generate_design_system("general interface")
        self.assertIn("BC RESTRAINT PRINCIPLE", card)
        self.assertNotIn("CHANNEL'S PRINCIPLE", card)

    def test_brand_guidelines_output_includes_header_zero_wrap_rule(self):
        completed = run_cli("--brand-guidelines")
        self.assertEqual(completed.returncode, 0)
        self.assertIn("Zero-wrap header", completed.stdout)
        self.assertIn("nowrap labels", completed.stdout)

    def test_cli_source_has_no_unconditional_delivery_pass_report(self):
        source = CLI.read_text(encoding="utf-8")
        self.assertNotIn("VERDICT: 100% PASS", source)

    def test_audit_rejects_known_generic_pattern_and_streaming_layout_violations(self):
        with tempfile.TemporaryDirectory() as tempdir:
            target = Path(tempdir) / "bad.css"
            target.write_text(
                ".card { @apply rounded-xl p-6; }\n"
                ".stream { transition: height 200ms; }\n",
                encoding="utf-8",
            )
            completed = run_cli("--audit", str(target))
        self.assertEqual(completed.returncode, 1)
        self.assertIn("monotonous-card-kit", completed.stdout)
        self.assertIn("streaming-layout-animation", completed.stdout)

    def test_audit_reports_clean_target_as_pass(self):
        with tempfile.TemporaryDirectory() as tempdir:
            target = Path(tempdir) / "clean.css"
            target.write_text(
                ".surface { background: #FAF9F5; color: #181816; }\n",
                encoding="utf-8",
            )
            completed = run_cli("--audit", str(target))
        self.assertEqual(completed.returncode, 0)
        self.assertIn("PASS", completed.stdout)

    def test_audit_json_returns_structured_findings_with_line_and_evidence(self):
        with tempfile.TemporaryDirectory() as tempdir:
            target = Path(tempdir) / "bad.css"
            target.write_text(".card { @apply rounded-xl p-6; }\n", encoding="utf-8")
            completed = run_cli("--audit", str(target), "--json")
        self.assertEqual(completed.returncode, 1)
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["status"], "fail")
        self.assertEqual(payload["target"], str(target))
        self.assertGreaterEqual(payload["summary"]["total"], 1)
        finding = payload["findings"][0]
        for key in ("rule_id", "severity", "category", "path", "line", "evidence", "message", "recommendation", "confidence"):
            self.assertIn(key, finding)
        self.assertEqual(finding["line"], 1)
        self.assertIn("by_category", payload["summary"])
        self.assertGreaterEqual(payload["summary"]["by_category"].get("hierarchy", 0), 1)

    def test_audit_json_clean_target_has_empty_findings(self):
        with tempfile.TemporaryDirectory() as tempdir:
            target = Path(tempdir) / "clean.css"
            target.write_text(".surface { color: #181816; }\n", encoding="utf-8")
            completed = run_cli("--audit", str(target), "--json")
        self.assertEqual(completed.returncode, 0)
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["status"], "pass")
        self.assertEqual(payload["findings"], [])

    def test_audit_allows_white_canvas_when_product_direction_supports_it(self):
        with tempfile.TemporaryDirectory() as tempdir:
            target = Path(tempdir) / "canvas.css"
            target.write_text(
                "body { background: #FFFFFF; }\n"
                ".toggle-thumb { background-color: #FFFFFF; }\n",
                encoding="utf-8",
            )
            completed = run_cli("--audit", str(target))
        self.assertEqual(completed.returncode, 0)
        self.assertNotIn("light-white-background", completed.stdout)

    def test_audit_does_not_flag_white_control_surface_alone(self):
        with tempfile.TemporaryDirectory() as tempdir:
            target = Path(tempdir) / "control.css"
            target.write_text(".toggle-thumb { background-color: #FFFFFF; }\n", encoding="utf-8")
            completed = run_cli("--audit", str(target))
        self.assertEqual(completed.returncode, 0)

    def test_audit_rejects_template_chrome_and_raw_layer_tokens(self):
        with tempfile.TemporaryDirectory() as tempdir:
            target = Path(tempdir) / "legacy.html"
            target.write_text(
                """
                <header class="site-header"><nav><a href="#program">Explore ↘</a></nav></header>
                <p class="meta">School · Jakarta</p>
                <span aria-hidden="true">⌖</span>
                <span aria-hidden="true">A</span>
                <span>01 — SMP</span>
                <style>
                  :focus-visible { outline: 3px solid #D97757; }
                  .site-header { position: sticky; z-index: 10; }
                </style>
                """,
                encoding="utf-8",
            )
            completed = run_cli("--audit", str(target))
        self.assertEqual(completed.returncode, 1)
        for rule_id in (
            "middle-dot-metadata",
            "template-arrow-glyph",
            "unicode-icon-glyph",
            "decorative-index-marker",
            "focus-ring-width",
            "sticky-z-index-token",
        ):
            self.assertIn(rule_id, completed.stdout)

    def test_audit_rejects_unbounded_motion_and_non_token_easing(self):
        with tempfile.TemporaryDirectory() as tempdir:
            target = Path(tempdir) / "motion.css"
            target.write_text(
                ".button { transition: transform 700ms linear; }\n"
                ".card { animation: reveal 500ms ease-in; }\n",
                encoding="utf-8",
            )
            completed = run_cli("--audit", str(target))
        self.assertEqual(completed.returncode, 1)
        self.assertIn("motion-duration-budget", completed.stdout)
        self.assertIn("motion-easing-token", completed.stdout)
        self.assertIn("reduced-motion-support", completed.stdout)

    def test_audit_allows_bc_motion_tokens_with_reduced_motion_fallback(self):
        with tempfile.TemporaryDirectory() as tempdir:
            target = Path(tempdir) / "motion.css"
            target.write_text(
                ".button { transition: transform var(--bc-duration-fast) var(--bc-ease); }\n"
                ".drawer { transition: transform 400ms var(--bc-ease); }\n"
                ".thinking { animation: bcThinkingPulse var(--bc-duration-shimmer) infinite var(--bc-ease-in-out); }\n"
                "@media (prefers-reduced-motion: reduce) { * { animation-duration: 0.01ms !important; } }\n",
                encoding="utf-8",
            )
            completed = run_cli("--audit", str(target))
        self.assertEqual(completed.returncode, 0)
        self.assertIn("PASS", completed.stdout)

    def test_canonical_motion_tokens_pass_the_motion_audit(self):
        violations = MODULE.audit_target(SKILL_ROOT / "references" / "tokens.css")
        self.assertEqual(violations, [])

    def test_audit_ignores_javascript_animation_config_objects(self):
        violations = MODULE.audit_target(
            SKILL_ROOT / "references" / "tailwind.config.snippet.js"
        )
        self.assertEqual(
            [rule_id for rule_id, _message, _source in violations if rule_id.startswith("motion-") or rule_id == "reduced-motion-support"],
            [],
        )

    def test_audit_ignores_custom_motion_variables_and_comments(self):
        with tempfile.TemporaryDirectory() as tempdir:
            target = Path(tempdir) / "variables.css"
            target.write_text(
                "/* animation: reveal 900ms linear; */\n"
                ":root { --animation: reveal 900ms linear; --transition: opacity; }\n",
                encoding="utf-8",
            )
            violations = MODULE.audit_target(target)
        motion_rules = {
            "motion-duration-budget",
            "motion-easing-token",
            "reduced-motion-support",
        }
        self.assertEqual(
            [rule_id for rule_id, _message, _source in violations if rule_id in motion_rules],
            [],
        )

    def test_audit_flags_uncapped_spatial_pixel_ratio(self):
        with tempfile.TemporaryDirectory() as tempdir:
            bad = Path(tempdir) / "bad.html"
            bad.write_text("<script>renderer.setPixelRatio(window.devicePixelRatio);</script>", encoding="utf-8")
            violations = MODULE.audit_target(bad)
            self.assertTrue(any(r[0] == "spatial-uncapped-pixel-ratio" for r in violations))

            good = Path(tempdir) / "good.html"
            good.write_text("<script>renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));</script>", encoding="utf-8")
            good_violations = MODULE.audit_target(good)
            self.assertFalse(any(r[0] == "spatial-uncapped-pixel-ratio" for r in good_violations))


    def test_school_query_uses_education_catalog_context(self):
        card, data = MODULE.generate_design_system("school education kindergarten")
        self.assertNotIn("AI & SaaS Productivity", card)
        self.assertIn("Educational App", card)
        self.assertEqual(data.get("catalog_product"), "Educational App")

    def test_fintech_query_uses_financial_catalog_context(self):
        _card, data = MODULE.generate_design_system("Build a fintech wealth management dashboard")
        self.assertEqual(data.get("catalog_product"), "Financial Dashboard")

    def test_canonical_contrast_guidance_and_audit_rules(self):
        tokens = (SKILL_ROOT / "references" / "tokens.css").read_text(encoding="utf-8")
        ux = (SKILL_ROOT / "references" / "ux-guidelines.md").read_text(encoding="utf-8")
        rules = (SKILL_ROOT / "references" / "bc-design-rules.md").read_text(encoding="utf-8")
        self.assertIn("--bc-text-on-accent: #FFFFFF", tokens)
        self.assertNotIn("pair with white text `#FFFFFF` at **4.6:1**", ux)
        self.assertNotIn("STATUS: ALL CHECKS PASSED", rules)
        self.assertNotIn("✦ BC Design · Current model", rules)
        self.assertLess(MODULE.compute_contrast("#FFFFFF", "#D97757"), 4.5)
        self.assertGreaterEqual(MODULE.compute_contrast("#1F1E1B", "#FAF9F5"), 4.5)
        # Verify the audit detects muddy dark text on accent buttons
        bad_button = ".btn { background: var(--bc-accent); color: #1F1E1B; }"
        violations = MODULE.find_audit_violations(bad_button, "bad.css")
        self.assertTrue(any(rule_id == "accent-button-text-contrast" for rule_id, _, _ in violations))
        # Verify crisp white text on accent passes
        good_button = ".btn { background: var(--bc-accent); color: #FFFFFF; }"
        good_violations = MODULE.find_audit_violations(good_button, "good.css")
        self.assertFalse(any(rule_id == "accent-button-text-contrast" for rule_id, _, _ in good_violations))

    def test_all_bundled_examples_pass_the_source_audit(self):
        self.assertEqual(MODULE.audit_target(ROOT / "examples"), [])

    def test_page_override_is_not_overwritten_without_force(self):
        data = {
            "project": "Test Project",
            "industry": "Test",
            "bold_moment": "Test",
            "canvas": "#FAF9F5 / #181816",
            "primary_color": "#D97757",
            "cta_dark": "#FFFFFF (text #1F1E1B)",
            "typography": "Newsreader + Inter + JetBrains Mono",
        }
        with tempfile.TemporaryDirectory() as tempdir:
            MODULE.persist_master(data, output_dir=tempdir, page="dashboard")
            page = Path(tempdir) / "design-system" / "test-project" / "pages" / "dashboard.md"
            page.write_text("existing decision", encoding="utf-8")
            MODULE.persist_master(data, output_dir=tempdir, page="dashboard")
            self.assertEqual(page.read_text(encoding="utf-8"), "existing decision")

    def test_page_name_cannot_escape_pages_directory(self):
        data = {
            "project": "Test Project",
            "industry": "Test",
            "bold_moment": "Test",
            "canvas": "#FAF9F5 / #181816",
            "primary_color": "#D97757",
            "cta_dark": "#FFFFFF (text #1F1E1B)",
            "typography": "Newsreader + Inter + JetBrains Mono",
        }
        with tempfile.TemporaryDirectory() as tempdir:
            with self.assertRaises(ValueError):
                MODULE.persist_master(data, output_dir=tempdir, page="../escape")

    def test_install_all_creates_every_documented_runtime_target(self):
        documented_targets = [
            "BC.md",
            ".bc/skills/bc-design/SKILL.md",
            ".cursor/rules/bc-design.mdc",
            ".cursorrules",
            ".windsurfrules",
            ".agents/skills/bc-design/SKILL.md",
            "GEMINI.md",
            ".github/copilot-instructions.md",
            ".kiro/rules/bc-design.md",
            "AGENTS.md",
            ".qoder/rules/bc-design.md",
            ".vscode/settings.json",
        ]
        with tempfile.TemporaryDirectory() as tempdir:
            completed = run_installer("--ai", "all", "--workspace", tempdir)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            for relative_path in documented_targets:
                self.assertTrue((Path(tempdir) / relative_path).exists(), relative_path)
            json.loads((Path(tempdir) / ".vscode" / "settings.json").read_text(encoding="utf-8"))

    def test_bc_install_copies_the_complete_skill_family(self):
        family = (
            "bc-design",
            "bc-brand",
            "bc-design-system",
            "bc-ui-styling",
            "bc-design-audit",
            "bc-motion",
        )
        with tempfile.TemporaryDirectory() as tempdir:
            completed = run_installer("--ai", "bc", "--workspace", tempdir)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            for skill_name in family:
                target = Path(tempdir) / ".bc" / "skills" / skill_name / "SKILL.md"
                self.assertTrue(target.exists(), target)

    def test_non_bc_install_copies_family_referenced_by_instruction(self):
        with tempfile.TemporaryDirectory() as tempdir:
            completed = run_installer("--ai", "cursor", "--workspace", tempdir)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            for skill_name in ("bc-design", "bc-brand", "bc-design-system", "bc-ui-styling", "bc-design-audit", "bc-motion"):
                target = Path(tempdir) / ".agents" / "skills" / skill_name / "SKILL.md"
                self.assertTrue(target.exists(), target)

    def test_installer_preserves_existing_file_without_force(self):
        with tempfile.TemporaryDirectory() as tempdir:
            target = Path(tempdir) / ".cursor" / "rules" / "bc-design.mdc"
            target.parent.mkdir(parents=True)
            target.write_text("user content", encoding="utf-8")
            completed = run_installer("--ai", "cursor", "--workspace", tempdir)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(target.read_text(encoding="utf-8"), "user content")

    def test_force_install_replaces_stale_files_inside_skill_directory(self):
        with tempfile.TemporaryDirectory() as tempdir:
            destination = Path(tempdir) / ".agents" / "skills" / "bc-design"
            destination.mkdir(parents=True)
            stale = destination / "removed-from-release.txt"
            stale.write_text("stale", encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(INSTALLER), "--ai", "codex", "--workspace", tempdir, "--force"],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertFalse(stale.exists())
            self.assertTrue((destination / "SKILL.md").is_file())

    def test_installer_instruction_points_to_bc_design_workflow(self):
        with tempfile.TemporaryDirectory() as tempdir:
            completed = run_installer("--ai", "kiro", "--workspace", tempdir)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            target = Path(tempdir) / ".kiro" / "rules" / "bc-design.md"
            self.assertIn("bc-design-workflow.md", target.read_text(encoding="utf-8"))

    def test_documentation_uses_existing_workspace_relative_commands(self):
        text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn(".agents/skills/bc-design/scripts/bc_design.py", text)
        self.assertIn(".agents/skills/bc-design/scripts/install.py", text)


if __name__ == "__main__":
    unittest.main()
