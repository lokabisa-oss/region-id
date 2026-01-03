from classifier.row_classifier import classify_row
from kepmendagri_parser.pipeline.context import RowType

def process_rows(rows, page_type, state):

    for row in rows:
        row_type = classify_row(row.code)

        if row_type == RowType.PROVINCE:
            state.current_province = row
            state.current_regency = None
            state.current_district = None

        elif row_type == RowType.REGENCY:
            state.current_regency = row
            state.current_district = None

        elif row_type == RowType.DISTRICT:
            state.current_district = row

        elif row_type == RowType.VILLAGE:
            pass  # no state change

        # emit handled elsewhere
