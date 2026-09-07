# Design System: BC Design Code Studio
Source of truth for the BC Design language.

## Core Directives
- **Pattern**: Interactive Sandbox & Parameter Tweaks Popover
  - *Conversion*: Product-led developer evaluation with live parameter tuning
  - *CTA*: 'Run inference' / 'Deploy to API' button inside tweaks drawer
- **Style**: Espresso Soot (Deep Literary Dark Mode)
  - *Canvas*: #181816 (Deep soot with espresso undertone)
  - *Surface*: #242421 (Elevated card) / #2A2A26 (Inset wells)
- **Palette**:
  - Primary: `#E28466`
  - CTA Light: `#D97757`
  - CTA Dark: `#E28466`
  - Text Primary: `#FAF9F5`
  - Border: `rgba(255, 255, 255, 0.08)`
- **Typography**:
  - Heading: `Instrument Serif (Serif)`
  - Body: `Geist (Sans)`
  - Code: `Geist Mono (Mono)`
  - CDN: `https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500;600&family=JetBrains+Mono&display=swap`

## Pre-Delivery Checklist
- [ ] No emojis as icons (use 1.5px monoline Lucide SVGs).
- [ ] Dark mode modal CTA uses Solid Crisp White (#FFFFFF) with dark text.
- [ ] Container dimensions NOT animated during AI token streaming.
- [ ] Light mode text contrast meets WCAG AAA (16.2:1).
- [ ] Visible 2px terracotta focus ring for keyboard navigation.
- [ ] Responsive: 375px, 768px, 1024px, 1440px.
