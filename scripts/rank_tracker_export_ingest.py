#!/usr/bin/env python3
"""Normalize rank tracker CSV exports for report generation."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CANONICAL_FIELDS = [
    "keyword",
    "location",
    "current_rank",
    "previous_rank",
    "best_rank",
    "target_url",
    "notes",
]

ALIASES = {
    "keyword": ["keyword", "query", "term"],
    "location": ["location", "region", "city", "geo", "market"],
    "current_rank": ["current_rank", "current", "rank", "position", "current_position"],
    "previous_rank": ["previous_rank", "previous", "last_rank", "prior_rank", "last_position"],
    "best_rank": ["best_rank", "best", "peak_rank", "best_position"],
    "target_url": ["target_url", "url", "landing_page", "page", "target"],
    "notes": ["notes", "comment", "comments", "annotation"],
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def normalize_header(value: str) -> str:
    return value.strip().lower().replace(" ", "_")


def load_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    try:
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            if not reader.fieldnames:
                raise SystemExit(f"CSV has no headers: {path}")
            headers = [normalize_header(name) for name in reader.fieldnames]
            rows: list[dict[str, str]] = []
            for row in reader:
                rows.append({normalize_header(k): (v or "").strip() for k, v in row.items()})
            return headers, rows
    except FileNotFoundError as exc:
        raise SystemExit(f"CSV not found: {path}") from exc


def map_headers(headers: list[str]) -> dict[str, str | None]:
    mapping: dict[str, str | None] = {}
    header_set = set(headers)
    for canonical, aliases in ALIASES.items():
        mapped = None
        for alias in aliases:
            if alias in header_set:
                mapped = alias
                break
        mapping[canonical] = mapped
    return mapping


def normalize_rows(rows: list[dict[str, str]], mapping: dict[str, str | None]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for row in rows:
        entry: dict[str, Any] = {}
        for field in CANONICAL_FIELDS:
            source = mapping.get(field)
            entry[field] = row.get(source, "") if source else ""
        normalized.append(entry)
    return normalized


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize rank tracker CSV exports.")
    parser.add_argument("--client-slug", required=True, help="Client slug under data/outputs/")
    parser.add_argument("--input", required=True, help="Path to rank tracker CSV export.")
    parser.add_argument(
        "--output-csv",
        default=None,
        help="Output CSV path (default: data/outputs/<client>/reports/rank-tracker-export.csv).",
    )
    parser.add_argument(
        "--output-json",
        default=None,
        help="Output JSON summary path (default: data/outputs/<client>/reports/rank-tracker-export.json).",
    )
    args = parser.parse_args()

    output_dir = Path("data") / "outputs" / args.client_slug / "reports"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_csv = Path(args.output_csv) if args.output_csv else output_dir / "rank-tracker-export.csv"
    output_json = Path(args.output_json) if args.output_json else output_dir / "rank-tracker-export.json"

    headers, rows = load_csv(Path(args.input))
    mapping = map_headers(headers)
    normalized_rows = normalize_rows(rows, mapping)

    with output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CANONICAL_FIELDS)
        writer.writeheader()
        writer.writerows(normalized_rows)

    summary = {
        "exported_at": now_iso(),
        "source_columns": headers,
        "mapping": mapping,
        "row_count": len(normalized_rows),
    }
    output_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"wrote {output_csv}")
    print(f"wrote {output_json}")


if __name__ == "__main__":
    main()
