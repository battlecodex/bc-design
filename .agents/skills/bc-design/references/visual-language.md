# BC Visual Language

BC Design is a house style: warm, literary, and editorial, with the quiet confidence of a finely printed book. Use this reference to apply the house style and to hold every page to the luxury standard below. When a project has its own brand colors, type, or imagery, map them onto the same roles and keep the standard.

## House style

- **Canvas and ink.** Warm parchment (`#FAF9F5`) in light mode and espresso (`#181816`) in dark mode, with high-contrast ink (`#1F1E1B` / `#FAF9F5`). Hairline borders at 8–9% ink opacity separate content instead of boxes.
- **One accent, chosen by subject.** Terracotta (`#D97757`) is the default. Use amber-brass for finance, instruments, and craft, and sage for health, wellbeing, and nature. Lock the chosen accent for the whole page; a second accent is a finding. Text-bearing fills and accent text use the strong accent (`#B35637`).
- **Type.** Newsreader for display and reading, with optical sizing on large headings; Inter for controls, labels, and data; a monospace face only for code and tabular figures.
- **Shape.** Small-to-moderate radii, crisp controls, and simple modal geometry. Pills are for tags, filters, and compact statuses.
- **Imagery.** Real product imagery, tactile diagrams, or sparse organic illustration that explains the subject. Decorative graphics must earn their space.

## Luxury standard

Luxury here means restraint, precision, and material quality. It never means more decoration. Every page meets all of these:

1. **Space is the first material.** Section rhythm uses generous, consistent vertical space (at least 96px between major sections on desktop, 64px on mobile). Crowding reads as cheap faster than any color choice.
2. **Few type sizes, clearly separated.** Use at most five sizes on a page, on a clear scale. The display size carries the page; body text stays at a comfortable 17–19px reading size with a 60–72 character measure.
3. **Hierarchy through weight and color before scale.** An oversized headline that shouts is not premium. Let a well-set serif at a moderate size, plus ink and secondary-ink contrast, carry importance.
4. **One signature moment per page.** Choose a single memorable element: a spatial 3D stage, an orchestrated hero sequence, a tactile diagram, or an editorial photograph. Everything else stays quiet so the signature can be seen.
5. **Precision in the details.** Hairlines align to the grid, numerals use tabular figures in data, optical margins hang punctuation in pull quotes, and icons share one 1.5px stroke. Misaligned details break the effect.
6. **Composed motion.** Motion is choreographed, not sprinkled. Enter sequences follow reading order in a single GSAP timeline, finish within about 1.2 seconds, and never replay on every scroll. See [gsap-orchestration.md](./gsap-orchestration.md).
7. **Honest content.** Real product facts, real imagery or a clearly marked placeholder, and specific copy. Invented statistics, testimonials, and compliance badges destroy trust instantly.
8. **Every state is finished.** Loading, empty, error, hover, focus, and reduced-motion states get the same care as the hero.

## Signature options

| Signature | Use when | Reference |
| --- | --- | --- |
| Spatial 3D stage | The product has a physical, structural, or data metaphor worth exploring | [spatial-3d.md](./spatial-3d.md), `bc_design.py --spatial list` |
| Orchestrated hero sequence | The story unfolds in steps: a reveal, a before/after, a process | [gsap-orchestration.md](./gsap-orchestration.md) |
| Scroll-driven narrative | A long page explains a system or a journey | [gsap-orchestration.md](./gsap-orchestration.md), `--spatial spatial-scrollytelling` |
| Editorial photography | The product is physical, crafted, or place-based | [landing-patterns.md](./landing-patterns.md) |

## Decision order

1. Preserve existing brand evidence and product constraints.
2. Choose the information hierarchy and the one signature moment.
3. Select the house accent from the subject, or map the brand palette onto house roles.
4. Assign typography by role and license availability.
5. Define component shape and motion from function.
6. Verify contrast, keyboard behavior, responsive states, loading, error, and reduced motion, then run `render_check.py` on the rendered page.

## Catalog alignment

The catalogs stay broad so BC Design can cover many products, stacks, and visual references. They are not a license to apply every row automatically. Use [catalog-alignment.md](./catalog-alignment.md) and the shared policy to classify each match as `core`, `compatible`, `conditional`, or `excluded`:

- Automatic recommendations may use only `core` and `compatible` entries.
- `conditional` directions need an explicit user request or approved brand evidence, and still inherit BC accessibility and motion gates.
- `excluded` combinations never bypass quality gates, even when a query names them.

## Failure signals

- A second accent color appears, or the accent fills the largest surface.
- Every content group becomes an identical rounded card.
- Oversized marketing typography displaces useful product content.
- Serif type appears in dense controls or data tables.
- Several competing signature moments fight for attention.
- Motion decorates entry but does not explain state, or replays on every scroll.
- Copy relies on buzzwords, invented numbers, or unearned superlatives.
