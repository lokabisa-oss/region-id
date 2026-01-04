import json
import argparse
import hashlib
from pathlib import Path
from datetime import datetime, timezone


DATASET_NAME = "region-id"
SOURCE_NAME = "Kementerian Dalam Negeri Republik Indonesia"
SOURCE_DOCUMENT_NAME = "Kepmendagri - Kode dan Data Wilayah Administrasi"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def count_rows(csv_path: Path) -> int:
    with csv_path.open(encoding="utf-8") as f:
        return sum(1 for _ in f) - 1  # exclude header


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate release metadata for region-id dataset"
    )

    parser.add_argument(
        "--version",
        required=True,
        help="Release version (e.g. v1.0.0)"
    )

    parser.add_argument(
        "--datasets",
        type=Path,
        default=Path("datasets"),
        help="Path to dataset CSV directory"
    )

    parser.add_argument(
        "--source",
        type=Path,
        required=True,
        help="Path to source Kepmendagri document"
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path("metadata/releases"),
        help="Output directory for release metadata"
    )

    return parser.parse_args()


def main():
    args = parse_args()

    datasets_dir = args.datasets
    output_dir = args.output
    source_doc = args.source
    version = args.version.lstrip("v")

    output_dir.mkdir(parents=True, exist_ok=True)

    records = {}
    for level in ["provinces", "regencies", "districts", "villages"]:
        path = datasets_dir / f"{level}.csv"
        if not path.exists():
            raise FileNotFoundError(f"Missing dataset file: {path}")
        records[level] = count_rows(path)

    metadata = {
        "dataset": DATASET_NAME,
        "version": version,
        "tag": f"v{version}",
        "status": "stable",
        "source": {
            "name": SOURCE_NAME,
            "document": SOURCE_DOCUMENT_NAME,
            "document_hash": {
                "algorithm": "sha256",
                "value": sha256_file(source_doc)
            }
        },
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "levels": [
            "province",
            "regency",
            "district",
            "village"
        ],
        "records": records,
        "format": "csv",
        "encoding": "utf-8"
    }

    output_path = output_dir / f"region-id-{version}.json"
    output_path.write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print(f"✔ Release metadata generated: {output_path}")


if __name__ == "__main__":
    main()
