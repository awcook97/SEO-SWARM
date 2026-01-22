# Schema approval workflow (schema.org strict)

Use the schema.org snapshot in `@data/downloads/schemaorg-current-https.jsonld`
as the canonical reference for allowed classes, properties, and ranges.

## Goal

Produce per-page JSON-LD that is valid against schema.org and matches the page
content. Avoid bulk generation without review.

## Steps

1) Start from the boilerplate
- Copy `@docs/seo/schema-boilerplate.jsonld` and fill in the page-specific values.

2) Validate against schema.org
- Run:
  - `python scripts/validation/schema_org_validator.py --input <path-to-jsonld-or-html>`
- Fix any validation errors (unknown types/properties or invalid ranges).

3) Spotcheck against the page
- Confirm title, description, canonical URL, FAQ content, and images match the
  visible page content and approved inputs.

4) Approval
- Record approval only after validation and spotcheck pass.

## Search appearance checklist

- One JSON-LD `<script>` per page; combine entities with `@graph` when needed.
- Keep schema types aligned with visible page intent (no extra types for other pages).
- Avoid duplicate entities on a single page (reuse `@id` references).
- Use absolute URLs for `@id`, `url`, image references, and `sameAs`.
- Include only verified, page-visible content (titles, descriptions, FAQs, offers).

## Notes

- Prefer explicit `@id` values and consistent identifiers for `WebSite`,
  `Organization`, and `LocalBusiness` entities across pages.
- Use only schema.org properties listed in the snapshot file.
