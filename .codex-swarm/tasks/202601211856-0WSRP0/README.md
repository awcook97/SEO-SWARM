---
id: "202601211856-0WSRP0"
title: "Automate review export ingest"
status: "TODO"
priority: "med"
owner: "CODER"
depends_on: ["202601211855-FAJDQP"]
tags: ["automation", "reviews"]
doc_version: 2
doc_updated_at: "2026-01-21T22:51:42+00:00"
doc_updated_by: "agentctl"
description: "Automate pulling review exports into outputs/<client>/reports/review-templates-input.json for response templates."
---
# 202601211856-0WSRP0: Automate review export ingest

## Summary

Automate conversion of review exports into input JSON for response templates.

## Context

- ...

## Scope

Add review export ingest script, documentation updates, and unit tests.

## Risks

CSV columns may not match expected headers; rows missing required fields are skipped.

## Verify Steps

1) /home/andrew/projects/codex-swarm/.venv/bin/python tests/test_review_export_ingest.py\n2) python scripts/review_export_ingest.py --client-slug <client> --input <export.csv>

## Rollback Plan

Revert commit(s) adding review_export_ingest.py and related docs/tests.

## Notes

- ...

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- `README.md`
- `docs/seo/review-response-templates.md`
- `scripts/review_export_ingest.py`
- `tests/test_review_export_ingest.py`
<!-- END AUTO SUMMARY -->

