#!/usr/bin/env python3
"""Generate markdown content briefs from service brief sources."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SECTION_MARKERS = {
    "page_structure": "## Page structure",
    "signals": "## Signals",
    "value_props": "### Value props (extracted)",
    "proof_points": "### Proof points (extracted)",
    "ctas": "### CTAs (extracted)",
    "links": "## Internal links (sampled)",
    "schema": "## Schema types (detected)",
    "faqs": "## FAQs (extracted)",
}


@dataclass
class ServiceBriefSnapshot:
    slug: str
    url: str = ""
    page_title: str = ""
    meta_description: str = ""
    h1: str = ""
    pricing_mentions: list[str] = field(default_factory=list)
    headings: list[str] = field(default_factory=list)
    value_props: list[str] = field(default_factory=list)
    proof_points: list[str] = field(default_factory=list)
    ctas: list[str] = field(default_factory=list)
    internal_links: list[str] = field(default_factory=list)
    schema_types: list[str] = field(default_factory=list)
    faqs: list[tuple[str, str]] = field(default_factory=list)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def parse_list_line(line: str) -> list[str]:
    if ":" not in line:
        return []
    _, rest = line.split(":", 1)
    return [item.strip() for item in rest.split(",") if item.strip()]


def parse_service_brief(path: Path) -> ServiceBriefSnapshot:
    snapshot = ServiceBriefSnapshot(slug=path.stem)

    active = None
    pending_question = None

    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            if active in {"value_props", "proof_points", "ctas", "links", "schema", "faqs"}:
                active = None
            continue

        if line == SECTION_MARKERS["page_structure"]:
            active = "page_structure"
            continue
        if line == SECTION_MARKERS["signals"]:
            active = "signals"
            continue
        if line == SECTION_MARKERS["value_props"]:
            active = "value_props"
            continue
        if line == SECTION_MARKERS["proof_points"]:
            active = "proof_points"
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

        if line.startswith("- URL:"):
            snapshot.url = line.replace("- URL:", "", 1).strip()
            continue
        if line.startswith("- Page title:"):
            snapshot.page_title = line.replace("- Page title:", "", 1).strip()
            continue
        if line.startswith("- Meta description:"):
            snapshot.meta_description = line.replace("- Meta description:", "", 1).strip()
            continue
        if line.startswith("- H1:"):
            snapshot.h1 = line.replace("- H1:", "", 1).strip()
            continue
        if line.startswith("- Pricing mentions:"):
            snapshot.pricing_mentions = parse_list_line(line)
            continue

        if active == "page_structure" and line.startswith("- H2/H3 headings:"):
            snapshot.headings = parse_list_line(line)
            continue

        if active == "value_props" and line.startswith("- "):
            snapshot.value_props.append(line[2:].strip())
            continue
        if active == "proof_points" and line.startswith("- "):
            snapshot.proof_points.append(line[2:].strip())
            continue
        if active == "ctas" and line.startswith("- "):
            snapshot.ctas.append(line[2:].strip())
            continue
        if active == "links" and line.startswith("- "):
            snapshot.internal_links.append(line[2:].strip())
            continue
        if active == "schema" and line.startswith("- "):
            snapshot.schema_types.append(line[2:].strip())
            continue
        if active == "faqs" and line.startswith("- Q:"):
            pending_question = line.replace("- Q:", "", 1).strip()
            continue
        if active == "faqs" and line.startswith("A:") and pending_question:
            answer = line.replace("A:", "", 1).strip()
            snapshot.faqs.append((pending_question, answer))
            pending_question = None
            continue

    return snapshot


def load_input(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"Input file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc


def scaffold_input(briefs_dir: Path, output_path: Path) -> None:
    entries = []
    for path in sorted(briefs_dir.glob("*.md")):
        entries.append(
            {
                "id": path.stem,
                "type": "service-page",
                "slug": path.stem,
                "service": "[service name]",
                "primary_keyword": "[primary keyword]",
                "target_url": "[target url]",
                "service_brief": path.stem,
                "notes": "[add brief-specific notes]",
            }
        )

    payload = {
        "client": {"name": "[client name]", "website": "[website]", "phone": "[phone]"},
        "briefs": entries,
    }

    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def render_brief(entry: dict[str, Any], snapshot: ServiceBriefSnapshot | None) -> str:
    lines: list[str] = []
    brief_id = entry.get("id") or entry.get("slug") or "brief"

    lines.append(f"# Content brief: {brief_id}")
    lines.append("")
    lines.append(f"Generated: {now_iso()}")
    lines.append("")

    lines.append("## Target page")
    lines.append(f"- Type: {entry.get('type') or '[type]'}")
    lines.append(f"- Service: {entry.get('service') or '[service]'}")
    lines.append(f"- City: {entry.get('city') or '[city]'}")
    lines.append(f"- Topic: {entry.get('topic') or '[topic]'}")
    lines.append(f"- Primary keyword: {entry.get('primary_keyword') or '[keyword]'}")
    lines.append(
        f"- Secondary keywords: {', '.join(entry.get('secondary_keywords', [])) or '[add keywords]'}"
    )
    lines.append(f"- Target URL: {entry.get('target_url') or '[target url]'}")
    lines.append(f"- Audience intent: {entry.get('intent') or '[intent]'}")
    lines.append(f"- Primary CTA: {entry.get('cta') or '[cta]'}")
    lines.append("")

    lines.append("## Brief inputs")
    if snapshot:
        lines.append(f"- Service brief source: {snapshot.url or snapshot.slug}")
        lines.append(f"- Source H1: {snapshot.h1 or '[missing]'}")
        if snapshot.pricing_mentions:
            lines.append(f"- Pricing mentions: {', '.join(snapshot.pricing_mentions)}")
        else:
            lines.append("- Pricing mentions: [none detected]")
    else:
        lines.append("- Service brief source: [missing]")
    notes = entry.get("notes") or "[add notes]"
    lines.append(f"- Notes: {notes}")
    lines.append("")

    lines.append("## Required sections")
    outline = entry.get("required_sections") or []
    if outline:
        for section in outline:
            lines.append(f"- {section}")
    elif snapshot and snapshot.headings:
        for heading in snapshot.headings:
            lines.append(f"- {heading}")
    else:
        lines.append("- [add required sections]")
    lines.append("")

    lines.append("## Source signals")
    if snapshot:
        if snapshot.value_props:
            lines.append("- Value props:")
            for prop in snapshot.value_props:
                lines.append(f"  - {prop}")
        else:
            lines.append("- Value props: [none extracted]")

        if snapshot.proof_points:
            lines.append("- Proof points:")
            for point in snapshot.proof_points:
                lines.append(f"  - {point}")
        else:
            lines.append("- Proof points: [none extracted]")

        if snapshot.ctas:
            lines.append("- CTAs:")
            for cta in snapshot.ctas:
                lines.append(f"  - {cta}")
        else:
            lines.append("- CTAs: [none extracted]")

        if snapshot.schema_types:
            lines.append(f"- Schema types: {', '.join(snapshot.schema_types)}")
        else:
            lines.append("- Schema types: [none detected]")

        lines.append(f"- Internal links sampled: {len(snapshot.internal_links)}")
        lines.append(f"- FAQ count: {len(snapshot.faqs)}")
    else:
        lines.append("- [no service brief data found]")
    lines.append("")

    lines.append("## Internal links and schema requirements")
    if entry.get("internal_links"):
        for link in entry["internal_links"]:
            lines.append(f"- {link}")
    else:
        lines.append("- [add internal link targets]")
    lines.append("- Schema requirements: [LocalBusiness/Service/FAQPage/etc]")
    lines.append("")

    lines.append("## Compliance checks")
    lines.append("- All claims backed by approved sources.")
    lines.append("- NAP matches approved inputs.")
    lines.append("- Placeholders resolved before publishing.")
    lines.append("")

    lines.append("## FAQs to include")
    if snapshot and snapshot.faqs:
        for question, answer in snapshot.faqs[:8]:
            lines.append(f"- Q: {question}")
            lines.append(f"  A: {answer or '[add answer]'}")
    else:
        lines.append("- [add 5 to 8 FAQs based on service brief]")
    lines.append("")

    return "\n".join(lines)


def build_payload(entry: dict[str, Any], snapshot: ServiceBriefSnapshot | None) -> dict[str, Any]:
    data: dict[str, Any] = {"brief": entry, "generated_at": now_iso()}
    if snapshot:
        data["service_brief"] = {
            "slug": snapshot.slug,
            "url": snapshot.url,
            "page_title": snapshot.page_title,
            "meta_description": snapshot.meta_description,
            "h1": snapshot.h1,
            "pricing_mentions": snapshot.pricing_mentions,
            "headings": snapshot.headings,
            "value_props": snapshot.value_props,
            "proof_points": snapshot.proof_points,
            "ctas": snapshot.ctas,
            "internal_links": snapshot.internal_links,
            "schema_types": snapshot.schema_types,
            "faq_count": len(snapshot.faqs),
        }
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate content briefs from service briefs.")
    parser.add_argument("--client-slug", required=True, help="Client slug under outputs/")
    parser.add_argument(
        "--input",
        default=None,
        help="Input JSON path (default: outputs/<client>/reports/content-brief-input.json)",
    )
    parser.add_argument(
        "--scaffold",
        action="store_true",
        help="Create a scaffold input file if it does not exist.",
    )
    args = parser.parse_args()

    base_dir = Path("outputs") / args.client_slug
    briefs_dir = base_dir / "reports" / "service-briefs"
    if not briefs_dir.exists():
        raise SystemExit(f"Service briefs folder not found: {briefs_dir}")

    input_path = Path(args.input) if args.input else base_dir / "reports" / "content-brief-input.json"
    if not input_path.exists():
        if args.scaffold:
            scaffold_input(briefs_dir, input_path)
            print(f"wrote scaffold input to {input_path}")
            return
        raise SystemExit(f"Input file not found: {input_path}. Use --scaffold to create one.")

    data = load_input(input_path)
    entries = data.get("briefs") or []
    if not entries:
        raise SystemExit("Input JSON must include briefs list")

    output_dir = base_dir / "reports" / "content-briefs"
    output_dir.mkdir(parents=True, exist_ok=True)

    summary = {
        "client": data.get("client", {}),
        "generated_at": now_iso(),
        "total": 0,
        "briefs": [],
    }

    for entry in entries:
        slug = entry.get("service_brief") or entry.get("slug")
        snapshot = None
        if slug:
            brief_path = briefs_dir / f"{slug}.md"
            if brief_path.exists():
                snapshot = parse_service_brief(brief_path)
        brief_id = entry.get("id") or entry.get("slug") or slug or "brief"
        out_md = output_dir / f"{brief_id}.md"
        out_md.write_text(render_brief(entry, snapshot), encoding="utf-8")

        summary["briefs"].append(
            {
                "id": brief_id,
                "type": entry.get("type"),
                "service_brief": slug,
                "output_md": str(out_md),
                "snapshot": build_payload(entry, snapshot),
            }
        )

    summary["total"] = len(summary["briefs"])
    summary_path = base_dir / "reports" / "content-briefs.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"wrote {summary_path}")


if __name__ == "__main__":
    main()
