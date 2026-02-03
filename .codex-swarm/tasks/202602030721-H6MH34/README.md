---
id: "202602030721-H6MH34"
title: "Phase 2 service brief program"
status: "DOING"
priority: "P1"
owner: "CODER"
depends_on: []
tags: ["code"]
verify: ["python scripts/workflow/runners/phase2_service_brief.py --help"]
comments:
  - { author: "CODER", body: "Start: Building Phase 2 service brief classes with gap analysis, outline, schema checklist, and report output." }
doc_version: 2
doc_updated_at: "2026-02-03T07:24:56+00:00"
doc_updated_by: "agentctl"
description: "Implement service brief classes, gap analysis, outline builder, and report output"
---
## Summary

Implemented Phase 2 service brief program with CrawlSnapshot ingestion, content gap analysis, outline builder, and schema checklist classes. Generates a structured Markdown + JSON service brief report from crawl exports.

## Scope

1. Added CrawlSnapshot, ContentGapAnalyzer, OutlineBuilder, SchemaChecklist classes
2. Implemented ServiceBriefProgram runner for reports
3. Added content gap detection, outline generation, and schema guidance
4. Ensured all functions <=20 lines for readability

## Risks

Low risk: new code is additive. Crawl export CSV headers may differ across tools and require field mapping adjustments.

## Verify Steps

1. Run: python scripts/workflow/runners/phase2_service_brief.py --help
2. Run with --crawl_csv and --service inputs plus client info
3. Verify outputs in data/outputs/<slug>/reports/service-brief.md and .json

## Rollback Plan

Revert commit 381ea8268e50 to remove Phase 2 service brief implementation.

