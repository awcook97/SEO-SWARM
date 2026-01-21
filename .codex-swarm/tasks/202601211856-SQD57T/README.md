---
id: "202601211856-SQD57T"
title: "Automate GBP export ingest"
status: "DONE"
priority: "med"
owner: "CODER"
depends_on: ["202601211855-FAJDQP"]
tags: ["automation", "gbp"]
commit: { hash: "3591cac59fa7b63b1c0339d05b96d12b1ca93f6d", message: "🧩 202601211856-SQD57T integrate task/202601211856-SQD57T/gbp" }
comments:
  - { author: "INTEGRATOR", body: "verified: Integrated via squash | details: verify=skipped(no commands); pr=.codex-swarm/tasks/202601211856-SQD57T/pr." }
  - { author: "INTEGRATOR", body: "verified: Integrated GBP export ingest." }
doc_version: 2
doc_updated_at: "2026-01-21T22:55:39+00:00"
doc_updated_by: "agentctl"
description: "Automate pulling GBP exports into outputs/<client>/reports/gbp-export.json for reporting and profile sync."
---
# 202601211856-SQD57T: Automate GBP export ingest

## Summary

Normalize GBP export CSVs into JSON with optional totals summary.

## Context

- ...

## Scope

Add GBP export ingest script, summary output, and unit tests.

## Risks

GBP exports differ by locale; missing columns will yield zeroed metrics.

## Verify Steps

1) /home/andrew/projects/codex-swarm/.venv/bin/python tests/test_gbp_export_ingest.py\n2) python scripts/gbp_export_ingest.py --client-slug <client> --input <export.csv> --summary

## Rollback Plan

Revert commit(s) adding gbp_export_ingest.py and related docs/tests.

## Notes

- ...

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- `README.md`
- `scripts/gbp_export_ingest.py`
- `tests/test_gbp_export_ingest.py`
<!-- END AUTO SUMMARY -->

