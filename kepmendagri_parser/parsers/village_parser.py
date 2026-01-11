import re

def clean_name(value: str | None) -> str | None:
    if not value:
        return None

    value = re.sub(r"[\n\r\t]+", " ", value)
    value = re.sub(r"\s{2,}", " ", value)

    return value.strip()


VILLAGE_CODE_RE = re.compile(r"^\d{2}\.\d{2}\.\d{2}\.\d{4}$")
DISTRICT_CODE_RE = re.compile(r"^\d{2}\.\d{2}\.\d{2}$")


def extract_villages_from_table(table, page, initial_district_code=None):
    rows = []

    current_district_code = initial_district_code

    for r in table:
        if not r or len(r) < 4:
            continue

        kode = str(r[0]).strip() if r[0] else ""
        kelurahan = str(r[5]).strip() if len(r) >= 2 and r[5] else ""
        desa = str(r[6]).strip() if len(r) >= 1 and r[6] else ""

        if DISTRICT_CODE_RE.fullmatch(kode) and not VILLAGE_CODE_RE.fullmatch(kode):
            current_district_code = kode.replace(".", "")
            rows.append({
                "code": kode.replace(".", ""),
                "name": None,
                "district_code": current_district_code,
                "type": None,
                "source_page": page,
            })
            continue

        if VILLAGE_CODE_RE.fullmatch(kode) and current_district_code:
            name = None
            vtype = None

            if kelurahan and desa:
                name = f"{kelurahan} {desa}".strip()
                vtype = "village"
            elif kelurahan:
                name = kelurahan
                vtype = "urban_village"
            elif desa:
                name = desa
                vtype = "village"
            else:
                continue

            name = clean_name(
                re.sub(r"^\d+\s*", "", name)
            )

            rows.append({
                "code": kode.replace(".", ""),
                "name": name,
                "district_code": current_district_code,
                "type": vtype,
                "source_page": page,
            })

    return rows
