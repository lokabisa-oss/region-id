# District CSV Schema

## File

datasets/districts.csv

## Description

Normalized dataset of Indonesian districts (Kecamatan).

## Columns

| Column       | Type   | Required | Description                |
| ------------ | ------ | -------- | -------------------------- |
| code         | string | yes      | District code (6 digits)   |
| regency_code | string | yes      | Parent regency / city code |
| name         | string | yes      | District name              |

## Rules

| Rule       | Description                                |
| ---------- | ------------------------------------------ |
| Uniqueness | `code` must be unique                      |
| Integrity  | `regency_code` must exist in regencies.csv |
| Format     | `code` must be numeric, length = 6         |
