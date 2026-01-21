---
id: "202601211646-VBPK9P"
title: "Execute all schema-tagged tasks"
status: "DONE"
priority: "P1"
owner: "ORCHESTRATOR"
depends_on: []
tags: ["schema", "orchestration"]
commit: { hash: "6126a46a1dd1eb7d24cc34abcad19d39d78980e9", message: "📝 VBPK9P docs: record schema backlog completion and verification" }
comments:
  - { author: "ORCHESTRATOR", body: "Start: close the schema-tagged backlog and record verification results across tasks (schema validator spotcheck + pytest)." }
  - { author: "ORCHESTRATOR", body: "verified: all tasks previously tagged schema are now DONE | details: ran schema validator spotcheck and ran python3 -m pytest (29 passed) to confirm baseline stays green." }
doc_version: 2
doc_updated_at: "2026-01-21T16:47:17+00:00"
doc_updated_by: "agentctl"
description: "Tracking task for executing the current backlog of tasks tagged 'schema' in direct workflow. Planned execution order: 202601180735-Y4CG1A (schemaorg reference/workflow), 202601180617-99GCXY (reuse inputs/entity tracking), 202601180634-1CANR1 (harden generator), 202601180654-K00W5C (Clearly Amazing service areas + newline output), 202601180919-K0MTNR (compact JSON-LD), 202601180914-7D0M68 (areaServed strings), 202601180753-2MBGAS (types + per-service offers), 202601180815-472897 (logo/address + geocoding), 202601180828-4Y3AP2 (geocode fallback/logging), 202601180609-WGXYXP (single JSON-LD per page + Search Appearance docs + pytest)."
---
# 202601211646-VBPK9P: Execute all schema-tagged tasks

## Summary

- Execute the current `schema`-tagged backlog end-to-end (code, docs, data), using per-task commits and `agentctl` finish metadata.
- Status: all `schema`-tagged tasks in scope are now marked `DONE`.

## Context

- This repo contains an automated schema generator and cached site inputs/outputs; multiple TODO tasks target correctness vs `schemaorg-current-https.jsonld`, output formatting, and enrichment (offers, areaServed, geo, logo).

## Scope

- In scope: 202601180735-Y4CG1A, 202601180617-99GCXY, 202601180634-1CANR1, 202601180654-K00W5C, 202601180919-K0MTNR, 202601180914-7D0M68, 202601180753-2MBGAS, 202601180815-472897, 202601180828-4Y3AP2, 202601180609-WGXYXP.
- Out of scope: unrelated SEO/content tasks not tagged `schema`.

## Risks

- Schema changes can regress validation for existing pages (type/property mismatches, accidental removal of required fields).
- Geo/logo enrichment may introduce optional dependencies and can fail when offline; generator must degrade gracefully.

## Verify Steps

- Run the repo test suite as declared on tasks that require it (at minimum: `python3 -m pytest` for 202601180609-WGXYXP).
- Regenerate representative schema outputs and spot-check JSON-LD validity (structure + one-script-per-page rule).

## Rollback Plan

- Revert the per-task commits for any failing change; keep tasks open/blocked with notes on what broke and why.

## Notes

- Completed tasks: 202601180735-Y4CG1A, 202601180617-99GCXY, 202601180634-1CANR1, 202601180654-K00W5C, 202601180919-K0MTNR, 202601180914-7D0M68, 202601180753-2MBGAS, 202601180815-472897, 202601180828-4Y3AP2, 202601180609-WGXYXP.
- Verification highlights: schema validator spotcheck passed (`scripts/schema_org_validator.py` on a generated page) and `python3 -m pytest` passed (29 tests).

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- (no file changes)
<!-- END AUTO SUMMARY -->

