# BC Visual Language

Use this reference after the product subject and existing brand evidence are known. It defines the recognizable BC Design direction without forcing one palette onto every product.

## Direction

- Pair an editorial serif hierarchy with a quiet, highly legible UI sans. Newsreader + Inter is the open-source default; use another licensed pairing when brand evidence supports it.
- Build primarily from warm or true neutrals, high-contrast ink, and hairline separators. Choose one restrained accent family from the subject; terracotta and sage are common options, not mandatory brand colors.
- Let typography, spacing, and composition carry the interface before adding containers. Cards are for real grouping or interaction, not default decoration.
- Prefer small-to-moderate radii, crisp controls, circular icon actions, and simple modal geometry. Pills are reserved for tags, filters, and compact statuses.
- Use sparse organic illustration, tactile diagrams, or product imagery when it explains the subject. Decorative graphics must earn their space.
- Keep motion short and state-driven: subtle opacity/transform feedback for controls, deliberate overlays, and calm loading. Honor reduced motion and keep streamed geometry stable.

## Decision order

1. Preserve existing brand evidence and product constraints.
2. Choose the information hierarchy and signature interaction.
3. Select the neutral base and subject-derived accent.
4. Assign typography by role and license availability.
5. Define component shape and motion from function.
6. Verify contrast, keyboard behavior, responsive states, loading, error, and reduced motion.

## Catalog alignment

The catalogs stay broad so BC Design can cover many products, stacks, and visual references. They are not a license to apply every row automatically. Use [catalog-alignment.md](./catalog-alignment.md) and the shared policy to classify each match as `core`, `compatible`, `conditional`, or `excluded`:

- Automatic recommendations may use only `core` and `compatible` entries.
- `conditional` directions need an explicit user request or approved brand evidence, and still inherit BC accessibility and motion gates.
- `excluded` combinations never bypass quality gates, even when a query names them.

## Failure signals

- The same palette appears across unrelated industries.
- Accent color fills the largest surface without subject evidence.
- Every content group becomes an identical rounded card.
- Oversized marketing typography displaces useful product content.
- Serif type appears in dense controls or data tables.
- Motion decorates entry but does not explain state.
