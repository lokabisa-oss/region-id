# Province Metadata JSON Schema

## File

metadata/province_metadata.json

---

## Root Object

| Field        | Type   | Required | Description                  |
| ------------ | ------ | -------- | ---------------------------- |
| version      | string | yes      | Metadata schema version      |
| source       | string | yes      | Legal / institutional source |
| last_updated | string | yes      | ISO date (`YYYY-MM-DD`)      |
| provinces    | object | yes      | Province metadata map        |

---

## Provinces Object

Keyed by **province code (2 digits)**.

```json
"provinces": {
  "31": { ... },
  "34": { ... }
}
```

---

## Province Entry

| Field                 | Type    | Required    | Description                             |
| --------------------- | ------- | ----------- | --------------------------------------- |
| name                  | string  | yes         | Official province name                  |
| is_special_region     | boolean | yes         | Indicates special administrative status |
| special_region_reason | string  | conditional | Required if `is_special_region = true`  |
| notes                 | string  | no          | Human-readable explanation              |

---

### `special_region_reason` Values

| Value               | Description                   |
| ------------------- | ----------------------------- |
| capital_city        | National capital region       |
| historical_monarchy | Monarchy-based special status |
| special_autonomy    | Special autonomy by law       |
| custom_governance   | Other special governance      |

---

### Constraints

- province_code must exist in provinces.csv
- If is_special_region = true, special_region_reason is required
- No structural or hierarchical data allowed

---

### Design Notes

- Metadata is separated from datasets
- Values are legal-based and stable
- Intended for flags, policy logic, and UI behavior
