import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / ".agents" / "skills" / "bc-design" / "scripts" / "bc_design.py"


class DistinctiveAuditTests(unittest.TestCase):
    def audit(self, source):
        with tempfile.TemporaryDirectory() as tempdir:
            target = Path(tempdir) / "fixture.css"
            target.write_text(source, encoding="utf-8")
            result = subprocess.run([sys.executable, str(CLI), "--audit", str(target), "--json"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        return result.returncode, json.loads(result.stdout)

    def rules(self, source):
        return {finding["rule_id"] for finding in self.audit(source)[1]["findings"]}

    def test_flags_unearned_gradient_and_excessive_pills(self):
        code, payload = self.audit(
            ".hero { background: linear-gradient(135deg, #7c3aed, #2563eb); }\n"
            + "\n".join(f".pill-{i} {{ border-radius: 999px; }}" for i in range(4))
        )
        self.assertEqual(1, code)
        rules = {finding["rule_id"] for finding in payload["findings"]}
        self.assertIn("generic-gradient-wash", rules)
        self.assertIn("excessive-pill-capsules", rules)

    def test_round_controls_are_not_pill_capsules(self):
        source = (
            '<img class="h-8 w-8 rounded-full" alt="Ana">\n'
            '<span class="avatar rounded-full">A</span>\n'
            '<input type="radio" class="rounded-full">\n'
            '<div class="progress h-2 rounded-full"></div>\n'
        )
        self.assertNotIn("excessive-pill-capsules", self.rules(source))

    def test_state_names_and_color_transitions_are_not_findings(self):
        source = (
            'const [mode, setMode] = useState("submit"); if (mode === "submit") {} setMode("submit");\n'
            '<div className="token-stream transition-colors hover:bg-muted px-4 h-full"></div>\n'
        )
        rules = self.rules(source)
        self.assertNotIn("repeated-generic-cta", rules)
        self.assertNotIn("streaming-layout-animation", rules)

    def test_allows_one_tag_pill_and_subject_requested_gradient(self):
        code, payload = self.audit(
            ".tag { border-radius: 999px; }\n"
            ".artwork { background: linear-gradient(135deg, #d97757, #e28466); }\n"
        )
        self.assertEqual(0, code)
        self.assertEqual([], payload["findings"])

    def test_flags_accent_dominating_the_page_canvas(self):
        code, payload = self.audit("body { background: #D97757; color: #1F1E1B; }\n")
        self.assertEqual(1, code)
        self.assertIn("accent-surface-domination", {finding["rule_id"] for finding in payload["findings"]})

    def test_flags_template_chrome_hero_displacement_and_repeated_ctas(self):
        source = (
            ".hero { font-size: 120px; }\n"
            '<p class="eyebrow">EXPLORE PLATFORM</p><p class="eyebrow">EXPLORE PLATFORM</p><p class="eyebrow">EXPLORE PLATFORM</p>\n'
            "<button>Get started</button><button>Get started</button><button>Get started</button>\n"
            "<div>New task</div><div>Projects</div><div>Settings</div>\n"
        )
        code, payload = self.audit(source)
        self.assertEqual(1, code)
        rules = {finding["rule_id"] for finding in payload["findings"]}
        self.assertIn("decorative-eyebrow-overload", rules)
        self.assertIn("oversized-hero-displacement", rules)
        self.assertIn("copied-platform-chrome", rules)
        self.assertIn("repeated-generic-cta", rules)


if __name__ == "__main__":
    unittest.main()
