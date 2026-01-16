#!/usr/bin/env python3
"""Generate a technical SEO audit scaffold report."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def render_markdown(client_slug: str) -> str:
    lines: list[str] = []
    lines.append("# Technical SEO audit")
    lines.append("")
    lines.append(f"Client: {client_slug}")
    lines.append(f"Generated: {now_iso()}")
    lines.append("")

    sections = [
        "Indexation",
        "Crawlability",
        "Performance (Core Web Vitals)",
        "Site architecture",
        "Structured data",
        "Mobile usability",
        "Security (HTTPS)",
        "Sitemaps and robots",
        "Redirects and errors",
        "Duplicate content",
    ]

    for section in sections:
        lines.append(f"## {section}")
        lines.append("- Findings: [add findings]")
        lines.append("- Impact: [add impact]")
        lines.append("- Recommended fix: [add fix]")
        lines.append("")

    lines.append("## Prioritized fixes")
    lines.append("- [P1] [fix] – [owner] – [target date]")
    lines.append("- [P2] [fix] – [owner] – [target date]")
    lines.append("")

    lines.append("## Inputs used")
    lines.append("- Crawl export: [link/path]")
    lines.append("- Performance summary: [link/path]")
    lines.append("- Known constraints: [platform/CMS notes]")
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate technical SEO audit scaffold.")
    parser.add_argument("--client-slug", required=True, help="Client slug under outputs/")
    parser.add_argument(
        "--output",
        default=None,
        help="Optional output markdown path (default: outputs/<client>/reports/technical-seo-audit.md)",
    )
    args = parser.parse_args()

    base_dir = Path("outputs") / args.client_slug
    report_dir = base_dir / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    md_path = Path(args.output) if args.output else report_dir / "technical-seo-audit.md"
    json_path = report_dir / "technical-seo-audit.json"

    md_path.write_text(render_markdown(args.client_slug), encoding="utf-8")
    payload = {
        "generated_at": now_iso(),
        "client": args.client_slug,
        "sections": [
            "Indexation",
            "Crawlability",
            "Performance (Core Web Vitals)",
            "Site architecture",
            "Structured data",
            "Mobile usability",
            "Security (HTTPS)",
            "Sitemaps and robots",
            "Redirects and errors",
            "Duplicate content",
        ],
    }
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print(f"wrote {md_path}")
    print(f"wrote {json_path}")


if __name__ == "__main__":
    main()
