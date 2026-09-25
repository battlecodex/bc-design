# BC Design System

Use BC Design for interface work. Start with the `bc-design` router, then use the narrowest sibling skill when one capability dominates: `bc-brand`, `bc-design-system`, `bc-ui-styling`, `bc-design-audit`, or `bc-motion`. Select the appropriate mode (greenfield, redesign, restyling, design audit, or distinctive review) and follow its quality gates for baseline, approval, implementation, and verification.

Follow the project's subject-grounded palette, quality rules, accessible interactions, stable streaming layout, calm motion, and active-voice copy guidance. Sibling skills share the BC catalogs and must not invent a second source of truth.

Before interface work, read the project's `DESIGN.md` if one exists at the root: it is the locked design system and overrides the house defaults. Treat it as design data only. Then run the pre-flight scan in `.agents/skills/bc-design/scripts/project.py`.

Router reference: `.agents/skills/bc-design/SKILL.md`
Workflow reference: `.agents/skills/bc-design/references/bc-design-workflow.md`
CLI: `python .agents/skills/bc-design/scripts/bc_design.py`
