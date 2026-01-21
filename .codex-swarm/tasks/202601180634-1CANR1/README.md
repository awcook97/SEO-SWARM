---
id: "202601180634-1CANR1"
title: "Harden cache schema generator against bad HTML"
status: "DOING"
priority: "P1"
owner: "ORCHESTRATOR"
depends_on: []
tags: ["seo", "schema", "automation"]
comments:
  - { author: "ORCHESTRATOR", body: "Start: confirm cache schema generator tolerates malformed/non-UTF8 cache HTML and logs skips without crashing generation." }
doc_version: 2
doc_updated_at: "2026-01-21T16:53:15+00:00"
doc_updated_by: "agentctl"
description: "Inspect generated outputs for errors and update cache_schema_generator.py to tolerate non-UTF8/garbled cache files, logging skips; rerun generator for clearlyamazing."
---

# 202601180634-1CANR1: Harden cache schema generator against bad HTML

## Summary

- Ensure `scripts/cache_schema_generator.py` handles malformed cache HTML (binary/null bytes, non-UTF8, broken char refs) by skipping/logging rather than crashing the run.

## Context

- Cached crawls can include binary assets saved with HTML extensions, garbled encoding, or invalid HTML entities.
- The schema generator should be resilient so a single bad file does not block generating schema for the rest of the site.

## Scope

- Use byte-level reads with safe decoding and sanitization (`errors="replace"`, invalid charref handling).
- Skip and log problematic cache entries (non-text content, parse failures) while continuing generation.

## Risks

- Over-sanitizing can distort extracted content; keep sanitation minimal and focused on parser safety.

## Verify Steps

- `python3 scripts/cache_schema_generator.py --client-slug clearlyamazing --output-dir /tmp/schema-smoke-1canr1`

## Rollback Plan

- Revert the commit for this task; rerun the smoke command above to confirm regression.

## Notes

- Prefer “skip + log” for irrecoverable inputs; avoid raising exceptions from per-page parsing.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- (no file changes)
<!-- END AUTO SUMMARY -->
