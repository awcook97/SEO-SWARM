---
id: "202601211727-39HENR"
title: "Enable branch_pr workflow mode"
status: "TODO"
priority: "P1"
owner: "ORCHESTRATOR"
depends_on: []
tags: ["workflow", "config"]
doc_version: 2
doc_updated_at: "2026-01-21T17:34:33+00:00"
doc_updated_by: "agentctl"
description: "Switch workflow_mode to branch_pr to allow parallel task execution via per-task branches/worktrees."
---
# 202601211727-39HENR: Enable branch_pr workflow mode

## Summary

- Switch `workflow_mode` to `branch_pr` to support parallel task execution with per-task branches/worktrees.

## Context

- The repo was configured for `direct` mode, which prohibits parallel work via branches/worktrees.
- `branch_pr` enables `agentctl work start` to create per-task worktrees for concurrent execution.

## Scope

- Update `.codex-swarm/config.json` to set `workflow_mode` to `branch_pr`.

## Risks

- Parallel work requires stricter coordination (worktrees, PR artifacts, and integration via `agentctl integrate`).

## Verify Steps

- `python3 .codex-swarm/agentctl.py config show` (confirm `workflow_mode` is `branch_pr`).

## Rollback Plan

- Revert the commit and set `workflow_mode` back to `direct` using `agentctl config set`.

## Notes

- Use `python3 .codex-swarm/agentctl.py work start <task-id> --agent <ROLE> --slug <slug> --worktree` for parallel worktrees.

## Changes Summary (auto)

<!-- BEGIN AUTO SUMMARY -->
- `.codex-swarm/config.json`
- `.codex-swarm/tasks/202601211727-39HENR/README.md`
<!-- END AUTO SUMMARY -->
