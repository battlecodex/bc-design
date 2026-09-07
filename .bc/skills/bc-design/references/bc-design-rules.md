# The 39 Distinctive Design Rules & Delivery Gate for BC Design System

> Practical rules for protecting the BC Design language from generic, subject-blind output.

## Rule tiers

### Tier 1: Hard gates

If a hard gate fails, the interface is not ready to ship:

- **R-02 Copywriting:** active-voice CTAs, no decorative em dashes in UI copy, and dignified errors.
- **R-03 Mobile Responsiveness:** verify 375px, 768px, 1024px, and 1440px; no horizontal overflow; 44×44px minimum touch targets.
- **R-17 Data & Numbers:** no fabricated statistics without a real source.
- **R-18 Testimonials:** no fabricated testimonials or unverified AI avatars.
- **R-23 Visual Assets:** use honest placeholders or genuine subject-relevant assets.
- **R-24 Navigation:** no dead links or placeholder anchors.
- **R-25 Color Contrast:** minimum WCAG AA 4.5:1. Parchment `#FAF9F5` with ink `#1F1E1B` measures 15.82:1 AAA; terracotta buttons use dark ink text.
- **R-26 Interactive Elements:** controls must perform their stated action.
- **R-27 UI States:** cover default, hover, active, focus-visible, disabled, loading, empty, and error states.
- **R-28 FAQ:** accordions are genuine and contain relevant questions when an FAQ is needed.
- **R-32 Keyboard Accessibility:** full tab/Enter support and a visible 2px focus ring.
- **R-33 Clean Source:** idiomatic component code; no patching hacks.
- **R-34 Dual Theme Functionality:** light and dark themes are both functional where offered.
- **R-35 Verification:** test interactive flows before claiming completion.
- **R-36 No Fabricated Claims:** no fake security stamps or performance metrics.
- **R-37 Design Direction Required:** decisions are grounded in an approved BC Design contract.
- **R-38 Real Content:** real content or clearly marked, honest placeholders.
- **R-39 Header Architecture:** controls use nowrap labels, 34–36px uniform heights, and a clear three-zone structure.

### Tier 2: Purpose gates

Techniques need a user or product purpose:

- **R-01 Color & Gradients:** ground palette in the subject; avoid decorative rainbow washes.
- **R-04 Icons:** purposeful 1.5px monoline SVG icons with accessible names; no emoji controls.
- **R-06 Typography:** use semantic editorial and UI roles; avoid tracked-out eyebrow filler and single-word color spans.
- **R-07 Background:** choose warm parchment/soot only when they fit the subject; never default to cold slate.
- **R-08 Button Arrows:** action labels carry the meaning; no decorative arrow suffixes.
- **R-09 Badges:** badges communicate real status such as `Current model` or `For you`.
- **R-10 Glassmorphism:** use only when it supports hierarchy and preserves contrast.
- **R-12 Shadows:** use ambient elevation rather than harsh black drops.
- **R-13 Glow:** reserve soft accent pulse for active thinking or status.
- **R-14 Feature Cards:** vary hierarchy; do not turn every item into the same card.
- **R-19 Animations:** use motion tokens and never animate streamed container dimensions.
- **R-22 Illustrations:** use subject-relevant artwork, not arbitrary decorative vectors.

### Tier 3: Quality locks

- **R-05 Layout & Rhythm:** intentional pacing and readable density.
- **R-11 Border Radius:** consistent roles; avoid full pills for primary actions without a reason.
- **R-15 CTA Hierarchy:** primary, secondary, and tertiary actions are visibly distinct.
- **R-31 Keystone Rule:** the experience remains cohesive from first view through completion.

## Delivery gate report template

Run the applicable checks and replace every placeholder with evidence. Never copy a PASS value from this template. If a check was not observed, report `NOT VERIFIED`.

```text
================================================================================
                    BC DESIGN SYSTEM - DELIVERY GATE REPORT
================================================================================

BLOCK 1: HARD GATE AUDIT
- R-02 Copywriting:          [PASS / FAIL / NOT VERIFIED] (evidence)
- R-03 Mobile Responsive:    [PASS / FAIL / NOT VERIFIED] (breakpoints and overflow)
- R-17 Data Integrity:        [PASS / FAIL / NOT VERIFIED] (source for claims)
- R-18 Social Proof:          [PASS / FAIL / NOT VERIFIED] (testimonial evidence)
- R-24 Navigation:            [PASS / FAIL / NOT VERIFIED] (route/link evidence)
- R-25 Color Contrast:        [PASS / FAIL / NOT VERIFIED] (measured pairs)
- R-26 Interactive Controls:  [PASS / FAIL / NOT VERIFIED] (flow evidence)
- R-27 UI State Coverage:     [PASS / FAIL / NOT VERIFIED] (state matrix)
- R-32 Keyboard A11y:         [PASS / FAIL / NOT VERIFIED] (focus/tab evidence)
- R-34 Dual Theme Health:     [PASS / FAIL / NOT VERIFIED] (theme evidence)
- R-35 Visual Evidence:       [PASS / FAIL / NOT VERIFIED] (screenshots or browser notes)

BLOCK 2: PURPOSE & DISTINCTIVE QUALITY
- Anti-SaaS-Card Kit:         [PASS / FAIL / NOT VERIFIED] (evidence)
- Anti-Template Chrome:       [PASS / FAIL / NOT VERIFIED] (evidence)
- Streaming Token Safety:     [PASS / FAIL / NOT VERIFIED] (evidence)
- BC Restraint Rule:          [PASS / FAIL / NOT VERIFIED] (evidence)

BLOCK 3: DESIGN DIALS
- ENERGY: [1–10] (rationale)
- RHYTHM: [1–10] (rationale)
- MOTION: [1–10] (rationale)

STATUS: [PASS / FAIL / NOT VERIFIED]
Blocking findings: [rule IDs or `none`]
Unverified surfaces: [list or `none`]
================================================================================
```
