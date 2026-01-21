#!/usr/bin/env python3
"""Convert crawl exports into normalized JSON for technical audits."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ALIASES = {
    "url": ["url", "address", "page"],
    "status_code": ["status_code", "status", "http_status", "statuscode"],
    "title": ["title", "page_title"],
    "meta_description": ["meta_description", "description", "meta_desc"],
    "h1": ["h1", "h1_1"],
    "word_count": ["word_count", "words"],
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def normalize_header(value: str) -> str:
    return value.strip().lower().replace(" ", "_")


def parse_int(value: str) -> int | None:
    if value is None:
        return None
    value = value.strip()
    if not value:
        return None
    try:
        return int(float(value))
    except ValueError:
        return None


def load_csv(path: Path) -> list[dict[str, str]]:
    try:
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            if not reader.fieldnames:
                raise SystemExit(f"CSV has no headers: {path}")
            rows: list[dict[str, str]] = []
            for row in reader:
                rows.append({normalize_header(k): (v or "").strip() for k, v in row.items()})
            return rows
    except FileNotFoundError as exc:
        raise SystemExit(f"CSV not found: {path}") from exc


def pick_value(row: dict[str, str], keys: list[str]) -> str:
    for key in keys:
        value = row.get(key)
        if value:
            return value
    return ""


def normalize_rows(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for row in rows:
        entry = {
            "url": pick_value(row, ALIASES["url"]),
            "status_code": parse_int(pick_value(row, ALIASES["status_code"])) or 0,
            "title": pick_value(row, ALIASES["title"]),
            "meta_description": pick_value(row, ALIASES["meta_description"]),
            "h1": pick_value(row, ALIASES["h1"]),
            "word_count": parse_int(pick_value(row, ALIASES["word_count"])) or 0,
        }
        if entry["url"]:
            normalized.append(entry)
    return normalized


def build_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    status_counts: dict[str, int] = defaultdict(int)
    for row in rows:
        status_counts[str(row.get("status_code") or 0)] += 1
    return {
        "generated_at": now_iso(),
        "status_counts": dict(status_counts),
        "total_urls": len(rows),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert crawl export CSV into JSON.")
    parser.add_argument("--client-slug", required=True, help="Client slug under outputs/")
    parser.add_argument("--input", required=True, help="Path to crawl export CSV.")
    parser.add_argument(
        "--output",
        default=None,
        help="Output JSON path (default: outputs/<client>/reports/crawl-export.json).",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Write crawl-summary.json with status counts.",
    )
    args = parser.parse_args()

    output_dir = Path("outputs") / args.client_slug / "reports"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.output) if args.output else output_dir / "crawl-export.json"

    rows = normalize_rows(load_csv(Path(args.input)))
    if not rows:
        raise SystemExit("No crawl rows found in export.")

    payload = {
        "exported_at": now_iso(),
        "rows": rows,
    }
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"wrote {output_path}")

    if args.summary:
        summary_path = output_dir / "crawl-summary.json"
        summary_path.write_text(json.dumps(build_summary(rows), indent=2), encoding="utf-8")
        print(f"wrote {summary_path}")


if __name__ == "__main__":
    main()
