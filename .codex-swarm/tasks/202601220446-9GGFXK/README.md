---
id: "202601220446-9GGFXK"
title: "Switch workflow mode to direct and streamline repo layout"
status: "TODO"
priority: "med"
owner: "ORCHESTRATOR"
depends_on: []
tags: []
doc_version: 2
doc_updated_at: "2026-01-22T15:44:34+00:00"
doc_updated_by: "agentctl"
description: "Set workflow_mode back to direct, review repo layout, propose and apply folder moves to make project more manageable, update references/docs."
---
## Summary

Set workflow_mode to direct and prepare a repo layout cleanup with path/doc updates.

## Context

User asked to switch the workflow back to direct and reorganize folders to make the repo easier to manage, with any required reference updates.

## Scope

1) Update config to direct. 2) Propose a streamlined folder layout. 3) Apply approved moves and update docs/scripts references.

## Risks

Folder moves can break script defaults and doc links; will update paths and keep defaults consistent.

## Verify Steps

After changes: run `python3 scripts/swarm_workflow.py --help` and spot-check one generator command with a test client slug.

## Rollback Plan

Revert the commit(s) and restore the previous folder locations; reset workflow_mode to branch_pr if needed.

## Notes

keyword_map_kpi now infers service pages from cache URLs when inputs.md is missing service data, so auto-from-cache still works.

