---
id: "202601180815-472897"
title: "Add logo image + geocoding to schema entities"
status: "DONE"
priority: "P1"
owner: "ORCHESTRATOR"
depends_on: []
tags: ["schema", "seo", "automation"]
commit: { hash: "c6f2b33d73580c7e14de2abcd0cc85c35825d193", message: "📝 472897 docs: verify logo image + geo enrichment" }
comments:
  - { author: "ORCHESTRATOR", body: "Start: confirm Organization/LocalBusiness include address + logo image and geo coordinates are hydrated via cached geocode (with optional geopy lookup)." }
  - { author: "ORCHESTRATOR", body: "verified: generator enriches Organization/LocalBusiness with address and logo image | details: LocalBusiness.geo is hydrated from outputs/<client>/reports/geocoded.json (confirmed on a fresh highpoint-hvac run to /tmp/schema-smoke-472897)." }
doc_version: 2
doc_updated_at: "2026-01-21T17:01:53+00:00"
doc_updated_by: "agentctl"
description: "Add Organization address, add logo image to Organization/LocalBusiness, and enrich LocalBusiness geo using geopy with caching."
---
# 202601180815-472897: Add logo image + geocoding to schema entities

## Summary

- Enrich `Organization` and `LocalBusiness` schema with address data, a logo image, and `geo` coordinates (when available).

## Context

- Basic business schema is more useful when it includes a consistent identifier set: name, url, address, and a representative image/logo.
- Geocoding can be sourced from a cached lookup file to avoid repeated external calls and to work offline.

## Scope

- `scripts/cache_schema_generator.py` extracts a logo URL from the homepage and assigns it as `image` on `Organization` and `LocalBusiness`.
- `scripts/cache_schema_generator.py` loads cached geocodes from `outputs/<client>/reports/geocoded.json` and assigns `LocalBusiness.geo` when present (with optional `geopy` lookup via `--geocode`).

## Risks

- Geocoding may be unavailable offline or without `geopy`; generator should degrade gracefully and omit `geo` rather than failing.

## Verify Steps

- `python3 scripts/cache_schema_generator.py --client-slug highpoint-hvac --output-dir /tmp/schema-smoke-472897`
- Confirm `/tmp/schema-smoke-472897/index.html` includes `Organization.image`, `LocalBusiness.image`, `Organization.address`, and `LocalBusiness.geo` (when cached geocode exists).

## Rollback Plan

- Revert the commit for this task and regenerate; confirm schema entities no longer include `image`/`geo` enrichment.

## Notes

- Keep geocode caching under `outputs/<client>/reports/geocoded.json` so runs can remain deterministic and offline-friendly.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- (no file changes)
<!-- END AUTO SUMMARY -->

