# GSAP Orchestration

Use GSAP when motion involves more than one element, depends on scroll, or drives a 3D scene. Single hover or focus feedback stays in CSS with the BC motion tokens. Everything choreographed goes through one GSAP timeline per moment.

GSAP is free under its [standard license](https://gsap.com/standard-license), including ScrollTrigger. BC Design does not bundle it; the consuming project loads it:

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/ScrollTrigger.min.js"></script>
```

With a bundler, install `gsap` and import `gsap` and `ScrollTrigger` from it. In React, use the `@gsap/react` package and its `useGSAP()` hook.

## BC tokens in GSAP

| BC token | CSS value | GSAP value | Use |
| --- | --- | --- | --- |
| `--bc-ease` | `cubic-bezier(0.16, 1, 0.3, 1)` | `"expo.out"` | Default for entrances and reveals |
| `--bc-ease-in-out` | `cubic-bezier(0.4, 0, 0.2, 1)` | `"power2.inOut"` | Overlays, crossfades, camera moves |
| Scroll scrub | n/a | `"none"` | Tweens driven by `scrub` |
| `--bc-duration-fast` | 150ms | `0.15` | Micro feedback |
| `--bc-duration-normal` | 250ms | `0.25` | Component entrance |
| `--bc-duration-slow` | 400ms | `0.4` | Structural moves, drawers, the longest UI tween |
| `--bc-duration-reveal` | 600ms | `0.6` | Once-only hero and section reveals; never above 0.75 |

`expo.out` is exactly `cubic-bezier(0.16, 1, 0.3, 1)`, so CSS and GSAP motion match. Avoid `bounce`, `elastic`, and `back` eases; they break the house calm.

[`assets/motion/bc-motion.js`](../assets/motion/bc-motion.js) exposes these values as `BCMotion.ease`, `BCMotion.duration`, and helpers that apply the rules below. Copy it next to the page, or port it into the project's motion module.

## Choreography rules

1. **One timeline per moment.** A hero entrance, a section reveal, or a 3D camera move is one `gsap.timeline()` with `defaults: { ease: "expo.out" }` and a duration from the token table. Do not fire independent tweens that happen to overlap.
2. **Follow reading order.** Sequence eyebrow, headline, body, action, then media. Overlap steps with the position parameter (`"-=0.25"` or `"<0.08"`) so the sequence feels like one gesture.
3. **Budget the whole sequence.** Tweens that answer an interaction stay at 0.4s or less. Large content that appears once (the hero, a section entering the viewport) may use the reveal tier, 0.5–0.75s, with `expo.out`. An entrance sequence finishes within about 1.4s. Stagger lists at 0.04–0.06s per item and cap the total at 0.3s.
4. **Animate transforms and opacity only.** Use `x`, `y`, `scale`, `rotation`, `autoAlpha`, and `clipPath`. Never tween `width`, `height`, `top`, `left`, `margin`, or `padding`; the audit flags them as `gsap-layout-property`.
5. **Reveal once.** Section reveals use `ScrollTrigger` with `once: true`. Replaying content on every scroll reads as a demo, not a product.
6. **Scrub only for narrative.** Use `scrub: 0.6` with `pin` for a scroll story or a 3D exploded view, and keep the scrubbed section to one or two viewports. The text must stay readable at every scroll position.
7. **Never move streamed content.** A container that receives AI tokens gets no GSAP tween on its geometry while it streams.
8. **Clean up.** Build inside `gsap.context()` or `useGSAP()` and call `revert()` on unmount or route change so tweens and ScrollTriggers do not leak.

## Reduced motion is mandatory

Wrap every choreography in `gsap.matchMedia()`. The audit flags GSAP code without it as `gsap-reduced-motion`.

```js
const mm = gsap.matchMedia();

mm.add(
  {
    motion: "(prefers-reduced-motion: no-preference)",
    reduced: "(prefers-reduced-motion: reduce)",
  },
  (context) => {
    if (context.conditions.reduced) {
      // Show the final state immediately; no tweens, no scrub, no pin.
      gsap.set("[data-reveal]", { autoAlpha: 1, y: 0 });
      return;
    }

    const hero = gsap.timeline({ defaults: { ease: "expo.out", duration: 0.6 } });
    hero
      .from("[data-hero='eyebrow']", { autoAlpha: 0, y: 12 })
      .from("[data-hero='title']", { autoAlpha: 0, y: 24 }, "-=0.45")
      .from("[data-hero='body']", { autoAlpha: 0, y: 16 }, "-=0.45")
      .from("[data-hero='action']", { autoAlpha: 0, y: 12 }, "-=0.45")
      .from("[data-hero='media']", { autoAlpha: 0, scale: 0.98 }, "<");

    gsap.utils.toArray("[data-reveal]").forEach((section) => {
      gsap.from(section, {
        autoAlpha: 0,
        y: 24,
        duration: 0.6,
        ease: "expo.out",
        scrollTrigger: { trigger: section, start: "top 80%", once: true },
      });
    });
  }
);
```

Hide nothing with CSS that only JavaScript can reveal. Set the initial hidden state from GSAP (`from` tweens or `gsap.set`), so the page stays readable when scripts fail.

## Orchestrating a 3D stage

GSAP drives Three.js values the same way it drives DOM values: tween the camera, an object's `position` or `rotation`, or a shader uniform.

```js
const story = gsap.timeline({
  defaults: { ease: "none" },
  scrollTrigger: { trigger: "#stage", start: "top top", end: "+=150%", scrub: 0.6, pin: true },
});
story
  .to(camera.position, { z: 6, y: 0.4 }, 0)
  .to(layers.map((layer) => layer.position), { y: (index) => index * 0.45 }, 0)
  .to(material.uniforms.uGlow, { value: 1 }, 0.5);
```

- Keep one render loop (`requestAnimationFrame` or `gsap.ticker`) and let GSAP only change values.
- Cap the pixel ratio with `Math.min(window.devicePixelRatio, 2)`.
- In the reduced-motion branch, render a single composed frame and skip the scrubbed timeline.
- Pause rendering when the canvas leaves the viewport.
- Read [spatial-3d.md](./spatial-3d.md) for scene composition, lighting, and disposal.

## React

```tsx
import { useRef } from "react";
import gsap from "gsap";
import { useGSAP } from "@gsap/react";

export function Hero() {
  const scope = useRef<HTMLElement>(null);
  useGSAP(() => {
    const mm = gsap.matchMedia();
    mm.add("(prefers-reduced-motion: no-preference)", () => {
      gsap.timeline({ defaults: { ease: "expo.out", duration: 0.4 } })
        .from("[data-hero='title']", { autoAlpha: 0, y: 24 })
        .from("[data-hero='body']", { autoAlpha: 0, y: 16 }, "-=0.25");
    });
  }, { scope });
  return <section ref={scope}>...</section>;
}
```

`useGSAP()` reverts every tween and ScrollTrigger created inside it when the component unmounts.

## Verification

- Run `bc_design.py --audit` on the source; fix `gsap-reduced-motion` and `gsap-layout-property` findings.
- Run `render_check.py` on the page to capture desktop, mobile, and reduced-motion screenshots and to catch console errors and horizontal overflow.
- Scroll the page with reduced motion enabled and confirm every section is visible without animation.

## Worked example

[`assets/motion/gsap-atelier.html`](../assets/motion/gsap-atelier.html) is a complete page: an orchestrated hero timeline, once-only section reveals, and a pinned, scroll-scrubbed 3D exploded view of a watch movement, all with a reduced-motion branch.
