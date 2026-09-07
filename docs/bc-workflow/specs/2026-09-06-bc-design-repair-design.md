# BC Design Skill Repair Design

## Goal

Make the BC Design skill's documented commands truthful, safe to use, and aligned with the repository's canonical design tokens.

## Scope

The repair covers the Python CLI, its documentation, an implementation of the promised installer, and automated regression tests. It does not alter the design database or add a new visual style.

## Architecture

The CLI resolves every bundled resource relative to its own skill root. Domain search and stack lookup consume those resolved paths. A new audit command accepts a target file or directory, examines text content for the enforceable generic-pattern and repository token rules, and exits non-zero if violations are found; it never reports an unconditional pass.

The installer is a small, deterministic Python command that writes only the explicit runtime instruction files listed in `SKILL.md`, preserving existing files unless `--force` is supplied. A common Python launcher section in the documentation uses `python`, `python3`, or `py -3` and always references the CLI by its workspace-relative path.

## Contracts

- `skill_root` is the directory containing `SKILL.md`; data resolves as `skill_root/data` and stack guides as `skill_root/stacks/<name>.md`.
- `--audit TARGET` emits named violations and returns status 1 when violations exist; a clean target returns status 0. `--delivery-gate` remains a backward-compatible alias requiring the same target.
- The generator uses `#FAF9F5` for light canvas and avoids `#FFFFFF` as a light surface. All dark-dialog CTA values are `#FFFFFF` with `#1F1E1B` text.
- `--page NAME` refuses to overwrite an existing page override unless `--force` is specified. Page names may not escape the `pages` directory.
- `scripts/install.py --ai <runtime|all> --workspace PATH [--force]` creates documented runtime instruction files and copies the skill directory only where the documented integration requires it.

## Testing

Tests use Python's standard-library `unittest` and execute the CLI in a temporary workspace. They prove correct resource resolution, stack output, meaningful audit pass/fail behavior, safe persistence, design-token output, and installer file creation/non-overwrite behavior. Documentation command paths are checked as part of the test suite.

## Constraints

- No third-party dependency.
- Preserve existing public flags where practical.
- The project is not a Git checkout, so no commit is expected.
- Documentation must not claim a behavior that lacks an executable implementation.
