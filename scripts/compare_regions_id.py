#!/usr/bin/env python3
"""
Compare flattened regions_id datasets using village-level semantics.

Rationale:
- regions_id is a denormalized view
- village is the canonical entity
- therefore, comparison MUST be village-equivalent

Only village-owned fields are compared.
"""

import csv
import argparse
from pathlib import Path

# =========================
# CONFIG
# =========================

KEY_FIELD = "village_code"

# Fields that truly belong to village entity
VILLAGE_FIELDS = {
    "village_name",
    "village_type",
    "district_code",
}

# =========================
# IO UTILITIES
# =========================

def load_csv(path, key):
    """
    Load CSV into dict[key] = row
    Rows without key are ignored safely.
    """
    rows = {}
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            k = row.get(key)
            if not k:
                continue
            rows[k] = row
    return rows


def write_csv(path, fieldnames, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

# =========================
# CORE LOGIC
# =========================

def compare(old_file, new_file, output_prefix):
    old_rows = load_csv(old_file, KEY_FIELD)
    new_rows = load_csv(new_file, KEY_FIELD)

    all_keys = set(old_rows) | set(new_rows)

    diffs = []
    summary = {
        "total_villages": len(all_keys),
        "added": 0,
        "removed": 0,
        "changed": 0,
    }

    for code in sorted(all_keys):
        old = old_rows.get(code)
        new = new_rows.get(code)

        if not old:
            summary["added"] += 1
            continue

        if not new:
            summary["removed"] += 1
            continue

        changed = False
        for field in VILLAGE_FIELDS:
            old_val = old.get(field)
            new_val = new.get(field)
            if old_val != new_val:
                diffs.append({
                    "village_code": code,
                    "field": field,
                    "old": old_val,
                    "new": new_val,
                })
                changed = True

        if changed:
            summary["changed"] += 1

    return diffs, summary

# =========================
# CLI
# =========================

def main():
    parser = argparse.ArgumentParser(
        description="Compare regions_id.csv using village-level treatment"
    )
    parser.add_argument("old", help="Old regions_id.csv")
    parser.add_argument("new", help="New regions_id.csv")
    parser.add_argument(
        "-o",
        "--output",
        default="regions_id_diff",
        help="Output prefix (default: regions_id_diff)",
    )

    args = parser.parse_args()

    diffs, summary = compare(args.old, args.new, args.output)

    out_prefix = Path(args.output)

    # Write field-level diff
    write_csv(
        out_prefix.with_name(out_prefix.name + "_field_diff.csv"),
        ["village_code", "field", "old", "new"],
        diffs,
    )

    # Write summary
    write_csv(
        out_prefix.with_name(out_prefix.name + "_summary.csv"),
        ["metric", "value"],
        [{"metric": k, "value": v} for k, v in summary.items()],
    )

    print("=== regions_id comparison completed ===")
    for k, v in summary.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()
