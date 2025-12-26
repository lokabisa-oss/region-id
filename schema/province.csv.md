# Province CSV Schema

## File

data/kemendagri/province.csv

## Columns

| Column       | Type    | Required | Description                       |
| ------------ | ------- | -------- | --------------------------------- |
| code         | string  | yes      | Province code (2 digits, numeric) |
| name         | string  | yes      | Official province name            |
| area_km2     | number  | no       | Official total area (km²)         |
| island_count | integer | no       | Official number of islands        |

## Rules

- `code` must be unique
- `code` must be numeric and length = 2
