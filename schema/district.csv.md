# District CSV Schema

## File

data/kemendagri/district.csv

## Columns

| Column       | Type   | Required | Description              |
| ------------ | ------ | -------- | ------------------------ |
| code         | string | yes      | District code (6 digits) |
| name         | string | yes      | Official district name   |
| regency_code | string | yes      | Parent regency/city code |

## Rules

- `regency_code` must exist in regency.csv
