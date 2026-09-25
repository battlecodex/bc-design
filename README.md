# ✦ BC Design System for AI Agents

> An open-source, universal design intelligence engine for clear, accessible, subject-grounded interfaces.
> Built from practical building blocks: **88 visual styles, 192 palettes, 74 typography pairings, 25 chart patterns, 119 UX checks, 22 searchable stack catalogs (8 focused guides), 31 spatial-effect references, design tokens, component contracts, and streaming-safe interaction guidance**.
> The catalog data derives from [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) and the spatial generators adapt [ThreeUI](https://github.com/MengTo/threeui), both MIT; see [Third-party notices](./THIRD_PARTY_NOTICES.md).

---

## 🚀 10-Assistant Multi-Runtime Support

Installable into any AI workflow with zero configuration:

| AI Assistant / Runtime | Integration Type | Workspace Target File | Install Flag |
| :--- | :---: | :--- | :--- |
| **BC Design Code** | ✅ Native / CLI | `BC.md` + `.bc/skills/bc-design/` | `--ai bc` |
| **Claude Code** | ✅ Native Skill | `.claude/skills/bc-design/` + `CLAUDE.md` | `--ai claude` |
| **Cursor IDE** | ✅ MDC Rule + Legacy | `.cursor/rules/bc-design.mdc` + `.cursorrules` | `--ai cursor` |
| **Windsurf** | ✅ Cascade Rules | `.windsurfrules` | `--ai windsurf` |
| **Google Antigravity** | ✅ Native Skill | `.agents/skills/bc-design/` + `GEMINI.md` | `--ai antigravity` |
| **GitHub Copilot** | ✅ Custom Instructions | `.github/copilot-instructions.md` | `--ai copilot` |
| **Kiro** | ✅ Native Skill + Steering | `.kiro/skills/bc-design/` + `.kiro/steering/bc-design.md` | `--ai kiro` |
| **Codex / Copilot CLI** | ✅ Agent Mandate | `AGENTS.md` + `.agents/skills/bc-design/` | `--ai codex` |
| **Qoder** | ✅ Rules Config | `.qoder/rules/bc-design.md` | `--ai qoder` |
| **VS Code** | ✅ Alias of Copilot | `.github/copilot-instructions.md` | `--ai vscode` |

### 1-Line Multi-Assistant Installer
Run the bundled zero-dependency Python installer:

```bash
# Install for a specific assistant
py -3 scripts/install.py --ai bc
py -3 scripts/install.py --ai claude
py -3 scripts/install.py --ai cursor
py -3 scripts/install.py --ai windsurf
py -3 scripts/install.py --ai antigravity
py -3 scripts/install.py --ai copilot
py -3 scripts/install.py --ai kiro
py -3 scripts/install.py --ai codex
py -3 scripts/install.py --ai qoder
py -3 scripts/install.py --ai vscode

# Or install for ALL 10 assistants at once
py -3 scripts/install.py --ai all
```

After installing, confirm the assistant actually loads the skill. Open the workspace in the tool, ask *"Design a pricing page for a bakery"*, and check that it names or reads `bc-design` before writing code.

If it does not, check that the family sits where that runtime looks for skills: `.claude/skills/` for Claude Code, `.kiro/skills/` for Kiro, and `.agents/skills/` for Codex and Antigravity.

The files in `adapters/` show what each runtime receives. They are generated from the installer, so edit `install.py` and regenerate them instead of editing them by hand:

```bash
py -3 scripts/sync_adapters.py
```

Validate repository integrity, skill mirror parity, adapter parity, and catalog consistency:

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
| `bc-motion` | Motion tiers, loading, overlays, reduced motion, and streamed feedback |

All siblings share the router's local catalogs and CLI. They do not create duplicate data sources.

| Feature Dimension | Generic starting point | BC Design System |
| :--- | :--- | :--- |
| **Aesthetic Craft** | Generic Tailwind / shadcn styling. Tends to generate stereotypical AI purple/blue gradients and cold enterprise gray. | **Subject-grounded editorial design**: neutral structure, purposeful typography, restrained subject-derived accents, hairline borders, and one earned signature moment. |
| **Visual Assets & Illustrations** | Text descriptions and ASCII tables only. No visual illustrations. | **Real Hand-Drawn SVG Crayon Artwork** (tactile thought bubbles with chalk squiggles) + **10 bundled HTML examples**, including spatial product stages and shader studies. |
| **AI / LLM Specific UX** | Standard web UX rules only. No LLM-specific safeguards. | **Streaming Token Isolation** (never animate container dimensions during generation to prevent layout thrashing), Thinking Pulse ambient glow, artifact drawers. |
| **Typography Intelligence** | Basic font suggestions without optical sizing. | **Optical Sizing (`opsz: 72`) Newsreader** paired with clean `Inter` and `JetBrains Mono`. Includes Google Fonts drop-in and Tailwind config. |
| **Button Hierarchy & Contrast** | Often uses saturated colored buttons everywhere. | **BC Design hierarchy**: Solid White (`#FFFFFF`) with dark text for primary modal CTAs in dark mode; Terracotta reserved for key actions. |
| **Multi-Framework Depth** | Summaries for React/Tailwind. | **22 searchable stack catalogs** plus **8 focused implementation guides** for common web and native stacks. |
| **Spatial 3D** | Decorative WebGL added as an interchangeable visual effect. | **Subject-grounded spatial stages**: a real product metaphor first, then a calm Three.js, WebGL, or Canvas implementation with canvas pass-through, reduced motion, DPR caps, and disposal guidance. |
| **CLI Dependencies** | Requires Node.js or a global package install. | **Pure Python Standard Library (Zero Dependencies)**. Runs out-of-the-box on `py -3`. |

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
|  MOTION DYNAMICS: Standard BC Design: 150ms buttons, 250ms cards, 1800ms thinking pulse, cubic-bezier(0.16, 1, 0.3, 1)|
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

BC Design keeps the broad catalog as reference knowledge while the shared alignment policy controls recommendations. The normalized catalog currently contains **1,775 classified rows**: **194 core**, **1,494 compatible**, **74 conditional**, and **13 excluded**. Automatic suggestions use only core or compatible entries; conditional directions require an explicit request or approved brand evidence, and excluded combinations remain blocked by accessibility and stability gates. See [catalog-alignment.md](./.agents/skills/bc-design/references/catalog-alignment.md).

| Domain | Depth | Guide Link | CLI Query |
| :--- | :--- | :--- | :--- |
| **Design Styles** | **88 cataloged styles** with use cases, risks, implementation notes, and accessibility checks | [references/styles.md](./.agents/skills/bc-design/references/styles.md) | `py -3 scripts/bc_design.py "canonical" --domain style` |
| **Color Palettes** | **192 product palettes** with semantic roles and contrast-oriented guidance | [references/palettes.md](./.agents/skills/bc-design/references/palettes.md) | `py -3 scripts/bc_design.py "saas" --domain color` |
| **Typography** | **74 font pairings** plus a local catalog of open-source font metadata | [references/typography.md](./.agents/skills/bc-design/references/typography.md) | `py -3 scripts/bc_design.py "canonical" --domain typography` |
| **Chart Types** | **25 visualization patterns** with selection and implementation guidance | [references/charts.md](./.agents/skills/bc-design/references/charts.md) | `py -3 scripts/bc_design.py "area" --domain chart` |
| **Landing Patterns** | **10 documented conversion layouts**: Hero+Prompt, Split Feature+Art, Academy Hub, Role Grid, Sandbox Tweaks, Enterprise Trust, Pricing, Editorial Story, Auth-First, Benchmark Matrix | [references/landing-patterns.md](./.agents/skills/bc-design/references/landing-patterns.md) | `py -3 scripts/bc_design.py "hero prompt" --domain landing` |
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

---

## 📄 License

[MIT License](./LICENSE) © 2026 for original BC Design code and documentation. The catalog data derived from UI UX Pro Max (MIT, © 2024 Next Level Builder), the spatial architecture adapted from ThreeUI (MIT, © 2026 Meng To), and the bundled Google Fonts and Phosphor reference metadata retain their upstream terms; see [Third-party notices](./THIRD_PARTY_NOTICES.md).
