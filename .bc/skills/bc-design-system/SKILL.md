---
name: bc-design-system
description: Use when creating or refactoring design tokens, component contracts, states, variants, themes, or design-system governance for a product interface.
---

# BC Design System

Use this skill when a visual decision must become a reusable, testable system. Keep primitive values separate from semantic roles and component decisions.

## Workflow

1. Read the approved brand contract or state that one is missing.
2. Define primitive tokens for color, type, spacing, radius, elevation, layer, and motion.
3. Map primitives to semantic roles such as canvas, surface, text, accent, focus, status, and motion.
4. Specify component anatomy, variants, interaction states, disabled/loading/error behavior, and responsive constraints.
5. Validate contrast, focus, touch targets, reduced motion, streamed geometry, and theme parity.
6. Provide migration guidance from raw values and document intentional exceptions.

## Non-negotiables

- Prefer semantic tokens over raw values inside components.
- Do not create a token only to preserve a decorative effect.
- Keep light and dark themes structurally equivalent and contrast-safe.
- Use the canonical motion tokens and never animate streamed container dimensions.
- A component is incomplete until its keyboard, loading, empty, error, and reduced-motion states are described.

## References

- Shared foundation: `../bc-design/SKILL.md`
- Canonical tokens: `../bc-design/references/tokens.css`
- Component contracts: `../bc-design/references/components.md`
- UX quality gates: `../bc-design/references/ux-guidelines.md`
