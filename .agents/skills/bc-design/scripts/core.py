"""Shared catalog configuration and zero-dependency BM25 search engine."""

from __future__ import annotations

import csv
import re
from collections import defaultdict
from alignment import classify_entry, explicit_direction_requested, query_conflicts_with_quality_gate
from math import log
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
DATA_DIR = SKILL_ROOT / "data"

CSV_CONFIG = {
    "style": {"file": "styles.csv", "search_cols": ["Style ID", "Style Category", "Aliases", "Keywords", "Best For", "Type"], "output_cols": ["Style Category", "Keywords", "Primary Colors", "Effects & Animation", "Best For", "Light Mode ✓", "Dark Mode ✓", "Implementation Checklist"]},
    "color": {"file": "colors.csv", "search_cols": ["Product Type", "Notes"], "output_cols": ["Product Type", "Primary", "Secondary", "Accent", "Background", "Foreground", "Card", "Border", "Notes"]},
    "chart": {"file": "charts.csv", "search_cols": ["Data Type", "Keywords", "Best Chart Type", "Secondary Options", "When to Use"], "output_cols": ["Data Type", "Best Chart Type", "When to Use", "When NOT to Use", "Color Guidance", "Accessibility Grade", "Library Recommendation"]},
    "landing": {"file": "landing.csv", "search_cols": ["Pattern ID", "Pattern Name", "Keywords", "Conversion Optimization"], "output_cols": ["Pattern Name", "Keywords", "Section Order", "Primary CTA Placement", "Color Strategy", "Conversion Optimization"]},
    "product": {"file": "products.csv", "search_cols": ["Product Type", "Keywords", "Primary Style Recommendation"], "output_cols": ["Product Type", "Keywords", "Primary Style Recommendation", "Secondary Styles", "Landing Page Pattern", "Color Palette Focus"]},
    "ux": {"file": "ux-guidelines.csv", "search_cols": ["Category", "Issue", "Description"], "output_cols": ["Category", "Issue", "Description", "Do", "Don't", "Severity"]},
    "typography": {"file": "typography.csv", "search_cols": ["Font Pairing Name", "Category", "Mood/Style Keywords", "Best For", "Heading Font", "Body Font"], "output_cols": ["Font Pairing Name", "Heading Font", "Body Font", "Mood/Style Keywords", "Best For", "Google Fonts URL", "Tailwind Config"]},
    "motion": {"file": "motion.csv", "search_cols": ["Category", "Intensity Tier", "Keywords", "Trigger", "Do", "Don't"], "output_cols": ["Category", "Intensity Tier", "Trigger", "Duration", "Easing", "Do", "Don't", "Performance Notes"]},
    "icons": {"file": "icons.csv", "search_cols": ["Category", "Icon Name", "Keywords", "Usage", "Best For", "Semantic Role", "Allowed Contexts"], "output_cols": ["Category", "Icon Name", "Library", "Import Code", "Usage", "Best For", "Semantic Role", "Allowed Contexts"]},
    "google-fonts": {"file": "google-fonts.csv", "search_cols": ["Family", "Category", "Classifications", "Keywords", "Styles", "Subsets"], "output_cols": ["Family", "Category", "Classifications", "Styles", "Variable Axes", "Google Fonts URL"]},
    "spatial": {"file": "spatial-effects.csv", "search_cols": ["Effect ID", "Effect Name", "Category", "Keywords", "Runtime", "Best For", "Description"], "output_cols": ["Effect Name", "Category", "Runtime", "Light Mode", "Dark Mode", "Best For", "Description", "CLI Command"]},
}

# Friendly names used in documentation can resolve to canonical catalog stems.
STACK_ALIASES = {"tailwind": "html-tailwind"}


def _token_in_text(token, text):
    """Match a query token as a complete term for semantic boosts."""
    return bool(re.search(r"(?<![\w-])" + re.escape(token) + r"(?![\w-])", text))


def stack_catalog_names():
    """Return every stack catalog shipped with BC Design."""
    return sorted(path.stem for path in (DATA_DIR / "stacks").glob("*.csv"))


def resolve_stack_name(stack):
    """Resolve a documented friendly stack name to its catalog stem."""
    return STACK_ALIASES.get(stack, stack)


class SimpleBM25:
    """Small BM25 scorer suitable for the bundled local CSV catalogs."""

    def __init__(self, corpus, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.corpus = corpus
        self.doc_len = [len(doc) for doc in corpus]
        self.avg_doc_len = sum(self.doc_len) / (len(corpus) or 1)
        self.df = defaultdict(int)
        for doc in corpus:
            for term in set(doc):
                self.df[term] += 1
        self.N = len(corpus)

    def score(self, query):
        q_tokens = [word.lower() for word in re.findall(r"\w+", query)]
        scores = [0.0] * self.N
        for term in q_tokens:
            if term not in self.df:
                continue
            df = self.df[term]
            idf = log((self.N - df + 0.5) / (df + 0.5) + 1.0)
            for index, doc in enumerate(self.corpus):
                tf = doc.count(term)
                numerator = tf * (self.k1 + 1)
                denominator = tf + self.k1 * (1 - self.b + self.b * (self.doc_len[index] / (self.avg_doc_len or 1)))
                scores[index] += idf * (numerator / (denominator or 1))
        return scores


def search_domain(domain, query, max_results=3, selection_mode="automatic"):
    """Search one bundled CSV domain with BC-aware BM25 ranking."""
    if domain not in CSV_CONFIG:
        return {"error": f"Unknown domain: {domain}"}
    if selection_mode not in {"automatic", "explicit"}:
        return {"error": "selection_mode must be 'automatic' or 'explicit'"}
    if query_conflicts_with_quality_gate(query):
        return {"domain": domain, "query": query, "count": 0, "results": [], "blocked": "Request conflicts with a BC quality gate."}
    config = CSV_CONFIG[domain]
    csv_path = DATA_DIR / config["file"]
    if not csv_path.exists():
        return {"error": f"Database file not found: {csv_path}"}

    rows = []
    corpus = []
    with csv_path.open("r", encoding="utf-8", errors="ignore", newline="") as handle:
        for row in csv.DictReader(handle):
            rows.append(row)
            tokens = []
            for column in config["search_cols"]:
                tokens.extend(re.findall(r"\w+", row.get(column, "").lower()))
            corpus.append(tokens)

    scores = SimpleBM25(corpus).score(query)
    query_tokens = set(re.findall(r"\w+", query.lower()))
    ranked = []
    for index, score in enumerate(scores):
        if score <= 0.05:
            continue
        if domain == "product":
            # Product grounding benefits from a small exact-semantic boost:
            # a query term in the product type or its canonical keywords is
            # stronger evidence than a coincidental hit in a style label.
            product_type = rows[index].get("Product Type", "").lower()
            product_keywords = rows[index].get("Keywords", "").lower()
            type_hits = sum(1 for token in query_tokens if _token_in_text(token, product_type))
            keyword_hits = sum(1 for token in query_tokens if _token_in_text(token, product_keywords))
            score += (1.5 * type_hits) + (0.75 * keyword_hits)
        alignment = classify_entry(domain, rows[index], explicit=selection_mode == "explicit")
        if alignment.status == "excluded":
            continue
        # Product rows provide subject/context grounding even when their
        # recommended visual style is conditional (for example, an
        # Educational App row that mentions Claymorphism).  Keep those rows
        # discoverable so the generator can choose a BC-safe style while
        # preserving the product match.  Visual-direction domains still hide
        # conditional entries during automatic selection.
        conditional_visual_domains = {"style", "color", "typography", "landing", "motion", "icons"}
        if alignment.status == "conditional" and selection_mode == "automatic" and domain in conditional_visual_domains:
            continue
        multiplier = {"core": 1.25, "compatible": 1.0, "conditional": 0.85}[alignment.status]
        ranked.append((score * multiplier, index, alignment))
    ranked.sort(key=lambda item: item[0], reverse=True)
    results = []
    for _, index, alignment in ranked[:max_results]:
        row = rows[index]
        item = {column: row.get(column, "") for column in config["output_cols"] if column in row}
        item["alignment"] = {
            "status": alignment.status,
            "score": round(alignment.score, 3),
            "matched_traits": list(alignment.matched_traits),
            "conflicts": list(alignment.conflicts),
            "reason": alignment.reason,
        }
        results.append(item)
    return {"domain": domain, "query": query, "count": len(results), "results": results}


def search_stack(stack, query=None, max_results=10):
    """Search a stack catalog, regardless of whether a focused Markdown guide exists."""
    canonical_stack = resolve_stack_name(stack)
    if canonical_stack not in stack_catalog_names():
        return {"error": f"Unknown stack: {stack}. Available: {', '.join(stack_catalog_names())}"}
    path = DATA_DIR / "stacks" / f"{canonical_stack}.csv"
    with path.open("r", encoding="utf-8-sig", errors="ignore", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if query:
        terms = set(re.findall(r"\w+", query.lower()))
        rows.sort(key=lambda row: sum(str(value).lower().count(term) for value in terms for value in row.values()), reverse=True)
    return {
        "stack": stack,
        "catalog": canonical_stack,
        "query": query,
        "count": min(len(rows), max_results),
        "results": [{"stack": stack, "guidance": row} for row in rows[:max_results]],
    }
