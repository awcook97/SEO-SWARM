# Cache schema generator

Generate a single JSON-LD `<script>` per cached page, built from on-page signals
and aligned with Google Search appearance guidance (JSON-LD, single script per
page, visible content parity, and required fields where available).

## Inputs

- `outputs/<client>/reports/site-cache/index.json` created by @scripts/crawl_cache.py.
- Cached HTML snapshots referenced by the index.
- Approved inputs via `outputs/<client>/reports/gbp-update-checklist.json` (preferred)
  or `outputs/<client>/inputs.md` (fallback) to hydrate Organization/LocalBusiness.

## Command

```bash
python scripts/cache_schema_generator.py --client-slug <client>
```

## Output

- `outputs/<client>/gen-schema/website-tree/**/index.html` (or `.html` per page path)
  containing a single JSON-LD `<script>` tag for each cached page.
