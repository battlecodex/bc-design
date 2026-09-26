#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BC Design System CLI - design intelligence engine
Combines BC Design's bundled subject catalog with its official design and frontend
directives. The catalogs are local, inspectable, and used as a starting point—not
as a substitute for validating a real product brief.
Zero external dependencies (pure Python standard library).

Capabilities:
1. --design-system: Multi-domain reasoning generator (Product -> Pattern, Style, Palette, Fonts, Distinctive Design guidance, Checklist).
2. --brand-guidelines: Print BC Design Distinctive Design directives and the enforceable checklist.
3. --domain <domain>: Fast search across style, color, typography, chart, landing, product, ux, motion, icons, and google-fonts.
4. --persist: Saves design system to design-system/<project-slug>/MASTER.md.
5. Design Dials: --variance (1-10), --motion (1-10), --density (1-10).
6. Structured audits: --audit TARGET --json for CI-friendly findings.
7. Multi-Runtime: Installable as a native skill through the `claude`, `codex`, `antigravity`, and `kiro` runtimes.
"""

import sys
import os
import io
import re
import csv
import json
import argparse
from pathlib import Path

# Force UTF-8 on Windows command line
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except Exception:
        pass
if sys.stderr.encoding and sys.stderr.encoding.lower() != 'utf-8':
    try:
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    except Exception:
        pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = Path(SCRIPT_DIR).resolve().parent
REPO_ROOT = SKILL_ROOT.parent.parent.parent
DATA_DIR = SKILL_ROOT / "data"
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
from core import CSV_CONFIG, SimpleBM25, search_domain, search_stack, stack_catalog_names, resolve_stack_name
from alignment import requested_selection_mode
from contrast import compute_contrast, parse_hex_color, relative_luminance, linearize_channel

# ----------------- BC DESIGN GUIDELINES & REASONING -----------------

BC_DESIGN_GUIDELINES = [
    ("Guideline 1: Subject-grounded palette", "Choose color from the product's materials, audience, and context. Use parchment and terracotta only when they support the brief."),
    ("Guideline 2: Calm dark surfaces", "Prefer warm, legible dark surfaces. Avoid pitch black paired with a single high-saturation gradient."),
    ("Guideline 3: Varied hierarchy", "Do not place every piece of content in identical rounded cards. Mix open space, dividers, lists, and anchored panels."),
    ("Guideline 4: Natural interface language", "Use sentence case, meaningful labels, and direct verbs. Avoid decorative eyebrow text, middle-dot strings, and repeated arrow suffixes."),
    ("Guideline 5: Purposeful type", "Reserve monospace for code, terminals, and tabular numbers. Use editorial type for hierarchy and a clear UI sans for controls."),
    ("Guideline 6: One signature moment", "Spend visual emphasis in one memorable interaction or graphic. Keep supporting surfaces quiet and easy to scan."),
    ("Guideline 7: User-first copy", "Use active CTAs, dignified errors, and actionable empty states."),
    ("Guideline 8: Streaming stability", "Never animate container width, height, margin, or padding while AI text streams."),
    ("Guideline 9: Zero-wrap header", "Keep identity, command search, and utilities in three zones with 34px–36px controls and nowrap labels.")
]

def generate_design_system(query, project_name=None, variance=None, motion=None, density=None):
    """Generate a subject-grounded BC Design direction and implementation checklist."""
    q = query.lower()
    proj = project_name or (query.strip().title() if len(query) < 32 else "Distinctive System")
    product_context = search_domain("product", query, max_results=1)
    product_match = (product_context.get("results") or [None])[0] if "error" not in product_context else None
    catalog_product = product_match.get("Product Type", "") if product_match else ""
    catalog_style = product_match.get("Primary Style Recommendation", "") if product_match else ""
    catalog_pattern = product_match.get("Landing Page Pattern", "") if product_match else ""
    catalog_palette = product_match.get("Color Palette Focus", "") if product_match else ""

    # 1. Subject Matter Grounding
    # "machine-learning" is not an education signal, so drop it before matching whole words.
    product_words = set(re.findall(r"\w+", re.sub(r"machine[- ]learning", " ", f"{catalog_product} {product_match.get('Keywords', '')}".lower())))
    if catalog_product and product_words & {"education", "educational", "learning", "school", "student", "kindergarten", "preschool"}:
        industry = "Education & Learning"
        primary_color = "#1F1E1B (Neutral Ink)"
        secondary_color = "#D97757 (Restrained Terracotta Accent)"
        cta_light = "#1F1E1B (Neutral Ink)"
        cta_dark = "#FFFFFF (text #1F1E1B)"
        canvas = "#FAF9F5 (Warm Neutral Canvas) / #181816 (Evening Study Soot)"
        style_name = "Warm Editorial Learning"
        pattern_name = catalog_pattern or "Storytelling-Driven"
        heading_font = "Newsreader (Editorial Serif, opsz: 72)"
        body_font = "Inter (Neutral UI Sans)"
        code_font = "JetBrains Mono (Tabular Values)"
        bold_moment = "Guided learning path with one tactile progress interaction"
    elif any(k in q for k in ["fintech", "wealth", "crypto", "trading", "bank", "invest", "money", "accounting", "ledger"]):
        industry = "Fintech & Wealth Intelligence"
        primary_color = "#E09F3E (Warm Amber Gold)"
        secondary_color = "#EAE7DF (Muted Stone)"
        cta_light = "#1F1E1B (Deep Formal Ink)"
        cta_dark = "#FFFFFF (text #1F1E1B)"
        canvas = "#F8F7F2 (Fine Stone Parchment) / #161514 (Charcoal Slate)"
        style_name = "Amber Nocturne (Financial Telemetry)" if (variance and variance > 6) else "The Canonical BC Design"
        pattern_name = "Conversion Pricing Matrix & Financial Ledger"
        heading_font = "Newsreader (Editorial Serif, opsz: 72)"
        body_font = "Inter (Neutral UI Sans)"
        code_font = "JetBrains Mono (Tabular Numbers)"
        bold_moment = "Real-time interactive portfolio yield ticker with hairline sparklines"
    elif any(k in q for k in ["health", "med", "doctor", "clinic", "bio", "pharma", "spa", "wellness", "care", "patient"]):
        industry = "Healthcare & Life Sciences"
        primary_color = "#7D8A68 (Eucalyptus Sage)"
        secondary_color = "#EAF1EE (Pastel Sage Tint)"
        cta_light = "#7D8A68 (Sage)"
        cta_dark = "#FFFFFF (text #1F1E1B)"
        canvas = "#F4F3EE (Calming Oatmeal) / #181A18 (Deep Forest Soot)"
        style_name = "Tactile Neo-Humanist (Calming Organic)" if (variance and variance > 5) else "Warm Editorial Organic"
        pattern_name = "Split Feature Hero + Empathetic Trust Verification"
        heading_font = "Fraunces (Soft Humanist Serif)" if (variance and variance > 5) else "Lora (Friendly Serif)"
        body_font = "DM Sans or Plus Jakarta Sans"
        code_font = "Space Mono"
        bold_moment = "Interactive patient health score dial with calming sage fill"
    elif any(k in q for k in ["dev", "code", "terminal", "ide", "api", "git", "cloud", "infra", "deploy", "server"]):
        industry = "Developer Tools & Code IDEs"
        primary_color = "#E28466 (Terracotta Glow)"
        secondary_color = "rgba(255, 255, 255, 0.08) (Subtle Inset Well)"
        cta_light = "#D97757 (Terracotta)"
        cta_dark = "#FFFFFF (text #1F1E1B)"
        canvas = "#141412 (Obsidian Carbon) / #1D1D1A (Active Editor Surface)"
        style_name = "Espresso Soot (Deep Technical Dark Mode)"
        pattern_name = "Interactive Sandbox & Parameter Tweaks Popover"
        heading_font = "Instrument Serif (Contemporary Sleek Serif)"
        body_font = "Geist (Clean Monospaced Sans)"
        code_font = "Geist Mono / JetBrains Mono"
        bold_moment = "Live prompt sandbox with instant token streaming & tweaks drawer"
    elif any(k in q for k in ["shop", "ecommerce", "store", "fashion", "book", "artisan", "buy", "cart"]):
        industry = "E-Commerce & Artisan Publishing"
        primary_color = "#AA4F32 (Deep Burnt Sienna)"
        secondary_color = "#E8CFC5 (Blush Clay)"
        cta_light = "#AA4F32 (Burnt Sienna)"
        cta_dark = "#FFFFFF (text #1F1E1B)"
        canvas = "#FAF8F3 (Woven Fine Linen) / #1A1918 (Deep Studio Soot)"
        style_name = "Studio Craft & Publishing"
        pattern_name = "Hero Visual Showcase + Curated Artisan Grid"
        heading_font = "Playfair Display (Luxury High-Craft Display)"
        body_font = "Outfit (Clean Circular Sans)"
        code_font = "Roboto Mono"
        bold_moment = "Full-bleed editorial product photograph with delicate framing rule"
    elif any(k in q for k in ["research", "paper", "academic", "journal", "university", "science", "citation"]):
        industry = "Academic Research & Higher Education"
        primary_color = "#34526F (Scholarly Oxford Navy)"
        secondary_color = "#F1EEE7 (Quoted Excerpt Paper Well)"
        cta_light = "#34526F (Navy) / #D97757 (DOI Link)"
        cta_dark = "#FFFFFF (text #1F1E1B)"
        canvas = "#FAF9F5 (Archival Cotton Parchment) / #181816 (Antique Library)"
        style_name = "Scholarly Academic & Research"
        pattern_name = "Role / Persona Explorer Grid & Citation Directory"
        heading_font = "Newsreader (Serif with optical sizing opsz: 72)"
        body_font = "Inter (UI Sans)"
        code_font = "JetBrains Mono (Exact Syntax)"
        bold_moment = "Interactive citation tree visualization with hairline links"
    else:
        # Default AI & SaaS Productivity
        industry = "AI & SaaS Productivity (Canonical BC Design)"
        primary_color = "#D97757 (Signature Terracotta)"
        secondary_color = "#ECEAE2 (Warm Parchment Pill)"
        cta_light = "#D97757 (Terracotta)"
        cta_dark = "#FFFFFF (text #1F1E1B)"
        canvas = "#FAF9F5 (Warm Book Parchment) / #181816 (Espresso Soot)"
        style_name = "BC Editorial Utility" if (variance and variance > 7) else "BC Editorial Neutral"
        pattern_name = "Hero + Centered Floating Prompt Box (720px wide)"
        heading_font = "Newsreader (Editorial Serif, opsz: 72)"
        body_font = "Inter (Neutral UI Sans)"
        code_font = "JetBrains Mono (Code & Artifacts)"
        bold_moment = "Elevated floating prompt container with model selector tag and terracotta send button"

    # Spacing Density Scale
    if density and density >= 8:
        spacing = "High Density (Dashboard): 8px base, 12px gap, 24px container padding"
    elif density and density <= 3:
        spacing = "Spacious Editorial: 24px base, 48px gap, 80px section padding"
    else:
        spacing = "Standard BC Design: 16px base, 24px card gap, 48px section padding"

    # Motion Intensity
    if motion and motion >= 8:
        motion_desc = "Choreographed: Staggered drawer entries, 400ms slide-in, cubic-bezier(0.16, 1, 0.3, 1)"
    elif motion and motion <= 3:
        motion_desc = "Subtle: 150ms micro-interactions only, zero non-functional motion, reduced-motion strictly honored"
    else:
        motion_desc = "Standard BC Design: 150ms buttons, 250ms cards, 600ms once-only reveals, 1800ms thinking pulse, cubic-bezier(0.16, 1, 0.3, 1)"

    typography_lines = [
        f"|     Headline: {heading_font}".ljust(89) + "|",
    ]
    lines = [
        "+----------------------------------------------------------------------------------------+",
        f"|  TARGET: {proj} - BC DESIGN SYSTEM".ljust(89) + "|",
        "+----------------------------------------------------------------------------------------+",
        "|                                                                                        |",
        f"|  GROUNDED SUBJECT: {industry}".ljust(89) + "|",
        f"|  CATALOG MATCH: {catalog_product or 'No verified product match; using explicit fallback'}".ljust(89) + "|",
        f"|  SIGNATURE MOMENT: {bold_moment[:66]}...".ljust(89) + "|",
        "|  BC RESTRAINT PRINCIPLE: Spend boldness in this ONE place; keep everything else quiet.  |",
        "|                                                                                        |",
        f"|  PATTERN: {pattern_name}".ljust(89) + "|",
        "|     CTA Placement: Above fold & anchor in header; active-voice naming ('Save changes') |",
        "|     Layout Architecture: Varied visual density (NOT a monotonous grid of cards)        |",
        "|                                                                                        |",
        f"|  STYLE: {style_name}".ljust(89) + "|",
        f"|     Canvas:  {canvas}".ljust(89) + "|",
        f"|     Surface: Subject-matched elevated neutral; preserve hierarchy and contrast".ljust(89) + "|",
        "|                                                                                        |",
        "|  COLOR PALETTE (SUBJECT GROUNDED):                                                     |",
        f"|     Primary:    {primary_color}".ljust(89) + "|",
        f"|     Secondary:  {secondary_color}".ljust(89) + "|",
        f"|     CTA Light:  {cta_light}".ljust(89) + "|",
        f"|     CTA Dark:   {cta_dark}".ljust(89) + "|",
        "|     Borders:    Delicate hairline 1px (rgba(31, 30, 27, 0.08) / 0.09 in dark mode)    |",
        "|                                                                                        |",
        "|  TYPOGRAPHY (EDITORIAL & DISTINCTIVE):                                                 |",
        *typography_lines,
        f"|     Body/UI:  {body_font}".ljust(89) + "|",
        f"|     Code:     {code_font}".ljust(89) + "|",
        "|     Directives: Natural sentence case. No tracked-out ALL-CAPS eyebrows.               |",
        "|                                                                                        |",
        f"|  SPACING SCALE:   {spacing}".ljust(89) + "|",
        f"|  MOTION DYNAMICS: {motion_desc}".ljust(89) + "|",
        "|                                                                                        |",
        "|  BC DESIGN QUALITY SAFEGUARDS:                                                       |",
        "|     [ ] Automatic suggestions use core/compatible catalog entries only               |",
        "|     [ ] Conditional styles require explicit direction or approved brand evidence     |",
        "|     [ ] No blind terracotta/cream reflex (Palette grounded in real industry materials) |",
        "|     [ ] No monotonous SaaS-card kit (Varied scale, open breathing space, true hierarchy)|",
        "|     [ ] Natural interface language (Sentence case, direct verbs, restrained metadata)  |",
        "|     [ ] Active voice UI copywriting ('Save changes', not 'Submit')                     |",
        "|     [ ] Streaming token isolation (Container dimensions locked during AI output)       |",
        "|                                                                                        |",
        "|  PRE-DELIVERY QUALITY CHECKLIST:                                                       |",
        "|     [ ] Dark mode modal CTA uses Solid Crisp White (#FFFFFF) with dark text            |",
        "|     [ ] 1.5px monoline Lucide SVG icons (no emoji icons as UI controls)                |",
        "|     [ ] Every foreground/background pair is contrast-tested (AA/AAA target recorded)  |",
        "|     [ ] Visible 2px focus ring for keyboard navigation                                 |",
        "|     [ ] prefers-reduced-motion respected                                               |",
        "|     [ ] Responsive test verified at 375px, 768px, 1024px, 1440px                       |",
        "|     [ ] Header Architecture: 3-zone layout, uniform 36px height, zero text-wrapping    |",
        "|                                                                                        |",
        "+----------------------------------------------------------------------------------------+"
    ]

    data = {
        "project": proj,
        "industry": industry,
        "style": style_name,
        "canvas": canvas,
        "primary_color": primary_color,
        "cta_dark": cta_dark,
        "typography": f"{heading_font} + {body_font} + {code_font}",
        "pattern": pattern_name,
        "bold_moment": bold_moment,
        "catalog_product": catalog_product,
        "catalog_style": catalog_style,
        "catalog_pattern": catalog_pattern,
        "catalog_palette": catalog_palette,
    }

    return "\n".join(lines), data

def persist_master(data, output_dir=".", page=None, force=False):
    """Save to design-system/<project-slug>/MASTER.md"""
    slug = re.sub(r'[^a-zA-Z0-9_-]', '-', data["project"].lower()).strip('-')
    base_dir = os.path.join(output_dir, "design-system", slug)
    os.makedirs(base_dir, exist_ok=True)
    master_file = os.path.join(base_dir, "MASTER.md")

    if os.path.exists(master_file) and not force and not page:
        print(f"[-] {master_file} already exists. Skipping write (use --force to overwrite).")
        return

    content = f"""# Distinctive Design System: {data['project']}
Grounded in BC Design's Distinctive Design Directives & BC Design Language.

## 1. Subject & Identity
- **Subject / Industry**: {data['industry']}
- **Signature Bold Moment**: {data['bold_moment']}
- **BC restraint principle**: Spend boldness in this ONE place. Keep surrounding elements restrained.

## 2. Palette & Contrast
- **Canvas**: {data['canvas']}
- **Primary Accent**: `{data['primary_color']}`
- **Dark Mode Primary CTA**: `{data['cta_dark']}`
- **Border**: 1px delicate hairline `rgba(31, 30, 27, 0.08)` (light) / `rgba(250, 249, 245, 0.09)` (dark).

## 3. Typography & Hierarchy
- **Stack**: {data['typography']}
- **Directives**: Sentence case headings. No tracked-out ALL-CAPS eyebrows. Avoid single-word color spans.

## 4. Distinctive Design Safeguards
- No repetitive SaaS cards with identical padding and shadows.
- Active voice CTAs: "Save changes", "Create project" (never generic "Submit").
- Never animate container width/height while AI text streams.
- 1.5px monoline Lucide icons (no emojis as UI controls).
"""
    if page:
        if not re.fullmatch(r"[A-Za-z0-9_-]+", page):
            raise ValueError("Page name may contain only letters, numbers, hyphens, and underscores")
        pages_dir = os.path.join(base_dir, "pages")
        os.makedirs(pages_dir, exist_ok=True)
        page_file = os.path.join(pages_dir, f"{page}.md")
        if os.path.exists(page_file) and not force:
            print(f"[-] {page_file} already exists. Skipping write (use --force to overwrite).")
            return
        with open(page_file, "w", encoding="utf-8") as f:
            f.write(f"# Page Override: {page.title()}\nInherits from MASTER.md with page-specific layouts.\n")
        print(f"  + Created page override: {page_file}")
    else:
        with open(master_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  + Persisted Design System Master to: {master_file}")

AUDIT_EXTENSIONS = {".css", ".html", ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte"}

MOTION_DECLARATION_RE = re.compile(
    r"(?P<property>(?<![-\w])(?:transition|animation)(?:-[a-z-]+)?\s*):(?!\s*\{)\s*"
    r"(?P<value>[^;{}]*[^;{}\s][^;{}]*)",
    re.IGNORECASE,
)
MOTION_TIME_RE = re.compile(r"(?<![\w.-])(?P<amount>(?:\d+\.?\d*|\.\d+))(?P<unit>ms|s)\b", re.IGNORECASE)
MOTION_EASING_TOKEN_RE = re.compile(
    r"var\(\s*--[^)]*ease[^)]*\)|cubic-bezier\s*\(",
    re.IGNORECASE,
)
# The four control points; Tailwind arbitrary values separate them with commas or underscores.
CUBIC_BEZIER_RE = re.compile(
    r"cubic-bezier\(\s*(-?\d*\.?\d+)[\s,_]+(-?\d*\.?\d+)[\s,_]+(-?\d*\.?\d+)[\s,_]+(-?\d*\.?\d+)\s*\)",
    re.IGNORECASE,
)


def _overshoots(value):
    """A cubic-bezier whose y1 or y2 leaves [0, 1] overshoots or bounces past its end state."""
    for match in CUBIC_BEZIER_RE.finditer(value):
        y1, y2 = float(match.group(2)), float(match.group(4))
        if not (0 <= y1 <= 1 and 0 <= y2 <= 1):
            return True
    return False


def _easing_value_ok(value):
    """An approved easing: a BC ease token or a calm cubic-bezier, never an overshooting curve."""
    return bool(MOTION_EASING_TOKEN_RE.search(value)) and not _overshoots(value)


# A reduced-motion branch: a CSS media query, a matchMedia query in script, or a Tailwind motion-reduce variant.
REDUCED_MOTION_BRANCH_RE = re.compile(
    r"prefers-reduced-motion\s*:\s*reduce|motion-reduce:|useReducedMotion|prefersReducedMotion",
    re.IGNORECASE,
)


def _motion_declarations(content):
    """Return CSS transition/animation declarations with normalized properties."""
    return [
        (match.group("property").strip().lower(), match.group("value").strip())
        for match in MOTION_DECLARATION_RE.finditer(content)
    ]


def _blank(text):
    """Replace text with spaces of the same length, keeping line breaks, so offsets and line numbers still line up."""
    return re.sub(r"[^\n]", " ", text)


def _strip_motion_comments(content):
    """Ignore block comments so examples and disabled declarations are not audited."""
    return re.sub(r"/\*[\s\S]*?\*/", lambda match: _blank(match.group(0)), content)


def _duration_ms(amount, unit):
    value = float(amount)
    return value if unit.lower() == "ms" else value * 1000


def _has_active_motion(declarations, content):
    """Return whether a source contains motion that needs reduced-motion handling."""
    for property_name, value in declarations:
        if property_name in {"transition", "animation"} and value.lower() in {"none", "initial", "inherit", "unset"}:
            continue
        if property_name.endswith("-name") and value.lower() == "none":
            continue
        return True
    return bool(re.search(r"@(?:-webkit-)?keyframes\b", content, re.IGNORECASE))


def _motion_violations(content, source_file):
    """Reduced-motion findings for CSS transitions and animations; durations and easing come from _motion_hits."""
    audit_content = _strip_motion_comments(content)
    declarations = _motion_declarations(audit_content)
    if _has_active_motion(declarations, audit_content) and not REDUCED_MOTION_BRANCH_RE.search(audit_content):
        return [(
            "reduced-motion-support",
            "Provide a prefers-reduced-motion: reduce override whenever the source defines transitions or animations.",
            source_file,
        )]
    return []


def iter_source_files(target):
    """Yield supported source files from a file or directory target."""
    target = Path(target)
    if target.is_file():
        if target.suffix.lower() in AUDIT_EXTENSIONS:
            yield target
        return
    if target.is_dir():
        for source_file in sorted(target.rglob("*")):
            if source_file.is_file() and source_file.suffix.lower() in AUDIT_EXTENSIONS:
                yield source_file


MARKUP_EXTENSIONS = {".html", ".jsx", ".tsx", ".vue", ".svelte"}
HIDDEN_MARKUP_RE = re.compile(r"<script\b.*?</script>|<style\b.*?</style>|<!--.*?-->", re.IGNORECASE | re.DOTALL)
BUZZWORD_RE = re.compile(
    r"\b(?:ai[- ]powered|next[- ]generation|revolutionary|revolutioni[sz]e[sd]?|seamless(?:ly)?|"
    r"cutting[- ]edge|unlock|elevate|empower|unleash|supercharge|game[- ]changer|effortless(?:ly)?)\b",
    re.IGNORECASE,
)
UNVERIFIED_CLAIM_RE = re.compile(
    r"\b(?:soc ?2|iso ?27001|(?:hipaa|gdpr)[- ](?:compliant|ready|certified)|pci[- ]dss)\b|"
    r"\b\d+(?:\.\d+)?% uptime\b|\b\d+x faster\b",
    re.IGNORECASE,
)
GSAP_CALL_RE = re.compile(r"\bgsap\.(?:to|from|fromTo|timeline|set)\s*\(")
GSAP_LAYOUT_TWEEN_RE = re.compile(
    r"\bgsap\.(?:to|from|fromTo)\s*\([^;]*?\{[^{}]*?\b(?:width|height|top|left|right|bottom|margin\w*|padding\w*)\s*:",
    re.DOTALL,
)


SCRIPT_MARKUP_EXTENSIONS = {".jsx", ".tsx", ".vue", ".svelte"}
# Strings come first so a comment marker inside a string (a URL, for example) is kept as text.
CODE_TOKEN_RE = re.compile(
    r"(?P<string>\"(?:\\.|[^\"\\\n])*\"|'(?:\\.|[^'\\\n])*'|`(?:\\.|[^`\\])*`)"
    r"|(?P<jsx_comment>\{\s*/\*[\s\S]*?\*/\s*\})"
    r"|(?P<block_comment>/\*[\s\S]*?\*/)"
    r"|(?P<line_comment>(?<![:\w\\])//[^\n]*)"
    r"|(?P<html_comment><!--[\s\S]*?-->)"
)
# Attribute values that hold code, not copy.
NON_COPY_ATTRIBUTE_RE = re.compile(
    r"\b(?:class(?:Name)?|href|src|id|key|type|name|role|rel|target|style|variant|size|as|ref|import|from|require)\s*[=(]?\s*$"
)


def strip_code_comments(content):
    """Blank //, /* */, {/* */}, and <!-- --> comments, keeping string literals, offsets, and line numbers intact."""
    return CODE_TOKEN_RE.sub(lambda match: match.group("string") or _blank(match.group(0)), content)


ARIA_HIDDEN_RE = re.compile(r"aria-hidden\s*=\s*(?:[\"']true[\"']|\{\s*true\s*\})", re.IGNORECASE)


def _copy_markup(content):
    """The markup with scripts, styles, and comments blanked out; same length as ``content``."""
    return strip_code_comments(HIDDEN_MARKUP_RE.sub(lambda match: _blank(match.group(0)), content))


def _top_level_spans(markup, start, end):
    """Parts of a JSX text run outside {expressions}."""
    spans, depth, run_start = [], 0, start
    for index in range(start, end):
        char = markup[index]
        if char == "{":
            if depth == 0 and index > run_start:
                spans.append((run_start, index))
            depth += 1
        elif char == "}" and depth:
            depth -= 1
            if depth == 0:
                run_start = index + 1
    if depth == 0 and end > run_start:
        spans.append((run_start, end))
    return spans


def _copy_spans(content, source_file):
    """(markup, spans): where interface copy sits, as offsets into ``content``.

    Copy is element text and, in script markup, human-readable string labels. Comments, scripts,
    styles, {expressions}, class lists, keys, ids, and text inside aria-hidden elements are not copy.
    """
    suffix = Path(source_file).suffix.lower()
    if suffix not in MARKUP_EXTENSIONS:
        return "", []
    markup = _copy_markup(content)
    spans = []
    for match in re.finditer(r">([^<>]+)<", markup):
        tag = markup[markup.rfind("<", 0, match.start()):match.start() + 1]
        # Decorative (aria-hidden) text and keyboard keys such as <kbd>⌘↵</kbd> are not prose.
        if ARIA_HIDDEN_RE.search(tag) or re.match(r"<kbd\b", tag, re.IGNORECASE):
            continue
        if suffix in SCRIPT_MARKUP_EXTENSIONS:
            spans.extend(_top_level_spans(markup, match.start(1), match.end(1)))
        else:
            spans.append((match.start(1), match.end(1)))
    if suffix in SCRIPT_MARKUP_EXTENSIONS:
        for match in CODE_TOKEN_RE.finditer(markup):
            literal = match.group("string")
            if not literal:
                continue
            text = literal[1:-1]
            if not re.search(r"[A-Za-z]{2,}", text) or not re.search(r"\s", text.strip()):
                continue
            if NON_COPY_ATTRIBUTE_RE.search(markup[max(0, match.start() - 40):match.start()]):
                continue
            spans.append((match.start() + 1, match.end() - 1))
    merged = []
    for start, end in sorted(spans):
        if merged and start < merged[-1][1]:
            merged[-1] = (merged[-1][0], max(end, merged[-1][1]))
        else:
            merged.append((start, end))
    return markup, [(start, end) for start, end in merged if markup[start:end].strip()]


def visible_text(content, source_file):
    """Return the human-readable copy of a markup file (element text and, in script markup, string labels)."""
    markup, spans = _copy_spans(content, source_file)
    return "\n".join(markup[start:end] for start, end in spans)


def _copy_hits(content, source_file, pattern):
    """(offset, matched text) for each match of ``pattern`` inside interface copy."""
    markup, spans = _copy_spans(content, source_file)
    return [
        (start + match.start(), match.group(0))
        for start, end in spans
        for match in pattern.finditer(markup[start:end])
    ]


# Symbols standing in for icons: bullets, arrows, checks, stars, sparkles, dingbats, geometric shapes, and emoji.
UNICODE_GLYPH_RE = re.compile(
    "[\u2022\u2023\u2043\u2190-\u21ff\u25a0-\u25ff\u2600-\u26ff\u2700-\u27bf\u27f0-\u27ff"
    "\u2b50\u2b55\U0001f300-\U0001faff]"
)
EM_DASH_COPY_RE = re.compile(r"\w[ \t]*\u2014[ \t]*\w")
CLASS_ATTRIBUTE_RE = re.compile(r"\bclass(?:Name)?\s*=\s*\{?\s*[\"'`]([^\"'`]*)[\"'`]")
CSS_BLOCK_RE = re.compile(r"\{([^{}]*)\}")


def iter_css_rule_spans(content):
    """Yield (selector, body, body offset) for each innermost {...} block."""
    for match in CSS_BLOCK_RE.finditer(content):
        start = max(content.rfind("{", 0, match.start()), content.rfind("}", 0, match.start())) + 1
        yield content[start:match.start()], match.group(1), match.start(1)


def iter_css_rules(content):
    """Yield (selector, body) for each innermost {...} block; the selector is the text since the previous brace."""
    for selector, body, _ in iter_css_rule_spans(content):
        yield selector, body


def _letter_spacing_is_wide(value):
    match = re.match(r"\s*(-?\d*\.?\d+)(em|rem|px)", value)
    if not match:
        return value.strip().lower() in {"wide", "wider", "widest"}
    amount, unit = float(match.group(1)), match.group(2)
    return amount >= (1 if unit == "px" else 0.05)


def _tracked_uppercase_hits(content):
    hits = []
    for match in CLASS_ATTRIBUTE_RE.finditer(content):
        classes = match.group(1)
        if not re.search(r"(?<![\w-])uppercase(?![\w-])", classes):
            continue
        if any(
            _letter_spacing_is_wide(tracking.strip("[]"))
            for tracking in re.findall(r"(?<![\w-])tracking-(wide|wider|widest|\[[^\]]+\])", classes)
        ):
            hits.append((match.start(), None))
    for _, body, offset in iter_css_rule_spans(content):
        transform = re.search(r"text-transform\s*:\s*uppercase", body, re.IGNORECASE)
        if transform:
            spacing = re.search(r"letter-spacing\s*:\s*([^;]+)", body, re.IGNORECASE)
            if spacing and _letter_spacing_is_wide(spacing.group(1)):
                hits.append((offset + transform.start(), None))
    return hits


GLOBAL_FOCUS_VISIBLE_RE = re.compile(
    r"(?:^|[\s,{}])(?:\*|button|:where\([^)]*\)|:is\([^)]*\))?\s*:focus-visible\s*[,{]", re.IGNORECASE
)


def _button_focus_hits(content, source_file, context=None):
    """Styled buttons with no focus-visible style in their class list, their stylesheet, or a global rule."""
    if (context or {}).get("global_focus_visible") or ":focus-visible" in content:
        return []
    if Path(source_file).suffix.lower() == ".css":
        # A button rule that paints its own surface needs its own focus style.
        return [
            (offset, None)
            for selector, body, offset in iter_css_rule_spans(content)
            if re.search(r"(?:^|[\s,>+~])(?:button\b|\.btn\b|\.button\b|\[type=[\"']?(?:button|submit))", selector)
            and re.search(r"\b(?:background|border)(?:-color)?\s*:", body, re.IGNORECASE)
        ]
    hits = []
    for tag in re.finditer(r"<button\b[^>]*>", content):
        classes = CLASS_ATTRIBUTE_RE.search(tag.group(0))
        if classes and not re.search(r"(?<![\w-])focus(?:-visible)?:", classes.group(1)):
            hits.append((tag.start(), None))
    return hits


PURE_BLACK_RE = r"(?:#000(?:000)?\b|\bblack\b|rgba?\(\s*0\s*,\s*0\s*,\s*0\b|rgba?\(\s*0\s+0\s+0\b)"
OVERLAY_CONTEXT_RE = re.compile(r"overlay|backdrop|scrim|modal|dialog|lightbox|(?<![\w-])inset-0(?![\w-])", re.IGNORECASE)


# bg-black and its arbitrary-value spellings: bg-[#000], bg-[#000000], bg-[rgb(0_0_0/0.5)], bg-[rgba(0,0,0,.5)].
BLACK_BACKGROUND_UTILITY_RE = re.compile(
    r"(?<![\w-])bg-(?:black|\[(?P<arbitrary>#000(?:000)?|rgba?\(\s*0[\s,_]+0[\s,_]+0(?P<alpha>[^\]]*)\))\])"
    r"(?P<opacity>/(?:\d+|\[[^\]]+\]))?(?![\w/-])",
    re.IGNORECASE,
)


def _line_at(content, offset):
    start = content.rfind("\n", 0, offset) + 1
    end = content.find("\n", offset)
    return content[start:end if end != -1 else len(content)]


def _pure_black_hits(content):
    """Translucent black backgrounds, and opaque black on overlays, instead of the warm ink scrim."""
    hits = []
    for match in BLACK_BACKGROUND_UTILITY_RE.finditer(content):
        translucent = bool(match.group("opacity")) or bool(re.search(r"[,/_]\s*\.?\d", match.group("alpha") or ""))
        if translucent or OVERLAY_CONTEXT_RE.search(_line_at(content, match.start())):
            hits.append((match.start(), None))
    for selector, body, offset in iter_css_rule_spans(content):
        if OVERLAY_CONTEXT_RE.search(selector):
            background = re.search(r"background(?:-color)?\s*:\s*" + PURE_BLACK_RE, body, re.IGNORECASE)
            if background:
                hits.append((offset + background.start(), None))
    # Inline styles on an overlay element: style={{ background: "#000" }} or style="background: #000".
    position = 0
    for line in content.splitlines(keepends=True):
        inline = re.search(r"background(?:Color)?\s*:\s*[\"'`]?\s*" + PURE_BLACK_RE, line, re.IGNORECASE)
        if inline and OVERLAY_CONTEXT_RE.search(line):
            hits.append((position + inline.start(), None))
        position += len(line)
    return hits


def _component_violations(content, source_file, context=None):
    """House rules that live in class lists and stylesheets: tracked capitals, focus rings, and overlays."""
    code = strip_code_comments(content)
    violations = []
    if _tracked_uppercase_hits(code):
        violations.append((
            "tracked-uppercase-label",
            "Set labels in sentence case without wide tracking; let size and weight carry the hierarchy.",
            source_file,
        ))
    if _button_focus_hits(code, source_file, context):
        violations.append((
            "button-focus-ring-missing",
            "Give every button a visible 2px focus-visible ring (focus-visible:ring-2 or a :focus-visible rule).",
            source_file,
        ))
    if _pure_black_hits(code):
        violations.append((
            "pure-black-overlay",
            "Tint overlays and backdrops with the warm ink scrim (var(--bc-scrim)), not pure black.",
            source_file,
        ))
    return violations


def _glyph_message(glyphs):
    distinct = ", ".join(f"'{glyph}'" for glyph in dict.fromkeys(glyphs))
    noun = "glyph" if len(dict.fromkeys(glyphs)) == 1 else "glyphs"
    return f"Replace the Unicode {noun} {distinct} in interface copy with a 1.5px monoline SVG icon or plain words."


def _craft_violations(content, source_file):
    """Copy, honesty, and focus findings shared with the house luxury standard."""
    violations = []
    # A dash between words is an aside; a leading dash used as a list marker is not copy.
    if _copy_hits(content, source_file, EM_DASH_COPY_RE):
        violations.append((
            "em-dash-copy",
            "Rewrite interface copy without em dashes; use a period, comma, colon, or parentheses.",
            source_file,
        ))
    if _copy_hits(content, source_file, BUZZWORD_RE):
        violations.append((
            "buzzword-copy",
            "Replace marketing buzzwords with a specific statement of what the product does.",
            source_file,
        ))
    if _copy_hits(content, source_file, UNVERIFIED_CLAIM_RE):
        violations.append((
            "unverified-claim",
            "Remove compliance, uptime, or speed claims unless the product can show evidence for them.",
            source_file,
        ))
    if re.search(r"<a\b[^>]*\bhref\s*=\s*[\"']#[\"']", content, re.IGNORECASE):
        violations.append((
            "dead-navigation-link",
            "Point every link at a real page or section, or render the item as plain text until it exists.",
            source_file,
        ))
    glyphs = [glyph for _, glyph in _copy_hits(content, source_file, UNICODE_GLYPH_RE)]
    if glyphs:
        violations.append(("unicode-glyph-copy", _glyph_message(glyphs), source_file))
    removes_outline = re.search(r"\boutline\s*:\s*(?:none|0)\b", content, re.IGNORECASE)
    replaces_focus = re.search(r":focus-visible[^{}]*\{[^{}]*\b(?:outline|box-shadow)\s*:", content, re.IGNORECASE)
    if removes_outline and not replaces_focus:
        violations.append((
            "focus-outline-removed",
            "Replace a removed outline with a visible :focus-visible indicator in the same source.",
            source_file,
        ))
    return violations


ACCENT_FILL = r"background(?:-color)?\s*:\s*(?:#(?:d97757|e28466|c15f3e)\b|var\(\s*--(?:bc-)?accent(?:-hover)?\s*\))"
WHITE_TEXT = r"(?<![-\w])color\s*:\s*(?:#fff(?:fff)?\b|white\b|var\(\s*--(?:bc-)?text-on-accent\s*\))"
ACCENT_FILL_WHITE_TEXT_RE = re.compile(
    r"\{[^{}]*?(?:" + ACCENT_FILL + r"[^{}]*?" + WHITE_TEXT + r"|" + WHITE_TEXT + r"[^{}]*?" + ACCENT_FILL + r")[^{}]*\}"
    r"|style\s*=\s*[\"'][^\"']*?(?:" + ACCENT_FILL + r"[^\"']*?" + WHITE_TEXT + r"|" + WHITE_TEXT + r"[^\"']*?" + ACCENT_FILL + r")",
    re.IGNORECASE,
)


def _accent_fill_violations(content, source_file):
    """White text on the mid-tone accent measures 3.12:1 and fails WCAG AA."""
    if ACCENT_FILL_WHITE_TEXT_RE.search(content):
        return [(
            "accent-fill-white-text",
            "White text on the mid-tone accent (#D97757) measures 3.12:1; fill with --bc-accent-strong (#B35637) instead.",
            source_file,
        )]
    return []


TAILWIND_DURATION_RE = re.compile(r"(?<![\w-])duration-(?:(?P<steps>\d+)|\[(?P<amount>\d*\.?\d+)(?P<unit>ms|s)\])(?![\w-])")
TAILWIND_EASE_RE = re.compile(r"(?<![\w-])ease-(?:in-out|in|out|linear)(?![\w-])")
TAILWIND_ARBITRARY_EASE_RE = re.compile(r"(?<![\w-])ease-\[([^\]]+)\]")
GSAP_EASE_RE = re.compile(r"\bease\s*:\s*[\"']([^\"']+)[\"']")
GSAP_DURATION_RE = re.compile(r"\bduration\s*:\s*(\d*\.?\d+)(?![\w.])")
# GSAP equivalents of the BC tokens (see references/gsap-orchestration.md).
GSAP_TOKEN_EASES = {"expo.out", "power2.inout", "none", "linear"}
GSAP_TOKEN_DURATIONS = {0.0, 0.15, 0.25, 0.4, 0.6, 1.8}


def _tailwind_duration_limit(line):
    if re.search(r"reveal", line, re.IGNORECASE):
        return 600
    if re.search(r"drawer|sheet|dialog|modal", line, re.IGNORECASE):
        return 400
    return 250


def _motion_hits(content):
    """(duration hits, easing hits) across CSS declarations, Tailwind classes, and GSAP calls.

    Each hit is (offset, None). CSS allows 400ms (drawers and modals) and the 1800ms thinking
    shimmer; Tailwind allows 250ms, 400ms on drawers and dialogs, and 600ms on reveals; GSAP uses
    the token table, except in scrubbed timelines, whose durations are proportions of scroll.
    """
    css = _strip_motion_comments(content)
    code = strip_code_comments(content)
    durations, easings = [], []
    for match in MOTION_DECLARATION_RE.finditer(css):
        property_name = match.group("property").strip().lower()
        value = match.group("value").strip()
        # Delays and iteration counts are not the visual motion duration budget.
        if property_name in {"transition", "animation"} or property_name.endswith("-duration"):
            for time in MOTION_TIME_RE.finditer(value):
                duration = _duration_ms(time.group("amount"), time.group("unit"))
                thinking = duration == 1800 and re.search(r"thinking|shimmer|pulse", f"{property_name} {value}", re.IGNORECASE)
                if duration > 400 and not thinking:
                    durations.append((match.start(), None))
                    break
        # Every active transition/animation must name an approved easing token or calm curve.
        if property_name in {"transition", "animation"} or property_name.endswith("-timing-function"):
            if value.lower() not in {"none", "initial", "inherit", "unset"} and not _easing_value_ok(value):
                easings.append((match.start(), None))
    for match in TAILWIND_DURATION_RE.finditer(code):
        if match.group("steps"):
            duration = float(match.group("steps"))
        else:
            duration = _duration_ms(match.group("amount"), match.group("unit"))
        if duration > _tailwind_duration_limit(_line_at(code, match.start())):
            durations.append((match.start(), None))
    easings.extend((match.start(), None) for match in TAILWIND_EASE_RE.finditer(code))
    for match in TAILWIND_ARBITRARY_EASE_RE.finditer(code):
        if _overshoots(match.group(1)):
            easings.append((match.start(), None))
    if GSAP_CALL_RE.search(code):
        easings.extend(
            (match.start(), None) for match in GSAP_EASE_RE.finditer(code) if match.group(1).lower() not in GSAP_TOKEN_EASES
        )
        if not re.search(r"\bscrub\s*:", code):
            durations.extend(
                (match.start(), None)
                for match in GSAP_DURATION_RE.finditer(code)
                if float(match.group(1)) not in GSAP_TOKEN_DURATIONS
            )
    return durations, easings


MOTION_DURATION_MESSAGE = (
    "Keep motion on the BC duration tokens: 150-250ms for UI (duration-150, duration-250, or 0.15/0.25 in GSAP), "
    "400ms for drawers and dialogs, 600ms only for once-only reveals, and the shimmer token for 1800ms thinking states."
)
MOTION_EASING_MESSAGE = (
    "Use a BC easing token (var(--bc-ease), ease-[var(--bc-ease)], or \"expo.out\"/\"power2.inOut\" in GSAP); "
    "avoid browser-default keywords and cubic-bezier curves that overshoot or bounce."
)


def _utility_motion_violations(content, source_file):
    """Duration and easing findings for CSS, Tailwind, and GSAP motion."""
    durations, easings = _motion_hits(content)
    violations = []
    if durations:
        violations.append(("motion-duration-budget", MOTION_DURATION_MESSAGE, source_file))
    if easings:
        violations.append(("motion-easing-token", MOTION_EASING_MESSAGE, source_file))
    return violations


def _gsap_violations(content, source_file):
    """Reduced-motion and layout findings for GSAP-driven motion."""
    if not GSAP_CALL_RE.search(content):
        return []
    violations = []
    if not re.search(r"prefers-reduced-motion|reduced?[-_ ]?motion|gsap\.matchMedia", content, re.IGNORECASE):
        violations.append((
            "gsap-reduced-motion",
            "Wrap GSAP choreography in gsap.matchMedia with a prefers-reduced-motion branch.",
            source_file,
        ))
    if GSAP_LAYOUT_TWEEN_RE.search(content):
        violations.append((
            "gsap-layout-property",
            "Tween transforms and opacity with GSAP; animating layout properties causes reflow and jank.",
            source_file,
        ))
    return violations


ROUND_BY_NATURE_RE = re.compile(
    r"avatar|radio|checkbox|switch|toggle|thumb|slider|progress|spinner|\bdot\b|indicator|aspect-square|\bsize-\d",
    re.IGNORECASE,
)
# A layout property named as what a transition or animation changes, in CSS, Tailwind, or a JS animate prop.
LAYOUT_ANIMATION_RE = re.compile(
    r"transition(?:-property)?\s*:\s*[^;{}\n]*\b(?:width|height|margin|padding)\b"
    r"|\btransition-\[[^\]]*(?:width|height|margin|padding)[^\]]*\]"
    r"|\banimate\s*[=:(]\s*\{\{?[^{}]*\b(?:width|height|margin\w*|padding\w*)\s*:",
    re.IGNORECASE,
)
IGNORE_COMMENT_RE = re.compile(r"bc-audit-ignore:\s*([a-z0-9-]+(?:\s*,\s*[a-z0-9-]+)*)", re.IGNORECASE)


def _naturally_round(line):
    """Avatars, radios, dots, progress bars, and equal-sided circles are round by nature, not pill buttons."""
    if ROUND_BY_NATURE_RE.search(line):
        return True
    return any(
        re.search(rf"\bw-{re.escape(size)}\b", line)
        for size in re.findall(r"\bh-(\d+(?:\.\d+)?|\[[^\]]+\])", line)
    )


def _pill_context(content, match):
    """The class list or CSS rule a radius sits in: its own line plus the selector of the rule it belongs to."""
    line_start = content.rfind("\n", 0, match.start()) + 1
    line_end = content.find("\n", match.end())
    rule_start = max(content.rfind("}", 0, match.start()) + 1, match.start() - 300)
    return content[min(line_start, rule_start):line_end if line_end != -1 else len(content)]


def _ignored_rules(content):
    """Rules a file opts out of with a `bc-audit-ignore: rule-id, rule-id` comment, for a reason stated beside it."""
    return {rule.strip().lower() for match in IGNORE_COMMENT_RE.finditer(content) for rule in match.group(1).split(",")}


# Rules found by one pattern each; every match is a finding on its own line.
PATTERN_CHECKS = [
    (
        "monotonous-card-kit",
        re.compile(r"rounded-xl\s+p-6", re.IGNORECASE),
        "Avoid the repeated rounded-xl p-6 card template.",
    ),
    (
        "template-arrow-cta",
        re.compile(r"(?:button|cta|class(?:name)?\s*=)[^\n]{0,160}→", re.IGNORECASE),
        "Use an active-voice CTA without a decorative arrow suffix.",
    ),
    (
        "middle-dot-metadata",
        re.compile(r"\s·\s"),
        "Avoid middle-dot metadata strings; use a label, line break, or meaningful punctuation.",
    ),
    (
        "template-arrow-glyph",
        re.compile(
            r"<(?:a|button)\b[^>]*>[\s\S]{0,320}?[↗↘→←↑↓][\s\S]{0,120}?</(?:a|button)>",
            re.IGNORECASE,
        ),
        "Remove decorative arrow glyphs from links and buttons; make the action label carry the meaning.",
    ),
    (
        "unicode-icon-glyph",
        re.compile(
            r"<[^>]*\baria-hidden\s*=\s*['\"]true['\"][^>]*>\s*[⌖↗↘→←↑↓★☆✦✧]\s*</[^>]+>",
            re.IGNORECASE,
        ),
        "Use a purposeful 1.5px monoline SVG icon instead of a Unicode glyph.",
    ),
    (
        "decorative-index-marker",
        re.compile(r"(?:>\s*[A-C]\s*<|\b0[1-9]\s+—\s+[A-Za-z])"),
        "Do not use decorative A/B/C or 01—03 markers unless they encode a real ordered sequence.",
    ),
    (
        "focus-ring-width",
        re.compile(
            r":focus-visible[^{}]*\{[^{}]*\boutline\s*:\s*(?!2px\b)\d+px",
            re.IGNORECASE | re.DOTALL,
        ),
        "Use a visible 2px focus ring for keyboard users.",
    ),
    (
        "sticky-z-index-token",
        re.compile(
            r"(?:position\s*:\s*sticky[^{}]*\bz-index\s*:\s*(?!30\b)\d+|"
            r"\bz-index\s*:\s*(?!30\b)\d+[^{}]*position\s*:\s*sticky)",
            re.IGNORECASE | re.DOTALL,
        ),
        "Use the semantic sticky-nav z-index token (30), not an arbitrary layer number.",
    ),
]

GLYPH_IN_MATCH_RE = re.compile("[⌖↗↘→←↑↓★☆✦✧]")


def _pattern_hits(pattern, content):
    """Offsets of each match, pointing at the glyph when the match spans a whole link or button."""
    hits = []
    for match in pattern.finditer(content):
        glyph = GLYPH_IN_MATCH_RE.search(match.group(0))
        hits.append((match.start() + (glyph.start() if glyph else 0), None))
    return hits


def _line_locators():
    """Rules whose findings can be pinned to each offending line, mapped to their hit finders."""
    code = strip_code_comments
    patterns = {
        rule_id: (lambda content, source_file, context, pattern=pattern: _pattern_hits(pattern, content))
        for rule_id, pattern, _ in PATTERN_CHECKS
    }
    return {
        **patterns,
        "motion-duration-budget": lambda content, source_file, context: _motion_hits(content)[0],
        "motion-easing-token": lambda content, source_file, context: _motion_hits(content)[1],
        "pure-black-overlay": lambda content, source_file, context: _pure_black_hits(code(content)),
        "tracked-uppercase-label": lambda content, source_file, context: _tracked_uppercase_hits(code(content)),
        "button-focus-ring-missing": lambda content, source_file, context: _button_focus_hits(code(content), source_file, context),
        "unicode-glyph-copy": lambda content, source_file, context: _copy_hits(content, source_file, UNICODE_GLYPH_RE),
        "em-dash-copy": lambda content, source_file, context: _copy_hits(content, source_file, EM_DASH_COPY_RE),
        "buzzword-copy": lambda content, source_file, context: _copy_hits(content, source_file, BUZZWORD_RE),
        "unverified-claim": lambda content, source_file, context: _copy_hits(content, source_file, UNVERIFIED_CLAIM_RE),
    }


def violation_locations(rule_id, content, source_file, context=None):
    """[(line, message or None)] for every line that breaks ``rule_id``, or None when the rule is file-level.

    A message is returned only when it differs by line: the glyph rule names the glyphs on that line.
    """
    locator = _line_locators().get(rule_id)
    if locator is None:
        return None
    by_line = {}
    for offset, detail in locator(content, source_file, context):
        by_line.setdefault(content.count("\n", 0, offset) + 1, []).append(detail)
    if rule_id == "unicode-glyph-copy":
        return [(line, _glyph_message(glyphs)) for line, glyphs in sorted(by_line.items())]
    return [(line, None) for line in sorted(by_line)]


def find_audit_violations(content, source_file, context=None):
    """Return explainable BC Design quality findings for one source file."""
    violations = []
    for rule_id, pattern, message in PATTERN_CHECKS:
        if pattern.search(content):
            violations.append((rule_id, message, source_file))

    if re.search(r"setPixelRatio\s*\(\s*(?:window\.)?devicePixelRatio\s*\)", content) and not re.search(r"Math\.min\s*\([^)]*(?:window\.)?devicePixelRatio", content):
        violations.append((
            "spatial-uncapped-pixel-ratio",
            "Cap WebGL pixel ratio with Math.min(window.devicePixelRatio, 2) to avoid GPU thermal throttling and frame drops.",
            source_file,
        ))

    pill_count = sum(
        1 for match in re.finditer(r"(?:border-radius\s*:\s*999(?:px)?|rounded-full)", content, re.IGNORECASE)
        if not _naturally_round(_pill_context(content, match))
    )
    if pill_count >= 3:
        violations.append((
            "excessive-pill-capsules",
            "Reserve full-pill geometry for tags, filters, and compact statuses; vary primary controls and surfaces.",
            source_file,
        ))
    if re.search(r"(?:linear|radial)-gradient\([^;{}\n]*(?:#(?:7c3aed|8b00ff|2563eb|6366f1)|neon|purple|electric blue)", content, re.IGNORECASE):
        violations.append((
            "generic-gradient-wash",
            "Do not use a saturated purple/blue gradient as unearned page decoration; ground visual emphasis in the subject.",
            source_file,
        ))
    if re.search(r"(?:^|\n)\s*(?:html|body|:root)\b[^\{]*\{[^}]*background(?:-color)?\s*:\s*(?:#(?:d97757|e28466)|var\(\s*--(?:bc-)?accent\b)", content, re.IGNORECASE):
        violations.append((
            "accent-surface-domination",
            "Keep subject-derived accents to intentional moments; do not make the page canvas the accent by default.",
            source_file,
        ))
    if re.search(r"--(?:bc-)?text-on-accent\s*:\s*#(?:1[fF]1[eE]1[bB]|181816|000000|000|111)\b", content, re.IGNORECASE):
        violations.append((
            "accent-button-text-contrast",
            "Do not put button text on the mid-tone accent; use the ink button (.bc-btn-contrast) or white text on --bc-accent-strong.",
            source_file,
        ))
    elif re.search(
        r"(?:button|\.btn[a-z0-9_-]*|\[type=['\"]?submit['\"]?\])[^{}]*\{[^{}]*background(?:-color)?\s*:\s*(?:#(?:d97757|e28466)|var\(\s*--(?:bc-)?accent\b)[^{}]*color\s*:\s*(?:#(?:1[fF]1[eE]1[bB]|181816|000000|000|111)\b|black\b|var\(\s*--(?:bc-)?text-primary\b)",
        content,
        re.IGNORECASE | re.DOTALL,
    ) or re.search(
        r"(?:button|\.btn[a-z0-9_-]*|\[type=['\"]?submit['\"]?\])[^{}]*\{[^{}]*color\s*:\s*(?:#(?:1[fF]1[eE]1[bB]|181816|000000|000|111)\b|black\b|var\(\s*--(?:bc-)?text-primary\b)[^{}]*background(?:-color)?\s*:\s*(?:#(?:d97757|e28466)|var\(\s*--(?:bc-)?accent\b)",
        content,
        re.IGNORECASE | re.DOTALL,
    ):
        violations.append((
            "accent-button-text-contrast",
            "Do not put button text on the mid-tone accent; use the ink button (.bc-btn-contrast) or white text on --bc-accent-strong.",
            source_file,
        ))
    elif re.search(
        r"<[^>]*(?:button|a\b)[^>]*style\s*=\s*['\"][^'\"]*background(?:-color)?\s*:\s*(?:#(?:d97757|e28466)|var\(\s*--(?:bc-)?accent\b)[^'\"]*color\s*:\s*(?:#(?:1[fF]1[eE]1[bB]|181816|000000|000|111)\b|black\b|var\(\s*--(?:bc-)?text-primary\b)",
        content,
        re.IGNORECASE,
    ) or re.search(
        r"<[^>]*(?:button|a\b)[^>]*style\s*=\s*['\"][^'\"]*color\s*:\s*(?:#(?:1[fF]1[eE]1[bB]|181816|000000|000|111)\b|black\b|var\(\s*--(?:bc-)?text-primary\b)[^'\"]*background(?:-color)?\s*:\s*(?:#(?:d97757|e28466)|var\(\s*--(?:bc-)?accent\b)",
        content,
        re.IGNORECASE,
    ):
        violations.append((
            "accent-button-text-contrast",
            "Do not put button text on the mid-tone accent; use the ink button (.bc-btn-contrast) or white text on --bc-accent-strong.",
            source_file,
        ))

    # Distinctive-quality heuristics are aggregate and deliberately
    # conservative: a single label or large heading can be legitimate, while
    # repeated template patterns are useful audit evidence.
    uppercase_labels = re.findall(
        r"<[^>]*class\s*=\s*[\"'][^\"']*(?:eyebrow|overline|kicker|label)[^\"']*[\"'][^>]*>\s*([A-Z][A-Z0-9 &'/-]{4,})\s*</",
        content,
    )
    if len(uppercase_labels) >= 3:
        violations.append((
            "decorative-eyebrow-overload",
            "Reduce repeated tracked-out or all-caps eyebrow labels; let hierarchy come from meaningful headings.",
            source_file,
        ))
    if re.search(
        r"(?:hero|masthead|headline)[^\{]{0,80}\{[^}]*font-size\s*:\s*(?:[9]\d|1\d\d|[2-9]\d{2})px",
        content,
        re.IGNORECASE | re.DOTALL,
    ) or re.search(r"(?:hero|masthead)[^\n]{0,120}\btext-(?:8|9)xl\b", content, re.IGNORECASE):
        violations.append((
            "oversized-hero-displacement",
            "Keep hero type proportional so useful product content remains visible in the first viewport.",
            source_file,
        ))
    chrome_markers = ("new task", "projects", "settings", "upgrade", "share")
    if sum(1 for marker in chrome_markers if re.search(r"\b" + re.escape(marker) + r"\b", content, re.IGNORECASE)) >= 3:
        violations.append((
            "copied-platform-chrome",
            "Remove copied platform labels unless they are required by the product's own information architecture.",
            source_file,
        ))
    # Count visible labels only (element text or a label attribute), not state names such as status === "submit".
    generic_cta_count = len(re.findall(
        r"(?:>|\b(?:aria-label|label|title|value)=[\"'])\s*(?:get started|learn more|explore now|sign up|submit)\s*(?:<|[\"'])",
        content,
        re.IGNORECASE,
    ))
    if generic_cta_count >= 3:
        violations.append((
            "repeated-generic-cta",
            "Replace repeated generic CTA labels with specific actions that describe the user's next step.",
            source_file,
        ))

    streaming_marker = re.search(r"\b(stream|streaming|token|ai[- ]output)\b", content, re.IGNORECASE)
    dimension_animation = LAYOUT_ANIMATION_RE.search(content)
    if streaming_marker and dimension_animation:
        violations.append(
            (
                "streaming-layout-animation",
                "Do not animate width, height, margin, or padding while tokens stream.",
                source_file,
            )
        )
    violations.extend(_motion_violations(content, source_file))
    violations.extend(_utility_motion_violations(content, source_file))
    violations.extend(_component_violations(content, source_file, context))
    violations.extend(_craft_violations(content, source_file))
    violations.extend(_gsap_violations(content, source_file))
    violations.extend(_accent_fill_violations(content, source_file))
    ignored = _ignored_rules(content)
    unique = {}
    for violation in violations:
        if violation[0] not in ignored:
            unique.setdefault(violation[0], violation)
    return list(unique.values())


def audit_target(target):
    """Audit a source file or directory and return rule violations."""
    target = Path(target)
    if not target.exists():
        raise FileNotFoundError(str(target))
    files = [(source_file, source_file.read_text(encoding="utf-8", errors="ignore")) for source_file in iter_source_files(target)]
    # A global :focus-visible rule in any stylesheet covers buttons in every component.
    context = {
        "global_focus_visible": any(
            GLOBAL_FOCUS_VISIBLE_RE.search(strip_code_comments(content))
            for source_file, content in files
            if source_file.suffix.lower() == ".css"
        )
    }
    violations = []
    for source_file, content in files:
        violations.extend(find_audit_violations(content, source_file, context))
    return violations

# ----------------- MAIN CLI DISPATCHER -----------------


def main():
    parser = argparse.ArgumentParser(
        description="BC Design System CLI - subject-grounded design intelligence"
    )
    parser.add_argument("query", nargs="?", default=None, help="Design brief or search query")
    parser.add_argument("--design-system", "-ds", action="store_true", help="Generate complete distinctive design system")
    parser.add_argument("--project-name", "-p", type=str, default=None, help="Project name")
    parser.add_argument("--brand-guidelines", action="store_true", help="Print BC Design guidelines and the quality checklist")
    parser.add_argument("--design-audit", "--audit", dest="design_audit", metavar="TARGET", help="Audit a source file or directory for enforceable BC Design quality findings")
    parser.add_argument("--json", action="store_true", help="Emit structured JSON findings (only with --audit)")
    parser.add_argument("--contrast", nargs=2, metavar=("HEX1", "HEX2"), help="Compute WCAG 2.x contrast ratio between two hex colors")
    parser.add_argument("--domain", "-d", choices=list(CSV_CONFIG.keys()), help="Search a bundled domain (style, color, typography, chart, landing, product, ux, motion, icons, google-fonts, spatial)")
    parser.add_argument("--max-results", "-n", type=int, default=3, help="Max results for domain search")
    parser.add_argument("--persist", action="store_true", help="Save design system to design-system/<project-slug>/MASTER.md")
    parser.add_argument("--page", type=str, default=None, help="Create page-specific override in design-system/<project-slug>/pages/")
    parser.add_argument("--output-dir", "-o", type=str, default=".", help="Output directory")
    parser.add_argument("--force", action="store_true", help="Overwrite existing MASTER.md")
    parser.add_argument("--variance", type=int, choices=range(1, 11), help="Design variance dial (1=minimal, 10=bold/asymmetric)")
    parser.add_argument("--motion", type=int, choices=range(1, 11), help="Motion intensity dial (1=subtle, 10=choreographed)")
    parser.add_argument("--density", type=int, choices=range(1, 11), help="Visual density dial (1=spacious, 10=dashboard)")
    parser.add_argument("--stack", metavar="STACK", help="Output a focused guide or searchable stack catalog")
    parser.add_argument("--spatial", nargs="?", const="list", metavar="PRESET", help="Generate a 3D / spatial WebGL component (ribbon-field, predictive-arc, school-spatial, etc.) or list available presets")
    parser.add_argument("--spatial-palette", default="terracotta", choices=["terracotta", "amber-brass", "sage-monochrome"], help="Color palette for spatial component")
    parser.add_argument("--spatial-theme", default="dark", choices=["dark", "light"], help="Theme mode for spatial component (dark or light)")
    parser.add_argument("--spatial-format", default="html", choices=["html", "react"], help="Output format for spatial component (html or react)")

    args = parser.parse_args()

    if args.json and args.design_audit is None:
        parser.error("--json requires --audit TARGET")

    # Spatial 3D shader generator
    if args.spatial:
        try:
            from spatial import PALETTES, SPATIAL_GENERATOR_PRESETS, SPATIAL_PRESET_ALIASES, SPATIAL_PRESETS, generate_spatial_component
        except ImportError:
            from .spatial import PALETTES, SPATIAL_GENERATOR_PRESETS, SPATIAL_PRESET_ALIASES, SPATIAL_PRESETS, generate_spatial_component

        if args.spatial == "list":
            print("\n" + "="*80)
            print("  BC DESIGN SPATIAL & 3D SHADER PRESETS")
            print("="*80 + "\n")
            for key in SPATIAL_GENERATOR_PRESETS:
                p = SPATIAL_PRESETS[key]
                print(f"• {key} ({p['name']}) [{p['runtime']}]")
                print(f"  Description: {p['description']}")
                print(f"  Best for: {p['best_for']}\n")
            print("Available palettes: " + ", ".join(PALETTES.keys()) + "\n")
            return 0

        preset = args.spatial
        if preset not in SPATIAL_GENERATOR_PRESETS and preset not in SPATIAL_PRESET_ALIASES:
            available = ", ".join(SPATIAL_GENERATOR_PRESETS)
            print(f"Error: Preset '{preset}' is catalog-only or unknown. Generatable presets: {available}")
            return 1

        code = generate_spatial_component(preset, args.spatial_palette, args.spatial_theme, args.spatial_format)
        ext = "html" if args.spatial_format == "html" else "tsx"
        if args.output_dir and args.output_dir != ".":
            out_path = Path(args.output_dir)
            if out_path.is_dir():
                out_path = out_path / f"bc-{preset}.{ext}"
        else:
            out_path = Path(f"bc-{preset}.{ext}")

        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(code, encoding="utf-8")
        print(f"[BC Spatial] Successfully generated '{preset}' [{args.spatial_palette} / {args.spatial_theme}] -> {out_path}")
        return 0

    # 1. BC Design guideline display
    if args.brand_guidelines:
        print("\n" + "="*80)
        print("  BC DESIGN GUIDELINES & QUALITY CHECKS")
        print("="*80 + "\n")
        for guideline, desc in BC_DESIGN_GUIDELINES:
            print(f"• {guideline}:")
            print(f"  {desc}\n")
        return

    # 2. Design audit validation
    if args.design_audit is not None:
        try:
            violations = audit_target(args.design_audit)
        except FileNotFoundError:
            if args.json:
                print(json.dumps({"status": "error", "target": args.design_audit, "findings": [], "summary": {"total": 0}}, ensure_ascii=False))
            else:
                print(f"Error: audit target not found: {args.design_audit}", file=sys.stderr)
            return 2
        if args.json:
            # Import lazily so the legacy single-file entrypoint remains usable
            # when copied into runtimes that only include this script.
            try:
                from audit import build_audit_findings, summarize_by_dimension
                findings = build_audit_findings(args.design_audit)
            except Exception as exc:
                print(json.dumps({"status": "error", "target": args.design_audit, "findings": [], "summary": {"total": 0}, "error": str(exc)}, ensure_ascii=False))
                return 2
            payload = {
                "status": "fail" if findings else "pass",
                "target": str(args.design_audit),
                "findings": findings,
                "summary": {
                    "total": len(findings),
                    "errors": sum(1 for finding in findings if finding["severity"] == "error"),
                    "warnings": sum(1 for finding in findings if finding["severity"] == "warning"),
                    "by_category": {
                        category: sum(1 for finding in findings if finding.get("category") == category)
                        for category in ("identity", "hierarchy", "decoration", "copy", "content", "motion", "accessibility", "performance")
                        if any(finding.get("category") == category for finding in findings)
                    },
                    "by_dimension": summarize_by_dimension(findings),
                },
            }
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            return 1 if findings else 0
        if not violations:
            print(f"AUDIT PASS: {args.design_audit}")
            return 0
        try:
            from audit import build_audit_findings
            findings = build_audit_findings(args.design_audit)
        except Exception:
            findings = [
                {"rule_id": rule_id, "message": message, "path": str(source_file), "line": 1, "evidence": ""}
                for rule_id, message, source_file in violations
            ]
        print(f"AUDIT FAIL: {len(findings)} finding(s) in {args.design_audit}")
        for finding in findings:
            evidence = f" Evidence: {finding['evidence']}" if finding.get("evidence") else ""
            message = finding["message"].rstrip(".")
            dimension = f" ({finding['dimension']})" if finding.get("dimension") else ""
            print(f"  [{finding['rule_id']}]{dimension} {finding['path']}:{finding['line']}: {message}.{evidence}")
        return 1

    # 3. Contrast Checker
    if args.contrast:
        try:
            h1, h2 = args.contrast
            ratio = compute_contrast(h1, h2)
            normal = ratio >= 4.5
            large = ratio >= 3.0
            print("\n" + "="*50)
            print(f"  WCAG 2.x CONTRAST RATIO: {h1} on {h2}")
            print("="*50)
            print(f"Ratio: {ratio:.2f}:1")
            print(f"Normal text (>= 4.5:1 WCAG AA): {'[PASS]' if normal else '[FAIL]'}")
            print(f"Large text  (>= 3.0:1 WCAG AA): {'[PASS]' if large else '[FAIL]'}")
            if ratio >= 7.0:
                print("WCAG AAA (>= 7.0:1):            [PASS] - High Distinction")
            print("="*50 + "\n")
            return
        except Exception as e:
            print(f"Error computing contrast: {e}")
            return

    # 4. Database Domain Search (BM25 across 192 products, 74 fonts, etc.)
    if args.domain and args.query:
        res = search_domain(args.domain, args.query, max_results=args.max_results, selection_mode=requested_selection_mode(args.query))
        if "error" in res:
            print(f"Error: {res['error']}")
            return
        print(f"\n[Search Domain: {args.domain.upper()} | Query: '{args.query}' | Found: {res['count']}]")
        if res.get("blocked"):
            print(f"[Blocked by quality gate: {res['blocked']}]")
        for i, r in enumerate(res['results'], 1):
            print(f"\n--- Result {i} ---")
            for k, v in r.items():
                if v:
                    print(f"  {k}: {v}")
        print()
        return

    # 5. Design system generator
    if args.design_system or (args.query and not any([args.domain, args.stack])):
        q = args.query or "AI Conversational Workspace"
        card, data = generate_design_system(
            q,
            project_name=args.project_name,
            variance=args.variance,
            motion=args.motion,
            density=args.density
        )
        print(card)
        if args.persist:
            persist_master(data, output_dir=args.output_dir, page=args.page, force=args.force)
        return

    # 6. Tech Stack Guide
    if args.stack:
        canonical_stack = resolve_stack_name(args.stack)
        if canonical_stack not in stack_catalog_names():
            print(f"Error: unknown stack '{args.stack}'. Available: {', '.join(stack_catalog_names())}")
            return 1
        stack_file = SKILL_ROOT / "stacks" / f"{args.stack}.md"
        if not stack_file.exists() and canonical_stack != args.stack:
            stack_file = SKILL_ROOT / "stacks" / f"{canonical_stack}.md"
        if os.path.exists(stack_file):
            with open(stack_file, "r", encoding="utf-8") as f:
                print(f"# Stack guidance: {args.stack}")
                print(f.read())
        else:
            result = search_stack(args.stack, args.query, max_results=args.max_results)
            print(f"# Stack guidance: {args.stack} ({result['count']} catalog rules)")
            for index, item in enumerate(result["results"], 1):
                print(f"\n## Rule {index}")
                for key, value in item["guidance"].items():
                    if value:
                        print(f"- {key}: {value}")
        return

    parser.print_help()

if __name__ == "__main__":
    raise SystemExit(main() or 0)
