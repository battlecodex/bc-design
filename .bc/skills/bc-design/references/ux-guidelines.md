# BC Design System - UX Guidelines & Quality Control

A comprehensive reference for **UX principles, accessibility (A11y), animation timing budgets, z-index architecture, loading states, and anti-patterns** tailored specifically for the BC Design / BC Design aesthetic.

---

## 1. Quick-Check UX Rules by Priority

| Priority | Category | Impact | Golden Rule (Must-Have) | Anti-Pattern (Never Do) |
| :--- | :--- | :--- | :--- | :--- |
| **1** | **Accessibility (A11y)** | CRITICAL | WCAG AA 4.5:1 min contrast, 2px focus ring, `aria-live="polite"` for streaming | Removing `:focus` outlines; Icon buttons without `aria-label` |
| **2** | **Animation Budget** | CRITICAL | `--bc-ease: cubic-bezier(0.16, 1, 0.3, 1)`, 150-250ms max | Animating width/height during AI streaming; Linear 500ms+ transitions |
| **3** | **Z-Index System** | HIGH | Strict 7-tier scale (`--z-toast: 70`, `--z-modal: 50`) | Arbitrary `z-9999` or competing stack orders |
| **4** | **Touch & Target** | HIGH | Min 44×44px hit targets for interactive controls, 8px spacing | Tiny 20px clickable text buttons on mobile |
| **5** | **Loading & Skeletons** | HIGH | Terracotta thinking pulse or warm parchment shimmer | Harsh blue spin circles or layout-shifting content pops |
| **6** | **Forms & Inputs** | MEDIUM | Visible persistent labels, inline error messages near input | Placeholder-only labels that disappear on typing |
| **7** | **Typography Contrast**| MEDIUM | Base 15px body, line-height 1.55, optical sizing on serifs | Gray text below 12px or low-contrast gray-on-gray |
| **8** | **Performance** | HIGH | Preload Newsreader/Inter, reserve card space to avoid CLS | Cumulative layout shifts when artifact drawers mount |

---

## 2. Animation & Motion Rules

BC Design's motion is **calm, intelligent, and natural**—it feels like pages turning in a fine hardcover book rather than bouncy cartoons.

### The Speed Budget
* **Micro-interactions (Buttons, Toggles, Tooltips)**: `150ms` using `--bc-ease`.
* **Card Reveals & Dropdowns**: `250ms` using `--bc-ease`.
* **Drawers & Modal Dialogs**: `350ms - 400ms` using `--bc-ease`.
* **AI Thinking State**: `1800ms` smooth continuous pulse.

### The Golden Streaming Isolation Rule
> **CRITICAL**: Never animate the width, height, or padding of a container that contains actively streaming AI text tokens! Animating container dimensions while tokens stream triggers catastrophic browser reflows (layout thrashing) and feels jittery. Keep container dimensions stable and append text smoothly.

### Reduced Motion Support
Always respect user accessibility preferences:

```css
@media (prefers-reduced-motion: reduce) {
  *, ::before, ::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

---

## 3. Accessibility (A11y) Standards

### Color Contrast Ratios
* **Parchment Light Mode (`#FAF9F5`)**:
  * Heading / Primary Text (`#1F1E1B`): **15.82:1** (Exceeds WCAG AAA).
  * Body Secondary Text (`#6B6760`): **5.34:1** (Exceeds WCAG AA).
  * Terracotta Accent (`#D97757`): **2.96:1** against parchment; do not use it for normal text.
  * Primary Action CTA (`.bc-btn-contrast` `#1F1E1B` with `#FFFFFF` text): **15.82:1** (canonical high-contrast standard).
  * Accent Terracotta Button Text (`#FFFFFF` on `#D97757`): **3.12:1** (Meets WCAG AA for bold CTA text >= 14px bold; hover `#C15F3E` reaches **4.22:1**). Avoid dark ink text on mid-tone accent buttons to prevent chromatic clash.
* **Espresso Soot Dark Mode (`#181816`)**:
  * Heading / Primary Text (`#FAF9F5`): **16.88:1** (Exceeds WCAG AAA).
  * Body Secondary Text (`#A39E93`): **6.66:1** (Exceeds WCAG AA).
  * Primary Action Button (`#FFFFFF` on `#181816`): **16.88:1** (Crisp high-contrast).

### Focus Rings
Never strip focus rings without a high-visibility accessible replacement:

```css
:focus-visible {
  outline: none;
  box-shadow: 0 0 0 2px var(--bc-bg), 0 0 0 4px var(--bc-accent) !important;
}
```

### Screen Reader Live Regions for AI Output
When rendering streamed markdown tokens, mark the output region so assistive technology knows text is arriving:

```html
<div class="bc-response-stream" aria-live="polite" aria-atomic="false">
  <!-- Streamed text tokens enter here -->
</div>
```

---

## 4. Z-Index Architectural Scale

Never guess z-index numbers or use `z-[9999]`. Adhere strictly to this semantic scale:

```css
:root {
  --z-base: 0;
  --z-card-hover: 10;
  --z-dropdown: 20;
  --z-sticky-nav: 30;
  --z-artifact-drawer: 40;
  --z-modal-backdrop: 50;
  --z-modal-content: 51;
  --z-popover: 60;
  --z-toast-notification: 70;
  --z-tooltip: 80;
}
```

---

## 5. Loading States & Shimmer Skeletons

Avoid cold industrial circular spinners or blue loading bars. BC Design uses two organic loading paradigms:

### A. The BC Design Thinking Pulse
For AI reasoning, search, or document parsing:

```css
@keyframes bcThinkingPulse {
  0% {
    opacity: 0.45;
    box-shadow: 0 0 0 0 rgba(217, 119, 87, 0.4);
  }
  50% {
    opacity: 1;
    box-shadow: 0 0 16px 2px rgba(217, 119, 87, 0.3);
  }
  100% {
    opacity: 0.45;
    box-shadow: 0 0 0 0 rgba(217, 119, 87, 0.4);
  }
}

.bc-thinking-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: var(--bc-accent-subtle);
  color: var(--bc-accent);
  padding: 4px 12px;
  border-radius: 9999px;
  animation: bcThinkingPulse 1.8s infinite var(--bc-ease);
}
```

### B. Warm Parchment Skeleton Shimmer
For initial card loads:

```css
@keyframes bcBoneShimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

.bc-skeleton {
  background: linear-gradient(
    90deg,
    rgba(31, 30, 27, 0.05) 25%,
    rgba(31, 30, 27, 0.10) 50%,
    rgba(31, 30, 27, 0.05) 75%
  );
  background-size: 200% 100%;
  animation: bcBoneShimmer var(--bc-duration-shimmer) infinite var(--bc-ease-in-out);
  border-radius: 6px;
}
```

---

## 6. Form Ergonomics & Validation

1. **Persistent Labels**: Never rely solely on placeholder text; inputs must display a persistent label above the field or floating label.
2. **Tactile Switches**: BC Design toggle switches use a smooth 24px capsule track with an inset 18px thumb that glides with `--bc-ease` (150ms).
3. **Inline Validation**: Errors should appear directly beneath the corresponding field with a terracotta error icon and clear, conversational remediation copy.
4. **Disabled Button Transparency**: Disabled buttons should maintain a minimum opacity of `0.45` and show `cursor: not-allowed;` with clear tooltip explanation.
