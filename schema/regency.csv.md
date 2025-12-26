# Regency / City CSV Schema

## File

data/kemendagri/regency.csv

## Columns

| Column        | Type   | Required | Description                  |     |
| ------------- | ------ | -------- | ---------------------------- | --- |
| code          | string | yes      | Regency/City code (4 digits) |     |
| name          | string | yes      | Official name                |     |
| province_code | string | yes      | Parent province code         |     |
| type          | string | yes      | regency / city               |     |
| capital       | string | no       | Administrative capital       |     |
| area_km2      | number | no       | Official total area (km²)    |     |

## Rules

- `province_code` must exist in province.csv
- `type` must be one of: regency, city
