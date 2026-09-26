---
name: bc-design
description: Use when creating a new interface, redesigning an existing one, restyling a product, reviewing UI quality, or auditing an AI-generated interface for generic patterns.
---

# BC Design (repository checkout)

This folder is the BC Design repository, cloned directly into a skills folder. It is a pointer, not a second copy of the skill:

1. Read `.agents/skills/bc-design/SKILL.md` inside this folder and follow it. Everything else (references, catalogs, scripts) lives next to that file.
2. Paths in that file start at `.agents/skills/bc-design/`. Resolve them from this folder: for example, run the pre-flight scan as `python <this folder>/.agents/skills/bc-design/scripts/project.py preflight` from the project root.
3. The sibling skills (`bc-brand`, `bc-design-system`, `bc-ui-styling`, `bc-design-audit`, `bc-motion`) are in `.agents/skills/` here. A checkout registers only this router, so read them by path when a request needs one.

For a regular install that registers all six skills and writes the paths for your assistant, run `python scripts/install.py --ai claude --global` from this folder, then remove the checkout from the skills folder.
