import pandas as pd
from pathlib import Path

def save_regency_rows(rows, out_dir: Path):
    if not rows:
        return

    out = out_dir / "regency_raw.csv"
    out.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(rows)
    df.to_csv(out, index=False)

    print(f"[CSV] regency: {len(df)} rows → {out}")
