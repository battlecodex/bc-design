# Kiro Rule: BC Design System

## Instructions
When generating, styling, or refactoring UI components:
- Match the **BC Design aesthetic**: Warm parchment `#FAF9F5`, espresso soot `#181816`, terracotta `#D97757`.
- Primary CTAs in dark mode: Solid White `#FFFFFF` with dark text.
- Headings: Editorial serif (`Newsreader`).
- UI Text: Neutral clean sans (`Inter`).
- Motion: `cubic-bezier(0.16, 1, 0.3, 1)`.
- Icons: 1.5px monoline stroke.
- Never animate container dimensions during AI token streaming.

## Command
Run design intelligence: `py -3 scripts/bc_design.py "<prompt>" --design-system`
