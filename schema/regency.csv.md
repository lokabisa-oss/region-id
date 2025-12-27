# Regency / City CSV Schema

## File

data/kemendagri/regency.csv

## Columns

| Column              | Type    | Required | Description                              |
| ------------------- | ------- | -------- | ---------------------------------------- |
| code                | string  | yes      | Regency / City code (4 digits, numeric)  |
| name                | string  | yes      | Official regency / city name             |
| province_code       | string  | yes      | Parent province code (2 digits)          |
| type                | string  | yes      | Administrative type: `regency` or `city` |
| capital             | string  | no       | Administrative capital                   |
| area_km2            | number  | no       | Official total area (km²)                |
| district_count      | integer | no       | Number of districts (kecamatan)          |
| urban_village_count | integer | no       | Number of kelurahan                      |
| rural_village_count | integer | no       | Number of desa                           |
| village_count       | integer | no       | Total villages (kelurahan + desa)        |

### Identity & Hierarchy

- code must be unique
- code must be numeric and length = 4
- province_code must exist in province.csv
- type must be one of:
  - regency
  - city

### Aggregate Consistency

- village_count must equal:

```text
urban_village_count + rural_village_count
```

- `district_count`, `urban_village_count`, `rural_village_count`, `village_count` must be non-negative integers

### Cross-Level Validation (later stage)

- Sum of district_count per province must equal province.district_count
- Sum of village_count per province must equal province.village_count

---

### Notes

- Aggregate fields are derived from Kemendagri official data
- During extract phase, aggregate fields may be empty
- Aggregate fields are populated during transform phase
- Validation failures must stop the pipeline

### Design Rationale

- Keeps regency identity lightweight and stable
- Aggregates are optional but standardized
- Schema mirrors province.csv design for consistency
- Enables strict validation without requiring geospatial data

---
