---
id: "202601150638-HSN5BY"
title: "Automate competitor snapshot builder"
status: "DOING"
priority: "med"
owner: "CODER"
depends_on: []
tags: []
comments:
  - { author: "CODER", body: "Start: build competitor snapshot builder script aligned to measurement spec outputs." }
doc_version: 2
doc_updated_at: "2026-01-21T18:03:51+00:00"
doc_updated_by: "agentctl"
description: "Create a script to parse SERP exports/screenshots or structured inputs and generate the competitor snapshot table + gap notes required by docs/seo/measurement-spec.md."
---
# 202601150638-HSN5BY: Automate competitor snapshot builder

## Summary

- Add `scripts/competitor_snapshot_builder.py` to generate the competitor snapshot table and gap notes from structured JSON inputs.

## Context

- The measurement spec requires a competitor snapshot table and gap notes for each reporting cycle.
- Structured JSON inputs are used to avoid parsing screenshots directly while preserving verified sources.

## Scope

- New script: `scripts/competitor_snapshot_builder.py`.
- Input: `outputs/<client>/reports/competitor-snapshot-input.json` (or `--input` override).
- Outputs: `outputs/<client>/reports/competitor-snapshot.md` and `competitor-snapshot.json`.

## Risks

- Garbage-in/garbage-out: snapshot accuracy depends on the upstream SERP export data being complete and verified.

## Verify Steps

- `python3 scripts/competitor_snapshot_builder.py --client-slug <client> --scaffold`
- `python3 scripts/competitor_snapshot_builder.py --client-slug <client>`

## Rollback Plan

- Revert the commit; remove the script if it causes workflow issues.

## Notes

- The scaffold input file documents expected fields and keeps data sourcing explicit.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- `.codex-swarm/tasks/202601150638-HSN5BY/README.md`
- `.codex-swarm/tasks/202601150638-HSN5BY/pr/diffstat.txt`
- `.codex-swarm/tasks/202601150638-HSN5BY/pr/meta.json`
- `.codex-swarm/tasks/202601150638-HSN5BY/pr/review.md`
- `.codex-swarm/tasks/202601150638-HSN5BY/pr/verify.log`
- `scripts/competitor_snapshot_builder.py`
<!-- END AUTO SUMMARY -->
