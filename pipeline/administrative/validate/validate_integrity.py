import csv
import sys


def load_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def fail(message):
    raise ValueError(message)


def validate_provinces(provinces):
    """
    Validate province.csv
    """
    required_columns = {"code", "name"}
    seen_codes = set()

    for idx, row in enumerate(provinces, start=1):
        # --- required columns ---
        missing = required_columns - row.keys()
        if missing:
            fail(f"[province.csv] Row {idx}: missing columns {missing}")

        code = row.get("code", "").strip()
        name = row.get("name", "").strip()

        # --- code rules ---
        if not code:
            fail(f"[province.csv] Row {idx}: code is empty")

        if not code.isdigit():
            fail(f"[province.csv] Row {idx}: code must be numeric (got '{code}')")

        if len(code) != 2:
            fail(f"[province.csv] Row {idx}: code must be 2 digits (got '{code}')")

        if code in seen_codes:
            fail(f"[province.csv] Row {idx}: duplicate code '{code}'")

        seen_codes.add(code)

        # --- name rules ---
        if not name:
            fail(f"[province.csv] Row {idx}: name is empty")

        # --- area_km2 rules ---
        area = row.get("area_km2", "").strip()
        if area:
            try:
                area_val = float(area)
            except ValueError:
                fail(f"[province.csv] Row {idx}: area_km2 must be numeric (got '{area}')")

            if area_val <= 0:
                fail(f"[province.csv] Row {idx}: area_km2 must be > 0 (got '{area}')")

        # --- island_count rules ---
        island_count = row.get("island_count", "").strip()
        if island_count:
            if not island_count.isdigit():
                fail(
                    f"[province.csv] Row {idx}: island_count must be integer "
                    f"(got '{island_count}')"
                )

            if int(island_count) < 0:
                fail(
                    f"[province.csv] Row {idx}: island_count must be >= 0 "
                    f"(got '{island_count}')"
                )

def validate_regencies(regencies, provinces):
    """
    Validate regency.csv
    """
    required_columns = {"code", "name", "province_code", "type"}
    seen_codes = set()
    province_codes = {p["code"].strip() for p in provinces}

    for idx, row in enumerate(regencies, start=1):
        # --- required columns ---
        missing = required_columns - row.keys()
        if missing:
            fail(f"[regency.csv] Row {idx}: missing columns {missing}")

        code = row.get("code", "").strip()
        name = row.get("name", "").strip()
        province_code = row.get("province_code", "").strip()
        regency_type = row.get("type", "").strip()

        # --- code rules ---
        if not code:
            fail(f"[regency.csv] Row {idx}: code is empty")

        if not code.isdigit():
            fail(f"[regency.csv] Row {idx}: code must be numeric (got '{code}')")

        if len(code) != 4:
            fail(f"[regency.csv] Row {idx}: code must be 4 digits (got '{code}')")

        if code in seen_codes:
            fail(f"[regency.csv] Row {idx}: duplicate code '{code}'")

        seen_codes.add(code)

        # --- name ---
        if not name:
            fail(f"[regency.csv] Row {idx}: name is empty")

        # --- province_code ---
        if not province_code:
            fail(f"[regency.csv] Row {idx}: province_code is empty")

        if not province_code.isdigit():
            fail(
                f"[regency.csv] Row {idx}: province_code must be numeric "
                f"(got '{province_code}')"
            )

        if len(province_code) != 2:
            fail(
                f"[regency.csv] Row {idx}: province_code must be 2 digits "
                f"(got '{province_code}')"
            )

        if province_code not in province_codes:
            fail(
                f"[regency.csv] Row {idx}: province_code '{province_code}' "
                f"does not exist in province.csv"
            )

        # --- type ---
        if regency_type not in {"regency", "city"}:
            fail(
                f"[regency.csv] Row {idx}: invalid type '{regency_type}' "
                f"(must be 'regency' or 'city')"
            )

        # --- area_km2 ---
        area = row.get("area_km2", "").strip()
        if area:
            try:
                area_val = float(area)
            except ValueError:
                fail(
                    f"[regency.csv] Row {idx}: area_km2 must be numeric "
                    f"(got '{area}')"
                )

            if area_val <= 0:
                fail(
                    f"[regency.csv] Row {idx}: area_km2 must be > 0 "
                    f"(got '{area}')"
                )

def validate_districts(districts, regencies):
    """
    Validate district.csv
    """
    required_columns = {"code", "name", "regency_code"}
    seen_codes = set()
    regency_codes = {r["code"].strip() for r in regencies}

    for idx, row in enumerate(districts, start=1):
        # --- required columns ---
        missing = required_columns - row.keys()
        if missing:
            fail(f"[district.csv] Row {idx}: missing columns {missing}")

        code = row.get("code", "").strip()
        name = row.get("name", "").strip()
        regency_code = row.get("regency_code", "").strip()

        # --- code rules ---
        if not code:
            fail(f"[district.csv] Row {idx}: code is empty")

        if not code.isdigit():
            fail(f"[district.csv] Row {idx}: code must be numeric (got '{code}')")

        if len(code) != 6:
            fail(f"[district.csv] Row {idx}: code must be 6 digits (got '{code}')")

        if code in seen_codes:
            fail(f"[district.csv] Row {idx}: duplicate code '{code}'")

        seen_codes.add(code)

        # --- name ---
        if not name:
            fail(f"[district.csv] Row {idx}: name is empty")

        # --- regency_code ---
        if not regency_code:
            fail(f"[district.csv] Row {idx}: regency_code is empty")

        if not regency_code.isdigit():
            fail(
                f"[district.csv] Row {idx}: regency_code must be numeric "
                f"(got '{regency_code}')"
            )

        if len(regency_code) != 4:
            fail(
                f"[district.csv] Row {idx}: regency_code must be 4 digits "
                f"(got '{regency_code}')"
            )

        if regency_code not in regency_codes:
            fail(
                f"[district.csv] Row {idx}: regency_code '{regency_code}' "
                f"does not exist in regency.csv"
            )

        # --- forbidden attributes ---
        if "area_km2" in row and row.get("area_km2", "").strip():
            fail(
                f"[district.csv] Row {idx}: area_km2 is not allowed at district level"
            )

        if "island_count" in row and row.get("island_count", "").strip():
            fail(
                f"[district.csv] Row {idx}: island_count is not allowed at district level"
            )

def validate_villages(villages, districts):
    """
    Validate village.csv
    """
    required_columns = {"code", "name", "district_code", "type"}
    seen_codes = set()
    district_codes = {d["code"].strip() for d in districts}

    for idx, row in enumerate(villages, start=1):
        # --- required columns ---
        missing = required_columns - row.keys()
        if missing:
            fail(f"[village.csv] Row {idx}: missing columns {missing}")

        code = row.get("code", "").strip()
        name = row.get("name", "").strip()
        district_code = row.get("district_code", "").strip()
        village_type = row.get("type", "").strip()

        # --- code rules ---
        if not code:
            fail(f"[village.csv] Row {idx}: code is empty")

        if not code.isdigit():
            fail(f"[village.csv] Row {idx}: code must be numeric (got '{code}')")

        if len(code) != 10:
            fail(f"[village.csv] Row {idx}: code must be 10 digits (got '{code}')")

        if code in seen_codes:
            fail(f"[village.csv] Row {idx}: duplicate code '{code}'")

        seen_codes.add(code)

        # --- name ---
        if not name:
            fail(f"[village.csv] Row {idx}: name is empty")

        # --- district_code ---
        if not district_code:
            fail(f"[village.csv] Row {idx}: district_code is empty")

        if not district_code.isdigit():
            fail(
                f"[village.csv] Row {idx}: district_code must be numeric "
                f"(got '{district_code}')"
            )

        if len(district_code) != 6:
            fail(
                f"[village.csv] Row {idx}: district_code must be 6 digits "
                f"(got '{district_code}')"
            )

        if district_code not in district_codes:
            fail(
                f"[village.csv] Row {idx}: district_code '{district_code}' "
                f"does not exist in district.csv"
            )

        # --- type ---
        if village_type not in {"desa", "kelurahan"}:
            fail(
                f"[village.csv] Row {idx}: invalid type '{village_type}' "
                f"(must be 'desa' or 'kelurahan')"
            )

        # --- forbidden attributes ---
        if "area_km2" in row and row.get("area_km2", "").strip():
            fail(
                f"[village.csv] Row {idx}: area_km2 is not allowed at village level"
            )

        if "island_count" in row and row.get("island_count", "").strip():
            fail(
                f"[village.csv] Row {idx}: island_count is not allowed at village level"
            )

def main():
    try:
        provinces = load_csv("data/kemendagri/province.csv")
        regencies = load_csv("data/kemendagri/regency.csv")
        districts = load_csv("data/kemendagri/district.csv")
        villages = load_csv("data/kemendagri/village.csv")

        validate_provinces(provinces)
        validate_regencies(regencies, provinces)
        validate_districts(districts, regencies)
        validate_villages(villages, districts)

    except Exception as e:
        print(f"VALIDATION FAILED: {e}", file=sys.stderr)
        sys.exit(1)

    print("Province, regency, district & village validation passed ✔")

if __name__ == "__main__":
    main()
