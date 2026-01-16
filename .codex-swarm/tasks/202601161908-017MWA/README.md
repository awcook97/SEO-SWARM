---
id: "202601161908-017MWA"
title: "Generate inputs.md from JSON-LD schema"
status: "DONE"
priority: "high"
owner: "CODER"
depends_on: []
tags: []
commit: { hash: "517cec87568b9d036ab084258a76071c2be0c961", message: "✨ 017MWA add schema-to-inputs scaffold" }
comments:
  - { author: "CODER", body: "Start: add schema-to-inputs scaffold script for inputs.md." }
  - { author: "CODER", body: "verified: added schema-to-inputs scaffold script with tests and docs." }
doc_version: 2
doc_updated_at: "2026-01-16T19:08:14+00:00"
doc_updated_by: "agentctl"
description: "Add a script to scaffold outputs/<client>/inputs.md from a JSON-LD LocalBusiness/Plumber/etc. snippet."
---
## Summary

Add a JSON-LD to inputs.md scaffold script with basic field extraction.

## Scope

- Parse name, URL, telephone, description, address, and geo from JSON-LD.
- Write `outputs/<client>/inputs.md` using the standard template structure.
- Add unit tests and doc page for usage.

## Risks

- Schema may omit fields; script will leave placeholders for missing data.

## Verify Steps

- Run `python3 -m unittest discover -s tests` (passes).

## Rollback Plan

- Revert `scripts/inputs_from_schema.py`, tests, and docs.

