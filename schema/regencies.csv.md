# Regency / City CSV Schema

## File

datasets/regencies.csv

## Description

Normalized dataset of Indonesian regencies (Kabupaten) and cities (Kota).

## Columns

| Column            | Type    | Required | Description                                 |
| ----------------- | ------- | -------- | ------------------------------------------- |
| code              | string  | yes      | Regency / city code (4 digits)              |
| province_code     | string  | yes      | Parent province code (2 digits)             |
| name              | string  | yes      | Official regency / city name                |
| type              | string  | yes      | `regency` or `city`                         |
| capital           | string  | no       | Administrative capital                      |
| is_administrative | boolean | no       | Administrative (non-autonomous) region flag |

## Rules

| Rule       | Description                                 |
| ---------- | ------------------------------------------- |
| Uniqueness | `code` must be unique                       |
| Integrity  | `province_code` must exist in provinces.csv |
| Type       | Must be `regency` or `city`                 |
| Capital    | Derived from district-level data            |

## Notes

Administrative cities are marked with `is_administrative = true`.
