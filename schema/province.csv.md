# Province CSV Schema

## File

datasetsprovince.csv

## Columns

| Column  | Type   | Required | Description                       |
| ------- | ------ | -------- | --------------------------------- |
| code    | string | yes      | Province code (2 digits, numeric) |
| name    | string | yes      | Official province name            |
| capital | string | no       | Administrative capital            |

## Rules

- `code` must be unique
- `code` must be numeric and length = 2
- Aggregate columns may be empty until derived from lower-level datasets
