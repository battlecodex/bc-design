# BC Design Skill Family Implementation Plan

> **For implementation:** Execute this plan task-by-task with review checkpoints. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn BC Design into a modular family of interoperable skills with catalog-backed synthesis, evidence-based audits, and preserved CLI/runtime compatibility.

**Architecture:** Keep `bc-design` as the public router and shared data owner. Add focused sibling skills for brand, design-system, UI styling, audit, and motion; keep their instructions thin and link them to shared references. Split the Python CLI behind its current entrypoint into focused standard-library modules, then install the full family into `.bc/skills/`.

**Tech Stack:** Python 3 standard library, Markdown/YAML skill files, CSV/JSON catalogs, CSS/HTML/JS source heuristics, `unittest`, PowerShell verification.

**Spec:** `docs/bc-workflow/specs/2026-09-06-bc-design-skill-family-design.md`

## Global Constraints

- Preserve `scripts/bc_design.py` and its current flags, persistence paths, and exit-code compatibility unless a new behavior is explicitly covered by tests.
- Keep the canonical source under `.agents/skills/`; install the complete family under `.bc/skills/` through `scripts/install.py`.
- Use only Python standard-library dependencies for the skill engine and installer.
- Keep BC Design as the public identity; do not copy the reference archive's names, prose, fonts, or assets.
- Use subject-grounded decisions first; parchment/terracotta are fallbacks, not universal outputs.
- Enforce accessible contrast, visible focus, reduced motion, stable streamed geometry, and meaningful interface copy.
- Write tests before production changes and run the relevant test after every task.

---

### Task 1: Lock the skill-family contract with failing tests

**Files:**
- Modify: `tests/test_bc_design.py`
- Modify: `tests/test_bc_design_rebrand.py`
- Modify: `tests/test_bc_design_workflow.py`

**Interfaces:**
- Produces structural expectations for six public skill directories, router descriptions, and installer parity.

- [ ] **Step 1: Write failing tests** for sibling directory names, required frontmatter, router mapping, and no duplicate large catalog copies.
- [ ] **Step 2: Run the focused tests and confirm they fail because sibling skills do not exist.**
- [ ] **Step 3: Keep the tests focused on observable structure, not exact prose.**

### Task 2: Add the focused BC Design sibling skills

**Files:**
- Create: `.agents/skills/bc-brand/SKILL.md`
- Create: `.agents/skills/bc-design-system/SKILL.md`
- Create: `.agents/skills/bc-ui-styling/SKILL.md`
- Create: `.agents/skills/bc-design-audit/SKILL.md`
- Create: `.agents/skills/bc-motion/SKILL.md`
- Modify: `.agents/skills/bc-design/SKILL.md`

**Interfaces:**
- Each sibling exposes a discriminating `Use when...` description and a focused workflow.
- The router links to sibling paths without copying their complete instructions.

- [ ] **Step 1: Write the smallest skill bodies that satisfy the failing structure tests.**
- [ ] **Step 2: Add routing guidance and preserve the five existing BC modes.**
- [ ] **Step 3: Run the focused structure tests and `quick_validate.py` for every new skill.**

### Task 3: Make installer/runtime support the complete family

**Files:**
- Modify: `.agents/skills/bc-design/scripts/install.py`
- Modify: `tests/test_bc_design.py`
- Modify: `.agents/skills/bc-design/SKILL.md`

**Interfaces:**
- `install_runtime("bc", workspace, force=False)` copies all six skill directories into `.bc/skills/`.
- Existing non-destructive behavior and runtime instruction targets remain intact.

- [ ] **Step 1: Add failing tests for complete BC runtime family copy and canonical/runtime parity.**
- [ ] **Step 2: Run the focused installer tests and verify the family-copy assertion fails.**
- [ ] **Step 3: Implement a single `SKILL_FAMILY` list and copy it without duplicating catalogs.**
- [ ] **Step 4: Run installer tests and confirm non-force preservation still passes.**

### Task 4: Split the CLI behind the compatibility entrypoint

**Files:**
- Create: `.agents/skills/bc-design/scripts/core.py`
- Create: `.agents/skills/bc-design/scripts/design_system.py`
- Create: `.agents/skills/bc-design/scripts/contrast.py`
- Create: `.agents/skills/bc-design/scripts/audit.py`
- Modify: `.agents/skills/bc-design/scripts/bc_design.py`
- Modify: `tests/test_bc_design.py`

**Interfaces:**
- `core.py` exposes catalog loading/search helpers.
- `contrast.py` exposes `parse_hex_color`, `compute_contrast`, and related helpers.
- `audit.py` exposes structured audit helpers while retaining compatibility wrappers in `bc_design.py`.
- `design_system.py` exposes generator/persistence helpers used by the CLI.

- [ ] **Step 1: Add import/parity tests that define the module boundaries.**
- [ ] **Step 2: Run them RED against the current monolithic entrypoint.**
- [ ] **Step 3: Move pure helpers with compatibility imports, preserving output and flags.**
- [ ] **Step 4: Run the complete existing suite and compare representative CLI output.**

### Task 5: Replace hardcoded industry branching with catalog-backed synthesis

**Files:**
- Modify: `.agents/skills/bc-design/scripts/core.py`
- Modify: `.agents/skills/bc-design/scripts/design_system.py`
- Modify: `.agents/skills/bc-design/scripts/bc_design.py`
- Modify: `tests/test_bc_design.py`

**Interfaces:**
- `search_domain` supports all catalog domains, including `motion`, `icons`, `google-fonts`, and stacks where data exists.
- `generate_design_system` resolves product/style/color/type/pattern/motion evidence before fallback.
- Empty or off-topic results produce an explicit fallback note.

- [ ] **Step 1: Add failing relevance tests for education, healthcare, finance, developer tools, commerce, and an ambiguous prompt.**
- [ ] **Step 2: Verify `school education kindergarten` currently resolves to the generic fallback.**
- [ ] **Step 3: Implement normalized multi-domain retrieval with a relevance threshold and one retry.**
- [ ] **Step 4: Add JSON and Markdown render modes with shared resolved data.**
- [ ] **Step 5: Run relevance and output-format tests.**

### Task 6: Correct contrast truth and contradictory references

**Files:**
- Modify: `.agents/skills/bc-design/references/tokens.css`
- Modify: `.agents/skills/bc-design/references/ux-guidelines.md`
- Modify: `.agents/skills/bc-design/references/bc-design-rules.md`
- Modify: `.agents/skills/bc-design/references/bc-design-guidelines.md`
- Modify: `.agents/skills/bc-design/scripts/bc_design.py`
- Modify: `tests/test_bc_design.py`

**Interfaces:**
- Canonical accent foreground/background pairs are contrast-tested by the same CLI implementation.
- Static report templates never claim an unconditional pass.
- Public guidance no longer recommends decorative glyphs or middle-dot metadata that the audit rejects.

- [ ] **Step 1: Add failing contrast/document consistency tests.**
- [ ] **Step 2: Verify white-on-terracotta and stale report claims fail.**
- [ ] **Step 3: Replace unsafe foregrounds, generated ratio claims, and contradictory examples with evidence-based wording.**
- [ ] **Step 4: Run contrast and documentation tests.**

### Task 7: Upgrade audit findings with evidence and JSON

**Files:**
- Modify: `.agents/skills/bc-design/scripts/audit.py`
- Modify: `.agents/skills/bc-design/scripts/bc_design.py`
- Modify: `tests/test_bc_design.py`
- Modify: `.agents/skills/bc-design/SKILL.md`
- Modify: `.agents/skills/bc-design/references/bc-design-workflow.md`

**Interfaces:**
- Findings include `rule_id`, `severity`, `path`, `line`, `evidence`, `message`, `recommendation`, and `confidence`.
- `--audit TARGET --json` emits stable JSON.
- Exit code `0` means clean, `1` findings, `2` invalid target/invocation.

- [ ] **Step 1: Add failing tests for line-aware human output, JSON shape, severity, and invalid-target exit code.**
- [ ] **Step 2: Verify the current audit output lacks these fields.**
- [ ] **Step 3: Implement line/evidence extraction and deterministic formatters.**
- [ ] **Step 4: Preserve current rule IDs and existing human-readable output semantics.**
- [ ] **Step 5: Run audit tests against fixtures and canonical tokens.**

### Task 8: Migrate bundled examples and enforce end-to-end quality

**Files:**
- Modify: `examples/bc-chat.html`
- Modify: `examples/bc-dashboard.html`
- Modify: `examples/bc-erp.html`
- Modify: `examples/bc-landing-page.html`
- Modify: `examples/login-page.html`
- Modify: `tests/test_school_landing.py`
- Modify: `tests/test_bc_design.py`

**Interfaces:**
- All bundled examples pass the current source audit.
- Existing examples keep their content and functional intent while adopting semantic tokens, safe copy, and reduced-motion support.

- [ ] **Step 1: Add an all-examples audit regression test.**
- [ ] **Step 2: Run it RED and record every file/rule.**
- [ ] **Step 3: Remediate each finding in small file-local patches.**
- [ ] **Step 4: Run all example audits and existing tests.**

### Task 9: Final validation and runtime synchronization

**Files:**
- Modify: `.bc/skills/` generated mirror via installer
- Modify: `BC.md` generated instruction via installer
- Modify: `docs/bc-workflow/README.md` if a family index is needed

- [ ] **Step 1: Run the installer with `--force` for the BC runtime.**
- [ ] **Step 2: Run `quick_validate.py` on every canonical sibling skill.**
- [ ] **Step 3: Run the full unit suite and Python compile checks.**
- [ ] **Step 4: Audit all examples and canonical references.**
- [ ] **Step 5: Verify canonical/runtime byte parity and report any visual surfaces not browser-verified.**
