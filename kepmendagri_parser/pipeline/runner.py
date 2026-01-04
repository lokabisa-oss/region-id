import pdfplumber
from pathlib import Path
from typing import Callable

from kepmendagri_parser.pipeline.state import ParsingState
from kepmendagri_parser.pipeline.context import PageType

from kepmendagri_parser.classifier.page_classifier import classify_page
from kepmendagri_parser.extractors.page_table import extract_page_table

from kepmendagri_parser.parsers.province_parser import extract_provinces_from_table
from kepmendagri_parser.parsers.regency_parser import extract_regencies_from_table
from kepmendagri_parser.parsers.district_parser import extract_districts_from_table
from kepmendagri_parser.parsers.village_parser import extract_villages_from_table

from kepmendagri_parser.builders.dataset_builder import build_dataset

from kepmendagri_parser.utils.raw_cache import dump_raw, load_raw,  cleanup_tmp


def dbg(level: int, current: int, msg: str):
    if current >= level:
        print(msg)

def report_and_validate_counts(
    province_rows, regency_rows, district_rows, village_rows, debug_level
):
    dbg(1, debug_level, "📊 Raw parsing summary:")
    dbg(1, debug_level, f"  Provinces : {len(province_rows)}")
    dbg(1, debug_level, f"  Regencies : {len(regency_rows)}")
    dbg(1, debug_level, f"  Districts : {len(district_rows)}")
    dbg(1, debug_level, f"  Villages  : {len(village_rows)}")
    dbg(1, debug_level, "-" * 60)

    # sanity checks (optional tapi sangat disarankan)
    if len(province_rows) < 30:
        raise ValueError("❌ Province count too low — parsing likely failed")

    if len(regency_rows) < 500:
        raise ValueError("❌ Regency count too low — possible skipped pages")

    if len(district_rows) == 0:
        raise ValueError("❌ No districts parsed at all")

    if len(village_rows) == 0:
        raise ValueError("❌ No villages parsed at all")

def run_pipeline(
    pdf_path: Path,
    out_dir: Path,
    start_page: int = 1,
    end_page: int | None = None,
    debug_level: int = 0,
    on_progress: Callable[[int, int], None] | None = None,
    reuse_raw: bool = False,
):
    dbg(1, debug_level, "🚀 Starting Kepmendagri Parser Pipeline")
    dbg(1, debug_level, f"📄 Source PDF : {pdf_path}")
    dbg(1, debug_level, f"📂 Output dir : {out_dir}")
    dbg(1, debug_level, "-" * 60)

    tmp_dir = out_dir.parent / ".tmp"

    # ===============================
    # LOAD RAW (FAST PATH)
    # ===============================
    if reuse_raw and (tmp_dir / "province.raw.json").exists():
        dbg(1, debug_level, "♻️ Reusing cached raw data")
        province_rows = load_raw(tmp_dir / "province.raw.json")
        regency_rows  = load_raw(tmp_dir / "regency.raw.json")
        district_rows = load_raw(tmp_dir / "district.raw.json")
        village_rows  = load_raw(tmp_dir / "village.raw.json")

    # ===============================
    # PARSE PDF (SLOW PATH)
    # ===============================
    else:
        state = ParsingState()

        seen_province = False

        province_rows = []
        regency_rows = []
        district_rows = []
        village_rows = []

        district_context = {
            "province_code": None,
            "regency_code": None,
            "province_capital": None,
            "regency_capital": None,
        }

        village_context = {"district_code": None}

        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            end_page = min(end_page or total_pages, total_pages)

            total_to_process = end_page - start_page + 1
            processed = 0

            for page_number in range(start_page, end_page + 1):
                processed += 1

                if on_progress:
                    on_progress(processed, total_to_process)

                page = pdf.pages[page_number - 1]
                page_type = classify_page(page)

                if seen_province and page_type == PageType.UNKNOWN:
                    if on_progress:
                        # force progress to 100%
                        on_progress(total_to_process, total_to_process)
                    break

                if page_type == PageType.PROVINSI:
                    seen_province = True
                    rows = extract_provinces_from_table(
                        extract_page_table(page), page_number
                    )
                    province_rows.extend(rows)

                elif page_type == PageType.KAB_KOTA:
                    rows = extract_regencies_from_table(
                        extract_page_table(page), page_number
                    )
                    regency_rows.extend(rows)

                elif page_type == PageType.KECAMATAN:
                    rows = extract_districts_from_table(
                        extract_page_table(page),
                        page_number,
                        initial_context=district_context,
                    )
                    if rows:
                        last = rows[-1]
                        last_provice_code =  last.get("province_code")
                        last_regency_code = last.get("regency_code")
                        last_province_capital = last.get("province_capital")
                        last_regency_capital = last.get("regency_capital")

                        district_rows.extend(r for r in rows if r.get("name") is not None)
                        district_context.update({
                            "province_code": last_provice_code,
                            "regency_code": last_regency_code,
                            "province_capital": last_province_capital,
                            "regency_capital": last_regency_capital,
                        })

                elif page_type == PageType.KELURAHAN_DESA:
                    rows = extract_villages_from_table(
                        extract_page_table(page),
                        page_number,
                        initial_district_code=village_context["district_code"],
                    )
                    if rows:
                        village_rows.extend(rows)
                        village_context["district_code"] = rows[-1]["district_code"]

                state.last_page_type = page_type

        # === dump raw parsed data (implicit cache) ===
        dump_raw(province_rows, tmp_dir / "province.raw.json")
        dump_raw(regency_rows,  tmp_dir / "regency.raw.json")
        dump_raw(district_rows, tmp_dir / "district.raw.json")
        dump_raw(village_rows,  tmp_dir / "village.raw.json")
    
    # ===============================
    # RAW DATA REPORT
    # ===============================
    report_and_validate_counts(
        province_rows,
        regency_rows,
        district_rows,
        village_rows,
        debug_level,
    )

    # ===============================
    # BUILD FINAL DATASET (ALWAYS)
    # ===============================
    dbg(1, debug_level, "🛠️ Building final datasets…")

    try:
        build_dataset(
            province_rows,
            regency_rows,
            district_rows,
            village_rows,
            out_dir,
        )

    except Exception as e:
        dbg(1, debug_level, "❌ Dataset build failed")
        dbg(1, debug_level, f"Raw cache preserved at: {tmp_dir}")
        raise

    else:
        cleanup_tmp(tmp_dir)
        dbg(1, debug_level, "🧹 Temporary raw cache cleaned up")

    dbg(1, debug_level, "✅ Pipeline finished successfully")

