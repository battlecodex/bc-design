# BC Design Skill Repair Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use bc-workflow:subagent-driven-development (recommended) or bc-workflow:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the BC Design CLI, installer, and documentation executable, safe, and consistent with the project design rules.

**Architecture:** `bc_design.py` derives all packaged-resource paths from its own skill directory. Its audit operates on user-provided source files and yields a meaningful status. `install.py` provides deterministic, non-destructive integration setup for every runtime claimed by the skill. Standard-library `unittest` tests drive all behavior through public commands and functions.

**Tech Stack:** Python 3 standard library (`argparse`, `pathlib`, `unittest`, `subprocess`, `tempfile`, `shutil`).

**Spec:** `docs/bc-workflow/specs/2026-09-06-bc-design-repair-design.md`

## Global Constraints

- No third-party dependencies.
- Resource paths resolve from `.agents/skills/bc-design`, never the process working directory.
- Light canvas is `#FAF9F5`; no generated light surface uses `#FFFFFF`.
- Every dark-dialog CTA specifies `#FFFFFF` with `#1F1E1B` text.
- Audit fails non-zero on violations and never returns an unconditional pass.
- Persistence and installer writes preserve existing content unless `--force` is explicit.
- The workspace is not a Git checkout; do not include commit steps.

---

### Task 1: Establish CLI resource-path and token regression tests

**Files:**
- Create: `tests/test_bc_design.py`
- Modify: `.agents/skills/bc-design/scripts/bc_design.py:40-42, 196-201, 276`

**Interfaces:**
- Consumes: `generate_design_system(query)` and `search_domain(domain, query)` from `bc_design.py`.
- Produces: test coverage for `SKILL_ROOT`, `DATA_DIR`, domain lookup, stack lookup, and generated canonical tokens.

- [ ] **Step 1: Write the failing tests**

```python
def test_domain_search_uses_bundled_data():
    result = module.search_domain("color", "wealth management")
    self.assertNotIn("error", result)
    self.assertGreater(result["count"], 0)

def test_design_generator_does_not_emit_white_light_surface_or_nonwhite_dark_cta():
    card, _ = module.generate_design_system("developer IDE")
    self.assertNotIn("Surface: Pure White", card)
    self.assertIn("Canvas:  #FAF9F5", card)
    self.assertIn("CTA Dark:   #FFFFFF", card)
    self.assertIn("text #1F1E1B", card)
```

- [ ] **Step 2: Run the tests to verify failure**

Run: `python -m unittest tests.test_bc_design.BCDesignTests.test_domain_search_uses_bundled_data tests.test_bc_design.BCDesignTests.test_design_generator_uses_canonical_light_surface_and_dark_dialog_cta -v`

Expected: the domain test reports the duplicated data directory; token test finds the current white surface or nonwhite CTA.

- [ ] **Step 3: Implement the minimal path and token repair**

```python
SKILL_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = SKILL_ROOT / "data"

# Reuse SKILL_ROOT / "stacks" / f"{args.stack}.md" for --stack.
# Make `cta_dark` consistently `#FFFFFF (text #1F1E1B)` and replace the
# generator's light surface with `#FAF9F5`.
```

- [ ] **Step 4: Run the tests to verify success**

Run: `python -m unittest tests.test_bc_design -v`

Expected: both tests pass.

### Task 2: Replace the unconditional delivery report with a real audit

**Files:**
- Modify: `.agents/skills/bc-design/scripts/bc_design.py:398-480`
- Modify: `tests/test_bc_design.py`

**Interfaces:**
- Consumes: `audit_target(target: Path) -> list[Violation]` and CLI `--audit TARGET` / `--delivery-gate TARGET`.
- Produces: stdout listing each rule violation and an exit code of 0 for clean files or 1 for violations.

- [ ] **Step 1: Write failing subprocess tests**

```python
def test_audit_rejects_known_generic_pattern_and_streaming_layout_violations(self):
    target.write_text(".card { @apply rounded-xl p-6; }\n.stream { transition: height 200ms; }")
    completed = run_cli("--audit", str(target))
    self.assertEqual(completed.returncode, 1)
    self.assertIn("monotonous-card-kit", completed.stdout)
    self.assertIn("streaming-layout-animation", completed.stdout)

def test_audit_reports_clean_target_as_pass(self):
    target.write_text(".surface { background: #FAF9F5; }")
    completed = run_cli("--audit", str(target))
    self.assertEqual(completed.returncode, 0)
    self.assertIn("PASS", completed.stdout)
```

- [ ] **Step 2: Run tests to verify failure**

Run: `python -m unittest tests.test_bc_design.BCDesignTests.test_audit_rejects_known_generic_pattern_and_streaming_layout_violations tests.test_bc_design.BCDesignTests.test_audit_reports_clean_target_as_pass -v`

Expected: current CLI accepts no audit target and prints unconditional PASS.

- [ ] **Step 3: Implement a targeted, explainable audit**

```python
def audit_target(target: Path) -> list[tuple[str, str, Path]]:
    violations = []
    for source_file in iter_source_files(target):
        content = source_file.read_text(encoding="utf-8", errors="ignore")
        violations.extend(find_audit_violations(content, source_file))
    return violations
```

`--audit` and `--delivery-gate` take one required path. Missing or nonexistent targets print an error and return status 2. The report may say PASS only when the scan produces no violations.

- [ ] **Step 4: Run the audit tests to verify success**

Run: `python -m unittest tests.test_bc_design -v`

Expected: violation and clean-target tests pass; no unconditional delivery-report path remains.

### Task 3: Make persisted page overrides non-destructive

**Files:**
- Modify: `.agents/skills/bc-design/scripts/bc_design.py:327-368`
- Modify: `tests/test_bc_design.py`

**Interfaces:**
- Consumes: `persist_master(data, output_dir, page, force)`.
- Produces: a return status / message that states whether `MASTER.md` or page override was created, skipped, or overwritten.

- [ ] **Step 1: Write failing tests**

```python
def test_page_override_is_not_overwritten_without_force(self):
    module.persist_master(DATA, output_dir=self.tempdir, page="dashboard")
    page.write_text("existing decision")
    module.persist_master(DATA, output_dir=self.tempdir, page="dashboard")
    self.assertEqual(page.read_text(), "existing decision")

def test_page_name_cannot_escape_pages_directory(self):
    with self.assertRaises(ValueError):
        module.persist_master(DATA, output_dir=self.tempdir, page="../escape")
```

- [ ] **Step 2: Run tests to verify failure**

Run: `python -m unittest tests.test_bc_design.BCDesignTests.test_page_override_is_not_overwritten_without_force tests.test_bc_design.BCDesignTests.test_page_name_cannot_escape_pages_directory -v`

Expected: current code overwrites the page and accepts traversal.

- [ ] **Step 3: Implement validation and overwrite guard**

Use a slug validator that accepts only alphanumeric, underscore, and hyphen page names; check both destination files before writing; only replace an existing file when `force=True`.

- [ ] **Step 4: Run persistence tests to verify success**

Run: `python -m unittest tests.test_bc_design -v`

Expected: existing files remain intact unless a test passes `force=True`.

### Task 4: Implement the documented installer and test all runtime targets

**Files:**
- Create: `.agents/skills/bc-design/scripts/install.py`
- Modify: `tests/test_bc_design.py`
- Modify: `.agents/skills/bc-design/SKILL.md:70-95`

**Interfaces:**
- Consumes: `install.py --ai {bc,cursor,windsurf,antigravity,copilot,kiro,codex,qoder,vscode,all} --workspace PATH [--force]`.
- Produces: only documented instruction files; runs are idempotent without `--force`.

- [ ] **Step 1: Write failing installer tests**

```python
def test_install_all_creates_every_documented_runtime_target(self):
    completed = run_installer("--ai", "all", "--workspace", self.tempdir)
    self.assertEqual(completed.returncode, 0)
    for path in DOCUMENTED_TARGETS:
        self.assertTrue((Path(self.tempdir) / path).exists())

def test_installer_preserves_existing_file_without_force(self):
    target.write_text("user content")
    run_installer("--ai", "cursor", "--workspace", self.tempdir)
    self.assertEqual(target.read_text(), "user content")
```

- [ ] **Step 2: Run installer tests to verify failure**

Run: `python -m unittest tests.test_bc_design.BCDesignTests.test_install_all_creates_every_documented_runtime_target tests.test_bc_design.BCDesignTests.test_installer_preserves_existing_file_without_force -v`

Expected: subprocess fails because `scripts/install.py` does not exist.

- [ ] **Step 3: Implement the installer**

`install.py` uses `Path`, `argparse`, and `shutil`. It has a central runtime-to-target mapping, creates missing parent directories, copies the bundled skill directory only for BC Design and Antigravity, writes stable instruction blocks, and skips any existing target unless `--force` appears. The VS Code target is valid JSON and preserves existing object keys.

- [ ] **Step 4: Run installer tests to verify success**

Run: `python -m unittest tests.test_bc_design -v`

Expected: every documented target exists after `--ai all`; pre-existing content is preserved by default.

### Task 5: Align documentation and perform end-to-end verification

**Files:**
- Modify: `AGENTS.md:1-15`
- Modify: `.agents/skills/bc-design/SKILL.md:1-104`
- Modify: `tests/test_bc_design.py`

**Interfaces:**
- Consumes: documented command examples and `python` launcher selection.
- Produces: commands that reference `.agents/skills/bc-design/scripts/...` from repository root and no unsupported files or claims.

- [ ] **Step 1: Write failing documentation assertions**

```python
def test_documentation_uses_existing_workspace_relative_commands(self):
    text = SKILL_FILE.read_text(encoding="utf-8")
    self.assertIn(".agents/skills/bc-design/scripts/bc_design.py", text)
    self.assertIn(".agents/skills/bc-design/scripts/install.py", text)
```

- [ ] **Step 2: Run test to verify failure**

Run: `python -m unittest tests.test_bc_design.BCDesignTests.test_documentation_uses_existing_workspace_relative_commands -v`

Expected: existing examples incorrectly use `scripts/...` from the workspace root.

- [ ] **Step 3: Update documentation minimally**

Document `python` / `python3` / `py -3` launcher choices, workspace-relative commands, the audit target contract, non-destructive installer behavior, and limitations of heuristic source auditing. Keep the nine-runtime table synchronized with the installer mapping.

- [ ] **Step 4: Run complete verification**

Run: `python -m unittest discover -s tests -v`

Expected: all tests pass. Also run:

```powershell
python .agents/skills/bc-design/scripts/bc_design.py "wealth management" --domain color
python .agents/skills/bc-design/scripts/bc_design.py --stack react
python .agents/skills/bc-design/scripts/bc_design.py --audit tests/fixtures/clean.css
python .agents/skills/bc-design/scripts/install.py --ai all --workspace $env:TEMP/bc-design-install-check
```

Expected: domain search and stack guide return content; audit exits 0 for the clean fixture; installer completes without overwriting existing files.

## Plan Self-Review

- Spec coverage: Tasks 1-5 cover all six audited defects plus regression coverage.
- Placeholder scan: no deferred implementation or unspecified validation remains.
- Interface consistency: all tasks use `SKILL_ROOT`, `audit_target`, `persist_master`, and the documented installer CLI consistently.
