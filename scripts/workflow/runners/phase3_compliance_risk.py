#!/usr/bin/env python3
"""Phase 3 runner: Compliance Risk Audit."""

from __future__ import annotations

from scripts.workflow.automation.runner_utils import build_parser, build_config, build_inputs

INPUT_KEYS = ["content_md", "policy_md"]


def main() -> int:
    parser = build_parser("Run Phase 3 compliance risk", INPUT_KEYS)
    args = parser.parse_args()
    from scripts.workflow.automation.phase3_compliance_risk import ComplianceRiskProgram

    program = ComplianceRiskProgram(build_config(args), build_inputs(args, INPUT_KEYS))
    if not args.dry_run:
        program.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
