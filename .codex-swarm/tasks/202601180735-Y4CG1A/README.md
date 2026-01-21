---
id: "202601180735-Y4CG1A"
title: "Align schema output to schemaorg-current-https.jsonld"
status: "DONE"
priority: "P1"
owner: "ORCHESTRATOR"
depends_on: []
tags: ["schema", "seo", "workflow"]
commit: { hash: "30c6847aa0686b71037c02040d63bcbc35d4ee34", message: "📝 Y4CG1A docs: document schema.org snapshot workflow verification" }
comments:
  - { author: "ORCHESTRATOR", body: "Start: audit schema generator + docs for schema.org snapshot alignment and update workflow artifacts as needed." }
  - { author: "ORCHESTRATOR", body: "verified: docs + strict schema.org snapshot workflow are in place | details: ran schema validator on outputs/highpoint-hvac/gen-schema/website-tree/index.html and it passed." }
doc_version: 2
doc_updated_at: "2026-01-21T16:51:22+00:00"
doc_updated_by: "agentctl"
description: "Use downloaded schemaorg-current-https.jsonld as strict reference; define boilerplate+spotcheck workflow and update generator/agent docs accordingly."
---
# 202601180735-Y4CG1A: Align schema output to schemaorg-current-https.jsonld

## Summary

- Enforce a strict schema.org reference workflow using `downloaded_files/schemaorg-current-https.jsonld` and the local validator script.
- Keep generator guidance aligned with the strict validator + boilerplate/spotcheck process.

## Context

- The schema generator emits per-page JSON-LD; correctness depends on using only schema.org-defined classes/properties and valid range values.
- This repo includes a pinned schema.org snapshot and a local validator to avoid “unknown property/type” drift.

## Scope

- Confirm `scripts/schema_org_validator.py` validates generator outputs against `downloaded_files/schemaorg-current-https.jsonld`.
- Confirm docs reference the strict workflow + boilerplate: `docs/seo/schema-approval-workflow.md`, `docs/seo/schema-boilerplate.jsonld`, `docs/seo/cache-schema-generator.md`.

## Risks

- Strict validation may surface existing output issues; fixes should be applied in the generator or inputs rather than weakening validation.

## Verify Steps

- `python3 scripts/schema_org_validator.py --input outputs/highpoint-hvac/gen-schema/website-tree/index.html`

## Rollback Plan

- Revert the commit for this task; re-run the validator to confirm prior behavior.

## Notes

- Keep `schemaorg-current-https.jsonld` as the canonical allowed-list; do not add properties/types that are not present in the snapshot.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- (no file changes)
<!-- END AUTO SUMMARY -->

