#!/usr/bin/env python3
"""Convert GA4 export CSVs into normalized JSON for reporting."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


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


def normalize_rows(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    numeric_keys = {
        "users",
        "active_users",
        "new_users",
        "sessions",
        "engaged_sessions",
        "event_count",
        "conversions",
        "total_revenue",
        "engagement_rate",
        "bounce_rate",
        "avg_session_duration",
    }
    normalized: list[dict[str, Any]] = []
    for row in rows:
        cleaned: dict[str, Any] = dict(row)
        for key in numeric_keys:
            if key in cleaned:
                cleaned[key] = parse_float(str(cleaned[key])) or 0.0
        normalized.append(cleaned)
    return normalized


def first_key(row: dict[str, Any], keys: list[str]) -> str:
    for key in keys:
        value = row.get(key)
        if value:
            return str(value).strip()
    return ""


def build_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    totals = {"users": 0.0, "sessions": 0.0, "conversions": 0.0}
    for row in rows:
        totals["users"] += float(row.get("users") or 0)
        totals["sessions"] += float(row.get("sessions") or 0)
        totals["conversions"] += float(row.get("conversions") or 0)

    def group_rows(keys: list[str], metric: str) -> list[dict[str, Any]]:
        bucket: dict[str, float] = defaultdict(float)
        for row in rows:
            name = first_key(row, keys)
            if not name:
                continue
            bucket[name] += float(row.get(metric) or 0)
        items = [{"name": name, metric: value} for name, value in bucket.items()]
        items.sort(key=lambda item: item[metric], reverse=True)
        return items[:10]

    summary = {
        "generated_at": now_iso(),
        "totals": totals,
        "top_pages": group_rows(["page_path", "page_location", "page"], "users"),
        "top_sources": group_rows(["session_source", "source", "traffic_source"], "users"),
    }
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert GA4 export CSV into JSON.")
    parser.add_argument("--client-slug", required=True, help="Client slug under data/outputs/")
    parser.add_argument("--input", required=True, help="Path to GA4 export CSV.")
    parser.add_argument("--property", default=None, help="GA4 property ID or name.")
    parser.add_argument("--start-date", default=None, help="Report start date (YYYY-MM-DD).")
    parser.add_argument("--end-date", default=None, help="Report end date (YYYY-MM-DD).")
    parser.add_argument(
        "--output",
        default=None,
        help="Output JSON path (default: data/outputs/<client>/reports/ga4-export.json).",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Write ga4-summary.json with top pages/sources.",
    )
    args = parser.parse_args()

    output_dir = Path("data") / "outputs" / args.client_slug / "reports"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.output) if args.output else output_dir / "ga4-export.json"

    rows = normalize_rows(load_csv(Path(args.input)))
    if not rows:
        raise SystemExit("No rows found in export.")

    payload = {
        "property": args.property or "[property]",
        "exported_at": now_iso(),
        "date_range": {"start": args.start_date or "", "end": args.end_date or ""},
        "columns": sorted({key for row in rows for key in row.keys()}),
        "rows": rows,
    }
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"wrote {output_path}")

    if args.summary:
        summary_path = output_dir / "ga4-summary.json"
        summary_path.write_text(json.dumps(build_summary(rows), indent=2), encoding="utf-8")
        print(f"wrote {summary_path}")


if __name__ == "__main__":
    main()
