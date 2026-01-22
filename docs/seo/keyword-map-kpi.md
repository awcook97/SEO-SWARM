# Keyword map + KPI targets

## Purpose

Create a keyword-to-URL map and define KPI targets for reporting cadence.

## Inputs

- `data/outputs/<client>/reports/keyword-map-input.json`

## Command

```bash
python scripts/keyword_map_kpi.py --client-slug <client>
```

Scaffold an input file if needed:

```bash
python scripts/keyword_map_kpi.py --client-slug <client> --scaffold
```

## Outputs

- `data/outputs/<client>/reports/keyword-map-kpi.md`
- `data/outputs/<client>/reports/keyword-map-kpi.json`

## Notes

- Fill in KPI targets with approved goals and cadence.
- Map each keyword to a target URL and intent.
