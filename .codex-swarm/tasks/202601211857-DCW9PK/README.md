---
id: "202601211857-DCW9PK"
title: "Add .env + DataForSEO credentials"
status: "TODO"
priority: "P1"
owner: "CODER"
depends_on: ["202601211855-FAJDQP"]
tags: ["config", "automation"]
doc_version: 2
doc_updated_at: "2026-01-21T22:57:13+00:00"
doc_updated_by: "agentctl"
description: "Create .env with DATAFORSEO_LOGIN/PASSWORD for SERP automation; ensure .gitignore excludes .env."
---
# 202601211857-DCW9PK: Add .env + DataForSEO credentials

## Summary

Add .env.example and document DataForSEO credential setup.

## Context

- ...

## Scope

Add .env.example with DataForSEO keys and update README environment notes.

## Risks

Missing credentials prevent SERP fetch scripts from running.

## Verify Steps

1) Copy .env.example to .env and set values\n2) python scripts/serp_dataforseo_fetch.py --client-slug <client> --scaffold

## Rollback Plan

Revert commit(s) adding .env.example and README environment notes.

## Notes

- ...

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- `.env.example`
- `README.md`
<!-- END AUTO SUMMARY -->

