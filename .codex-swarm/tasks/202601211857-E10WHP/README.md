---
id: "202601211857-E10WHP"
title: "Automate crawl capture ingest"
status: "TODO"
priority: "med"
owner: "CODER"
depends_on: ["202601211855-FAJDQP"]
tags: ["automation", "crawl"]
doc_version: 2
doc_updated_at: "2026-01-21T22:58:06+00:00"
doc_updated_by: "agentctl"
description: "Automate site crawl collection into outputs/<client>/reports/site-cache/index.json (replace manual crawl)."
---
# 202601211857-E10WHP: Automate crawl capture ingest

## Summary

Convert crawl exports into normalized JSON and summary counts.

## Context

- ...

## Scope

Add crawl export ingest script, summary output, and tests.

## Risks

Crawl exports may omit expected columns; missing fields default to empty or zero.

## Verify Steps

1) /home/andrew/projects/codex-swarm/.venv/bin/python tests/test_crawl_export_ingest.py\n2) python scripts/crawl_export_ingest.py --client-slug <client> --input <export.csv> --summary

## Rollback Plan

Revert commit(s) adding crawl_export_ingest.py and related tests.

## Notes

- ...

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- `README.md`
- `scripts/crawl_export_ingest.py`
- `tests/test_crawl_export_ingest.py`
<!-- END AUTO SUMMARY -->

