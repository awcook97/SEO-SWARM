---
id: "202601150036-GNY4PM"
title: "Enforce schema requirement in templates"
status: "DONE"
priority: "med"
owner: "DOCS"
depends_on: []
tags: []
commit: { hash: "4c00f0de914dbf0033f236ced91f3e19b5cd6e8d", message: "✨ GNY4PM require schema in HighPoint HVAC template docs" }
comments:
  - { author: "DOCS", body: "verified: schema requirement marked as required in webpage and article template docs | details: no tests run (docs-only)." }
doc_version: 2
doc_updated_at: "2026-01-15T00:43:39+00:00"
doc_updated_by: "agentctl"
description: "Update HighPoint HVAC webpage and article templates to require schema on every page."
---
## Summary

Enforced required schema guidance across webpage and article templates.

## Context

User requested schema be required on every template page.

## Scope

Update @docs/highpoint-hvac/webpage-templates.md and @docs/highpoint-hvac/article-templates.md to mark schema as required.

## Risks

Risk: none; change is documentation only and reinforces existing intent.

## Verify Steps

1) Confirm schema is marked as required in both template docs. 2) Ensure no schema guidance was removed.

## Rollback Plan

Revert the commit that updates schema guidance in the template docs.

## Notes

Schema is now explicitly required for every template page.

