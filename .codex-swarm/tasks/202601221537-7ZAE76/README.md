---
id: "202601221537-7ZAE76"
title: "Audit runner: handle missing inputs for export ingest steps"
status: "DONE"
priority: "med"
owner: "ORCHESTRATOR"
depends_on: []
tags: []
commit: { hash: "a239e906ffd7cbb3867ef1f3bc5a067ffb90bd7d", message: "🔧 7ZAE76 skip ingest steps when exports missing" }
comments:
  - { author: "ORCHESTRATOR", body: "verified: not run | details: change only adds input-existence guards in the audit runner." }
doc_version: 2
doc_updated_at: "2026-01-22T15:52:37+00:00"
doc_updated_by: "agentctl"
description: "Adjust site_audit_runner to skip or scaffold when required --input files are missing for crawl/gsc/ga4/gbp/citation/rank-tracker ingest steps, or accept optional paths."
---
## Summary

Skip export ingest steps in site_audit_runner when required input files are missing.

## Context

Autorunner failed when ingest scripts required --input. We need to detect missing exports and skip with a warning.

## Scope

Add file existence checks and pass --input for crawl, GSC, GA4, GBP, citation audit, and rank tracker export ingests.

## Risks

Skipping steps could hide missing exports; warnings are logged to surface gaps.

## Verify Steps

Run site_audit_runner with missing exports and confirm ingest steps are skipped with warnings, not failures.

## Rollback Plan

Revert the runner changes to restore strict failure on missing inputs.

## Notes

Runner now searches common export filenames and injects --input when present; otherwise logs a skip.

