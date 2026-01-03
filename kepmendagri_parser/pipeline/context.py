from enum import Enum

class PageType(str, Enum):
    PROVINSI = "provinsi"
    KAB_KOTA = "kab_kota"
    KECAMATAN = "kecamatan"
    KELURAHAN_DESA = "kelurahan_desa"
    UNKNOWN = "unknown"


class RowType(str, Enum):
    PROVINCE = "province"
    REGENCY = "regency"
    DISTRICT = "district"
    VILLAGE = "village"
    OTHER = "other"
