from pathlib import Path

import pdfplumber
from kepmendagri_parser.classifier.page_classifier import classify_page
from kepmendagri_parser.extractors.page_text import extract_page_text

BASE_DIR = Path(__file__).resolve().parent.parent

PDF_PATH = BASE_DIR / "data/kemendagri/raw/kepmendagri-300.2.2-2138-2025.pdf"

with pdfplumber.open(PDF_PATH) as pdf:
    for i, page in enumerate(pdf.pages[:31], start=1):
        page_type = classify_page(page)

    
        print(f"Page {i}")
        print(f"PageType: {page_type}")

        print("=" * 60)
