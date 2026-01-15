---
id: "202601150449-28MV5A"
title: "Execute SEO swarm workflow for HighPoint HVAC"
status: "TODO"
priority: "P1"
owner: "ORCHESTRATOR"
depends_on: []
tags: ["seo", "docs", "content"]
verify: [".venv/bin/python scripts/swarm_workflow.py --help"]
doc_version: 2
doc_updated_at: "2026-01-15T04:49:48+00:00"
doc_updated_by: "agentctl"
description: "Run docs/seo/swarm-execution-workflow.md end-to-end using approved inputs (with placeholders for missing proof/measurement), scaffold outputs/highpoint, draft cycle deliverables, and pass docs/release-checklist.md sanity checks."
---

# Summary

Execute the reusable SEO swarm workflow for HighPoint HVAC, producing one cycle of draft deliverables under `outputs/highpoint/` using approved inputs and placeholders where measurement/proof details are not yet approved.

# Context

- Workflow source: `docs/seo/swarm-execution-workflow.md`
- Templates: `docs/client-templates/webpage-templates.md`, `docs/client-templates/article-templates.md`
- Measurement requirements: `docs/seo/measurement-spec.md` and `docs/seo/measurement-intake-template.md`
- Approved inputs captured in: `outputs/highpoint/inputs.md`

# Scope

- Scaffold `outputs/highpoint/` using `scripts/swarm_workflow.py`
- Draft cycle deliverables (service page, local landing page, topical blog post, social posts, subscriber email)
- Add placeholder measurement artifacts (rank tracking report + competitor snapshot format)
- Run `docs/release-checklist.md` sanity checks that apply in-repo

# Risks

- Placeholders must be replaced with approved proof points, keyword targets, competitors, and ranking exports before publishing.
- Address/NAP and any superlative/quantified claims are intentionally omitted until sources are approved.

# Verify Steps

- Run `./.venv/bin/python scripts/swarm_workflow.py --help` without error.
- Confirm `outputs/highpoint/` contains drafts and `reports/` placeholders.
- Confirm `outputs/` is ignored by git and contains no committed client data.

# Rollback Plan

- Revert any committed changes via `git revert <commit>`.
- Delete `outputs/highpoint/` locally if needed (folder is ignored by git).

# Notes

- This task intentionally uses placeholders for measurement inputs and proof points per user instruction.
