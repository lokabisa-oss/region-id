# Data Sources

## Administrative Data (Codes & Hierarchy)

Primary source:

- **Ministry of Home Affairs (Kemendagri)**
  - Official administrative code publications
  - Legal basis for province, regency/city, district, and village codes

Secondary sources (for cross-checking and enrichment):

- **Statistics Indonesia (BPS)**
  - Administrative reference tables
  - Population and statistical context (where applicable)

Administrative data is treated as the **canonical source of truth**
for codes, names, and hierarchical relationships.

---

## Postal Codes (Reference Data)

- **PT Pos Indonesia**
  - Official postal code directory
  - Source: https://kodepos.posindonesia.co.id/

Postal codes are treated as **supplementary reference data** and:

- are **not** part of the administrative hierarchy
- are **not** used as canonical identifiers
- may map to one or more villages/areas depending on postal coverage

---

## Geospatial Boundaries (Geometry Only)

- **OpenStreetMap contributors**
- Extracted via **Geofabrik**
- License: **ODbL 1.0**

Geospatial data is used **only for boundary geometry** and
is not considered authoritative for administrative codes or hierarchy.
