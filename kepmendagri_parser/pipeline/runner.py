import pdfplumber
from pathlib import Path

from kepmendagri_parser.pipeline.state import ParsingState
from kepmendagri_parser.pipeline.context import PageType

from kepmendagri_parser.classifier.page_classifier import classify_page
from kepmendagri_parser.extractors.page_table import extract_page_table

from kepmendagri_parser.parsers.province_parser import extract_provinces_from_table
from kepmendagri_parser.parsers.regency_parser import extract_regencies_from_table
from kepmendagri_parser.parsers.district_parser import extract_districts_from_table
from kepmendagri_parser.parsers.village_parser import extract_villages_from_table

from kepmendagri_parser.sinks.province_csv import save_province_rows
from kepmendagri_parser.sinks.regency_csv import save_regency_rows
from kepmendagri_parser.sinks.district_csv import save_district_rows
from kepmendagri_parser.sinks.village_csv import save_village_rows


def dbg(level: int, current: int, msg: str):
    if current >= level:
        print(msg)


def run_pipeline(
    pdf_path: Path,
    out_dir: Path,
    start_page: int = 1,
    end_page: int | None = None,
    debug_level: int = 0,
):
    dbg(1, debug_level, "🚀 Starting Kepmendagri Parser Pipeline")
    dbg(1, debug_level, f"📄 Source PDF : {pdf_path}")
    dbg(1, debug_level, f"📂 Output dir : {out_dir}")
    dbg(1, debug_level, "-" * 60)

    state = ParsingState()

    seen_province = False
    unknown_after_province = 0

    province_rows = []
    regency_rows = []
    district_rows = []
    village_rows = []

    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        end_page = min(end_page or total_pages, total_pages)

        for page_number in range(start_page, end_page + 1):
            dbg(1, debug_level, f"\n📄 Page {page_number}/{total_pages}")

            page = pdf.pages[page_number - 1]
            page_type = classify_page(page)

            dbg(1, debug_level, f"   🔎 Classified as: {page_type.name}")

            # --- province tracking ---
            if page_type == PageType.PROVINSI and not seen_province:
                seen_province = True
                unknown_after_province = 0
                dbg(1, debug_level, "   🏳️ First PROVINSI page detected")

            if seen_province:
                if page_type == PageType.UNKNOWN:
                    unknown_after_province += 1
                    dbg(1, debug_level, f"   ⚠️ UNKNOWN after PROVINSI ({unknown_after_province})")
                else:
                    unknown_after_province = 0

                if unknown_after_province >= 1:
                    dbg(1, debug_level, "   ⛔ Stop condition reached (UNKNOWN after PROVINSI)")
                    break

            # fallback ke last_page_type
            if page_type == PageType.UNKNOWN and state.last_page_type:
                dbg(2, debug_level, f"   ↩️ Fallback to last page type: {state.last_page_type.name}")
                page_type = state.last_page_type

            tables = extract_page_table(page)
            dbg(2, debug_level, f"   📊 Tables detected: {len(tables)}")

            if debug_level >= 3 and tables:
                dbg(3, debug_level, f"   🧾 Table[0] header preview: {tables[0][:5]}")

            # --- routing ---
            if page_type == PageType.PROVINSI:
                rows = extract_provinces_from_table(tables, page_number)
                province_rows.extend(rows)
                dbg(2, debug_level, f"   ✅ Provinces parsed: {len(rows)}")

            elif page_type == PageType.KAB_KOTA:
                rows = extract_regencies_from_table(tables, page_number)
                regency_rows.extend(rows)
                dbg(2, debug_level, f"   ✅ Regencies parsed: {len(rows)}")

            elif page_type == PageType.KECAMATAN:
                rows = extract_districts_from_table(tables, page_number)
                district_rows.extend(rows)
                dbg(2, debug_level, f"   ✅ Districts parsed: {len(rows)}")

            elif page_type == PageType.KELURAHAN_DESA:
                rows = extract_villages_from_table(tables, page_number)
                village_rows.extend(rows)
                dbg(2, debug_level, f"   ✅ Villages parsed: {len(rows)}")

            state.last_page_type = page_type

    dbg(1, debug_level, "\n" + "=" * 60)
    dbg(1, debug_level, "📝 Writing CSV outputs...")
    dbg(1, debug_level, f"   Provinces : {len(province_rows)}")
    dbg(1, debug_level, f"   Regencies : {len(regency_rows)}")
    dbg(1, debug_level, f"   Districts : {len(district_rows)}")
    dbg(1, debug_level, f"   Villages  : {len(village_rows)}")

    save_province_rows(province_rows, out_dir)
    save_regency_rows(regency_rows, out_dir)
    save_district_rows(district_rows, out_dir)
    save_village_rows(village_rows, out_dir)

    dbg(1, debug_level, "✅ Pipeline finished successfully")

