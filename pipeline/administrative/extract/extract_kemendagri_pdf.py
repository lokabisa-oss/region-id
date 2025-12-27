import pandas as pd
from pathlib import Path

from .parsers.province_aggregate import extract_province_aggregate
from .parsers.regency_aggregate import extract_regency_aggregate_from_text


PDF = Path("data/kemendagri/raw/kepmendagri-300.2.2-2138-2025.pdf")


def extract_province():
    out = Path("data/kemendagri/raw/extracted/province_aggregate_raw.csv")
    rows = extract_province_aggregate(PDF, pages=[16, 17])

    df = pd.DataFrame(rows)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)

    print(f"Extracted {len(df)} province aggregate rows → {out}")


def extract_regency():
    out = Path("data/kemendagri/raw/extracted/regency_raw.csv")
    all_rows = []

    pages = [18, 19]

    import pdfplumber
    with pdfplumber.open(PDF) as pdf:
        for page_num in pages:
            page = pdf.pages[page_num - 1]
            text = page.extract_text() or ""
    
            rows = extract_regency_aggregate_from_text(text, page_num)
            all_rows.extend(rows)

    df = pd.DataFrame(all_rows)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)

    print(f"Extracted {len(df)} regency rows → {out}")




if __name__ == "__main__":
    # extract_province()
    extract_regency()
