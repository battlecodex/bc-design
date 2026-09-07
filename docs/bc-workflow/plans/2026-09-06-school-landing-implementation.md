# Sekolah Cakrawala Landing Page Implementation Plan

> **For implementation:** Execute this plan task-by-task with review checkpoints. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a portable static school landing page that demonstrates the BC Design workflow in a real interface.

**Architecture:** Keep the demo dependency-free with one HTML entry point, one stylesheet, and one small behavior script. Load Newsreader with a Georgia fallback, keep content and layout semantic, and use the BC Design CLI audit as a source-level quality gate.

**Tech Stack:** HTML5, CSS custom properties, vanilla JavaScript, Newsreader/Inter web fonts, BC Design CLI.

**Spec:** `docs/bc-workflow/specs/2026-09-06-school-landing-design.md`

## Global Constraints

- Use `#FAF9F5` and `#181816` as the BC Design light/dark foundations.
- Use Newsreader for editorial hierarchy and Inter for interface controls.
- Keep CTAs active voice and avoid decorative arrow suffixes.
- Respect keyboard focus, 44px touch targets, reduced motion, and responsive widths.
- Keep the page dependency-free and do not introduce fabricated testimonials or metrics.

---

### Task 1: Add the semantic page structure

**Files:**
- Create: `examples/school-cakrawala/index.html`

- [x] **Step 1: Write the accessible HTML shell and sections**

Add landmark elements for skip link, header/nav, main, hero, programs, rhythm, visit form, and footer. Use real labels and `aria-live` for form feedback.

### Task 2: Implement BC Design styling and responsive behavior

**Files:**
- Create: `examples/school-cakrawala/styles.css`

- [x] **Step 1: Add tokens, typography, layout, states, and media queries**

Use Newsreader with a Georgia fallback, semantic colors, a 3-zone header, an asymmetrical hero, a dark admissions panel, focus styles, and breakpoints for 768px and 1024px.

### Task 3: Add bounded interactions

**Files:**
- Create: `examples/school-cakrawala/script.js`

- [x] **Step 1: Implement theme toggle, anchor focus, and form validation**

Persist the theme preference, update the toggle label, focus the visit form from the hero CTA, and report a successful submission inline without navigating away.

### Task 4: Verify the demonstration

**Files:**
- Test: `examples/school-cakrawala/**`

- [x] **Step 1: Run BC Design source audit and static checks**

Run `python .agents/skills/bc-design/scripts/bc_design.py --audit examples/school-cakrawala`, check HTML/CSS/JS syntax with a local server, and inspect the rendered page at 375px, 768px, 1024px, and 1440px.
