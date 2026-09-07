# BC Design System for Tailwind CSS

Utility rules, responsive patterns, accessibility (a11y), and animation presets for **Tailwind CSS v3 & v4**.

---

## 1. Full Preset Configuration (`tailwind.config.js`)

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ['class', '[data-theme="dark"]'],
  theme: {
    extend: {
      colors: {
        bc: {
          bg: 'var(--bc-bg, #FAF9F5)',
          surface: 'var(--bc-surface, #FFFFFF)',
          accent: 'var(--bc-accent, #D97757)',
          'accent-hover': 'var(--bc-accent-hover, #C15F3E)',
          text: 'var(--bc-text-primary, #1F1E1B)',
          muted: 'var(--bc-text-secondary, #6B6760)',
          border: 'var(--bc-border, rgba(31, 30, 27, 0.08))',
          sage: 'var(--bc-pastel-sage, #A8C2B7)',
          peach: 'var(--bc-pastel-peach, #E8CFC5)',
        },
      },
      fontFamily: {
        serif: ['var(--font-serif)', 'Newsreader', 'Georgia', 'serif'],
        sans: ['var(--font-sans)', 'Inter', 'system-ui', 'sans-serif'],
        mono: ['var(--font-mono)', 'JetBrains Mono', 'monospace'],
      },
      borderRadius: {
        'bc-card': '16px',
        'bc-button': '8px',
        'bc-prompt': '20px',
      },
      boxShadow: {
        'bc-soft': '0 4px 16px -2px rgba(31, 30, 27, 0.06)',
      },
      transitionTimingFunction: {
        'bc-ease': 'cubic-bezier(0.16, 1, 0.3, 1)',
      },
    },
  },
};
```

---

## 2. Accessibility (a11y) & Micro-Interactions

### A. Focus Rings
Never remove default focus outlines without replacing them with BC Design's terracotta focus ring:

```html
<button class="outline-none focus-visible:ring-2 focus-visible:ring-[var(--bc-accent)] focus-visible:ring-offset-2">
  Accessible Button
</button>
```

### B. Reduced Motion Compliance
Always disable spatial translation when user has `prefers-reduced-motion` enabled:

```html
<div class="transition-transform duration-200 motion-reduce:transform-none motion-reduce:transition-none">
  Calm Card
</div>
```

---

## 3. Responsive Drawer Pattern (Desktop Split vs Mobile Sheet)

```html
<!-- Responsive Artifact Container -->
<div class="fixed inset-y-0 right-0 z-40 
            w-full md:w-[480px] lg:w-[600px] 
            bg-[var(--bc-surface)] border-l border-[var(--bc-border)] 
            shadow-2xl md:shadow-lg 
            transition-transform duration-300 ease-[cubic-bezier(0.16,1,0.3,1)]">
  <!-- Drawer Header -->
</div>
```
