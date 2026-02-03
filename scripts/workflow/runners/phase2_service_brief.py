#!/usr/bin/env python3
"""Phase 2 runner: Service Page Content Brief."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.workflow.automation.runner_utils import build_parser, build_config, build_inputs

INPUT_KEYS = ["crawl_csv", "service"]


def main() -> int:
    parser = build_parser("Run Phase 2 service brief", INPUT_KEYS)
    args = parser.parse_args()
    from scripts.workflow.automation.phase2_service_brief import ServiceBriefProgram

    program = ServiceBriefProgram(build_config(args), build_inputs(args, INPUT_KEYS))
    if not args.dry_run:
        program.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
