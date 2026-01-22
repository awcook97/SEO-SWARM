#!/usr/bin/env python3
"""Generate a technical SEO audit report from cached HTML and live checks."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse, urljoin


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass
class Finding:
    label: str
    detail: str
    impact: str
    fix: str


@dataclass
class AuditSection:
    name: str
    findings: list[Finding] = field(default_factory=list)


def load_inputs_website(path: Path) -> str:
    if not path.exists():
        return ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("- Website:"):
            return line.split(":", 1)[1].strip()
    return ""


def load_cache_index(path: Path) -> dict[str, dict[str, str]]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def parse_schema_types(soup: Any) -> list[str]:
    types: list[str] = []
    for tag in soup.find_all("script"):
        if tag.get("type") != "application/ld+json":
            continue
        try:
            payload = json.loads(tag.string or "")
        except Exception:
            continue
        nodes = []
        if isinstance(payload, dict):
            nodes.append(payload)
            if isinstance(payload.get("@graph"), list):
                nodes.extend(payload["@graph"])
        elif isinstance(payload, list):
            nodes.extend(payload)
        for node in nodes:
            if not isinstance(node, dict):
                continue
            raw = node.get("@type")
            if isinstance(raw, list):
                for item in raw:
                    if isinstance(item, str):
                        types.append(item)
            elif isinstance(raw, str):
                types.append(raw)
    return sorted(set(types))


def extract_text(soup: Any) -> str:
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    return " ".join(soup.stripped_strings)


def render_markdown(client_slug: str, website: str, sections: list[AuditSection], metrics: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# Technical SEO audit")
    lines.append("")
    lines.append(f"Client: {client_slug}")
    if website:
        lines.append(f"Website: {website}")
    lines.append(f"Generated: {now_iso()}")
    lines.append("")

    lines.append("## Summary metrics")
    for key, value in metrics.items():
        lines.append(f"- {key}: {value}")
    lines.append("")

    for section in sections:
        lines.append(f"## {section.name}")
        if not section.findings:
            lines.append("- Findings: [none detected]")
            lines.append("")
            continue
        for finding in section.findings:
            lines.append(f"- Finding: {finding.label}")
            lines.append(f"  - Detail: {finding.detail}")
            lines.append(f"  - Impact: {finding.impact}")
            lines.append(f"  - Recommended fix: {finding.fix}")
        lines.append("")

    lines.append("## Prioritized fixes")
    lines.append("- [P1] [fix] – [owner] – [target date]")
    lines.append("- [P2] [fix] – [owner] – [target date]")
    lines.append("")

    lines.append("## Inputs used")
    lines.append("- Site cache: data/outputs/<client>/reports/site-cache/index.json")
    lines.append("- Inputs: data/outputs/<client>/inputs.md")
    lines.append("- Performance: live fetch timing (if available)")
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate technical SEO audit scaffold.")
    parser.add_argument("--client-slug", required=True, help="Client slug under data/outputs/")
    parser.add_argument(
        "--output",
        default=None,
        help="Optional output markdown path (default: data/outputs/<client>/reports/technical-seo-audit.md)",
    )
    args = parser.parse_args()

    base_dir = Path("data") / "outputs" / args.client_slug
    report_dir = base_dir / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    md_path = Path(args.output) if args.output else report_dir / "technical-seo-audit.md"
    json_path = report_dir / "technical-seo-audit.json"

    cache_index = load_cache_index(report_dir / "site-cache" / "index.json")
    website = load_inputs_website(base_dir / "inputs.md")
    if not website and cache_index:
        first_url = next(iter(cache_index.keys()))
        parsed = urlparse(first_url)
        website = f"{parsed.scheme}://{parsed.netloc}/"

    sections: list[AuditSection] = [
        AuditSection(name="Indexation"),
        AuditSection(name="Crawlability"),
        AuditSection(name="Performance (Core Web Vitals)"),
        AuditSection(name="Site architecture"),
        AuditSection(name="Structured data"),
        AuditSection(name="Mobile usability"),
        AuditSection(name="Security (HTTPS)"),
        AuditSection(name="Sitemaps and robots"),
        AuditSection(name="Redirects and errors"),
        AuditSection(name="Duplicate content"),
    ]
    metrics: dict[str, Any] = {}

    try:
        from bs4 import BeautifulSoup  # type: ignore
    except Exception:
        raise SystemExit("BeautifulSoup is required. Install beautifulsoup4 before running this audit.")

    pages = []
    titles: dict[str, list[str]] = {}
    descriptions: dict[str, list[str]] = {}
    canonicals: dict[str, list[str]] = {}
    schema_pages = 0
    viewport_missing = 0
    noindex_pages = 0
    http_pages = 0
    thin_pages = 0

    for url, meta in cache_index.items():
        path = meta.get("path")
        if not path:
            continue
        parsed = urlparse(url)
        if parsed.scheme != "https":
            http_pages += 1
        html = Path(path).read_text(encoding="utf-8", errors="ignore")
        soup = BeautifulSoup(html, "html.parser")
        title = soup.title.string.strip() if soup.title and soup.title.string else ""
        if title:
            titles.setdefault(title, []).append(url)
        desc_tag = soup.find("meta", attrs={"name": "description"})
        desc = desc_tag.get("content", "").strip() if desc_tag else ""
        if desc:
            descriptions.setdefault(desc, []).append(url)
        canonical_tag = soup.find("link", attrs={"rel": "canonical"})
        canonical = canonical_tag.get("href", "").strip() if canonical_tag else ""
        if canonical:
            canonicals.setdefault(canonical, []).append(url)
        robots_tag = soup.find("meta", attrs={"name": re.compile(r"robots", re.I)})
        if robots_tag and "noindex" in (robots_tag.get("content", "") or "").lower():
            noindex_pages += 1
        if not soup.find("meta", attrs={"name": "viewport"}):
            viewport_missing += 1
        schema_types = parse_schema_types(soup)
        if schema_types:
            schema_pages += 1
        text = extract_text(soup)
        if len(text.split()) < 200:
            thin_pages += 1
        pages.append(
            {
                "url": url,
                "title": title,
                "description": desc,
                "canonical": canonical,
                "schema_types": schema_types,
            }
        )

    metrics["cached_pages"] = len(pages)
    metrics["noindex_pages"] = noindex_pages
    metrics["missing_viewport"] = viewport_missing
    metrics["pages_with_schema"] = schema_pages
    metrics["thin_pages_under_200_words"] = thin_pages

    if noindex_pages:
        sections[0].findings.append(
            Finding(
                label="Noindex pages detected",
                detail=f"{noindex_pages} cached pages include noindex meta tags.",
                impact="Pages with noindex will not be eligible for organic visibility.",
                fix="Confirm noindex is intentional; remove from pages that should rank.",
            )
        )
    if thin_pages:
        sections[0].findings.append(
            Finding(
                label="Thin content pages",
                detail=f"{thin_pages} pages have fewer than ~200 words.",
                impact="Thin pages struggle to rank and may be seen as low value.",
                fix="Expand with service details, FAQs, and proof points.",
            )
        )

    duplicate_titles = {k: v for k, v in titles.items() if len(v) > 1}
    duplicate_descriptions = {k: v for k, v in descriptions.items() if len(v) > 1}
    if duplicate_titles:
        sections[9].findings.append(
            Finding(
                label="Duplicate title tags",
                detail=f"{len(duplicate_titles)} duplicate titles across cached pages.",
                impact="Duplicates reduce click-through and blur topical relevance.",
                fix="Write unique, service- and location-specific titles.",
            )
        )
    if duplicate_descriptions:
        sections[9].findings.append(
            Finding(
                label="Duplicate meta descriptions",
                detail=f"{len(duplicate_descriptions)} duplicate descriptions across cached pages.",
                impact="Duplicates reduce SERP differentiation.",
                fix="Tailor descriptions by service, location, and proof point.",
            )
        )

    if viewport_missing:
        sections[5].findings.append(
            Finding(
                label="Missing viewport meta tag",
                detail=f"{viewport_missing} pages lack a viewport meta tag.",
                impact="Pages may render poorly on mobile devices.",
                fix="Add <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">.",
            )
        )

    if schema_pages == 0:
        sections[4].findings.append(
            Finding(
                label="No structured data detected",
                detail="No JSON-LD found across cached pages.",
                impact="Search engines have less context on services and business details.",
                fix="Add LocalBusiness + Service schema for key pages.",
            )
        )

    if http_pages:
        sections[6].findings.append(
            Finding(
                label="Non-HTTPS URLs detected",
                detail=f"{http_pages} cached URLs use http://.",
                impact="Non-HTTPS pages can cause security warnings and ranking issues.",
                fix="Force HTTPS redirects and update internal links.",
            )
        )

    if canonicals:
        duplicate_canonicals = {k: v for k, v in canonicals.items() if len(v) > 1}
        if duplicate_canonicals:
            sections[9].findings.append(
                Finding(
                    label="Duplicate canonicals",
                    detail=f"{len(duplicate_canonicals)} canonicals point to the same URL.",
                    impact="Duplicate canonicals can collapse ranking signals.",
                    fix="Ensure each page self-canonicals unless intentionally consolidated.",
                )
            )

    if website:
        try:
            import requests  # type: ignore
        except Exception:
            requests = None
        if requests:
            robots_url = urljoin(website, "/robots.txt")
            sitemap_url = urljoin(website, "/sitemap.xml")
            robots_ok = False
            sitemap_ok = False
            response_time = None
            try:
                resp = requests.get(robots_url, timeout=15)
                robots_ok = resp.status_code == 200
            except Exception:
                robots_ok = False
            try:
                resp = requests.get(sitemap_url, timeout=15)
                sitemap_ok = resp.status_code == 200
            except Exception:
                sitemap_ok = False
            try:
                resp = requests.get(website, timeout=20)
                response_time = resp.elapsed.total_seconds()
            except Exception:
                response_time = None

            if not robots_ok:
                sections[7].findings.append(
                    Finding(
                        label="robots.txt missing or unreachable",
                        detail=f"{robots_url} did not return 200.",
                        impact="Crawlers may not have clear directives.",
                        fix="Ensure robots.txt is reachable and intentional.",
                    )
                )
            if not sitemap_ok:
                sections[7].findings.append(
                    Finding(
                        label="sitemap.xml missing or unreachable",
                        detail=f"{sitemap_url} did not return 200.",
                        impact="Discovery of pages may be slower or incomplete.",
                        fix="Publish a sitemap.xml and reference it in robots.txt.",
                    )
                )
            if response_time is not None:
                metrics["homepage_response_time_seconds"] = round(response_time, 2)
                if response_time > 2.5:
                    sections[2].findings.append(
                        Finding(
                            label="Slow homepage response time",
                            detail=f"Homepage response time {response_time:.2f}s.",
                            impact="Slow pages can impact rankings and conversions.",
                            fix="Optimize server response time, caching, and page weight.",
                        )
                    )

    payload = {
        "generated_at": now_iso(),
        "client": args.client_slug,
        "website": website,
        "metrics": metrics,
        "pages": pages,
        "sections": [
            {
                "name": section.name,
                "findings": [finding.__dict__ for finding in section.findings],
            }
            for section in sections
        ],
    }

    md_path.write_text(render_markdown(args.client_slug, website, sections, metrics), encoding="utf-8")
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print(f"wrote {md_path}")
    print(f"wrote {json_path}")


if __name__ == "__main__":
    main()
