# Third-Party Component Libraries

Copy-paste component libraries save time, and many ship exactly the effects this skill audits against: glow borders, gradient text, spotlight cards, uniform bento grids, and animated backgrounds behind body copy. Treat every third-party component as a draft that must earn its place in the house style.

## The house style on modern components

BC Design's warm editorial language is meant to run on current component libraries, not on hand-rolled markup. For React projects the default base is **shadcn/ui** (Radix primitives with Tailwind), themed with [`assets/components/shadcn-bc-theme.css`](../assets/components/shadcn-bc-theme.css). That file maps every shadcn variable onto the house palette: parchment canvas, ink primary actions, hairline borders, a terracotta focus ring, and the illustration palette for charts. When the project has a brand color, set `--primary` to its strong variant and `--ring` to the brand color (`project.py accent HEX` prints both). Blocks from registries built on shadcn (shadcnblocks, ReUI, Evil Charts, and others) inherit the same look.

## Brainstorm, choose, and apply

For every component in scope, weigh the options and pick the best one. Run:

```bash
python .agents/skills/bc-design/scripts/components.py hero pricing chart navbar
python .agents/skills/bc-design/scripts/components.py --all
```

It tailors three options per component to what the project already has:

- **A. Keep and restyle** the project's own implementation, when one exists.
- **B. Installed base:** a primitive from the component library the project already uses (reported by pre-flight), or the shadcn/ui primitive that would be added.
- **C. New library:** candidate blocks (shadcnblocks, ReUI, Spectrum UI, coss ui, 21st.dev) and effects (React Bits, Rare UI, Vanta UI) that would modernize it.

Record the choice as a short table per component, with the reason, and include it in the handoff, for example:

| Component | Option | Recommendation |
| --- | --- | --- |
| Hero | A: restyle `src/sections/Hero.tsx`; C: a shadcnblocks hero block; C: a React Bits text reveal as the signature | Restyle A and add the text reveal rebuilt on GSAP, because the layout already works |

Rules:

- **Apply the best option on an explicit request.** When the user asked to build, redesign, or restyle, use the recommended option directly: restyling the project's components, adding primitives of a library the project already uses (for example `npx shadcn@latest add tabs`), or pasting copy-paste code from a registry that brings no new package.
- **Ask once before adding a package or a paid item.** A new dependency in `package.json`, a new UI or animation library, or a paid (Pro) block needs a yes first. Ask these together at the end and finish everything else meanwhile.
- **Name the alternatives in the handoff.** One recommendation per component, with at most two alternatives the user can switch to.
- **Confirm before adopting.** Library contents change; open the candidate, confirm it exists and fits, and read its license before using it.
- **Prefer working components.** In a redesign, restyling a component that already works usually beats replacing it; replace it when the upgrade is clearly better, and say why.

Every adopted component goes through the checklist below.

## Before a component ships

1. **Check the license of that component.** Libraries mix free and paid items, and some free items carry their own terms. Record the source URL and license in the component file header or the project's notices. Never paste a paid (Pro) component the user has not licensed.
2. **Check that it solves a real need.** Prefer the project's existing components and plain semantic HTML. A dependency or a visual effect needs a reason in the design contract.
3. **Restyle it to BC tokens.** Replace raw colors, radii, shadows, fonts, and durations with `--bc-*` tokens. Remove glows, neon, gradient text, and decorative motion that does not explain state.
4. **Make it accessible.** Keyboard operation, a visible 2px focus ring, accessible names, and a `prefers-reduced-motion` path (a `gsap.matchMedia` branch for GSAP code).
5. **Verify it.** Run `bc_design.py --audit` on the component and `render_check.py` on a page that uses it. Run `prune.py` afterwards to catch packages and styles the import left behind.

## Libraries and how they fit

| Library | What it offers | Fit with the house style |
| --- | --- | --- |
| [shadcn/ui](https://ui.shadcn.com) and blocks built on it: [shadcnblocks](https://shadcnblocks.com), [ReUI](https://reui.io), [Spectrum UI](https://ui.spectrumhq.in), [coss ui](https://coss.com/ui) | Accessible primitives and page blocks for React and Tailwind | Good base. Map its CSS variables onto BC tokens; shadcnblocks includes paid blocks |
| [21st.dev](https://21st.dev) | Community components from many authors | Quality and license vary by component; review each one |
| [Evil Charts](https://evilcharts.com) | Chart components | Use for data views; follow the chart guidance in `charts.md` and keep colors on tokens |
| [React Bits](https://reactbits.dev), [Rare UI](https://rareui.com), [BeUI](https://beui.dev), [Easy UI](https://easyui.site), [Vanta UI](https://vantaui.com) | Animated and decorative components and templates | Use sparingly. Most effects are the kind of motion the audit flags; keep at most one, as the page's signature moment, and rebuild its motion on GSAP tokens |
| [8bitcn](https://8bitcn.com) | Retro pixel-art components | A deliberate theme, not the house style; use only when the brand calls for it |
| [Simply Buttons](https://simply-buttons.vercel.app) | Button styles | Inspiration only; buttons follow the CTA voice (brand or ink primary, outline secondary) |
| [Keyline Icons](https://github.com/keyline-icons/keyline-icons) | MIT icon set in four styles | See [icons.md](./icons.md) |

## Red flags that mean restyle or reject

- Text over an animated or gradient background without a measured contrast pair.
- Gradient or rainbow text, glow shadows, spotlight or aurora effects used as decoration.
- Infinite motion with no pause, or motion without a reduced-motion path.
- A component that pulls a large dependency (a whole animation or 3D runtime) for a small effect.
- Placeholder content such as fake logos, testimonials, or statistics left in the markup.
