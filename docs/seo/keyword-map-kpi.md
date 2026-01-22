# Keyword map + KPI targets

## Purpose

Create a keyword-to-URL map and define KPI targets for reporting cadence.

## Inputs

- `data/outputs/<client>/reports/keyword-map-input.json`

## Command

```bash
python scripts/generators/keyword_map_kpi.py --client-slug <client>
```

Scaffold an input file if needed:

```bash
python scripts/generators/keyword_map_kpi.py --client-slug <client> --scaffold
```

Auto-extract keywords from cached HTML (uses RAKE + textstat):

```bash
python scripts/generators/keyword_map_kpi.py --client-slug <client> --auto-from-cache
```

Dependencies for auto-extraction: `rake_nltk`, `textstat`, and `beautifulsoup4`.

## Outputs

- `data/outputs/<client>/reports/keyword-map-kpi.md`
- `data/outputs/<client>/reports/keyword-map-kpi.json`

## Notes

- Fill in KPI targets with approved goals and cadence.
- Map each keyword to a target URL and intent.
