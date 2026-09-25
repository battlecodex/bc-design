# Design Dimensions

Every BC Design review, design contract, and handoff covers the same eighteen dimensions: twelve for the interface (UI) and six for the experience (UX). A dimension is either verified with evidence, marked as needing work, or explicitly marked not verified. None is skipped silently.

How each dimension is verified:

- **Audit**: `bc_design.py --audit TARGET` reports it automatically; the rule IDs are listed.
- **Render**: `render_check.py PAGE` reports it or captures the screenshots needed to judge it.
- **Review**: a person or agent judges it from the screenshots, the source, and the brief.

## UI dimensions

| Dimension | What it governs | BC house standard | Verified by |
| --- | --- | --- | --- |
| **Color** | Primary accent, canvas, text, borders, success and error states | Parchment canvas `#FAF9F5`, ink text, hairline borders. One UI accent for actions, links, and focus; text-bearing accent fills use `--bc-accent-strong`. Illustrations may use the muted illustration palette. Status colors never carry meaning alone. | Audit: `generic-gradient-wash`, `accent-surface-domination`, `accent-button-text-contrast`. Review: contrast of every text pair with `bc_design.py --contrast`. |
| **Typography** | Typeface, size, weight, line height, legibility | Serif display (Newsreader, light 300–400 at large sizes) for headings; sans (Inter) for UI and body; at most five sizes. Body 15–17px in product UI, 17–19px for reading; lead text about 22px in secondary ink; line height 1.5–1.65 for body. | Review: screenshots at every width. Audit: `oversized-hero-displacement`. |
| **Layout & grid** | Content arrangement, columns, sidebar position, page width | 12-column grid with a 1160–1200px content width, 24px gutters on mobile. Asymmetric splits (7/5, 5/7) over identical thirds. Sidebars stay on the leading edge in product UI. | Render: `render-horizontal-overflow`. Review: screenshots. |
| **Spacing & whitespace** | Distance between elements | 4px base scale. Major sections 96–128px apart on desktop, 64–72px on mobile. Related items sit closer than unrelated ones. | Review: screenshots. |
| **Visual hierarchy** | What is seen first, what leads, what supports | One primary focal point per view, one primary action per section, and a clear order of headline, support, and action. Weight and ink contrast before size. | Audit: `decorative-eyebrow-overload`, `monotonous-card-kit`, `decorative-index-marker`. Review: squint test on screenshots. |
| **Imagery & icons** | Photography, illustration, icons, and a consistent style | Real product screens or hand-drawn monoline illustration on flat muted tiles. Icons are 1.5px monoline from one family. Every informative image has alt text. | Audit: `unicode-icon-glyph`, `template-arrow-glyph`. Render: `render-image-alt`. |
| **Shape & effects** | Corner radius, borders, shadow, depth | Radius 4px for small controls, 8px for buttons and inputs, 12px for cards, 16px for large panels. Hairline borders first; soft shadow only for floating layers (menus, popovers, toasts). No glow, no neon, no glassmorphism by default. | Audit: `excessive-pill-capsules`. Review: screenshots. |
| **UI components** | Buttons, forms, cards, menus, tabs, modals, tables | Primary button in solid ink, secondary in outline, tertiary as a text link. Inputs with visible labels. Cards only for real grouping. Tables with tabular figures and left-aligned text. | Review: component inventory against `components.md`. Audit: `repeated-generic-cta`. |
| **Interaction & states** | Hover, focus, active, loading, empty, error, success | Every interactive element has hover, focus-visible, active, and disabled states. Every data view has loading, empty, and error states. Success is confirmed in words. | Audit: `focus-ring-width`, `focus-outline-removed`. Review: state inventory. |
| **Motion** | Transitions and movement that explain change | CSS on BC tokens for feedback; GSAP timelines for sequences, scroll, and 3D. Explains state, never decorates. Reduced motion always supported. | Audit: `motion-duration-budget`, `motion-easing-token`, `reduced-motion-support`, `streaming-layout-animation`, `gsap-reduced-motion`, `gsap-layout-property`. Render: reduced-motion screenshots. |
| **Responsiveness** | Phone, tablet, and desktop adaptation | Designed at 375, 768, 1024, and 1440px. Stacks below 860px, touch targets at least 44px, no horizontal scroll, and pinned or scrubbed motion only on wide screens. | Render: screenshots at each width, `render-horizontal-overflow`. |
| **Accessibility** | Readable contrast, keyboard navigation, screen-reader support | WCAG AA contrast (4.5:1 text, 3:1 large text and UI parts), full keyboard path with a visible 2px focus ring, semantic landmarks and headings, accessible names on every control, a skip link. | Audit: `focus-ring-width`, `focus-outline-removed`, `accent-button-text-contrast`. Render: `render-unnamed-control`, `render-image-alt`. Review: keyboard walk-through. |

## UX dimensions

| Dimension | Question it answers | BC practice | Verified by |
| --- | --- | --- | --- |
| **User research** | Who uses this, and what do they need? | Name the primary user, their goal, and their context in the brief. When research is missing, write the assumptions down and label them as assumptions. | Review: the brief states users, goals, and assumptions. |
| **Information architecture** | How is content grouped and found? | Group content by the user's task, not the org chart. Navigation labels use the user's words; no more than seven top-level items; every link has a real destination. | Audit: `dead-navigation-link`. Review: navigation and content inventory. |
| **User flow** | What steps take the user from entry to done? | Map the main flow step by step before designing screens. Remove steps that do not move the user forward, and show progress in multi-step flows. | Review: a written flow for each primary task. |
| **Wireframe & prototype** | Is the structure right before it is styled? | Agree on structure with a low-fidelity layout first, then build a single-file prototype (see [web-artifacts.md](./web-artifacts.md)) to test the flow before production code. | Review: the approved structure exists before visual polish. |
| **UX writing** | Are labels, instructions, and errors clear? | Active verbs on buttons that name the outcome ("Book a visit", not "Submit"). Errors say what happened and how to fix it. No buzzwords, invented numbers, or em-dash asides. | Audit: `repeated-generic-cta`, `template-arrow-cta`, `em-dash-copy`, `buzzword-copy`, `unverified-claim`, `middle-dot-metadata`. |
| **Usability testing** | Can people use it without confusion? | Write three to five realistic tasks, watch five people (or run the tasks yourself on the prototype), and record where they hesitate or fail. Fix the top issues before visual refinement. | Review: task list and observed results in the verification report. |

## UI versus UX in one example

For a checkout button, the color, type, and shape are UI decisions. How easily the button is found, how clearly the total is shown, and how smoothly payment completes are UX decisions. A design system keeps the UI decisions consistent; this reference makes sure the UX decisions are checked too.

## Review scorecard

Use this template in every audit, design contract, and verification report. Status is `pass`, `needs work`, or `not verified`.

```text
UI
  Color .................. status | evidence
  Typography ............. status | evidence
  Layout & grid .......... status | evidence
  Spacing & whitespace ... status | evidence
  Visual hierarchy ....... status | evidence
  Imagery & icons ........ status | evidence
  Shape & effects ........ status | evidence
  UI components .......... status | evidence
  Interaction & states ... status | evidence
  Motion ................. status | evidence
  Responsiveness ......... status | evidence
  Accessibility .......... status | evidence
UX
  User research .......... status | evidence
  Information architecture status | evidence
  User flow .............. status | evidence
  Wireframe & prototype .. status | evidence
  UX writing ............. status | evidence
  Usability testing ...... status | evidence
```

`bc_design.py --audit TARGET --json` groups its findings by these dimensions under `summary.by_dimension`, so the automatic part of the scorecard fills itself in.
