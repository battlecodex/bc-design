# BC Design Catalog Alignment Implementation Plan

> **For agentic workers:** Execute this plan task-by-task with test-first changes and a review checkpoint after every task.

**Goal:** Ensure BC Design keeps its broad design-intelligence catalogs while every automatic recommendation follows the BC editorial visual language unless the user explicitly requests another direction.

**Architecture:** Add a policy layer between catalog retrieval and recommendation output. Catalog rows remain reference knowledge; normalized compatibility metadata, intent detection, and deterministic ranking decide whether an entry is core, compatible, conditional, or excluded. The generator and audit consume the same policy so documentation, recommendations, and enforcement cannot drift.

**Tech Stack:** Python standard library, CSV/JSON catalogs, `unittest`, Markdown skill instructions.

**Spec:** `DESIGN.md`

## Global Constraints

- Public brand name is BC Design.
- Newsreader + Inter is the open-source default pairing, not an unbreakable brand override.
- Automatic output is neutral-first, editorial, restrained, accessible, and subject-grounded.
- Terracotta, sage, parchment, white, and warm black are options rather than universal requirements.
- Conditional or excluded styles require an explicit user request and must retain accessibility gates.
- The CLI remains zero-dependency at runtime.
- `.agents/skills` is canonical; `.bc/skills` must remain byte-equivalent in releases.

---

### Task 1: Define the compatibility taxonomy and contract

**Files:**
- Create: `.agents/skills/bc-design/data/bc-alignment-policy.json`
- Create: `.agents/skills/bc-design/references/catalog-alignment.md`
- Modify: `.agents/skills/bc-design/references/visual-language.md`
- Test: `tests/test_catalog_alignment.py`

**Interfaces:**
- Produces: four statuses—`core`, `compatible`, `conditional`, `excluded`—and explicit-request rules consumed by Task 2.

- [x] Write a failing test requiring the policy file, four statuses, recognized BC traits, conflict traits, and a schema version.
- [x] Run `py -3 -m unittest tests.test_catalog_alignment.CatalogAlignmentTests.test_policy_schema -v`; expect failure because the policy does not exist.
- [x] Add `bc-alignment-policy.json` with `schemaVersion`, `statuses`, `coreTraits`, `conflictTraits`, `explicitRequestSignals`, and `qualityGates`.
- [x] Document that catalog breadth is reference knowledge and compatibility status controls automatic selection.
- [x] Run the focused test and confirm it passes.

### Task 2: Implement one shared alignment engine

**Files:**
- Create: `.agents/skills/bc-design/scripts/alignment.py`
- Modify: `.agents/skills/bc-design/scripts/core.py`
- Test: `tests/test_catalog_alignment.py`

**Interfaces:**
- Produces: `classify_entry(domain: str, row: dict) -> AlignmentResult` and `explicit_direction_requested(query: str, row: dict) -> bool`.
- `AlignmentResult` fields: `status`, `score`, `matched_traits`, `conflicts`, and `reason`.

- [x] Write failing tests classifying editorial minimalism as `core`, a restrained adjacent style as `compatible`, Claymorphism as `conditional`, and inaccessible/decorative combinations as `excluded`.
- [x] Add tests proving explicit requests unlock `conditional` entries but never bypass accessibility requirements.
- [x] Run the tests and confirm they fail because `alignment.py` is absent.
- [x] Implement deterministic token/field matching using only the standard library; keep thresholds in the JSON policy.
- [x] Add `alignment` metadata to results returned by `search_domain` without removing existing fields.
- [x] Run focused tests and existing catalog-search tests.

### Task 3: Make ranking BC-aware without destroying catalog breadth

**Files:**
- Modify: `.agents/skills/bc-design/scripts/core.py`
- Modify: `.agents/skills/bc-design/scripts/bc_design.py`
- Test: `tests/test_catalog_alignment.py`

**Interfaces:**
- Produces: `search_domain(domain, query, max_results=3, selection_mode="automatic")`.
- `selection_mode` values: `automatic` and `explicit`.

- [x] Write failing ranking tests for education, finance, healthcare, developer tools, and editorial publishing prompts.
- [x] Require automatic mode to rank `core` then `compatible`, suppress `conditional`, and reject `excluded`.
- [x] Require explicit style terms such as `brutalist`, `claymorphism`, or `material 3` to enable matching conditional rows.
- [x] Implement a compatibility multiplier after BM25 scoring and before final sorting.
- [x] Make design-system generation explain the chosen status and subject evidence.
- [x] Run the focused ranking matrix and all existing CLI tests.

### Task 4: Normalize every catalog row

**Files:**
- Create: `.agents/skills/bc-design/scripts/normalize_catalog.py`
- Create: `.agents/skills/bc-design/data/alignment-overrides.json`
- Modify: `.agents/skills/bc-design/data/catalog-summary.json`
- Test: `tests/test_catalog_alignment.py`

**Interfaces:**
- Produces: a deterministic report containing counts by domain/status, unclassified rows, conflicts, and override coverage.

- [x] Write a failing test requiring all 88 styles, 192 palettes, 74 typography pairings, 119 UX rules, 25 charts, 17 motion rows, and 22 stack catalogs to receive a status.
- [x] Implement normalization as a read-only report command first: `py -3 .../normalize_catalog.py --check`.
- [x] Add narrowly scoped overrides only where field-based classification is ambiguous; every override must include `reason`.
- [x] Fail `--check` on unclassified rows, invalid statuses, missing reasons, duplicate identities, or inaccessible core recommendations.
- [x] Store status totals in `catalog-summary.json` and run the full coverage test.

### Task 5: Unify stack support and correct the 22-stack claim

**Files:**
- Modify: `.agents/skills/bc-design/scripts/core.py`
- Modify: `.agents/skills/bc-design/scripts/bc_design.py`
- Modify: `.agents/skills/bc-design/SKILL.md`
- Modify: `README.md`
- Test: `tests/test_stack_catalogs.py`

**Interfaces:**
- Produces: `search_stack(stack: str, query: str | None, max_results=10) -> dict`.
- CLI: `--stack` accepts every stem found in `data/stacks/*.csv` rather than a hard-coded list.

- [x] Write a failing matrix test invoking all 22 stack names and asserting useful output.
- [x] Implement stack discovery and CSV search; use a focused Markdown guide when available and catalog guidance otherwise.
- [x] Make `--stack unknown` return a nonzero exit with the available names.
- [x] Update documentation to distinguish eight focused guides from 22 searchable stack catalogs.
- [x] Run the 22-stack matrix and installer regression suite.

### Task 6: Strengthen distinctive-quality auditing

**Files:**
- Modify: `.agents/skills/bc-design/scripts/audit.py`
- Modify: `.agents/skills/bc-design/scripts/bc_design.py`
- Modify: `.agents/skills/bc-design/references/bc-design-guidelines.md`
- Test: `tests/test_distinctive_audit.py`

**Interfaces:**
- Produces confidence-scored findings grouped under `identity`, `hierarchy`, `decoration`, `copy`, `motion`, and `accessibility`.

- [x] Add failing fixtures for repeated card geometry, excessive pills, unearned gradients/glows, decorative eyebrow overload, oversized hero displacement, copied platform chrome, accent-surface domination, and repeated generic CTA labels.
- [x] Add negative fixtures showing legitimate cards, tags, white canvases, gradients, and subject-requested conditional styles remain valid.
- [x] Implement cross-file aggregate checks separately from high-confidence single-line checks.
- [x] Keep aesthetic findings as warnings with evidence; accessibility and streaming violations remain errors.
- [x] Run the audit fixtures and confirm JSON findings include location, evidence, recommendation, and confidence.

### Task 7: Add behavioral release gates and honest metrics

**Files:**
- Create: `tests/fixtures/prompts/catalog-alignment.json`
- Modify: `tests/test_production_readiness.py`
- Modify: `scripts/package.py`
- Modify: `skill.json`
- Modify: `README.md`

**Interfaces:**
- Produces: a release report with catalog totals, classification totals, prompt-matrix results, mirror parity, installer results, and archive hash.

- [x] Add a prompt matrix covering greenfield, redesign, restyling, quality audit, distinctive review, explicit conditional style, and conflicting requests.
- [x] Test observable output invariants rather than exact prose: selected status, evidence, accessibility gates, and absence of unauthorized overrides.
- [x] Add a package preflight that refuses release when normalization, mirror parity, or metadata validation fails; run the test suite as a separate release gate.
- [x] Update `skill.json` metrics from computed data during packaging rather than maintaining hand-written totals.
- [x] Run the repository test modules and require zero failures.
- [x] Run all six skill validators and require six passes.
- [x] Build twice and require identical SHA-256 hashes.
- [x] Install all runtimes into a clean temporary workspace and verify all six skills and instruction files resolve.

### Task 8: Mirror, documentation, and release

**Files:**
- Update: `.bc/skills/bc-*` from canonical `.agents/skills/bc-*`
- Update: `DESIGN.md`
- Update: `README.md`
- Update: `skill.json`

**Interfaces:**
- Consumes all completed tasks and produces the release archive.

- [x] Sync the complete skill family only after canonical tests pass.
- [x] Run byte-parity verification across all six skill directories.
- [x] Confirm public documentation never claims every catalog entry is part of the BC core identity.
- [x] Document exact totals for `core`, `compatible`, `conditional`, and `excluded` entries.
- [x] Build `dist/bc-design-<version>.zip` and record its SHA-256.
- [x] Do not publish or push until the archive passes every release gate.

## Completion criteria

- Every shipped catalog row has a deterministic compatibility status.
- Automatic recommendations contain only `core` or `compatible` entries.
- Conditional styles appear only after an explicit request.
- Excluded combinations never bypass accessibility gates.
- All 22 stack catalogs are reachable through the CLI.
- Audit results distinguish objective failures from aesthetic warnings.
- Documentation reports computed metrics and states the eight-guide/22-catalog distinction.
- Full tests, validators, clean-room installation, mirror parity, and reproducible packaging pass.
