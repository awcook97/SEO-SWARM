---
id: "202601180919-K0MTNR"
title: "Compact JSON-LD output"
status: "DONE"
priority: "P1"
owner: "ORCHESTRATOR"
depends_on: []
tags: ["schema", "seo", "automation"]
commit: { hash: "dcb0df00bfbf425d0d9d827be59406604fa5a668", message: "📝 K0MTNR docs: document compact JSON-LD render_script" }
comments:
  - { author: "ORCHESTRATOR", body: "Start: confirm cache schema generator emits compact JSON-LD payloads (no pretty-printing) inside the single script tag." }
  - { author: "ORCHESTRATOR", body: "verified: render_script uses json.dumps(..., separators=(,, :)) with no indent so JSON-LD payloads are compact while keeping script block newlines." }
doc_version: 2
doc_updated_at: "2026-01-21T16:57:07+00:00"
doc_updated_by: "agentctl"
description: "Emit JSON-LD without pretty printing for output scripts."
---
# 202601180919-K0MTNR: Compact JSON-LD output

## Summary

- Emit compact JSON-LD payloads in generated `<script type="application/ld+json">` blocks (no pretty-print indentation).

## Context

- The generator writes one schema script per page; compact output reduces page size and keeps diffs smaller for review.

## Scope

- Use `json.dumps(..., separators=(",", ":"))` (no `indent`) when rendering JSON-LD.

## Risks

- Compact JSON is harder to read manually; rely on validation tools (`scripts/schema_org_validator.py`) for correctness checks.

## Verify Steps

- Confirm `scripts/cache_schema_generator.py:render_script()` uses `json.dumps(..., separators=(",", ":"))`.

## Rollback Plan

- Revert the commit for this task; regenerate a sample client output and compare payload formatting.

## Notes

- Keep the surrounding HTML readable by retaining newlines around the compact JSON payload.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- (no file changes)
<!-- END AUTO SUMMARY -->

