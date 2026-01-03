import pandas as pd
from pathlib import Path

def save_district_rows(rows, out_dir: Path):
    if not rows:
        return

    out = out_dir / "district_raw.csv"
    out.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(rows).drop_duplicates(subset=["code"])
    df.to_csv(out, index=False)

    print(f"[CSV] district: {len(df)} rows → {out}")
