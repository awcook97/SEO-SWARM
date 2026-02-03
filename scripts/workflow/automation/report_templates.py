#!/usr/bin/env python3
"""Markdown report templating helpers."""

from __future__ import annotations


def render_section(title: str, body: str) -> str:
    return f"## {title}\n\n{body.strip()}\n"


def _pad_row(row: list[str], size: int) -> list[str]:
    if len(row) >= size:
        return row[:size]
    return row + [""] * (size - len(row))


def render_table(headers: list[str], rows: list[list[str]]) -> str:
    if not rows:
        rows = [["No data"] + [""] * (len(headers) - 1)]
    padded = [_pad_row(list(row), len(headers)) for row in rows]
    head = "| " + " | ".join(headers) + " |"
    sep = "| " + " | ".join(["---"] * len(headers)) + " |"
    body = "\n".join("| " + " | ".join(row) + " |" for row in padded)
    return "\n".join([head, sep, body]).strip() + "\n"


def render_list(items: list[str]) -> str:
    if not items:
        return "- None"
    return "\n".join(f"- {item}" for item in items)
