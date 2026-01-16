---
id: "202601150639-7SA5CQ"
title: "Automate keyword map and KPI targets"
status: "DOING"
priority: "med"
owner: "CODER"
depends_on: []
tags: []
comments:
  - { author: "CODER", body: "Start: implement keyword map and KPI targets generator and docs." }
doc_version: 2
doc_updated_at: "2026-01-15T06:39:09+00:00"
doc_updated_by: "agentctl"
description: "Create a generator that produces keyword→URL map, service-area targets, SERP feature targets, and KPI cadence from approved inputs per docs/client-templates/swarm-roles.md."
---
## Summary

Generate a keyword map and KPI targets report from approved input JSON.

## Scope

- Add `scripts/keyword_map_kpi.py` with scaffoldable input format.
- Emit markdown and JSON reports under `outputs/<client>/reports/`.
- Document usage and add unit tests.

## Risks

- Inputs require manual fill-in for KPIs and keyword mapping details.

## Verify Steps

- Run `python3 -m unittest discover -s tests` (passes).

## Rollback Plan

- Revert the keyword map generator script, docs, and tests.

