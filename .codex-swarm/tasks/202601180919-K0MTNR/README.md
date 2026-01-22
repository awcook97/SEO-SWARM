---
id: "202601180919-K0MTNR"
title: "Compact JSON-LD output"
status: "DONE"
priority: "P1"
owner: "ORCHESTRATOR"
depends_on: []
tags: ["schema", "seo", "automation"]
commit: { hash: "d6e93247a41098921f0e10f789732c19bdce2789", message: "🧩 202601180919-K0MTNR integrate task/202601180919-K0MTNR/compact-jsonld" }
comments:
  - { author: "INTEGRATOR", body: "verified: Integrated via squash | details: verify=skipped(no commands); pr=.codex-swarm/tasks/202601180919-K0MTNR/pr." }
  - { author: "INTEGRATOR", body: "verified: Integrated via squash | details: verify=skipped(no commands); pr=.codex-swarm/tasks/202601180919-K0MTNR/pr." }
doc_version: 2
doc_updated_at: "2026-01-18T09:19:07+00:00"
doc_updated_by: "agentctl"
description: "Emit JSON-LD without pretty printing for output scripts."
---
## Summary

Emit compact single-line JSON-LD script tags.

## Scope

Update `scripts/cache_schema_generator.py` to inline JSON-LD payload without extra newlines.

## Risks

Single-line output is harder to read manually; JSON remains valid and machine-readable.

## Verify Steps

1) Run `python scripts/cache_schema_generator.py --client-slug <client>`.
2) Confirm generated HTML has single-line JSON-LD script tags.

## Rollback Plan

Revert the `render_script` formatting change in `scripts/cache_schema_generator.py`.

## Notes

JSON remains compacted via `json.dumps(..., separators=(",", ":"))`.

