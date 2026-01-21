---
id: "202601211856-3BR951"
title: "Automate GSC data export ingest"
status: "DONE"
priority: "med"
owner: "CODER"
depends_on: ["202601211855-FAJDQP"]
tags: ["automation", "gsc"]
commit: { hash: "5d669bf4739caf687d99edb4378793da091f2652", message: "🧩 202601211856-3BR951 integrate task/202601211856-3BR951/gsc" }
comments:
  - { author: "INTEGRATOR", body: "verified: Integrated via squash | details: verify=skipped(no commands); pr=.codex-swarm/tasks/202601211856-3BR951/pr." }
  - { author: "INTEGRATOR", body: "verified: Integrated GSC export ingest." }
doc_version: 2
doc_updated_at: "2026-01-21T22:52:35+00:00"
doc_updated_by: "agentctl"
description: "Automate pulling GSC exports into outputs/<client>/reports/gsc-export.json (or csv) for reporting."
---
# 202601211856-3BR951: Automate GSC data export ingest

## Summary

Automate ingestion of GSC CSV exports into normalized JSON and summary.

## Context

- ...

## Scope

Add GSC export ingest script, optional summary output, and unit tests.

## Risks

GSC export headers vary; unmapped fields remain raw and summaries may be incomplete.

## Verify Steps

1) /home/andrew/projects/codex-swarm/.venv/bin/python tests/test_gsc_export_ingest.py\n2) python scripts/gsc_export_ingest.py --client-slug <client> --input <export.csv> --summary

## Rollback Plan

Revert commit(s) adding gsc_export_ingest.py and related docs/tests.

## Notes

- ...

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- `README.md`
- `scripts/gsc_export_ingest.py`
- `tests/test_gsc_export_ingest.py`
<!-- END AUTO SUMMARY -->

