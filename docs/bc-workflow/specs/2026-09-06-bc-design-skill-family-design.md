# BC Design Skill Family Architecture

## Purpose

Evolve BC Design from one large skill into a modular design-intelligence family. The family should have the discoverability, searchable depth, deterministic tooling, and stack coverage of a mature UI/UX skill suite while retaining BC Design's own warm editorial visual language.

This is an architectural pattern adoption, not a content clone. No names, bundled fonts, visual assets, prose, or brand rules are copied from the reference archive.

## Product identity

BC Design remains:

- editorial, warm, restrained, and interface-first;
- subject-grounded before applying any house defaults;
- Newsreader plus Inter by default when an editorial hierarchy fits the brief;
- calm in motion, with stable streamed-text geometry and reduced-motion support;
- explicit about evidence, accessibility, responsive behavior, and verification;
- branded only as BC Design in public skill names, output, examples, and installer instructions.

Parchment and terracotta are house fallbacks, not mandatory colors for every industry. A generated direction must explain why a palette fits the subject.

## Public skill family

### `bc-design`

The primary router and shared design-intelligence skill. It handles new interface direction, redesign, restyling, and ambiguous interface requests, then routes specialized work when one capability dominates.

It owns:

- the shared searchable catalogs;
- the design-system generator and persistence contract;
- the design contract and mode-selection workflow;
- stack detection and shared delivery requirements;
- compatibility CLI entrypoint `scripts/bc_design.py`.

It must not duplicate detailed procedures owned by sibling skills.

### `bc-brand`

Use for defining, extracting, reviewing, or updating a product's brand system. It owns brand evidence, palette rationale, typography roles, voice principles, asset-usage decisions, and mapping approved brand choices into semantic design tokens.

It does not generate arbitrary logos or replace an existing brand without explicit approval.

### `bc-design-system`

Use for token architecture, component specifications, states and variants, themes, governance, and migration from raw values to semantic tokens.

It owns primitive, semantic, and component token layers; contrast-safe pairings; state matrices; component contracts; and token validation. It consumes an approved brand contract when one exists.

### `bc-ui-styling`

Use when implementing or restyling the visual layer of an existing interface without changing its product behavior. It owns stack-specific styling guidance, responsive implementation, typography delivery, component composition, and visual-state completeness.

It preserves routes, data contracts, navigation semantics, and behavior unless the user approves a broader redesign.

### `bc-design-audit`

Use for read-only design audits, accessibility reviews, responsive reviews, consistency reviews, and distinctive-quality reviews. One skill contains two explicit modes:

- `quality`: usability, accessibility, interaction, responsive layout, performance, forms, navigation, and state coverage;
- `distinctive`: generic-template patterns, subject disconnect, hierarchy monotony, decorative filler, and unearned visual effects.

Every finding carries severity, evidence location, impact, recommendation, and confidence. Audit does not silently modify targets. Requested remediation routes back through `bc-design` as redesign or restyling.

### `bc-motion`

Use for animation systems, interaction motion, loading and thinking states, page transitions, drawers, overlays, and streamed AI interfaces. It owns motion tokens, timing tiers, easing, reduced-motion alternatives, performance constraints, and stack-specific implementation notes.

Motion must communicate state or spatial continuity. Ordinary interaction motion stays within 150–250ms, structural motion within 350–400ms, and approved ambient thinking motion uses the 1800ms token. Streaming containers never animate layout dimensions.

## Internal engine

The engine remains inside `bc-design`; it is not a public skill. The compatibility entrypoint stays at `scripts/bc_design.py`, but implementation responsibilities are split into focused modules:

```text
.agents/skills/bc-design/scripts/
├── bc_design.py          # CLI parsing and dispatch only
├── core.py               # Catalog loading, tokenization, BM25 search
├── design_system.py      # Multi-domain synthesis and persistence
├── audit.py              # Structured source findings and formatters
├── contrast.py           # Color parsing and WCAG contrast calculations
└── install.py            # Runtime installation of the complete family
```

All modules use the Python standard library. Existing CLI commands remain compatible.

## Query and synthesis contract

`--design-system` must use catalog results rather than a fixed industry `if/elif` tree. It queries product, style, color, typography, landing, UX, motion, and relevant stack data, then synthesizes one coherent direction.

For each domain:

1. Search using one dominant product intent and meaningful constraints.
2. Require a minimum relevance threshold.
3. Retry once with normalized or narrower terms when the result is empty or off-topic.
4. Label a general fallback explicitly when no verified match exists.
5. Never persist an unverified result as if it were a catalog match.

The generator must correctly distinguish education, healthcare, finance, developer tools, commerce, public service, hospitality, creative work, and other catalog-supported products. A school query must not fall into the AI/SaaS default.

Supported output:

- terminal-friendly ASCII;
- Markdown suitable for `MASTER.md`;
- JSON containing resolved matches, confidence, generated tokens, verification notes, and persistence status.

## BC visual contract

The engine separates house language from subject decisions:

- House language: editorial hierarchy, calm motion, warm neutrals when appropriate, precise hairlines, restrained elevation, active copy, monoline icons, and one signature moment.
- Subject decisions: palette, type personality, density, imagery, signature interaction, and information architecture.
- Accessibility constraints: contrast-safe text/background pairs, visible focus, touch targets, readable type, and reduced motion.

Terracotta `#D97757` may be used as a background only with a contrast-safe foreground. `#FFFFFF` on `#D97757` is prohibited because its measured contrast is approximately 3.12:1. The canonical foreground on that accent is dark ink such as `#1F1E1B`, which measures approximately 5.34:1.

All documented contrast ratios must be generated or tested by the same contrast implementation used by the CLI.

## Audit contract

The audit engine returns structured findings with this interface:

```text
rule_id
severity
path
line
evidence
message
recommendation
confidence
```

CLI behavior:

- human-readable output groups findings by severity and file;
- `--json` emits stable machine-readable output;
- exit code `0` means no enforceable source findings;
- exit code `1` means findings exist;
- exit code `2` means the target or audit invocation is invalid;
- a clean source audit never claims the rendered UI is accessible or ready to ship.

The implementation must avoid false positives from comments, configuration object names, custom properties, and example text.

## Skill routing

The primary router uses the narrowest matching capability:

| User intent | Route |
| --- | --- |
| New interface, redesign, broad restyle, unclear mixed request | `bc-design` |
| Brand identity, palette rationale, typography roles, voice | `bc-brand` |
| Tokens, component architecture, variants, themes, governance | `bc-design-system` |
| CSS/UI implementation within frozen behavior | `bc-ui-styling` |
| Read-only quality or distinctive review | `bc-design-audit` |
| Animation, transitions, loading motion, streamed UI motion | `bc-motion` |

Descriptions must be mutually discriminating. Sibling skills may link to the shared BC foundation, but they remain understandable without loading every sibling.

## Installer and runtime layout

The canonical source remains `.agents/skills/`. The installer copies the complete family when the selected runtime needs a runtime-local skill directory.

```text
.agents/skills/
├── bc-design/
├── bc-brand/
├── bc-design-system/
├── bc-ui-styling/
├── bc-design-audit/
└── bc-motion/
```

The BC runtime mirror uses the same names under `.bc/skills/`. Installation remains non-destructive unless `--force` is explicitly supplied. Runtime instruction files point to the router and list the specialized skills without duplicating their full instructions.

## Migration and compatibility

- Preserve `bc_design.py`, current flags, existing persisted `MASTER.md` paths, and page override behavior.
- Move implementation behind the compatibility entrypoint incrementally with tests.
- Keep shared catalogs in one canonical location; sibling skills must not copy large CSV or JSON datasets.
- Replace conflicting or stale references rather than maintaining two sources of truth.
- Rewrite static `PASS` templates as blank evidence-based report templates.
- Update every bundled example until auditing the repository examples produces no findings.
- Synchronize `.bc` only through the installer and verify byte parity for installed skill files.

## Test strategy

### Skill structure

- Validate each `SKILL.md` frontmatter and discoverability description.
- Verify the router maps each user intent to one primary skill.
- Verify sibling references resolve and no public text contains legacy branding.

### Engine behavior

- Unit-test catalog loading, relevance thresholds, retry behavior, and fallback labeling.
- Use relevance fixtures for education, healthcare, finance, developer tools, commerce, and ambiguous prompts.
- Assert that `school education kindergarten` resolves to an education product direction.
- Verify ASCII, Markdown, and JSON outputs describe the same resolved system.

### Accessibility and tokens

- Test every canonical foreground/background pair against its documented threshold.
- Reject white text on terracotta and approve dark ink on terracotta.
- Audit canonical tokens and sibling examples with no findings.

### Audit

- Test severity, path, line, evidence, recommendation, JSON output, and exit codes.
- Maintain regression tests for generic-template rules, motion rules, streaming isolation, comments, configuration objects, and custom properties.

### Installation

- Test non-destructive installation and explicit-force behavior.
- Verify the complete skill family is installed to `.bc/skills/`.
- Verify canonical/runtime parity after installation.

### End-to-end examples

- Audit all bundled examples successfully.
- Verify at least one greenfield page, one restyle, one quality audit, one distinctive audit, and one motion-focused implementation fixture.
- Record rendered verification separately; source-audit success alone is not a visual pass.

## Delivery phases

1. Establish tests for family layout, routing, contrast truth, generator relevance, audit evidence, and installer behavior.
2. Add the specialized skills and update the router.
3. Split the CLI into internal modules while preserving compatibility.
4. Replace the hardcoded generator with catalog-backed synthesis and structured output.
5. Upgrade audit findings with severity, lines, evidence, JSON, and deterministic exit codes.
6. Correct color tokens and contradictory references.
7. Migrate every bundled example to pass the current source audit.
8. Install the family into `.bc`, validate every skill, run all tests, and report any visual surfaces not rendered.

## Out of scope for this architecture

- Bundled proprietary or custom fonts.
- Copying assets or prose from the reference archive.
- General-purpose slide, banner, logo, or corporate-identity generation unrelated to interface design.
- Package installation, deployment, or unrelated operating-system changes.
- Claiming visual or accessibility completion without rendered evidence.

These can become separate BC capabilities later only when a real user workflow requires them.
