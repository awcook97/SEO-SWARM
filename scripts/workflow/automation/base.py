#!/usr/bin/env python3
"""Base OOP framework for automation programs."""

from __future__ import annotations

import abc
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .io_utils import write_json, write_markdown


@dataclass
class ProgramConfig:
    client_name: str
    client_slug: str
    output_dir: Path

    @classmethod
    def from_args(cls, args: Any) -> "ProgramConfig":
        output_dir = Path(args.output_dir)
        return cls(args.client_name, args.client_slug, output_dir)


@dataclass
class ProgramInputs:
    values: dict[str, str]

    def require_path(self, key: str) -> Path:
        value = self.values.get(key)
        if not value:
            raise SystemExit(f"Missing input: {key}")
        path = Path(value)
        if not path.exists():
            raise SystemExit(f"Input not found: {path}")
        return path

    def require_text(self, key: str) -> str:
        value = (self.values.get(key) or "").strip()
        if not value:
            raise SystemExit(f"Missing input: {key}")
        return value


@dataclass
class ProgramOutput:
    payload: dict[str, Any]
    report_md: str
    report_path: Path
    json_path: Path

    def write(self) -> None:
        write_markdown(self.report_path, self.report_md)
        write_json(self.json_path, self.payload)


class ProgramRunner(abc.ABC):
    def __init__(self, config: ProgramConfig, inputs: ProgramInputs) -> None:
        self.config = config
        self.inputs = inputs

    def run(self) -> ProgramOutput:
        data = self.execute()
        report_md = self.render_report(data)
        report_path, json_path = self.get_output_paths()
        output = ProgramOutput(data, report_md, report_path, json_path)
        output.write()
        return output

    @abc.abstractmethod
    def execute(self) -> dict[str, Any]:
        raise NotImplementedError

    @abc.abstractmethod
    def render_report(self, data: dict[str, Any]) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def report_basename(self) -> str:
        raise NotImplementedError

    def get_output_paths(self) -> tuple[Path, Path]:
        base = self.config.output_dir / self.config.client_slug / "reports"
        name = self.report_basename()
        return base / f"{name}.md", base / f"{name}.json"
