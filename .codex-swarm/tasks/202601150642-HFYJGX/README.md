---
id: "202601150642-HFYJGX"
title: "Automate service brief generation"
status: "DONE"
priority: "med"
owner: "CODER"
depends_on: []
tags: []
commit: { hash: "179b1d7a51819eff49125100a1460c714c8f44c2", message: "✨ HFYJGX add crawl cache and service brief generator" }
comments:
  - { author: "ORCHESTRATOR", body: "Start: implement crawl cache + service brief generator with strict rate limits and cached fixtures to avoid repeated live requests." }
  - { author: "CODER", body: "verified: ran .venv/bin/python -m unittest tests/test_service_brief_generator.py | details: added crawl cache utility with per-URL rate limiting and service brief generator that reads cached HTML snapshots." }
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

