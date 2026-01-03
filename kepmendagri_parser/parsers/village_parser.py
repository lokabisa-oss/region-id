import re

VILLAGE_CODE_RE = re.compile(r"\d{2}\.\d{2}\.\d{2}\.\d{4}")
DISTRICT_CODE_RE = re.compile(r"\d{2}\.\d{2}\.\d{2}")


def extract_villages_from_table(table, page):
    rows = []
    current_district_code = None

    for r in table[1:]:  # skip header
        if not r or len(r) < 7:
            continue

        kode = str(r[0]).strip() if r[0] else ""
        kelurahan = str(r[5]).strip() if len(r) > 5 and r[5] else ""
        desa = str(r[6]).strip() if len(r) > 6 and r[6] else ""

        # --- detect kecamatan header ---
        if DISTRICT_CODE_RE.fullmatch(kode) and not VILLAGE_CODE_RE.fullmatch(kode):
            current_district_code = kode.replace(".", "")
            continue

        # --- detect desa / kelurahan ---
        if VILLAGE_CODE_RE.fullmatch(kode) and current_district_code:
            if kelurahan:
                name = kelurahan
                vtype = "kelurahan"
            elif desa:
                name = desa
                vtype = "desa"
            else:
                continue

            # buang numbering "1 Nama"
            name = re.sub(r"^\d+\s*", "", name)

            rows.append({
                "code": kode.replace(".", ""),
                "name": name,
                "district_code": current_district_code,
                "type": vtype,
                "source_page": page,
            })

    return rows
