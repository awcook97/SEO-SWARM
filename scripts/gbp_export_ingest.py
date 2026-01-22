#!/usr/bin/env python3
"""Convert GBP export CSVs into normalized JSON for reporting."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ALIASES = {
    "date": ["date", "day", "week", "month"],
    "views": ["views", "profile_views", "viewers"],
    "searches": ["searches", "search_queries", "queries"],
    "calls": ["calls", "phone_calls"],
    "website_clicks": ["website_clicks", "website_visits", "website_clicks_to_site"],
    "direction_requests": ["direction_requests", "directions", "driving_directions"],
    "messages": ["messages", "messages_started"],
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def normalize_header(value: str) -> str:
    return value.strip().lower().replace(" ", "_")


def parse_float(value: str) -> float | None:
    if value is None:
        return None
    value = value.strip().replace("%", "")
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


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


def pick_value(row: dict[str, str], keys: list[str]) -> str:
    for key in keys:
        value = row.get(key)
        if value:
            return value
    return ""


def normalize_rows(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for row in rows:
        entry: dict[str, Any] = {}
        entry["date"] = pick_value(row, ALIASES["date"])
        for key in ("views", "searches", "calls", "website_clicks", "direction_requests", "messages"):
            raw = pick_value(row, ALIASES[key])
            entry[key] = parse_float(raw) or 0.0
        normalized.append(entry)
    return normalized


def build_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    totals = {"views": 0.0, "searches": 0.0, "calls": 0.0, "website_clicks": 0.0}
    for row in rows:
        totals["views"] += float(row.get("views") or 0)
        totals["searches"] += float(row.get("searches") or 0)
        totals["calls"] += float(row.get("calls") or 0)
        totals["website_clicks"] += float(row.get("website_clicks") or 0)
    return {"generated_at": now_iso(), "totals": totals}


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert GBP export CSV into JSON.")
    parser.add_argument("--client-slug", required=True, help="Client slug under data/outputs/")
    parser.add_argument("--input", required=True, help="Path to GBP export CSV.")
    parser.add_argument("--location", default=None, help="Location name or ID.")
    parser.add_argument(
        "--output",
        default=None,
        help="Output JSON path (default: data/outputs/<client>/reports/gbp-export.json).",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Write gbp-summary.json with totals.",
    )
    args = parser.parse_args()

    output_dir = Path("data") / "outputs" / args.client_slug / "reports"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.output) if args.output else output_dir / "gbp-export.json"

    headers, rows = load_csv(Path(args.input))
    normalized = normalize_rows(rows)
    if not normalized:
        raise SystemExit("No rows found in export.")

    payload = {
        "location": args.location or "[location]",
        "exported_at": now_iso(),
        "source_columns": headers,
        "rows": normalized,
    }
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"wrote {output_path}")

    if args.summary:
        summary_path = output_dir / "gbp-summary.json"
        summary_path.write_text(json.dumps(build_summary(normalized), indent=2), encoding="utf-8")
        print(f"wrote {summary_path}")


if __name__ == "__main__":
    main()
