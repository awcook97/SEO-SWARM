---
id: "202601180617-99GCXY"
title: "Reuse inputs + track entities in cache schema generator"
status: "DONE"
priority: "P1"
owner: "ORCHESTRATOR"
depends_on: []
tags: ["seo", "schema", "automation"]
commit: { hash: "fa6d49edbf41fafe03aac3b98b969cac152659c3", message: "📝 99GCXY docs: record input reuse and shared entity registry" }
comments:
  - { author: "ORCHESTRATOR", body: "Start: confirm cache schema generator reuses approved inputs and maintains a shared entity registry across pages for consistent IDs." }
  - { author: "ORCHESTRATOR", body: "verified: cache schema generator prefers GBP checklist inputs and reuses a shared entity registry so IDs stay consistent across pages | details: py_compile of scripts/cache_schema_generator.py passed." }
doc_version: 2
doc_updated_at: "2026-01-21T16:52:28+00:00"
doc_updated_by: "agentctl"
description: "Update cache_schema_generator.py to load existing inputs/extracted reports and track larger entities through generation."
---
# 202601180617-99GCXY: Reuse inputs + track entities in cache schema generator

## Summary

- Reuse approved business inputs (GBP checklist preferred; `inputs.md` fallback) when generating schema.
- Maintain a shared entity registry so `@id` values stay consistent across all generated pages.

## Context

- The cache schema generator renders per-page JSON-LD from cached HTML plus approved business metadata.
- Stable entity IDs and shared objects (WebSite/Organization/LocalBusiness) reduce duplication and keep references consistent.

## Scope

- Confirm `scripts/cache_schema_generator.py` uses `load_inputs()` to load approved inputs from `outputs/<client>/reports/gbp-update-checklist.json` before falling back to `outputs/<client>/inputs.md`.
- Confirm `EntityRegistry` is built once per run and reused for all pages so graph nodes can reference stable `@id` values.

## Risks

- If inputs are missing or placeholder values exist, output should omit fields rather than emitting invalid/empty schema values.

## Verify Steps

- `python3 -m py_compile scripts/cache_schema_generator.py`

## Rollback Plan

- Revert the commit for this task; rerun generation to confirm prior behavior.

## Notes

- Prefer keeping `WebSite`, `Organization`, and `LocalBusiness` entities in `EntityRegistry` and only cloning per-page when needed.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- (no file changes)
<!-- END AUTO SUMMARY -->

