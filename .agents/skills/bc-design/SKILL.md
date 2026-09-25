---
name: bc-design
description: Use when creating a new interface, redesigning an existing one, restyling a product, reviewing UI quality, or auditing an AI-generated interface for generic patterns.
---

# BC Design System

BC Design is a practical design-intelligence family for building clear, accessible, subject-grounded interfaces. This skill is the router and shared engine; focused sibling skills handle brand, tokens, UI styling, audits, and motion without duplicating the catalogs.

## Design foundation

BC Design has a recognizable editorial language, not a mandatory theme. Start from the product subject and existing brand evidence, then express it through these defaults:

- **Composition:** use clear editorial hierarchy, open space, hairline borders, restrained radii, and a mix of open groups, lists, and anchored panels. Avoid turning every section into a rounded card.
- **Color:** begin with warm or true neutral canvases and high-contrast ink. Draw one or two restrained accents from the subject. Parchment, terracotta, sage, and black are options—not automatic requirements—and an accent must not become a large default surface without evidence.
- **Typography:** default to Newsreader for editorial hierarchy and Inter for UI clarity. Change the pairing when brand evidence or the product context calls for it; reserve monospace for code and tabular values.
- **Contrast:** use tested foreground/background pairs grounded in the canonical high-contrast standard: primary actions default to solid ink `.bc-btn-contrast` (`#1F1E1B` with `#FFFFFF` text in light mode, `#FFFFFF` with `#1F1E1B` text in dark mode); accent/terracotta buttons use crisp white `#FFFFFF` text, never muddy dark ink.
- **Motion:** use `cubic-bezier(0.16, 1, 0.3, 1)` with a 150–250ms budget for ordinary interactions. Honor reduced motion.
- **Streaming:** never animate container width, height, margin, or padding while AI text streams.
- **Icons:** use 1.5px monoline icons, preferably Lucide, with visible focus states.

### Default enforcement

These are non-optional defaults for every BC Design implementation. Treat a deviation as a finding unless the user explicitly requests it and the design contract records the reason:

- Primary action buttons follow the canonical high-contrast standard (`.bc-btn-contrast` or crisp `#FFFFFF` text on accent); never pair dark ink text on mid-tone accent/terracotta buttons.
- Write metadata as labels or separate lines; do not use middle-dot separators (`A · B`).
- Use meaningful action labels; do not append Unicode arrows to links or buttons.
- Use purposeful 1.5px monoline SVG icons instead of Unicode glyphs for interface symbols.
- Do not add A/B/C or 01/02/03 markers unless they encode a real ordered sequence.
- Use a visible 2px focus ring derived from the active accent and the semantic sticky-navigation z-index token (`30`).
- Keep ordinary transitions/animations on motion tokens (150–250ms; up to 400ms for drawers/modals), use the shimmer token for 1800ms thinking states, and avoid browser-default easing keywords.
- Include a `prefers-reduced-motion: reduce` override in any source file that defines transitions or animations.

The CLI audit enforces these checks, including motion duration, easing-token, reduced-motion, and streaming-layout rules. A clean result still requires rendered-state verification.

## Workflow router

Classify the request before choosing a visual direction:

| Mode | Use when | First artifact |
| :--- | :--- | :--- |
| **Greenfield** | Creating a new interface or product surface | Brief and approved design contract |
| **Redesign** | Improving an existing interface while preserving useful behavior | Baseline inventory and invariants |
| **Restyling** | Changing visual language without changing behavior or information architecture | Semantic token map and frozen invariants |
| **Design audit** | Reviewing usability, accessibility, responsive quality, or consistency | Evidence-backed findings |
| **Distinctive review** | Checking whether a design feels generic or disconnected from its subject | Per-pattern evidence and a prioritized verdict |

Follow [references/bc-design-workflow.md](./references/bc-design-workflow.md) for the selected mode. It defines the baseline, design contract, quality gates, implementation plan, and verification report. Keep audit scope separate from remediation scope, and do not present an unverified pass.

### Specialized skills

Route to the narrowest sibling skill when one capability dominates the request:

- [`bc-brand`](../bc-brand/SKILL.md) for brand evidence, palette rationale, typography roles, voice, and asset usage.
- [`bc-design-system`](../bc-design-system/SKILL.md) for primitive/semantic tokens, component contracts, states, variants, themes, and governance.
- [`bc-ui-styling`](../bc-ui-styling/SKILL.md) for implementation or restyling while preserving approved behavior and stack-specific constraints.
- [`bc-design-audit`](../bc-design-audit/SKILL.md) for read-only quality, accessibility, responsive, consistency, or distinctive-pattern review.
- [`bc-motion`](../bc-motion/SKILL.md) for transitions, loading, overlays, page motion, reduced motion, and streamed AI feedback.

Keep `bc-design` as the entrypoint for mixed or ambiguous requests. Sibling skills consume this foundation and return to the router when scope expands.

## Progressive references

- Read [references/bc-design-guidelines.md](./references/bc-design-guidelines.md) for subject grounding, hierarchy, copy, and distinctiveness checks.
- Read [references/visual-language.md](./references/visual-language.md) when selecting typography, palette, shape, illustration, or layout direction.
- Read [references/catalog-alignment.md](./references/catalog-alignment.md) when a catalog search or generated direction needs compatibility classification; automatic output is limited to `core` and `compatible` entries.
- Read [references/ux-guidelines.md](./references/ux-guidelines.md) for accessibility, forms, motion, loading, and layout checks.
- Read [references/spatial-3d.md](./references/spatial-3d.md) when building 3D product visualizations, scroll-driven exploded views, or interactive spatial artifacts.
- Read the relevant guide in `stacks/` when implementing React, Next.js, Vue, Svelte, SwiftUI, React Native, Flutter, or Tailwind.
- Use [references/tokens.css](./references/tokens.css) as the canonical semantic token layer.

## Repository map

```text
.agents/skills/
├── bc-design/                    # Router, shared catalogs, engine, and compatibility CLI
├── bc-brand/                     # Brand evidence and token mapping
├── bc-design-system/             # Token/component contracts and governance
├── bc-ui-styling/                # Stack-specific visual implementation
├── bc-design-audit/              # Quality and distinctive review
└── bc-motion/                    # Motion and streamed-state guidance
```

## Installer

```bash
python .agents/skills/bc-design/scripts/install.py --ai all --workspace .
```

The installer is non-destructive by default. Add `--force` only when generated instruction files or the bundled skill directory should be replaced. Supported runtimes are `bc`, `claude`, `cursor`, `windsurf`, `antigravity`, `copilot`, `kiro`, `codex`, `qoder`, and `vscode`. The `claude` and `kiro` runtimes install the family into `.claude/skills/` and `.kiro/skills/`, where those tools discover skills natively; the other runtimes share `.agents/skills/`.

## CLI

Run commands from the workspace root. Use `python3` or `py -3` when that is the available launcher.

```bash
# Generate a complete direction and optionally persist MASTER.md
python .agents/skills/bc-design/scripts/bc_design.py "medical healthcare clinic" --design-system -p "Aether Care" --persist

# Print BC Design guidelines and quality checks
python .agents/skills/bc-design/scripts/bc_design.py --brand-guidelines

# Search the bundled design data
python .agents/skills/bc-design/scripts/bc_design.py "wealth management" --domain color
python .agents/skills/bc-design/scripts/bc_design.py "developer terminal" --domain style
python .agents/skills/bc-design/scripts/bc_design.py "luxury editorial" --domain typography
python .agents/skills/bc-design/scripts/bc_design.py "drawer reveal" --domain motion
python .agents/skills/bc-design/scripts/bc_design.py "navigation" --domain icons
python .agents/skills/bc-design/scripts/bc_design.py "editorial serif" --domain google-fonts
python .agents/skills/bc-design/scripts/bc_design.py "school academy 3d" --domain spatial

# Generate 3D spatial artifacts and scrollytelling stages
python .agents/skills/bc-design/scripts/bc_design.py --spatial list
python .agents/skills/bc-design/scripts/bc_design.py --spatial school-spatial --spatial-theme light -o examples/school-preview.html
python .agents/skills/bc-design/scripts/bc_design.py --spatial ribbon-field --spatial-palette terracotta -o examples/ribbon.html
python .agents/skills/bc-design/scripts/bc_design.py --spatial spatial-scrollytelling --spatial-theme dark -o examples/scrolly.html

# Read a framework guide
python .agents/skills/bc-design/scripts/bc_design.py --stack react
python .agents/skills/bc-design/scripts/bc_design.py --stack nextjs

# Audit a source file or directory; exits 1 when findings exist
python .agents/skills/bc-design/scripts/bc_design.py --audit path/to/source
python .agents/skills/bc-design/scripts/bc_design.py --audit path/to/source --json
```

## Delivery standard

Before handoff, report the inspected artifacts, commands run, observed results, design-contract checks, unverified surfaces, and any remaining user decision. A clean CLI result is one signal, not proof that a rendered interface is accessible or correct.
