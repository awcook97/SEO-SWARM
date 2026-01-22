---
id: "202601221537-TDGCTP"
title: "Compliance risk log: fix import path after scripts restructure"
status: "DONE"
priority: "med"
owner: "ORCHESTRATOR"
depends_on: []
tags: []
commit: { hash: "eabf1b12e561bf8d7778f8b4254126413877e4aa", message: "🐛 TDGCTP fix compliance risk import path" }
comments:
  - { author: "ORCHESTRATOR", body: "verified: not run | details: compliance risk log now resolves validation imports." }
doc_version: 2
doc_updated_at: "2026-01-22T15:58:46+00:00"
doc_updated_by: "agentctl"
description: "Update compliance_risk_log.py to import draft_compliance_lint from scripts/validation or use module relative import."
---
## Summary

Fix compliance_risk_log import path after scripts restructure.

## Context

compliance_risk_log fails to import draft_compliance_lint after moving scripts into validation/.

## Scope

Update compliance_risk_log to resolve imports from scripts/validation.

## Risks

Modifying sys.path could mask other import issues; only adds the validation dir.

## Verify Steps

Run compliance_risk_log.py with a client slug and confirm it completes without import errors.

## Rollback Plan

Revert to the previous import if the module path is restored.

## Notes

compliance_risk_log now adds scripts/validation to sys.path before importing draft_compliance_lint.

