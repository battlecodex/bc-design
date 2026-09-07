---
name: bc-design-audit
description: Use when performing a read-only quality, accessibility, responsive, consistency, or distinctive-pattern audit of an interface or design source.
---

# BC Design Audit

Use this skill to inspect before changing. Choose one explicit mode so a usability finding is not confused with a distinctive-quality opinion.

## Modes

- **Quality:** accessibility, interaction, responsive behavior, performance/CLS, typography, forms, navigation, states, motion, and 3D spatial safety (canvas pointer pass-through, mobile DPR capping, and WebGL lifecycle teardown).
- **Distinctive:** subject fit, authentic physical metaphors vs generic gimmicks, hierarchy monotony, decorative filler, copy, and unearned visual effects.

## Workflow

1. Establish scope, stack, routes, source files, screenshots, and unverified surfaces.
2. Run `bc_design.py --audit TARGET`; use `--json` when findings need machine processing.
3. Inspect the rendered states at required breakpoints and with keyboard/reduced-motion settings when available.
4. Report each finding with severity, exact evidence location, affected user, impact, smallest recommendation, and confidence.
5. Do not modify the target during an audit. If remediation is requested, route it back to `bc-design` as redesign or restyling.

## Non-negotiables

- A clean source audit is not a claim that the rendered interface is accessible or ready to ship.
- Do not silently waive a finding; record an explicit user-approved exception.
- Distinguish a real product constraint from an aesthetic preference.
- Ignore comments, disabled examples, and configuration object names when judging source evidence.

## References

- Shared foundation: `../bc-design/SKILL.md`
- Audit workflow: `../bc-design/references/bc-design-workflow.md`
- UX checks: `../bc-design/references/ux-guidelines.md`
- Distinctive checks: `../bc-design/references/bc-design-guidelines.md`
