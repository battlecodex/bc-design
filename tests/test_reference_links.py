import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agents" / "skills"
LINK = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")


class ReferenceLinkTests(unittest.TestCase):
    def test_relative_links_in_skill_docs_resolve(self):
        broken = []
        for document in sorted(SKILLS.rglob("*.md")):
            for target in LINK.findall(document.read_text(encoding="utf-8")):
                if "://" in target or target.startswith("mailto:"):
                    continue
                if not (document.parent / target).exists():
                    broken.append(f"{document.relative_to(ROOT)} -> {target}")
        self.assertEqual(broken, [])

    def test_new_references_are_reachable_from_the_router(self):
        router = (SKILLS / "bc-design" / "SKILL.md").read_text(encoding="utf-8")
        for name in ("inspiration-sources.md", "third-party-components.md", "pruning.md", "project-memory.md", "design-dimensions.md"):
            with self.subTest(reference=name):
                self.assertIn(f"references/{name}", router)


if __name__ == "__main__":
    unittest.main()
