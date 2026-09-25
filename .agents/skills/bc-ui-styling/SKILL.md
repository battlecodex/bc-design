---
name: bc-ui-styling
description: Use when implementing or restyling an interface's visual layer while preserving its routes, data contracts, interaction semantics, and approved behavior.
---

# BC UI Styling

Use this skill for implementation work after the direction and invariants are clear. It turns the contract into responsive, accessible code without silently redesigning product behavior.

## Workflow

1. Detect the actual stack from project files; never assume React or Tailwind.
2. Inventory routes, components, content hierarchy, tokens, and preserved behavior. Run `python ../bc-design/scripts/project.py preflight` to see which component library the project already installs.
3. Brainstorm component sources with `python ../bc-design/scripts/components.py <components>`: keep and restyle, the installed library's primitive, or an upgrade from a newer library. Offer one recommendation per component and ask whether to switch; install nothing before the user approves. On shadcn/ui, apply `../bc-design/assets/components/shadcn-bc-theme.css`.
4. Apply shared tokens and typography before one-off selectors.
5. Implement responsive structure at 375px, 768px, 1024px, and 1440px.
6. Cover default, hover, active, focus-visible, disabled, loading, empty, and error states.
7. Verify keyboard order, touch targets, contrast, wrapping, reduced motion, and streamed content stability.
8. Run the BC source audit and report rendered states that were not observed.

## Non-negotiables

- Do not change routes, data, navigation, or semantics during a restyle without approval.
- Keep interface copy active and meaningful; remove decorative arrow suffixes and filler metadata.
- Use purposeful 1.5px monoline SVG icons with accessible names.
- Use motion tokens and avoid layout-property animation for streamed output.
- Keep fallbacks explicit when a font, image, or browser feature is unavailable.
- For 3D spatial canvas backgrounds, enforce `pointer-events: none` and place interactive typography in a dedicated column (`z-index: 10` above canvas `z-index: 0/1`) to guarantee zero text overlap.

## References

- Shared foundation: `../bc-design/SKILL.md`
- Stack notes: `../bc-design/stacks/`
- Component guidance: `../bc-design/references/components.md`
- Third-party component libraries and the reuse order: `../bc-design/references/third-party-components.md`
- Icons, including Keyline Icons: `../bc-design/references/icons.md`
- Motion guidance: `../bc-motion/SKILL.md`
