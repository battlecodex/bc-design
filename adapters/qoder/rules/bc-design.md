# Qoder Rule: BC Design System

## Instructions
- Target Style: BC Design language.
- Backgrounds: Warm Parchment `#FAF9F5` / Espresso Soot `#181816`.
- Accent: Terracotta `#D97757`.
- Dark Mode Buttons: Solid White `#FFFFFF` for primary CTAs.
- Fonts: `Newsreader` (Headlines) + `Inter` (UI).
- Motion: `cubic-bezier(0.16, 1, 0.3, 1)`.
- Stroke Width: 1.5px for monoline SVG icons.
- Avoid animating container dimensions during token streaming.

## Engine
Query design system: `py -3 scripts/bc_design.py "<prompt>" --design-system`
