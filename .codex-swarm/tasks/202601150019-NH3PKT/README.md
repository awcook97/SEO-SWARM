---
id: "202601150019-NH3PKT"
title: "Define HighPoint HVAC swarm roles"
status: "DONE"
priority: "med"
owner: "DOCS"
depends_on: ["[\"202601150018-R48DCR\"]"]
tags: []
commit: { hash: "123a250fcff2cf605e0cfee293e3da5e33e02f2d", message: "✨ NH3PKT add HighPoint HVAC swarm roles spec with handoffs and guardrails" }
comments:
  - { author: "DOCS", body: "verified: role roster and handoffs documented in docs/highpoint-hvac/swarm-roles.md | details: no tests run (docs-only)." }
doc_version: 2
doc_updated_at: "2026-01-15T00:24:42+00:00"
doc_updated_by: "agentctl"
description: "Specify agent roster, responsibilities, inputs/outputs, and handoffs for the HighPoint HVAC local SEO swarm."
---
## Summary

Defined the local SEO swarm role roster, responsibilities, and handoffs for HighPoint HVAC.

## Context

HighPoint HVAC is the target local business; this role definition anchors downstream webpage and article templates for local SEO.

## Scope

Add a documented swarm role roster with responsibilities, inputs/outputs, handoffs, and guardrails at @docs/highpoint-hvac/swarm-roles.md.

## Risks

Risk: roles imply data that is not yet available. Mitigation: require approved inputs and avoid unverified claims in role outputs.

## Verify Steps

1) Confirm @docs/highpoint-hvac/swarm-roles.md exists. 2) Review role roster and handoff flow for clarity and alignment.

## Rollback Plan

Revert the commit that adds the swarm role spec file.

## Notes

Roles are generic; adapt once HighPoint HVAC confirms services, service areas, and compliance constraints.

