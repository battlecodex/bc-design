"""Structured audit interfaces for BC Design quality gates.

The compatibility CLI owns the rule implementation. This module normalizes its
legacy tuples into stable machine-readable findings for integrations and CI.
"""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path


SEVERITY = {
    "excessive-pill-capsules": "warning",
    "generic-gradient-wash": "warning",
    "accent-surface-domination": "warning",
    "decorative-eyebrow-overload": "warning",
    "oversized-hero-displacement": "warning",
    "copied-platform-chrome": "warning",
    "repeated-generic-cta": "warning",
    "focus-ring-width": "error",
    "accent-button-text-contrast": "error",
    "sticky-z-index-token": "warning",
    "streaming-layout-animation": "error",
    "motion-duration-budget": "warning",
    "motion-easing-token": "warning",
    "reduced-motion-support": "error",
    "spatial-uncapped-pixel-ratio": "warning",
    "em-dash-copy": "warning",
    "buzzword-copy": "warning",
    "unverified-claim": "error",
    "dead-navigation-link": "warning",
    "focus-outline-removed": "error",
    "gsap-reduced-motion": "error",
    "gsap-layout-property": "warning",
}

CATEGORY = {
    "monotonous-card-kit": "hierarchy",
    "decorative-index-marker": "hierarchy",
    "excessive-pill-capsules": "decoration",
    "generic-gradient-wash": "identity",
    "accent-surface-domination": "identity",
    "unicode-icon-glyph": "identity",
    "decorative-eyebrow-overload": "hierarchy",
    "oversized-hero-displacement": "hierarchy",
    "copied-platform-chrome": "identity",
    "repeated-generic-cta": "copy",
    "template-arrow-cta": "copy",
    "middle-dot-metadata": "copy",
    "template-arrow-glyph": "copy",
    "motion-duration-budget": "motion",
    "motion-easing-token": "motion",
    "streaming-layout-animation": "motion",
    "reduced-motion-support": "accessibility",
    "focus-ring-width": "accessibility",
    "accent-button-text-contrast": "accessibility",
    "sticky-z-index-token": "accessibility",
    "spatial-uncapped-pixel-ratio": "performance",
    "em-dash-copy": "copy",
    "buzzword-copy": "copy",
    "unverified-claim": "content",
    "dead-navigation-link": "content",
    "focus-outline-removed": "accessibility",
    "gsap-reduced-motion": "accessibility",
    "gsap-layout-property": "performance",
}

# Every rule reports under one of the review dimensions in
# references/design-dimensions.md.
DIMENSIONS = (
    "Color",
    "Typography",
    "Layout & grid",
    "Spacing & whitespace",
    "Visual hierarchy",
    "Imagery & icons",
    "Shape & effects",
    "UI components",
    "Interaction & states",
    "Motion",
    "Responsiveness",
    "Accessibility",
    "Information architecture",
    "UX writing",
)
DIMENSION = {
    "monotonous-card-kit": "Visual hierarchy",
    "decorative-index-marker": "Visual hierarchy",
    "decorative-eyebrow-overload": "Visual hierarchy",
    "oversized-hero-displacement": "Typography",
    "excessive-pill-capsules": "Shape & effects",
    "generic-gradient-wash": "Color",
    "accent-surface-domination": "Color",
    "accent-button-text-contrast": "Accessibility",
    "unicode-icon-glyph": "Imagery & icons",
    "template-arrow-glyph": "Imagery & icons",
    "copied-platform-chrome": "Information architecture",
    "dead-navigation-link": "Information architecture",
    "repeated-generic-cta": "UX writing",
    "template-arrow-cta": "UX writing",
    "middle-dot-metadata": "UX writing",
    "em-dash-copy": "UX writing",
    "buzzword-copy": "UX writing",
    "unverified-claim": "UX writing",
    "focus-ring-width": "Accessibility",
    "focus-outline-removed": "Accessibility",
    "sticky-z-index-token": "Layout & grid",
    "streaming-layout-animation": "Motion",
    "motion-duration-budget": "Motion",
    "motion-easing-token": "Motion",
    "reduced-motion-support": "Motion",
    "gsap-reduced-motion": "Motion",
    "gsap-layout-property": "Motion",
    "spatial-uncapped-pixel-ratio": "Responsiveness",
}

RECOMMENDATIONS = {
    "excessive-pill-capsules": "Use full pills only for tags, filters, and compact statuses; vary controls and surfaces.",
    "generic-gradient-wash": "Replace the saturated gradient with subject-grounded color or an earned signature visual.",
    "accent-surface-domination": "Keep the canvas neutral and reserve the accent for hierarchy, actions, or status.",
    "decorative-eyebrow-overload": "Reduce repeated all-caps eyebrow labels and use meaningful headings.",
    "oversized-hero-displacement": "Scale hero type so useful product content remains visible in the first viewport.",
    "copied-platform-chrome": "Remove copied platform labels unless they belong to the product's own information architecture.",
    "repeated-generic-cta": "Use specific action labels that describe the user's next step.",
    "monotonous-card-kit": "Vary hierarchy with open space, dividers, lists, or an anchored panel.",
    "template-arrow-cta": "Let the action label carry the meaning and remove the decorative suffix.",
    "middle-dot-metadata": "Use labels, line breaks, or meaningful punctuation for metadata.",
    "template-arrow-glyph": "Use an accessible action label and a purposeful icon only when it adds information.",
    "unicode-icon-glyph": "Replace the glyph with a 1.5px monoline SVG and an accessible name.",
    "decorative-index-marker": "Remove the marker or make the sequence meaningful and ordered.",
    "focus-ring-width": "Use a visible 2px focus ring with sufficient contrast.",
    "accent-button-text-contrast": "Avoid dark ink text on mid-tone accent/terracotta buttons. Use crisp white (#FFFFFF) text or switch primary actions to the canonical high-contrast button (.bc-btn-contrast).",
    "sticky-z-index-token": "Use the semantic sticky-navigation layer token (30).",
    "streaming-layout-animation": "Animate opacity/transform only while streamed content is changing.",
    "motion-duration-budget": "Use a BC duration token; reserve longer timing for a documented state.",
    "motion-easing-token": "Use a BC easing token or the approved deceleration curve.",
    "reduced-motion-support": "Add a prefers-reduced-motion: reduce fallback in the same source unit.",
    "spatial-uncapped-pixel-ratio": "Cap WebGL pixel ratio with Math.min(window.devicePixelRatio, 2) to protect mobile GPU thermal budget.",
    "em-dash-copy": "Rewrite the sentence with a period, comma, colon, or parentheses.",
    "buzzword-copy": "State what the product does for this reader in concrete terms.",
    "unverified-claim": "Cite the certificate or measurement, or remove the claim.",
    "dead-navigation-link": "Link to a real destination or render the item as plain text.",
    "focus-outline-removed": "Add a :focus-visible rule with a 2px accent outline or equivalent ring.",
    "gsap-reduced-motion": "Use gsap.matchMedia() with a (prefers-reduced-motion: reduce) branch that sets final states without tweening.",
    "gsap-layout-property": "Replace width/height/top/left/margin/padding tweens with x, y, scale, clipPath, or opacity.",
}

EVIDENCE_MARKERS = {
    "excessive-pill-capsules": ("999", "rounded-full"),
    "generic-gradient-wash": ("gradient", "7c3aed", "2563eb"),
    "accent-surface-domination": ("background", "d97757", "e28466"),
    "decorative-eyebrow-overload": ("EXPLORE PLATFORM",),
    "oversized-hero-displacement": ("font-size", "text-9xl"),
    "copied-platform-chrome": ("new task", "projects", "settings"),
    "repeated-generic-cta": ("get started", "learn more", "explore now", "sign up", "submit"),
    "monotonous-card-kit": ("rounded-xl", "p-6"),
    "template-arrow-cta": ("→",),
    "middle-dot-metadata": ("·",),
    "template-arrow-glyph": ("↗", "↘", "→", "←", "↑", "↓"),
    "unicode-icon-glyph": ("aria-hidden", "⌖", "★", "✦"),
    "decorative-index-marker": ("01", "02", "03"),
    "focus-ring-width": ("focus-visible", "outline"),
    "accent-button-text-contrast": ("text-on-accent", "1f1e1b", "181816", "d97757", "e28466"),
    "sticky-z-index-token": ("sticky", "z-index"),
    "streaming-layout-animation": ("transition", "animation", "stream"),
    "motion-duration-budget": ("transition", "animation"),
    "motion-easing-token": ("transition", "animation", "ease"),
    "reduced-motion-support": ("transition", "animation", "keyframes"),
    "spatial-uncapped-pixel-ratio": ("setpixelratio",),
    "em-dash-copy": ("\u2014",),
    "buzzword-copy": ("seamless", "unlock", "elevate", "empower", "unleash", "supercharge", "revolution", "cutting-edge", "cutting edge", "next-generation", "next generation", "ai-powered", "ai powered", "effortless", "game-changer"),
    "unverified-claim": ("soc 2", "soc2", "iso 27001", "hipaa", "gdpr", "pci", "uptime", "x faster"),
    "dead-navigation-link": ('href="#"', "href='#'"),
    "focus-outline-removed": ("outline: none", "outline:none", "outline: 0", "outline:0"),
    "gsap-reduced-motion": ("gsap.",),
    "gsap-layout-property": ("gsap.to", "gsap.from"),
}


def _legacy():
    path = Path(__file__).with_name("bc_design.py")
    spec = importlib.util.spec_from_file_location("bc_design_audit_compat", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def audit_target(target):
    """Return legacy ``(rule_id, message, source_path)`` tuples for compatibility."""
    return _legacy().audit_target(target)


def _line_for_rule(content, rule_id, message):
    markers = EVIDENCE_MARKERS.get(rule_id, ())
    lines = content.splitlines()
    for number, line in enumerate(lines, 1):
        lowered = line.lower()
        if rule_id == "motion-duration-budget" and re.search(r"(?:\d+\.?\d*|\.\d+)(?:ms|s)\b", lowered) and re.search(r"(?:transition|animation)", lowered):
            if re.search(r"(?:[5-9]\d{2}|\d{4,})ms\b|(?:\.5|[1-9]\d*)s\b", lowered):
                return number
        if rule_id == "motion-easing-token" and re.search(r"(?:transition|animation).*\b(?:linear|ease(?:-in|-out|-in-out)?)\b", lowered):
            return number
        if markers and any(marker.lower() in lowered for marker in markers):
            return number
        if message.lower() in lowered:
            return number
    return 1


def build_audit_findings(target):
    """Return stable finding dictionaries with evidence and remediation guidance."""
    target_path = Path(target)
    findings = []
    for rule_id, message, source in audit_target(target_path):
        source_path = Path(source)
        try:
            content = source_path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            content = ""
        line = _line_for_rule(content, rule_id, message)
        lines = content.splitlines()
        evidence = lines[line - 1].strip() if lines and line <= len(lines) else ""
        findings.append(
            {
                "rule_id": rule_id,
                "severity": SEVERITY.get(rule_id, "warning"),
                "category": CATEGORY.get(rule_id, "identity"),
                "dimension": DIMENSION.get(rule_id, "Visual hierarchy"),
                "path": str(source_path),
                "line": line,
                "evidence": evidence,
                "message": message,
                "recommendation": RECOMMENDATIONS.get(rule_id, message),
                "confidence": "high",
            }
        )
    return findings


def summarize_by_dimension(findings):
    """Count findings per review dimension, in scorecard order."""
    counts = {}
    for dimension in DIMENSIONS:
        total = sum(1 for finding in findings if finding.get("dimension") == dimension)
        if total:
            counts[dimension] = total
    return counts
