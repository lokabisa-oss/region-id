def extract_page_text(page) -> str:
    return page.extract_text() or ""
