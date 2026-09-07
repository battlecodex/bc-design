# BC Design System - Conversion-Optimized Landing Patterns

A directory of **conversion-optimized landing page patterns** built to honor the **warm, literary, and high-trust aesthetic of BC Design**. Each pattern outlines layout flow, CTA hierarchy, color strategy, and structural code skeletons.

---

## Pattern Directory

| # | Pattern Name | Best Suited For | Key Visual Anchor | Primary CTA Strategy |
| :- | :--- | :--- | :--- | :--- |
| **1** | **Hero + Floating Prompt** | Conversational AI, Assistants, Search | Floating input box (`#FFFFFF`, shadow) | Instant interactive query prompt |
| **2** | **Split Feature + Crayon Art**| Feature reveals, Model launches | Asymmetric terracotta thought bubble | Solid white (dark) / Terracotta (light)|
| **3** | **Video-First Academy Hub** | Tutorials, EdTech, Product Education | macOS chrome frame with play trigger | "Start tutorial" card overlay |
| **4** | **Role / Persona Explorer Grid**| Multi-persona SaaS, Enterprise | 10-card bento grid with monoline icons| Role filter chip + direct workflow jump|
| **5** | **Interactive Sandbox & Tweaks**| Developer tools, Model playgrounds | Inset parameter drawer / popover slider | "Run inference" / "Deploy prompt" |
| **6** | **Enterprise Trust & Governance**| B2B SaaS, FinTech, Compliance | High-density audit list & SOC2 badges | "Request security whitepaper" |
| **7** | **Conversion Pricing Matrix** | SaaS subscriptions, API credit plans | 4-tier cards with recommended pill tag | Dual hierarchy: Solid White vs Hairline |
| **8** | **Editorial Story / Manifesto**| Research institutes, Brand launches | Large Newsreader serif editorial column | Inline citation links & newsletter opt-in|
| **9** | **Auth-First Clean Card** | Member portals, Private Betas | Centered 420px card on parchment canvas| "Continue with email" |
| **10**| **Benchmark Evaluation Matrix**| Model comparisons, Performance proofs| Hairline data grid with subtle amber bars| "Explore technical report" |

---

## 1. Pattern: Hero + Floating Prompt (BC Design Core Landing)
*The signature first-glance interaction of BC Design.*

* **Layout Flow**:
  1. Top Navigation: Minimalist logo + breadcrumb/version tag + theme toggle.
  2. Centered Serif Headline: *"Where will your mind go today?"* or *"Intelligent answers, crafted with care."*
  3. Floating Elevated Prompt Box: 720px wide, rounded-2xl (`18px`), subtle shadow, model badge selector (`BC Design current model`), and a clearly labelled send control.
  4. Prompt Suggestions / Starter Pills: Horizontal row of warm parchment pills (e.g. *"Analyze financial statement"*, *"Refactor React hook"*).
* **CTA Strategy**: Zero friction. Let the user start typing immediately or click a starter suggestion to demonstrate capability before sign-up.

```html
<section class="bc-hero-section">
  <h1 class="font-serif text-4xl text-center font-medium mb-8">What would you like to explore?</h1>
  <div class="bc-prompt-box max-w-2xl mx-auto bg-white border border-stone-200 rounded-2xl p-4 shadow-sm">
    <textarea rows="3" placeholder="Message BC Design..." class="w-full resize-none outline-none font-sans text-base"></textarea>
    <div class="flex justify-between items-center mt-3 pt-2 border-t border-stone-100">
      <span class="text-xs text-stone-500 bg-stone-100 px-3 py-1 rounded-full">BC Design current model</span>
      <button class="rounded-full bg-[#D97757] px-3 py-2 text-[#1F1E1B]">Send</button>
    </div>
  </div>
</section>
```

---

## 2. Pattern: Split Feature + Organic Crayon Art (Product Launch)
*High-conversion announcement pattern seen in BC Design's "Customize BC Design" and "Memory Updates".*

* **Layout Flow**:
  * Asymmetric 2-column container: Left 60% contains authoritative serif headline, bulleted benefits with 1.5px monoline icons, and action triggers. Right 40% contains a warm, organic hand-drawn terracotta illustration (e.g. thought bubbles with white crayon squiggles).
* **CTA Strategy**:
  * In Dark Mode: Primary CTA is **Solid Crisp White (`#FFFFFF`) with dark text** (`#1F1E1B`); Secondary is **Translucent Dark Glass (`rgba(255,255,255,0.09)`)**.
  * In Light Mode: Primary CTA is **Solid Terracotta (`#D97757`)**; Secondary is **Warm Parchment Pill (`#ECEAE2`)**.

---

## 3. Pattern: Video-First Academy Hub (BC Design Learn)
*Optimized for product tutorials, developer walkthroughs, and educational onboarding.*

* **Layout Flow**:
  1. Section Header: *"Learn"* with subtle book icon.
  2. 3-Column Tutorial Cards:
     * Card Thumbnail: Simulated macOS chrome window frame (red, yellow, green window dots) with high-contrast UI preview.
     * Card Meta: Duration badge (`5 min`), topic badge (`Prompt Engineering`).
     * Card Title: Bold 16px title + 13.5px description.
  3. Interactive "Watch Course" modal popover on click.
* **CTA Strategy**: High-conversion play button overlay with hover lift (`translateY(-2px)`).

---

## 4. Pattern: Role / Persona Explorer Grid
*Conversion through self-segmentation ("Browse by role").*

* **Layout Flow**:
  * 10-card auto-filling grid (`repeat(auto-fill, minmax(220px, 1fr))`).
  * Roles: Engineering, Product, Design, Sales, Marketing, HR & Recruiting, Legal, Finance, Research, Customer Support.
  * Card Elements: 40×40px squircle icon container with monoline 1.5px icon + Role title + Optional "For you" blue badge.
* **CTA Strategy**: Clicking a role instantly filters the page to relevant templates, case studies, and prompt workflows.

---

## 5. Pattern: Interactive Sandbox & Tweaks Popover
*Empower prospective customers to test parameters live.*

* **Layout Flow**:
  * Split screen: Left editor shows live system prompt / markdown output; Right popover panel ("Tweaks") lets the user toggle parameters (Temperature slider, Thinking budget, System role, Web search toggle).
* **CTA Strategy**: Immediate "Deploy to API" or "Save preset" button anchored inside the tweaks panel.

---

## 6. Pattern: Enterprise Trust & Governance
*Essential for high-value enterprise sales, financial services, and healthcare buyers.*

* **Layout Flow**:
  1. Header: *"Built for enterprise security, privacy, and compliance."*
  2. Certification Badge Strip: SOC2 Type II, HIPAA Compliant, GDPR, ISO 27001 in monochrome hairline emblems.
  3. Data Retention Guarantee: Explicit callout box: *"Your data is never used to train our models."* with a quiet checkmark.
  4. Audit Log Preview: Simulated table showing timestamp, actor, event, and IP address.
* **CTA Strategy**: Primary button *"Schedule security review"*, Secondary link *"Download compliance packet (PDF)"*.

---

## 7. Pattern: Conversion Pricing Matrix
*Optimized for tier comparison with crystal-clear visual hierarchy.*

* **Layout Flow**:
  * 4-column horizontal card deck: **Free**, **Pro**, **Team**, **Enterprise**.
  * Recommended Tier ("Pro"): Elevated with a hairline terracotta border (`border: 1.5px solid #D97757`) and a floating pill: *"Most Popular"*.
  * Features List: Checkmarked items using monoline 1.5px icons in soft eucalyptus sage (`#7D8A68`).
* **CTA Hierarchy**:
  * Free: Hairline secondary button (*"Get started"*).
  * Pro (Featured): Solid Terracotta `#D97757` or Solid White button (*"Upgrade to Pro"*).
  * Enterprise: High-contrast Dark button (*"Contact Sales"*).

---

## 8. Pattern: Editorial Story / Manifesto
*For thought leadership, AI alignment research, and company mission.*

* **Layout Flow**:
  * Single centered 680px editorial column.
  * Serif headline at 42px with 1.2 line height.
  * Lead paragraph in 20px with drop-cap styling.
  * Inset pull-quotes styled like fine hardcover books with a 2px left border in `#D97757`.
  * Inline footnote citations that expand on hover.
* **CTA Strategy**: Subtle newsletter subscription box or "Read technical paper" at the conclusion.
