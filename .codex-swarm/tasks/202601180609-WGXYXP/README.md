---
id: "202601180609-WGXYXP"
title: "Review Search Appearance best practices + single JSON-LD per page"
status: "DOING"
priority: "P1"
owner: "ORCHESTRATOR"
depends_on: []
tags: ["seo", "schema", "docs"]
verify: ["python3 -m pytest"]
comments:
  - { author: "ORCHESTRATOR", body: "Start: confirm one JSON-LD script per page and align docs to Google Search appearance best practices; run python3 -m pytest as declared verify." }
doc_version: 2
doc_updated_at: "2026-01-21T17:03:50+00:00"
doc_updated_by: "agentctl"
description: "Inspect Google Search Appearance docs for best practices and ensure outputs use one JSON-LD script per page; run verification."
---

# 202601180609-WGXYXP: Review Search Appearance best practices + single JSON-LD per page

## Summary

- Confirm generator output follows “single JSON-LD script per page” guidance and keeps schema aligned with on-page visible content.
- Run the repo test suite (`python3 -m pytest`) as the declared verification step for this task.

## Context

- The cache schema generator writes one JSON-LD `<script type="application/ld+json">` per generated HTML file.
- Search appearance best practices for structured data emphasize JSON-LD, correctness, and parity with page content.

## Scope

- Confirm `scripts/cache_schema_generator.py` writes exactly one JSON-LD `<script>` per output file (no multi-script concatenation).
- Keep docs aligned with the “single script per page + visible content parity” guidance in `docs/seo/cache-schema-generator.md`.

## Risks

- Adding multiple schema scripts per page can cause confusing review and validation results; keep output one-script-per-page unless a clear need is documented.

## Verify Steps

- `python3 -m pytest`

## Rollback Plan

- Revert the commit(s) for this task; rerun `python3 -m pytest` to confirm prior test baseline.

## Notes

- Output files under `outputs/<client>/gen-schema/website-tree/` are intentionally simple containers for a single schema `<script>` tag.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- (no file changes)
<!-- END AUTO SUMMARY -->
