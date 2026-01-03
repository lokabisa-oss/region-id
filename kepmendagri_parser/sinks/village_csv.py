import pandas as pd
from pathlib import Path

def save_village_rows(rows, out_dir: Path):
    if not rows:
        return

    out = out_dir / "village_raw.csv"
    out.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(rows)
    df = df.drop_duplicates(subset=["code"])
    df = df.sort_values("code")

    df.to_csv(out, index=False)

    print(f"[CSV] village: {len(df)} rows → {out}")
