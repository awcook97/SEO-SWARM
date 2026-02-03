#!/usr/bin/env python3
"""Load orchestration config for automation programs."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .io_utils import read_json


@dataclass
class OrchestratorConfig:
    client_name: str
    client_slug: str
    output_dir: Path
    phases: dict[str, dict[str, str]]

    @classmethod
    def load(cls, path: Path) -> "OrchestratorConfig":
        raw = read_json(path)
        return cls.from_dict(raw)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "OrchestratorConfig":
        output_dir = Path(data.get("output_dir", "data/outputs"))
        return cls(data["client_name"], data["client_slug"], output_dir, data.get("phases", {}))

    def get_inputs(self, phase_key: str) -> dict[str, str]:
        phase = self.phases.get(phase_key, {})
        return {key: str(value) for key, value in phase.items()}
