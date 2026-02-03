#!/usr/bin/env python3
"""Phase 8 runner: Internal Link Map + Content Clusters."""

from __future__ import annotations

from scripts.workflow.automation.runner_utils import build_parser, build_config, build_inputs

INPUT_KEYS = ["linkmap_csv"]


def main() -> int:
    parser = build_parser("Run Phase 8 internal link map", INPUT_KEYS)
    args = parser.parse_args()
    from scripts.workflow.automation.phase8_internal_link import InternalLinkProgram

    program = InternalLinkProgram(build_config(args), build_inputs(args, INPUT_KEYS))
    if not args.dry_run:
        program.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
