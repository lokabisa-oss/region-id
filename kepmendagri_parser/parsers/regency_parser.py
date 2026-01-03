import re

def split_cell(cell):
    if not cell:
        return []
    return [x.strip() for x in str(cell).split("\n") if x.strip()]

REGENCY_CODE_RE = re.compile(r"^\d{2}\.\d{2}$")

def extract_regencies_from_table(table, page_num):
    rows = []

    # baris data utama biasanya index ke-2 (setelah header)
    data_row = next((r for r in table if r and r[1] and "\n" in str(r[1])), None)
    if not data_row:
        return rows

    codes  = split_cell(data_row[1])  # KODE
    names  = split_cell(data_row[2])  # NAMA KABUPATEN / KOTA

    for code_raw, name in zip(codes, names):
        if not REGENCY_CODE_RE.fullmatch(code_raw):
            continue

        code = code_raw.replace(".", "")
        province_code = code[:2]

        regency_type = "city" if name.startswith("Kota") else "regency"

        rows.append({
            "code": code,
            "province_code": province_code,
            "name": name,
            "type": regency_type,
            "source_page": page_num,
        })

    return rows
