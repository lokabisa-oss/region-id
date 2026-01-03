def extract_page_table(page) -> list[any]:
    return page.extract_table() or []