#!/usr/bin/env python3
import csv
import argparse
from pathlib import Path
from collections import Counter


def load_csv(path, key="code"):
    rows = {}
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows[row[key]] = row
    return rows, reader.fieldnames


def compare(old_file, new_file, output_file):
    old_rows, old_fields = load_csv(old_file)
    new_rows, new_fields = load_csv(new_file)

    # fields to compare (exclude code)
    compare_fields = [f for f in old_fields if f != "code"]

    all_codes = sorted(set(old_rows) | set(new_rows))
    diffs = []
    stats = Counter()

    for code in all_codes:
        old = old_rows.get(code)
        new = new_rows.get(code)

        if old and not new:
            stats["ONLY_IN_OLD"] += 1
            diffs.append({
                "code": code,
                "status": "ONLY_IN_OLD",
                **{f"old_{f}": old.get(f, "") for f in compare_fields},
                **{f"new_{f}": "" for f in compare_fields},
            })
            continue

        if new and not old:
            stats["ONLY_IN_NEW"] += 1
            diffs.append({
                "code": code,
                "status": "ONLY_IN_NEW",
                **{f"old_{f}": "" for f in compare_fields},
                **{f"new_{f}": new.get(f, "") for f in compare_fields},
            })
            continue

        changed = []
        for f in compare_fields:
            if old.get(f) != new.get(f):
                changed.append(f)

        if not changed:
            stats["UNCHANGED"] += 1
            continue

        if len(changed) == 1:
            status = f"CHANGED_{changed[0].upper()}"
        else:
            status = "MULTIPLE_CHANGED"

        stats[status] += 1

        diffs.append({
            "code": code,
            "status": status,
            **{f"old_{f}": old.get(f, "") for f in compare_fields},
            **{f"new_{f}": new.get(f, "") for f in compare_fields},
        })

    # write diff csv
    output_file = Path(output_file)
    with output_file.open("w", newline="", encoding="utf-8") as f:
        fieldnames = (
            ["code", "status"]
            + [f"old_{f}" for f in compare_fields]
            + [f"new_{f}" for f in compare_fields]
        )
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(diffs)

    return stats, output_file


def main():
    parser = argparse.ArgumentParser(
        description="Compare region CSV files (district / village)"
    )
    parser.add_argument("old", help="Old CSV file")
    parser.add_argument("new", help="New CSV file")
    parser.add_argument("-o", "--output", default="diff.csv", help="Output diff CSV")

    args = parser.parse_args()

    stats, out = compare(args.old, args.new, args.output)

    print("\n=== COMPARISON SUMMARY ===")
    for k, v in stats.items():
        print(f"{k:20} : {v}")
    print(f"\nDiff file written to: {out.resolve()}")


if __name__ == "__main__":
    main()
