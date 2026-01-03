from pathlib import Path
from collections import defaultdict
import csv


# =========================
# Helpers: CSV IO
# =========================

def write_csv(path: Path, rows: list[dict], fieldnames: list[str]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k) for k in fieldnames})


# =========================
# Helpers: Validation
# =========================

def assert_unique(rows: list[dict], key: str, label: str):
    seen = set()
    for r in rows:
        v = r.get(key)
        if v in seen:
            raise ValueError(f"[{label}] duplicate {key}: {v}")
        seen.add(v)


def assert_fk(
    children,
    child_key,
    parents,
    parent_key,
    label,
    context_keys: list[str] | None = None,
):
    parent_values = {p[parent_key] for p in parents}

    for c in children:
        v = c.get(child_key)
        if v not in parent_values:
            lines = [
                f"[{label}] invalid foreign key",
                f"  {child_key} = {v}",
            ]

            if context_keys:
                for k in context_keys:
                    if k in c:
                        lines.append(f"  {k} = {c[k]}")

            sample = sorted(list(parent_values))[:10]
            lines.append(f"  known {parent_key}s (sample): {sample}")

            raise ValueError("\n".join(lines))


# =========================
# Normalize Builders
# =========================

def normalize_district(district_rows: list[dict]) -> list[dict]:
    out = []
    for r in district_rows:
        out.append({
            "code": r["code"],
            "regency_code": r["regency_code"],
            "province_code": r["province_code"],
            "name": r["name"],
        })

    # validations
    assert_unique(out, "code", "district")
    return sorted(out, key=lambda x: x["code"])

def normalize_regency(regency_rows: list[dict], districts: list[dict]):
    by_regency = defaultdict(set)

    for d in districts:
        if d.get("regency_capital"):
            by_regency[d["regency_code"]].add(d["regency_capital"])

    out = []
    for r in regency_rows:
        capitals = by_regency.get(r["code"], set())

        if len(capitals) == 1:
            capital = next(iter(capitals))
        elif len(capitals) == 0:
            capital = None
        else:
            raise ValueError(
                f"[province] multiple capitals for {p['code']}: {sorted(capitals)}"
            )

        out.append({
            "code": r["code"],
            "province_code": r["province_code"],
            "name": r["name"],
            "type": r["type"],
            "capital": capital,
        })

    assert_unique(out, "code", "regency")
    return sorted(out, key=lambda x: x["code"])

def normalize_province(province_rows: list[dict], districts: list[dict]) -> list[dict]:
    by_province = defaultdict(set)

    for d in districts:
        if d.get("province_capital"):
            by_province[d["province_code"]].add(d["province_capital"])

    out = []
    for p in province_rows:
        capitals = by_province.get(p["code"], set())

        if len(capitals) == 1:
            capital = next(iter(capitals))
        elif len(capitals) == 0:
            capital = None
        else:
            raise ValueError(
                f"[province] multiple capitals for {p['code']}: {sorted(capitals)}"
            )


        out.append({
            "code": p["code"],
            "name": p["name"],
            "capital": capital,
        })

    # validations
    assert_unique(out, "code", "province")
    return sorted(out, key=lambda x: x["code"])


def normalize_village(village_rows: list[dict]) -> list[dict]:
    out = []
    for v in village_rows:
        out.append({
            "code": v["code"],
            "district_code": v["district_code"],
            "name": v.get("name"),
            "type": v["type"],
            "note": v.get("note"),
        })

    # validations
    assert_unique(out, "code", "village")
    return sorted(out, key=lambda x: x["code"])


# =========================
# Orchestrator (1x run)
# =========================

def build_dataset(
    province_rows: list[dict],
    regency_rows: list[dict],
    district_rows: list[dict],
    village_rows: list[dict],
    out_dir: Path,
):
    """
    One-shot builder:
    parse → normalize → derive → validate → write FINAL CSV
    """

    districts_raw = district_rows

    # 1) normalize base
    districts = normalize_district(district_rows)

    # 2) regency (capital from district)
    regencies = normalize_regency(regency_rows, districts_raw)

    # 3) province (capital from regency → district)
    provinces = normalize_province(province_rows, districts_raw)

    # 4) village (pure)
    villages = normalize_village(village_rows)

    # 5) foreign key validations (now all parents exist)
    assert_fk(regencies, "province_code", provinces, "code", "regency")
    assert_fk(districts, "regency_code", regencies, "code", "district")
    assert_fk(villages, "district_code", districts, "code", "village")

    # 6) write FINAL datasets
    write_csv(out_dir / "province.csv", provinces,
              ["code", "name", "capital"])
    write_csv(out_dir / "regency.csv", regencies,
              ["code", "name", "province_code", "type", "capital"])
    write_csv(out_dir / "district.csv", districts,
              ["code", "name", "regency_code", "province_code"])
    write_csv(out_dir / "village.csv", villages,
              ["code", "name", "district_code", "type", "note"])
