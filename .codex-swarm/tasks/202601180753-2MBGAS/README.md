---
id: "202601180753-2MBGAS"
title: "Refine schema types + per-service offers"
status: "DONE"
priority: "P1"
owner: "ORCHESTRATOR"
depends_on: []
tags: ["schema", "seo", "automation"]
commit: { hash: "ec459f94bd6cfa244e2b036c0e585f73e35b704b", message: "🧩 202601180753-2MBGAS integrate task/202601180753-2MBGAS/schema-offers" }
comments:
  - { author: "INTEGRATOR", body: "verified: Integrated via squash | details: verify=skipped(no commands); pr=.codex-swarm/tasks/202601180753-2MBGAS/pr." }
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

