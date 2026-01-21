---
id: "202601180828-4Y3AP2"
title: "Improve geocode fallback + logging"
status: "DOING"
priority: "P1"
owner: "ORCHESTRATOR"
depends_on: []
tags: ["schema", "seo", "automation"]
comments:
  - { author: "ORCHESTRATOR", body: "Start: verify resolve_geo builds address variants, prefers cached geocodes, and logs failures when geocoding is enabled." }
doc_version: 2
doc_updated_at: "2026-01-21T17:02:54+00:00"
doc_updated_by: "agentctl"
description: "Add address variants and logging to geocoding so geo coordinates resolve and cache file is created."
---

# 202601180828-4Y3AP2: Improve geocode fallback + logging

## Summary

- Improve geocoding resilience by trying multiple address variants, preferring cached results, and emitting useful logs for failures when geocoding is enabled.

## Context

- Address formatting varies by data source (Line 2/unit, missing postal codes, or city/state-only lookups).
- Geocoding is optional and can be unavailable offline; cached results should still resolve deterministically.

## Scope

- Build address variants (full address, without Line 2, unit-inlined, city/state) for lookups.
- Prefer cached results from `outputs/<client>/reports/geocoded.json` before attempting any live geocoding.
- Log each attempted variant when live geocoding is enabled and fails.

## Risks

- Variant generation that is too aggressive can increase false positives; keep the variant set small and ordered (most specific → least specific).

## Verify Steps

- Offline cache hit: create a temp cache file and confirm `resolve_geo(..., enable_geocode=False)` returns the cached coordinates (executed during this run with `/tmp/geocode-4y3ap2.json`).
- Code inspection: confirm `resolve_geo()` tries variants in order and prints `geocode failed for: ...` when live geocoding is enabled.

## Rollback Plan

- Revert the commit for this task; rerun the offline cache-hit snippet to confirm prior behavior.

## Notes

- Live geocoding should remain opt-in (flag-gated) to avoid unexpected external calls.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- (no file changes)
<!-- END AUTO SUMMARY -->
