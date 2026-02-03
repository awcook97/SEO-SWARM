#!/usr/bin/env python3
"""Shared IO helpers for automation programs."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise SystemExit(f"CSV has no headers: {path}")
        return [normalize_row(row) for row in reader]


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_markdown(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def normalize_row(row: dict[str, str]) -> dict[str, str]:
    return {normalize_key(k): (v or "").strip() for k, v in row.items()}


def normalize_key(value: str) -> str:
    return value.strip().lower().replace(" ", "_")


def pick_value(row: dict[str, str], keys: Iterable[str]) -> str:
    for key in keys:
        value = row.get(key)
        if value:
            return value
    return ""
