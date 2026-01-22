#!/usr/bin/env python3
"""Aggregate service brief markdown files into a summary report."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


SECTION_MARKERS = {
    "headings": "## Page structure",
    "ctas": "### CTAs (extracted)",
    "links": "## Internal links (sampled)",
    "schema": "## Schema types (detected)",
    "faqs": "## FAQs (extracted)",
}


@dataclass
class BriefSummary:
    slug: str
    url: str
    headings: list[str]
    ctas: list[str]
    internal_links: list[str]
    schema_types: list[str]
    faq_questions: list[str]


def parse_list_line(line: str) -> list[str]:
    if ":" not in line:
        return []
    _, rest = line.split(":", 1)
    items = [item.strip() for item in rest.split(",") if item.strip()]
    return items


def parse_brief(path: Path) -> BriefSummary:
    slug = path.stem
    url = ""
    headings: list[str] = []
    ctas: list[str] = []
    internal_links: list[str] = []
    schema_types: list[str] = []
    faq_questions: list[str] = []

    active = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            if active in {"ctas", "links", "schema", "faqs"}:
                active = None
            continue

        if line.startswith("- URL:"):
            url = line.replace("- URL:", "", 1).strip()
            continue

        if line == SECTION_MARKERS["headings"]:
            active = "headings"
            continue
        if line == SECTION_MARKERS["ctas"]:
            active = "ctas"
            continue
        if line == SECTION_MARKERS["links"]:
            active = "links"
            continue
        if line == SECTION_MARKERS["schema"]:
            active = "schema"
            continue
        if line == SECTION_MARKERS["faqs"]:
            active = "faqs"
            continue

        if active == "headings" and line.startswith("- H2/H3 headings:"):
            headings = parse_list_line(line)
            continue

        if active == "ctas" and line.startswith("- "):
            ctas.append(line[2:].strip())
            continue

        if active == "links" and line.startswith("- "):
            internal_links.append(line[2:].strip())
            continue

        if active == "schema" and line.startswith("- "):
            schema_types.append(line[2:].strip())
            continue

        if active == "faqs" and line.startswith("- Q:"):
            faq_questions.append(line.replace("- Q:", "", 1).strip())
            continue

    return BriefSummary(
        slug=slug,
        url=url,
        headings=headings,
        ctas=ctas,
        internal_links=internal_links,
        schema_types=schema_types,
        faq_questions=faq_questions,
    )


def render_markdown(
    summaries: list[BriefSummary],
    heading_counts: Counter,
    cta_counts: Counter,
    schema_counts: Counter,
) -> str:
    lines: list[str] = []
    lines.append("# Service brief summary")
    lines.append("")
    lines.append("## Totals")
    lines.append(f"- Briefs analyzed: {len(summaries)}")
    lines.append("")

    lines.append("## Top headings")
    for text, count in heading_counts.most_common(20):
        lines.append(f"- {text} ({count})")
    if not heading_counts:
        lines.append("- [No headings found]")
    lines.append("")

    lines.append("## Top CTAs")
    for text, count in cta_counts.most_common(20):
        lines.append(f"- {text} ({count})")
    if not cta_counts:
        lines.append("- [No CTA text found]")
    lines.append("")

    lines.append("## Schema types")
    for text, count in schema_counts.most_common():
        lines.append(f"- {text} ({count})")
    if not schema_counts:
        lines.append("- [No schema types found]")
    lines.append("")

    lines.append("## Per-page snapshot")
    for summary in summaries:
        lines.append(f"### {summary.slug}")
        if summary.url:
            lines.append(f"- URL: {summary.url}")
        lines.append(f"- Headings: {', '.join(summary.headings) if summary.headings else '[none]'}")
        lines.append(f"- CTAs: {', '.join(summary.ctas) if summary.ctas else '[none]'}")
        lines.append(f"- Schema: {', '.join(summary.schema_types) if summary.schema_types else '[none]'}")
        lines.append(f"- FAQ questions: {len(summary.faq_questions)}")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize service briefs.")
    parser.add_argument("--client-slug", required=True, help="Client slug under data/outputs/")
    args = parser.parse_args()

    briefs_dir = Path("data") / "outputs" / args.client_slug / "reports" / "service-briefs"
    if not briefs_dir.exists():
        raise SystemExit(f"Briefs folder not found: {briefs_dir}")

    summaries: list[BriefSummary] = []
    heading_counts: Counter = Counter()
    cta_counts: Counter = Counter()
    schema_counts: Counter = Counter()

    for path in sorted(briefs_dir.glob("*.md")):
        summary = parse_brief(path)
        summaries.append(summary)
        heading_counts.update(summary.headings)
        cta_counts.update(summary.ctas)
        schema_counts.update(summary.schema_types)

    report_dir = Path("data") / "outputs" / args.client_slug / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    json_path = report_dir / "service-briefs-summary.json"
    md_path = report_dir / "service-briefs-summary.md"

    payload = {
        "client": args.client_slug,
        "total": len(summaries),
        "top_headings": heading_counts.most_common(20),
        "top_ctas": cta_counts.most_common(20),
        "schema_types": schema_counts.most_common(),
        "pages": [
            {
                "slug": summary.slug,
                "url": summary.url,
                "headings": summary.headings,
                "ctas": summary.ctas,
                "internal_links": summary.internal_links,
                "schema_types": summary.schema_types,
                "faq_questions": summary.faq_questions,
            }
            for summary in summaries
        ],
    }

    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    md_path.write_text(
        render_markdown(summaries, heading_counts, cta_counts, schema_counts),
        encoding="utf-8",
    )
    print(f"wrote {md_path}")
    print(f"wrote {json_path}")


if __name__ == "__main__":
    main()
