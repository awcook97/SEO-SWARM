---
id: "202601220109-0G2X3H"
title: "Allow optional LocalBusiness subtype from inputs"
status: "DONE"
priority: "P1"
owner: "ORCHESTRATOR"
depends_on: []
tags: ["schema", "automation"]
commit: { hash: "31d54a7fc7b5951dbf6abd9f7ad272404de3f83a", message: "🧩 202601220109-0G2X3H integrate task/202601220109-0G2X3H/business-type" }
comments:
  - { author: "Codex", body: "Start: Implement optional business type input for LocalBusiness schema." }
  - { author: "INTEGRATOR", body: "verified: Integrated via squash | details: verify=skipped(no commands); pr=.codex-swarm/tasks/202601220109-0G2X3H/pr." }
  - { author: "INTEGRATOR", body: "verified: Integrated via squash | details: verify=skipped(no commands); pr=.codex-swarm/tasks/202601220109-0G2X3H/pr." }
doc_version: 2
doc_updated_at: "2026-01-22T01:09:29+00:00"
doc_updated_by: "agentctl"
description: "Support optional business type in inputs.md/GBP inputs to extend LocalBusiness @type list in cache schema generator."
---
## Summary

Allow optional schema.org business subtypes to extend LocalBusiness `@type` values.

## Scope

Add business type parsing for inputs.md and GBP inputs, then apply it when building LocalBusiness schema types.

## Risks

Invalid schema.org types could be provided; output still includes `LocalBusiness` as a safe base type.

## Verify Steps

1) Add `Business type: HVACBusiness` to `outputs/<client>/inputs.md`.
2) Run `python scripts/cache_schema_generator.py --client-slug <client>`.
3) Confirm LocalBusiness `@type` includes both `LocalBusiness` and the subtype.

## Rollback Plan

Revert business type parsing and `@type` construction in `scripts/cache_schema_generator.py`.

## Notes

Comma-separated subtypes are supported in inputs.

