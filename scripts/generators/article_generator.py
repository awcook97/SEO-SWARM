#!/usr/bin/env python3
"""Generate markdown articles from content briefs."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class ContentBriefSnapshot:
    brief_id: str
    service: str = ""
    city: str = ""
    topic: str = ""
    primary_keyword: str = ""
    secondary_keywords: list[str] = field(default_factory=list)
    target_url: str = ""
    intent: str = ""
    cta: str = ""
    value_props: list[str] = field(default_factory=list)
    proof_points: list[str] = field(default_factory=list)
    faqs: list[tuple[str, str]] = field(default_factory=list)
    internal_links: list[str] = field(default_factory=list)
    schema_types: list[str] = field(default_factory=list)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_input(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"Input file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc


def load_brief(briefs_dir: Path, brief_id: str) -> ContentBriefSnapshot | None:
    """Load a content brief from markdown file."""
    brief_path = briefs_dir / f"{brief_id}.md"
    if not brief_path.exists():
        return None

    snapshot = ContentBriefSnapshot(brief_id=brief_id)
    content = brief_path.read_text(encoding="utf-8")

    # Parse basic fields from content brief
    for line in content.splitlines():
        line = line.strip()
        if line.startswith("- Service:"):
            snapshot.service = line.replace("- Service:", "").strip()
        elif line.startswith("- City:"):
            snapshot.city = line.replace("- City:", "").strip()
        elif line.startswith("- Topic:"):
            snapshot.topic = line.replace("- Topic:", "").strip()
        elif line.startswith("- Primary keyword:"):
            snapshot.primary_keyword = line.replace("- Primary keyword:", "").strip()
        elif line.startswith("- Secondary keywords:"):
            kws = line.replace("- Secondary keywords:", "").strip()
            snapshot.secondary_keywords = [k.strip() for k in kws.split(",") if k.strip()]
        elif line.startswith("- Target URL:"):
            snapshot.target_url = line.replace("- Target URL:", "").strip()
        elif line.startswith("- Audience intent:"):
            snapshot.intent = line.replace("- Audience intent:", "").strip()
        elif line.startswith("- Primary CTA:"):
            snapshot.cta = line.replace("- Primary CTA:", "").strip()

    return snapshot


def scaffold_input(output_path: Path) -> None:
    """Create a scaffold input JSON file."""
    payload = {
        "client": {
            "name": "[client name]",
            "website": "[website]",
            "phone": "[phone]",
            "hours": "[business hours]",
        },
        "articles": [
            {
                "id": "sample-service-area-article",
                "type": "service-area-landing",
                "service": "[primary service]",
                "city": "[city or area]",
                "primary_keyword": "[primary keyword]",
                "secondary_keywords": ["[keyword 1]", "[keyword 2]"],
                "target_url": "[target url]",
                "content_brief": "[brief-id or leave empty]",
                "proof_points": ["[proof point 1]", "[proof point 2]"],
                "service_areas": ["[area 1]", "[area 2]"],
                "internal_links": {
                    "service_page": "[service page url]",
                    "contact_page": "[contact page url]",
                },
                "notes": "[add article-specific notes]",
            },
            {
                "id": "sample-topical-guide",
                "type": "topical-guide",
                "topic": "[topic]",
                "primary_keyword": "[primary keyword]",
                "secondary_keywords": ["[keyword 1]", "[keyword 2]"],
                "target_url": "[target url]",
                "content_brief": "[brief-id or leave empty]",
                "internal_links": {
                    "service_page": "[related service page url]",
                    "contact_page": "[contact page url]",
                },
                "notes": "[add article-specific notes]",
            },
        ],
    }

    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def render_service_area_article(
    entry: dict[str, Any], client: dict[str, Any], snapshot: ContentBriefSnapshot | None
) -> str:
    """Render a service-area landing article."""
    lines: list[str] = []

    article_id = entry.get("id") or "article"
    service = entry.get("service") or (snapshot.service if snapshot else "[service]")
    city = entry.get("city") or (snapshot.city if snapshot else "[city]")
    client_name = client.get("name") or "[Client Name]"
    phone = client.get("phone") or "[phone]"
    hours = client.get("hours") or "[business hours]"

    # Header
    lines.append(f"# {service} in {city}")
    lines.append("")
    lines.append(f"Generated: {now_iso()}")
    lines.append(f"Type: Service-area landing article")
    lines.append(f"ID: {article_id}")
    lines.append("")

    # Introduction
    lines.append("## Introduction")
    lines.append("")
    lines.append(
        f"[2 to 3 sentence intro about {service} in {city} with local context. Use only approved facts.]"
    )
    lines.append("")

    # What this service covers
    lines.append("## What This Service Covers")
    lines.append("")
    lines.append(f"[2 to 3 short paragraphs explaining {service}]")
    lines.append("")
    lines.append("Our service includes:")
    lines.append("- [Scope item 1]")
    lines.append("- [Scope item 2]")
    lines.append("- [Scope item 3]")
    lines.append("")

    # Local considerations
    lines.append(f"## Local Considerations in {city}")
    lines.append("")
    lines.append(
        f"[Climate, housing, or system context for {city} - only include verified information]"
    )
    lines.append("")

    service_areas = entry.get("service_areas", [])
    if service_areas:
        lines.append(f"We serve these areas in {city}:")
        for area in service_areas:
            lines.append(f"- {area}")
        lines.append("")

    # Common issues
    lines.append(f"## Common Issues in {city}")
    lines.append("")
    lines.append(f"Residents in {city} often experience:")
    lines.append("- [Issue 1]")
    lines.append("- [Issue 2]")
    lines.append("- [Issue 3]")
    lines.append("- [Issue 4]")
    lines.append("- [Issue 5]")
    lines.append("")

    # Why choose us
    lines.append(f"## Why Choose {client_name}")
    lines.append("")
    proof_points = entry.get("proof_points") or (snapshot.proof_points if snapshot else [])
    if proof_points:
        for point in proof_points:
            lines.append(f"- {point}")
    else:
        lines.append("- [Proof point 1 with source]")
        lines.append("- [Proof point 2 with source]")
        lines.append("- [Proof point 3 with source]")
    lines.append("")

    # FAQs
    lines.append("## Frequently Asked Questions")
    lines.append("")
    if snapshot and snapshot.faqs:
        for q, a in snapshot.faqs[:7]:
            lines.append(f"### {q}")
            lines.append("")
            lines.append(f"{a}")
            lines.append("")
    else:
        for i in range(1, 6):
            lines.append(f"### [Question {i}]")
            lines.append("")
            lines.append(f"[Answer {i}]")
            lines.append("")

    # Call to action
    lines.append("## Get Started Today")
    lines.append("")
    cta = entry.get("cta") or (snapshot.cta if snapshot else "Call us today")
    lines.append(f"{cta} at {phone}")
    lines.append("")
    lines.append(f"Hours: {hours}")
    lines.append("")

    # Metadata section
    lines.append("---")
    lines.append("")
    lines.append("## Metadata")
    lines.append("")
    lines.append(f"- **Title tag**: {service} in {city} | {client_name}")
    lines.append(
        f"- **Meta description**: {service} in {city}. [Add proof point]. Call {phone}."
    )
    lines.append("- **Schema types**: LocalBusiness, Service, FAQPage")
    lines.append("")

    # Internal links
    lines.append("## Internal Links")
    lines.append("")
    internal_links = entry.get("internal_links", {})
    if internal_links:
        for link_type, url in internal_links.items():
            lines.append(f"- {link_type}: {url}")
    else:
        lines.append("- [Add internal link targets]")
    lines.append("")

    return "\n".join(lines)


def render_topical_guide(
    entry: dict[str, Any], client: dict[str, Any], snapshot: ContentBriefSnapshot | None
) -> str:
    """Render a topical service guide article."""
    lines: list[str] = []

    article_id = entry.get("id") or "article"
    topic = entry.get("topic") or (snapshot.topic if snapshot else "[topic]")
    client_name = client.get("name") or "[Client Name]"
    phone = client.get("phone") or "[phone]"
    hours = client.get("hours") or "[business hours]"

    # Header
    lines.append(f"# {topic} for Homeowners")
    lines.append("")
    lines.append(f"Generated: {now_iso()}")
    lines.append(f"Type: Topical service guide")
    lines.append(f"ID: {article_id}")
    lines.append("")

    # Introduction
    lines.append("## Introduction")
    lines.append("")
    lines.append(
        f"[2 to 3 sentence overview of {topic} and who this guide is for. Use approved sources only.]"
    )
    lines.append("")

    # Key takeaways
    lines.append("## Key Takeaways")
    lines.append("")
    lines.append("- [Takeaway 1]")
    lines.append("- [Takeaway 2]")
    lines.append("- [Takeaway 3]")
    lines.append("")

    # Core sections
    lines.append(f"## Understanding {topic}")
    lines.append("")
    lines.append(f"[Explanation of {topic} concept]")
    lines.append("")

    lines.append("## Step-by-Step Guide")
    lines.append("")
    lines.append("1. [Step 1]")
    lines.append("2. [Step 2]")
    lines.append("3. [Step 3]")
    lines.append("4. [Step 4]")
    lines.append("")

    lines.append("## Common Mistakes to Avoid")
    lines.append("")
    lines.append("- [Mistake 1]")
    lines.append("- [Mistake 2]")
    lines.append("- [Mistake 3]")
    lines.append("")

    # When to call a pro
    lines.append("## When to Call a Professional")
    lines.append("")
    lines.append("Contact a professional if you experience:")
    lines.append("- [Symptom 1]")
    lines.append("- [Symptom 2]")
    lines.append("- [Symptom 3]")
    lines.append("")

    # FAQs
    lines.append("## Frequently Asked Questions")
    lines.append("")
    if snapshot and snapshot.faqs:
        for q, a in snapshot.faqs[:6]:
            lines.append(f"### {q}")
            lines.append("")
            lines.append(f"{a}")
            lines.append("")
    else:
        for i in range(1, 5):
            lines.append(f"### [Question {i}]")
            lines.append("")
            lines.append(f"[Answer {i}]")
            lines.append("")

    # Call to action
    lines.append("## Need Professional Help?")
    lines.append("")
    lines.append(f"Contact {client_name} at {phone}")
    lines.append("")
    lines.append(f"Hours: {hours}")
    lines.append("")

    # Metadata section
    lines.append("---")
    lines.append("")
    lines.append("## Metadata")
    lines.append("")
    lines.append(f"- **Title tag**: {topic} | {client_name}")
    lines.append(f"- **Meta description**: {topic} guide with tips from {client_name}. Call {phone}.")
    lines.append("- **Schema types**: Article, FAQPage")
    lines.append("")

    # Internal links
    lines.append("## Internal Links")
    lines.append("")
    internal_links = entry.get("internal_links", {})
    if internal_links:
        for link_type, url in internal_links.items():
            lines.append(f"- {link_type}: {url}")
    else:
        lines.append("- [Add internal link targets]")
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate markdown articles from content briefs.")
    parser.add_argument("--client-slug", required=True, help="Client slug under data/outputs/")
    parser.add_argument(
        "--input",
        default=None,
        help="Input JSON path (default: data/outputs/<client>/reports/article-input.json)",
    )
    parser.add_argument(
        "--scaffold",
        action="store_true",
        help="Create a scaffold input file if it does not exist.",
    )
    args = parser.parse_args()

    base_dir = Path("data") / "outputs" / args.client_slug
    briefs_dir = base_dir / "reports" / "content-briefs"

    input_path = Path(args.input) if args.input else base_dir / "reports" / "article-input.json"

    if not input_path.exists():
        if args.scaffold:
            scaffold_input(input_path)
            print(f"wrote scaffold input to {input_path}")
            return
        raise SystemExit(f"Input file not found: {input_path}. Use --scaffold to create one.")

    data = load_input(input_path)
    articles = data.get("articles") or []
    if not articles:
        raise SystemExit("Input JSON must include articles list")

    client = data.get("client", {})
    output_dir = base_dir / "articles"
    output_dir.mkdir(parents=True, exist_ok=True)

    summary = {
        "client": client,
        "generated_at": now_iso(),
        "total": 0,
        "articles": [],
    }

    for entry in articles:
        article_id = entry.get("id") or "article"
        article_type = entry.get("type") or "service-area-landing"
        brief_id = entry.get("content_brief")

        # Load content brief if specified
        snapshot = None
        if brief_id and briefs_dir.exists():
            snapshot = load_brief(briefs_dir, brief_id)

        # Render article based on type
        if article_type == "topical-guide":
            content = render_topical_guide(entry, client, snapshot)
        else:
            content = render_service_area_article(entry, client, snapshot)

        # Write article
        out_md = output_dir / f"{article_id}.md"
        out_md.write_text(content, encoding="utf-8")

        summary["articles"].append(
            {
                "id": article_id,
                "type": article_type,
                "content_brief": brief_id,
                "output_md": str(out_md),
            }
        )

    summary["total"] = len(summary["articles"])
    summary_path = base_dir / "reports" / "articles.json"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"wrote {summary['total']} article(s)")
    print(f"wrote summary to {summary_path}")


if __name__ == "__main__":
    main()
