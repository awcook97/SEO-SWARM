---
id: "202602030713-Y48NPR"
title: "Phase 1 monthly performance program"
status: "DOING"
priority: "P1"
owner: "CODER"
depends_on: []
tags: ["code"]
verify: ["python scripts/workflow/runners/phase1_monthly_performance.py --help"]
comments:
  - { author: "CODER", body: "Start: Building Phase 1 classes (GA4/GBP/Rank/KPI/Opportunities) and report output with <=20 line functions." }
doc_version: 2
doc_updated_at: "2026-02-03T07:18:28+00:00"
doc_updated_by: "agentctl"
description: "Implement Phase 1 classes, report builder, and runner wiring"
---
## Summary

Implemented Phase 1 monthly performance program with dedicated GA4, GBP, rank tracker, KPI, and opportunity classes plus a report generator. Added orchestration logic that loads CSV exports, aggregates KPIs, ranks winners/losers, and produces Markdown + JSON outputs with safe table rendering and date parsing.

## Scope

1. Added Phase 1 OOP classes: GA4Report, GBPReport, RankTrackerReport, KPISummary, OpportunityFinder
2. Implemented MonthlyPerformanceProgram to generate JSON + Markdown report
3. Added CSV parsing, date filtering, KPI aggregation, and opportunity extraction
4. Ensured all functions are <=20 lines for readability

## Risks

Low risk: New Phase 1 code is additive and only runs when invoked. Input assumptions (CSV headers for GA4/GBP/rank) may need adjustments per client export formats.

## Verify Steps

1. Run: python scripts/workflow/runners/phase1_monthly_performance.py --help
2. Provide GA4/GBP/rank CSVs and run with --client-name, --client-slug, --output-dir
3. Verify outputs in data/outputs/<slug>/reports/monthly-performance-report.md and .json

## Rollback Plan

Revert commit 9b3900e2e1b3 if issues occur. This removes Phase 1 classes and runner without affecting existing workflows.

