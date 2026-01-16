---
id: "202601150642-TG431S"
title: "Automate review response templates"
status: "DOING"
priority: "med"
owner: "CODER"
depends_on: []
tags: []
comments:
  - { author: "CODER", body: "Start: automate review response template generation with compliance guardrails." }
doc_version: 2
doc_updated_at: "2026-01-15T06:42:34+00:00"
doc_updated_by: "agentctl"
description: "Create a tool to generate review response templates and escalation rules from approved brand voice and constraints."
---
## Summary

Automate review response templates tailored to rating, platform, and issues.

## Scope

- Add `scripts/review_response_templates.py` with scaffoldable review inputs.
- Emit markdown and JSON templates under `outputs/<client>/reports/`.
- Document usage and add unit tests.

## Risks

- Templates must stay compliant; maintain approved tone and issue-handling guidance.

## Verify Steps

- Run `python3 -m unittest discover -s tests` (passes).

## Rollback Plan

- Revert the review response template script/docs/tests.
