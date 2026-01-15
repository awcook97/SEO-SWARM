---
id: "202601150642-W4NYDM"
title: "Automate metadata and internal link map generation"
status: "DONE"
priority: "med"
owner: "CODER"
depends_on: []
tags: ["seo", "onpage", "automation"]
commit: { hash: "355c34b2599928faeafb61014e7716c7f1f6674f", message: "✨ W4NYDM add metadata/internal link map generator and tests" }
comments:
  - { author: "CODER", body: "Start: Implement metadata + internal link map generator (spec, script, tests, wiring) per approved plan." }
  - { author: "CODER", body: "verified: ran python -m unittest tests/test_metadata_internal_link_map.py | details: generated metadata+link map script/spec wired into workflow docs." }
doc_version: 2
doc_updated_at: "2026-01-15T07:28:39+00:00"
doc_updated_by: "agentctl"
description: "Create a generator that outputs title/meta drafts and internal link maps for pages based on approved inputs and templates."
---
## Summary

Automate generation of page metadata drafts and internal link maps from approved inputs/templates, producing consistent on-page artifacts for content workflows.

## Context

Current workflow lacks automated metadata/internal link mapping. This task adds a generator aligned with existing SEO templates and outputs under outputs/<client>/reports/.

## Scope

- Define output schema for metadata drafts and internal link maps.
- Implement generator script with input validation.
- Add/update tests and wire into docs/workflow usage.

## Risks

- Output schema mismatches existing templates.
- Input data gaps could cause partial maps.
- Internal link logic may over/under-link without guardrails.

## Verify Steps

- Run relevant test command(s).
- Generate sample outputs for a client and sanity-check schema/links.

## Rollback Plan

Revert generator script and remove new outputs/tests; prior manual process remains available.

## Notes

Approved plan: spec -> implementation+tests -> wiring+docs.

