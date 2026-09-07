#!/usr/bin/env python3
"""Check BC catalog coverage against the alignment policy."""

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

from alignment import classify_entry


SKILL_ROOT = Path(__file__).resolve().parent.parent
DATA_ROOT = SKILL_ROOT / "data"
SUMMARY_PATH = DATA_ROOT / "catalog-summary.json"
OVERRIDES_PATH = DATA_ROOT / "alignment-overrides.json"
ROOT_CSVS = ("styles.csv", "colors.csv", "typography.csv", "ux-guidelines.csv", "charts.csv", "motion.csv")


def iter_catalogs():
    for filename in ROOT_CSVS:
        yield filename, DATA_ROOT / filename
    for path in sorted((DATA_ROOT / "stacks").glob("*.csv")):
        yield f"stacks/{path.name}", path


def build_report():
    policy = json.loads((DATA_ROOT / "bc-alignment-policy.json").read_text(encoding="utf-8"))
    overrides = json.loads(OVERRIDES_PATH.read_text(encoding="utf-8")) if OVERRIDES_PATH.exists() else {}
    allowed = set(policy["statuses"])
    totals = Counter()
    files = {}
    errors = []
    for relative, path in iter_catalogs():
        counts = Counter()
        with path.open(encoding="utf-8-sig", newline="") as handle:
            for number, row in enumerate(csv.DictReader(handle), 2):
                identity = row.get("Style ID") or row.get("No") or row.get("Product Type") or f"row-{number}"
                override = overrides.get(relative, {}).get(str(identity))
                if override:
                    status = override.get("status")
                    if status not in allowed or not override.get("reason"):
                        errors.append(f"{relative}:{number}: invalid override")
                else:
                    status = classify_entry(relative, row).status
                if status not in allowed:
                    errors.append(f"{relative}:{number}: unclassified={identity}")
                    status = "unclassified"
                counts[status] += 1
                totals[status] += 1
        files[relative] = dict(sorted(counts.items()))
    return {"schemaVersion": policy["schemaVersion"], "totals": dict(sorted(totals.items())), "files": files, "errors": errors}


def write_summary(report):
    summary = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
    summary["alignment"] = {"policyVersion": report["schemaVersion"], "totals": report["totals"], "files": report["files"]}
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Check BC catalog alignment coverage")
    parser.add_argument("--check", action="store_true", help="Exit nonzero on policy or coverage errors")
    parser.add_argument("--write-summary", action="store_true", help="Persist alignment totals in catalog-summary.json")
    args = parser.parse_args(argv)
    report = build_report()
    if args.write_summary:
        write_summary(report)
    totals = report["totals"]
    print("alignment=" + json.dumps(totals, sort_keys=True))
    print(f"unclassified={totals.get('unclassified', 0)}")
    if report["errors"]:
        for error in report["errors"]:
            print("ERROR: " + error)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
