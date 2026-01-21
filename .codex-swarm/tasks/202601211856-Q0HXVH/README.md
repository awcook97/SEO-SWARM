---
id: "202601211856-Q0HXVH"
title: "Automate SERP data fetch (DataForSEO)"
status: "DONE"
priority: "P1"
owner: "CODER"
depends_on: ["202601211855-FAJDQP"]
tags: ["automation", "serp"]
commit: { hash: "a75697fa921088fc7fc1089137f6d55d1ec4f09c", message: "🧩 202601211856-Q0HXVH integrate task/202601211856-Q0HXVH/serp" }
comments:
  - { author: "INTEGRATOR", body: "verified: Integrated via squash | details: verify=skipped(no commands); pr=.codex-swarm/tasks/202601211856-Q0HXVH/pr." }
  - { author: "INTEGRATOR", body: "verified: Integrated DataForSEO SERP fetch updates." }
doc_version: 2
doc_updated_at: "2026-01-21T23:03:53+00:00"
doc_updated_by: "agentctl"
description: "Create a DataForSEO-backed SERP fetcher to generate serp-insights-input.json and competitor-snapshot-input.json."
---
# 202601211856-Q0HXVH: Automate SERP data fetch (DataForSEO)

## Summary

Add scaffolding and tests for DataForSEO SERP fetch automation.

## Context

- ...

## Scope

Add SERP fetch input scaffold, update docs, and add unit tests.

## Risks

Requires DataForSEO credentials and a valid endpoint; API failures will stop the run.

## Verify Steps

1) /home/andrew/projects/codex-swarm/.venv/bin/python tests/test_serp_dataforseo_fetch.py\n2) python scripts/serp_dataforseo_fetch.py --client-slug <client> --scaffold

## Rollback Plan

Revert commit(s) updating serp_dataforseo_fetch.py and tests.

## Notes

- ...

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- `.codex-swarm/tasks/202601211856-Q0HXVH/README.md`
- `.codex-swarm/tasks/202601211856-Q0HXVH/pr/diffstat.txt`
- `.codex-swarm/tasks/202601211856-Q0HXVH/pr/meta.json`
- `README.md`
- `scripts/serp_dataforseo_fetch.py`
- `tests/test_serp_dataforseo_fetch.py`
<!-- END AUTO SUMMARY -->

