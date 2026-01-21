---
id: "202601150642-34TXH1"
title: "Automate compliance risk log"
status: "DOING"
priority: "med"
owner: "CODER"
depends_on: []
tags: []
comments:
  - { author: "CODER", body: "Start: implement compliance risk log tool for drafts using swarm role guidelines." }
doc_version: 2
doc_updated_at: "2026-01-21T18:05:36+00:00"
doc_updated_by: "agentctl"
description: "Create a tool that compiles a risk log for drafts: missing sources, placeholders, or unverified claims, per docs/client-templates/swarm-roles.md."
---
# 202601150642-34TXH1: Automate compliance risk log

## Summary

- Add `scripts/compliance_risk_log.py` to generate a risk log for draft markdown files.

## Context

- The Editor and Compliance role requires a risk log that flags placeholders, missing sources, and risky claims.
- Drafts live under `outputs/<client>/pages` and `outputs/<client>/articles`.

## Scope

- New script: `scripts/compliance_risk_log.py`.
- Inputs: draft markdown files under `outputs/<client>/pages` and `outputs/<client>/articles`.
- Outputs: `outputs/<client>/reports/compliance-risk-log.md` and `compliance-risk-log.json`.

## Risks

- Heuristic checks can produce false positives; the log is for review, not automatic enforcement.

## Verify Steps

- `python3 scripts/compliance_risk_log.py --client-slug <client>`
- `python3 scripts/compliance_risk_log.py --client-slug <client> --paths pages articles`

## Rollback Plan

- Revert the commit; remove the script if it creates noise in workflow.

## Notes

- The script reuses the NAP parser to confirm business name/phone are present in drafts.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- `.codex-swarm/tasks/202601150642-34TXH1/README.md`
- `.codex-swarm/tasks/202601150642-34TXH1/pr/diffstat.txt`
- `.codex-swarm/tasks/202601150642-34TXH1/pr/meta.json`
- `.codex-swarm/tasks/202601150642-34TXH1/pr/review.md`
- `.codex-swarm/tasks/202601150642-34TXH1/pr/verify.log`
- `scripts/compliance_risk_log.py`
<!-- END AUTO SUMMARY -->
