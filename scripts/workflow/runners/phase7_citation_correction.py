#!/usr/bin/env python3
"""Phase 7 runner: Citation Audit + Correction Workflow."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.workflow.automation.runner_utils import build_parser, build_config, build_inputs

INPUT_KEYS = ["citation_csv"]


def main() -> int:
    parser = build_parser("Run Phase 7 citation correction", INPUT_KEYS)
    args = parser.parse_args()
    from scripts.workflow.automation.phase7_citation_correction import CitationCorrectionProgram

    program = CitationCorrectionProgram(build_config(args), build_inputs(args, INPUT_KEYS))
    if not args.dry_run:
        program.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
