---
id: "202601150638-HJ1QRA"
title: "Generate GBP update checklist"
status: "DONE"
priority: "med"
owner: "CODER"
depends_on: []
tags: []
commit: { hash: "fccb504645775f743e41d9ed0e9e063c97bb1d3d", message: "✨ HJ1QRA add GBP update checklist generator" }
comments:
  - { author: "CODER", body: "Start: implement GBP update checklist generator with docs-aligned inputs." }
  - { author: "CODER", body: "verified: added GBP update checklist generator and ran unittest suite." }
doc_version: 2
doc_updated_at: "2026-01-15T06:38:57+00:00"
doc_updated_by: "agentctl"
description: "Create a script to produce a GBP update checklist and posting plan from approved NAP/services/attributes per docs/client-templates/swarm-roles.md."
---
## Summary

Generate a GBP update checklist and posting plan from approved input data.

## Scope

- Add GBP checklist generator script reading `outputs/<client>/inputs.md`.
- Output markdown and JSON reports under `outputs/<client>/reports/`.
- Document usage in SEO docs and index.
- Add unit tests for parsing and post plan rotation.

## Risks

- Inputs file format drift could cause missing fields in the checklist.

## Verify Steps

- Run `python3 -m unittest discover -s tests` (passes).

## Rollback Plan

- Revert the GBP checklist generator script, docs, and tests.

