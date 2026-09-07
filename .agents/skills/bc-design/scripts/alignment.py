"""BC Design compatibility classification for broad catalog entries."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re


POLICY_PATH = Path(__file__).resolve().parent.parent / "data" / "bc-alignment-policy.json"
POLICY = json.loads(POLICY_PATH.read_text(encoding="utf-8"))


@dataclass(frozen=True)
class AlignmentResult:
    status: str
    score: float
    matched_traits: tuple[str, ...]
    conflicts: tuple[str, ...]
    reason: str


def _text(row: dict) -> str:
    return " ".join(str(value) for value in row.values() if value is not None).lower()


def _has(text: str, trait: str) -> bool:
    return bool(re.search(r"(?<![\w-])" + re.escape(trait.lower()) + r"(?![\w-])", text))


def explicit_direction_requested(query: str, row: dict) -> bool:
    """Return true when a query deliberately requests this row's visual direction."""
    query_text = query.lower()
    row_text = _text(row)
    row_terms = [trait for trait in POLICY["conditionalTraits"] if _has(row_text, trait)]
    if not row_terms:
        return False
    return any(_has(query_text, signal.strip()) for signal in POLICY["explicitRequestSignals"]) and any(
        _has(query_text, term) for term in row_terms
    )


def requested_selection_mode(query: str) -> str:
    """Choose explicit mode only when the query names a conditional direction."""
    query_text = query.lower()
    return "explicit" if any(_has(query_text, term) for term in POLICY["conditionalTraits"]) else "automatic"


def query_conflicts_with_quality_gate(query: str) -> bool:
    """Return true when a request itself names an unsafe quality condition."""
    query_text = query.lower()
    return any(_has(query_text, trait) for trait in POLICY["conflictTraits"])


def classify_entry(domain: str, row: dict, explicit: bool = False) -> AlignmentResult:
    """Classify one catalog row without changing the source catalog."""
    text = _text(row)
    matched = tuple(trait for trait in POLICY["coreTraits"] if _has(text, trait))
    conditional = tuple(trait for trait in POLICY["conditionalTraits"] if _has(text, trait))
    conflicts = tuple(trait for trait in POLICY["conflictTraits"] if _has(text, trait))

    # Saturated combinations are not made safe merely by asking for them.
    if ("neon" in text and ("glassmorphism" in text or "gradient" in text)) or conflicts:
        return AlignmentResult(
            "excluded", 0.0, matched, conflicts or ("high-risk combination",),
            f"{domain} entry conflicts with a BC quality gate.",
        )
    if conditional:
        reason = "Explicit direction requested." if explicit else "Requires explicit direction or brand evidence."
        return AlignmentResult("conditional", 0.35, matched, conditional, reason)
    if matched:
        score = min(0.95, 0.55 + (0.08 * len(matched)))
        return AlignmentResult("core", score, matched, (), f"Matches {len(matched)} BC visual traits.")
    return AlignmentResult(
        "compatible", 0.5, (), (),
        "No direct conflict; use semantic tokens and verify the BC quality gates.",
    )
