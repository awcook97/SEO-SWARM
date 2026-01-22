#!/usr/bin/env python3
"""Generate a citation update log and summary report."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class CitationEntry:
    platform: str
    listing_url: str
    status: str
    action_date: str | None = None
    owner: str | None = None
    notes: str | None = None


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
        "client": {"name": "[client name]", "website": "https://example.com"},
        "citations": [
            {
                "platform": "Google Business Profile",
                "listing_url": "https://maps.app.goo.gl/example",
                "status": "Needs update",
                "action_date": "",
                "owner": "GBP Optimizer",
                "notes": "Update service list and hours from approved inputs.",
            }
        ],
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def parse_citations(data: dict[str, Any]) -> list[CitationEntry]:
    entries: list[CitationEntry] = []
    for raw in data.get("citations", []):
        platform = raw.get("platform")
        listing = raw.get("listing_url")
        status = raw.get("status")
        if not platform or not listing or not status:
            continue
        entries.append(
            CitationEntry(
                platform=platform,
                listing_url=listing,
                status=status,
                action_date=raw.get("action_date"),
                owner=raw.get("owner"),
                notes=raw.get("notes"),
            )
        )
    return entries


def render_markdown(client: dict[str, Any], entries: list[CitationEntry]) -> str:
    lines: list[str] = []
    lines.append("# Citation update log")
    lines.append("")
    lines.append(f"Client: {client.get('name') or '[client name]'}")
    lines.append(f"Generated: {now_iso()}")
    lines.append("")
    lines.append("| Platform | Listing URL | Status | Action date | Owner | Notes |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for entry in entries:
        lines.append(
            f"| {entry.platform} | {entry.listing_url} | {entry.status} | {entry.action_date or ''} |"
            f" {entry.owner or ''} | {entry.notes or ''} |"
        )
    lines.append("")
    summary: dict[str, int] = {}
    for entry in entries:
        summary.setdefault(entry.status, 0)
        summary[entry.status] += 1
    lines.append("## Status summary")
    for status, count in summary.items():
        lines.append(f"- {status}: {count}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate citation update log reports.")
    parser.add_argument("--client-slug", required=True, help="Client slug under data/outputs/")
    parser.add_argument(
        "--input",
        default=None,
        help="Path to citation input JSON (default: data/outputs/<client>/reports/citation-log-input.json)",
    )
    parser.add_argument(
        "--scaffold",
        action="store_true",
        help="Create a scaffold input file if missing.",
    )
    args = parser.parse_args()

    base_dir = Path("data") / "outputs" / args.client_slug
    report_dir = base_dir / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    input_path = Path(args.input) if args.input else report_dir / "citation-log-input.json"
    if not input_path.exists():
        if args.scaffold:
            scaffold_input(input_path)
            print(f"wrote scaffold input to {input_path}")
            return
        raise SystemExit(f"Input file not found: {input_path}. Use --scaffold to create one.")

    data = load_input(input_path)
    entries = parse_citations(data)
    if not entries:
        raise SystemExit("No valid citation entries found in input.")

    payload = {
        "generated_at": now_iso(),
        "client": data.get("client", {}),
        "citations": [entry.__dict__ for entry in entries],
    }

    md_path = report_dir / "citation-update-log.md"
    json_path = report_dir / "citation-update-log.json"

    md_path.write_text(render_markdown(data.get("client", {}), entries), encoding="utf-8")
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print(f"wrote {md_path}")
    print(f"wrote {json_path}")


if __name__ == "__main__":
    main()
