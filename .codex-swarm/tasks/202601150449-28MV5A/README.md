---
id: "202601150449-28MV5A"
title: "Execute SEO swarm workflow for HighPoint HVAC"
status: "DOING"
priority: "P1"
owner: "ORCHESTRATOR"
depends_on: []
tags: ["seo", "docs", "content"]
verify: [".venv/bin/python scripts/swarm_workflow.py --help"]
doc_version: 2
doc_updated_at: "2026-01-15T06:29:59+00:00"
doc_updated_by: "agentctl"
description: "Run docs/seo/swarm-execution-workflow.md end-to-end using approved inputs (with placeholders for missing proof/measurement), scaffold outputs/highpoint, draft cycle deliverables, and pass docs/release-checklist.md sanity checks."
---
## Summary

Execute the SEO swarm workflow for HighPoint HVAC, producing updated drafts and workflow artifacts under outputs/highpoint using approved inputs and site-sourced FAQ content.

## Scope

- Updated outputs/highpoint drafts with pricing proof points and FAQ answers sourced from non-blog site pages.
- Produced FAQ audit artifacts for non-blog pages.
- Added FAQ audit helper script in scripts/faq_audit.py.

## Risks

- Pricing/FAQ claims must stay aligned to the cited pages; revalidate before publishing.
- Measurement, competitors, and tracking inputs remain placeholders and require approved data.

## Verify Steps

- Run .venv/bin/python scripts/swarm_workflow.py --help (completed).
- Confirm outputs/highpoint drafts and reports updated with FAQ answers and proof points (completed).

## Rollback Plan

- Revert commit 81e1dc179b2e if needed.
- Discard local outputs/highpoint changes (outputs/ is ignored by git).

## Notes

- Updated drafts in outputs/highpoint with verified pricing proof points and FAQ answers from site pages.
- Generated FAQ audit report at outputs/highpoint/reports/faq-audit.json and FAQ extract at outputs/highpoint/reports/faq-extract.md.
- Added scripts/faq_audit.py to crawl the site and extract FAQ questions from non-blog pages.
- Measurement inputs and competitor/rank tracking remain placeholders pending confirmed data.

