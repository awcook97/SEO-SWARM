#!/usr/bin/env python3
"""Small metric helpers used across programs."""

from __future__ import annotations

from typing import Iterable


def _clean_number(value: str) -> str:
    return value.replace(",", "").strip()


def to_int(value: str) -> int:
    cleaned = _clean_number(value)
    return int(cleaned) if cleaned else 0


def to_float(value: str) -> float:
    cleaned = _clean_number(value)
    return float(cleaned) if cleaned else 0.0


def safe_div(numerator: float, denominator: float) -> float:
    return numerator / denominator if denominator else 0.0


def sum_metric(rows: Iterable[dict[str, str]], key: str) -> int:
    return sum(to_int(row.get(key, "")) for row in rows)
