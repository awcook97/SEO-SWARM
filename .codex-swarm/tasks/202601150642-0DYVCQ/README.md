---
id: "202601150642-0DYVCQ"
title: "Automate technical SEO audit scaffold"
status: "DONE"
priority: "med"
owner: "CODER"
depends_on: []
tags: []
commit: { hash: "1f81760c2f103b05d4492c38e10e2d6f7e36f496", message: "✨ 0DYVCQ add technical SEO audit scaffold" }
comments:
  - { author: "CODER", body: "Start: add technical SEO audit scaffold generator and docs." }
  - { author: "CODER", body: "verified: added technical SEO audit scaffold and ran unittest suite." }
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

