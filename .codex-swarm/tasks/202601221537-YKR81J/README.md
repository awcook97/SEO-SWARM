---
id: "202601221537-YKR81J"
title: "Audit runner: SERP fetch env guard and skip"
status: "TODO"
priority: "med"
owner: "ORCHESTRATOR"
depends_on: []
tags: []
doc_version: 2
doc_updated_at: "2026-01-22T15:55:22+00:00"
doc_updated_by: "agentctl"
description: "In site_audit_runner, detect missing DATAFORSEO_LOGIN/PASSWORD and skip SERP fetch with a clear warning."
---
## Summary

Skip SERP fetch in site_audit_runner when DataForSEO env vars are missing.

## Context

Autorunner fails on SERP fetch when DATAFORSEO credentials are unset; it should skip with a warning.

## Scope

Add an env guard in site_audit_runner before adding the SERP fetch step.

## Risks

Skipping SERP fetch may hide missing SERP inputs; warning output calls this out.

## Verify Steps

Run site_audit_runner without DATAFORSEO env vars and confirm SERP fetch is skipped with a warning.

## Rollback Plan

Revert the env guard to restore strict DataForSEO enforcement.

## Notes

SERP fetch step now only runs when DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD are set.

