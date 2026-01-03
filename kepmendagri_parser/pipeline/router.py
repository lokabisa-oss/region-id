from kepmendagri_parser.pipeline.context import PageType

PARSER_BY_PAGE_TYPE = {
    PageType.PROVINSI: "province",
    PageType.KAB_KOTA: "regency",
    PageType.KECAMATAN: "district",
    PageType.KELURAHAN_DESA: "village",
}
