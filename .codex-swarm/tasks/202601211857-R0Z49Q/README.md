---
id: "202601211857-R0Z49Q"
title: "Automate metadata linkmap inputs"
status: "DONE"
priority: "med"
owner: "CODER"
depends_on: ["202601211855-FAJDQP"]
tags: ["automation", "metadata"]
commit: { hash: "870526ddc6af0eeb2085b64fa9c1d6884c718ea5", message: "🧩 202601211857-R0Z49Q integrate task/202601211857-R0Z49Q/metadata" }
comments:
  - { author: "INTEGRATOR", body: "verified: Integrated via squash | details: verify=skipped(no commands); pr=.codex-swarm/tasks/202601211857-R0Z49Q/pr." }
  - { author: "INTEGRATOR", body: "verified: Integrated metadata linkmap ingest." }
doc_version: 2
doc_updated_at: "2026-01-21T22:58:51+00:00"
doc_updated_by: "agentctl"
description: "Automate generating metadata-linkmap-input.json from existing site info or CMS exports."
---
# 202601211857-R0Z49Q: Automate metadata linkmap inputs

## Summary

Generate metadata/internal link map inputs from a page plan CSV.

## Context

- ...

## Scope

Add metadata linkmap ingest script and unit tests.

## Risks

Page plan CSV must include required fields; rows without type/slug are skipped.

## Verify Steps

1) /home/andrew/projects/codex-swarm/.venv/bin/python tests/test_metadata_linkmap_ingest.py\n2) python scripts/metadata_linkmap_ingest.py --client-slug <client> --input <plan.csv> --client-name <name> --client-phone <phone>

## Rollback Plan

Revert commit(s) adding metadata_linkmap_ingest.py and related tests.

## Notes

- ...

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- `README.md`
- `scripts/metadata_linkmap_ingest.py`
- `tests/test_metadata_linkmap_ingest.py`
<!-- END AUTO SUMMARY -->

