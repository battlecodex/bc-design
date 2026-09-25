---
name: bc-motion
description: Use when designing or implementing interface animation, transitions, loading states, overlays, page motion, or streamed AI feedback.
---

# BC Motion

Use this skill when motion is part of the interface contract. Motion should explain state, preserve spatial continuity, and respect cognitive and accessibility limits.

## Workflow

1. Name the state or spatial relationship the motion communicates.
2. Choose a tier: micro 150ms, component 250ms, structural 350–400ms, reveal 500–750ms (`--bc-duration-reveal`, once-only hero and section entrances), or approved thinking 1800ms.
3. Pick the engine: CSS transitions on BC tokens for single-element feedback; a GSAP timeline for anything that sequences several elements, follows scroll, or drives a 3D scene.
4. Use a semantic BC easing token (`expo.out` in GSAP); avoid browser-default easing keywords.
5. Prefer opacity and transform; never animate width, height, margin, or padding of a container receiving streamed tokens.
6. Add a `prefers-reduced-motion: reduce` fallback in the same source unit. For GSAP, wrap the choreography in `gsap.matchMedia()`; for 3D scenes, pause continuous rotation and present a calm static view.
7. Check interruption, focus, loading, off-screen, and failure states. Content must stay readable when scripts fail.
8. Run `bc_design.py --audit TARGET`, then `render_check.py PAGE` for normal and reduced-motion screenshots, and report any unrendered motion state.

## Non-negotiables

- Decorative motion must not compete with the product's signature moment.
- Infinite motion is reserved for active status or loading feedback and must have a readable static fallback.
- 3D spatial camera interaction must use smooth inertia damping (friction factor <= 0.08) and never snap abruptly.
- Do not use motion to hide layout instability or missing content.
- Keep easing and duration on tokens so a theme can change motion coherently.
- One timeline per moment; an entrance sequence finishes within about 1.4s, and section reveals play once.
- The reveal tier never answers a click, hover, or keystroke; interaction feedback stays at 250ms or less.
- Exits are faster than entrances (about two thirds of the entrance duration) and leave in the direction the user dismissed them.

## References

- Shared foundation: `../bc-design/SKILL.md`
- Canonical tokens: `../bc-design/references/tokens.css`
- Motion guide: `../bc-design/references/animations.md`
- GSAP orchestration: `../bc-design/references/gsap-orchestration.md`
- GSAP helpers: `../bc-design/assets/motion/bc-motion.js`
- Worked example with a 3D stage: `../bc-design/assets/motion/gsap-atelier.html`
- UX motion and reduced-motion rules: `../bc-design/references/ux-guidelines.md`
