---
id: "202601150638-E7R3X5"
title: "Automate measurement intake generation"
status: "DONE"
priority: "med"
owner: "CODER"
depends_on: []
tags: []
commit: { hash: "544454af6d5a0b0582b837eec980f4fe8f8a7c2c", message: "✨ E7R3X5 add measurement intake generator" }
comments:
  - { author: "ORCHESTRATOR", body: "Start: automate measurement intake generation as part of metrics bundle." }
  - { author: "CODER", body: "verified: added measurement intake generator with docs and unit tests." }
doc_version: 2
doc_updated_at: "2026-01-15T06:38:33+00:00"
doc_updated_by: "agentctl"
description: "Create a script to generate a measurement intake file from structured inputs, preserving placeholders for missing data."
---
## Summary

Automate measurement intake sheet creation using approved structured inputs.

## Scope

- Add `scripts/measurement_intake_generator.py` with output markdown + JSON.
- Provide a `--scaffold` mode to bootstrap inputs.
- Document usage and add unit tests.

## Risks

- Missing fields remain placeholders; ensure approved sources feed the JSON.

## Verify Steps

- Run `python3 -m unittest discover -s tests` (passes).

## Rollback Plan

- Revert the measurement intake generator script, docs, and tests.

