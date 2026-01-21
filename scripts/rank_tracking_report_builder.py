#!/usr/bin/env python3
"""Build a rank tracking report from CSV exports."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def normalize_header(value: str) -> str:
    return value.strip().lower().replace(" ", "_")


def scaffold_config(path: Path) -> None:
    payload = {
        "client": "Client Name",
        "period": "2026-01",
        "prepared_by": "Analyst Name",
        "data_sources": ["Rank tracker export"],
        "exported_at": now_iso(),
        "drop_threshold": 10,
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def load_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc


def parse_rank(value: str | None) -> int | None:
    if value is None:
        return None
    value = value.strip()
    if not value or value.upper() in {"NA", "N/A", "-"}:
        return None
    try:
        return int(float(value))
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


def row_value(row: dict[str, str], *keys: str) -> str:
    for key in keys:
        if key in row:
            return row[key]
    return ""


def build_report(rows: list[dict[str, str]], drop_threshold: int) -> tuple[list[dict[str, Any]], list[str]]:
    table_rows: list[dict[str, Any]] = []
    alerts: list[str] = []

    for row in rows:
        keyword = row_value(row, "keyword")
        location = row_value(row, "location")
        current_rank_raw = row_value(row, "current_rank", "current")
        best_rank_raw = row_value(row, "best_rank", "best")
        previous_rank_raw = row_value(row, "previous_rank", "previous")
        target_url = row_value(row, "target_url", "url")
        notes = row_value(row, "notes")

        current_rank = parse_rank(current_rank_raw)
        previous_rank = parse_rank(previous_rank_raw)
        delta = None
        if current_rank is not None and previous_rank is not None:
            delta = previous_rank - current_rank

        table_rows.append(
            {
                "keyword": keyword,
                "location": location,
                "current_rank": current_rank_raw or "[Current]",
                "change": f"{delta:+d}" if delta is not None else "",
                "best_rank": best_rank_raw or "[Best]",
                "target_url": target_url or "[URL]",
                "notes": notes,
            }
        )

        if delta is not None and delta <= -drop_threshold:
            alerts.append(
                f"{keyword or '[Keyword]'} ({location or 'Location'}) dropped {abs(delta)} positions"
            )

    return table_rows, alerts


def render_markdown(config: dict[str, Any], table_rows: list[dict[str, Any]], alerts: list[str]) -> str:
    lines: list[str] = []
    lines.append(f"# Rank tracking report for {config.get('client', '[Client]')}")
    lines.append(f"Generated: {now_iso()}")
    lines.append("")
    lines.append("## Report header")
    lines.append(f"- Client: {config.get('client', '[Client]')}")
    lines.append(f"- Period: {config.get('period', '[Period]')}")
    lines.append(f"- Prepared by: {config.get('prepared_by', '[Analyst]')}")
    sources = ", ".join(config.get("data_sources", []) or [])
    lines.append(f"- Data sources: {sources or '[Sources]'}")
    lines.append(f"- Export timestamp: {config.get('exported_at', '[timestamp]')}")
    lines.append("")
    lines.append("## Executive summary")
    lines.append("- Net change in visibility: [Summary]")
    lines.append("- Top gains: [List] ")
    lines.append("- Top drops: [List]")
    lines.append("- Priority actions: [Actions]")
    lines.append("")
    lines.append("## Rank tracking summary")
    lines.append("")
    lines.append("### Keyword performance table")
    lines.append("| Keyword | Location | Current Rank | Change | Best Rank | Target URL | Notes |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    if table_rows:
        for row in table_rows:
            lines.append(
                "| {keyword} | {location} | {current_rank} | {change} | {best_rank} | {target_url} | {notes} |".format(
                    **row
                )
            )
    else:
        lines.append("| [Keyword] | [City] | [#] | [+/-] | [#] | [URL] | [Note] |")
    lines.append("")
    lines.append("### Alerts")
    if alerts:
        for alert in alerts:
            lines.append(f"- {alert}")
    else:
        lines.append("- None")
    lines.append("")
    lines.append("## Recommendations")
    lines.append("1) [Action 1] - [Owner] - [Due date]")
    lines.append("2) [Action 2] - [Owner] - [Due date]")
    lines.append("3) [Action 3] - [Owner] - [Due date]")
    lines.append("")
    lines.append("## Appendix")
    lines.append("- Export files: [List inputs used]")
    lines.append("- Notes or caveats: [Notes]")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate rank tracking report markdown from CSV export.")
    parser.add_argument("--client-slug", required=True, help="Client slug under outputs/")
    parser.add_argument(
        "--input",
        default=None,
        help="Input CSV path (default: outputs/<client>/reports/rank-tracking.csv)",
    )
    parser.add_argument(
        "--config",
        default=None,
        help="Config JSON path (default: outputs/<client>/reports/rank-tracking-config.json)",
    )
    parser.add_argument("--scaffold-config", action="store_true", help="Create scaffold config file if missing.")
    args = parser.parse_args()

    base_dir = Path("outputs") / args.client_slug
    report_dir = base_dir / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    csv_path = Path(args.input) if args.input else report_dir / "rank-tracking.csv"
    config_path = Path(args.config) if args.config else report_dir / "rank-tracking-config.json"
    if args.scaffold_config and not config_path.exists():
        scaffold_config(config_path)
        print(f"wrote scaffold config to {config_path}")

    config = load_config(config_path)
    if not csv_path.exists():
        raise SystemExit(f"Input CSV not found: {csv_path}")

    rows = load_csv(csv_path)
    drop_threshold = int(config.get("drop_threshold", 10))
    table_rows, alerts = build_report(rows, drop_threshold)

    md_path = report_dir / "rank-tracking-report.md"
    json_path = report_dir / "rank-tracking-report.json"

    md_path.write_text(render_markdown(config, table_rows, alerts), encoding="utf-8")
    json_path.write_text(
        json.dumps(
            {"generated_at": now_iso(), "config": config, "rows": table_rows, "alerts": alerts},
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"wrote {md_path}")
    print(f"wrote {json_path}")


if __name__ == "__main__":
    main()
