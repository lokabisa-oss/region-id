import re

REGEX = re.compile(
    r"(?P<code>\d{2}\.\d{2})\s+"
    r"(?P<name>(Kabupaten|Kota)\s+[A-Za-z\s]+?)\s+"
    r"(?P<numbers>(\d[\d.,]*\s+){3,})"
)

def extract_regency_aggregate_from_text(text, page_num):
    rows = []

    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue

        m = REGEX.search(line)
        if not m:
            continue

        raw_code = m.group("code")
        code = raw_code.replace(".", "")
        province_code = code[:2]

        name = m.group("name").strip()
        regency_type = "city" if name.startswith("Kota") else "regency"

        # Ambil semua angka di baris
        numbers = re.findall(r"\d[\d.,]*", line)

        # Struktur Aceh: KEC, DESA, LUAS, PENDUDUK
        if len(numbers) < 4:
            continue

        rows.append({
            "code": code,
            "name": name,
            "province_code": province_code,
            "type": regency_type,
            "district_count": numbers[-4],
            "urban_village_count": "0",
            "rural_village_count": numbers[-3],
            "area_km2": numbers[-2],
            "population": numbers[-1],
            "source_page": page_num,
        })

    return rows
