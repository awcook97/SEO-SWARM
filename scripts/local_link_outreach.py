#!/usr/bin/env python3
"""Generate a log of local link outreach targets and status updates."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class OutreachTarget:
    organization: str
    contact: str
    priority: str
    target_url: str
    status: str
    last_touch: str | None = None
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
        "client": {"name": "[Client]", "website": "https://example.com"},
        "targets": [
            {
                "organization": "City Chamber",
                "contact": "city@chamber.example",
                "priority": "high",
                "target_url": "/community/partners",
                "status": "pending",
                "last_touch": "",
                "notes": "Offer partnership mention and link.",
            }
        ],
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def parse_targets(data: dict[str, Any]) -> list[OutreachTarget]:
    targets: list[OutreachTarget] = []
    for raw in data.get("targets", []):
        org = raw.get("organization")
        contact = raw.get("contact")
        priority = raw.get("priority")
        target_url = raw.get("target_url")
        status = raw.get("status")
        if not org or not contact or not priority or not target_url or not status:
            continue
        targets.append(
            OutreachTarget(
                organization=org,
                contact=contact,
                priority=priority,
                target_url=target_url,
                status=status,
                last_touch=raw.get("last_touch"),
                notes=raw.get("notes"),
            )
        )
    return targets


def render_markdown(client: dict[str, Any], targets: list[OutreachTarget]) -> str:
    lines: list[str] = []
    lines.append("# Local link outreach log")
    lines.append("")
    lines.append(f"Client: {client.get('name') or '[client name]'}")
    lines.append(f"Generated: {now_iso()}")
    lines.append("")
    lines.append("| Org | Contact | Priority | Target URL | Status | Last touch | Notes |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for target in targets:
        lines.append(
            f"| {target.organization} | {target.contact} | {target.priority} | {target.target_url} |"
            f" {target.status} | {target.last_touch or ''} | {target.notes or ''} |"
        )
    lines.append("")
    summary: dict[str, int] = {}
    for target in targets:
        summary.setdefault(target.status, 0)
        summary[target.status] += 1
    lines.append("## Status counts")
    for status, count in summary.items():
        lines.append(f"- {status}: {count}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate local link outreach log.")
    parser.add_argument("--client-slug", required=True, help="Client slug under data/outputs/")
    parser.add_argument(
        "--input",
        default=None,
        help="Input JSON path (default: data/outputs/<client>/reports/local-link-input.json)",
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

    input_path = Path(args.input) if args.input else report_dir / "local-link-input.json"
    if not input_path.exists():
        if args.scaffold:
            scaffold_input(input_path)
            print(f"wrote scaffold input to {input_path}")
            return
        raise SystemExit(f"Input file not found: {input_path}. Use --scaffold to create one.")

    data = load_input(input_path)
    targets = parse_targets(data)
    if not targets:
        raise SystemExit("No valid targets found in input.")

    payload = {
        "generated_at": now_iso(),
        "client": data.get("client", {}),
        "targets": [target.__dict__ for target in targets],
    }

    md_path = report_dir / "local-link-outreach.md"
    json_path = report_dir / "local-link-outreach.json"

    md_path.write_text(render_markdown(data.get("client", {}), targets), encoding="utf-8")
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print(f"wrote {md_path}")
    print(f"wrote {json_path}")


if __name__ == "__main__":
    main()
