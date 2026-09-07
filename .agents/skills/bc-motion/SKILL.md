---
name: bc-motion
description: Use when designing or implementing interface animation, transitions, loading states, overlays, page motion, or streamed AI feedback.
---

# BC Motion

Use this skill when motion is part of the interface contract. Motion should explain state, preserve spatial continuity, and respect cognitive and accessibility limits.

## Workflow

1. Name the state or spatial relationship the motion communicates.
2. Choose a tier: micro 150ms, component 250ms, structural 350–400ms, or approved thinking 1800ms.
3. Use a semantic BC easing token; avoid browser-default easing keywords.
4. Prefer opacity and transform; never animate width, height, margin, or padding of a container receiving streamed tokens.
5. Add a `prefers-reduced-motion: reduce` fallback in the same source unit.
6. Check interruption, focus, loading, off-screen, and failure states.
7. Run `bc_design.py --audit TARGET` and report any unrendered motion state.

## Non-negotiables

- Decorative motion must not compete with the product's signature moment.
- Infinite motion is reserved for active status or loading feedback and must have a readable static fallback.
- Do not use motion to hide layout instability or missing content.
- Keep easing and duration on tokens so a theme can change motion coherently.

## References

- Shared foundation: `../bc-design/SKILL.md`
- Canonical tokens: `../bc-design/references/tokens.css`
- Motion guide: `../bc-design/references/animations.md`
- UX motion and reduced-motion rules: `../bc-design/references/ux-guidelines.md`
