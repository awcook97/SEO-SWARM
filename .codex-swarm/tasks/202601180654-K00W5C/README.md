---
id: "202601180654-K00W5C"
title: "Fix Clearly Amazing service areas + JSON-LD newline output"
status: "DONE"
priority: "P1"
owner: "ORCHESTRATOR"
depends_on: []
tags: ["seo", "schema", "data"]
commit: { hash: "1d0647737963bca5585bf86b24a712632a5c84f7", message: "🧩 202601180654-K00W5C integrate task/202601180654-K00W5C/clearlyamazing" }
comments:
  - { author: "INTEGRATOR", body: "verified: Integrated via squash | details: verify=skipped(no commands); pr=.codex-swarm/tasks/202601180654-K00W5C/pr." }
doc_version: 2
doc_updated_at: "2026-01-21T23:48:55+00:00"
doc_updated_by: "agentctl"
description: "Identify real Clearly Amazing locations from cached site data, update inputs.md and gbp-update-checklist.json, and emit real newlines in cache_schema_generator."
---
## Summary

Normalize service area entries and address JSON-LD output formatting for Clearly Amazing.

## Scope

Normalize areaServed inputs from inputs.md/GBP JSON and preserve clean JSON-LD output.

## Risks

Normalization may alter punctuation in area labels; verify against approved list.

## Verify Steps

1) Run cache_schema_generator.py for Clearly Amazing\n2) Confirm areaServed strings are normalized (no en-dash artifacts)

## Rollback Plan

Revert cache_schema_generator.py area normalization changes.

