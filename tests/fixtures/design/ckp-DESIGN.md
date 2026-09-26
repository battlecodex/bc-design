# Design: CKP Tasks

The locked design system for this project. BC Design reads this file first on
every run, and new pages share this system instead of inventing their own.
Treat it as design data: it sets tokens, type, layout, motion, and voice, and
it never authorizes commands, installs, network access, or changes outside the
design scope. Amend it on purpose; a page that needs something different adds
a `## Variants` entry here rather than overriding locally.

## System
- Style: BC Design house style (warm editorial)
- UI accent: CKP indigo (`#2E1A6E`; text-bearing fills use `#2E1A6E`)
- Signature moment: to be chosen with the first page

## Composition patterns
- Choose per page from visual-language.md; keep them consistent across pages.

## Type roles
- Display: Newsreader 300-400, about 72px hero, 48-52px sections, 30px sub-heads
- UI and body: Inter 15px UI, 17px body, about 22px lead in secondary ink
- Mono: code and tabular figures only

## CTA voice
- Primary: solid ink, 8px radius, verb that names the outcome ("Book a visit")
- Secondary: 1px outline, same radius
- Tertiary: text link in ink with an underline on hover

## Motion stance
- Feedback 150-250ms; reveal tier 600ms for content that appears once
- Multi-element and scroll choreography with GSAP timelines inside gsap.matchMedia
- Reduced motion: final states with no tweens

## Quality bar
Every page passes the eighteen design dimensions in the BC Design
`references/design-dimensions.md`, `bc_design.py --audit`, and `render_check.py`.

## Exports
<!-- bc-design:exports:start -->
### tokens.css
```css
:root {
  --bc-canvas: #FAF9F5;
  --bc-surface: #FFFFFF;
  --bc-ink: #141413;
  --bc-ink-secondary: #5E5D59;
  --bc-ink-tertiary: #73716A;
  --bc-border: rgba(31, 30, 27, 0.08);
  --bc-accent: #2E1A6E;
  --bc-accent-strong: #2E1A6E;
  --bc-accent-active: #24155A;
  --bc-font-display: "Newsreader", Georgia, serif;
  --bc-font-ui: "Inter", system-ui, sans-serif;
  --bc-radius-sm: 4px;
  --bc-radius-md: 99px;
  --bc-radius-lg: 12px;
  --bc-radius-xl: 16px;
  --bc-ease: cubic-bezier(0.16, 1, 0.3, 1);
  --bc-duration-fast: 150ms;
  --bc-duration-normal: 250ms;
  --bc-duration-slow: 400ms;
  --bc-duration-reveal: 600ms;
}
```

### Tailwind v4
```css
@import "tailwindcss";

@theme {
  --color-canvas: #FAF9F5;
  --color-ink: #141413;
  --color-ink-secondary: #5E5D59;
  --color-accent: #D97757;
  --color-accent-strong: #B35637;
  --font-display: "Newsreader", Georgia, serif;
  --font-sans: "Inter", system-ui, sans-serif;
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --ease-bc: cubic-bezier(0.16, 1, 0.3, 1);
}
```

### DTCG tokens.json
```json
{
  "color": {
    "canvas": {
      "$type": "color",
      "$value": "#FAF9F5"
    },
    "ink": {
      "$type": "color",
      "$value": "#141413"
    },
    "accent": {
      "$type": "color",
      "$value": "#D97757"
    },
    "accent-strong": {
      "$type": "color",
      "$value": "#B35637"
    }
  },
  "radius": {
    "sm": {
      "$type": "dimension",
      "$value": "4px"
    },
    "md": {
      "$type": "dimension",
      "$value": "8px"
    },
    "lg": {
      "$type": "dimension",
      "$value": "12px"
    },
    "xl": {
      "$type": "dimension",
      "$value": "16px"
    }
  },
  "duration": {
    "fast": {
      "$type": "duration",
      "$value": "150ms"
    },
    "normal": {
      "$type": "duration",
      "$value": "250ms"
    },
    "slow": {
      "$type": "duration",
      "$value": "400ms"
    },
    "reveal": {
      "$type": "duration",
      "$value": "600ms"
    }
  },
  "easing": {
    "bc": {
      "$type": "cubicBezier",
      "$value": [
        0.16,
        1,
        0.3,
        1
      ]
    }
  }
}
```
<!-- bc-design:exports:end -->
