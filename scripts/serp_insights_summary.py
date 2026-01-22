#!/usr/bin/env python3
"""Summarize SERP insights from approved exports without fabrication."""

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
            "data_sources": ["SERP export"],
            "exported_at": now_iso(),
        },
        "serp_patterns": [
            "Local pack appears for 8/10 primary keywords.",
            "FAQ rich results visible on service keywords.",
        ],
        "competitor_gaps": [
            "Competitors include location pages for [City] while client does not.",
            "Competitor A uses FAQ schema on service pages.",
        ],
        "feature_targets": ["Local Pack", "FAQ", "Reviews"],
        "recommended_angles": ["Highlight financing options", "Add service FAQ section"],
        "notes": ["All observations are from the 2026-01-01 SERP export."]
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def load_input(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"Input file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc


def render_list(title: str, items: list[str] | None) -> list[str]:
    lines = [f"## {title}"]
    if items:
        for entry in items:
            lines.append(f"- {entry}")
    else:
        lines.append("- [None]")
    lines.append("")
    return lines


def render_markdown(data: dict[str, Any]) -> str:
    client = data.get("client", {})
    lines: list[str] = []
    lines.append(f"# SERP insights summary for {client.get('name', '[Client]')}")
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

    lines.extend(render_list("SERP pattern notes", data.get("serp_patterns")))
    lines.extend(render_list("Competitor gap list", data.get("competitor_gaps")))
    lines.extend(render_list("SERP feature targets", data.get("feature_targets")))
    lines.extend(render_list("Recommended content angles", data.get("recommended_angles")))

    lines.append("## Notes")
    notes = data.get("notes") or []
    if notes:
        for note in notes:
            lines.append(f"- {note}")
    else:
        lines.append("- [Notes]")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate SERP insights summary from JSON inputs.")
    parser.add_argument("--client-slug", required=True, help="Client slug under data/outputs/")
    parser.add_argument(
        "--input",
        default=None,
        help="Input JSON path (default: data/outputs/<client>/reports/serp-insights-input.json)",
    )
    parser.add_argument("--scaffold", action="store_true", help="Create scaffold input file if missing.")
    args = parser.parse_args()

    base_dir = Path("data") / "outputs" / args.client_slug
    report_dir = base_dir / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    input_path = Path(args.input) if args.input else report_dir / "serp-insights-input.json"
    if not input_path.exists():
        if args.scaffold:
            scaffold_input(input_path)
            print(f"wrote scaffold input to {input_path}")
            return
        raise SystemExit(f"Input file not found: {input_path}. Use --scaffold to create one.")

    data = load_input(input_path)
    md_path = report_dir / "serp-insights-summary.md"
    json_path = report_dir / "serp-insights-summary.json"

    md_path.write_text(render_markdown(data), encoding="utf-8")
    json_path.write_text(json.dumps({"generated_at": now_iso(), "data": data}, indent=2), encoding="utf-8")

    print(f"wrote {md_path}")
    print(f"wrote {json_path}")


if __name__ == "__main__":
    main()
