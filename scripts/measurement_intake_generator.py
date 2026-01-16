#!/usr/bin/env python3
"""Generate measurement intake markdown from structured inputs."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class MeasurementProfile:
    client_name: str
    contact: str
    website: str
    service_areas: list[str]
    primary_services: list[str]
    secondary_services: list[str]
    keywords: list[str]
    cadence: str
    tools: dict[str, str]
    alerts: dict[str, str]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def scaffold_input(path: Path) -> None:
    payload = {
        "client": {
            "name": "Client Name",
            "primary_contact": "owner@example.com",
            "website": "https://example.com",
        },
        "services": {
            "primary": ["HVAC Maintenance", "Dryer Vent Cleaning"],
            "secondary": ["Chimney Services"],
        },
        "keywords": ["hvac maintenance denver", "dryer vent cleaning"],
        "service_areas": ["Denver", "Colorado Springs"],
        "measurement": {
            "cadence": "monthly",
            "rank_tracking_tool": "Example Tracker",
            "gsc_access": "yes",
            "analytics_access": "yes",
        },
        "alerts": {
            "drop_alert": "10 positions",
            "volatility": "15 positions",
        },
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def load_input(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"Input file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc


def render_markdown(data: dict[str, Any]) -> str:
    client = data.get("client", {})
    services = data.get("services", {})
    measurement = data.get("measurement", {})
    alerts = data.get("alerts", {})
    keywords = data.get("keywords", [])
    service_areas = data.get("service_areas", [])

    lines: list[str] = []
    lines.append(f"# Measurement intake for {client.get('name', '[Client]')}")
    lines.append(f"Generated: {now_iso()}")
    lines.append("")
    lines.append("## Client profile")
    lines.append(f"- Primary contact: {client.get('primary_contact', '[contact]')}")
    lines.append(f"- Website: {client.get('website', '[website]')}")
    if service_areas:
        lines.append("- Service Areas:")
        for area in service_areas:
            lines.append(f"  - {area}")
    lines.append("")
    lines.append("## Services")
    if services.get("primary"):
        lines.append("- Primary services:")
        for svc in services["primary"]:
            lines.append(f"  - {svc}")
    if services.get("secondary"):
        lines.append("- Secondary services:")
        for svc in services["secondary"]:
            lines.append(f"  - {svc}")
    lines.append("")
    lines.append("## Keywords")
    for kw in keywords:
        lines.append(f"- {kw}")
    lines.append("")
    lines.append("## Measurement setup")
    lines.append(f"- Cadence: {measurement.get('cadence', '[cadence]')}")
    lines.append(f"- Rank tracking tool: {measurement.get('rank_tracking_tool', '[tool]')}")
    lines.append(f"- GSC access: {measurement.get('gsc_access', '[yes/no]')}")
    lines.append(f"- Analytics access: {measurement.get('analytics_access', '[yes/no]')}")
    lines.append("")
    lines.append("## Alerts")
    lines.append(f"- Drop alert threshold: {alerts.get('drop_alert', '[positions]')}")
    lines.append(f"- Volatility threshold: {alerts.get('volatility', '[positions]')}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate measurement intake markdown.")
    parser.add_argument("--client-slug", required=True, help="Client slug under outputs/")
    parser.add_argument(
        "--input",
        default=None,
        help="Input JSON path (default: outputs/<client>/reports/measurement-intake-input.json)",
    )
    parser.add_argument(
        "--scaffold",
        action="store_true",
        help="Create scaffold input file if missing.",
    )
    args = parser.parse_args()

    base_dir = Path("outputs") / args.client_slug
    report_dir = base_dir / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    input_path = Path(args.input) if args.input else report_dir / "measurement-intake-input.json"
    if not input_path.exists():
        if args.scaffold:
            scaffold_input(input_path)
            print(f"wrote scaffold input to {input_path}")
            return
        raise SystemExit(f"Input file not found: {input_path}. Use --scaffold to create one.")

    data = load_input(input_path)
    md_path = report_dir / "measurement-intake.md"
    json_path = report_dir / "measurement-intake.json"

    md_path.write_text(render_markdown(data), encoding="utf-8")
    json_path.write_text(json.dumps({"generated_at": now_iso(), "data": data}, indent=2), encoding="utf-8")

    print(f"wrote {md_path}")
    print(f"wrote {json_path}")


if __name__ == "__main__":
    main()
