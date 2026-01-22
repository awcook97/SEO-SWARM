#!/usr/bin/env python3
"""Generate review response templates based on review sentiment and issue flags."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class ReviewEntry:
    reviewer: str
    rating: int
    platform: str
    date: str
    summary: str
    issues: list[str]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_input(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"Input file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc


def scaffold_input(path: Path) -> None:
    payload = {
        "client": {"name": "[Client Name]", "contact": "owner@example.com"},
        "reviews": [
            {
                "reviewer": "Jane",
                "rating": 5,
                "platform": "Google",
                "date": "2026-01-02",
                "summary": "Great service",
                "issues": [],
            }
        ],
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def parse_reviews(data: dict[str, Any]) -> list[ReviewEntry]:
    entries: list[ReviewEntry] = []
    for raw in data.get("reviews", []):
        reviewer = raw.get("reviewer")
        rating = raw.get("rating")
        platform = raw.get("platform")
        date = raw.get("date")
        summary = raw.get("summary")
        issues = raw.get("issues") or []
        if not reviewer or rating is None or not platform or not date:
            continue
        entries.append(
            ReviewEntry(
                reviewer=reviewer,
                rating=int(rating),
                platform=platform,
                date=date,
                summary=summary or "",
                issues=list(issues),
            )
        )
    return entries


def template_for(entry: ReviewEntry) -> str:
    if entry.rating >= 4:
        tone = "Thank the reviewer, mention what they liked, and invite them back."
    else:
        tone = "Acknowledge the issue, outline next steps, offer contact."
    issues_block = "".join(f"Issues: {item}. " for item in entry.issues)
    return (
        f"Reviewer: {entry.reviewer} ({entry.platform}, {entry.date}) – Rating: {entry.rating}\n"
        f"Summary: {entry.summary}\n"
        f"Tone: {tone}\n"
        f"{issues_block}\n"
        "Template: [Write response referencing approved guidelines]"
    )


def render_markdown(client: dict[str, Any], entries: list[ReviewEntry]) -> str:
    lines: list[str] = []
    lines.append("# Review response templates")
    lines.append("")
    lines.append(f"Client: {client.get('name') or '[client]'}")
    lines.append(f"Generated: {now_iso()}")
    lines.append("")
    for entry in entries:
        lines.append(template_for(entry))
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate review response templates.")
    parser.add_argument("--client-slug", required=True, help="Client slug under data/outputs/")
    parser.add_argument(
        "--input",
        default=None,
        help="Input JSON path (default: data/outputs/<client>/reports/review-templates-input.json)",
    )
    parser.add_argument(
        "--scaffold",
        action="store_true",
        help="Create scaffold input file if missing.",
    )
    args = parser.parse_args()

    base_dir = Path("data") / "outputs" / args.client_slug
    report_dir = base_dir / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    input_path = Path(args.input) if args.input else report_dir / "review-templates-input.json"
    if not input_path.exists():
        if args.scaffold:
            scaffold_input(input_path)
            print(f"wrote scaffold input to {input_path}")
            return
        raise SystemExit(f"Input file not found: {input_path}. Use --scaffold to create one.")

    data = load_input(input_path)
    entries = parse_reviews(data)
    if not entries:
        raise SystemExit("No reviews found in input.")

    payload = {
        "generated_at": now_iso(),
        "client": data.get("client", {}),
        "reviews": [entry.__dict__ for entry in entries],
    }

    md_path = report_dir / "review-response-templates.md"
    json_path = report_dir / "review-response-templates.json"

    md_path.write_text(render_markdown(data.get("client", {}), entries), encoding="utf-8")
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print(f"wrote {md_path}")
    print(f"wrote {json_path}")


if __name__ == "__main__":
    main()
