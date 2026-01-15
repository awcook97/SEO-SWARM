# Metadata + internal link map spec

This spec defines a tool-agnostic input and output format for generating metadata drafts and internal link maps for page plans.

## Input JSON

Store the input file at: `outputs/<client>/reports/metadata-linkmap-input.json`.

```json
{
  "client": {
    "name": "Client Name",
    "phone": "(000) 000-0000",
    "website": "https://example.com"
  },
  "defaults": {
    "contact_url": "/contact",
    "service_hub_url": "/services",
    "maintenance_url": "/maintenance",
    "service_pages": {
      "Service Name": "/services/service-slug"
    }
  },
  "pages": [
    {
      "id": "optional-id",
      "type": "service-page",
      "slug": "service-slug",
      "service": "Service Name",
      "primary_keyword": "service keyword",
      "related_services": ["Other Service"],
      "service_area_links": ["/service-areas/city"],
      "include_faq_schema": true,
      "internal_links": [
        {"label": "Blog", "url": "/blog", "type": "supporting"}
      ]
    }
  ]
}
```

### Supported page types

- `local-landing` (requires `service`, `city`)
- `service-page` (requires `service`)
- `service-area-article` (requires `service`, `city`)
- `topical-guide` (requires `topic`)

Optional fields:

- `proof_point`: appended to the meta description.
- `related_services`: list of service names resolved via `defaults.service_pages`.
- `service_area_links`: list of URLs for service-area pages.
- `internal_links`: additional internal links with `label`, `url`, and optional `type`.

## Output files

The generator writes two files under `outputs/<client>/reports/`:

- `metadata-internal-link-map.json`: structured output for downstream tools.
- `metadata-internal-link-map.md`: human-readable summary.

## Generator usage

```bash
python scripts/metadata_internal_link_map.py --client-slug <client>
```

Optional: specify a different input filename under `outputs/<client>/reports/` via `--input`.

## Output JSON fields

```json
{
  "generated_at": "2026-01-15T00:00:00+00:00",
  "client": {"name": "Client Name", "phone": "(000) 000-0000", "website": "https://example.com"},
  "pages": [
    {
      "id": "service-slug",
      "type": "service-page",
      "slug": "service-slug",
      "inputs": {
        "service": "Service Name",
        "city": null,
        "topic": null,
        "primary_keyword": "service keyword"
      },
      "metadata": {
        "title_tag": "Service Name | Client Name",
        "meta_description": "Service Name with Client Name. Call (000) 000-0000.",
        "schema_types": ["Service", "LocalBusiness", "FAQPage"]
      },
      "internal_links": [
        {"label": "Contact", "url": "/contact", "type": "contact"}
      ],
      "missing_links": [],
      "errors": []
    }
  ]
}
```

## Notes

- Missing required fields are reported under `errors` for each page entry.
- Missing internal link targets (no URL available) are listed under `missing_links`.
- Use only approved inputs when populating `client` and `pages`.
