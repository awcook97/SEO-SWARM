---
id: "202601150638-WETYHE"
title: "Automate draft compliance lint"
status: "DONE"
priority: "med"
owner: "CODER"
depends_on: []
tags: []
commit: { hash: "17a1ddf806df2d5827b36608ed391b1a6943e917", message: "✨ WETYHE add draft compliance lint" }
comments:
  - { author: "CODER", body: "verified: added draft compliance lint and ran unittest suite." }
doc_version: 2
doc_updated_at: "2026-01-15T06:38:44+00:00"
doc_updated_by: "agentctl"
description: "Build a linter that scans outputs/<client>/ drafts for placeholders, missing schema blocks (Service/LocalBusiness/FAQPage/Article), and NAP consistency issues per docs/client-templates/*.md and docs/seo/swarm-execution-workflow.md."
---
## Summary

Add a draft compliance lint script to flag placeholders and risky claims.

## Scope

- Scan draft markdown files under `outputs/<client>/pages` and `outputs/<client>/articles`.
- Flag placeholders, TODOs, and risky claims.
- Emit markdown and JSON reports under `outputs/<client>/reports/`.
- Add documentation and unit tests.

## Risks

- Heuristic claim detection may flag legitimate, sourced statements.

## Verify Steps

- Run `python3 -m unittest discover -s tests` (passes).

## Rollback Plan

- Revert the lint script, docs, and tests.

