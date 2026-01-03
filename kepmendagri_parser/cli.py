import argparse
import sys
from pathlib import Path

from tqdm import tqdm

from .pipeline.runner import run_pipeline
from .utils.input_resolver import is_url, download_file


def main():
    parser = argparse.ArgumentParser(
        prog="kepmendagri-parser",
        description="Parse Kepmendagri PDF into structured regional datasets",
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path or URL to Kepmendagri PDF",
    )
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Output directory for generated CSV files",
    )

    parser.add_argument(
        "--sha256",
        help="Expected SHA256 hash of the PDF (recommended for CI)",
    )

    parser.add_argument("--start-page", type=int, default=1)
    parser.add_argument("--end-page", type=int)

    parser.add_argument(
        "--reuse-raw",
        action="store_true",
        help="Reuse cached raw parsed data if available (skip PDF parsing)",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug output (same as --debug-level=1)",
    )
    parser.add_argument(
        "--debug-level",
        type=int,
        choices=[0, 1, 2, 3],
        default=0,
        help="Debug verbosity level",
    )

    args = parser.parse_args()

    # -------------------------
    # Resolve debug level
    # -------------------------
    debug_level = args.debug_level
    if args.debug:
        debug_level = max(debug_level, 1)

    # -------------------------
    # Resolve output dir
    # -------------------------
    out_dir = args.output.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    # -------------------------
    # Resolve input PDF
    # -------------------------
    if is_url(args.input):
        pdf_path = download_file(
            url=args.input,
            expected_sha256=args.sha256,
            debug_level=debug_level,
        )
    else:
        pdf_path = Path(args.input).resolve()
        if not pdf_path.exists():
            parser.error(f"Input PDF not found: {pdf_path}")

    # -------------------------
    # Progress bar (CLI concern only)
    # -------------------------
    show_progress = sys.stdout.isatty() and debug_level == 0 or debug_level == 1

    try:
        with tqdm(
            desc="Parsing pages",
            unit="page",
            disable=not show_progress,
            dynamic_ncols=True,
        ) as parse_pbar:

            def on_parse_progress(current, total):
                parse_pbar.total = total
                parse_pbar.n = current
                parse_pbar.refresh()

            run_pipeline(
                pdf_path=pdf_path,
                out_dir=out_dir,
                start_page=args.start_page,
                end_page=args.end_page,
                debug_level=debug_level,
                on_progress=on_parse_progress if show_progress else None,
                reuse_raw=args.reuse_raw,
            )

    except Exception as e:
        print("\n❌ Pipeline failed:", file=sys.stderr)
        print(str(e), file=sys.stderr)
        sys.exit(1)

    print("✅ Dataset generation completed successfully")


if __name__ == "__main__":
    main()
