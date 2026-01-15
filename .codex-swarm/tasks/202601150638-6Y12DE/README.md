---
id: "202601150638-6Y12DE"
title: "Automate internal link validation"
status: "DOING"
priority: "med"
owner: "CODER"
depends_on: []
tags: ["seo", "onpage", "automation", "code", "backend"]
verify: ["python -m unittest tests/test_internal_link_validator.py"]
comments:
  - { author: "CODER", body: "Start: define internal link validation rules, implement validator + tests, wire into docs." }
doc_version: 2
doc_updated_at: "2026-01-15T07:36:52+00:00"
doc_updated_by: "agentctl"
description: "Create a checker that verifies internal link targets referenced in drafts (service hub, related services, contact) exist or are approved, and reports missing/placeholder links."
---
## Summary

Add an internal link validation tool that checks metadata/link map outputs for required link targets and placeholders, producing a report.

## Context

Internal links are required across templates, but we lack automated validation. This validator will read metadata/internal link maps and flag missing or placeholder links before publishing.

## Scope

- Define required link types per page type.
- Implement validator script outputting JSON + Markdown report.
- Add tests and document usage.

## Risks

- Rule set could be too strict for some pages.
- Placeholder detection may flag legitimate URLs.
- Validation depends on accurate link map generation.

## Verify Steps

- Run python -m unittest tests/test_internal_link_validator.py.
- Generate a sample validation report for a client and review missing/placeholder counts.

## Rollback Plan

Revert the validator script/docs/tests; continue manual internal link review.

## Notes

Approved plan: rules -> validator+tests -> docs wiring.

