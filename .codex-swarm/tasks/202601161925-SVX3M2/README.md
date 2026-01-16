---
id: "202601161925-SVX3M2"
title: "Improve schema-to-inputs extraction"
status: "DOING"
priority: "high"
owner: "CODER"
depends_on: []
tags: []
comments:
  - { author: "CODER", body: "Start: improve schema-to-inputs extraction for @graph and richer fields." }
doc_version: 2
doc_updated_at: "2026-01-16T19:25:49+00:00"
doc_updated_by: "agentctl"
description: "Handle @graph JSON-LD, extract richer fields (name, description, hours, services, social, payment, geo) when present, and improve errors."
---
## Summary

Enhance the schema-to-inputs scaffold to parse @graph nodes and richer business fields.

## Scope

- Support @graph and nested nodes when extracting name, URL, and description.
- Extract hours, areas served, services, social profiles, price range, and payments when available.
- Update tests to cover @graph-based schemas.

## Risks

- Schema variants may still omit fields; placeholders remain where data is missing.

## Verify Steps

- Run `python3 -m unittest discover -s tests` (passes).

## Rollback Plan

- Revert updates to `scripts/inputs_from_schema.py` and related tests.
