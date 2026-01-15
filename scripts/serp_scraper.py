#!/usr/bin/env python3
"""
Direct Google SERP scraper using SeleniumBase.

Notes:
- Intended for light, low-volume checks to avoid abuse.
- May be blocked by Google; handle captchas manually if needed.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import random
import re
import time
from pathlib import Path
from typing import Iterable
from urllib.parse import quote_plus, urlparse

from seleniumbase import SB


def _split_terms(raw: str) -> list[str]:
    parts = re.split(r"[,;]", raw)
    return [p.strip() for p in parts if p.strip()]


def _extract_inline_value(line: str) -> str:
    return line.split(":", 1)[1].strip() if ":" in line else ""


def parse_inputs(path: Path) -> dict[str, object]:
    data: dict[str, object] = {
        "business_name": "",
        "website": "",
        "areas": [],
        "keywords": [],
        "branded_keywords": [],
    }

    lines = path.read_text(encoding="utf-8").splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("- Business name:"):
            data["business_name"] = _extract_inline_value(line)
        if line.startswith("- Website:"):
            data["website"] = _extract_inline_value(line)
        if line.startswith("- Areas served"):
            areas: list[str] = []
            i += 1
            while i < len(lines):
                nxt = lines[i]
                if nxt.startswith("  - "):
                    areas.append(nxt.replace("  - ", "", 1).strip())
                    i += 1
                    continue
                if nxt.strip() == "":
                    i += 1
                    continue
                if nxt.strip().startswith("##") or nxt.strip().startswith("- "):
                    break
                i += 1
            data["areas"] = areas
            continue
        if line.startswith("- Keywords (approved list):"):
            data["keywords"] = _split_terms(_extract_inline_value(line))
        if line.startswith("- Branded keywords:"):
            data["branded_keywords"] = _split_terms(_extract_inline_value(line))
        i += 1

    return data


def normalize_domain(url: str) -> str:
    try:
        host = urlparse(url).netloc.lower()
    except Exception:
        return ""
    return host.replace("www.", "")


def iter_queries(keywords: Iterable[str], areas: Iterable[str]) -> list[str]:
    queries = []
    for kw in keywords:
        for area in areas:
            queries.append(f"{kw} {area}")
    return queries


def maybe_accept_cookies(sb: SB) -> None:
    candidates = [
        "button:contains('I agree')",
        "button:contains('Accept all')",
        "button:contains('Accept all cookies')",
        "button:contains('Accept')",
    ]
    for sel in candidates:
        try:
            sb.click(sel, timeout=2)
            return
        except Exception:
            continue


def scrape_query(sb: SB, query: str, max_results: int, timeout: int) -> list[dict[str, str]]:
    url = f"https://www.google.com/search?q={quote_plus(query)}"
    sb.driver.set_page_load_timeout(timeout)
    sb.open(url)
    time.sleep(1.5)
    maybe_accept_cookies(sb)
    time.sleep(1.0)

    results = []
    cards = sb.find_elements("css selector", "div.g")
    for card in cards:
        try:
            link_el = card.find_element("css selector", "a")
            title_el = card.find_element("css selector", "h3")
        except Exception:
            continue
        href = link_el.get_attribute("href")
        title = title_el.text.strip()
        if not href or not title:
            continue
        results.append({"title": title, "url": href})
        if len(results) >= max_results:
            break

    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape Google SERPs for local keywords.")
    parser.add_argument("--client-slug", required=True, help="Output folder slug (e.g., highpoint)")
    parser.add_argument("--base-dir", default="outputs", help="Base output directory (default: outputs)")
    parser.add_argument("--limit-cities", type=int, default=5, help="Limit number of cities/areas")
    parser.add_argument("--limit-keywords", type=int, default=5, help="Limit number of keywords")
    parser.add_argument("--max-results", type=int, default=10, help="Max results per query")
    parser.add_argument("--timeout", type=int, default=30, help="Page load timeout in seconds")
    parser.add_argument("--sleep-min", type=float, default=2.0, help="Minimum sleep between queries")
    parser.add_argument("--sleep-max", type=float, default=4.0, help="Maximum sleep between queries")
    parser.add_argument("--headless", action="store_true", help="Run browser headless")
    args = parser.parse_args()

    inputs_path = Path(args.base_dir) / args.client_slug / "inputs.md"
    if not inputs_path.exists():
        raise SystemExit(f"inputs.md not found at {inputs_path}")

    inputs = parse_inputs(inputs_path)
    business_name = inputs.get("business_name") or args.client_slug
    website = inputs.get("website") or ""
    client_domain = normalize_domain(website)

    areas = (inputs.get("areas") or [])[: args.limit_cities]
    keywords = (inputs.get("keywords") or [])[: args.limit_keywords]
    if not areas or not keywords:
        raise SystemExit("Missing areas or keywords in inputs.md")

    timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M")
    reports_dir = Path(args.base_dir) / args.client_slug / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    csv_path = reports_dir / f"serp-snapshot-{timestamp}.csv"
    json_path = reports_dir / f"serp-summary-{timestamp}.json"

    query_list = iter_queries(keywords, areas)

    rows = []
    errors: list[dict[str, str]] = []
    competitor_counts: dict[str, int] = {}
    client_ranks: list[dict[str, object]] = []

    with SB(headless=args.headless) as sb:
        for idx, query in enumerate(query_list, start=1):
            print(f"[{idx}/{len(query_list)}] {query}")
            time.sleep(random.uniform(args.sleep_min, args.sleep_max))
            try:
                results = scrape_query(sb, query, args.max_results, args.timeout)
            except Exception as exc:
                errors.append({"query": query, "error": str(exc)})
                continue
            client_rank = None
            for idx, result in enumerate(results, start=1):
                domain = normalize_domain(result["url"])
                if domain:
                    competitor_counts[domain] = competitor_counts.get(domain, 0) + 1
                if client_domain and domain == client_domain and client_rank is None:
                    client_rank = idx
                rows.append(
                    {
                        "query": query,
                        "rank": idx,
                        "title": result["title"],
                        "url": result["url"],
                        "domain": domain,
                    }
                )
            client_ranks.append({"query": query, "rank": client_rank})

    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["query", "rank", "title", "url", "domain"])
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "client": business_name,
        "website": website,
        "client_domain": client_domain,
        "areas": areas,
        "keywords": keywords,
        "queries": len(query_list),
        "max_results": args.max_results,
        "client_ranks": client_ranks,
        "errors": errors,
        "competitor_counts": dict(
            sorted(competitor_counts.items(), key=lambda kv: kv[1], reverse=True)
        ),
        "csv": str(csv_path),
        "timestamp": timestamp,
    }
    json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"Wrote {csv_path}")
    print(f"Wrote {json_path}")


if __name__ == "__main__":
    main()
