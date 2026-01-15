---
id: "202601150046-Q6HB8K"
title: "Add rank tracking and competitor inputs to templates"
status: "DONE"
priority: "med"
owner: "DOCS"
depends_on: ["[\"202601150018-R48DCR\"]"]
tags: []
commit: { hash: "64c1aafe5d3f7307032570f658ebb61de7c0a64d", message: "✨ Q6HB8K add rank tracking and competitor inputs to templates" }
comments:
  - { author: "DOCS", body: "verified: rank tracking and competitor input placeholders added to webpage and article templates | details: no tests run (docs-only)." }
doc_version: 2
doc_updated_at: "2026-01-15T00:50:38+00:00"
doc_updated_by: "agentctl"
description: "Update HighPoint HVAC webpage and article templates to accept rank tracking and competitor analysis parameters."
---
## Summary

Added rank tracking and competitor analysis input placeholders to webpage and article templates.

## Context

Future rank tracking and competitor analysis should be captured as structured inputs for all templates.

## Scope

Update @docs/highpoint-hvac/webpage-templates.md and @docs/highpoint-hvac/article-templates.md inputs to include rank tracking targets and competitor sets.

## Risks

Risk: placeholders could be mistaken for required data early on. Mitigation: keep as optional inputs and align with strategist/analyst workflow.

## Verify Steps

1) Confirm rank tracking and competitor inputs appear in both template docs. 2) Ensure no existing template sections were removed.

## Rollback Plan

Revert the commit that adds rank tracking and competitor inputs.

## Notes

Inputs are placeholders and can be filled once rank tracking and SERP data are available.

