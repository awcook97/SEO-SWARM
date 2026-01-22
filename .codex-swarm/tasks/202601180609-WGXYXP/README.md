---
id: "202601180609-WGXYXP"
title: "Review Search Appearance best practices + single JSON-LD per page"
status: "TODO"
priority: "P1"
owner: "ORCHESTRATOR"
depends_on: []
tags: ["seo", "schema", "docs"]
verify: ["python3 -m pytest"]
doc_version: 2
doc_updated_at: "2026-01-21T23:42:58+00:00"
doc_updated_by: "agentctl"
description: "Inspect Google Search Appearance docs for best practices and ensure outputs use one JSON-LD script per page; run verification."
---
## Summary

Document Search Appearance best practices and single JSON-LD script guidance.

## Scope

Update schema approval and cache schema generator docs with Search Appearance checklist.

## Risks

If guidance is too strict, it could block valid multi-entity schemas; use @graph where necessary.

## Verify Steps

1) Review docs/seo/schema-approval-workflow.md\n2) Review docs/seo/cache-schema-generator.md

## Rollback Plan

Revert doc changes in schema-approval-workflow.md and cache-schema-generator.md.

