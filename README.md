# ✦ BC Design System for AI Agents

> An open-source design skill for Claude Code, Codex, Antigravity, and Kiro. It gives the agent a warm editorial house style, GSAP motion orchestration, subject-grounded 3D, project memory through `DESIGN.md`, and audits across eighteen UI and UX dimensions.
> Built from practical building blocks: **88 visual styles, 192 palettes, 74 typography pairings, 25 chart patterns, 119 UX checks, 22 searchable stack catalogs (8 focused guides), 31 spatial-effect references, design tokens, component contracts, and streaming-safe interaction guidance**.
> The catalog data derives from [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill), the spatial generators adapt [ThreeUI](https://github.com/MengTo/threeui), and the craft rules adapt [anti-slop](https://github.com/miqdadbadjuber/anti-slop) and [taste-skill](https://github.com/Leonxlnx/taste-skill), all MIT; see [Third-party notices](./THIRD_PARTY_NOTICES.md).

---

## 🚀 Supported Assistants

BC Design installs as a native skill for four assistants:

| Assistant | Skill directory | Instruction file | Install flag |
| :--- | :--- | :--- | :--- |
| **Claude Code** | `.claude/skills/bc-design/` | `CLAUDE.md` | `--ai claude` |
| **Codex** | `.agents/skills/bc-design/` | `AGENTS.md` | `--ai codex` |
| **Google Antigravity** | `.agents/skills/bc-design/` | `GEMINI.md` | `--ai antigravity` |
| **Kiro** | `.kiro/skills/bc-design/` | `.kiro/steering/bc-design.md` | `--ai kiro` |

### Installer
Run the bundled zero-dependency Python installer. `--workspace` selects the project that receives the skill and defaults to the current directory:

```bash
# Install for one assistant
py -3 scripts/install.py --ai claude
py -3 scripts/install.py --ai codex
py -3 scripts/install.py --ai antigravity
py -3 scripts/install.py --ai kiro

# Or install for all four at once
py -3 scripts/install.py --ai all
```

On macOS or Linux, use `python3` in place of `py -3`, or run `scripts/install.sh`. On Windows PowerShell, `scripts/install.ps1` wraps the same installer.

The installer copies each skill into the runtime's folder and rewrites the documented script paths to match, so a Claude Code install tells the agent to run `.claude/skills/bc-design/scripts/project.py`. If the project already has its own `CLAUDE.md`, `AGENTS.md`, or `GEMINI.md`, the installer keeps every line and adds a BC Design section between `<!-- bc-design:start -->` and `<!-- bc-design:end -->` markers. Running it again leaves that section alone; `--force` replaces only the section and the installed skills.

To make BC Design available in every Claude Code project, install it once into your home folder:

```bash
py -3 scripts/install.py --ai claude --global
```

This writes `~/.claude/skills/` and adds the section to `~/.claude/CLAUDE.md`. If you cloned this repository straight into a skills folder instead, the root `SKILL.md` still registers `bc-design` and points the assistant at `.agents/skills/bc-design/SKILL.md`, but only the installer registers the five sibling skills and rewrites their paths.

After installing, confirm the assistant actually loads the skill. Open the workspace in the tool, ask *"Design a pricing page for a bakery"*, and check that it names or reads `bc-design` before writing code.

If it does not, check that the family sits where that runtime looks for skills: `.claude/skills/` for Claude Code, `.kiro/skills/` for Kiro, and `.agents/skills/` for Codex and Antigravity.

The files in `adapters/` show what each runtime receives. They are generated from the installer, so edit `install.py` and regenerate them instead of editing them by hand:

```bash
py -3 scripts/sync_adapters.py
```

Validate repository integrity, adapter parity, upstream notices, and catalog consistency:

```bash
py -3 scripts/validate.py
```

---

## What BC Design provides

### Modular skill family

Use `bc-design` as the router for mixed requests, or invoke the narrowest entrypoint when the intent is clear:

| Entry point | Scope |
| :--- | :--- |
| `bc-brand` | Brand evidence, palette rationale, typography roles, voice, and asset decisions |
| `bc-design-system` | Semantic tokens, component contracts, states, variants, themes, and governance |
| `bc-ui-styling` | Stack-aware implementation and restyling with behavior preserved |
| `bc-design-audit` | Read-only quality and distinctive-pattern review with evidence and confidence |
| `bc-motion` | Motion tiers, GSAP timeline and scroll orchestration, loading, overlays, reduced motion, and streamed feedback |

All siblings share the router's local catalogs and CLI. They do not create duplicate data sources.

### Modes and when it acts

The router classifies every request into one mode before choosing a visual direction:

| Mode | Use when | First artifact |
| :--- | :--- | :--- |
| **Greenfield** | Creating a new interface or product surface | Brief and a recorded design contract |
| **Redesign** | Improving an existing interface while preserving useful behavior | Baseline inventory and invariants |
| **Restyling** | Changing visual language without changing behavior or information architecture | Semantic token map and frozen invariants |
| **Design audit** | Reviewing usability, accessibility, responsive quality, or consistency | Evidence-backed findings |
| **Distinctive review** | Checking whether a design feels generic or disconnected from its subject | Per-pattern evidence and a prioritized verdict |
| **Study** | The user shares a URL or screenshot of a design they admire | A diagnosis mapped onto BC roles |
| **Prune** | The user wants to slim a project's design code | A numbered report; only approved numbers are removed |

A request to build, redesign, or restyle is approval to change the visuals. The agent picks the direction and the components, implements them, verifies the result, and explains its choices in the handoff, without stopping for sign-off on visual decisions. It asks first, in one short question at the end, only before it would:

- add a package to `package.json` or another manifest;
- change behavior or content, such as a flow, navigation, data, or existing copy;
- delete files, including prune findings;
- use a paid component or an asset whose license is unclear.

Questions, reviews, and audits change nothing. When you ask for a plan or options first, the agent gives them and waits.

| Feature Dimension | Generic starting point | BC Design System |
| :--- | :--- | :--- |
| **Aesthetic Craft** | Generic Tailwind / shadcn styling. Tends to generate stereotypical AI purple/blue gradients and cold enterprise gray. | **A warm editorial house style held to a luxury standard**: parchment and ink, one subject-chosen accent, generous space, Newsreader display type, hairline borders, and one signature moment per page. |
| **Visual Assets & Illustrations** | Text descriptions and ASCII tables only. No visual illustrations. | **Real Hand-Drawn SVG Crayon Artwork** (tactile thought bubbles with chalk squiggles) + **10 bundled HTML examples**, including spatial product stages and shader studies. |
| **AI / LLM Specific UX** | Standard web UX rules only. No LLM-specific safeguards. | **Streaming Token Isolation** (never animate container dimensions during generation to prevent layout thrashing), a calm thinking pulse that respects reduced motion, artifact drawers. |
| **Typography Intelligence** | Basic font suggestions without optical sizing. | **Optical Sizing (`opsz: 72`) Newsreader** paired with clean `Inter` and `JetBrains Mono`. Includes Google Fonts drop-in and Tailwind config. |
| **Button Hierarchy & Contrast** | Often uses saturated colored buttons everywhere. | **BC Design hierarchy**: solid ink primary actions (white in dark mode); accent-filled buttons use the strong terracotta `#B35637` so white text passes WCAG AA. |
| **Multi-Framework Depth** | Summaries for React/Tailwind. | **22 searchable stack catalogs** plus **8 focused implementation guides** for common web and native stacks. |
| **Motion Orchestration** | Scattered CSS keyframes, each element animating on its own. | **GSAP timelines on BC tokens**: one choreographed sequence per moment, ScrollTrigger narratives, `gsap.matchMedia` reduced-motion fallbacks, and cleanup through `gsap.context`. |
| **Spatial 3D** | Decorative WebGL added as an interchangeable visual effect. | **Subject-grounded spatial stages**: a real product metaphor first, then a calm Three.js, WebGL, or Canvas implementation with canvas pass-through, reduced motion, DPR caps, and disposal guidance. |
| **CLI Dependencies** | Requires Node.js or a global package install. | **Pure Python standard library**. The CLI, audit, pre-flight, prune, and components scripts run out of the box on `py -3`; only `render_check.py` and `study.py` need Playwright. |

---

## Design system generation

Analyze any free-form project description and output a complete, production-ready design system recommendation in seconds:

```bash
py -3 scripts/bc_design.py "Build a fintech wealth management dashboard" --design-system -p "Aura Wealth"
```

```
+----------------------------------------------------------------------------------------+
|  TARGET: Aura Wealth - BC DESIGN SYSTEM                                                |
+----------------------------------------------------------------------------------------+
|                                                                                        |
|  GROUNDED SUBJECT: Fintech & Wealth Intelligence                                       |
|  CATALOG MATCH: Financial Dashboard                                                    |
|  SIGNATURE MOMENT: Real-time interactive portfolio yield ticker with hairline sparkli...|
|  BC RESTRAINT PRINCIPLE: Spend boldness in this ONE place; keep everything else quiet.  |
|                                                                                        |
|  PATTERN: Conversion Pricing Matrix & Financial Ledger                                 |
|     CTA Placement: Above fold & anchor in header; active-voice naming ('Save changes') |
|     Layout Architecture: Varied visual density (NOT a monotonous grid of cards)        |
|                                                                                        |
|  STYLE: The Canonical BC Design                                                        |
|     Canvas:  #F8F7F2 (Fine Stone Parchment) / #161514 (Charcoal Slate)                 |
|     Surface: Subject-matched elevated neutral; preserve hierarchy and contrast         |
|                                                                                        |
|  COLOR PALETTE (SUBJECT GROUNDED):                                                     |
|     Primary:    #E09F3E (Warm Amber Gold)                                              |
|     Secondary:  #EAE7DF (Muted Stone)                                                  |
|     CTA Light:  #1F1E1B (Deep Formal Ink)                                              |
|     CTA Dark:   #FFFFFF (text #1F1E1B)                                                 |
|     Borders:    Delicate hairline 1px (rgba(31, 30, 27, 0.08) / 0.09 in dark mode)    |
|                                                                                        |
|  TYPOGRAPHY (EDITORIAL & DISTINCTIVE):                                                 |
|     Headline: Newsreader (Editorial Serif, opsz: 72)                                   |
|     Body/UI:  Inter (Neutral UI Sans)                                                  |
|     Code:     JetBrains Mono (Tabular Numbers)                                         |
|     Directives: Natural sentence case. No tracked-out ALL-CAPS eyebrows.               |
|                                                                                        |
|  SPACING SCALE:   Standard BC Design: 16px base, 24px card gap, 48px section padding   |
|  MOTION DYNAMICS: Standard BC Design: 150ms buttons, 250ms cards, 600ms once-only reveals, 1800ms thinking pulse, cubic-bezier(0.16, 1, 0.3, 1)|
|                                                                                        |
|  BC DESIGN QUALITY SAFEGUARDS:                                                         |
|     [ ] Automatic suggestions use core/compatible catalog entries only                 |
|     [ ] Conditional styles require explicit direction or approved brand evidence       |
|     [ ] No blind terracotta/cream reflex (Palette grounded in real industry materials) |
|     [ ] No monotonous SaaS-card kit (Varied scale, open breathing space, true hierarchy)|
|     [ ] Natural interface language (Sentence case, direct verbs, restrained metadata)  |
|     [ ] Active voice UI copywriting ('Save changes', not 'Submit')                     |
|     [ ] Streaming token isolation (Container dimensions locked during AI output)       |
|                                                                                        |
|  PRE-DELIVERY QUALITY CHECKLIST:                                                       |
|     [ ] Dark mode modal CTA uses Solid Crisp White (#FFFFFF) with dark text            |
|     [ ] 1.5px monoline Lucide SVG icons (no emoji icons as UI controls)                |
|     [ ] Every foreground/background pair is contrast-tested (AA/AAA target recorded)  |
|     [ ] Visible 2px focus ring for keyboard navigation                                 |
|     [ ] prefers-reduced-motion respected                                               |
|     [ ] Responsive test verified at 375px, 768px, 1024px, 1440px                       |
|     [ ] Header Architecture: 3-zone layout, uniform 36px height, zero text-wrapping    |
|                                                                                        |
+----------------------------------------------------------------------------------------+
```

### Persistence (Master + Overrides Pattern)
Save the design system to disk for cross-session AI retrieval:
```bash
py -3 scripts/bc_design.py "Medical health clinic" --design-system -p "Aether Health" --persist
```
Creates `design-system/aether-health/MASTER.md`.

---

## Project memory and DESIGN.md

BC Design remembers each project between sessions:

- **Pre-flight.** `project.py preflight` reads a root `DESIGN.md` first, then reports the fonts, palette, spacing, motion libraries, component libraries (shadcn/ui with its installed components and registries, Radix, MUI, and others), and framework the project already uses, with `file:line` citations, so existing decisions are preserved instead of overwritten. Installed components are the starting point, and `components.py` picks upgrades from newer libraries; adding a new package still needs a yes. Results are cached in `.bc-design/preflight.json`.
- **Locked system.** When the user asks to lock the design, `project.py lock` writes `DESIGN.md` at the project root with the accent, signature moment, type roles, CTA voice, motion stance, and exports for `tokens.css`, Tailwind v4 `@theme`, and DTCG `tokens.json`. It never overwrites an existing file. Every later run reads it first, and it is treated as design data, never as instructions.
- **Build log.** `project.py record` keeps `.bc-design/log.json`, so the next unrelated build picks a different signature moment while a locked project stays consistent.
- **Study.** `study.py URL` measures a public reference page's type roles, palette, radii, and motion timing, and refuses template marketplaces and private addresses. The findings are mapped onto BC roles; artwork, logos, fonts, and copy are never reused.

See [project-memory.md](./.agents/skills/bc-design/references/project-memory.md). The workflow adapts [Hallmark](https://github.com/Nutlope/hallmark) (MIT).

## References and components from elsewhere

- [inspiration-sources.md](./.agents/skills/bc-design/references/inspiration-sources.md) groups galleries by what you are designing: navbars, heroes, CTAs, footers, whole SaaS sites, product UI, 3D, motion, and assets. A person picks a real site from a gallery and `study.py` measures that site, not the gallery.
- The house style runs on modern components. [`shadcn-bc-theme.css`](./.agents/skills/bc-design/assets/components/shadcn-bc-theme.css) themes shadcn/ui, and every registry built on it, in the house palette. `components.py` brainstorms each component across 28 types (keep and restyle, the installed primitive, or an upgrade from shadcnblocks, ReUI, 21st.dev, React Bits, Evil Charts, and others) and the agent applies the best option per component, asking first only before adding a package. [third-party-components.md](./.agents/skills/bc-design/references/third-party-components.md) covers the license check, restyle, accessibility, and audit each adopted component needs.
- [Keyline Icons](https://github.com/keyline-icons/keyline-icons) (MIT, no attribution) is documented as an alternative icon set in [icons.md](./.agents/skills/bc-design/references/icons.md).

## Pruning unused design code

`prune.py` reports design code a project no longer uses, with a confidence level and `file:line` evidence for each finding: unused tokens, classes, fonts, assets, and design packages, raw colors that duplicate a token (matched by role: text, background, or border), and near-duplicate colors. It never edits files. The user approves findings by number, only those are removed, and `render_check.py` screenshots before and after prove nothing visible broke. Use `--keep` for files that are public API, such as a shipped token sheet. See [pruning.md](./.agents/skills/bc-design/references/pruning.md).

## Design dimensions

Every contract, review, and handoff covers eighteen dimensions: twelve for the interface (color, typography, layout and grid, spacing, visual hierarchy, imagery and icons, shape and effects, UI components, interaction and states, motion, responsiveness, accessibility) and six for the experience (user research, information architecture, user flow, wireframe and prototype, UX writing, usability testing). [design-dimensions.md](./.agents/skills/bc-design/references/design-dimensions.md) sets the house standard for each, names how it is verified, and provides the scorecard. `--audit --json` groups findings under `summary.by_dimension`.

## Motion orchestration with GSAP

BC Design orchestrates multi-element and scroll-driven motion with [GSAP](https://gsap.com) timelines on the house motion tokens (`expo.out` equals the `--bc-ease` curve). Every choreography runs inside `gsap.matchMedia()` with a reduced-motion branch, animates transforms and opacity only, and cleans up through `gsap.context()` or `useGSAP()`.

- [GSAP orchestration guide](./.agents/skills/bc-design/references/gsap-orchestration.md): token mapping, choreography budgets, ScrollTrigger narratives, 3D stage control, React.
- [`bc-motion.js`](./.agents/skills/bc-design/assets/motion/bc-motion.js): `BCMotion.orchestrate`, `heroSequence`, `revealOnce`, and `staggerList` helpers.
- [`editorial-patterns.html`](./.agents/skills/bc-design/assets/patterns/editorial-patterns.html): every house composition pattern on one reference page.
- [`gsap-atelier.html`](./.agents/skills/bc-design/assets/motion/gsap-atelier.html): a complete luxury page with an orchestrated hero and a pinned, scroll-scrubbed 3D exploded view of a watch movement.

The audit flags GSAP code without a reduced-motion branch (`gsap-reduced-motion`) and tweens of layout properties (`gsap-layout-property`).

## Rendered verification

The source audit cannot see the rendered page. `render_check.py` opens it in Chromium through Playwright, saves screenshots at 375, 768, and 1440px plus reduced-motion views, and reports horizontal overflow, console and page errors, failed requests, images without alt text, and controls without an accessible name:

```bash
pip install playwright && python -m playwright install chromium
py -3 .agents/skills/bc-design/scripts/render_check.py path/to/page.html --out render-check
```

## Spatial 3D & scrollytelling

Spatial work in BC Design is a product-specific storytelling tool, not decorative wallpaper. The spatial catalog contains **31 references** across industry stages, mathematical shader foundations, and tactile UI primitives. The CLI currently ships five generated templates: `school-spatial`, `erp-spatial`, `ribbon-field`, `predictive-arc`, and `spatial-scrollytelling`.

Every spatial direction starts with a concrete product metaphor: an academy receives an open codex rather than a galaxy; an ERP receives a modular supply-chain hub rather than a spinning globe. The implementation rules require a non-interactive canvas layer, readable foreground content, capped device pixel ratio on mobile, complete WebGL teardown, and a calm reduced-motion fallback.

```bash
# Inspect the spatial catalog and preset definitions
py -3 scripts/bc_design.py --spatial list

# Search 31 subject-grounded spatial references
py -3 scripts/bc_design.py "academy codex" --domain spatial

# Generate a standalone, light-theme school stage
py -3 scripts/bc_design.py --spatial school-spatial --spatial-theme light --output-dir examples/school-preview.html

# Generate a standalone WebGL ribbon field
py -3 scripts/bc_design.py --spatial ribbon-field --spatial-palette terracotta --output-dir examples/ribbon.html

# Generate the Predictive Arc as a React component
py -3 scripts/bc_design.py --spatial predictive-arc --spatial-format react --output-dir src/components/PredictiveArc.tsx
```

Read the [Spatial 3D reference](./.agents/skills/bc-design/references/spatial-3d.md) for the contextual matrix, implementation patterns, and accessibility/performance gate.

---

## 🎨 Design Intelligence Modules

### Catalog alignment

BC Design keeps the broad catalog as reference knowledge while the shared alignment policy controls recommendations. The normalized catalog currently contains **1,775 classified rows**: **194 core**, **1,494 compatible**, **74 conditional**, and **13 excluded**. Automatic suggestions use only core or compatible entries; conditional directions require an explicit request or approved brand evidence, and excluded combinations remain blocked by accessibility and stability gates. The catalog search returns catalog rows as they are, so a query such as `"saas" --domain color` can return upstream palettes with indigo or violet primaries. The house style comes from `--design-system` and the BC tokens, not from raw catalog rows. See [catalog-alignment.md](./.agents/skills/bc-design/references/catalog-alignment.md).

| Domain | Depth | Guide Link | CLI Query |
| :--- | :--- | :--- | :--- |
| **Design Styles** | **88 cataloged styles** with use cases, risks, implementation notes, and accessibility checks | [references/styles.md](./.agents/skills/bc-design/references/styles.md) | `py -3 scripts/bc_design.py "editorial" --domain style` |
| **Color Palettes** | **192 product palettes** with semantic roles and contrast-oriented guidance | [references/palettes.md](./.agents/skills/bc-design/references/palettes.md) | `py -3 scripts/bc_design.py "saas" --domain color` |
| **Typography** | **74 font pairings** plus a local catalog of open-source font metadata | [references/typography.md](./.agents/skills/bc-design/references/typography.md) | `py -3 scripts/bc_design.py "editorial serif" --domain typography` |
| **Chart Types** | **25 visualization patterns** with selection and implementation guidance | [references/charts.md](./.agents/skills/bc-design/references/charts.md) | `py -3 scripts/bc_design.py "trend" --domain chart` |
| **Landing Patterns** | **10 conversion layouts**, eight with full specifications: Hero+Prompt, Split Feature+Art, Academy Hub, Role Grid, Sandbox Tweaks, Enterprise Trust, Pricing, Editorial Story, Auth-First, Benchmark Matrix | [references/landing-patterns.md](./.agents/skills/bc-design/references/landing-patterns.md) | `py -3 scripts/bc_design.py "hero prompt" --domain landing` |
| **UX Guidelines** | **119 quality checks** covering accessibility, animation, streaming, forms, hierarchy, loading, and responsive behavior | [references/ux-guidelines.md](./.agents/skills/bc-design/references/ux-guidelines.md) | `py -3 scripts/bc_design.py "animation" --domain ux` |
| **Spatial Effects** | **31 subject-grounded 3D, shader, and tactile-UI references** with runtime, theme, use case, and forbidden-gimmick guidance | [references/spatial-3d.md](./.agents/skills/bc-design/references/spatial-3d.md) | `py -3 scripts/bc_design.py "academy codex" --domain spatial` |

---

## 💻 22 Stack Catalogs

Eight stacks have focused Markdown guides below; the remaining catalog-only stacks are still searchable through the same CLI. `tailwind` is a friendly alias for the canonical `html-tailwind` catalog.

| Framework / Stack | Focus Areas | Guide Link | CLI Command |
| :--- | :--- | :--- | :--- |
| ⚛️ **React** | State, hooks, compound components, streaming isolation, and complete spatial-scene disposal | [stacks/react.md](./.agents/skills/bc-design/stacks/react.md) | `py -3 scripts/bc_design.py --stack react` |
| 🚀 **Next.js** | App Router, Server Components, zero-CLS fonts, SSE streaming, and SSR-safe spatial client boundaries | [stacks/nextjs.md](./.agents/skills/bc-design/stacks/nextjs.md) | `py -3 scripts/bc_design.py --stack nextjs` |
| 💚 **Vue 3** | Composition API, Pinia theme store, page transitions, and WebGL lifecycle cleanup | [stacks/vue.md](./.agents/skills/bc-design/stacks/vue.md) | `py -3 scripts/bc_design.py --stack vue` |
| 🧡 **Svelte 5** | Svelte 5 Runes (`$state`), SvelteKit, cubic transitions, and spatial teardown | [stacks/svelte.md](./.agents/skills/bc-design/stacks/svelte.md) | `py -3 scripts/bc_design.py --stack svelte` |
| 🍏 **SwiftUI** | iOS 17+ / macOS, Color extensions, ViewModifiers | [stacks/swiftui.md](./.agents/skills/bc-design/stacks/swiftui.md) | `py -3 scripts/bc_design.py --stack swiftui` |
| 📱 **React Native** | Expo / Bare RN, KeyboardAvoidingView, navigation | [stacks/react-native.md](./.agents/skills/bc-design/stacks/react-native.md) | `py -3 scripts/bc_design.py --stack react-native` |
| 💙 **Flutter** | Material 3 ThemeData, GoogleFonts, custom widgets | [stacks/flutter.md](./.agents/skills/bc-design/stacks/flutter.md) | `py -3 scripts/bc_design.py --stack flutter` |
| 🎨 **Tailwind CSS** | Utilities, responsive drawer sheet, a11y focus rings | [stacks/tailwind.md](./.agents/skills/bc-design/stacks/tailwind.md) | `py -3 scripts/bc_design.py --stack tailwind` |

---

## 💻 Live Interactive Demos

Explore selected bundled standalone HTML examples:

* **[BC dashboard](./examples/bc-dashboard.html)**: Hero, split modal, tutorial cards, and role grid.
* **[BC chat](./examples/bc-chat.html)**: Prompt bar, thinking pulse, and sliding artifact drawer.
* **[Login surface](./examples/login-page.html)**: Reference authentication surface with light/dark toggle.
* **[Spatial showcase](./examples/bc-spatial-showcase.html)**: Layered scrollytelling stage with an editorial 3D depth system.
* **[School spatial](./examples/school-spatial.html)**: Interactive academic codex stage for an education product.
* **[ERP spatial](./examples/bc-erp-spatial.html)**: Modular supply-chain visualization for enterprise operations.
* **[Ribbon field](./examples/bc-ribbon-field.html)**: WebGL mathematical ribbon substrate.
* **[Predictive arc](./examples/bc-predictive-arc.html)**: Canvas attention-arc telemetry study.
* **[Landing page](./examples/bc-landing-page.html)**: Editorial product landing page in the house style.
* **[ERP workspace](./examples/bc-erp.html)**: Dense operational dashboard for enterprise work.
* **[GSAP atelier](./.agents/skills/bc-design/assets/motion/gsap-atelier.html)**: Luxury page with an orchestrated hero and a scroll-scrubbed 3D exploded watch movement.
* **[Editorial patterns](./.agents/skills/bc-design/assets/patterns/editorial-patterns.html)**: Every house composition pattern on one reference page.

---

## 📄 License

[MIT License](./LICENSE) © 2026 for original BC Design code and documentation. The catalog data derived from UI UX Pro Max (MIT, © 2024 Next Level Builder), the spatial architecture adapted from ThreeUI (MIT, © 2026 Meng To), the craft rules adapted from anti-slop (MIT, © 2026 Miqdad Badjuber) and taste-skill (MIT, © 2026 Leonxlnx), the project-memory workflow adapted from Hallmark (MIT, © 2026 Hallmark contributors), and the Google Fonts metadata and Phosphor icon references retain their upstream terms; see [Third-party notices](./THIRD_PARTY_NOTICES.md).
