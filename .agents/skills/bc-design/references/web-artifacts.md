# Single-File Web Artifacts

Use this reference when the deliverable is one shareable HTML file: a prototype, a demo, a pitch page, an interactive explainer, or a page someone opens straight from chat or email. The file must open by double-click, work offline except for pinned CDN assets, and meet the same luxury standard as a production page.

## When to choose a single file

| Deliverable | Format |
| --- | --- |
| A page to share, review, or present | One HTML file with inline CSS and JavaScript |
| A React prototype with several components | A bundled single file (see below) |
| Production code in an existing app | The project's own stack, not a single file |

## Rules for the file

1. **Everything inline except pinned libraries.** Put CSS in one `<style>` block and page logic in `<script>` at the end of `<body>`. Load libraries from a CDN with an exact version, for example `gsap@3.15.0` and `three@0.160.0`, never `@latest`.
2. **Fonts load with a fallback.** Link Newsreader and Inter from Google Fonts with `display=swap`, and give every stack a system fallback so the page stays composed offline.
3. **Tokens first.** Declare the BC tokens on `:root`, redefine them under `prefers-color-scheme: dark`, and give `body` an explicit background. Components read tokens, never raw hex values.
4. **Readable without JavaScript.** Content is in the HTML. Scripts enhance it: they never hold text that would otherwise be missing, and they never hide content that only they can reveal.
5. **Small and honest assets.** Inline only small SVGs and icons. Use real images by URL or a clearly marked placeholder; do not embed large base64 photos.
6. **One signature moment.** Even a demo has one: an orchestrated hero, a spatial stage, or a live interaction. See [visual-language.md](./visual-language.md).
7. **Phone width works.** Use a 16–24px side gutter, no horizontal scroll, and a stacked layout below 860px.

## Bundling a React prototype into one file

When a prototype needs React components, build it with Vite and inline the output:

```bash
npm create vite@latest artifact -- --template react-ts
cd artifact
npm install
npm install -D vite-plugin-singlefile
```

```ts
// vite.config.ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { viteSingleFile } from "vite-plugin-singlefile";

export default defineConfig({ plugins: [react(), viteSingleFile()] });
```

`npm run build` then writes one self-contained `dist/index.html`. Keep BC tokens in a global stylesheet imported once, and load GSAP through `gsap` and `@gsap/react` from npm.

## Verification

1. Run `bc_design.py --audit FILE` and fix every finding.
2. Run `render_check.py FILE` and review the mobile, desktop, and reduced-motion screenshots.
3. Open the file from disk with the network off and confirm the content and layout survive.

The worked example [`assets/motion/gsap-atelier.html`](../assets/motion/gsap-atelier.html) follows every rule above.
