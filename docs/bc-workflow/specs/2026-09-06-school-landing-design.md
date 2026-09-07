# Sekolah Cakrawala Landing Page Design

## Mode and scope

Greenfield static landing-page prototype for an Indonesian independent school. This test covers one page, local interactions, responsive layout, and an evidence-backed BC Design audit; it does not add enrollment backend or CMS behavior.

## Audience and success criteria

- Primary audience: parents comparing schools for the next academic year.
- Secondary audience: prospective students and teachers checking the school's learning culture.
- A visitor should understand the school's point of view, see the next action, and find practical visit information in the first scroll.
- The page must remain readable and actionable at 375px, 768px, 1024px, and 1440px.

## Visual contract

- Canvas: warm parchment `#FAF9F5`; dark forest panel `#21332D`; terracotta is reserved for the primary action; sage and ink provide subject-grounded support tones.
- Typography: Newsreader for display copy; Inter for controls and supporting text.
- Signature moment: an editorial “learning in motion” hero panel with a live-looking weekly rhythm strip, not a stock-photo carousel.
- Hierarchy: one asymmetrical hero, an open three-line promise section, a compact program rail, and one dark admissions callout. Do not make every section an identical card grid.
- Copy: Indonesian sentence case, direct verbs, concrete school language, no decorative all-caps eyebrows or arrow-suffixed CTAs.

## Interaction and accessibility contract

- Navigation links scroll to sections; the primary CTA focuses the visit form.
- Visit form validates required name/email fields and shows an inline status without a page reload.
- Theme toggle changes light/dark tokens and updates its accessible label.
- Every interactive element has a visible focus ring, minimum 44px touch target, and semantic label.
- `prefers-reduced-motion` disables reveal transitions and pulse animation.

## Rejected patterns

- No generic SaaS dashboard cards, gradients, emoji controls, or fabricated statistics.
- No image dependency for the prototype; the hero uses typographic rhythm and real school-specific content so the page remains deterministic and portable.
