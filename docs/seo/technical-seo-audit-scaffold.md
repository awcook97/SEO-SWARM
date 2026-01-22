# Technical SEO audit

## Purpose

Generate a technical SEO audit report from cached HTML plus live checks when available.

## Command

```bash
python scripts/generators/technical_seo_audit_scaffold.py --client-slug <client>
```

## Outputs

- `data/outputs/<client>/reports/technical-seo-audit.md`
- `data/outputs/<client>/reports/technical-seo-audit.json`

## Notes

- Uses cached HTML for titles, descriptions, canonicals, schema presence, and word-count checks.
- Attempts live checks for robots.txt, sitemap, and homepage response time when network access is available.
- Use the prioritized fixes section to assign owners and timelines.
