---
id: "202601180634-1CANR1"
title: "Harden cache schema generator against bad HTML"
status: "TODO"
priority: "P1"
owner: "ORCHESTRATOR"
depends_on: []
tags: ["seo", "schema", "automation"]
doc_version: 2
doc_updated_at: "2026-01-21T23:44:52+00:00"
doc_updated_by: "agentctl"
description: "Inspect generated outputs for errors and update cache_schema_generator.py to tolerate non-UTF8/garbled cache files, logging skips; rerun generator for clearlyamazing."
---
## Summary

Harden cache schema generator against unreadable or malformed HTML inputs.

## Scope

Add decoding safeguards, size limits, and parse error handling in cache_schema_generator.

## Risks

Large HTML files may now be skipped; adjust MAX_HTML_BYTES if needed.

## Verify Steps

1) Run cache schema generator on a sample cache\n2) Confirm unreadable/oversized pages are skipped with warnings

## Rollback Plan

Revert cache_schema_generator.py changes to remove decode/size guards.

