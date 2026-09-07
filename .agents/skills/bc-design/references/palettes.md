# BC Design System - Product-Specific Color Palettes

A comprehensive suite of **10 product-specific color palettes** engineered to preserve the **warm, earthy, humanist, and editorial DNA of BC Design** across distinct commercial verticals.

---

## Palettes Overview

| Industry / Vertical | Primary Accent | CTA Mode (Light/Dark) | Canvas Mood | Status Accent |
| :--- | :--- | :--- | :--- | :--- |
| **1. AI & SaaS Productivity** | Terracotta `#D97757` | Terracotta / Solid White `#FFF` | Warm Parchment `#FAF9F5` | Amber `#E09F3E` |
| **2. Fintech & Wealth Intelligence** | Warm Amber `#E09F3E` | Deep Ink / Solid White `#FFF` | Solid Stone `#F8F7F2` | Forest `#4D8C57` |
| **3. Healthcare & Life Sciences** | Eucalyptus Sage `#7D8A68`| Sage `#7D8A68` / White | Soft Oatmeal `#F4F3EE` | Terracotta Alert |
| **4. Developer Tools & Code IDEs**| Terracotta Glow `#E28466`| Glow `#E28466` / Soot | Deep Obsidian `#141412`| Muted Cyan `#68B0AB`|
| **5. E-Commerce & Artisan Brands** | Burnt Sienna `#AA4F32` | Burnt Sienna / White | Fine Linen `#FAF8F3` | Blush Clay `#E8CFC5`|
| **6. Academic Research & Policy** | Scholarly Navy `#34526F` | Navy `#34526F` / Terracotta | Archival Paper `#FAF9F5`| Terracotta `#D97757`|
| **7. Creative Studio & Media** | Terracotta `#D97757` | Peach `#E8CFC5` / Terracotta| Warm Cream `#FAF7F2` | Coral `#D46243` |
| **8. Legal & Enterprise Governance**| Deep Ink `#1F1E1B` | Ink `#1F1E1B` / Solid White | Formal Paper `#FAF9F6` | Amber `#C68A2E` |
| **9. Cloud Infrastructure & Cyber** | Cyan Stone `#4A8B99` | Cyan `#4A8B99` / White | Charcoal Ash `#151616` | Terracotta Alert |
| **10. Community & Social Discussion**| Olive Stone `#6E7F5E`| Olive `#6E7F5E` / White | Natural Sand `#F6F4ED` | Warm Terracotta |

---

## 1. AI & SaaS Productivity (The Canonical Palette)
*For conversational AI, productivity suites, knowledge management, and collaborative docs.*

```css
:root {
  --palette-canvas: #FAF9F5;          /* Warm fine-book parchment */
  --palette-canvas-subtle: #F4F3EE;   /* Inset well / sidebar */
  --palette-surface: #FFFFFF;         /* Elevated cards */
  --palette-primary: #D97757;         /* Signature Terracotta */
  --palette-primary-hover: #C15F3E;   /* Deep Terracotta */
  --palette-secondary: #ECEAE2;       /* Warm pill button background */
  --palette-cta-light: #D97757;       /* Terracotta send/continue */
  --palette-cta-dark: #FFFFFF;        /* Solid white in dark mode */
  --palette-text-primary: #1F1E1B;    /* Warm ink black */
  --palette-text-secondary: #6B6760;  /* Muted stone */
  --palette-text-tertiary: #99948B;   /* Placeholder / disabled */
  --palette-border: rgba(31, 30, 27, 0.08);
  --palette-border-strong: rgba(31, 30, 27, 0.16);
  --palette-status-success: #4D8C57;
  --palette-status-warning: #E09F3E;
  --palette-status-error: #D97757;
}

[data-theme="dark"] {
  --palette-canvas: #181816;          /* Deep espresso soot */
  --palette-canvas-subtle: #20201D;
  --palette-surface: #242421;
  --palette-primary: #E28466;
  --palette-primary-hover: #EA967B;
  --palette-secondary: rgba(255, 255, 255, 0.09);
  --palette-cta-light: #FFFFFF;
  --palette-cta-dark: #FFFFFF;
  --palette-text-primary: #FAF9F5;
  --palette-text-secondary: #A39E93;
  --palette-text-tertiary: #6E6A62;
  --palette-border: rgba(250, 249, 245, 0.09);
  --palette-border-strong: rgba(250, 249, 245, 0.18);
}
```

---

## 2. Fintech & Wealth Intelligence
*For wealth management, trading desks, accounting software, and financial analytics.*

| Token | Hex / Value | Purpose |
| :--- | :--- | :--- |
| **Canvas Light / Dark** | `#F8F7F2` / `#161514` | Neutral warm stone foundation |
| **Surface** | `#FFFFFF` / `#21201D` | Metric card surface |
| **Primary Accent** | `#E09F3E` | Warm Amber Gold (Value metrics, premium tiers) |
| **Positive Trend** | `#4D8C57` | Forest Green (Growth, non-neon) |
| **Negative Trend** | `#C75440` | Muted Terracotta Red (Drawdowns, risk) |
| **CTA Light / Dark** | `#1F1E1B` / `#FFFFFF` | High-contrast authoritative buttons |
| **Dividers** | `rgba(31, 30, 27, 0.09)` | Hairline tabular ledger lines |

---

## 3. Healthcare, Bio & Life Sciences
*For clinical trial platforms, patient portals, health metrics, and mental wellness apps.*

| Token | Hex / Value | Purpose |
| :--- | :--- | :--- |
| **Canvas** | `#F4F3EE` (Light Oatmeal) / `#181A18` | Soothing organic ground |
| **Surface** | `#FFFFFF` / `#222421` | Diagnostic report cards |
| **Primary Accent** | `#7D8A68` | Eucalyptus / Sage Green (Vitality & calm) |
| **Soft Wellness Tint** | `#EAF1EE` | Pastel Sage pill badges |
| **Urgent Callout** | `#D97757` | Terracotta Clay (Urgent triage alerts) |
| **Text Primary** | `#1E221C` | Deep medicinal slate ink |
| **Border** | `rgba(30, 34, 28, 0.08)` | Gentle unobtrusive dividers |

---

## 4. Developer Tools & Code Intelligence
*For terminal IDEs, API consoles, code review tools, and deployment pipelines.*

| Token | Hex / Value | Purpose |
| :--- | :--- | :--- |
| **Canvas Dark** | `#141412` | Deep charcoal obsidian (default) |
| **Surface Dark** | `#1D1D1A` | File tree and active editor surface |
| **Primary Accent** | `#E28466` | Terracotta Glow (Execution, compile, build) |
| **Syntax Keyword** | `#E09F3E` | Function signatures & keywords |
| **Syntax String** | `#68B0AB` | Strings & variables (Muted cyan) |
| **Syntax Comment** | `#6E6A62` | Warm dimmed commentary |
| **Border** | `rgba(255, 255, 255, 0.08)` | Crisp 1px editor pane dividers |

---

## 5. E-Commerce & Artisan Publishing
*For luxury bookstores, craft fashion, bespoke furniture, and lifestyle commerce.*

| Token | Hex / Value | Purpose |
| :--- | :--- | :--- |
| **Canvas** | `#FAF8F3` | Fine woven linen paper |
| **Surface** | `#FFFFFF` | Product vitrines and lookbooks |
| **Primary CTA** | `#AA4F32` | Deep Burnt Sienna (Add to bag, Checkout) |
| **Secondary Accent**| `#E8CFC5` | Soft Blush Clay (Discount pills, editorial chips) |
| **Text Primary** | `#171614` | Deepest book printer's ink |
| **Text Secondary** | `#7A756D` | Material notes, pricing subtitles |
| **Border** | `rgba(23, 22, 20, 0.08)` | Frame outlines |

---

## 6. Academic Research & Higher Education
*For university archives, preprint repositories, scientific journals, and policy institutes.*

| Token | Hex / Value | Purpose |
| :--- | :--- | :--- |
| **Canvas** | `#FAF9F5` | Archival cotton paper |
| **Surface** | `#FFFFFF` | Abstract & peer-review panels |
| **Primary Accent** | `#34526F` | Scholarly Oxford Navy |
| **Action Accent** | `#D97757` | Terracotta (Download PDF, View DOI) |
| **Quote Well** | `#F1EEE7` | Quoted bibliography background wells |
| **Text Primary** | `#1C1B19` | Authoritative serif text |
| **Border** | `rgba(28, 27, 25, 0.09)` | Footnote and citation dividers |

---

## 7. Creative Studio & Generative Media
*For audio production, video generation, digital design tools, and typography studios.*

| Token | Hex / Value | Purpose |
| :--- | :--- | :--- |
| **Canvas** | `#FAF7F2` (Light) / `#1A1918` (Dark) | Warm studio canvas |
| **Surface** | `#FFFFFF` / `#252422` | Canvas panels and timeline tracks |
| **Primary Accent** | `#D97757` | Terracotta (Render, Export, Generate) |
| **Timeline Tint** | `#E8CFC5` | Track selection ranges |
| **Text Primary** | `#1E1C1A` | Sharp high-contrast copy |
| **Border** | `rgba(30, 28, 26, 0.09)` | Layer bounding outlines |

---

## 8. Legal, Compliance & Governance
*For contract analysis, compliance verification, policy management, and audits.*

| Token | Hex / Value | Purpose |
| :--- | :--- | :--- |
| **Canvas** | `#FAF9F6` | Clean legal bond paper |
| **Surface** | `#FFFFFF` | Clause cards and contract diffs |
| **Primary Accent** | `#1F1E1B` | Deep Formal Ink |
| **Status Verified** | `#4D8C57` | Compliant / Approved stamp |
| **Flagged Clause** | `#D97757` | Terracotta review marker |
| **Border** | `rgba(31, 30, 27, 0.12)` | Strict structural dividers |

---

## 9. Cloud Infrastructure & Cybersecurity
*For server monitoring, threat mitigation, microservice topologies, and access control.*

| Token | Hex / Value | Purpose |
| :--- | :--- | :--- |
| **Canvas Dark** | `#151616` | Dark ash bedrock |
| **Surface** | `#1E2020` | Server health nodes |
| **Primary Accent** | `#4A8B99` | Muted Turquoise (Network healthy) |
| **Alert Accent** | `#E28466` | Cyber Terracotta (Breach warning, high latency) |
| **Text Primary** | `#F5F7F7` | Crisp terminal white |
| **Border** | `rgba(255, 255, 255, 0.08)` | Grid connection lines |

---

## 10. Community & Social Discussion
*For intellectual discussion boards, forum spaces, book clubs, and team chats.*

| Token | Hex / Value | Purpose |
| :--- | :--- | :--- |
| **Canvas** | `#F6F4ED` | Natural sand foundation |
| **Surface** | `#FFFFFF` | Comment thread bubbles |
| **Primary Accent** | `#6E7F5E` | Olive Stone (Upvote, topic follow) |
| **Author Badge** | `#D97757` | Terracotta creator badge |
| **Text Primary** | `#20211D` | Relaxed conversational text |
| **Border** | `rgba(32, 33, 29, 0.07)` | Thread indentation lines |
