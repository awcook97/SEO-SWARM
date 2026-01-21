#!/usr/bin/env python3
"""Generate competitor snapshot table + gap notes from structured inputs."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def scaffold_input(path: Path) -> None:
    payload = {
        "client": {
            "name": "Client Name",
            "period": "2026-01",
            "prepared_by": "Analyst Name",
            "data_sources": ["SERP export", "Rank tracker"],
            "exported_at": now_iso(),
        },
        "competitors": [
            {
                "name": "Competitor A",
                "domain": "example.com",
                "primary_services": ["Service 1", "Service 2"],
                "top_pages": [
                    {"keyword": "service keyword", "url": "https://example.com/service"},
                    {"keyword": "city keyword", "url": "https://example.com/location"},
                ],
                "serp_features": ["Local Pack", "FAQ"],
                "notes": "Verified via SERP export dated 2026-01-01.",
            }
        ],
        "gaps": {
            "content": ["Missing service FAQ section"],
            "service_areas": ["No location page for [City]"],
            "serp_features": ["No FAQ schema on service pages"],
            "reviews": ["Competitors show review count; ours missing."],
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


def render_table_row(competitor: dict[str, Any]) -> str:
    name = competitor.get("name") or competitor.get("domain") or "[Competitor]"
    services = ", ".join(competitor.get("primary_services", []) or [])
    top_pages = ", ".join(entry.get("url", "") for entry in competitor.get("top_pages", []) if entry.get("url"))
    features = ", ".join(competitor.get("serp_features", []) or [])
    notes = competitor.get("notes", "")
    return f"| {name} | {services or '[Services]'} | {top_pages or '[URLs]'} | {features or '[Features]'} | {notes or ''} |"


def render_gap_list(label: str, values: list[str] | None) -> list[str]:
    lines = [f"- {label}:"]
    if values:
        for entry in values:
            lines.append(f"  - {entry}")
    else:
        lines.append("  - [None]")
    return lines


def render_markdown(data: dict[str, Any]) -> str:
    client = data.get("client", {})
    competitors = data.get("competitors", [])
    gaps = data.get("gaps", {})

    lines: list[str] = []
    lines.append(f"# Competitor snapshot for {client.get('name', '[Client]')}")
    lines.append(f"Generated: {now_iso()}")
    lines.append("")
    lines.append("## Report header")
    lines.append(f"- Client: {client.get('name', '[Client]')}")
    lines.append(f"- Period: {client.get('period', '[Period]')}")
    lines.append(f"- Prepared by: {client.get('prepared_by', '[Analyst]')}")
    sources = ", ".join(client.get("data_sources", []) or [])
    lines.append(f"- Data sources: {sources or '[Sources]'}")
    lines.append(f"- Export timestamp: {client.get('exported_at', '[timestamp]')}")
    lines.append("")
    lines.append("## Competitor snapshot table")
    lines.append("| Competitor | Primary Services | Top Ranking Pages | SERP Features | Notes |")
    lines.append("| --- | --- | --- | --- | --- |")
    if competitors:
        for competitor in competitors:
            lines.append(render_table_row(competitor))
    else:
        lines.append("| [Competitor] | [Services] | [URLs] | [Features] | [Notes] |")
    lines.append("")
    lines.append("## Gap and opportunity notes")
    lines.extend(render_gap_list("Content gaps", gaps.get("content")))
    lines.extend(render_gap_list("Service area gaps", gaps.get("service_areas")))
    lines.extend(render_gap_list("SERP feature gaps", gaps.get("serp_features")))
    lines.extend(render_gap_list("Review/ratings gaps (verified only)", gaps.get("reviews")))
    lines.append("")
    lines.append("## Appendix")
    lines.append("- Export files: [List inputs used]")
    lines.append("- Notes or caveats: [Notes]")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate competitor snapshot table + gaps from JSON inputs.")
    parser.add_argument("--client-slug", required=True, help="Client slug under outputs/")
    parser.add_argument(
        "--input",
        default=None,
        help="Input JSON path (default: outputs/<client>/reports/competitor-snapshot-input.json)",
    )
    parser.add_argument("--scaffold", action="store_true", help="Create scaffold input file if missing.")
    args = parser.parse_args()

    base_dir = Path("outputs") / args.client_slug
    report_dir = base_dir / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    input_path = Path(args.input) if args.input else report_dir / "competitor-snapshot-input.json"
    if not input_path.exists():
        if args.scaffold:
            scaffold_input(input_path)
            print(f"wrote scaffold input to {input_path}")
            return
        raise SystemExit(f"Input file not found: {input_path}. Use --scaffold to create one.")

    data = load_input(input_path)
    md_path = report_dir / "competitor-snapshot.md"
    json_path = report_dir / "competitor-snapshot.json"

    md_path.write_text(render_markdown(data), encoding="utf-8")
    json_path.write_text(json.dumps({"generated_at": now_iso(), "data": data}, indent=2), encoding="utf-8")

    print(f"wrote {md_path}")
    print(f"wrote {json_path}")


if __name__ == "__main__":
    main()
