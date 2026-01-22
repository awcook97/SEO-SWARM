---
id: "202601180735-Y4CG1A"
title: "Align schema output to schemaorg-current-https.jsonld"
status: "DONE"
priority: "P1"
owner: "ORCHESTRATOR"
depends_on: []
tags: ["schema", "seo", "workflow"]
commit: { hash: "73550639803691a1339f1efd5759dfb284ce78ce", message: "🧩 202601180735-Y4CG1A integrate task/202601180735-Y4CG1A/schemaorg-align" }
comments:
  - { author: "INTEGRATOR", body: "verified: Integrated via squash | details: verify=skipped(no commands); pr=.codex-swarm/tasks/202601180735-Y4CG1A/pr." }
  - { author: "INTEGRATOR", body: "verified: Integrated via squash | details: verify=skipped(no commands); pr=.codex-swarm/tasks/202601180735-Y4CG1A/pr." }
doc_version: 2
doc_updated_at: "2026-01-21T23:51:38+00:00"
doc_updated_by: "agentctl"
description: "Use downloaded schemaorg-current-https.jsonld as strict reference; define boilerplate+spotcheck workflow and update generator/agent docs accordingly."
---
## Summary

Add optional schema.org snapshot validation to cache schema generator output.

## Scope

Introduce --validate-schemaorg option and skip invalid pages based on snapshot validation.

## Risks

Validation may skip pages with existing schema issues; ensure snapshot path is correct.

## Verify Steps

1) Run cache_schema_generator.py --validate-schemaorg\n2) Confirm invalid pages are skipped with warnings

## Rollback Plan

Revert cache_schema_generator.py validation changes.

