---
id: "202601150222-Y4P9QY"
title: "Remove client-specific references from public docs"
status: "TODO"
priority: "med"
owner: "DOCS"
depends_on: []
tags: []
doc_version: 2
doc_updated_at: "2026-01-15T02:23:40+00:00"
doc_updated_by: "agentctl"
description: "Make templates client-agnostic and remove tracked client outputs before publishing."
---
## Summary

Removed client-specific references and made templates client-agnostic for open-source publishing.

## Context

User requested removal of HighPoint HVAC references from public files prior to publishing.

## Scope

Rename @docs/highpoint-hvac to @docs/client-templates, remove client-specific mentions, and delete tracked outputs/highpoint-hvac.

## Risks

Risk: removing tracked outputs may affect local history. Mitigation: outputs are now ignored and can be regenerated via templates.

## Verify Steps

1) rg for HighPoint/HighPoint HVAC returns no results. 2) outputs/highpoint-hvac removed from git.

## Rollback Plan

Revert the commit that renames docs and removes outputs.

## Notes

Templates now use [Client Name] placeholders instead of a specific business.

