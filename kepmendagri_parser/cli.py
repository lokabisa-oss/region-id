import argparse
from pathlib import Path
from .pipeline.runner import run_pipeline

def main():
    parser = argparse.ArgumentParser(
        prog="kepmendagri-parser",
        description="Parse Kepmendagri PDF into structured regional datasets"
    )

    parser.add_argument("pdf", type=Path)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--start-page", type=int, default=1)
    parser.add_argument("--end-page", type=int)

    # 🔧 DEBUG OPTIONS
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug output (same as --debug-level=1)"
    )
    parser.add_argument(
        "--debug-level",
        type=int,
        choices=[0, 1, 2, 3],
        default=0,
        help="Debug level: 0=off, 1=info, 2=verbose, 3=trace"
    )

    args = parser.parse_args()

    debug_level = args.debug_level
    if args.debug:
        debug_level = max(debug_level, 1)

    run_pipeline(
        pdf_path=args.pdf,
        out_dir=args.out_dir,
        start_page=args.start_page,
        end_page=args.end_page,
        debug_level=debug_level,
    )

if __name__ == "__main__":
    main()
