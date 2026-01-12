import re
from typing import List, Dict, Optional

# ============================================================
# 1. DETECTOR REGEX (HANYA UNTUK MENEMUKAN BARIS DATA)
# ============================================================

RE_MAIN_ROW = re.compile(
    r"""
    ^\s*
    (\d+)                    # nomor urut
    \s+
    (\d{2})\.(\d{2})         # kode wilayah
    \s+
    (Kabupaten|Kab|Kota)\s+
    (.+?)                    # kandidat nama (belum final)
    (?=\s+\d|\s*$)           # stop sebelum angka / akhir baris
    """,
    re.X | re.I,
)

RE_STOP_LINE = re.compile(
    r"(undang-?undang|keterangan\s*:)",
    re.I,
)

# ============================================================
# 2. NORMALISASI & SEMANTIC CLEANING
# ============================================================

ABBR_MAP = {
    "Kep.": "Kepulauan",
    "Kab.": "Kabupaten",
    "Propinsi": "Provinsi",
}

# kata hukum / relasi
STOP_NAME_TOKENS = {
    "tentang", "pembentukan", "perubahan", "perpanjangan",
    "provinsi", "propinsi", "daerah", "tingkat",
    "lingkungan", "keterangan", "hal",
    "dan", "di", "dalam", "termasuk",
}

# token yang TIDAK BOLEH muncul sebagai kelanjutan nama
ILLEGAL_TRAILING_TOKENS = {
    # induk / wilayah lain
    "kabupaten", "kabupaten-kabupaten",

    # artefak pemekaran
    "keerom", "paniai",

    # duplikasi umum
    "bharat", "bedagai",

    # arah wilayah (bukan nama resmi lanjutan)
    "utara", "selatan", "barat", "timur", "tengah",
}

def normalize(text: str) -> str:
    for k, v in ABBR_MAP.items():
        text = text.replace(k, v)
    return " ".join(text.split()).strip()


def clean_region_name(raw_name: str) -> str:
    """
    Pemotong NAMA FINAL (rule-based, nasional)

    Prinsip:
    - Ambil frasa TERPENDEK
    - Stop jika:
      * kata hukum / relasi
      * delimiter
      * token ilegal (pemekaran / induk / duplikasi)
    """

    tokens = (
        raw_name
        .replace(",", " ")
        .replace(";", " ")
        .split()
    )

    cleaned = []
    for t in tokens:
        tl = t.lower()

        if tl in STOP_NAME_TOKENS:
            break

        if cleaned and tl in ILLEGAL_TRAILING_TOKENS:
            break

        cleaned.append(t)

    return " ".join(cleaned).strip()


def looks_like_capital(line: str) -> bool:
    """
    Heuristik ibu kota:
    Boroko, Ondong Siau, Kota Mulia, dll
    """
    words = line.split()
    return 1 <= len(words) <= 3 and all(w[:1].isupper() for w in words)

# ============================================================
# 3. MAIN EXTRACTOR
# ============================================================

def extract_regencies_from_page_text(
    text: str,
    page_num: int,
    expected_province_code: Optional[str] = None,
) -> List[Dict]:

    rows: List[Dict] = []
    current = None

    def flush():
        nonlocal current
        if not current:
            return

        raw_name = normalize(" ".join(current["name_parts"]))
        final_name = clean_region_name(raw_name)

        if not final_name:
            current = None
            return

        rows.append({
            "code": current["code"],
            "province_code": current["code"][:2],
            "name": f'{current["kind"]} {final_name}',
            "type": "city" if current["kind"].lower() == "kota" else "regency",
            "source_page": page_num,
        })
        current = None

    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue

        # ====================================================
        # PRIORITAS 1 — BARIS DATA
        # ====================================================
        m = RE_MAIN_ROW.search(line)
        if m:
            flush()

            _, prov, kab, kind, name = m.groups()

            if expected_province_code and prov != expected_province_code:
                continue

            current = {
                "code": f"{prov}{kab}",
                "kind": "Kota" if kind.lower() == "kota" else "Kabupaten",
                "name_parts": [name],
            }
            continue

        # ====================================================
        # PRIORITAS 2 — METADATA / HUKUM
        # ====================================================
        if RE_STOP_LINE.search(line):
            continue

        # ====================================================
        # PRIORITAS 3 — LANJUTAN NAMA (MULTILINE)
        # ====================================================
        if current:
            if re.search(r"\d", line):
                continue
            if looks_like_capital(line):
                continue

            current["name_parts"].append(line)

    flush()
    return rows
