---
id: "202601180753-2MBGAS"
title: "Refine schema types + per-service offers"
status: "TODO"
priority: "P1"
owner: "ORCHESTRATOR"
depends_on: []
tags: ["schema", "seo", "automation"]
doc_version: 2
doc_updated_at: "2026-01-18T07:53:48+00:00"
doc_updated_by: "agentctl"
description: "Switch LocalBusiness to HVACBusiness, replace serviceOffered with makesOffer, and limit offers to matching service pages."
---
## Summary

Refine schema output to use HVACBusiness and per-page Service offers linked via `@id`.

## Scope

Update `scripts/cache_schema_generator.py` to emit Service nodes and reference them from `makesOffer` on matching service pages, with homepage offers listing all services.

## Risks

Service nodes depend on service names; missing names would drop offers. Mitigate by skipping unnamed services and keeping existing schema intact otherwise.

## Verify Steps

1) Run `python scripts/cache_schema_generator.py --client-slug <client>` for a sample client.
2) Confirm service pages include only their matching offer and homepage includes all service offers.

## Rollback Plan

Revert changes in `scripts/cache_schema_generator.py` and regenerate schema outputs.

## Notes

Service nodes are linked via `@id` to reduce duplication across offers.
