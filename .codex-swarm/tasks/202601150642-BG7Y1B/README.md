---
id: "202601150642-BG7Y1B"
title: "Automate SERP insights summary"
status: "DOING"
priority: "med"
owner: "CODER"
depends_on: []
tags: []
comments:
  - { author: "CODER", body: "Start: implement SERP insights summary tool based on approved exports with no fabrication." }
doc_version: 2
doc_updated_at: "2026-01-21T18:06:27+00:00"
doc_updated_by: "agentctl"
description: "Create a tool to summarize SERP patterns and competitor gaps from approved SERP exports/URLs without fabricating data, aligned to docs/client-templates/swarm-roles.md."
---
# 202601150642-BG7Y1B: Automate SERP insights summary

## Summary

- Add `scripts/serp_insights_summary.py` to generate SERP pattern notes and competitor gap summaries from structured inputs.

## Context

- The Competitor and SERP Analyst role requires clear, sourced insights without fabricated data.
- A structured input JSON keeps the tool tool-agnostic and prevents unsupported claims.

## Scope

- New script: `scripts/serp_insights_summary.py`.
- Input: `outputs/<client>/reports/serp-insights-input.json` (or `--input` override).
- Outputs: `outputs/<client>/reports/serp-insights-summary.md` and `serp-insights-summary.json`.

## Risks

- Insights are only as good as the approved exports; ensure inputs include timestamps and sources.

## Verify Steps

- `python3 scripts/serp_insights_summary.py --client-slug <client> --scaffold`
- `python3 scripts/serp_insights_summary.py --client-slug <client>`

## Rollback Plan

- Revert the commit; remove the script if it conflicts with reporting workflows.

## Notes

- Use the scaffold JSON to document sources explicitly and avoid unverified claims.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- `.codex-swarm/tasks/202601150642-BG7Y1B/README.md`
- `.codex-swarm/tasks/202601150642-BG7Y1B/pr/diffstat.txt`
- `.codex-swarm/tasks/202601150642-BG7Y1B/pr/meta.json`
- `.codex-swarm/tasks/202601150642-BG7Y1B/pr/review.md`
- `.codex-swarm/tasks/202601150642-BG7Y1B/pr/verify.log`
- `scripts/serp_insights_summary.py`
<!-- END AUTO SUMMARY -->
