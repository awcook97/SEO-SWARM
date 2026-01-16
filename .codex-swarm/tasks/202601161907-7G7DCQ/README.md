---
id: "202601161907-7G7DCQ"
title: "Add inputs.md template doc"
status: "DONE"
priority: "high"
owner: "DOCS"
depends_on: []
tags: []
commit: { hash: "ae92d65a6a500882bf2e7605de95f128012955f6", message: "✅ 017MWA verified: added schema-to-inputs scaffold script with tests and docs." }
comments:
  - { author: "DOCS", body: "verified: added inputs template doc and linked it in README/workflow." }
doc_version: 2
doc_updated_at: "2026-01-16T19:07:48+00:00"
doc_updated_by: "agentctl"
description: "Create a clear inputs.md template and link it from README and workflow docs."
---
## Summary

Add a standard inputs.md template and link it from core documentation.

## Scope

- Create `docs/seo/inputs-template.md`.
- Link the template from `README.md`, `docs/seo/README.md`, and `docs/seo/swarm-execution-workflow.md`.

## Risks

- Template may drift as inputs evolve; keep it updated with new fields.

## Verify Steps

- Manual review of the template and links in docs.

## Rollback Plan

- Revert the inputs template doc and related README/workflow changes.

