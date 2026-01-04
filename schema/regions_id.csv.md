# Regions ID (Denormalized) CSV Schema

## File

datasets/regions_id.csv

## Description

Fully denormalized administrative hierarchy at village level.

## Columns

| Column           | Type   | Required | Description                    |
| ---------------- | ------ | -------- | ------------------------------ |
| province_code    | string | yes      | Province code (2 digits)       |
| province_name    | string | yes      | Province name                  |
| province_capital | string | no       | Province capital               |
| regency_code     | string | yes      | Regency / city code (4 digits) |
| regency_name     | string | yes      | Regency / city name            |
| regency_type     | string | yes      | `regency` or `city`            |
| regency_capital  | string | no       | Regency Capital                |
| district_code    | string | yes      | District code (6 digits)       |
| district_name    | string | yes      | District name                  |
| village_code     | string | yes      | Village code (10 digits)       |
| village_name     | string | yes      | Village name                   |
| village_type     | string | yes      | `village` or `urban_village`   |

## Rules

| Rule        | Description                            |
| ----------- | -------------------------------------- |
| Uniqueness  | `village_code` must be unique          |
| Integrity   | All hierarchy resolved during build    |
| Granularity | One row represents exactly one village |

## Purpose

Optimized for API usage, analytics, and direct database import.
