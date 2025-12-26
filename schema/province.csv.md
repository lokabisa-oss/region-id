# Province CSV Schema

## File

data/kemendagri/province.csv

## Columns

| Column              | Type    | Required | Description                                 |
| ------------------- | ------- | -------- | ------------------------------------------- |
| code                | string  | yes      | Province code (2 digits, numeric)           |
| name                | string  | yes      | Official province name                      |
| area_km2            | number  | no       | Official total area (km²)                   |
| island_count        | integer | no       | Official number of islands                  |
| regency_count       | integer | no       | Number of regencies (kabupaten)             |
| city_count          | integer | no       | Number of cities (kota)                     |
| district_count      | integer | no       | Number of districts (kecamatan)             |
| village_count       | integer | no       | Total number of villages and urban villages |
| rural_village_count | integer | no       | Number of villages (desa)                   |
| urban_village_count | integer | no       | Number of urban villages (kelurahan)        |

## Rules

- `code` must be unique
- `code` must be numeric and length = 2
- Aggregate columns may be empty until derived from lower-level datasets
