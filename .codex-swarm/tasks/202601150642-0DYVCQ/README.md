---
id: "202601150642-0DYVCQ"
title: "Automate technical SEO audit scaffold"
status: "DOING"
priority: "med"
owner: "CODER"
depends_on: []
tags: []
comments:
  - { author: "CODER", body: "Start: add technical SEO audit scaffold generator and docs." }
doc_version: 2
doc_updated_at: "2026-01-15T06:42:36+00:00"
doc_updated_by: "agentctl"
description: "Create a tool to scaffold technical SEO audits from sitemap/Core Web Vitals inputs and output prioritized fix lists."
---
## Summary

Add a technical SEO audit scaffold generator with markdown and JSON outputs.

## Scope

- Generate a reusable audit template with key technical sections.
- Output to `outputs/<client>/reports/technical-seo-audit.*`.
- Document usage and add unit tests.

## Risks

- Scaffold requires manual input of crawl/performance findings.

## Verify Steps

- Run `python3 -m unittest discover -s tests` (passes).

## Rollback Plan

- Revert the audit scaffold script, docs, and tests.
