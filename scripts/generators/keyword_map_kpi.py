#!/usr/bin/env python3
"""Generate keyword map and KPI targets report from approved inputs."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class KeywordEntry:
    keyword: str
    target_url: str
    intent: str | None = None
    priority: str | None = None
    service: str | None = None
    location: str | None = None
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
        "client": {
            "name": "[client name]",
            "website": "https://example.com",
        },
        "serp_features": ["Local pack", "Maps", "FAQ", "Reviews"],
        "kpi_targets": {
            "cadence": "monthly",
            "rank_tracking": {
                "top_3": "[target count]",
                "top_10": "[target count]",
                "top_20": "[target count]",
            },
            "traffic": {
                "organic_sessions": "[target range]",
                "form_fills": "[target range]",
            },
        },
        "keywords": [
            {
                "keyword": "[primary keyword]",
                "target_url": "/service-page",
                "intent": "service",
                "priority": "primary",
                "service": "[service name]",
                "location": "[city]",
                "notes": "[notes]",
            }
        ],
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def parse_keywords(items: list[dict[str, Any]]) -> list[KeywordEntry]:
    entries: list[KeywordEntry] = []
    for item in items:
        keyword = item.get("keyword")
        target_url = item.get("target_url")
        if not keyword or not target_url:
            raise SystemExit("Each keyword entry must include keyword and target_url")
        entries.append(
            KeywordEntry(
                keyword=keyword,
                target_url=target_url,
                intent=item.get("intent"),
                priority=item.get("priority"),
                service=item.get("service"),
                location=item.get("location"),
                notes=item.get("notes"),
            )
        )
    return entries


def render_markdown(client: dict[str, Any], keywords: list[KeywordEntry], kpis: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# Keyword map + KPI targets")
    lines.append("")
    lines.append(f"Generated: {now_iso()}")
    lines.append("")

    lines.append("## Client")
    lines.append(f"- Name: {client.get('name') or '[client name]'}")
    lines.append(f"- Website: {client.get('website') or '[website]'}")
    lines.append("")

    lines.append("## KPI targets")
    cadence = kpis.get("cadence") or "[cadence]"
    lines.append(f"- Cadence: {cadence}")
    for section, values in kpis.items():
        if section == "cadence":
            continue
        lines.append(f"- {section}:")
        if isinstance(values, dict):
            for key, value in values.items():
                lines.append(f"  - {key}: {value}")
        else:
            lines.append(f"  - {values}")
    lines.append("")

    lines.append("## Keyword map")
    lines.append("| Keyword | Target URL | Intent | Priority | Service | Location | Notes |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for entry in keywords:
        lines.append(
            f"| {entry.keyword} | {entry.target_url} | {entry.intent or ''} | {entry.priority or ''} |"
            f" {entry.service or ''} | {entry.location or ''} | {entry.notes or ''} |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate keyword map and KPI targets.")
    parser.add_argument("--client-slug", required=True, help="Client slug under data/outputs/")
    parser.add_argument(
        "--input",
        default=None,
        help="Input JSON path (default: data/outputs/<client>/reports/keyword-map-input.json)",
    )
    parser.add_argument(
        "--scaffold",
        action="store_true",
        help="Create a scaffold input file if it does not exist.",
    )
    args = parser.parse_args()

    base_dir = Path("data") / "outputs" / args.client_slug
    report_dir = base_dir / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    input_path = Path(args.input) if args.input else report_dir / "keyword-map-input.json"
    if not input_path.exists():
        if args.scaffold:
            scaffold_input(input_path)
            print(f"wrote scaffold input to {input_path}")
            return
        raise SystemExit(f"Input file not found: {input_path}. Use --scaffold to create one.")

    data = load_input(input_path)
    client = data.get("client", {})
    keywords = parse_keywords(data.get("keywords", []))
    kpis = data.get("kpi_targets", {})

    payload = {
        "generated_at": now_iso(),
        "client": client,
        "kpi_targets": kpis,
        "keywords": [entry.__dict__ for entry in keywords],
    }

    json_path = report_dir / "keyword-map-kpi.json"
    md_path = report_dir / "keyword-map-kpi.md"

    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(client, keywords, kpis), encoding="utf-8")

    print(f"wrote {md_path}")
    print(f"wrote {json_path}")


if __name__ == "__main__":
    main()
