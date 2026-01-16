---
id: "202601160538-DY6Z96"
title: "Expand swarm role playbooks and agent profiles"
status: "DONE"
priority: "med"
owner: "DOCS"
depends_on: []
tags: []
commit: { hash: "1511bcf848971450d2c204cedcc40267cd64c938", message: "✨ DY6Z96 add role playbooks and agent profiles" }
comments:
  - { author: "DOCS", body: "verified: Added playbooks for remaining swarm roles and created matching agent profiles with approved-input guardrails and outputs for each role." }
  - { author: "DOCS", body: "verified: synced cloud-generated role playbooks and agent profiles to tracked commit." }
doc_version: 2
doc_updated_at: "2026-01-16T05:39:39+00:00"
doc_updated_by: "agentctl"
description: "Add missing role playbooks to docs/client-templates/swarm-roles.md and create corresponding agent JSON profiles under .codex-swarm/agents/."
---
## Summary

Add role playbooks for remaining local SEO swarm roles and create matching agent profiles.

## Context

Roles doc lives at docs/client-templates/swarm-roles.md; agent profiles live under .codex-swarm/agents/.

## Scope

- Add playbooks for Service Researcher, On-Page SEO Specialist, Technical SEO Auditor, Citation Manager, Review and Reputation, and Local Link Builder.\n- Add corresponding agent JSON profiles for each role.

## Risks

- Roles must require approved inputs and avoid unverified claims.\n- Agent profiles must stay client-agnostic and consistent with the swarm workflow.

## Verify Steps

- Confirm new playbooks exist in docs/client-templates/swarm-roles.md.\n- Confirm new JSON files under .codex-swarm/agents/ parse cleanly.

## Rollback Plan

- Revert the commit and remove the added .codex-swarm/agents/*.json files.

## Notes

No external data required; all changes are docs and agent scaffolding.

