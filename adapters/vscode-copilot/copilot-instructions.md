# BC Design System - GitHub Copilot Custom Instructions

When writing or modifying frontend code in this workspace, follow the **BC Design System**:

## Aesthetic Philosophy
- Always design for a warm, literary, humanistic experience.
- Never default to cold, sterile tech gray (`#0F172A`) or pure harsh `#FFFFFF` canvases.
- Canvas background: Light mode uses `#FAF9F5` (warm parchment), dark mode uses `#181816` (espresso soot).
- Primary brand accent: Signature Terracotta `#D97757` (dark mode `#E28466`).
- Dark mode modal CTA: Crisp Solid White (`#FFFFFF`) with dark text.

## Typography
- Headings: Always use an editorial serif (`Newsreader`, `Georgia`).
- Interface & Body: Clean, readable neutral sans-serif (`Inter`, `system-ui`).
- Code: Warm monospace (`JetBrains Mono`, `Fira Code`).

## Motion & Interaction
- BC Design signature easing: `cubic-bezier(0.16, 1, 0.3, 1)`.
- Duration budget: 150ms for buttons, 250ms for cards, 400ms for drawers.
- Streaming rule: Never animate container dimensions while AI text streams.

## Icons & UI Components
- Icons: Monoline SVG with stroke width `1.5` (use `lucide-react` with `strokeWidth={1.5}`).
- Button radius: `8px` to `10px` (`rounded-lg`). Do not use full pill capsules for main CTAs.
- Inset wells: Subtle borders (`rgba(31, 30, 27, 0.08)`) with soft warm inner background.

## Full Reference Files
- Master Intelligence Skill: `.agents/skills/bc-design/SKILL.md`
- 10 Design Styles: `.agents/skills/bc-design/references/styles.md`
- 10 Product Palettes: `.agents/skills/bc-design/references/palettes.md`
- 10 Typography Pairings: `.agents/skills/bc-design/references/typography.md`
- Data Visualization Charts: `.agents/skills/bc-design/references/charts.md`
- 7 Landing Patterns: `.agents/skills/bc-design/references/landing-patterns.md`
- UX Guidelines: `.agents/skills/bc-design/references/ux-guidelines.md`
- CSS Tokens: `.agents/skills/bc-design/references/tokens.css`
- Components: `.agents/skills/bc-design/references/components.md`
