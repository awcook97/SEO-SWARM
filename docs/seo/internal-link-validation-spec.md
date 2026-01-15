# Internal link validation spec

This spec defines how to validate internal link targets using the metadata + internal link map output.

## Inputs

- `outputs/<client>/reports/metadata-internal-link-map.json`

## Generator usage

```bash
python scripts/internal_link_validator.py --client-slug <client>
```

## Output files

- `outputs/<client>/reports/internal-link-validation.json`
- `outputs/<client>/reports/internal-link-validation.md`

## Required link types by page type

- `local-landing`: related-service, service-hub, contact
- `service-page`: related-service, service-area, maintenance
- `service-area-article`: service-page, contact
- `topical-guide`: service-page, contact

## Issue types

- `page-error`: page entry has errors from the link map generation step.
- `missing-target`: a link target was listed in `missing_links` (no URL available).
- `missing-required`: required link type is absent from `internal_links`.
- `placeholder-url`: URL contains placeholder markers (e.g., `[CONTACT_URL]`, TODO).

## Output JSON shape

```json
{
  "generated_at": "2026-01-15T00:00:00+00:00",
  "client": {"name": "Client Name"},
  "summary": {"total": 3, "failed": 1, "passed": 2},
  "results": [
    {
      "id": "service-slug",
      "type": "service-page",
      "status": "pass",
      "issues": []
    }
  ]
}
```
