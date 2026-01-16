---
id: "202601160307-D2J7GG"
title: "Implement consistent content brief generation"
status: "DOING"
priority: "med"
owner: "ORCHESTRATOR"
depends_on: []
tags: []
comments:
  - { author: "ORCHESTRATOR", body: "Start: implement consistent markdown content brief generation workflow." }
doc_version: 2
doc_updated_at: "2026-01-16T03:07:38+00:00"
doc_updated_by: "agentctl"
description: "Top-level: implement 5-step content brief workflow; subtask CODER=202601160307-JK5QHC, DOCS=202601160307-4S2YF2."
---
## Summary

Add a consistent markdown content brief generator that turns service brief inputs
into structured briefs for page and article production.

## Scope

- Add `scripts/content_brief_generator.py` to create briefs from service-brief sources.
- Support a JSON input spec plus a scaffold option for quick setup.
- Emit briefs under `outputs/<client>/reports/content-briefs/` and a summary JSON.
- Add unit tests for parsing and scaffold behavior.

## Risks

- Input JSON requires manual fill-in for keywords and targets; missing data will create placeholders.

## Verify Steps

- Run `python3 -m unittest discover -s tests` (passes).

## Rollback Plan

- Revert the content brief generator script and its tests.
