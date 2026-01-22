---
id: "202601221537-TYKQP3"
title: "Rank tracking report: skip when CSV missing in audit runner"
status: "TODO"
priority: "med"
owner: "ORCHESTRATOR"
depends_on: []
tags: []
doc_version: 2
doc_updated_at: "2026-01-22T15:57:10+00:00"
doc_updated_by: "agentctl"
description: "When rank-tracking.csv is missing, the audit runner should either skip the report or only scaffold config without failing."
---
## Summary

Skip rank tracking report in site_audit_runner when rank-tracking.csv is missing.

## Context

Autorunner fails when rank-tracking.csv is missing; it should skip instead of erroring.

## Scope

Add a file existence check in site_audit_runner before running rank_tracking_report_builder.

## Risks

Skipping the report may hide missing rank tracking data; warning output signals the gap.

## Verify Steps

Run site_audit_runner without rank-tracking.csv and confirm the step is skipped with a warning.

## Rollback Plan

Revert the runner change to enforce the report even when the CSV is missing.

## Notes

Rank tracking report now runs only when rank-tracking.csv exists.

