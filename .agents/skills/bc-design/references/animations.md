# BC Design System - Motion & Animation Guide

## 1. The BC Design Motion Philosophy

BC Design's motion language is **deliberate, literary, and respectful of cognitive load**. Unlike high-octane gaming interfaces with flashy neon or jarring spring physics, BC Design feels like a **fine fountain pen touching smooth parchment**:

* **Quiet Elegance**: Transitions are smooth, gentle, and intentional.
* **Warmth over Cold Tech**: Pulses and shimmers radiate soft terracotta and warm amber, not cybernetic blues or greens.
* **Physical Restraint**: Animations do not bounce aggressively. They decelerate with an organic, custom curve (`cubic-bezier(0.16, 1, 0.3, 1)`).

---

## 2. Timing and Easing Curves

| Token Name | Value | Purpose |
| :--- | :--- | :--- |
| `--bc-ease` | `cubic-bezier(0.16, 1, 0.3, 1)` | **Default Motion**. Smooth, exponential deceleration. |
| `--bc-ease-in-out` | `cubic-bezier(0.4, 0, 0.2, 1)` | Symmetric transitions (dialog opacity, backdrop). |
| `--bc-ease-bounce` | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Micro-delight only (reaction badges, subtle popovers). |

### Duration Budget

* **Micro-interactions (150ms - 200ms)**: Button press, checkbox toggle, tooltip scale.
* **Component Entrance (200ms - 250ms)**: Cards appearing, dropdown menus, tab switches (`bcFadeUp`).
* **Spatial / Structural (350ms - 400ms)**: Sidebar collapse, Artifacts drawer slide-in (`bcDrawerIn`).
* **Ambient / Generative (1800ms token)**: Model thinking pulse and streaming shimmers. Longer loops require a documented product reason and a reduced-motion fallback.

---

## 3. Signature BC Design Animations

### A. The "BC Design Thinking" Pulse
Used while the AI model is synthesizing or processing a deep query:

```css
@keyframes bcThinkingPulse {
  0% {
    opacity: 0.45;
    box-shadow: 0 0 0 0 rgba(217, 119, 87, 0.4);
  }
  50% {
    opacity: 1;
    box-shadow: 0 0 14px 2px rgba(217, 119, 87, 0.28);
  }
  100% {
    opacity: 0.45;
    box-shadow: 0 0 0 0 rgba(217, 119, 87, 0.4);
  }
}
```

### B. The Artifact Drawer Slide-In
The split-screen panel sliding in smoothly when code or documents are rendered:

```css
@keyframes bcDrawerIn {
  from {
    opacity: 0;
    transform: translateX(24px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}
```

### C. The Micro-Press Feedback
Applied to all primary and secondary interactive surfaces:

```css
.bc-button {
  transition: transform 150ms cubic-bezier(0.16, 1, 0.3, 1),
              background-color 150ms cubic-bezier(0.16, 1, 0.3, 1),
              box-shadow 150ms cubic-bezier(0.16, 1, 0.3, 1);
}

.bc-button:hover {
  background-color: var(--bc-accent-hover);
  box-shadow: 0 2px 8px rgba(217, 119, 87, 0.2);
}

.bc-button:active {
  transform: scale(0.985);
}
```

---

## 4. Transition Principles

These rules decide how an element moves between states. They apply to CSS and GSAP alike.

* **Enter slower than you exit.** An element arriving needs a moment to be read; one leaving should get out of the way. Use about two thirds of the entrance duration for the exit.
* **Move from where it came from.** A menu grows from its trigger, a drawer slides from its edge, and a dismissed toast leaves the way it was swiped. Set `transform-origin` to the trigger.
* **Keep distances short.** Travel 8–24px for entrances. Long travel reads as a slide show, not as a state change.
* **Scale subtly.** Start scale-in transitions at 0.96–0.98, never from zero.
* **Crossfade content, not containers.** When content swaps inside a stable frame, fade the old content out and the new content in; keep the frame still.
* **Stagger with a cap.** 40–60ms between items, and no more than 300ms for the whole group.
* **Interruptible by default.** A new state change must be able to start from the current in-between position without a jump. GSAP tweens and CSS transitions both do this; keyframe animations do not.

For sequences with more than one element, scroll-driven stories, and 3D scenes, use the GSAP patterns in [gsap-orchestration.md](./gsap-orchestration.md).

---

## 5. Accessibility (`prefers-reduced-motion`)

Always respect user preferences. When reduced motion is enabled, avoid spatial transforms:

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
