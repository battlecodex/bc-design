# BC Design Workflow

Use this reference after selecting a mode in `SKILL.md`. The workflow keeps visual decisions grounded in the brief, preserves approved scope, and leaves an evidence trail from baseline to verification.

## Operating contract

| Mode | Observable trigger | Primary outcome |
| --- | --- | --- |
| Greenfield | A new page, product, component, or design system has no visual baseline | Approved design contract, implementation plan, and shipped interface |
| Redesign | An existing interface needs better hierarchy, usability, conversion, accessibility, or clarity | Before/after direction with useful behavior preserved |
| Restyling | Structure and behavior stay stable while visual language changes | Token/component restyle with frozen invariants |
| Design audit | The user asks whether an interface is usable, accessible, consistent, responsive, or performant | Prioritized findings with evidence and remediation guidance |
| Distinctive review | The user asks whether a design feels generic or disconnected from its subject | Subject-grounded pattern review with a clear verdict |
| Study | The user shares a URL or screenshot of a design they admire and wants its direction | Diagnosis of structure and tokens mapped onto BC roles, following [project-memory.md](./project-memory.md) § Study |

Do not silently change modes. If a redesign reveals a new product surface, reclassify that surface as greenfield. If a restyle needs interaction or layout changes, record the scope expansion and obtain approval.

## Universal sequence

Each mode uses the same quality gate: baseline, approved design contract, implementation evidence, and verification report.
There is no unconditional pass: a clean checklist still requires evidence from the relevant rendered states.

0. **Run pre-flight.** Run `project.py preflight`. Read `DESIGN.md` first when it exists, show the findings with what will be preserved, and check `project.py log` before choosing a signature moment. See [project-memory.md](./project-memory.md).
1. **Frame the request.** Capture product, audience, context, platform, stack, existing artifacts, constraints, and success criteria. State assumptions that could affect direction.
2. **Establish the baseline.** For new work, baseline means the brief and subject matter. For existing work, inspect files, routes, tokens, screenshots, responsive states, and known defects.
3. **Commit to one direction.** Before writing code, state in two or three sentences the subject, the house accent chosen for it, and the one signature moment (a spatial 3D stage, an orchestrated sequence, a scroll narrative, or editorial imagery). Name what the page will deliberately leave out. A direction that could describe any product is not a direction.
4. **Present the direction.** Share the mode, key decisions, alternatives where meaningful, and proposed scope. Obtain approval before creative implementation or behavior changes.
5. **Choose references progressively.** Run `bc_design.py --design-system` for a system-wide direction. Read `bc-design-guidelines.md` for subject and generic-pattern checks, `ux-guidelines.md` for usability checks, and the detected stack guide for implementation details.
6. **Write the design contract.** Record hierarchy, type pairing, semantic tokens, responsive behavior, interaction states, motion budget, accessibility requirements, and rejected patterns.
7. **Plan multi-step work.** When work spans multiple files, pages, states, or independently testable changes, write an implementation plan naming files, interfaces, tests, and verification commands.
8. **Implement in small slices.** Update shared tokens and components before one-off screens. Write a failing test for behavior changes, implement the smallest change, and rerun the relevant suite. Keep streamed-text geometry stable.
9. **Review the result.** Check the design contract, run the CLI audit when source artifacts exist, run `render_check.py` on each rendered page, and inspect the screenshots for responsive, keyboard, reduced-motion, loading, error, empty, and streamed states.
10. **Verify before handoff.** Run fresh checks and report actual results. Never claim complete, accessible, or passing without evidence.
11. **Handoff safely.** Report changed paths, commands, observed results, limitations, and any remaining user decision. Record the build with `project.py record`, and when no `DESIGN.md` exists, offer in one line to lock the system; write it only if the user agrees.

## Stop conditions

Stop and ask the user when:

- the target, platform, or artifact is missing and guessing would change the direction;
- a proposed change alters behavior, content, navigation, data, or accessibility semantics outside approved scope;
- a check fails and its cause is not understood;
- an audit has no inspectable artifact; provide a limited review and label it not verified;
- a quick pass would skip the design contract, approval, or verification gate.

## Greenfield

1. Frame product, audience, context, platform, stack, and content density.
2. Run `bc_design.py "<product> <industry> <keywords>" --design-system`; verify the product, style, color, and type fit before persisting.
3. Read the matched palette, typography, landing, UX, and stack references. Keep one signature moment and vary hierarchy across the page.
4. Present and approve a contract covering information hierarchy, responsive layout, semantic tokens, states, motion, accessibility, and copy.
5. Plan and implement when the work spans more than one independently testable change.
6. Verify 375px, 768px, 1024px, and 1440px plus keyboard, reduced-motion, contrast, empty, loading, error, and streaming states.

Minimum output: baseline brief, approved design contract, implementation plan when needed, implementation, and verification report.

## Redesign

1. Inventory routes/screens, components, tokens, content hierarchy, responsive behavior, and interactions. Capture screenshots or equivalent evidence when available.
2. Separate invariants from opportunities. Preserve data, permissions, navigation, and interaction contracts unless explicitly changed.
3. State the problem with evidence and define observable success criteria. Offer alternatives only when a real trade-off exists.
4. Present the redesign contract with an exact change list and obtain approval.
5. Implement in comparable vertical slices. Add regression tests or snapshots for preserved behavior.
6. Recheck the original defect across responsive, keyboard, error, loading, and reduced-motion states.

Minimum output: baseline inventory, invariant list, evidence-backed contract, implementation plan, and before/after verification report.

## Restyling

1. Freeze content, routes, component states, interaction semantics, and layout constraints as invariants.
2. Map raw values to semantic tokens: canvas, surface, text, border, accent, focus, status, type, radius, shadow, and motion.
3. Select palette and type from the subject and data results. Prefer tokens over raw values inside components.
4. Present a token-first contract and call out any unavoidable layout or copy change. Obtain approval for exceptions.
5. Update tokens and shared components before one-off screens. Compare preserved states before accepting visual drift.
6. Verify contrast, focus visibility, touch targets, wrapping, reduced-motion, and streaming isolation.

Minimum output: frozen invariants, semantic token map, approved restyle contract, and verification report.

## Design audit

1. Define the target and stack. Inspect source, rendered states, screenshots, and tokens; record what was not observable.
2. Evaluate every dimension in [design-dimensions.md](./design-dimensions.md): the twelve UI dimensions and the six UX dimensions, plus performance/CLS and data displays where they apply.
3. Run `bc_design.py --audit TARGET` for enforceable source heuristics, including template chrome, Unicode icon glyphs, decorative index markers, focus-ring width, sticky-layer tokens, motion duration/easing budgets, reduced-motion support, and streaming-layout isolation. A CLI pass is one signal, not proof of rendered correctness.
4. Report each finding with severity (P0–P3), evidence location, affected user, impact, recommended fix, and confidence. Do not silently waive a finding; only an explicit user request recorded in the contract can justify a deviation.
5. Do not modify the target during an audit. If fixes are requested, switch to redesign or restyling and repeat the universal sequence.

Minimum output: audit scope, inspected artifacts and gaps, prioritized findings, and verification report or explicit not-verified status.

## Distinctive review

1. Read `bc-design-guidelines.md` and identify the subject, materials, vernacular, audience, and intended signature moment.
2. Check palette fit, dark-surface restraint, hierarchy variety, interface language, type purpose, emphasis balance, copy clarity, streaming stability, and header wrapping.
3. Compare the design against its subject. Explain why a technically valid choice may still feel generic or culturally wrong.
4. Report each finding as pattern, concrete evidence, impact on identity or usability, smallest corrective direction, and confidence.
5. Do not redesign while reviewing. If remediation is requested, create a redesign/restyle contract that preserves the evidence and obtains approval first.

Minimum output: subject-grounding assessment, per-pattern evidence table, prioritized verdict, and verification limits.

## Deliverable templates

### Design contract

```text
Mode and scope:
Baseline and success criteria:
Invariants / approved changes:
Hierarchy and responsive behavior:
Semantic tokens and typography:
Interaction, accessibility, motion, and streaming constraints:
UI dimensions (color, typography, layout, spacing, hierarchy, imagery, shape, components, states, motion, responsiveness, accessibility):
UX dimensions (users and assumptions, information architecture, main flow, prototype plan, UX writing, usability tasks):
Rejected patterns and why:
Approval status:
```

### Audit finding

```text
[P1] Rule/pattern — short title
Evidence: file, selector, route, screenshot state, or missing artifact
Impact: who is affected and how
Recommendation: smallest actionable correction
Confidence: high / medium / low
```

### Verification report

```text
Commands/checks run:
Observed results:
Design-dimensions scorecard (see design-dimensions.md):
Design-contract checks:
Unverified surfaces or limitations:
Remaining user decision:
```
