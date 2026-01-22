---
id: "202601220109-0G2X3H"
title: "Allow optional LocalBusiness subtype from inputs"
status: "DOING"
priority: "P1"
owner: "ORCHESTRATOR"
depends_on: []
tags: ["schema", "automation"]
comments:
  - { author: "Codex", body: "Start: Implement optional business type input for LocalBusiness schema." }
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
