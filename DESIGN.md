# DESIGN.md - BC Design Visual Direction

> This document defines the visual soul, brand identity, and aesthetic direction for this project.
> It pairs with the Distinctive Review filter to ensure every UI built is authentic, warm, and distinctive, with zero generic AI tropes.

---

## 1. Visual Soul & Brand Identity

* **Aesthetic Philosophy**: Warm, literary, editorial, humanist, and calm. Express the BC Design language through clear hierarchy, practical tokens, and subject-aware choices.
* **Atmosphere**: Editorial, composed, and tactile. It may feel like fine paper in light mode or a calm ink-black workspace in dark mode, but the product subject decides the final material character.
* **Color rule**: Start with a neutral structure and derive one or two accents from product or brand evidence. White, near-white, parchment, and warm black are all valid canvases when contrast and hierarchy hold. Avoid defaulting unrelated products to the same terracotta, sage, blue, or gradient palette.

---

## 2. Reference Palette Tokens

This is the canonical BC reference theme, not a mandatory palette. Rename and remap semantic values from the approved brand contract before implementation.

```css
:root {
  /* Canvas & Elevation */
  --bc-bg: #FAF9F5;                  /* Warm fine-book parchment */
  --bc-bg-subtle: #F4F3EE;           /* Inset wells & secondary containers */
  --bc-surface: #FFFFFF;             /* Elevated cards & dialogs */
  
  /* Brand Accent */
  --bc-accent: #D97757;              /* Signature Terracotta */
  --bc-accent-hover: #C15F3E;        /* Deep Terracotta */
  --bc-accent-active: #AA4F32;       /* Active state */
  --bc-accent-subtle: #FDF3EE;       /* Warm tint for badges */
  
  /* Modal CTAs */
  --bc-cta-dark: #FFFFFF;            /* Solid Crisp White in dark mode modals */
  --bc-glass: rgba(255, 255, 255, 0.09); /* Secondary glass button */

  /* Ink & Typography */
  --bc-text-primary: #1F1E1B;        /* Deep warm printer's ink */
  --bc-text-secondary: #6B6760;      /* Muted stone */
  --bc-text-tertiary: #99948B;       /* Placeholders */
  
  /* Borders & Dividers */
  --bc-border: rgba(31, 30, 27, 0.08); /* 1px delicate hairline */
  --bc-border-strong: rgba(31, 30, 27, 0.16);
  --bc-ring: 0 0 0 2px rgba(217, 119, 87, 0.28);
}

[data-theme="dark"] {
  --bc-bg: #181816;                  /* Espresso soot */
  --bc-bg-subtle: #20201D;           /* Inset wells */
  --bc-surface: #242421;             /* Elevated panels */
  --bc-accent: #E28466;              /* Warm Terracotta Glow */
  --bc-text-primary: #FAF9F5;        /* Off-white parchment */
  --bc-text-secondary: #A39E93;      /* Muted taupe */
  --bc-border: rgba(250, 249, 245, 0.09);
  --bc-border-strong: rgba(250, 249, 245, 0.18);
}
```

---

## 3. Typography Hierarchy

* **Editorial Headings (`font-serif`)**:
  * Stack: `"Newsreader", "Georgia", serif`
  * Role: Use Newsreader for editorial hierarchy, with Georgia as a reliable fallback.
  * Optical sizing: `font-optical-sizing: auto; font-variation-settings: "opsz" 72;`
  * Weight: `500` (Medium), letter-spacing: `-0.02em`.
* **Interface & Body (`font-sans`)**:
  * Stack: `"Inter", -apple-system, sans-serif`
  * Clean, neutral, high-legibility. `line-height: 1.55`.
* **Code & Tabular Numbers (`font-mono`)**:
  * Stack: `"JetBrains Mono", "Fira Code", monospace`.
* **Google Fonts Drop-In**:
  ```html
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Newsreader:ital,opsz,wght@0,6..72,400..600;1,6..72,400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  ```

---

## 4. Motion & Animation Signature

* **Core Deceleration Curve**: `cubic-bezier(0.16, 1, 0.3, 1)`.
* **Speed Budget**:
  * Micro-interactions (buttons, switches): `150ms`
  * Cards & Popovers: `250ms`
  * Drawers & Modals: `350ms - 400ms`
  * AI Thinking Pulse: `1800ms` continuous ambient glow
* **Streaming Isolation Rule**: NEVER animate container dimensions while AI text streams.

---

## 5. Visual Geometry & Tactile Assets

* **Border Radius**:
  * Buttons & Inputs: `8px - 10px` (`rounded-lg`). **Avoid full pill capsules for main action CTAs.**
  * Cards & Prompt Box: `16px - 18px` (`rounded-2xl`).
* **Icons**:
  * Monoline 1.5px stroke width (`lucide-react` with `strokeWidth={1.5}`). Never use emojis as interactive icons.
* **Organic illustration**:
  * Use sparse hand-drawn forms, diagrams, or product imagery only when they reinforce the subject or explain an interaction. Derive their color from the active accent.
* **Product chrome**:
  * Reproduce recognizable window or device chrome only when the content is demonstrating that environment; do not use it as decorative filler.

---

## 6. Header & Navigation Architecture (Zero-Wrap Standard)

To prevent visual crowding and clumsy text-wrapping in navigation bars:

* **The 3-Zone Header Standard**:
  * **Left Zone (Identity & Context)**: Brand logo (`Newsreader` serif) + 1px vertical hairline divider + Entity/Project dropdown. Single line.
  * **Center Zone (Global Command Search)**: Dedicated horizontal search input (`280px`–`440px` width, `36px` height) with search icon and keyboard shortcut badge (`<kbd>⌘K</kbd>`).
  * **Right Zone (Status, Utility & Profile)**: Compact status indicator (e.g. green pulsing dot + `Ledger Balanced`), Theme Toggle button (`34px` height), and circular user avatar (`34px`).
* **Zero Text Wrapping Rule**:
  * Every single interactive element inside the header MUST have `white-space: nowrap !important;`.
  * Never allow button labels, badge text, or dropdowns to break onto 2–3 awkward lines.
* **Uniform Control Height**:
  * All interactive elements in the top header (inputs, selects, buttons, avatars) MUST share an identical height (`34px`–`36px`) and `align-items: center`.
* **Announcement Separation**:
  * Long, multi-sentence status announcements (e.g. *"Q3 Fiscal Close in 4d • 99.98% Automated Reconciliation"*) MUST NOT be squeezed into the top navigation row. Place them in a dedicated sub-header notification strip (`.fiscal-notice-strip`) with full horizontal breathing space.


---

## 7. Liveliness Dials (Distinctive Quality Alignment)

* **ENERGY: 6/10** (Warm, human, confident, literary authority without chaotic noise).
* **RHYTHM: 6/10** (Varied visual hierarchy, open editorial breathing room, breaking the SaaS-card monotony).
* **MOTION: 5/10** (Intentional decelerated interactions; zero non-functional parallax or distracting hover fluff).
