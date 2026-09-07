# BC Design System - Curated Design Styles

A comprehensive catalog of **10 curated design styles** built on top of the **BC Design Language**. Each style provides full token specs, visual atmosphere, CSS snippets, and framework compatibility notes.

---

## Quick Reference Matrix

| Style | Canvas Mood | Surface | Border / Line | Primary CTA | Best Suited For |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Canonical BC Design** | Warm Parchment (`#FAF9F5`) | Crisp White (`#FFFFFF`) | Hairline `0.08` | Terracotta (`#D97757`) | Conversational AI, Workspaces, Chat |
| **2. Warm Editorial Glass** | Diffused Parchment Glass | Translucent White (`0.75`) | Warm Reflection `0.3` | Terracotta / Glass | Floating prompts, Navbars, Drawers |
| **3. Espresso Soot Dark** | Deep Antique Library (`#181816`)| Soot Carbon (`#242421`) | Hairline `0.09` | Solid White (`#FFFFFF`) | Night coding, IDEs, Deep reading |
| **4. Tactile Neo-Humanist** | Organic Paper (`#FAF8F3`) | Soft Cream (`#FFFDF9`) | Soft Pencil `0.12` | Terracotta + Crayon Art | Feature announcements, Onboarding |
| **5. Scholarly Academic** | Natural Archival Paper (`#FAF9F5`)| Pure White (`#FFFFFF`) | Precise Hairline `0.1` | Scholarly Navy / Terra | Research hubs, Longform reading |
| **6. Executive Enterprise** | Deep Soot / Stone Slate | Elevated Obsidian (`#242421`)| Strict 1px Divider | Solid White / Carbon | Admin portals, Security, Compliance |
| **7. BC Design Bento Grid** | Muted Oatmeal (`#F4F3EE`) | Modular White Cards | Inset Border `0.08` | Pill Badges + Terracotta| Feature showcases, Dashboards |
| **8. Quiet Monochromatic** | Pure Parchment (`#FAF9F5`) | Flat White (`#FFFFFF`) | Subtle Ink `0.06` | Deep Ink (`#1F1E1B`) | Distraction-free writing, Markdown |
| **9. Studio Craft & Editorial**| Woven Fine Linen (`#F9F7F1`) | Ivory Cardboard (`#FFF`) | Double Hairline | Burnt Sienna (`#AA4F32`)| High-end artisan goods, Books, Media |
| **10. Amber Nocturne** | Warm Midnight Charcoal (`#161513`)| Inset Smoked Quartz | Amber Glow `0.15` | Warm Amber (`#E09F3E`) | Financial dashboards, Analytics |

---

## 1. The Canonical BC Design (Warm Minimalist)
*The default production aesthetic of BC Design.*

* **Atmosphere**: Warm fine-book parchment paper touching printer's ink. Quiet, focused, devoid of cold clinical blues.
* **Canvas**: `#FAF9F5` (light) / `#181816` (dark espresso soot).
* **Surfaces**: Crisp white `#FFFFFF` cards with 1px hairline border (`rgba(31, 30, 27, 0.08)`).
* **Typography**: Medium-weight editorial serif (`var(--bc-font-serif)`) for headlines + clean neutral sans (`Inter`) for UI.
* **Buttons**: Terracotta `#D97757` for AI action/send; Solid crisp white `#FFFFFF` with dark text in dark mode modals.
* **Framework Compatibility**: React, Next.js, Vue, Svelte, SwiftUI, React Native, Flutter, Tailwind.

```css
:root {
  --bc-bg: #FAF9F5;
  --bc-surface: #FFFFFF;
  --bc-border: rgba(31, 30, 27, 0.08);
  --bc-accent: #D97757;
  --bc-text-primary: #1F1E1B;
  --bc-text-secondary: #6B6760;
  --bc-radius: 8px;
  --bc-ease: cubic-bezier(0.16, 1, 0.3, 1);
}
```

---

## 2. Warm Editorial Glass (Modern Translucent)
*Frosted parchment glassmorphism that maintains BC Design's warm human character.*

* **Atmosphere**: Diffused sunlight through linen or rice paper. No icy blue/cyan frost.
* **Glass Surface**: `rgba(255, 255, 255, 0.75)` (light) / `rgba(36, 36, 33, 0.72)` (dark).
* **Backdrop Blur**: `backdrop-filter: blur(14px) saturate(160%);`.
* **Border**: Delicate warm light reflection: `1px solid rgba(255, 255, 255, 0.35)` (light) / `1px solid rgba(255, 255, 255, 0.08)` (dark).
* **Shadow**: `0 8px 32px 0 rgba(31, 30, 27, 0.05)`.
* **Best For**: Floating chat prompt containers, sticky navigation bars, overlay popovers, bottom sheets.

```css
.bc-glass {
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(14px) saturate(160%);
  -webkit-backdrop-filter: blur(14px) saturate(160%);
  border: 1px solid rgba(31, 30, 27, 0.08);
  box-shadow: 0 8px 32px 0 rgba(31, 30, 27, 0.05);
}
[data-theme="dark"] .bc-glass {
  background: rgba(36, 36, 33, 0.72);
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.35);
}
```

---

## 3. Espresso Soot (Deep Literary Dark Mode)
*The authentic BC Design dark mode from real user screenshots.*

* **Atmosphere**: An antique library at night. Avoids cold pitch-black (`#000000`) and blue slate (`#0f172a`).
* **Canvas**: `#181816` (Deep soot with warm espresso undertone).
* **Card Surfaces**: `#242421` (elevated panels) / `#2A2A26` (inset input wells).
* **Primary CTAs**: Solid Crisp White (`#FFFFFF`) with ink black text (`#1F1E1B`) for modals and heroes.
* **Secondary CTAs**: Dark translucent glass (`rgba(255, 255, 255, 0.09)`) with white text.
* **Accent**: Vibrant Terracotta `#E28466` for active toggles, badge highlights, and AI streaming indicators.
* **Best For**: Night development environments, technical dashboards, prolonged reading tools.

---

## 4. Tactile Neo-Humanist (Hand-Drawn & Organic)
*BC Design's distinctive feature announcement and onboarding personality.*

* **Atmosphere**: Crafted, artisanal, human. Contrasts sharply with sterile vector robots or geometric AI tropes.
* **Artwork**: Hand-drawn asymmetrical terracotta thought bubbles (`#D97757`) with white chalk/crayon squiggles (`stroke-width: 6; stroke-linecap: round`).
* **Card Thumbnails**: Soft muted earth pastels in Sage Green (`#A8C2B7`) and Blush Peach (`#E8CFC5`).
* **Icon Wells**: 40×40px squircle containers with light warm tint (`rgba(217, 119, 87, 0.08)`).
* **Best For**: Feature modals, product tours, learning hubs, welcome cards.

```html
<!-- Hand-Drawn Thought Bubble Vector -->
<svg width="180" height="180" viewBox="0 0 200 200" fill="none">
  <path d="M40,100 C30,70 60,35 110,35 C160,35 185,70 175,105 C165,140 130,155 85,150 C55,145 45,120 40,100 Z" fill="#D97757" />
  <circle cx="35" cy="165" r="12" fill="#D97757" />
  <circle cx="20" cy="180" r="7" fill="#D97757" />
  <path d="M60,95 Q75,70 90,95 T120,95 T150,95" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" />
</svg>
```

---

## 5. Scholarly Academic & Research
*For data-heavy, document-centric, or scientific interfaces.*

* **Atmosphere**: High-density reading, authoritative footnotes, dignified typography.
* **Typography**: Optical sizing `opsz: 72` Newsreader headlines, small-caps section headers (`font-variant: small-caps; letter-spacing: 0.08em;`), crisp monospace citation tags.
* **Color Palette**: Archival parchment `#FAF9F5`, Scholarly Navy `#34526F`, and Terracotta `#D97757` download badges.
* **Separators**: Subtle 1px solid hairline horizontal rules (`rgba(31, 30, 27, 0.08)`).
* **Best For**: Academic papers, research archives, policy databases, medical publications.

---

## 6. Executive BC Design (Enterprise & Governance)
*For enterprise settings, compliance dashboards, and admin consoles.*

* **Atmosphere**: Calm restraint, high institutional trust, zero decorative clutter.
* **Color Discipline**: Strict soot/parchment monochrome foundation with a single terracotta focal point for critical operations.
* **Components**: Clean toggle switches, compact role selector grids, audit logs with monoline 1.5px icons.
* **Buttons**: Rounded-md (`8px`), quiet border outlines, solid black or white confirmation buttons.
* **Best For**: Workspace management, audit logs, security settings, API key vaults.

---

## 7. BC Design Bento Grid (Modular Humanist)
*A structured grid of asymmetric feature cards balanced with warm paper textures.*

* **Atmosphere**: Organized, discoverable, interactive. Each card highlights a specific capability or role.
* **Card Geometry**: Rounded-2xl (`16px` to `18px`), inset hairline borders, soft lift on hover (`translateY(-2px)`).
* **Header Elements**: Monoline 1.5px icons paired with pill tags (e.g. `For you` in soft blue `#EBF3FF` / text `#1A62D6`).
* **Grid Layout**: 2-column or 3-column auto-fill (`grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));`).
* **Best For**: "Browse by role" sections, feature capability matrices, dashboard overview pages.

---

## 8. Quiet Monochromatic (Distraction-Free Minimalist)
*Maximum typographical clarity with minimal visual distraction.*

* **Atmosphere**: Ink on pure woven paper. Extreme readability for extended writing sessions.
* **Palette**: 95% neutral tones (`#FAF9F5`, `#ECEAE2`, `#6B6760`, `#1F1E1B`) with accent reserved strictly for the cursor or send trigger.
* **Surfaces**: Borderless or faint hairline containers, zero heavy box shadows.
* **Best For**: Document editors, markdown note-taking apps, distraction-free reading modes.

---

## 9. Studio Craft & Publishing
*High-end craft publication style for bookmakers, media houses, and artisans.*

* **Atmosphere**: Luxury editorial quarterly magazine. Warm antique cream and deep burnt sienna.
* **Palette**: Canvas `#F9F7F1`, Surface `#FFFFFF`, Accent Burnt Sienna `#AA4F32`, Soft Clay `#E8CFC5`.
* **Details**: Large display serifs (`Playfair` or `Newsreader`), double hairline framing rules, generous letter-spacing on subheadings.
* **Best For**: Literary publications, artisan e-commerce, portfolios, design agencies.

---

## 10. Amber Nocturne (Night Mode Glow)
*A warm, golden dark mode alternative for financial and analytical tools.*

* **Atmosphere**: Warm lamplight illuminating charcoal drafting paper.
* **Canvas**: Deep stone `#161513`.
* **Surface**: Elevated warm slate `#201F1C`.
* **Accents**: Warm Amber `#E09F3E` paired with Terracotta `#E28466`.
* **Glow**: Subtle warm halos on active cards (`box-shadow: 0 0 20px -4px rgba(224, 159, 62, 0.15)`).
* **Best For**: Financial analytics, telemetry consoles, late-night trading terminals.
