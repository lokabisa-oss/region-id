from kepmendagri_parser.models.row import Row

def extract_rows(page) -> list[Row]:
    """
    Abstract extractor.
    Implement with pdfplumber / camelot later.
    """
    raise NotImplementedError
