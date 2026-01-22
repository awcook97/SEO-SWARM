---
id: "202601180815-472897"
title: "Add logo image + geocoding to schema entities"
status: "TODO"
priority: "P1"
owner: "ORCHESTRATOR"
depends_on: []
tags: ["schema", "seo", "automation"]
doc_version: 2
doc_updated_at: "2026-01-18T08:15:45+00:00"
doc_updated_by: "agentctl"
description: "Add Organization address, add logo image to Organization/LocalBusiness, and enrich LocalBusiness geo using geopy with caching."
---
## Summary

Add explicit `logo` properties for Organization and LocalBusiness schema nodes.

## Scope

Update `scripts/cache_schema_generator.py` to emit `logo` alongside `image` for Organization and LocalBusiness.

## Risks

If `logo_url` is empty, the property should remain absent; ensure nulls are pruned.

## Verify Steps

1) Run `python scripts/cache_schema_generator.py --client-slug <client>`.
2) Confirm Organization and LocalBusiness include `logo` when a logo URL is detected.

## Rollback Plan

Revert the `logo` property additions in `scripts/cache_schema_generator.py`.

## Notes

Address and geo enrichment are already present; this change focuses on the `logo` field.
