#!/usr/bin/env python3
"""Convert review exports into the review response template input JSON."""

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


def load_json(path: Path) -> list[dict[str, Any]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"JSON not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        reviews = data.get("reviews")
        if isinstance(reviews, list):
            return reviews
    raise SystemExit(f"JSON must be a list or include a 'reviews' list: {path}")


def pick_value(row: dict[str, Any], keys: Iterable[str]) -> str:
    for key in keys:
        value = row.get(key)
        if value is None:
            continue
        text = str(value).strip()
        if text:
            return text
    return ""


def parse_rating(value: str) -> int | None:
    if not value:
        return None
    try:
        return int(round(float(value)))
    except ValueError:
        return None


def parse_issues(value: str) -> list[str]:
    if not value:
        return []
    tokens = []
    for sep in (";", "|", ","):
        if sep in value:
            tokens = [item.strip() for item in value.split(sep)]
            break
    if not tokens:
        tokens = [value.strip()]
    return [item for item in tokens if item]


def build_reviews(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    reviews: list[dict[str, Any]] = []
    for row in rows:
        reviewer = pick_value(
            row,
            (
                "reviewer",
                "reviewer_name",
                "name",
                "author",
                "user",
                "profile_name",
            ),
        )
        rating_raw = pick_value(row, ("rating", "stars", "star_rating", "score"))
        platform = pick_value(row, ("platform", "source", "site", "provider"))
        date = pick_value(row, ("date", "review_date", "timestamp", "time", "created_at"))
        summary = pick_value(row, ("summary", "text", "review", "comment", "content", "body"))
        issues_raw = pick_value(row, ("issues", "flags", "complaints", "problems"))
        rating = parse_rating(rating_raw)
        if not reviewer or rating is None or not platform or not date:
            continue
        reviews.append(
            {
                "reviewer": reviewer,
                "rating": rating,
                "platform": platform,
                "date": date,
                "summary": summary,
                "issues": parse_issues(issues_raw),
            }
        )
    return reviews


def scaffold_csv(path: Path) -> None:
    sample = [
        {
            "reviewer": "Jamie",
            "rating": "5",
            "platform": "Google",
            "date": "2026-01-02",
            "summary": "Quick response and friendly team.",
            "issues": "",
        }
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(sample[0].keys()))
        writer.writeheader()
        writer.writerows(sample)


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert review exports into input JSON.")
    parser.add_argument("--client-slug", required=True, help="Client slug under data/outputs/")
    parser.add_argument("--input", required=True, help="Path to review export (CSV or JSON).")
    parser.add_argument("--format", choices=("csv", "json"), default=None, help="Override input format.")
    parser.add_argument("--client-name", default=None, help="Client display name override.")
    parser.add_argument("--client-contact", default=None, help="Client contact email override.")
    parser.add_argument(
        "--output",
        default=None,
        help="Output JSON path (default: data/outputs/<client>/reports/review-templates-input.json).",
    )
    parser.add_argument(
        "--scaffold-csv",
        action="store_true",
        help="Write a CSV scaffold to the input path instead of ingesting.",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if args.scaffold_csv:
        input_path.parent.mkdir(parents=True, exist_ok=True)
        scaffold_csv(input_path)
        print(f"wrote scaffold CSV to {input_path}")
        return

    output_dir = Path("data") / "outputs" / args.client_slug / "reports"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.output) if args.output else output_dir / "review-templates-input.json"

    fmt = args.format or input_path.suffix.lstrip(".").lower()
    if fmt == "json":
        rows = load_json(input_path)
    else:
        rows = load_csv(input_path)

    reviews = build_reviews(rows)
    if not reviews:
        raise SystemExit("No valid reviews found in export.")

    payload = {
        "client": {
            "name": args.client_name or "[Client Name]",
            "contact": args.client_contact or "owner@example.com",
        },
        "exported_at": now_iso(),
        "reviews": reviews,
    }
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"wrote {output_path}")


if __name__ == "__main__":
    main()
