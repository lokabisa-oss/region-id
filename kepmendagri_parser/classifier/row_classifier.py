import re
from kepmendagri_parser.pipeline.context import RowType

def classify_row(code: str) -> RowType:
    if re.match(r"^\d{2}$", code):
        return RowType.PROVINCE

    if re.match(r"^\d{2}\.\d{2}$", code):
        return RowType.REGENCY

    if re.match(r"^\d{2}\.\d{2}\.\d{2}$", code):
        return RowType.DISTRICT

    if re.match(r"^\d{2}\.\d{2}\.\d{2}\.\d{4}$", code):
        return RowType.VILLAGE

    return RowType.OTHER
