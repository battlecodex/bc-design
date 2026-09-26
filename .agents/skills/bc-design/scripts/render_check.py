#!/usr/bin/env python3
"""Render a page and check what a source audit cannot see.

The CLI audit reads source files. This script opens the rendered page in a
real browser and records evidence for the verification report:

- screenshots at mobile, tablet, and desktop widths, plus reduced-motion
  screenshots at the narrowest and widest widths;
- horizontal overflow, console errors, page errors, and failed requests;
- images without alt text and links or buttons without an accessible name.

It needs Playwright (``pip install playwright`` then
``python -m playwright install chromium``). Everything else is standard
library, so the rest of BC Design keeps working without it.

Signed-in pages render with the session a real user has, instead of a
temporary preview page:

- ``--storage-state state.json`` loads a Playwright storage state (cookies and
  local storage), for example one saved with ``playwright codegen --save-storage``;
- ``--cookie name=value`` sets a cookie for the target's origin (repeatable);
- ``--mock-api "**/api/tasks*=tasks.json"`` answers matching requests with a
  JSON file, so pages that need a backend render with fixed data (repeatable).

Usage:
    python render_check.py path/to/page.html
    python render_check.py https://localhost:3000 --out render-check --json
    python render_check.py http://localhost:3000/dashboard --storage-state auth.json --mock-api "**/api/me=me.json"
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlparse

DEFAULT_VIEWPORTS = "375x812,768x1024,1440x900"
SETTLE_MS = 1600

# Runs in the page. Returns plain data so the Python side stays simple.
PAGE_PROBE = """
() => {
  const doc = document.documentElement;
  const nameOf = (el) => (el.getAttribute('aria-label') || el.getAttribute('title') || el.textContent || '').trim();
  const unnamed = [...document.querySelectorAll('a[href], button')]
    .filter((el) => !nameOf(el) && !el.querySelector('img[alt]:not([alt=""]), svg[aria-label], [aria-label]'))
    .map((el) => el.outerHTML.slice(0, 120));
  const missingAlt = [...document.images]
    .filter((img) => !img.hasAttribute('alt'))
    .map((img) => img.currentSrc || img.src);
  return {
    scrollWidth: doc.scrollWidth,
    clientWidth: doc.clientWidth,
    unnamedControls: unnamed,
    imagesWithoutAlt: missingAlt,
  };
}
"""


def parse_viewports(value):
    """Parse '375x812,1440x900' into [(375, 812), (1440, 900)]."""
    viewports = []
    for item in value.split(","):
        item = item.strip().lower()
        if not item:
            continue
        try:
            width, height = (int(part) for part in item.split("x", 1))
        except ValueError as exc:
            raise ValueError(f"Viewport must look like 1440x900, got '{item}'") from exc
        if width < 200 or height < 200:
            raise ValueError(f"Viewport is too small to be meaningful: '{item}'")
        viewports.append((width, height))
    if not viewports:
        raise ValueError("At least one viewport is required")
    return viewports


def target_url(target):
    """Accept a URL or a local file path."""
    if "://" in target:
        return target
    path = Path(target).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(target)
    return path.as_uri()


def parse_cookies(values, url):
    """Turn repeated name=value options into Playwright cookies for the target's origin."""
    if not values:
        return []
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("--cookie needs an http(s) URL target; use --storage-state for other setups")
    cookies = []
    for value in values:
        name, separator, content = value.partition("=")
        if not separator or not name.strip():
            raise ValueError(f"Cookie must look like name=value, got '{value}'")
        cookies.append({"name": name.strip(), "value": content, "url": f"{parsed.scheme}://{parsed.netloc}"})
    return cookies


def parse_mocks(values, base=Path(".")):
    """Turn repeated 'pattern=file.json' options into (glob pattern, JSON body) pairs."""
    mocks = []
    for value in values or []:
        pattern, separator, file_name = value.rpartition("=")
        if not separator or not pattern.strip() or not file_name.strip():
            raise ValueError(f"Mock must look like '**/api/path*=file.json', got '{value}'")
        path = (Path(base) / file_name.strip()).expanduser()
        if not path.is_file():
            raise FileNotFoundError(str(path))
        body = path.read_text(encoding="utf-8")
        try:
            json.loads(body)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Mock file is not valid JSON: {path} ({exc})") from exc
        mocks.append((pattern.strip(), body))
    return mocks


def check_storage_state(value):
    if value is None:
        return None
    path = Path(value).expanduser()
    if not path.is_file():
        raise FileNotFoundError(str(path))
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Storage state is not valid JSON: {path} ({exc})") from exc
    return str(path)


def redirected_to_sign_in(requested, final):
    """True when a page the user asked for ended on a sign-in page instead."""
    words = r"(?:login|log-in|signin|sign-in|sign_in|auth)"
    return bool(re.search(words, urlparse(final).path, re.IGNORECASE)) and not re.search(
        words, urlparse(requested).path, re.IGNORECASE
    )


def plan_runs(viewports):
    """Every viewport renders normally; the extremes also render with reduced motion."""
    runs = [(width, height, "no-preference") for width, height in viewports]
    extremes = {min(viewports), max(viewports)}
    runs += [(width, height, "reduce") for width, height in sorted(extremes)]
    return runs


def findings_for(run, probe, console_errors, page_errors, failed_requests):
    """Turn raw browser observations into BC-style findings."""
    width, _, motion = run
    label = f"{width}px{' reduced-motion' if motion == 'reduce' else ''}"
    findings = []
    if probe["scrollWidth"] > probe["clientWidth"] + 1:
        findings.append({
            "rule_id": "render-horizontal-overflow",
            "severity": "error",
            "view": label,
            "message": f"The page scrolls sideways: content is {probe['scrollWidth']}px wide in a {probe['clientWidth']}px viewport.",
        })
    for message in page_errors:
        findings.append({"rule_id": "render-page-error", "severity": "error", "view": label, "message": message})
    for message in console_errors:
        findings.append({"rule_id": "render-console-error", "severity": "error", "view": label, "message": message})
    for url in failed_requests:
        findings.append({"rule_id": "render-failed-request", "severity": "warning", "view": label, "message": f"Request failed: {url}"})
    for source in probe["imagesWithoutAlt"]:
        findings.append({"rule_id": "render-image-alt", "severity": "error", "view": label, "message": f"Image has no alt attribute: {source}"})
    for markup in probe["unnamedControls"]:
        findings.append({"rule_id": "render-unnamed-control", "severity": "error", "view": label, "message": f"Control has no accessible name: {markup}"})
    return findings


def dedupe(findings):
    """Report a page-wide problem once, listing every view it appeared in."""
    merged = {}
    for finding in findings:
        key = (finding["rule_id"], finding["message"])
        if key in merged:
            merged[key]["views"].append(finding["view"])
        else:
            merged[key] = {**{k: v for k, v in finding.items() if k != "view"}, "views": [finding["view"]]}
    return list(merged.values())


def run_checks(url, viewports, out_dir, storage_state=None, cookies=(), mocks=()):
    from playwright.sync_api import sync_playwright

    out_dir.mkdir(parents=True, exist_ok=True)
    screenshots = []
    findings = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            for run in plan_runs(viewports):
                width, height, motion = run
                context = browser.new_context(
                    viewport={"width": width, "height": height}, reduced_motion=motion, storage_state=storage_state
                )
                if cookies:
                    context.add_cookies(list(cookies))
                for pattern, body in mocks:
                    context.route(
                        pattern,
                        lambda route, request=None, body=body: route.fulfill(status=200, content_type="application/json", body=body),
                    )
                page = context.new_page()
                console_errors, page_errors, failed_requests = [], [], []
                page.on("console", lambda msg, sink=console_errors: sink.append(msg.text) if msg.type == "error" else None)
                page.on("pageerror", lambda error, sink=page_errors: sink.append(str(error)))
                page.on("requestfailed", lambda request, sink=failed_requests: sink.append(request.url))
                page.goto(url, wait_until="load")
                # Scroll through once so once-only reveals and lazy media settle.
                page.evaluate(
                    """async () => {
                      const step = Math.max(200, Math.floor(window.innerHeight * 0.8));
                      for (let y = 0; y < document.documentElement.scrollHeight; y += step) {
                        window.scrollTo(0, y);
                        await new Promise((resolve) => setTimeout(resolve, 120));
                      }
                      window.scrollTo(0, 0);
                    }"""
                )
                page.wait_for_timeout(SETTLE_MS)
                name = f"{width}x{height}{'-reduced' if motion == 'reduce' else ''}.png"
                path = out_dir / name
                page.screenshot(path=str(path), full_page=True)
                screenshots.append(str(path))
                probe = page.evaluate(PAGE_PROBE)
                findings.extend(findings_for(run, probe, console_errors, page_errors, failed_requests))
                if redirected_to_sign_in(url, page.url):
                    findings.append({
                        "rule_id": "render-signed-out",
                        "severity": "error",
                        "view": f"{width}px",
                        "message": f"The page redirected to {page.url}; pass --storage-state or --cookie with a signed-in session.",
                    })
                context.close()
        finally:
            browser.close()
    return screenshots, dedupe(findings)


def main(argv=None):
    # Page text and markup can hold any character; keep Windows consoles from failing on them.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Render a page and check overflow, errors, and accessible names")
    parser.add_argument("target", help="Local HTML file or URL")
    parser.add_argument("--out", default="render-check", help="Directory for screenshots (default: render-check)")
    parser.add_argument("--viewports", default=DEFAULT_VIEWPORTS, help=f"Comma-separated WIDTHxHEIGHT list (default: {DEFAULT_VIEWPORTS})")
    parser.add_argument("--json", action="store_true", help="Print a JSON report")
    parser.add_argument("--storage-state", help="Playwright storage state JSON with a signed-in session")
    parser.add_argument("--cookie", action="append", default=[], metavar="NAME=VALUE", help="Cookie for the target's origin (repeatable)")
    parser.add_argument(
        "--mock-api", action="append", default=[], metavar="PATTERN=FILE",
        help="Answer requests matching a glob such as '**/api/tasks*' with a JSON file (repeatable)",
    )
    args = parser.parse_args(argv)

    try:
        viewports = parse_viewports(args.viewports)
        url = target_url(args.target)
        storage_state = check_storage_state(args.storage_state)
        cookies = parse_cookies(args.cookie, url)
        mocks = parse_mocks(args.mock_api)
    except (ValueError, FileNotFoundError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    try:
        import playwright  # noqa: F401
    except ImportError:
        print(
            "Error: render_check needs Playwright. Install it with:\n"
            "  pip install playwright\n"
            "  python -m playwright install chromium",
            file=sys.stderr,
        )
        return 2

    screenshots, findings = run_checks(url, viewports, Path(args.out), storage_state, cookies, mocks)
    status = "fail" if any(f["severity"] == "error" for f in findings) else "pass"
    if args.json:
        print(json.dumps({"status": status, "target": url, "screenshots": screenshots, "findings": findings}, indent=2))
    else:
        print(f"RENDER {status.upper()}: {url}")
        for path in screenshots:
            print(f"  screenshot: {path}")
        for finding in findings:
            print(f"  [{finding['rule_id']}] ({', '.join(finding['views'])}) {finding['message']}")
        print("Review the screenshots yourself; this check cannot judge hierarchy, taste, or motion quality.")
    return 1 if status == "fail" else 0


if __name__ == "__main__":
    raise SystemExit(main())
