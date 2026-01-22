#!/usr/bin/env python3
"""Audit FAQs across a site.

- Crawls sitemap(s) if available, else falls back to homepage link discovery.
- Detects FAQ content from JSON-LD FAQPage and from visible HTML FAQ patterns.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


FAQ_TEXT_RE = re.compile(r"faq|frequently asked questions", re.I)
QUESTION_RE = re.compile(r"\?$|^(how|what|when|where|why|do|does|is|can|should|will|are)\b", re.I)


@dataclass
class PageFaqResult:
    url: str
    html_questions: list[str]
    jsonld_questions: list[str]


def normalize_url(url: str) -> str:
    parsed = urlparse(url)
    return parsed._replace(fragment="").geturl()


def fetch_sitemaps(base: str, timeout: int) -> list[str]:
    candidates = ["/sitemap.xml", "/sitemap_index.xml"]
    urls = set()

    for path in candidates:
        url = urljoin(base, path)
        try:
            resp = requests.get(url, timeout=timeout)
            if resp.status_code != 200:
                continue
            soup = BeautifulSoup(resp.text, "xml")
            if soup.find("sitemapindex"):
                for loc in soup.find_all("loc"):
                    sub_url = loc.get_text(strip=True)
                    try:
                        sub_resp = requests.get(sub_url, timeout=timeout)
                        if sub_resp.status_code == 200:
                            subsoup = BeautifulSoup(sub_resp.text, "xml")
                            for subloc in subsoup.find_all("loc"):
                                urls.add(subloc.get_text(strip=True))
                    except Exception:
                        continue
            else:
                for loc in soup.find_all("loc"):
                    urls.add(loc.get_text(strip=True))
        except Exception:
            continue

    return sorted({normalize_url(u) for u in urls if u.startswith(base)})


def discover_from_home(base: str, timeout: int) -> list[str]:
    resp = requests.get(base, timeout=timeout)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    urls = set()
    for a in soup.select("a[href]"):
        href = a.get("href")
        if not href:
            continue
        if href.startswith("/"):
            urls.add(urljoin(base, href))
        elif href.startswith(base):
            urls.add(href)
    return sorted({normalize_url(u) for u in urls})


def extract_jsonld_faqs(soup: BeautifulSoup) -> list[str]:
    questions = []
    for script in soup.find_all("script", type=re.compile("ld\+json", re.I)):
        raw = script.string or script.get_text()
        if not raw:
            continue
        try:
            data = json.loads(raw)
        except Exception:
            continue

        nodes = data if isinstance(data, list) else [data]
        for node in nodes:
            if isinstance(node, dict) and node.get("@type") == "FAQPage":
                for item in node.get("mainEntity", []) or []:
                    q = item.get("name")
                    if q:
                        questions.append(q.strip())
            if isinstance(node, dict) and node.get("@graph"):
                for graph_node in node.get("@graph"):
                    if graph_node.get("@type") == "FAQPage":
                        for item in graph_node.get("mainEntity", []) or []:
                            q = item.get("name")
                            if q:
                                questions.append(q.strip())
    return questions


def extract_html_faqs(soup: BeautifulSoup) -> list[str]:
    # Look for headings or list items near FAQ sections.
    questions = []

    # Identify a FAQ container if possible.
    faq_sections = []
    for el in soup.find_all(["section", "div"]):
        text = " ".join(el.stripped_strings)
        if FAQ_TEXT_RE.search(text):
            faq_sections.append(el)

    search_scopes = faq_sections if faq_sections else [soup]

    for scope in search_scopes:
        for el in scope.find_all(["h2", "h3", "h4", "p", "li", "button", "summary"]):
            text = " ".join(el.stripped_strings)
            if not text:
                continue
            if len(text) < 6 or len(text) > 180:
                continue
            if QUESTION_RE.search(text) and text.strip().endswith("?"):
                questions.append(text.strip())

    # De-dup preserve order
    seen = set()
    deduped = []
    for q in questions:
        if q.lower() in seen:
            continue
        seen.add(q.lower())
        deduped.append(q)
    return deduped


def audit_page(url: str, timeout: int) -> PageFaqResult:
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    return PageFaqResult(
        url=url,
        html_questions=extract_html_faqs(soup),
        jsonld_questions=extract_jsonld_faqs(soup),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit site FAQs across all pages.")
    parser.add_argument("--base", required=True, help="Base site URL, e.g. https://example.com")
    parser.add_argument("--timeout", type=int, default=25, help="Request timeout (seconds)")
    parser.add_argument("--include-blog", action="store_true", help="Include blog pages")
    parser.add_argument("--output", required=True, help="Output JSON file path")
    args = parser.parse_args()

    base = args.base.rstrip("/")
    urls = fetch_sitemaps(base, args.timeout)
    if not urls:
        urls = discover_from_home(base, args.timeout)

    if not args.include_blog:
        urls = [u for u in urls if not re.search(r"/blog|/category|/tag|/author|/page/", u)]

    results = []
    for idx, url in enumerate(urls, start=1):
        print(f"[{idx}/{len(urls)}] {url}")
        try:
            result = audit_page(url, args.timeout)
            results.append(result)
        except Exception as exc:
            results.append(PageFaqResult(url=url, html_questions=[f"ERROR: {exc}"], jsonld_questions=[]))

    payload = {
        "base": base,
        "include_blog": args.include_blog,
        "total_pages": len(urls),
        "pages": [
            {
                "url": r.url,
                "html_faq_count": len([q for q in r.html_questions if not q.startswith("ERROR:")]),
                "jsonld_faq_count": len(r.jsonld_questions),
                "html_questions": r.html_questions,
                "jsonld_questions": r.jsonld_questions,
            }
            for r in results
        ],
    }

    with open(args.output, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)


if __name__ == "__main__":
    main()
