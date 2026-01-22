#!/usr/bin/env python3
"""Convert GSC export CSVs into normalized JSON for downstream reports."""

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
    normalized: list[dict[str, Any]] = []
    for row in rows:
        cleaned: dict[str, Any] = dict(row)
        for key in ("clicks", "impressions", "ctr", "position"):
            if key in cleaned:
                cleaned[key] = parse_float(str(cleaned[key])) or 0.0
        normalized.append(cleaned)
    return normalized


def build_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    totals = {"clicks": 0.0, "impressions": 0.0}
    for row in rows:
        totals["clicks"] += float(row.get("clicks") or 0)
        totals["impressions"] += float(row.get("impressions") or 0)
    ctr = (totals["clicks"] / totals["impressions"]) if totals["impressions"] else 0.0

    def group_rows(key: str) -> list[dict[str, Any]]:
        bucket: dict[str, dict[str, float]] = defaultdict(lambda: {"clicks": 0.0, "impressions": 0.0})
        for row in rows:
            value = str(row.get(key) or "").strip()
            if not value:
                continue
            bucket[value]["clicks"] += float(row.get("clicks") or 0)
            bucket[value]["impressions"] += float(row.get("impressions") or 0)
        items = [
            {"name": name, "clicks": data["clicks"], "impressions": data["impressions"]}
            for name, data in bucket.items()
        ]
        items.sort(key=lambda item: item["clicks"], reverse=True)
        return items[:10]

    summary = {
        "generated_at": now_iso(),
        "totals": {
            "clicks": totals["clicks"],
            "impressions": totals["impressions"],
            "ctr": round(ctr, 4),
        },
        "top_queries": group_rows("query"),
        "top_pages": group_rows("page"),
    }
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert GSC export CSV into JSON.")
    parser.add_argument("--client-slug", required=True, help="Client slug under data/outputs/")
    parser.add_argument("--input", required=True, help="Path to GSC export CSV.")
    parser.add_argument("--site", default=None, help="GSC property or site URL.")
    parser.add_argument("--start-date", default=None, help="Report start date (YYYY-MM-DD).")
    parser.add_argument("--end-date", default=None, help="Report end date (YYYY-MM-DD).")
    parser.add_argument(
        "--output",
        default=None,
        help="Output JSON path (default: data/outputs/<client>/reports/gsc-export.json).",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Write gsc-summary.json with top queries/pages.",
    )
    args = parser.parse_args()

    output_dir = Path("data") / "outputs" / args.client_slug / "reports"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.output) if args.output else output_dir / "gsc-export.json"

    rows = normalize_rows(load_csv(Path(args.input)))
    if not rows:
        raise SystemExit("No rows found in export.")

    payload = {
        "client": {"site": args.site or "[property]"},
        "exported_at": now_iso(),
        "date_range": {"start": args.start_date or "", "end": args.end_date or ""},
        "columns": sorted({key for row in rows for key in row.keys()}),
        "rows": rows,
    }
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"wrote {output_path}")

    if args.summary:
        summary_path = output_dir / "gsc-summary.json"
        summary_path.write_text(json.dumps(build_summary(rows), indent=2), encoding="utf-8")
        print(f"wrote {summary_path}")


if __name__ == "__main__":
    main()
