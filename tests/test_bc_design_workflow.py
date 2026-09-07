import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / ".agents" / "skills" / "bc-design"
SKILL_FILE = SKILL_ROOT / "SKILL.md"
WORKFLOW_FILE = SKILL_ROOT / "references" / "bc-design-workflow.md"


class BCDesignWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = SKILL_FILE.read_text(encoding="utf-8")
        cls.workflow = WORKFLOW_FILE.read_text(encoding="utf-8") if WORKFLOW_FILE.exists() else ""

    def test_skill_description_is_discoverable_by_intent(self):
        self.assertIn("description: Use when", self.skill)
        for trigger in ("new interface", "redesign", "restyling", "audit", "generic patterns"):
            self.assertIn(trigger, self.skill.lower())

    def test_skill_routes_all_five_design_modes(self):
        for mode in ("greenfield", "redesign", "restyling", "design audit", "distinctive review"):
            self.assertIn(mode, self.skill.lower())
            self.assertIn(mode, self.workflow.lower())

    def test_workflow_requires_quality_gates_and_deliverables(self):
        for gate in ("Present the direction", "Plan multi-step work", "Implement in small slices", "Verify before handoff"):
            self.assertIn(gate, self.workflow)
        for deliverable in ("baseline", "design contract", "implementation plan", "verification report"):
            self.assertIn(deliverable, self.workflow.lower())

    def test_workflow_preserves_audit_boundary_and_stop_conditions(self):
        self.assertIn("do not modify", self.workflow.lower())
        self.assertIn("approval", self.workflow.lower())
        self.assertIn("evidence", self.workflow.lower())
        self.assertIn("no unconditional pass", self.workflow.lower())

    def test_skill_links_relevant_references_progressively(self):
        self.assertIn("references/bc-design-workflow.md", self.skill)
        self.assertIn("references/bc-design-guidelines.md", self.skill)
        self.assertIn("references/ux-guidelines.md", self.skill)
        self.assertIn("stacks/", self.skill)


if __name__ == "__main__":
    unittest.main()
