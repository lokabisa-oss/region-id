# Province CSV Schema

## File

datasets/provinces.csv

## Description

Normalized dataset of Indonesian provinces.

## Columns

| Column  | Type   | Required | Description              |
| ------- | ------ | -------- | ------------------------ |
| code    | string | yes      | Province code (2 digits) |
| name    | string | yes      | Official province name   |
| capital | string | no       | Provincial capital       |

## Rules

| Rule       | Description                        |
| ---------- | ---------------------------------- |
| Uniqueness | `code` must be unique              |
| Format     | `code` must be numeric, length = 2 |
| Capital    | Derived from district-level data   |

## Notes

Special-region metadata is stored separately in `province_metadata.json`.
