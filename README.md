# id-wilayah-indonesia 🇮🇩

Reference dataset, geospatial boundaries, and API
for Indonesian administrative regions.

## Scope

This repository provides:

- Official administrative codes (BPS)
- Administrative boundaries (GeoJSON)
- Reproducible data pipeline
- Read-only public API

## Administrative Levels

- Country
- Province
- Regency / City
- District
- Village / Kelurahan

## Data Sources

- BPS (codes and naming)
- OpenStreetMap contributors (geometry)

## Structure

- `data/bps` — administrative codes (source of truth)
- `geojson` — final geospatial boundaries
- `pipeline` — reproducible data pipeline
- `public/api` — static API output (GitHub Pages)
- `api` — optional runtime API (Cloudflare Workers)

## License

- Code & pipeline: MIT
- Geospatial data: ODbL (derived from OpenStreetMap)
