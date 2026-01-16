---
id: "202601161958-DFC3CY"
title: "Add user-agent option to crawl cache"
status: "DOING"
priority: "med"
owner: "CODER"
depends_on: []
tags: []
comments:
  - { author: "CODER", body: "Start: add user-agent flag and reuse headers in crawl_cache requests." }
doc_version: 2
doc_updated_at: "2026-01-16T19:58:23+00:00"
doc_updated_by: "agentctl"
description: "Allow crawl_cache to set a custom User-Agent and reuse headers in sitemap/home discovery to avoid 403."
---
## Summary

Add a configurable User-Agent flag and use headers during sitemap/home discovery.

## Scope

- Add `--user-agent` CLI flag to `scripts/crawl_cache.py`.
- Use the same headers for sitemap and homepage discovery requests.
- Remove unused imports if present.

## Risks

- Some sites may still block requests regardless of user-agent.

## Verify Steps

- Run the crawl command against a known site and confirm no immediate 403.

## Rollback Plan

- Revert the crawl_cache changes.
