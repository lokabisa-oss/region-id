import pandas as pd
from pathlib import Path

RAW = Path("data/kemendagri/raw/extracted/regency_raw.csv")
OUT = Path("data/kemendagri/regency.csv")

def parse_number(val):
    if pd.isna(val) or val == "":
        return None
    val = str(val).replace(".", "").replace(",", ".")
    try:
        return float(val) if "." in val else int(val)
    except ValueError:
        return None

def build_regency():
    df = pd.read_csv(RAW, dtype=str)

    for col in [
        "district_count",
        "urban_village_count",
        "rural_village_count",
        "area_km2",
    ]:
        df[col] = df[col].apply(parse_number)

    df["urban_village_count"] = df["urban_village_count"].fillna(0).astype(int)
    df["rural_village_count"] = df["rural_village_count"].fillna(0).astype(int)

    df["village_count"] = (
        df["urban_village_count"] + df["rural_village_count"]
    )

    df["capital"] = None

    df = df[
        [
            "code",
            "name",
            "province_code",
            "type",
            "capital",
            "area_km2",
            "district_count",
            "urban_village_count",
            "rural_village_count",
            "village_count",
        ]
    ]

    df = df.sort_values(["province_code", "code"])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)

    print(f"Wrote {len(df)} rows → {OUT}")

if __name__ == "__main__":
    build_regency()
