---
id: "202601180914-7D0M68"
title: "Simplify areaServed to string list"
status: "TODO"
priority: "P1"
owner: "ORCHESTRATOR"
depends_on: []
tags: ["schema", "seo", "automation"]
doc_version: 2
doc_updated_at: "2026-01-18T09:14:13+00:00"
doc_updated_by: "agentctl"
description: "Emit areaServed as list of strings instead of Place objects in cache schema generator."
---
## Summary

Normalize `areaServed` to a deduped list of strings.

## Scope

Update `scripts/cache_schema_generator.py` to coerce area values into plain strings before emitting schema.

## Risks

If inputs include malformed data, normalization may drop entries; mitigate by keeping only non-empty names.

## Verify Steps

1) Run `python scripts/cache_schema_generator.py --client-slug <client>`.
2) Confirm `areaServed` values are plain strings in LocalBusiness and Service nodes.

## Rollback Plan

Revert the `normalize_area_list` usage in `scripts/cache_schema_generator.py`.

## Notes

Dictionary entries (e.g., `{name: ...}`) are reduced to their `name` fields.
