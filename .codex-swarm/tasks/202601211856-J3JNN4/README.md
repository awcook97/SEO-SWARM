---
id: "202601211856-J3JNN4"
title: "Automate GA4 data export ingest"
status: "TODO"
priority: "med"
owner: "CODER"
depends_on: ["202601211855-FAJDQP"]
tags: ["automation", "ga4"]
doc_version: 2
doc_updated_at: "2026-01-21T22:54:08+00:00"
doc_updated_by: "agentctl"
description: "Automate pulling GA4 exports into outputs/<client>/reports/ga4-export.json (or csv) for reporting."
---
# 202601211856-J3JNN4: Automate GA4 data export ingest

## Summary

Automate GA4 CSV ingestion into normalized JSON and optional summary.

## Context

- ...

## Scope

Add GA4 export ingest script, summary output, and unit tests.

## Risks

GA4 exports vary by report; missing metrics default to zero in summaries.

## Verify Steps

1) /home/andrew/projects/codex-swarm/.venv/bin/python tests/test_ga4_export_ingest.py\n2) python scripts/ga4_export_ingest.py --client-slug <client> --input <export.csv> --summary

## Rollback Plan

Revert commit(s) adding ga4_export_ingest.py and related docs/tests.

## Notes

- ...

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- `README.md`
- `scripts/ga4_export_ingest.py`
- `tests/test_ga4_export_ingest.py`
<!-- END AUTO SUMMARY -->

