---
id: "202601211856-YVEF7N"
title: "Automate citation audit ingest"
status: "DONE"
priority: "med"
owner: "CODER"
depends_on: ["202601211855-FAJDQP"]
tags: ["automation", "citations"]
commit: { hash: "30dd84135f3ecb3972f49d0940faae8333de78ec", message: "🧩 202601211856-YVEF7N integrate task/202601211856-YVEF7N/citations" }
comments:
  - { author: "INTEGRATOR", body: "verified: Integrated via squash | details: verify=skipped(no commands); pr=.codex-swarm/tasks/202601211856-YVEF7N/pr." }
  - { author: "INTEGRATOR", body: "verified: Integrated citation audit ingest." }
doc_version: 2
doc_updated_at: "2026-01-21T22:56:26+00:00"
doc_updated_by: "agentctl"
description: "Automate pulling citation audit data into outputs/<client>/reports/citation-log-input.json."
---
# 202601211856-YVEF7N: Automate citation audit ingest

## Summary

Convert citation audit exports into citation log input JSON.

## Context

- ...

## Scope

Add citation audit ingest script and unit tests.

## Risks

Citation audits vary in structure; rows missing required fields are skipped.

## Verify Steps

1) /home/andrew/projects/codex-swarm/.venv/bin/python tests/test_citation_audit_ingest.py\n2) python scripts/citation_audit_ingest.py --client-slug <client> --input <export.csv>

## Rollback Plan

Revert commit(s) adding citation_audit_ingest.py and related tests.

## Notes

- ...

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- `README.md`
- `scripts/citation_audit_ingest.py`
- `tests/test_citation_audit_ingest.py`
<!-- END AUTO SUMMARY -->

