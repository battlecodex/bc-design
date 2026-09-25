# Pruning Unused Design Code

Design code piles up: tokens nobody reads, classes left behind by a redesign, fonts still loading after the type changed, images no page shows, and packages installed for an experiment. Use the **prune** mode to find it and slim the project without breaking what users see.

## Rules

1. **Report first, change nothing.** `prune.py` only reads the project. It never edits or deletes a file.
2. **The user approves by number.** Show the numbered report and wait. Remove only the numbers the user approves; numbers they do not mention stay untouched.
3. **Prove nothing broke.** Run `render_check.py` on the affected pages before and after the removal and compare the screenshots. Run the project's own tests and build.
4. **Public API is not dead code.** A design system or component library ships tokens and classes for other projects to use. Pass those files with `--keep` so they are not reported.

## Run it

```bash
python .agents/skills/bc-design/scripts/prune.py
python .agents/skills/bc-design/scripts/prune.py --keep "src/styles/tokens.css" --json
```

The report is printed and saved to `.bc-design/prune-report.json`, so an approval such as "remove 1, 3, and 6" maps to exact findings.

## What it finds

| Kind | Confidence | What it means | Before removing |
| --- | --- | --- | --- |
| `unused-package` | high | A design package in `package.json` (motion, icons, fonts, UI kits) that nothing imports | Uninstall it and run the build |
| `unused-font` | high | A font family loaded through Google Fonts, `@font-face`, or `@fontsource` that no font-family, token, or script names | Remove the link, the `@font-face`, or the package |
| `unused-token` | high | A CSS custom property declared but never read by `var()` or a script | Remove every declaration, in all themes |
| `hardcoded-token-color` | high or low | A raw hex color that equals a token. High when the token's name matches the property's role (text, background, border); low when only a token for a different role has that value | Swap in the token; for low confidence, confirm the role first |
| `near-duplicate-color` | medium | Hard-coded colors within 4 of each other per channel, grouped into one cluster | Keep the most used value, make it a token, and replace the rest |
| `unused-class` | medium or low | A class selector that no markup or script mentions. Low when names with the same prefix are built at runtime (for example `` `btn-${variant}` ``) | Search for runtime construction by hand |
| `unused-asset` | medium | An image, icon, font, or media file that no file mentions. Favicons and social images are skipped | Confirm no CMS or computed path loads it |

## Limits

- The scan reads source text, so it cannot see class names or asset paths assembled at runtime, content in a CMS, or files loaded by a server. That is why classes and assets are never reported as high confidence.
- Tailwind utility classes are generated, not declared, so they are neither reported nor needed.
- A token read only from another repository looks unused here. Use `--keep` for shipped token files.

## After pruning

Record the result in the verification report: the approved numbers, what was removed, the before and after `render_check` screenshots, and the test and build results. If the project has a `DESIGN.md`, update its tokens section when a token was removed.
