---
id: "202601180914-7D0M68"
title: "Simplify areaServed to string list"
status: "DONE"
priority: "P1"
owner: "ORCHESTRATOR"
depends_on: []
tags: ["schema", "seo", "automation"]
commit: { hash: "625a84eeab9b3cd2e5f26df59017801dc8ae3598", message: "📝 7D0M68 docs: verify areaServed string list output" }
comments:
  - { author: "ORCHESTRATOR", body: "Start: confirm cache schema generator emits areaServed as a list of strings (no Place objects) for LocalBusiness." }
  - { author: "ORCHESTRATOR", body: "verified: generator output now emits LocalBusiness.areaServed as a list of strings (confirmed on a fresh run to /tmp/schema-smoke-7d0m68 for clearlyamazing)." }
doc_version: 2
doc_updated_at: "2026-01-21T16:57:56+00:00"
doc_updated_by: "agentctl"
description: "Emit areaServed as list of strings instead of Place objects in cache schema generator."
---
# 202601180914-7D0M68: Simplify areaServed to string list

## Summary

- Emit `areaServed` as a simple list of strings for `LocalBusiness` instead of `Place` objects.

## Context

- Some validators and downstream tools treat `areaServed` string lists as the simplest, most compatible representation for service area labels.

## Scope

- Ensure `scripts/cache_schema_generator.py` assigns `areaServed` from approved inputs as `list[str]`.

## Risks

- If richer `Place` detail is later required (geo/address), it should be added intentionally and validated against schema.org ranges.

## Verify Steps

- `python3 scripts/cache_schema_generator.py --client-slug clearlyamazing --output-dir /tmp/schema-smoke-7d0m68`
- Confirm the generated JSON-LD `LocalBusiness.areaServed` values are strings (not objects) in `/tmp/schema-smoke-7d0m68/**/index.html`.

## Rollback Plan

- Revert the commit for this task and regenerate; compare `areaServed` representation in output HTML.

## Notes

- Repo-stored `outputs/**` may be stale relative to current generator behavior; use a fresh run for verification.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- (no file changes)
<!-- END AUTO SUMMARY -->

