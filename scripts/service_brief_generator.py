#!/usr/bin/env python3
"""Generate service briefs from cached site HTML snapshots.

Reads outputs/<client>/reports/site-cache/index.json and extracts
service page information without additional live requests.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse

from bs4 import BeautifulSoup


EXCLUDE_SLUGS = {
    "",
    "about",
    "contact",
    "pricing",
    "privacy-policy",
    "find-your-city",
    "all-services",
}

PRICE_RE = re.compile(r"\$\d+[\d,]*")
QUESTION_RE = re.compile(r"\?$|^(how|what|when|where|why|do|does|is|can|should|will|are)\b", re.I)


@dataclass
class ServiceBrief:
    url: str
    title: str
    meta_description: str
    h1: str
    value_props: list[str]
    pricing_mentions: list[str]
    faqs: list[tuple[str, str]]


def is_service_page(url: str) -> bool:
    slug = urlparse(url).path.strip("/")
    if not slug:
        return False
    if slug in EXCLUDE_SLUGS:
        return False
    if re.search(r"/blog|/category|/tag|/author|/page/", url):
        return False
    return True


def extract_meta(soup: BeautifulSoup) -> tuple[str, str]:
    title = soup.title.get_text(strip=True) if soup.title else ""
    meta_desc = ""
    desc_tag = soup.find("meta", attrs={"name": "description"})
    if desc_tag and desc_tag.get("content"):
        meta_desc = desc_tag["content"].strip()
    return title, meta_desc


def extract_value_props(soup: BeautifulSoup) -> list[str]:
    props: list[str] = []
    # collect first few substantive paragraphs
    for p in soup.find_all("p"):
        text = " ".join(p.stripped_strings)
        if len(text) < 40:
            continue
        props.append(text)
        if len(props) >= 4:
            break
    return props


def extract_pricing(text: str) -> list[str]:
    mentions = []
    for match in PRICE_RE.finditer(text):
        mentions.append(match.group(0))
    return list(dict.fromkeys(mentions))


def extract_faqs(soup: BeautifulSoup) -> list[tuple[str, str]]:
    faqs = []
    for el in soup.find_all(["h2", "h3", "h4", "button", "summary", "p", "div"]):
        q = " ".join(el.stripped_strings)
        if not q.endswith("?"):
            continue
        if len(q) < 6 or len(q) > 200:
            continue
        if not QUESTION_RE.search(q):
            continue
        ans = None
        sib = el.find_next_sibling()
        if sib:
            sib_text = " ".join(sib.stripped_strings)
            if sib_text and len(sib_text) > 10:
                ans = sib_text
        if not ans:
            parent = el.parent
            if parent:
                found = False
                for child in parent.find_all(recursive=False):
                    if child == el:
                        found = True
                        continue
                    if found:
                        ctext = " ".join(child.stripped_strings)
                        if ctext and len(ctext) > 10:
                            ans = ctext
                            break
        if ans:
            faqs.append((q.strip(), ans.strip()))
    # dedupe
    seen = set()
    deduped = []
    for q, a in faqs:
        key = q.lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append((q, a))
    return deduped


def parse_html(html: str, url: str) -> ServiceBrief:
    soup = BeautifulSoup(html, "html.parser")
    title, meta_desc = extract_meta(soup)
    h1 = ""
    h1_tag = soup.find("h1")
    if h1_tag:
        h1 = " ".join(h1_tag.stripped_strings)
    text = " ".join(soup.stripped_strings)
    pricing = extract_pricing(text)
    return ServiceBrief(
        url=url,
        title=title,
        meta_description=meta_desc,
        h1=h1,
        value_props=extract_value_props(soup),
        pricing_mentions=pricing,
        faqs=extract_faqs(soup),
    )


def load_cache(index_path: Path) -> dict[str, Path]:
    data = json.loads(index_path.read_text(encoding="utf-8"))
    return {url: Path(meta["path"]) for url, meta in data.items()}


def render_brief(brief: ServiceBrief) -> str:
    lines: list[str] = []
    lines.append(f"# Service Brief: {brief.h1 or brief.title}")
    lines.append("")
    lines.append(f"- Source URL: {brief.url}")
    if brief.title:
        lines.append(f"- Page title: {brief.title}")
    if brief.meta_description:
        lines.append(f"- Meta description: {brief.meta_description}")
    if brief.pricing_mentions:
        lines.append(f"- Pricing mentions: {', '.join(brief.pricing_mentions)}")
    lines.append("")
    lines.append("## Value props (extracted)")
    for prop in brief.value_props:
        lines.append(f"- {prop}")
    if not brief.value_props:
        lines.append("- [No paragraphs extracted]")
    lines.append("")
    lines.append("## FAQs (extracted)")
    if brief.faqs:
        for q, a in brief.faqs:
            lines.append(f"- Q: {q}")
            lines.append(f"  A: {a}")
    else:
        lines.append("- [No FAQs detected]")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate service briefs from cache.")
    parser.add_argument("--client-slug", required=True, help="Client slug under outputs/")
    args = parser.parse_args()

    cache_dir = Path("outputs") / args.client_slug / "reports" / "site-cache"
    index_path = cache_dir / "index.json"
    if not index_path.exists():
        raise SystemExit(f"Cache index not found: {index_path}")

    cache = load_cache(index_path)
    out_dir = Path("outputs") / args.client_slug / "reports" / "service-briefs"
    out_dir.mkdir(parents=True, exist_ok=True)

    for url, path in cache.items():
        if not is_service_page(url):
            continue
        html = path.read_text(encoding="utf-8")
        brief = parse_html(html, url)
        slug = urlparse(url).path.strip("/")
        out_path = out_dir / f"{slug}.md"
        out_path.write_text(render_brief(brief), encoding="utf-8")
        print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
