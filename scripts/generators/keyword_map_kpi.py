#!/usr/bin/env python3
"""Generate keyword map and KPI targets report from approved inputs."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlparse


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


def load_client_from_inputs(path: Path, slug: str) -> dict[str, str]:
    client = {"name": slug, "website": ""}
    if not path.exists():
        return client
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("- Business name:"):
            client["name"] = line.split(":", 1)[1].strip() or client["name"]
        elif line.startswith("- Website:"):
            client["website"] = line.split(":", 1)[1].strip()
    return client


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


def load_inputs_services(path: Path) -> tuple[list[str], dict[str, str]]:
    if not path.exists():
        return [], {}
    lines = [line.rstrip("\n") for line in path.read_text(encoding="utf-8").splitlines()]
    services: list[str] = []
    service_urls: dict[str, str] = {}
    in_services = False
    for line in lines:
        if line.startswith("## Approved service list"):
            in_services = True
            continue
        if line.startswith("## ") and in_services:
            in_services = False
        if in_services and line.startswith("- "):
            entry = line.replace("- ", "", 1).strip()
            if not entry:
                continue
            name, _, rest = entry.partition(":")
            name = name.strip()
            url_match = re.search(r"\((https?://[^)]+)\)", rest)
            url = url_match.group(1) if url_match else ""
            if name:
                services.append(name)
            if url:
                service_urls[name] = url
    return services, service_urls


def load_site_cache_index(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return {url: meta.get("path", "") for url, meta in data.items() if isinstance(meta, dict)}


def normalize_phrase(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip())


def iter_ranked_phrases(phrases: Iterable[tuple[float, str]]) -> list[tuple[float, str]]:
    out: list[tuple[float, str]] = []
    for score, phrase in phrases:
        phrase = normalize_phrase(phrase)
        if not phrase:
            continue
        words = phrase.split()
        if len(words) < 2 or len(words) > 6:
            continue
        out.append((score, phrase))
    return out


def generate_keywords_from_cache(
    cache_index: dict[str, str],
    service_urls: dict[str, str],
    max_per_page: int,
) -> list[KeywordEntry]:
    try:
        from bs4 import BeautifulSoup  # type: ignore
    except Exception as exc:
        raise SystemExit("BeautifulSoup is required. Install beautifulsoup4 before running --auto-from-cache.") from exc
    try:
        from rake_nltk import Rake  # type: ignore
    except Exception as exc:
        raise SystemExit("rake_nltk is required. Install rake_nltk before running --auto-from-cache.") from exc
    try:
        import textstat  # type: ignore
    except Exception as exc:
        raise SystemExit("textstat is required. Install textstat before running --auto-from-cache.") from exc

    entries: list[KeywordEntry] = []
    seen: set[str] = set()
    rake = Rake()

    for service, url in service_urls.items():
        cache_path = cache_index.get(url)
        if not cache_path:
            continue
        html = Path(cache_path).read_text(encoding="utf-8", errors="ignore")
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
        text = " ".join(soup.stripped_strings)
        if not text:
            continue
        rake.extract_keywords_from_text(text)
        ranked = iter_ranked_phrases(rake.get_ranked_phrases_with_scores())
        scored: list[tuple[float, str]] = []
        for score, phrase in ranked:
            lexicon = textstat.lexicon_count(phrase) or 1
            adjusted = score * (1.0 + min(0.5, lexicon / 10))
            scored.append((adjusted, phrase))
        scored.sort(key=lambda item: item[0], reverse=True)

        slug = urlparse(url).path
        picked = 0
        for _, phrase in scored:
            key = phrase.lower()
            if key in seen:
                continue
            seen.add(key)
            priority = "primary" if picked == 0 else "secondary"
            entries.append(
                KeywordEntry(
                    keyword=phrase,
                    target_url=slug,
                    intent="service",
                    priority=priority,
                    service=service,
                )
            )
            picked += 1
            if picked >= max_per_page:
                break
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
    parser.add_argument(
        "--auto-from-cache",
        action="store_true",
        help="Extract keywords from cached HTML using RAKE + textstat.",
    )
    parser.add_argument(
        "--max-per-page",
        type=int,
        default=6,
        help="Max keywords per service page when auto-extracting (default: 6).",
    )
    args = parser.parse_args()

    base_dir = Path("data") / "outputs" / args.client_slug
    report_dir = base_dir / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    input_path = Path(args.input) if args.input else report_dir / "keyword-map-input.json"
    data: dict[str, Any] = {}
    if input_path.exists():
        data = load_input(input_path)
    elif args.scaffold and not args.auto_from_cache:
        scaffold_input(input_path)
        print(f"wrote scaffold input to {input_path}")
        return
    elif not args.auto_from_cache:
        raise SystemExit(f"Input file not found: {input_path}. Use --scaffold to create one.")

    client = data.get("client", {}) if data else load_client_from_inputs(base_dir / "inputs.md", args.client_slug)
    kpis = data.get("kpi_targets", {}) if data else {}

    keyword_items = data.get("keywords", []) if data else []
    keywords: list[KeywordEntry]
    if args.auto_from_cache:
        inputs_path = base_dir / "inputs.md"
        services, service_urls = load_inputs_services(inputs_path)
        cache_index = load_site_cache_index(base_dir / "reports" / "site-cache" / "index.json")
        keywords = generate_keywords_from_cache(cache_index, service_urls, args.max_per_page)
        if not keywords and isinstance(keyword_items, list):
            keywords = parse_keywords(keyword_items)
    else:
        keywords = parse_keywords(keyword_items or [])

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
