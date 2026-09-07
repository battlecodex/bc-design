# BC Design Code Configuration: BC Design System

This project uses the **BC Design System & Design Intelligence Engine**.

## Core Visual Directives
- **Canvas & Elevation**: Use warm book parchment `#FAF9F5` in light mode and deep espresso soot `#181816` in dark mode. Never use cold blue slates (`#0F172A`) or harsh `#000000`.
- **Primary Brand Accent**: Terracotta `#D97757` (dark mode `#E28466`, hover `#C15F3E`).
- **Dark Mode Modal CTAs**: Use Crisp Solid White (`#FFFFFF`) with dark text (`#1F1E1B`) for primary dialog and hero action buttons. Terracotta is reserved for AI streaming and brand moments.
- **Typography**: Editorial Serif headlines (`Newsreader`) paired with a neutral `Inter` UI sans. Enable optical sizing `opsz`.
- **Motion**: Signature exponential curve `cubic-bezier(0.16, 1, 0.3, 1)`. Speed budget: 150ms for buttons, 250ms for cards, 400ms for drawers.
- **Streaming Rule**: NEVER animate container dimensions while AI text streams (prevents browser layout thrashing).
- **Icons**: Monoline 1.5px stroke (`lucide-react` with `strokeWidth={1.5}`).

## Design Intelligence CLI
Run the zero-dependency Python design engine for instant recommendations:
```bash
py -3 scripts/bc_design.py "<user_request>" --design-system
py -3 scripts/bc_design.py "canonical" --domain style
py -3 scripts/bc_design.py "saas" --domain color
py -3 scripts/bc_design.py "canonical" --domain typography
py -3 scripts/bc_design.py "area" --domain chart
py -3 scripts/bc_design.py "hero prompt" --domain landing
py -3 scripts/bc_design.py "animation" --domain ux
```

## Deep References
- Design Tokens: `.agents/skills/bc-design/references/tokens.css`
- Component Blueprints: `.agents/skills/bc-design/references/components.md`
- 10 Design Styles: `.agents/skills/bc-design/references/styles.md`
- 10 Color Palettes: `.agents/skills/bc-design/references/palettes.md`
- 10 Typography Pairings: `.agents/skills/bc-design/references/typography.md`
- Data Visualizations: `.agents/skills/bc-design/references/charts.md`
- 7 Landing Patterns: `.agents/skills/bc-design/references/landing-patterns.md`
- UX & A11y Guidelines: `.agents/skills/bc-design/references/ux-guidelines.md`
