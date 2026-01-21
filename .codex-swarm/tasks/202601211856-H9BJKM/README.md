---
id: "202601211856-H9BJKM"
title: "Automate rank tracker ingest"
status: "DONE"
priority: "med"
owner: "CODER"
depends_on: ["202601211855-FAJDQP"]
tags: ["automation", "rank"]
commit: { hash: "4b1a4cd8d105a5bd009d5d0269d61145481f2c51", message: "🧩 202601211856-H9BJKM integrate task/202601211856-H9BJKM/rank" }
comments:
  - { author: "INTEGRATOR", body: "verified: Integrated via squash | details: verify=skipped(no commands); pr=.codex-swarm/tasks/202601211856-H9BJKM/pr." }
  - { author: "INTEGRATOR", body: "verified: Integrated rank tracker export ingest." }
doc_version: 2
doc_updated_at: "2026-01-21T22:53:22+00:00"
doc_updated_by: "agentctl"
description: "Automate collecting rank tracker exports into outputs/<client>/reports/rank-tracking.csv."
---
# 202601211856-H9BJKM: Automate rank tracker ingest

## Summary

Normalize rank tracker exports into a standard CSV and summary JSON.

## Context

- ...

## Scope

Add rank tracker ingest script, output summary JSON, and tests.

## Risks

Export headers differ by vendor; unmapped fields stay blank in the normalized output.

## Verify Steps

1) /home/andrew/projects/codex-swarm/.venv/bin/python tests/test_rank_tracker_export_ingest.py\n2) python scripts/rank_tracker_export_ingest.py --client-slug <client> --input <export.csv>

## Rollback Plan

Revert commit(s) adding rank_tracker_export_ingest.py and related docs/tests.

## Notes

- ...

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- `README.md`
- `scripts/rank_tracker_export_ingest.py`
- `tests/test_rank_tracker_export_ingest.py`
<!-- END AUTO SUMMARY -->

