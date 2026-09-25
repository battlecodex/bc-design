import re
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / ".agents" / "skills" / "bc-design"
FAMILY_ROOT = ROOT / ".agents" / "skills"
SKILL_FAMILY = (
    "bc-design",
    "bc-brand",
    "bc-design-system",
    "bc-ui-styling",
    "bc-design-audit",
    "bc-motion",
)
LEGACY_TERMS = (
    "cl" + "aude",
    "anthr" + "opic",
    "super" + "power",
    "anti[- ]?sl" + "op",
)
FORBIDDEN = re.compile("|".join(LEGACY_TERMS), re.IGNORECASE)
# Install targets name the host tool a runtime writes to; they are not branding.
RUNTIME_TARGET_REFERENCES = re.compile(r'[`"]claude[`"]|\.claude/skills|CLAUDE\.md')


def without_runtime_targets(text):
    return RUNTIME_TARGET_REFERENCES.sub("", text)


class BCDesignRebrandTests(unittest.TestCase):
    def test_bc_design_skill_family_has_discriminating_entrypoints(self):
        for skill_name in SKILL_FAMILY:
            with self.subTest(skill=skill_name):
                skill_file = FAMILY_ROOT / skill_name / "SKILL.md"
                self.assertTrue(skill_file.exists(), skill_file)
                skill = skill_file.read_text(encoding="utf-8")
                self.assertIn(f"name: {skill_name}", skill)
                self.assertRegex(skill, r"description:\s*Use when")
                self.assertNotRegex(without_runtime_targets(skill), FORBIDDEN)

    def test_router_names_every_specialized_skill_without_copying_catalogs(self):
        router = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        for skill_name in SKILL_FAMILY[1:]:
            self.assertIn(skill_name, router)
            self.assertFalse((FAMILY_ROOT / skill_name / "data").exists())

    def test_sibling_skill_references_resolve_to_existing_resources(self):
        for skill_name in SKILL_FAMILY[1:]:
            skill_file = FAMILY_ROOT / skill_name / "SKILL.md"
            text = skill_file.read_text(encoding="utf-8")
            for relative in re.findall(r"`(\.\.?/[^`]+)`", text):
                self.assertTrue((skill_file.parent / relative).exists(), (skill_name, relative))

    def test_bc_design_skill_layout_and_identity(self):
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("name: bc-design", skill)
        self.assertIn("BC Design", skill)
        self.assertNotRegex(without_runtime_targets(skill), FORBIDDEN)

    def test_active_skill_contains_no_legacy_brand_or_process_terms(self):
        self.assertTrue(SKILL_ROOT.is_dir())
        offenders = []
        for path in SKILL_ROOT.rglob("*"):
            if not path.is_file():
                continue
            # Upstream licenses require naming the projects BC Design builds on.
            if path.name == "THIRD_PARTY_NOTICES.md":
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if FORBIDDEN.search(without_runtime_targets(text)) or FORBIDDEN.search(path.name):
                offenders.append(str(path.relative_to(ROOT)))
        self.assertEqual(offenders, [], f"legacy terms remain in: {offenders}")

    def test_workflow_uses_bc_design_quality_language(self):
        workflow = (SKILL_ROOT / "references" / "bc-design-workflow.md").read_text(encoding="utf-8")
        for mode in ("greenfield", "redesign", "restyling", "design audit", "distinctive review"):
            self.assertIn(mode, workflow.lower())
        for deliverable in ("baseline", "design contract", "implementation plan", "verification report"):
            self.assertIn(deliverable, workflow.lower())
        self.assertIn("quality gate", workflow.lower())

    def test_bc_cli_and_installer_are_rebranded(self):
        cli = SKILL_ROOT / "scripts" / "bc_design.py"
        installer = SKILL_ROOT / "scripts" / "install.py"
        self.assertTrue(cli.exists())
        self.assertTrue(installer.exists())
        self.assertIn("--brand-guidelines", cli.read_text(encoding="utf-8"))
        self.assertIn("bc-design", installer.read_text(encoding="utf-8"))
        self.assertNotRegex(without_runtime_targets(installer.read_text(encoding="utf-8")), FORBIDDEN)

    def test_repository_entrypoint_delegates_to_bc_cli(self):
        entrypoint = ROOT / "scripts" / "bc_design.py"
        completed = subprocess.run(
            [sys.executable, str(entrypoint), "--brand-guidelines"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0)
        self.assertIn("BC DESIGN GUIDELINES", completed.stdout)


if __name__ == "__main__":
    unittest.main()
