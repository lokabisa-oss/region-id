#!/usr/bin/env python3
"""
Administrative pipeline runner.

Orchestrates the administrative data pipeline:
extract → transform → validate.

Validation is treated as a mandatory quality gate.
"""

import sys
import argparse
from pathlib import Path

from pipeline.administrative.validate.validate_integrity import (
    load_csv,
    validate_provinces,
    validate_regencies,
    validate_districts,
    validate_villages,
)


DEFAULT_DATA_DIR = Path("data/kemendagri")


def extract(verbose=False):
    """
    Extract raw administrative data from source documents.
    """
    if verbose:
        print("Extract step: started")
    print("Extract step: skipped (not implemented)")


def transform(verbose=False):
    """
    Transform raw data into normalized CSV outputs.
    """
    if verbose:
        print("Transform step: started")
    print("Transform step: skipped (not implemented)")


def validate(data_dir: Path, verbose=False):
    """
    Run integrity validation on administrative CSV outputs.
    """
    if verbose:
        print(f"Validation step: loading data from {data_dir}")

    provinces = load_csv(data_dir / "province.csv")
    regencies = load_csv(data_dir / "regency.csv")
    districts = load_csv(data_dir / "district.csv")
    villages = load_csv(data_dir / "village.csv")

    validate_provinces(provinces)
    validate_regencies(regencies, provinces)
    validate_districts(districts, regencies)
    validate_villages(villages, districts)

    print("Validation step: passed ✔")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run administrative data pipeline"
    )

    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Run validation only (skip extract and transform)",
    )

    parser.add_argument(
        "--skip-extract",
        action="store_true",
        help="Skip extract step",
    )

    parser.add_argument(
        "--skip-transform",
        action="store_true",
        help="Skip transform step",
    )

    parser.add_argument(
        "--data-dir",
        type=Path,
        default=DEFAULT_DATA_DIR,
        help="Path to administrative data directory (default: data/kemendagri)",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    try:
        if args.validate_only:
            validate(args.data_dir, verbose=args.verbose)
        else:
            if not args.skip_extract:
                extract(verbose=args.verbose)

            if not args.skip_transform:
                transform(verbose=args.verbose)

            validate(args.data_dir, verbose=args.verbose)

    except Exception as e:
        print(f"PIPELINE FAILED: {e}", file=sys.stderr)
        sys.exit(1)

    print("Administrative pipeline completed successfully ✔")


if __name__ == "__main__":
    main()
