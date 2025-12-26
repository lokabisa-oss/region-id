# Postal Code Mapping Schema

## File

data/postal/postal_code.csv

## Description

Mapping between postal codes and administrative areas.
Postal codes are treated as reference data and are not part of the administrative hierarchy.

## Columns

| Column        | Type   | Required | Description                                |
| ------------- | ------ | -------- | ------------------------------------------ |
| postal_code   | string | yes      | Indonesian postal code (5 digits)          |
| village_code  | string | no       | Related village/kelurahan code (10 digits) |
| district_code | string | no       | Related district code (6 digits)           |
| regency_code  | string | no       | Related regency/city code (4 digits)       |
| province_code | string | no       | Related province code (2 digits)           |
| source        | string | yes      | Data source (e.g. posindonesia)            |

## Rules

- `postal_code` must be a 5-digit numeric string
- At least one of `village_code`, `district_code`, `regency_code`, or `province_code` MUST be present
- Codes must exist in their respective administrative CSV files
- `postal_code` is NOT unique
- Combination of (`postal_code`, `village_code`) SHOULD be unique when village_code is present
