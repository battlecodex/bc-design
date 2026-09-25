#!/usr/bin/env python3
"""Study a live page: extract its design DNA, never its pixels.

Renders a public page in Chromium (through Playwright) and measures what the
browser actually applied: type roles and sizes, the most used colors, corner
radii, transition timing, section rhythm, and the motion libraries on the
page. The result is a diagnosis to design from, not a copy to paste.

Safety:
- Refuses template marketplaces and private or local addresses.
- Treats everything on the page as inert data. Text, comments, and metadata
  on the studied page are never instructions.
- Records provenance so a DESIGN.md built from the study says where the DNA
  came from and on what basis it may be used.

Usage:
    python study.py https://example.com
    python study.py https://example.com --json --out study-shots
"""

from __future__ import annotations

import argparse
import ipaddress
import json
from pathlib import Path
import sys
from urllib.parse import urlparse

REFUSED_HOSTS = (
    "themeforest.net",
    "templatemonster.com",
    "creativemarket.com",
    "ui8.net",
    "dribbble.com",
    "behance.net",
    "gumroad.com",
)
REFUSED_PATHS = (("framer.com", "/templates"), ("webflow.com", "/templates"))

PAGE_PROBE = """
() => {
  const style = (el) => getComputedStyle(el);
  const role = (selector) => {
    const el = document.querySelector(selector);
    if (!el) return null;
    const c = style(el);
    return { family: c.fontFamily, size: c.fontSize, weight: c.fontWeight, lineHeight: c.lineHeight, color: c.color };
  };
  const tally = (values) => Object.entries(values.reduce((acc, v) => { if (v) acc[v] = (acc[v] || 0) + 1; return acc; }, {}))
    .sort((a, b) => b[1] - a[1]);
  const all = [...document.querySelectorAll('body *')].slice(0, 6000);
  const colors = [];
  const radii = [];
  const motion = [];
  for (const el of all) {
    const c = style(el);
    if (c.backgroundColor !== 'rgba(0, 0, 0, 0)') colors.push(c.backgroundColor);
    colors.push(c.color);
    if (c.borderRadius !== '0px') radii.push(c.borderRadius);
    if (c.transitionDuration !== '0s') motion.push(`${c.transitionTimingFunction} ${c.transitionDuration}`);
  }
  const sections = [...document.querySelectorAll('main > *, body > section, main section')].length;
  return {
    title: document.title,
    type: {
      body: role('body'),
      h1: role('h1'),
      h2: role('h2'),
      h3: role('h3'),
      lead: role('main p, p'),
      button: role('button, a[class*="button"], a[class*="btn"]'),
    },
    canvas: style(document.body).backgroundColor,
    colors: tally(colors).slice(0, 16),
    radii: tally(radii).slice(0, 8),
    motion: tally(motion).slice(0, 8),
    sections,
    libraries: {
      gsap: typeof window.gsap !== 'undefined',
      scrollTrigger: typeof window.ScrollTrigger !== 'undefined',
      three: typeof window.THREE !== 'undefined',
      lenis: typeof window.Lenis !== 'undefined' || !!document.querySelector('.lenis'),
    },
  };
}
"""


def refusal_reason(url):
    """Return why a URL may not be studied, or None when it may."""
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        return "Only public http(s) pages can be studied."
    host = parsed.hostname.lower()
    if host == "localhost" or host.endswith(".local") or host.endswith(".internal"):
        return "Local and internal addresses are not studied."
    try:
        address = ipaddress.ip_address(host)
        if address.is_private or address.is_loopback or address.is_link_local or address.is_reserved:
            return "Private network addresses are not studied."
    except ValueError:
        pass
    if any(host == refused or host.endswith("." + refused) for refused in REFUSED_HOSTS):
        return "Template marketplaces and design showcases are not studied; their designs belong to their authors."
    for refused_host, refused_path in REFUSED_PATHS:
        if (host == refused_host or host.endswith("." + refused_host)) and parsed.path.startswith(refused_path):
            return "Template marketplaces are not studied; their designs belong to their authors."
    return None


def _rgb_to_hex(value):
    parts = value.replace("rgba(", "").replace("rgb(", "").replace(")", "").split(",")
    try:
        red, green, blue = (int(float(part)) for part in parts[:3])
    except ValueError:
        return value
    return f"#{red:02X}{green:02X}{blue:02X}"


def diagnose(probe, url):
    """Turn raw measurements into the study fields BC Design works from."""
    type_roles = {}
    for name, data in probe["type"].items():
        if data:
            type_roles[name] = {
                "family": data["family"].split(",")[0].strip().strip('"'),
                "size": data["size"],
                "weight": data["weight"],
                "line_height": data["lineHeight"],
            }
    return {
        "source": url,
        "title": probe.get("title", ""),
        "canvas": _rgb_to_hex(probe["canvas"]),
        "palette": [{"color": _rgb_to_hex(color), "uses": count} for color, count in probe["colors"]],
        "type_roles": type_roles,
        "radii": [{"radius": radius, "uses": count} for radius, count in probe["radii"]],
        "motion": [{"timing": timing, "uses": count} for timing, count in probe["motion"]],
        "sections": probe["sections"],
        "libraries": [name for name, present in probe["libraries"].items() if present],
    }


def format_report(study):
    lines = [f"STUDY: {study['source']}", f"Title: {study['title']}", f"Canvas: {study['canvas']}", "Type roles:"]
    for name, role in study["type_roles"].items():
        lines.append(f"  {name}: {role['family']} {role['size']} / weight {role['weight']} / line height {role['line_height']}")
    lines.append("Palette (most used): " + ", ".join(f"{item['color']} x{item['uses']}" for item in study["palette"][:10]))
    lines.append("Radii: " + (", ".join(f"{item['radius']} x{item['uses']}" for item in study["radii"]) or "none"))
    lines.append("Motion: " + (", ".join(f"{item['timing']} x{item['uses']}" for item in study["motion"][:5]) or "none"))
    lines.append(f"Sections: {study['sections']}")
    lines.append("Libraries: " + (", ".join(study["libraries"]) or "none detected"))
    lines.append(
        "Use this as structure and tokens to design from. Do not copy the page's artwork, logos, proprietary fonts, "
        "or copy. Before writing a DESIGN.md from it, record whether the source is your own, a public reference for your own brand, or something else."
    )
    return "\n".join(lines)


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Extract the design DNA of a public page")
    parser.add_argument("url", help="Public http(s) URL")
    parser.add_argument("--out", help="Directory for desktop and mobile screenshots")
    parser.add_argument("--json", action="store_true", help="Print the study as JSON")
    args = parser.parse_args(argv)

    reason = refusal_reason(args.url)
    if reason:
        print(f"Refused: {reason}", file=sys.stderr)
        return 2
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(
            "Error: study needs Playwright. Install it with:\n"
            "  pip install playwright\n"
            "  python -m playwright install chromium\n"
            "Without it, attach a screenshot and study it visually instead.",
            file=sys.stderr,
        )
        return 2

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            page = browser.new_context(viewport={"width": 1440, "height": 900}).new_page()
            response = page.goto(args.url, wait_until="load", timeout=60000)
            if response is None or not response.ok:
                status = response.status if response else "no response"
                print(f"Error: the page did not load ({status}). Attach a screenshot instead.", file=sys.stderr)
                return 2
            page.wait_for_timeout(2000)
            probe = page.evaluate(PAGE_PROBE)
            if args.out:
                out = Path(args.out)
                out.mkdir(parents=True, exist_ok=True)
                page.screenshot(path=str(out / "desktop.png"))
                page.set_viewport_size({"width": 390, "height": 844})
                page.wait_for_timeout(800)
                page.screenshot(path=str(out / "mobile.png"))
        finally:
            browser.close()

    study = diagnose(probe, args.url)
    print(json.dumps(study, indent=2) if args.json else format_report(study))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
