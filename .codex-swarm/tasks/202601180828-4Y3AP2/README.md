---
id: "202601180828-4Y3AP2"
title: "Improve geocode fallback + logging"
status: "DONE"
priority: "P1"
owner: "ORCHESTRATOR"
depends_on: []
tags: ["schema", "seo", "automation"]
commit: { hash: "7ef5c49c9f29000df32c858a72646fa318601907", message: "🧩 202601180828-4Y3AP2 integrate task/202601180828-4Y3AP2/geocode-fallback" }
comments:
  - { author: "INTEGRATOR", body: "verified: Integrated via squash | details: verify=skipped(no commands); pr=.codex-swarm/tasks/202601180828-4Y3AP2/pr." }
  - { author: "INTEGRATOR", body: "verified: Integrated via squash | details: verify=skipped(no commands); pr=.codex-swarm/tasks/202601180828-4Y3AP2/pr." }
doc_version: 2
doc_updated_at: "2026-01-18T08:28:37+00:00"
doc_updated_by: "agentctl"
description: "Add address variants and logging to geocoding so geo coordinates resolve and cache file is created."
---
## Summary

Expand geocoding fallback variants and add logging for cache hits and disabled geocoding.

## Scope

Update `scripts/cache_schema_generator.py` to try additional city/state variants and log cache hits and geocode skips.

## Risks

More geocode attempts can increase API usage; mitigate by honoring the cache and only enabling when `--geocode` is set.

## Verify Steps

1) Run `python scripts/cache_schema_generator.py --client-slug <client> --geocode`.
2) Confirm stderr logs cache hits and fallback attempts for missing coordinates.

## Rollback Plan

Revert the resolve_geo changes in `scripts/cache_schema_generator.py`.

## Notes

Variant normalization collapses extra whitespace to keep cache keys consistent.

