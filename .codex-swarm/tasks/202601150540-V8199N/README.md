---
id: "202601150540-V8199N"
title: "Define SEO swarm role agents"
status: "TODO"
priority: "P2"
owner: "ORCHESTRATOR"
depends_on: []
tags: ["docs", "agents"]
doc_version: 2
doc_updated_at: "2026-01-15T05:40:26+00:00"
doc_updated_by: "agentctl"
description: "Expand docs/client-templates/swarm-roles.md with actionable role definitions and add corresponding specialist agent profiles under .codex-swarm/agents/ for local SEO execution."
---

# Summary

Add “ready-to-run” role playbooks to the local SEO swarm roles doc and create matching specialist agent profiles under `.codex-swarm/agents/` to support execution handoffs.

# Context

- Roles doc: `docs/client-templates/swarm-roles.md`
- Agent profiles live in: `.codex-swarm/agents/`
- Canonical workflow context: `docs/seo/swarm-execution-workflow.md`

# Scope

- Extend `docs/client-templates/swarm-roles.md` with concise playbooks for core roles and pointers to optional Codex agent profiles.
- Add agent profiles for strategy, SERP analysis, GBP planning, content planning, copywriting, compliance editing, and reporting.

# Risks

- Agent roles must not encourage scraping or fabricating facts; they should require approved inputs and use placeholders when missing.
- Role docs must stay client-agnostic and reusable across engagements.

# Verify Steps

- Run `./.venv/bin/python .codex-swarm/agentctl.py agents` and confirm new IDs appear.
- Confirm the new JSON files in `.codex-swarm/agents/` parse cleanly.

# Rollback Plan

- Revert the commit and delete the added `.codex-swarm/agents/*.json` files.

# Notes

- No changes are made to task backends or automation; this is docs + agent-profile scaffolding only.
