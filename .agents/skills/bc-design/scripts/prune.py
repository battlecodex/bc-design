#!/usr/bin/env python3
"""Find design code a project no longer uses, without changing anything.

prune.py reads a project and reports numbered candidates for removal or
consolidation:

    unused-token          CSS custom properties that are declared but never referenced
    unused-class          Class selectors that no markup or script mentions
    unused-font           Font families that are loaded but never set anywhere
    unused-asset          Images, icons, fonts, and media files nothing links to
    unused-package        Design packages in package.json that nothing imports
    hardcoded-token-color Raw hex colors that equal an existing token
    near-duplicate-color  Hex colors so close they should be one token

Every finding carries a confidence level and file:line evidence. The report
is saved to .bc-design/prune-report.json so the user can approve findings by
number. prune.py never deletes or edits files: remove only the approved
findings, and compare render_check.py screenshots before and after.

Standard library only.
"""

from __future__ import annotations

import argparse
from datetime import date
from fnmatch import fnmatch
import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from project import MEMORY_DIR, _walk_files  # noqa: E402

REPORT_FILE = "prune-report.json"
STYLE_SUFFIXES = {".css", ".scss", ".sass", ".less"}
MARKUP_SUFFIXES = {".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte", ".astro", ".mdx", ".php", ".erb", ".liquid", ".hbs", ".njk"}
SCRIPT_SUFFIXES = {".js", ".mjs", ".cjs", ".ts"}
DATA_SUFFIXES = {".json", ".md", ".yml", ".yaml", ".toml", ".webmanifest", ".xml"}
ASSET_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif", ".svg", ".ico", ".woff", ".woff2", ".ttf", ".otf", ".mp4", ".webm", ".lottie"}
LOCKFILES = {"package-lock.json", "yarn.lock", "pnpm-lock.yaml", "bun.lockb", "npm-shrinkwrap.json"}
CONVENTIONAL_ASSETS = ("favicon*", "apple-touch-icon*", "android-chrome-*", "mstile-*", "safari-pinned-tab*", "og-image*", "opengraph-image*", "twitter-image*", "icon.*", "robots.*")
DESIGN_PACKAGES = (
    "gsap", "@gsap/react", "framer-motion", "motion", "lenis", "@studio-freight/lenis", "lottie-react", "lottie-web",
    "three", "@react-three/fiber", "@react-three/drei", "animate.css", "aos", "swiper", "lucide-react", "lucide",
    "@phosphor-icons/react", "react-icons", "@heroicons/react", "@headlessui/react", "bootstrap", "bulma",
    "tailwindcss-animate", "@tailwindcss/typography", "@tailwindcss/forms", "@formkit/auto-animate", "@react-spring/web",
)
DESIGN_PACKAGE_PREFIXES = ("@fontsource/", "@fontsource-variable/", "@radix-ui/")
CONFIDENCE_ORDER = {"high": 0, "medium": 1, "low": 2}


class Source:
    """One readable project file with line lookup."""

    def __init__(self, root, path):
        self.path = path
        self.rel = path.relative_to(root).as_posix()
        self.text = path.read_text(encoding="utf-8", errors="ignore")
        self.suffix = path.suffix.lower()

    def line(self, offset):
        return self.text.count("\n", 0, offset) + 1

    def cite(self, offset):
        return f"{self.rel}:{self.line(offset)}"

    def styles(self):
        """Yield (offset, css) for this file's stylesheet text."""
        if self.suffix in STYLE_SUFFIXES:
            yield 0, self.text
        elif self.suffix in MARKUP_SUFFIXES:
            for match in re.finditer(r"<style\b[^>]*>(.*?)</style>", self.text, re.IGNORECASE | re.DOTALL):
                yield match.start(1), match.group(1)


def load_sources(root, keep=()):
    sources, assets = [], []
    readable = STYLE_SUFFIXES | MARKUP_SUFFIXES | SCRIPT_SUFFIXES | DATA_SUFFIXES
    for path in _walk_files(root):
        rel = path.relative_to(root).as_posix()
        if rel.startswith(MEMORY_DIR + "/") or path.name in LOCKFILES:
            continue
        suffix = path.suffix.lower()
        if suffix in ASSET_SUFFIXES:
            assets.append(path)
        if suffix in readable or path.name.startswith("tailwind.config"):
            source = Source(root, path)
            source.kept = any(fnmatch(rel, pattern) for pattern in keep)
            sources.append(source)
    return sources, assets


def _strip_comments(css):
    return re.sub(r"/\*.*?\*/", lambda m: " " * len(m.group(0)), css, flags=re.DOTALL)


def _word(name):
    return re.compile(r"(?<![\w-])" + re.escape(name) + r"(?![\w-])")


# ------------------------------------------------------------------ checks


def find_unused_tokens(sources):
    declared = {}
    for source in sources:
        if source.kept:
            continue
        for offset, css in source.styles():
            for match in re.finditer(r"(?<![\w-])(--[A-Za-z0-9_-]+)\s*:", _strip_comments(css)):
                declared.setdefault(match.group(1), []).append(source.cite(offset + match.start(1)))
    findings = []
    for name, sites in sorted(declared.items()):
        pattern = _word(name)
        uses = sum(len(pattern.findall(source.text)) for source in sources)
        if uses <= len(sites):
            findings.append({
                "kind": "unused-token",
                "confidence": "high",
                "subject": name,
                "evidence": sites[0],
                "detail": f"Declared {len(sites)} time(s), never read with var({name}) or by script.",
                "action": f"Remove the {name} declaration.",
            })
    return findings


def find_unused_classes(sources):
    readers = [s for s in sources if s.suffix in MARKUP_SUFFIXES | SCRIPT_SUFFIXES]
    if not readers:
        return []
    reader_text = "\n".join(s.text for s in readers)
    declared = {}
    for source in sources:
        if source.kept:
            continue
        for offset, css in source.styles():
            clean = _strip_comments(css)
            for block in re.finditer(r"([^{}]+)\{", clean):
                selector = block.group(1)
                if selector.lstrip().startswith("@"):
                    continue
                for match in re.finditer(r"\.(-?[A-Za-z_][\w-]*)", selector):
                    declared.setdefault(match.group(1), source.cite(offset + block.start(1) + match.start()))
    findings = []
    for name, site in sorted(declared.items()):
        if _word(name).search(reader_text):
            continue
        prefix = name.rsplit("-", 1)[0] + "-" if "-" in name else None
        dynamic = prefix and re.search(re.escape(prefix) + r"(?:\$\{|[\"']\s*\+)", reader_text)
        findings.append({
            "kind": "unused-class",
            "confidence": "low" if dynamic else "medium",
            "subject": f".{name}",
            "evidence": site,
            "detail": "No markup or script mentions this class" + (f"; names starting with '{prefix}' are built dynamically, so check by hand." if dynamic else "."),
            "action": f"Remove the .{name} rule after confirming it is not added at runtime.",
        })
    return findings


def _family_pattern(family):
    parts = [re.escape(part) for part in re.split(r"[\s+_-]+", family.strip()) if part]
    return re.compile(r"(?<![\w-])" + r"[\s+_-]?".join(parts) + r"(?![\w-])", re.IGNORECASE)


def find_unused_fonts(root, sources):
    loaded = {}
    masked = {}
    for source in sources:
        text = source.text
        spans = []
        for match in re.finditer(r"fonts\.googleapis\.com/css2?\?[^\"')\s]+", text):
            for family in re.findall(r"family=([^&:\"']+)", match.group(0).replace("&amp;", "&")):
                loaded.setdefault(family.replace("+", " "), source.cite(match.start()))
            spans.append(match.span())
        for offset, css in source.styles():
            for block in re.finditer(r"@font-face\s*\{[^}]*\}", css):
                family = re.search(r"font-family\s*:\s*[\"']?([^;\"']+)", block.group(0))
                if family:
                    loaded.setdefault(family.group(1).strip(), source.cite(offset + block.start()))
                spans.append((offset + block.start(), offset + block.end()))
        masked[source.rel] = spans
    package = Path(root) / "package.json"
    if package.is_file():
        package_text = package.read_text(encoding="utf-8", errors="ignore")
        try:
            deps = json.loads(package_text)
        except json.JSONDecodeError:
            deps = {}
        for name in {**deps.get("dependencies", {}), **deps.get("devDependencies", {})}:
            for prefix in ("@fontsource/", "@fontsource-variable/"):
                if name.startswith(prefix):
                    family = name[len(prefix):].replace("-", " ").title()
                    line = package_text.count("\n", 0, package_text.find(f'"{name}"')) + 1
                    loaded.setdefault(family, f"package.json:{line}")

    def usable(source):
        text = source.text
        for start, end in sorted(masked.get(source.rel, []), reverse=True):
            text = text[:start] + " " * (end - start) + text[end:]
        return text

    corpus = "\n".join(usable(s) for s in sources if s.path.name != "package.json")
    findings = []
    for family, site in sorted(loaded.items()):
        if not _family_pattern(family).search(corpus):
            findings.append({
                "kind": "unused-font",
                "confidence": "high",
                "subject": family,
                "evidence": site,
                "detail": "Loaded, but no font-family, token, or script ever names it.",
                "action": f"Stop loading {family}.",
            })
    return findings


def find_unused_assets(root, sources, assets):
    corpus = "\n".join(s.text for s in sources)
    findings = []
    for path in assets:
        if any(fnmatch(path.name.lower(), pattern) for pattern in CONVENTIONAL_ASSETS):
            continue
        if path.name in corpus:
            continue
        rel = path.relative_to(root).as_posix()
        findings.append({
            "kind": "unused-asset",
            "confidence": "medium",
            "subject": rel,
            "evidence": rel,
            "detail": f"No file mentions {path.name}; it may still be loaded by a CMS or a computed path.",
            "action": f"Delete {rel} after confirming no runtime path builds it.",
        })
    return findings


def find_unused_packages(root, sources):
    package = Path(root) / "package.json"
    if not package.is_file():
        return []
    text = package.read_text(encoding="utf-8", errors="ignore")
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return []
    deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
    corpus = "\n".join(s.text for s in sources if s.path.name != "package.json")
    findings = []
    for name in sorted(deps):
        if name not in DESIGN_PACKAGES and not name.startswith(DESIGN_PACKAGE_PREFIXES):
            continue
        if re.search(r"[\"'`(]" + re.escape(name) + r"(?:[/\"'`)])", corpus):
            continue
        line = text.count("\n", 0, text.find(f'"{name}"')) + 1
        findings.append({
            "kind": "unused-package",
            "confidence": "high",
            "subject": name,
            "evidence": f"package.json:{line}",
            "detail": "Installed, but nothing imports, requires, or @imports it.",
            "action": f"Uninstall {name}.",
        })
    return findings


def _hex6(value):
    value = value.lower().lstrip("#")
    if len(value) == 3:
        value = "".join(ch * 2 for ch in value)
    return "#" + value.upper() if len(value) == 6 else None


ROLE_HINTS = {
    "text": ("text", "ink", "fg", "foreground", "on-"),
    "background": ("bg", "background", "surface", "canvas", "paper", "fill"),
    "border": ("border", "rule", "line", "divider", "outline", "stroke"),
}


def _role(property_name):
    if property_name in ("color", "fill", "caret-color", "-webkit-text-fill-color"):
        return "text"
    if property_name.startswith("background"):
        return "background"
    if property_name.startswith(("border", "outline")):
        return "border"
    return None


def _pick_token(names, role):
    """Prefer a token whose name matches the property's role; None if only a mismatched role exists."""
    if not names:
        return None, None
    if role is None:
        return names[0], "high"
    for name in names:
        if any(hint in name for hint in ROLE_HINTS[role]):
            return name, "high"
    return names[0], "low"


def find_color_debt(sources):
    tokens = {}  # value -> token names anywhere (used to exclude token-owned colors)
    local_tokens = {}  # file -> value -> token names
    shared_tokens = {}  # value -> token names from standalone stylesheets, which pages share
    raw = {}
    raw_by_use = {}
    for source in sources:
        for offset, css in source.styles():
            clean = _strip_comments(css)
            for match in re.finditer(r"(--[A-Za-z0-9_-]+)\s*:\s*(#[0-9a-fA-F]{3}(?:[0-9a-fA-F]{3})?)\b\s*;", clean):
                value = _hex6(match.group(2))
                if not value:
                    continue
                name = match.group(1)
                for bucket in (tokens.setdefault(value, []), local_tokens.setdefault(source.rel, {}).setdefault(value, [])):
                    if name not in bucket:
                        bucket.append(name)
                if source.suffix in STYLE_SUFFIXES and name not in shared_tokens.setdefault(value, []):
                    shared_tokens[value].append(name)
            for match in re.finditer(r"(?<![-\w])([a-z-]+)\s*:\s*([^;{}]*)", clean):
                if match.group(1).startswith("--"):
                    continue
                for color in re.finditer(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b", match.group(2)):
                    value = _hex6(color.group(0))
                    if value:
                        site = source.cite(offset + match.start(2) + color.start())
                        raw.setdefault(value, []).append(site)
                        raw_by_use.setdefault((value, source.rel, _role(match.group(1))), []).append(site)
    findings = []
    for (value, rel, role), sites in sorted(raw_by_use.items(), key=lambda item: (item[0][0], item[0][1], item[0][2] or "")):
        names = local_tokens.get(rel, {}).get(value) or shared_tokens.get(value) or []
        token, confidence = _pick_token(names, role)
        if not token:
            continue
        role_note = "" if confidence == "high" else f" Its name does not match this {role} use, so check the role before swapping."
        findings.append({
            "kind": "hardcoded-token-color",
            "confidence": confidence,
            "subject": value,
            "evidence": sites[0],
            "detail": f"Hard-coded {len(sites)} time(s) as a {role or 'color'} value in this file although {token} holds the same value.{role_note}",
            "action": f"Replace {value} with var({token}).",
        })
    # Near-duplicates: only raw colors that no token owns, grouped into clusters,
    # because deliberate token steps (for example two near-blacks) are not debt.
    loose = sorted(value for value in raw if value not in tokens)
    rgb = {value: tuple(int(value[i:i + 2], 16) for i in (1, 3, 5)) for value in loose}
    parent = {value: value for value in loose}

    def find(value):
        while parent[value] != value:
            parent[value] = parent[parent[value]]
            value = parent[value]
        return value

    for index, first in enumerate(loose):
        for second in loose[index + 1:]:
            if max(abs(a - b) for a, b in zip(rgb[first], rgb[second])) <= 4:
                parent[find(second)] = find(first)
    clusters = {}
    for value in loose:
        clusters.setdefault(find(value), []).append(value)
    for members in clusters.values():
        if len(members) < 2:
            continue
        members.sort(key=lambda value: -len(raw[value]))
        keeper = members[0]
        findings.append({
            "kind": "near-duplicate-color",
            "confidence": "medium",
            "subject": " / ".join(members),
            "evidence": raw[members[1]][0],
            "detail": f"{len(members)} hard-coded colors differ by at most 4 per channel and read as one color.",
            "action": f"Keep {keeper} (used most), make it a token, and replace the others.",
        })
    return findings


# ------------------------------------------------------------------ report


def analyze(root, keep=()):
    root = Path(root).resolve()
    sources, assets = load_sources(root, keep)
    findings = (
        find_unused_packages(root, sources)
        + find_unused_fonts(root, sources)
        + find_unused_tokens(sources)
        + find_color_debt(sources)
        + find_unused_classes(sources)
        + find_unused_assets(root, sources, assets)
    )
    findings.sort(key=lambda f: (CONFIDENCE_ORDER[f["confidence"]], f["kind"], f["subject"]))
    for number, finding in enumerate(findings, 1):
        finding["number"] = number
    return findings


def save_report(root, findings):
    path = Path(root) / MEMORY_DIR / REPORT_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"date": date.today().isoformat(), "findings": findings}, indent=2) + "\n", encoding="utf-8")
    return path


def format_report(findings):
    if not findings:
        return "PRUNE: nothing unused found. The design code is lean."
    lines = [f"PRUNE: {len(findings)} candidate(s). Nothing was changed."]
    for finding in findings:
        lines.append(f"  {finding['number']:>3}. [{finding['kind']}] ({finding['confidence']}) {finding['subject']} at {finding['evidence']}")
        lines.append(f"       {finding['detail']} {finding['action']}")
    lines.append(
        "Approve findings by number. Remove only those, then run render_check.py before and after and compare the screenshots."
    )
    return "\n".join(lines)


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Report unused design code: tokens, classes, fonts, assets, packages, and color debt")
    parser.add_argument("--workspace", default=".", help="Project root (default: current directory)")
    parser.add_argument("--keep", action="append", default=[], metavar="GLOB", help="Treat matching files as public API (for example a shipped tokens.css); repeatable")
    parser.add_argument("--json", action="store_true", help="Print findings as JSON")
    args = parser.parse_args(argv)
    root = Path(args.workspace)
    if not root.is_dir():
        print(f"Error: workspace not found: {root}", file=sys.stderr)
        return 2
    findings = analyze(root, args.keep)
    save_report(root, findings)
    if args.json:
        print(json.dumps(findings, indent=2))
    else:
        print(format_report(findings))
        print(f"Saved {MEMORY_DIR}/{REPORT_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
