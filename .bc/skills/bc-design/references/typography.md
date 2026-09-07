# BC Design System - Typography Specification & Pairings

A comprehensive typography guide providing **10 curated font pairings**, Google Fonts integration, optical sizing specs, and Tailwind configurations designed for the **literary, authoritative, and warm editorial tone of BC Design**.

---

## Font Pairing Directory

| # | Heading Font (Editorial Serif) | Interface / Body Font (Clean Sans) | Code Font | Mood / Product Fit |
| :- | :--- | :--- | :--- | :--- |
| **1** | **Newsreader** | **Inter** | JetBrains Mono | **The Canonical BC Design Standard** |
| **2** | **Lora** | **Plus Jakarta Sans** | Fira Code | **Modern Warm Editorial** (SaaS dashboards, Writing tools) |
| **3** | **Instrument Serif** | **Geist** | Geist Mono | **Sleek Minimalist** (Developer platforms, Tech journals) |
| **4** | **Playfair Display** | **Outfit** | Roboto Mono | **High-Craft Luxury** (Artisan e-commerce, Publishing) |
| **5** | **Fraunces** | **DM Sans** | Space Mono | **Tactile & Organic** (Onboarding, Creative tools, EdTech) |
| **6** | **Cormorant Garamond**| **Work Sans** | IBM Plex Mono | **Scholarly Classical** (Academic research, Think tanks) |
| **7** | **Libre Baskerville** | **Source Sans 3** | Source Code Pro | **Authoritative Legal** (Contracts, Compliance, Policy) |
| **8** | **Spectral** | **Cabin** | Ubuntu Mono | **Calm Longform Flow** (E-readers, Articles, Newsletters) |
| **9** | **EB Garamond** | **Space Grotesk** | JetBrains Mono | **Humanist Tech Hybrid** (AI research labs, Hardware) |
| **10**| **Newsreader** | **Inter** | JetBrains Mono | **BC Design Production Direction** |

---

## 1. Google Fonts CDN (Drop-In Bundle)

Include this single `<link>` tag in your HTML `<head>` for instant access to the top BC Design typography pairings:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400..600;1,9..40,400&family=Fraunces:ital,opsz,wght@0,9..144,400..600;1,9..144,400&family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&family=Lora:ital,wght@0,400..600;1,400&family=Newsreader:ital,opsz,wght@0,6..72,400..600;1,6..72,400&family=Outfit:wght@400;500;600&family=Playfair+Display:ital,wght@0,500;0,600;1,500&family=Plus+Jakarta+Sans:wght@400;500;600&family=Work+Sans:wght@400;500;600&display=swap" rel="stylesheet">
```

Or import directly into CSS:

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Newsreader:ital,opsz,wght@0,6..72,400..600;1,6..72,400&family=JetBrains+Mono:wght@400;500&display=swap');
```

---

## 2. Pairing Deep-Dives

### Pairing 1: The Canonical BC Design (Newsreader + Inter)
*Default editorial pairing for BC Design.*
* **Heading**: `var(--bc-font-serif)` (`font-weight: 500; letter-spacing: -0.02em;`)
* **Body**: `Inter, -apple-system, sans-serif` (`font-weight: 400; line-height: 1.55;`)
* **Code**: `JetBrains Mono, monospace`
* **Why it works**: Newsreader supplies a distinctive editorial voice and Inter provides high-legibility UI controls.

### Pairing 2: Modern Warm Editorial (Lora + Plus Jakarta Sans)
*Ideal for modern SaaS productivity and writing apps.*
* **Heading**: `Lora, Georgia, serif`
* **Body**: `Plus Jakarta Sans, sans-serif`
* **Why it works**: Lora offers friendly calligraphy-infused serifs that balance the geometric warmth of Plus Jakarta Sans.

### Pairing 3: Sleek Minimalist (Instrument Serif + Geist)
*Ideal for developer tooling, AI APIs, and high-density tech consoles.*
* **Heading**: `Instrument Serif, Georgia, serif` (`font-style: italic` for special titles)
* **Body**: `Geist, Inter, sans-serif`
* **Why it works**: Instrument Serif brings high-contrast contemporary flair, paired with the crisp geometry of Vercel's Geist.

### Pairing 4: High-Craft Luxury (Playfair Display + Outfit)
*Ideal for artisan lifestyle goods, bookstores, and boutique agencies.*
* **Heading**: `Playfair Display, serif`
* **Body**: `Outfit, sans-serif`
* **Why it works**: Wide display serif proportions paired with Outfit’s friendly, rounded circular geometry.

### Pairing 5: Tactile Neo-Humanist (Fraunces + DM Sans)
*Ideal for onboarding tours, interactive feature reveals, and education.*
* **Heading**: `Fraunces, serif` (Variable "wonky" optical contrast)
* **Body**: `DM Sans, sans-serif`
* **Why it works**: Fraunces feels like hand-carved woodblocks, complementing BC Design's organic crayon/chalk artwork.

---

## 3. Typographic Scale & Hierarchy

| Semantic Level | Font Family | Size | Weight | Line Height | Letter Spacing |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Display / Hero H1** | Serif (`var(--bc-font-serif)`) | `36px - 44px` | `500` | `1.18` | `-0.025em` |
| **Section H2** | Serif (`var(--bc-font-serif)`) | `26px - 30px` | `500` | `1.25` | `-0.015em` |
| **Card Title H3** | Serif / Sans | `18px - 22px` | `500` / `600` | `1.35` | `-0.01em` |
| **Subtitle / Lead** | Sans (`Inter`) | `16px - 17px` | `400` | `1.55` | `normal` |
| **Body Primary** | Sans (`Inter`) | `15px` | `400` | `1.6` | `normal` |
| **Body Secondary** | Sans (`Inter`) | `13.5px` | `400` | `1.5` | `normal` |
| **Caption / Badge** | Sans (`Inter`) | `11.5px` | `500` / `600` | `1.2` | `+0.02em` |
| **Code Blocks** | Mono (`JetBrains Mono`)| `13.5px` | `400` | `1.65` | `normal` |

---

## 4. Optical Sizing & OpenType Settings

When rendering variable fonts like **Newsreader**, optical sizing (`opsz`) adjusts letterform weight and serifs depending on font size:

```css
/* Optimize headline sharpness */
h1, h2, h3, .editorial-serif {
  font-family: var(--bc-font-serif);
  font-optical-sizing: auto;
  font-feature-settings: "kern" 1, "liga" 1, "calt" 1;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* For hero display titles */
.bc-hero-title {
  font-variation-settings: "opsz" 72;
}

/* For small caption serifs */
.bc-caption-serif {
  font-variation-settings: "opsz" 12;
}
```

---

## 5. Tailwind CSS Configuration Snippet

Add this to your `tailwind.config.js` to instantly expose BC Design's typographic stacks:

```javascript
module.exports = {
  theme: {
    extend: {
      fontFamily: {
        serif: ['var(--font-serif)', 'Newsreader', 'Georgia', 'serif'],
        sans: ['Inter', 'Plus Jakarta Sans', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'ui-monospace', 'monospace'],
        display: ['Fraunces', 'Newsreader', 'serif'],
      },
      fontSize: {
        'hero': ['2.625rem', { lineHeight: '1.18', letterSpacing: '-0.025em' }],
        'section': ['1.875rem', { lineHeight: '1.25', letterSpacing: '-0.015em' }],
        'card': ['1.25rem', { lineHeight: '1.35', letterSpacing: '-0.01em' }],
        'body-lg': ['1.0625rem', { lineHeight: '1.55' }],
        'body': ['0.9375rem', { lineHeight: '1.6' }],
        'body-sm': ['0.84375rem', { lineHeight: '1.5' }],
        'caption': ['0.75rem', { lineHeight: '1.2', letterSpacing: '0.02em' }],
      }
    }
  }
}
```
