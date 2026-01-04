def split_cell(cell):
    if not cell:
        return []
    return [x.strip() for x in cell.split("\n") if x.strip()]


def extract_provinces_from_table(table, page_num):
    rows = []

    for row in table[1:]:
        if not row or len(row) < 3:
            continue

        codes = split_cell(row[1])
        names = split_cell(row[2])

        if not codes or not names:
            continue

        # remaining columns = aggregates
        aggregates = [split_cell(c) for c in row[3:]]

        for i, code in enumerate(codes):
            if not code.isdigit() or len(code) != 2:
                continue

            try:
                rows.append(
                    {
                        "code": code,
                        "name": names[i],
                        "island_count": aggregates[7][i],
                        "source_page": page_num,
                    }
                )
            except IndexError:
                continue

    return rows
