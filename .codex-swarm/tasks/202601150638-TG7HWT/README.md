---
id: "202601150638-TG7HWT"
title: "Generate content briefs from inputs"
status: "DONE"
priority: "med"
owner: "CODER"
depends_on: []
tags: []
commit: { hash: "4df67e220ad81191f2dbffdb236cd555994d53ff", message: "✨ D2J7GG add content brief generator" }
comments:
  - { author: "CODER", body: "verified: content brief generator emits service/local/topical briefs from inputs." }
doc_version: 2
doc_updated_at: "2026-01-15T06:38:52+00:00"
doc_updated_by: "agentctl"
description: "Create a script that takes approved inputs and emits service page brief, local landing brief, and topical blog brief per docs/client-templates/swarm-roles.md content planner outputs."
---
## Summary

Use the content brief generator script to emit markdown briefs from approved inputs.

## Scope

- Leverage `scripts/content_brief_generator.py` to generate briefs by type.
- Support service-page, local-landing, and topical-guide brief entries via input JSON.
- Store outputs under `outputs/<client>/reports/content-briefs/`.

## Risks

- Input JSON requires manual fill-in of keywords, targets, and CTAs.

## Verify Steps

- Run `python3 -m unittest discover -s tests` (passes).

## Rollback Plan

- Revert the content brief generator script and related docs/tests if needed.

