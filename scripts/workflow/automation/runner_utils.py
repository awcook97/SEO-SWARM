#!/usr/bin/env python3
"""Shared CLI helper for phase runners."""

from __future__ import annotations

import argparse
from typing import Iterable

from .base import ProgramConfig, ProgramInputs


def build_parser(description: str, input_keys: Iterable[str]) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--client-name", required=True)
    parser.add_argument("--client-slug", required=True)
    parser.add_argument("--output-dir", default="data/outputs")
    for key in input_keys:
        parser.add_argument(f"--{key}", required=True)
    parser.add_argument("--dry-run", action="store_true")
    return parser


def build_config(args: argparse.Namespace) -> ProgramConfig:
    return ProgramConfig.from_args(args)


def build_inputs(args: argparse.Namespace, input_keys: Iterable[str]) -> ProgramInputs:
    values = {key: str(getattr(args, key)) for key in input_keys}
    return ProgramInputs(values)
