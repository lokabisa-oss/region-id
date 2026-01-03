from dataclasses import dataclass
from kepmendagri_parser.pipeline.context import PageType

@dataclass
class PageResult:
    page: int
    content_type: PageType
