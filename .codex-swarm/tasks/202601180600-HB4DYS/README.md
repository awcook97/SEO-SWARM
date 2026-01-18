---
id: "202601180600-HB4DYS"
title: "Generate JSON-LD schema from cached pages"
status: "DONE"
priority: "med"
owner: "CODER"
depends_on: []
tags: []
commit: { hash: "971e1d695f0499c1140f181414cc83b277808f3d", message: "✨ HB4DYS add cache schema generator for cached pages; document usage; update SEO docs index" }
comments:
  - { author: "CODER", body: "Start: inspect cache inputs and existing schema tooling; implement JSON-LD generator script." }
  - { author: "CODER", body: "verified: not run (no cached outputs available) | details: reviewed generator logic, output paths, and doc updates for completeness." }
doc_version: 2
doc_updated_at: "2026-01-18T06:05:18+00:00"
doc_updated_by: "agentctl"
description: "Add a script that reads cached site pages and outputs a single JSON-LD script per page, aligned with Google Search Appearance best practices."
---
## Summary

Add a cache-driven JSON-LD generator that emits one schema script per page and documents usage.

## Scope

Create scripts/cache_schema_generator.py to read cached HTML and output JSON-LD scripts under outputs/<client>/gen-schema/website-tree, plus add a brief doc entry in @docs/seo.

## Risks

Schema output relies on available on-page metadata; sparse pages may yield minimal nodes or non-ideal titles.

## Verify Steps

Run: python scripts/cache_schema_generator.py --client-slug <client> (with cached pages present) and confirm per-page HTML snippets are written under outputs/<client>/gen-schema/website-tree/.

## Rollback Plan

Revert the commit to remove the generator and documentation changes.

