import pandas as pd
from pathlib import Path

def save_province_rows(rows, out_dir: Path):
    if not rows:
        return

    out = out_dir / "province_raw.csv"
    out.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(rows)
    df.to_csv(out, index=False)

    print(f"[CSV] province: {len(df)} rows → {out}")
