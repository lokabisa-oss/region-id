# region-id

Open reference dataset and geospatial boundaries for Indonesian administrative regions.

This project provides structured, authoritative, and extensible data for Indonesian regions — from province to village — designed for developers, researchers, civic tech, and public-interest projects.

---

## ✨ Features

- Complete Indonesian administrative hierarchy:
  - Province
  - Regency / City
  - District
  - Village
- Official administrative boundaries (GeoJSON)
- Normalized datasets in **JSON and CSV**
- Postal codes (Kode Pos)
- Vehicle license plate region codes (Kode Plat Nomor)
- Clear data sources and attribution
- Designed for long-term maintenance and extension

---

## 📂 Repository Structure

```text
region-id/
├─ data/
│  ├─ json/
│  └─ csv/
├─ geojson/
│   └─ big/
├─ schema/
├─ pipeline/
├─ metadata/
├─ examples/
├─ README.md
├─ LICENSE
```

---

## 📊 Data Coverage

| Dataset                | Status   |
| ---------------------- | -------- |
| Province               | ✅       |
| Regency / City         | ✅       |
| District               | ✅       |
| Village                | ✅       |
| Geospatial Boundary    | ✅ (BIG) |
| Postal Code (Kode Pos) | ✅       |
| Vehicle Plate Code     | ✅       |

---

## 📚 Data Sources

This project is built from official and verifiable public references.

### Administrative Boundaries

Badan Informasi Geospasial (BIG)
Official source for Indonesian administrative boundary geometries
(province to village level).

### Administrative Codes & References

Ministry of Home Affairs (Kemendagri)

Statistics Indonesia (BPS)

### Postal Codes

- Pos Indonesia

  Postal code reference data obtained from https://kodepos.posindonesia.co.id/

### Vehicle License Plate Codes

Publicly documented regional vehicle plate code references
aligned with Indonesian administrative regions.

Detailed dataset references, versions, and notes are documented in the `metadata/` directory.

---

## 🧩 Extensibility

The project is intentionally named region-id to support future dataset extensions such as:

- Additional postal and logistics identifiers
- Transportation and regional mobility codes
- Statistical and demographic indicators
- Additional geospatial layers

---

## 📜 License

### Code

MIT License

### Data & Content

- Administrative boundary geometries are derived from public datasets published by **Badan Informasi Geospasial (BIG)**.
- Postal code data is referenced from Pos Indonesia public information.
- Vehicle plate code mappings are derived from publicly available regional references.

Usage of data is subject to the terms, attribution, and redistribution rules defined by the original data providers.

Refer to the `metadata/` directory for dataset-specific notes.

## 🤝 Contributing

Contributions are welcome.

You can help by:

- Improving data accuracy
- Adding or verifying references
- Enhancing schemas or validation
- Improving data processing pipelines or documentation

Contribution guidelines will be added in CONTRIBUTING.md.

## 🏷️ Project Status

- Status: Active
- Type: Open Source Dataset
- Scope: Indonesian regional reference data
- Maintained by: Lokabisa OSS

## 🌐 About Lokabisa OSS

Lokabisa OSS is an open-source initiative focused on public reference datasets, regional infrastructure, and developer tools for communities and local ecosystems in Indonesia.

Website: https://oss.lokabisa.id
