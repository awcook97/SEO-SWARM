---
id: "202601150638-P2QAD6"
title: "Automate rank tracking report builder"
status: "DOING"
priority: "med"
owner: "CODER"
depends_on: []
tags: []
comments:
  - { author: "CODER", body: "Start: build rank tracking report script from CSV exports per measurement template." }
doc_version: 2
doc_updated_at: "2026-01-21T18:04:44+00:00"
doc_updated_by: "agentctl"
description: "Create a script that ingests rank tracker exports (CSV) and outputs a rank tracking report aligned to docs/seo/measurement-reporting-template.md and docs/seo/measurement-spec.md."
---
# 202601150638-P2QAD6: Automate rank tracking report builder

## Summary

- Add `scripts/rank_tracking_report_builder.py` to transform rank tracker CSV exports into a markdown + JSON report.

## Context

- The measurement reporting template expects a keyword performance table and alerts for drops.
- Rank tracking exports typically arrive as CSV, so the tool should normalize headers and compute deltas.

## Scope

- New script: `scripts/rank_tracking_report_builder.py`.
- Input: `outputs/<client>/reports/rank-tracking.csv` plus optional config JSON.
- Outputs: `outputs/<client>/reports/rank-tracking-report.md` and `rank-tracking-report.json`.

## Risks

- CSV header mismatches can drop fields; the script includes header normalization but still relies on consistent exports.

## Verify Steps

- `python3 scripts/rank_tracking_report_builder.py --client-slug <client> --scaffold-config`
- `python3 scripts/rank_tracking_report_builder.py --client-slug <client> --input <csv>`

## Rollback Plan

- Revert the commit; remove the script if it conflicts with the reporting workflow.

## Notes

- Use `rank-tracking-config.json` to store reporting metadata and drop thresholds.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- `.codex-swarm/tasks/202601150638-P2QAD6/README.md`
- `.codex-swarm/tasks/202601150638-P2QAD6/pr/diffstat.txt`
- `.codex-swarm/tasks/202601150638-P2QAD6/pr/meta.json`
- `.codex-swarm/tasks/202601150638-P2QAD6/pr/review.md`
- `.codex-swarm/tasks/202601150638-P2QAD6/pr/verify.log`
- `scripts/rank_tracking_report_builder.py`
<!-- END AUTO SUMMARY -->
