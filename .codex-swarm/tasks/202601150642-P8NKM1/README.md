---
id: "202601150642-P8NKM1"
title: "Automate local link outreach log"
status: "DOING"
priority: "med"
owner: "CODER"
depends_on: []
tags: []
comments:
  - { author: "CODER", body: "Start: automate local link outreach log generator with target + status tracking." }
doc_version: 2
doc_updated_at: "2026-01-15T06:42:35+00:00"
doc_updated_by: "agentctl"
description: "Create a generator for local link builder outreach targets and tracking log templates."
---
## Summary

Generate a local link outreach log report capturing organization, contact, status, and priority.

## Scope

- Add `scripts/local_link_outreach.py` with scaffolded JSON input.
- Emit markdown and JSON reports under `outputs/<client>/reports/`.
- Document usage and add unit tests.

## Risks

- Outreach targets must stay approved; incorrect contacts or URLs could waste effort.

## Verify Steps

- Run `python3 -m unittest discover -s tests` (passes).

## Rollback Plan

- Revert the local link outreach script, docs, and tests.
