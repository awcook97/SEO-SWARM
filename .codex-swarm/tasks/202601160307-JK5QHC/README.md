---
id: "202601160307-JK5QHC"
title: "Extend brief generator extraction"
status: "DOING"
priority: "med"
owner: "CODER"
depends_on: ["202601160307-D2J7GG"]
tags: []
comments:
  - { author: "CODER", body: "Start: extend brief generator extraction for richer content briefs." }
doc_version: 2
doc_updated_at: "2026-01-16T03:07:45+00:00"
doc_updated_by: "agentctl"
description: "Implement structured extraction from cached HTML and generate standardized briefs."
---
## Summary

Extend service brief extraction to include social preview metadata and CTA link targets.

## Scope

- Extract canonical URL, Open Graph, and Twitter metadata from cached HTML.
- Capture CTA link targets in addition to CTA text.
- Update service brief output to include the new fields.
- Extend unit tests and fixtures to cover the new extraction fields.

## Risks

- Sites without social meta tags will produce empty fields; output remains valid.

## Verify Steps

- Run `python3 -m unittest discover -s tests` (passes).

## Rollback Plan

- Revert service brief generator changes and updated fixtures/tests.
