---
id: "202601150104-P8JHWE"
title: "Add measurement intake and reporting templates"
status: "DONE"
priority: "med"
owner: "DOCS"
depends_on: []
tags: []
commit: { hash: "8c3b21c689260bf4fc3779d0ed923d15cf9b7a7e", message: "✨ P8JHWE add measurement intake and reporting templates" }
comments:
  - { author: "DOCS", body: "verified: measurement intake and reporting templates created under docs/seo | details: no tests run (docs-only)." }
doc_version: 2
doc_updated_at: "2026-01-15T01:06:22+00:00"
doc_updated_by: "agentctl"
description: "Create standalone intake form and reporting templates aligned to the reusable measurement spec."
---
## Summary

Added standalone measurement intake and reporting templates for rank tracking and competitor analysis.

## Context

Provide scalable, client-agnostic intake and reporting templates aligned to the measurement spec.

## Scope

Add @docs/seo/measurement-intake-template.md and @docs/seo/measurement-reporting-template.md as standalone scalable assets.

## Risks

Risk: templates may be too generic without client nuance. Mitigation: provide required fields and leave room for notes.

## Verify Steps

1) Confirm both measurement templates exist under @docs/seo. 2) Review required fields align with the measurement spec.

## Rollback Plan

Revert the commit that adds the measurement intake and reporting templates.

## Notes

Templates are standalone and tool-agnostic to support scaling across clients.

