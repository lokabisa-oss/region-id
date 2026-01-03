import re
from kepmendagri_parser.pipeline.context import PageType
from kepmendagri_parser.extractors.page_table import extract_page_table


def classify_page(page) -> PageType:
    tables = extract_page_table(page)
    if not tables:
        return PageType.UNKNOWN 

    header = tables[0]

    if not header:
        return PageType.UNKNOWN

    # helper
    LETTER_SPACING_RE = re.compile(r"(?<=\b[A-Z])\s+(?=[A-Z]\b)")
    def normalize_header(cell: str | None) -> str:
        if not cell:
            return ""

        s = cell.upper()

        # 1️⃣ rapatkan huruf yang terpisah satu-satu (K O D E → KODE)
        s = LETTER_SPACING_RE.sub("", s)

        # 2️⃣ buang footnote (*), **), dll
        s = re.sub(r"\*+\)", "", s)

        # 3️⃣ normalisasi whitespace biasa
        s = re.sub(r"\s+", " ", s).strip()

        return s.split()[-1]
    

    col1_last = normalize_header(header[0])
    col3_last = normalize_header(header[2]) if len(header) >= 3 else ""

    has_no_col = col1_last == "NO"
    
    # === FINAL RULES ===

    # Leaf table: Desa / Kelurahan
    if col1_last == "KODE":
        return PageType.KELURAHAN_DESA

    # Provinsi → daftar kabupaten/kota
    if col3_last == "PROVINSI" and has_no_col:
        return PageType.PROVINSI

    # Kabupaten/Kota → daftar kecamatan
    if col3_last == "KOTA" and has_no_col:
        return PageType.KAB_KOTA

    # Kecamatan → halaman desa/kelurahan (tanpa NO)
    if col3_last == "KECAMATAN" and has_no_col:
        return PageType.KECAMATAN


    return PageType.UNKNOWN
