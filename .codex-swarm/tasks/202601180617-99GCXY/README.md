---
id: "202601180617-99GCXY"
title: "Reuse inputs + track entities in cache schema generator"
status: "DOING"
priority: "P1"
owner: "ORCHESTRATOR"
depends_on: []
tags: ["seo", "schema", "automation"]
comments:
  - { author: "ORCHESTRATOR", body: "Start: update cache schema generator to reuse stored inputs and keep entity registry consistent across pages." }
doc_version: 2
doc_updated_at: "2026-01-21T18:07:28+00:00"
doc_updated_by: "agentctl"
description: "Update cache_schema_generator.py to load existing inputs/extracted reports and track larger entities through generation."
---
# 202601180617-99GCXY: Reuse inputs + track entities in cache schema generator

## Summary

- Extend `cache_schema_generator.py` to reuse cached input JSON and persist an entity registry snapshot per run.

## Context

- Schema generation should prefer approved inputs from reports when available, then fall back to `inputs.md`.
- Persisting entity registry data keeps large entities observable between runs and supports auditing.

## Scope

- Load optional `outputs/<client>/reports/cache-schema-inputs.json` when present.
- Write `outputs/<client>/reports/cache-schema-entity-registry.json` after building entities.

## Risks

- Cached inputs can drift from approved facts; treat them as secondary to GBP checklist inputs.

## Verify Steps

- `python3 -m py_compile scripts/cache_schema_generator.py`
- `python3 scripts/cache_schema_generator.py --client-slug <client>` (confirm entity registry snapshot is written).

## Rollback Plan

- Revert the commit; remove cached input handling and registry snapshot writes.

## Notes

- `cache-schema-entity-registry.json` is for audit/debug only; output HTML remains unchanged.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- `.codex-swarm/tasks/202601180617-99GCXY/README.md`
- `.codex-swarm/tasks/202601180617-99GCXY/pr/diffstat.txt`
- `.codex-swarm/tasks/202601180617-99GCXY/pr/meta.json`
- `.codex-swarm/tasks/202601180617-99GCXY/pr/review.md`
- `.codex-swarm/tasks/202601180617-99GCXY/pr/verify.log`
<!-- END AUTO SUMMARY -->
