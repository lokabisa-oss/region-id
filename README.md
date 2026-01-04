<p align="center">
  <img src="https://raw.githubusercontent.com/lokabisa-oss/region-id/main/metadata/og-region-id.png" alt="region-id — Indonesian Administrative Regions Dataset" width="100%" />
</p>

<p align="center">
  <a href="https://github.com/lokabisa-oss/region-id/releases">
    <img src="https://img.shields.io/github/v/release/lokabisa/region-id?style=flat-square" alt="Latest Release">
  </a>
  <a href="https://github.com/lokabisa-oss/region-id">
    <img src="https://img.shields.io/github/repo-size/lokabisa/region-id?style=flat-square" alt="Repo Size">
  </a>
  <a href="https://github.com/lokabisa-oss/region-id/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/lokabisa/region-id?style=flat-square" alt="License">
  </a>
  <a href="https://github.com/lokabisa-oss/region-id/commits/main">
    <img src="https://img.shields.io/github/last-commit/lokabisa/region-id?style=flat-square" alt="Last Commit">
  </a>
</p>

# region-id

Reference datasets for Indonesian administrative regions.

This repository provides **validated reference datasets** for Indonesian administrative divisions, generated from official sources and published as **versioned release artifacts**.

The repository itself does **not store dataset files directly**.  
All datasets are distributed via **GitHub Releases** to keep the repository clean, versioned, and reproducible.

---

## Administrative Coverage

The datasets follow the official Indonesian administrative hierarchy:

1. Province
2. Regency / City
3. District
4. Village

A denormalized dataset is also provided for convenience.

---

## 📄 Spreadsheet Preview

For quick browsing and human-friendly inspection, a public Google Spreadsheet
version of the dataset is available:

👉 https://docs.google.com/spreadsheets/d/1fWEIztD397_9uG4ZvAuv9IX43ek9gNvlRuykpwza9_I

**Note:**  
This spreadsheet is a read-only preview.  
The authoritative and versioned datasets are published via GitHub Releases.

---

## 📦 Download Datasets

All datasets are published as versioned release assets.

👉 **Download latest release:**  
https://github.com/lokabisa-oss/region-id/releases/latest

Each release contains ready-to-use CSV files.

---

## Available Datasets

All datasets are published as CSV files in GitHub Releases.

| Dataset        | File             | Description                                    | Records |
| -------------- | ---------------- | ---------------------------------------------- | ------- |
| Province       | `provinces.csv`  | Indonesian provinces                           | 38      |
| Regency / City | `regencies.csv`  | Regencies (Kabupaten) and Cities (Kota)        | 514     |
| District       | `districts.csv`  | District-level administrative units            | 7,285   |
| Village        | `villages.csv`   | Villages and urban villages (Desa / Kelurahan) | 83,762  |
| Denormalized   | `regions_id.csv` | Flattened province → village reference         | 83,762  |

Each dataset is versioned and validated before release.

---

## Dataset Format

- Primary format: **CSV**
- Encoding: UTF-8
- Stable schemas documented in the `schema/` directory

Schemas are versioned independently from dataset releases.

---

## Data Integrity Guarantees

All released datasets are built with strict validation:

- Unique codes at every administrative level
- Valid foreign-key relationships across levels
- One-to-one hierarchy consistency
- Denormalized data generated only from validated normalized datasets

If validation fails, the dataset is **not released**.

---

## Data Sources

The datasets are derived from official and publicly verifiable references, including:

- Ministry of Home Affairs (Kemendagri)

Source details, legal notes, and special-region metadata are documented in the `metadata/` directory.

---

## Repository Purpose

This repository serves as:

- A **dataset generator**
- A **schema authority**
- A **validation pipeline**
- A **reference implementation** for Indonesian region identifiers

It is intentionally kept free from large data files.

---

## 🔁 Reproducing the Dataset Locally

This repository includes a complete pipeline to **reproduce the datasets from source documents**.

Reproducing the dataset is **optional** and intended for:

- Auditing and verification
- Research and reference
- Contributing improvements to the pipeline

Most users should download the ready-to-use datasets from **GitHub Releases**.

### Requirements

- Python 3.10+
- `pdfplumber`
- Other dependencies listed in `requirements.txt`

### Steps

Clone the repository:

```bash
git clone https://github.com/lokabisa-oss/region-id.git
cd region-id
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the pipeline:

```bash
python -m kepmendagri_parser \
  --input kepmendagri-2025.pdf \
  --output ./datasets
```

The pipeline will:

1. Parse official source documents
2. Normalize administrative hierarchies
3. Validate all relationships and codes
4. Generate final CSV datasets
5. Abort if validation fails

### Output

The generated datasets will be written to:

```text
./datasets/
├── provinces.csv
├── regencies.csv
├── districts.csv
├── villages.csv
└── regions_id.csv
```

Generated outputs should match the corresponding GitHub Release for the same version.

---

### Source Document (Kepmendagri PDF)

The dataset is generated from the official **Kepmendagri administrative reference document**.

You can obtain the source PDF from one of the following locations:

- **Archived release (recommended for reproducibility):**  
  https://github.com/lokabisa-oss/id-documents/releases/download/kepmendagri-2025/kepmendagri-2025.pdf

- **Original source references:**  
  Official publication links are documented in  
  `metadata/sources.md`

Using the archived release is recommended to ensure that the dataset can be reproduced **exactly** as published in the corresponding GitHub Release.
