class Row:
    def __init__(self, code: str, name: str, raw: dict):
        self.code = code
        self.name = name
        self.raw = raw  # full row payload (columns)
