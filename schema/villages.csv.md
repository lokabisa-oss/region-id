# Village CSV Schema

## File

datasets/villages.csv

## Description

Normalized dataset of villages (Desa) and urban villages (Kelurahan).

## Columns

| Column        | Type   | Required | Description                  |
| ------------- | ------ | -------- | ---------------------------- |
| code          | string | yes      | Village code (10 digits)     |
| district_code | string | yes      | Parent district code         |
| name          | string | yes      | Village name                 |
| type          | string | yes      | `village` or `urban_village` |

## Rules

| Rule       | Description                                 |
| ---------- | ------------------------------------------- |
| Uniqueness | `code` must be unique                       |
| Integrity  | `district_code` must exist in districts.csv |
| Type       | Must be `village` or `urban_village`        |
