#!/usr/bin/env python3
"""Generate service briefs from cached site HTML snapshots.

Reads data/outputs/<client>/reports/site-cache/index.json and extracts
service page information without additional live requests.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin, urlparse

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
CTA_RE = re.compile(r"\b(call|contact|schedule|book|request|quote|estimate|get started)\b", re.I)


@dataclass
class ServiceBrief:
    url: str
    title: str
    meta_description: str
    h1: str
    canonical_url: str
    og_title: str
    og_description: str
    og_image: str
    twitter_title: str
    twitter_description: str
    twitter_image: str
    headings: list[str]
    value_props: list[str]
    proof_points: list[str]
    pricing_mentions: list[str]
    ctas: list[str]
    cta_links: list[str]
    internal_links: list[str]
    schema_types: list[str]
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


def extract_canonical(soup: BeautifulSoup) -> str:
    link = soup.find("link", rel="canonical")
    if link and link.get("href"):
        return link["href"].strip()
    return ""


def extract_open_graph(soup: BeautifulSoup) -> tuple[str, str, str]:
    og_title = ""
    og_desc = ""
    og_image = ""
    for tag in soup.find_all("meta"):
        prop = tag.get("property")
        content = tag.get("content", "").strip()
        if not prop or not content:
            continue
        if prop == "og:title":
            og_title = content
        elif prop == "og:description":
            og_desc = content
        elif prop == "og:image":
            og_image = content
    return og_title, og_desc, og_image


def extract_twitter(soup: BeautifulSoup) -> tuple[str, str, str]:
    tw_title = ""
    tw_desc = ""
    tw_image = ""
    for tag in soup.find_all("meta"):
        name = tag.get("name")
        content = tag.get("content", "").strip()
        if not name or not content:
            continue
        if name == "twitter:title":
            tw_title = content
        elif name == "twitter:description":
            tw_desc = content
        elif name == "twitter:image":
            tw_image = content
    return tw_title, tw_desc, tw_image


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


def extract_headings(soup: BeautifulSoup) -> list[str]:
    headings: list[str] = []
    for tag in soup.find_all(["h2", "h3"]):
        text = " ".join(tag.stripped_strings)
        if not text:
            continue
        if text in headings:
            continue
        headings.append(text)
        if len(headings) >= 12:
            break
    return headings


def extract_proof_points(soup: BeautifulSoup) -> list[str]:
    points: list[str] = []
    for li in soup.find_all("li"):
        text = " ".join(li.stripped_strings)
        if len(text) < 20:
            continue
        points.append(text)
        if len(points) >= 6:
            break
    return points


def extract_pricing(text: str) -> list[str]:
    mentions = []
    for match in PRICE_RE.finditer(text):
        mentions.append(match.group(0))
    return list(dict.fromkeys(mentions))


def extract_ctas(soup: BeautifulSoup) -> list[str]:
    ctas: list[str] = []
    for el in soup.find_all(["a", "button"]):
        text = " ".join(el.stripped_strings)
        if not text:
            continue
        if not CTA_RE.search(text):
            continue
        if text in ctas:
            continue
        ctas.append(text)
        if len(ctas) >= 6:
            break
    return ctas


def extract_cta_links(soup: BeautifulSoup, base_url: str) -> list[str]:
    links: list[str] = []
    for el in soup.find_all(["a", "button"]):
        text = " ".join(el.stripped_strings)
        if not text or not CTA_RE.search(text):
            continue
        href = ""
        if el.name == "a":
            href = el.get("href", "").strip()
        if href:
            full = urljoin(base_url, href)
            links.append(f"{text} -> {full}")
        else:
            links.append(f"{text} -> [no link]")
        if len(links) >= 8:
            break
    return links


def extract_internal_links(soup: BeautifulSoup, base_url: str) -> list[str]:
    links: list[str] = []
    base = urlparse(base_url)
    for a in soup.find_all("a", href=True):
        href = a.get("href", "").strip()
        if not href:
            continue
        if href.startswith("#") or href.startswith("mailto:") or href.startswith("tel:"):
            continue
        full = urljoin(base_url, href)
        parsed = urlparse(full)
        if parsed.netloc and parsed.netloc != base.netloc:
            continue
        normalized = parsed._replace(fragment="").geturl()
        if normalized in links:
            continue
        links.append(normalized)
        if len(links) >= 12:
            break
    return links


def extract_schema_types(soup: BeautifulSoup) -> list[str]:
    types: list[str] = []
    for script in soup.find_all("script", type=re.compile("ld\\+json", re.I)):
        raw = script.string or ""
        if not raw.strip():
            continue
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue
        candidates: list[dict] = []
        if isinstance(data, dict):
            candidates.append(data)
        elif isinstance(data, list):
            candidates.extend([item for item in data if isinstance(item, dict)])
        for item in candidates:
            schema_type = item.get("@type")
            if not schema_type:
                continue
            if isinstance(schema_type, list):
                for entry in schema_type:
                    if isinstance(entry, str) and entry not in types:
                        types.append(entry)
            elif isinstance(schema_type, str) and schema_type not in types:
                types.append(schema_type)
    return types


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
    canonical_url = extract_canonical(soup)
    og_title, og_desc, og_image = extract_open_graph(soup)
    tw_title, tw_desc, tw_image = extract_twitter(soup)
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
        canonical_url=canonical_url,
        og_title=og_title,
        og_description=og_desc,
        og_image=og_image,
        twitter_title=tw_title,
        twitter_description=tw_desc,
        twitter_image=tw_image,
        headings=extract_headings(soup),
        value_props=extract_value_props(soup),
        proof_points=extract_proof_points(soup),
        pricing_mentions=pricing,
        ctas=extract_ctas(soup),
        cta_links=extract_cta_links(soup, url),
        internal_links=extract_internal_links(soup, url),
        schema_types=extract_schema_types(soup),
        faqs=extract_faqs(soup),
    )


def load_cache(index_path: Path) -> dict[str, Path]:
    data = json.loads(index_path.read_text(encoding="utf-8"))
    return {url: Path(meta["path"]) for url, meta in data.items()}


def render_brief(brief: ServiceBrief) -> str:
    lines: list[str] = []
    lines.append(f"# Service Brief: {brief.h1 or brief.title}")
    lines.append("")
    lines.append("## Source")
    lines.append(f"- URL: {brief.url}")
    if brief.title:
        lines.append(f"- Page title: {brief.title}")
    if brief.meta_description:
        lines.append(f"- Meta description: {brief.meta_description}")
    if brief.canonical_url:
        lines.append(f"- Canonical: {brief.canonical_url}")
    if brief.og_title:
        lines.append(f"- Open Graph title: {brief.og_title}")
    if brief.og_description:
        lines.append(f"- Open Graph description: {brief.og_description}")
    if brief.og_image:
        lines.append(f"- Open Graph image: {brief.og_image}")
    if brief.twitter_title:
        lines.append(f"- Twitter title: {brief.twitter_title}")
    if brief.twitter_description:
        lines.append(f"- Twitter description: {brief.twitter_description}")
    if brief.twitter_image:
        lines.append(f"- Twitter image: {brief.twitter_image}")
    if brief.h1:
        lines.append(f"- H1: {brief.h1}")
    if brief.pricing_mentions:
        lines.append(f"- Pricing mentions: {', '.join(brief.pricing_mentions)}")
    lines.append("")
    lines.append("## Page structure")
    if brief.headings:
        lines.append(f"- H2/H3 headings: {', '.join(brief.headings)}")
    else:
        lines.append("- H2/H3 headings: [None detected]")
    lines.append("")
    lines.append("## Signals")
    lines.append("### Value props (extracted)")
    for prop in brief.value_props:
        lines.append(f"- {prop}")
    if not brief.value_props:
        lines.append("- [No paragraphs extracted]")
    lines.append("")
    lines.append("### Proof points (extracted)")
    for point in brief.proof_points:
        lines.append(f"- {point}")
    if not brief.proof_points:
        lines.append("- [No proof points detected]")
    lines.append("")
    lines.append("### CTAs (extracted)")
    for cta in brief.ctas:
        lines.append(f"- {cta}")
    if not brief.ctas:
        lines.append("- [No CTA text detected]")
    lines.append("")
    lines.append("### CTA links (extracted)")
    for link in brief.cta_links:
        lines.append(f"- {link}")
    if not brief.cta_links:
        lines.append("- [No CTA links detected]")
    lines.append("")
    lines.append("## Internal links (sampled)")
    for link in brief.internal_links:
        lines.append(f"- {link}")
    if not brief.internal_links:
        lines.append("- [No internal links detected]")
    lines.append("")
    lines.append("## Schema types (detected)")
    for schema_type in brief.schema_types:
        lines.append(f"- {schema_type}")
    if not brief.schema_types:
        lines.append("- [No schema types detected]")
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
    parser.add_argument("--client-slug", required=True, help="Client slug under data/outputs/")
    args = parser.parse_args()

    cache_dir = Path("data") / "outputs" / args.client_slug / "reports" / "site-cache"
    index_path = cache_dir / "index.json"
    if not index_path.exists():
        raise SystemExit(f"Cache index not found: {index_path}")

    cache = load_cache(index_path)
    out_dir = Path("data") / "outputs" / args.client_slug / "reports" / "service-briefs"
    out_dir.mkdir(parents=True, exist_ok=True)

    for url, path in cache.items():
        if not is_service_page(url):
            continue
        html = path.read_text(encoding="utf-8")
        brief = parse_html(html, url)
        slug = urlparse(url).path.strip("/")
        if not slug:
            slug = "index"
        out_path = out_dir / f"{slug}.md"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(render_brief(brief), encoding="utf-8")
        print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
