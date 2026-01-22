#!/usr/bin/env python3
"""Convert citation audit exports into citation log input JSON."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def normalize_header(value: str) -> str:
    return value.strip().lower().replace(" ", "_")


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


def pick_value(row: dict[str, Any], keys: Iterable[str]) -> str:
    for key in keys:
        value = row.get(key)
        if value:
            return str(value).strip()
    return ""


def build_citations(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    citations: list[dict[str, Any]] = []
    for row in rows:
        platform = pick_value(row, ("platform", "directory", "listing", "site"))
        listing_url = pick_value(row, ("listing_url", "url", "listing_link", "profile_url"))
        status = pick_value(row, ("status", "state", "issue"))
        if not platform or not listing_url or not status:
            continue
        citations.append(
            {
                "platform": platform,
                "listing_url": listing_url,
                "status": status,
                "action_date": pick_value(row, ("action_date", "date", "updated_at")),
                "owner": pick_value(row, ("owner", "assignee", "responsible")),
                "notes": pick_value(row, ("notes", "comment", "comments", "details")),
            }
        )
    return citations


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert citation audit export CSV into input JSON.")
    parser.add_argument("--client-slug", required=True, help="Client slug under data/outputs/")
    parser.add_argument("--input", required=True, help="Path to citation audit CSV.")
    parser.add_argument("--client-name", default=None, help="Client display name override.")
    parser.add_argument("--client-website", default=None, help="Client website override.")
    parser.add_argument(
        "--output",
        default=None,
        help="Output JSON path (default: data/outputs/<client>/reports/citation-log-input.json).",
    )
    args = parser.parse_args()

    output_dir = Path("data") / "outputs" / args.client_slug / "reports"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.output) if args.output else output_dir / "citation-log-input.json"

    rows = load_csv(Path(args.input))
    citations = build_citations(rows)
    if not citations:
        raise SystemExit("No valid citation entries found in export.")

    payload = {
        "client": {
            "name": args.client_name or "[Client Name]",
            "website": args.client_website or "https://example.com",
        },
        "exported_at": now_iso(),
        "citations": citations,
    }
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"wrote {output_path}")


if __name__ == "__main__":
    main()
