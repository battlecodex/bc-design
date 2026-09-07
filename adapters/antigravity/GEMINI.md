# Antigravity Workspace Rule: BC Design System

Adhere to the **BC Design language and component guidance** for all frontend, component, and visual layout tasks in this workspace.

## Key Rules
- **Canvas Colors**: Light mode `#FAF9F5` (warm parchment), Dark mode `#181816` (espresso soot).
- **Brand Accent**: Terracotta `#D97757` (dark mode `#E28466`).
- **Dark Mode Button Contrast**: Solid Crisp White `#FFFFFF` with `#1F1E1B` text for primary modal/hero CTAs.
- **Serif Headlines**: `Newsreader` (`opsz` optical sizing).
- **Sans Interface**: `Inter` for clean, readable UI controls.
- **BC Design Motion**: `cubic-bezier(0.16, 1, 0.3, 1)` with 150ms-250ms duration budget.
- **Streaming Token Safety**: Never animate container dimensions while text streams.
- **Hairline Icons**: 1.5px stroke width (`lucide-react` with `strokeWidth={1.5}`).

## Available Skill
Activate the router at `.agents/skills/bc-design/SKILL.md`, then route to the narrowest sibling skill under `.agents/skills/` when appropriate.
Use the design engine:
```bash
py -3 scripts/bc_design.py "<prompt>" --design-system
```
