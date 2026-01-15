---
id: "202601150642-HFYJGX"
title: "Automate service brief generation"
status: "DOING"
priority: "med"
owner: "CODER"
depends_on: []
tags: []
comments:
  - { author: "ORCHESTRATOR", body: "Start: implement crawl cache + service brief generator with strict rate limits and cached fixtures to avoid repeated live requests." }
doc_version: 2
doc_updated_at: "2026-01-15T07:06:14+00:00"
doc_updated_by: "agentctl"
description: "Create a generator that outputs service briefs with sources from approved service inputs and proof points."
---
## Summary

Generate service briefs from cached client site HTML using a rate-limited crawl cache and deterministic parsing.

## Scope

- Add crawl cache utility with per-URL rate limiting and snapshot storage.
- Implement service brief generator that reads cached HTML.
- Add unit tests using cached fixtures (no live requests).

## Risks

- Extraction is heuristic; review brief output for accuracy before use.
- Cached HTML may become stale; refresh cache when site content changes.

## Verify Steps

- Run .venv/bin/python -m unittest tests/test_service_brief_generator.py (passes).
- Run crawl cache with safe rate limits and confirm cache files created (optional).

## Rollback Plan

- Revert commit for crawl cache/service brief generator.
- Remove generated cache/output files under outputs/<client>/reports if needed.

