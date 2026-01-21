---
id: "202601180654-K00W5C"
title: "Fix Clearly Amazing service areas + JSON-LD newline output"
status: "DONE"
priority: "P1"
owner: "ORCHESTRATOR"
depends_on: []
tags: ["seo", "schema", "data"]
commit: { hash: "1f4b145bc8d0cb934b6cc057d379a6617eac822e", message: "📝 K00W5C docs: record clearlyamazing service areas + newline output checks" }
comments:
  - { author: "ORCHESTRATOR", body: "Start: confirm Clearly Amazing service area list matches cached /locations/ navigation and generator emits JSON-LD with real newlines." }
  - { author: "ORCHESTRATOR", body: "verified: Clearly Amazing service_areas match cached /locations/ navigation labels, and generated JSON-LD HTML contains real newline characters around the script payload." }
doc_version: 2
doc_updated_at: "2026-01-21T16:56:05+00:00"
doc_updated_by: "agentctl"
description: "Identify real Clearly Amazing locations from cached site data, update inputs.md and gbp-update-checklist.json, and emit real newlines in cache_schema_generator."
---
# 202601180654-K00W5C: Fix Clearly Amazing service areas + JSON-LD newline output

## Summary

- Keep Clearly Amazing `service_areas` aligned to the cached `/locations/` navigation labels.
- Ensure generated JSON-LD scripts are written with real newlines (not literal `\\n` sequences in HTML).

## Context

- The cache schema generator hydrates `areaServed` from approved inputs (GBP checklist preferred).
- Incorrect or “guessed” service areas can cause schema mismatches versus on-site location pages.

## Scope

- Confirm Clearly Amazing `service_areas` in `outputs/clearlyamazing/reports/gbp-update-checklist.json` match the cached `/locations/` menu labels.
- Confirm rendered JSON-LD scripts include actual newline characters around the JSON payload.

## Risks

- If the site updates location labels, the approved inputs must be refreshed to avoid drift.

## Verify Steps

- Extract + compare service area labels: see the python snippet used during execution (records `match True` for extracted vs GBP list).
- Newline check: `outputs/clearlyamazing/gen-schema/website-tree/the-ultimate-guide-to-holiday-and-christmas-lighting/index.html` contains `<script type="application/ld+json">\\n` and ends with `\\n`.

## Rollback Plan

- Restore prior inputs and rerun generation for Clearly Amazing; spot-check `areaServed` and script formatting again.

## Notes

- Source of truth for service area labels in this repo is the cached `/locations/` navigation captured in `outputs/clearlyamazing/reports/site-cache/`.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- (no file changes)
<!-- END AUTO SUMMARY -->

