#!/usr/bin/env python3
"""Orchestrate all automation programs across phases 1-8."""

from __future__ import annotations

import argparse
from pathlib import Path

from scripts.workflow.automation.base import ProgramConfig, ProgramInputs
from scripts.workflow.automation.config_loader import OrchestratorConfig
from scripts.workflow.automation.phase_registry import PHASE_BUILDERS


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run automation programs by phase")
    parser.add_argument("--config", required=True, help="Path to orchestration JSON")
    parser.add_argument("--phase", type=int, help="Phase number (1-8)")
    parser.add_argument("--all", action="store_true", help="Run all phases")
    parser.add_argument("--dry-run", action="store_true", help="Validate config only")
    return parser.parse_args()


def get_phase_keys(args: argparse.Namespace) -> list[str]:
    if args.all:
        return [str(i) for i in range(1, 9)]
    if args.phase:
        return [str(args.phase)]
    raise SystemExit("Must pass --phase or --all")


def run_phase(phase_key: str, cfg: OrchestratorConfig, dry_run: bool) -> None:
    inputs = ProgramInputs(cfg.get_inputs(phase_key))
    config = ProgramConfig(cfg.client_name, cfg.client_slug, cfg.output_dir)
    builder = PHASE_BUILDERS.get(phase_key)
    if not builder:
        raise SystemExit(f"Unknown phase: {phase_key}")
    program = builder(config, inputs)
    if dry_run:
        return
    program.run()


def main() -> int:
    args = parse_args()
    cfg = OrchestratorConfig.load(Path(args.config))
    for phase_key in get_phase_keys(args):
        run_phase(phase_key, cfg, args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
