# Village / Kelurahan CSV Schema

## File

dataset/village.csv

## Columns

| Column        | Type   | Required | Description              |
| ------------- | ------ | -------- | ------------------------ |
| code          | string | yes      | Village code (10 digits) |
| name          | string | yes      | Official village name    |
| district_code | string | yes      | Parent district code     |
| type          | string | yes      | desa / kelurahan         |

## Rules

- `district_code` must exist in district.csv
- `type` must be one of: desa, kelurahan
