---
id: "202601160320-1BC28K"
title: "Implement brief summary generator"
status: "DONE"
priority: "med"
owner: "CODER"
depends_on: ["202601160320-AY535W"]
tags: []
commit: { hash: "289430d143ad5a2bf20406dea900a0037ca8e12b", message: "✨ 1BC28K add service brief summary generator" }
comments:
  - { author: "CODER", body: "verified: ran unittest suite and captured verify log for summary generator." }
doc_version: 2
doc_updated_at: "2026-01-16T03:20:52+00:00"
doc_updated_by: "agentctl"
description: "Create script to aggregate service briefs into a summary report for onboarding."
---
## Summary

Provide a script that aggregates service brief markdown files into summary
markdown and JSON reports.

## Scope

- Parse brief sections (headings, CTAs, internal links, schema types, FAQs).
- Generate `service-briefs-summary.md` and `service-briefs-summary.json`.
- Emit basic aggregation counts plus per-page snapshots.

## Risks

- Briefs that deviate from the expected section markers may be partially parsed.

## Verify Steps

- Run `python3 -m unittest discover -s tests` (passes).

## Rollback Plan

- Revert the summary report generator script commit(s).

