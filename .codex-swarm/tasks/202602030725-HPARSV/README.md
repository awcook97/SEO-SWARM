---
id: "202602030725-HPARSV"
title: "Phase 3 compliance risk program"
status: "DONE"
priority: "P1"
owner: "CODER"
depends_on: []
tags: ["code"]
verify: ["python scripts/workflow/runners/phase3_compliance_risk.py --help"]
commit: { hash: "cc222d9db3afa1e49f2c4026a14e37be5ec18258", message: "✨ HPARSV Phase 3: add compliance risk program" }
comments:
  - { author: "CODER", body: "Start: Building Phase 3 compliance scanner, risk scoring, remediation planner, and report output." }
doc_version: 2
doc_updated_at: "2026-02-03T07:27:36+00:00"
doc_updated_by: "agentctl"
description: "Implement compliance scanner, risk scoring, remediation planner, and report output"
---
## Summary

Implemented Phase 3 compliance risk audit with claim extraction, risk scoring, and remediation planning. Generates structured compliance report with risk buckets and checklist.

## Scope

1. Added ComplianceScanner, RiskScorer, RemediationPlanner classes
2. Implemented ComplianceRiskProgram report generator
3. Added claim parsing, risk bucketing, and remediation checklist output
4. Ensured all functions <=20 lines

## Risks

Low risk: additive report generation. Claim detection is heuristic and may over-flag without policy tuning.

## Verify Steps

1. Run: python scripts/workflow/runners/phase3_compliance_risk.py --help
2. Provide --content_md and --policy_md inputs with client details
3. Verify outputs in data/outputs/<slug>/reports/compliance-risk-report.md and .json

## Rollback Plan

Revert commit cc222d9db3af to remove Phase 3 compliance risk implementation.

