import re

PROVINCE_CODE_RE = re.compile(r"^\d{2}$")
REGENCY_CODE_RE  = re.compile(r"^\d{2}\.\d{2}$")
DISTRICT_CODE_RE = re.compile(r"^\d{2}\.\d{2}\.\d{2}$")

def clean_name(value: str | None) -> str | None:
    if not value:
        return None

    value = re.sub(r"[\n\r\t]+", " ", value)

    value = re.sub(r"\s{2,}", " ", value)

    return value.strip()

def normalize_header_rows(table, max_rows=2):
    headers = table[:max_rows]

    col_count = max(len(r) for r in headers)
    merged = [""] * col_count

    for r in headers:
        for i, cell in enumerate(r):
            if cell:
                merged[i] += " " + str(cell)

    return [h.strip().upper().replace("\n", " ") for h in merged]

def find_col_idx(headers, keyword):
    for i, h in enumerate(headers):
        if keyword in h:
            return i
    return None

def extract_districts_from_table(table, page_num, initial_context=None):
    current_province_code = None
    current_regency_code = None
    current_province_capital = None
    current_regency_capital = None

    if initial_context:
        current_province_code = initial_context.get("province_code")
        current_regency_code = initial_context.get("regency_code")
        current_province_capital = initial_context.get("province_capital")
        current_regency_capital = initial_context.get("regency_capital")

    rows = []

    headers = normalize_header_rows(table)
    idx_code = find_col_idx(headers, "KODE")
    idx_name = find_col_idx(headers, "KECAMATAN")
    idx_cap  = find_col_idx(headers, "IBUKOTA")

    if idx_code is None or idx_name is None:
        return rows

    for r in table:
        if not r or idx_code >= len(r):
            continue

        code = str(r[idx_code]).strip() if r[idx_code] else ""
        name = str(r[idx_name]).strip() if r[idx_name] else ""
        capital = clean_name(
            str(r[idx_cap]).strip()
            if idx_cap is not None and idx_cap < len(r) and r[idx_cap]
            else ""
        )

        if not code:
            continue

        # === PROVINSI ===
        if PROVINCE_CODE_RE.fullmatch(code):
            current_province_code = code
            if capital:
                current_province_capital = capital
                rows.append({
                    "code": code.replace(".", ""),
                    "province_code": current_province_code,
                    "regency_code": current_regency_code,
                    "name": None,
                    "province_capital": current_province_capital,
                    "regency_capital": current_regency_capital,
                    "source_page": page_num,
                })
            continue

        # === KABUPATEN / KOTA ===
        if REGENCY_CODE_RE.fullmatch(code):
            current_regency_code = code.replace(".", "")
            if capital:
                current_regency_capital = capital
                rows.append({
                    "code": code.replace(".", ""),
                    "province_code": current_province_code,
                    "regency_code": current_regency_code,
                    "name": None,
                    "province_capital": current_province_capital,
                    "regency_capital": current_regency_capital,
                    "source_page": page_num,
                })
            continue

        # === KECAMATAN ===
        if DISTRICT_CODE_RE.fullmatch(code):
            rows.append({
                "code": code.replace(".", ""),
                "province_code": current_province_code,
                "regency_code": current_regency_code,
                "name": re.sub(r"^\d+\s+", "", name),
                "province_capital": current_province_capital,
                "regency_capital": current_regency_capital,
                "source_page": page_num,
            })

    return rows