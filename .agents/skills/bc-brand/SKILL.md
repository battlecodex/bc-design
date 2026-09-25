---
name: bc-brand
description: Use when defining, extracting, reviewing, or updating a product brand system for an interface, including palette, typography roles, voice, and asset usage.
---

# BC Brand

Use this skill to turn brand evidence into a usable interface contract. Start from the product, audience, existing references, and approved constraints; do not invent a visual identity from a generic template.

## Workflow

1. Look for a written brand source before anything else: `DESIGN.md`, a brand or style guide, design tokens, or a Figma library. Then inventory existing logos, colors, type, imagery, copy, legal constraints, and examples.
2. Separate observed brand facts from proposed decisions.
3. Define semantic roles for canvas, surfaces, text, borders, accents, status, focus, type, and motion.
4. Check every foreground/background pairing with the BC contrast command.
5. Write voice rules with examples of active labels, errors, empty states, and status copy.
6. Record rejected directions and the reason for each.
7. Hand the approved brand contract to `bc-design-system` or `bc-ui-styling`.

## Non-negotiables

- Brand evidence outranks the BC house palette and type; map it onto the house roles and keep the luxury standard.
- Without brand evidence, apply the house style and pick the one accent from the subject.
- A color is not approved until its intended text pair is contrast-tested.
- Do not add fonts, logos, or imagery to a project without a license/source decision.
- Keep brand decisions semantic so components do not depend on raw hex values.
- Report uncertainty instead of presenting an inferred brand fact as verified.

## References

- Shared foundation: `../bc-design/SKILL.md`
- Palette guidance: `../bc-design/references/palettes.md`
- Typography guidance: `../bc-design/references/typography.md`
- Copy and distinctiveness: `../bc-design/references/bc-design-guidelines.md`
