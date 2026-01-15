---
id: "202601150137-RB4XWY"
title: "Cleanup stale task dependencies"
status: "TODO"
priority: "med"
owner: "DOCS"
depends_on: []
tags: []
doc_version: 2
doc_updated_at: "2026-01-15T01:40:06+00:00"
doc_updated_by: "agentctl"
description: "Remove stale dependency references from completed tasks so the task list is clean."
---
## Summary

Removed stale dependency references from completed tasks.

## Context

Task list showed stale missing dependency flags even though dependencies were complete.

## Scope

Clear depends_on fields for completed tasks that still showed missing deps.

## Risks

Risk: none; dependency cleanup only.

## Verify Steps

1) Run task list and confirm no missing deps are shown. 2) Ensure no task status changed.

## Rollback Plan

Revert the commit that updates task dependencies.

## Notes

Cleared depends_on for NH3PKT, T0F77E, Z0P215, GNY4PM, Q6HB8K.

