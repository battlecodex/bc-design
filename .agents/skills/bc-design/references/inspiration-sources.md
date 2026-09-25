# Inspiration Sources

Asking an agent to invent a frontend from nothing produces the average of its training data. Real references produce better work. This directory lists places to find them, grouped by the part of the page you are designing.

## How to use a reference

1. **A person picks the reference.** Browse a gallery and choose one or two real product sites whose structure fits the brief. Galleries are for people; an agent reading a gallery page learns only how the gallery itself is built.
2. **Study the original site, not the gallery.** Run `study.py` on the product's own URL (see [project-memory.md](./project-memory.md) § Study). `study.py` refuses gallery and showcase hosts for this reason and tells you to follow the link to the original.
3. **Take structure and tokens, never assets.** Keep the layout idea, rhythm, type scale, and motion stance. Do not copy artwork, logos, photography, copy, or proprietary fonts.
4. **Map it onto the house style.** Translate what you learned into BC tokens and composition patterns, then run the audit and `render_check.py`.

Sites and their terms change. The links below were collected in September 2026; check a site's terms before relying on anything you download from it.

## Page sections

| Designing | Where to look |
| --- | --- |
| Navigation bars | [navbar.gallery](https://navbar.gallery) |
| Hero sections | [supahero.io](https://supahero.io) |
| Calls to action | [cta.gallery](https://cta.gallery) |
| Footers | [footer.design](https://footer.design) |
| 404 pages | [404s.design](https://404s.design) |
| Page sections in general | [unsection.com](https://unsection.com) |
| Bento and grid layouts | [bentogrids.com](https://bentogrids.com), [gridddy.framer.website](https://gridddy.framer.website) |
| Buttons | [simply-buttons.vercel.app](https://simply-buttons.vercel.app) |

Bento grids are a common AI default. Use one only when the content really is a set of unequal, independent tiles, and vary the cells (see the audit's `monotonous-card-kit` rule).

## Whole sites and product UI

| Looking for | Where to look |
| --- | --- |
| SaaS marketing sites | [saaspo.com](https://saaspo.com), [saasframe.io](https://saasframe.io) |
| Landing pages | [landing.love](https://landing.love), [landdding.com](https://landdding.com) |
| One-page sites | [onepagelove.com](https://onepagelove.com) |
| Product UI styles | [styles.refero.design](https://styles.refero.design) |
| Curated and recent web design | [godly.design](https://godly.design), [curated.design](https://curated.design), [recent.design](https://recent.design), [webinspoo.com](https://webinspoo.com) |
| Rebrands | [rebrand.gallery](https://rebrand.gallery) |
| Logos (for inspiration, never reuse) | [logotouse.com](https://logotouse.com) |
| 3D websites | [mesh3d.gallery](https://mesh3d.gallery) |

## Motion

| Looking for | Where to look |
| --- | --- |
| Web animation references | [60fps.design](https://60fps.design), [animos.app](https://animos.app) |
| Microinteractions | [designspells.com](https://designspells.com) |
| Animation prompt ideas | [motionin.design](https://motionin.design) |
| CSS transition recipes | [transitions.dev](https://transitions.dev): use in your product only; its terms forbid repackaging the collection, so BC Design keeps only its own written principles |

Translate any reference into the BC motion tiers and the GSAP rules in [gsap-orchestration.md](./gsap-orchestration.md); a reference is a direction, not a duration.

## Assets

| Need | Where to look | Before using |
| --- | --- | --- |
| Icons | [Keyline Icons](https://github.com/keyline-icons/keyline-icons) (MIT, no attribution), Lucide, Phosphor | Follow [icons.md](./icons.md): one family per interface, 1.5px stroke |
| Backgrounds | [backgrounds.supply](https://backgrounds.supply) | Check each item's license; keep backgrounds behind content, never behind body text without a contrast check |
| Design resources | [kage.design](https://kage.design) | Check each item's license |

## Component libraries

Ready-made components are covered in [third-party-components.md](./third-party-components.md), including the license check and restyle each one needs before it ships.

## Not design references

Presentation galleries, coding courses, AI site builders, and document tools can be useful elsewhere, but they do not inform interface design in this skill.
