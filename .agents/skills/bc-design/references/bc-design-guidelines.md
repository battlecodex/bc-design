# BC Design Distinctive Design & Distinctive Frontend Design Directives

> *"Approach this as the design lead at a design studio known for giving every client a distinct visual identity that is not mistaken for anyone else's. This client has already rejected proposals that felt cliché or templated, and is paying for a distinctive point of view."* — BC Design Frontend Design Mandate

---

## 1. Common Generic Patterns (What to Avoid)

AI-generated interfaces suffer from recognizable algorithmic tropes that immediately signal "lazy template." Avoid these 5 tells:

| # | Generic Pattern | The Pattern in the Wild | The BC Design Direction |
| :- | :--- | :--- | :--- |
| **1** | **Blind Terracotta / Cream Default** | Forcing warm cream (`#F4F1EA`) with terracotta (`#D97757`) onto *every* brief, even when designing a fintech ledger, cybersecurity tool, or medical app. | Ground the palette in the subject's actual world. Use Terracotta **only when it fits the brand brief**, not as an automated reflex. |
| **2** | **The Dark Mode Neon Cliche** | Near-black (`#0B0B0B`) background with a single blinding acid-green, electric purple, or vermilion accent. | Multi-layered warm espresso soot (`#181816`), obsidian carbon (`#141412`), and balanced editorial contrast. |
| **3** | **The Monotonous SaaS-Card Kit** | Chopping every piece of content into identical rounded cards (`rounded-xl p-6`), identical 1px border, the same soft grey shadow (`rgba(0,0,0,0.1)`), and decorative gradient washes. | Vary visual hierarchy! Use open breathing room, asymmetrical hero anchors, hairline rules, and varied container weights instead of cards for everything. |
| **4** | **Template Chrome & Filler** | • Tracked-out ALL-CAPS eyebrow labels above every heading (`EXPLORE PLATFORM`)<br>• Middle-dot meta strings (`A · B · C`)<br>• Spaced em dashes (`WORD — fragment`)<br>• Accenting a single word in a headline with italic/color<br>• Appending `→` to every button | Cut decorative filler. Use natural sentence case, clean typographic scaling, and purposeful CTAs without decorative arrows. |
| **5** | **Lazy Monospace Abuse** | Reaching for monospace typefaces for tiny metadata or random data chips purely for a "techy" vibe. | Reserve monospace strictly for code blocks, terminal output, git commits, or actual numeric tabular data. |

The CLI's distinctive review also checks for repeated generic CTAs, copied platform chrome, oversized hero type that displaces useful content, and decorative all-caps eyebrow overload. These are warnings with file evidence; contrast, focus, reduced-motion, and streaming geometry violations remain hard errors.

---

## 2. Grounding Design in the Subject Matter

Never build a generic template and re-skin the colors. Ground every aesthetic choice in the **materials, vernacular, and audience of the subject**:

* **A financial analytics terminal**: Needs high-density data tables, tabular monospace alignment, muted muted green/amber ledger indicators, strict vertical grids, and zero decorative fluff.
* **A clinical healthcare portal**: Needs soothing oatmeal grounds, eucalyptus sage accents, high WCAG contrast, calm spacious readability, and non-alarmist feedback.
* **A developer IDE**: Needs deep obsidian contrast, hairline pane separators, crisp monospace syntax tokens, and zero lag animations.
* **An artisan bookstore**: Needs fine linen textures, wide display serifs (`Playfair`), rich burnt sienna, and editorial whitespace.

---

## 3. Restraint & BC's Rule

> **BC's Rule**: *"Before shipping, remove one decorative decision that does not help the user."*

* **Spend boldness in ONE place**:
  * Let **one element** be the memorable hero: an interactive live demo, an organic hand-drawn illustration, an unforgettable typographic moment, or a signature parameter drawer.
  * Keep everything around it quiet, disciplined, and restrained.
  * Cut any decorative element that does not convey functional information.
* **Structural Devices Are Information, Not Decoration**:
  * Dividers, borders, numbering, and badges encode real information.
  * Never use numbered markers (`01 / 02 / 03`) unless the content is genuinely an ordered sequence or timeline.

---

## 4. Distinctive Design UI Copywriting

Words are design content, not decorative filler. Bring the same intentionality to copy as to layout:

1. **User-Perspective Naming**:
   * Name things by what users understand, not backend system architecture.
   * *Bad:* `"Webhook Event Dispatcher"` → *Good:* `"Manage notifications"`
   * *Bad:* `"Execute Transaction Entity"` → *Good:* `"Transfer funds"`
2. **Active Voice CTAs**:
   * A button says exactly what happens when clicked.
   * *Bad:* `"Submit"`, `"Click here"`, `"Proceed"`
   * *Good:* `"Save changes"`, `"Create project"`, `"Send message"`
3. **Consistency Through the Flow**:
   * The button says `"Publish"`, so the resulting confirmation toast says `"Published"`.
4. **Dignified Failure & Errors**:
   * Errors must never apologize cutely or use robotic vague slang.
   * *Bad:* `"Oops! Something went wonky on our end!"`
   * *Good:* `"Card expired. Update your payment method to continue."`
5. **Actionable Empty States**:
   * An empty screen is an invitation to act, not an apology for having no data. Provide an immediate primary action button to create or import the first item.

---

## 5. Streaming Token Safety (AI / LLM Specific)

> **CRITICAL**: Never animate the width, height, or margin of a container while AI text tokens stream into it.

* Animating dimensions during streaming causes continuous browser reflows (layout thrashing) and makes reading impossible.
* Keep container geometry stable; append text tokens quietly.
* Use `aria-live="polite"` so screen readers announce streamed tokens comfortably.
