---
id: "202601180753-2MBGAS"
title: "Refine schema types + per-service offers"
status: "DONE"
priority: "P1"
owner: "ORCHESTRATOR"
depends_on: []
tags: ["schema", "seo", "automation"]
commit: { hash: "4d2ab79c5b0dcb6a26f5756f525cdb15b3461105", message: "📝 2MBGAS docs: verify HVACBusiness + per-service makesOffer" }
comments:
  - { author: "ORCHESTRATOR", body: "Start: confirm generator uses HVACBusiness + makesOffer and limits offers to the matching service page (all offers only on homepage)." }
  - { author: "ORCHESTRATOR", body: "verified: generator emits LocalBusiness as [HVACBusiness, LocalBusiness] and uses makesOffer | details: on a highpoint-hvac run, homepage included 12 offers and air-duct-services page included only the matching service offer." }
doc_version: 2
doc_updated_at: "2026-01-21T17:00:24+00:00"
doc_updated_by: "agentctl"
description: "Switch LocalBusiness to HVACBusiness, replace serviceOffered with makesOffer, and limit offers to matching service pages."
---
# 202601180753-2MBGAS: Refine schema types + per-service offers

## Summary

- Use `HVACBusiness` (alongside `LocalBusiness`) for the business entity and emit per-page offers via `makesOffer`.
- Limit `makesOffer` to the matching service on service pages, while allowing the homepage to list all services.

## Context

- Large “serviceOffered” lists on every page can be noisy; limiting offers to relevant pages improves parity with on-page intent and reviewability.

## Scope

- `scripts/cache_schema_generator.py` uses `@type: ["HVACBusiness","LocalBusiness"]` for the business entity.
- Replace broad `serviceOffered` usage with `makesOffer` and match offers to service page URLs via slug-based matching.

## Risks

- Offer matching is heuristic (slug containment). If URLs or service names change, offers may not attach as expected.

## Verify Steps

- `python3 scripts/cache_schema_generator.py --client-slug highpoint-hvac --output-dir /tmp/schema-smoke-2mbgas`
- Confirm `/tmp/schema-smoke-2mbgas/index.html` includes all service offers, while `/tmp/schema-smoke-2mbgas/air-duct-services.html` includes only `Air Duct Services`.

## Rollback Plan

- Revert the commit for this task and regenerate the same sample; compare `LocalBusiness.makesOffer` behavior on homepage vs service pages.

## Notes

- Keep offers limited to what is supported by approved inputs (`outputs/<client>/inputs.md` or GBP checklist).

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- (no file changes)
<!-- END AUTO SUMMARY -->

