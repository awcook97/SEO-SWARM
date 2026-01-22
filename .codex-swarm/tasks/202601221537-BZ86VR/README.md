---
id: "202601221537-BZ86VR"
title: "FAQ audit: fix regex escape warning"
status: "TODO"
priority: "low"
owner: "ORCHESTRATOR"
depends_on: []
tags: []
doc_version: 2
doc_updated_at: "2026-01-22T16:00:30+00:00"
doc_updated_by: "agentctl"
description: "Correct FAQ audit regex to avoid invalid escape sequence warning (ld+json pattern)."
---
## Summary

Fix FAQ audit regex to avoid invalid escape warnings.

## Context

FAQ audit emits a SyntaxWarning from the ld+json regex escape sequence.

## Scope

Use a raw string for the ld+json regex to prevent warnings.

## Risks

Minimal; regex behavior remains unchanged.

## Verify Steps

Run faq_audit.py and confirm no SyntaxWarning appears.

## Rollback Plan

Revert the regex change.

## Notes

Regex now uses a raw string for ld+json pattern.

