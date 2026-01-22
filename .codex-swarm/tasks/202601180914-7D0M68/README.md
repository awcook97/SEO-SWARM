---
id: "202601180914-7D0M68"
title: "Simplify areaServed to string list"
status: "DONE"
priority: "P1"
owner: "ORCHESTRATOR"
depends_on: []
tags: ["schema", "seo", "automation"]
commit: { hash: "6b8476cfec2b6f64e6a9d253820666fd3fc6d688", message: "🧩 202601180914-7D0M68 integrate task/202601180914-7D0M68/area-served" }
comments:
  - { author: "INTEGRATOR", body: "verified: Integrated via squash | details: verify=skipped(no commands); pr=.codex-swarm/tasks/202601180914-7D0M68/pr." }
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

