#!/usr/bin/env python3
"""Generate JSON-LD schema scripts from cached HTML pages.

Reads outputs/<client>/reports/site-cache/index.json and writes one JSON-LD
<script> tag per page under outputs/<client>/gen-schema/website-tree/.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup


FAQ_QUESTION_RE = re.compile(r"\?$|^(how|what|when|where|why|do|does|is|can|should|will|are)\b", re.I)


@dataclass
class PageSignals:
    url: str
    canonical_url: str
    title: str
    h1: str
    meta_description: str
    og_title: str
    og_description: str
    og_image: str
    og_type: str
    twitter_title: str
    twitter_description: str
    twitter_image: str
    site_name: str
    lang: str
    published_time: str
    modified_time: str
    faqs: list[tuple[str, str]]


def load_cache(index_path: Path) -> dict[str, Path]:
    data = json.loads(index_path.read_text(encoding="utf-8"))
    return {url: Path(meta["path"]) for url, meta in data.items()}


def normalize_title(text: str) -> str:
    return " ".join(text.split()).strip()


def dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        if not value:
            continue
        key = value.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(value)
    return out


def extract_meta_values(soup: BeautifulSoup) -> dict[str, str]:
    values: dict[str, str] = {}
    for tag in soup.find_all("meta"):
        content = tag.get("content", "").strip()
        if not content:
            continue
        prop = tag.get("property")
        name = tag.get("name")
        if prop and prop not in values:
            values[prop] = content
        if name and name not in values:
            values[name] = content
    return values


def extract_canonical(soup: BeautifulSoup) -> str:
    link = soup.find("link", rel="canonical")
    if link and link.get("href"):
        return link["href"].strip()
    return ""


def extract_h1(soup: BeautifulSoup) -> str:
    h1_tag = soup.find("h1")
    if h1_tag:
        return " ".join(h1_tag.stripped_strings)
    return ""


def extract_faqs(soup: BeautifulSoup) -> list[tuple[str, str]]:
    faqs: list[tuple[str, str]] = []
    for el in soup.find_all(["h2", "h3", "h4", "button", "summary", "p", "div"]):
        question = " ".join(el.stripped_strings)
        if not question.endswith("?"):
            continue
        if len(question) < 6 or len(question) > 200:
            continue
        if not FAQ_QUESTION_RE.search(question):
            continue
        answer = None
        sibling = el.find_next_sibling()
        if sibling:
            sib_text = " ".join(sibling.stripped_strings)
            if sib_text and len(sib_text) > 10:
                answer = sib_text
        if not answer:
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
                            answer = ctext
                            break
        if answer:
            faqs.append((question.strip(), answer.strip()))
    seen = set()
    deduped = []
    for question, answer in faqs:
        key = question.lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append((question, answer))
    return deduped


def parse_page(html: str, url: str) -> PageSignals:
    soup = BeautifulSoup(html, "html.parser")
    title = normalize_title(soup.title.get_text()) if soup.title else ""
    h1 = normalize_title(extract_h1(soup))
    meta_values = extract_meta_values(soup)
    meta_description = meta_values.get("description", "")
    og_title = meta_values.get("og:title", "")
    og_description = meta_values.get("og:description", "")
    og_image = meta_values.get("og:image", "")
    og_type = meta_values.get("og:type", "")
    twitter_title = meta_values.get("twitter:title", "")
    twitter_description = meta_values.get("twitter:description", "")
    twitter_image = meta_values.get("twitter:image", "")
    site_name = meta_values.get("og:site_name", "")
    lang = soup.html.get("lang", "").strip() if soup.html else ""
    published_time = meta_values.get("article:published_time", "")
    modified_time = meta_values.get("article:modified_time", "") or meta_values.get("og:updated_time", "")
    canonical_url = extract_canonical(soup)
    return PageSignals(
        url=url,
        canonical_url=canonical_url,
        title=title,
        h1=h1,
        meta_description=meta_description,
        og_title=og_title,
        og_description=og_description,
        og_image=og_image,
        og_type=og_type,
        twitter_title=twitter_title,
        twitter_description=twitter_description,
        twitter_image=twitter_image,
        site_name=site_name,
        lang=lang,
        published_time=published_time,
        modified_time=modified_time,
        faqs=extract_faqs(soup),
    )


def build_breadcrumbs(page_url: str) -> list[dict[str, Any]]:
    parsed = urlparse(page_url)
    base = f"{parsed.scheme}://{parsed.netloc}/"
    segments = [seg for seg in parsed.path.split("/") if seg]
    items: list[dict[str, Any]] = []
    position = 1
    items.append(
        {
            "@type": "ListItem",
            "position": position,
            "name": "Home",
            "item": base,
        }
    )
    position += 1
    current = base
    for seg in segments:
        current = urljoin(current, f"{seg}/")
        name = seg.replace("-", " ").replace("_", " ").title()
        items.append(
            {
                "@type": "ListItem",
                "position": position,
                "name": name,
                "item": current,
            }
        )
        position += 1
    return items


def prune_empty(value: Any) -> Any:
    if isinstance(value, dict):
        cleaned = {k: prune_empty(v) for k, v in value.items()}
        return {k: v for k, v in cleaned.items() if v not in ("", None, [], {})}
    if isinstance(value, list):
        cleaned_list = [prune_empty(item) for item in value]
        return [item for item in cleaned_list if item not in ("", None, [], {})]
    return value


def ensure_absolute(url: str, base_url: str) -> str:
    if not url:
        return ""
    return urljoin(base_url, url)


def choose_titles(signals: PageSignals) -> tuple[str, list[str]]:
    candidates = dedupe(
        [
            signals.title,
            signals.h1,
            signals.og_title,
            signals.twitter_title,
        ]
    )
    if not candidates:
        fallback = urlparse(signals.url).path.strip("/") or "Homepage"
        return fallback.replace("-", " ").title(), []
    primary = candidates[0]
    alternates = candidates[1:]
    return primary, alternates


def generate_schema(signals: PageSignals) -> dict[str, Any]:
    raw_url = signals.canonical_url or signals.url
    parsed = urlparse(raw_url)
    page_url = parsed._replace(query="", fragment="").geturl()
    site_url = f"{parsed.scheme}://{parsed.netloc}/"
    page_id = page_url.rstrip("/") or page_url
    webpage_id = f"{page_id}#webpage"
    website_id = f"{site_url}#website"
    org_id = f"{site_url}#organization"
    primary_title, alternate_titles = choose_titles(signals)
    description = signals.meta_description or signals.og_description or signals.twitter_description
    image_url = ensure_absolute(signals.og_image or signals.twitter_image, page_url)
    image_id = f"{page_id}#primaryimage" if image_url else ""
    breadcrumbs = build_breadcrumbs(page_url)
    breadcrumb_id = f"{page_id}#breadcrumb"

    graph: list[dict[str, Any]] = []

    site_name = signals.site_name or primary_title
    site_alternates = dedupe(
        [primary_title] if signals.site_name and primary_title != signals.site_name else []
    )

    website = {
        "@type": "WebSite",
        "@id": website_id,
        "url": site_url,
        "name": site_name,
        "alternateName": site_alternates if site_alternates else None,
    }
    graph.append(website)

    if site_name:
        organization = {
            "@type": "Organization",
            "@id": org_id,
            "name": site_name,
            "url": site_url,
        }
        graph.append(organization)

    if image_url:
        graph.append(
            {
                "@type": "ImageObject",
                "@id": image_id,
                "url": image_url,
                "contentUrl": image_url,
                "caption": primary_title,
            }
        )

    graph.append(
        {
            "@type": "BreadcrumbList",
            "@id": breadcrumb_id,
            "itemListElement": breadcrumbs,
        }
    )

    webpage = {
        "@type": "WebPage",
        "@id": webpage_id,
        "url": page_url,
        "name": primary_title,
        "alternateName": alternate_titles if alternate_titles else None,
        "description": description,
        "inLanguage": signals.lang or None,
        "isPartOf": {"@id": website_id},
        "primaryImageOfPage": {"@id": image_id} if image_id else None,
        "breadcrumb": {"@id": breadcrumb_id},
        "datePublished": signals.published_time or None,
        "dateModified": signals.modified_time or None,
    }
    graph.append(webpage)

    is_article = signals.og_type.lower() == "article" if signals.og_type else False
    if is_article:
        graph.append(
            {
                "@type": "Article",
                "@id": f"{page_id}#article",
                "headline": primary_title,
                "description": description,
                "datePublished": signals.published_time or None,
                "dateModified": signals.modified_time or None,
                "mainEntityOfPage": {"@id": webpage_id},
                "publisher": {"@id": org_id},
                "image": {"@id": image_id} if image_id else None,
            }
        )

    if signals.faqs:
        graph.append(
            {
                "@type": "FAQPage",
                "@id": f"{page_id}#faq",
                "url": page_url,
                "isPartOf": {"@id": website_id},
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": question,
                        "acceptedAnswer": {"@type": "Answer", "text": answer},
                    }
                    for question, answer in signals.faqs
                ],
            }
        )

    data = {
        "@context": "https://schema.org",
        "@graph": graph,
    }
    return prune_empty(data)


def output_path_for(url: str, out_dir: Path) -> Path:
    parsed = urlparse(url)._replace(query="", fragment="")
    path = parsed.path
    if not path or path.endswith("/"):
        relative = Path(path.lstrip("/")) / "index.html"
    else:
        relative = Path(path.lstrip("/"))
        if not relative.suffix:
            relative = relative.with_suffix(".html")
    return out_dir / relative


def render_script(schema: dict[str, Any]) -> str:
    payload = json.dumps(schema, ensure_ascii=False, indent=2)
    return f'<script type="application/ld+json">\\n{payload}\\n</script>\\n'


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate JSON-LD schema scripts from cache.")
    parser.add_argument("--client-slug", required=True, help="Client slug under outputs/")
    parser.add_argument(
        "--output-dir",
        help="Optional output directory (default: outputs/<client>/gen-schema/website-tree)",
    )
    args = parser.parse_args()

    cache_dir = Path("outputs") / args.client_slug / "reports" / "site-cache"
    index_path = cache_dir / "index.json"
    if not index_path.exists():
        raise SystemExit(f"Cache index not found: {index_path}")

    out_dir = (
        Path(args.output_dir)
        if args.output_dir
        else Path("outputs") / args.client_slug / "gen-schema" / "website-tree"
    )
    out_dir.mkdir(parents=True, exist_ok=True)

    cache = load_cache(index_path)
    for url, path in cache.items():
        if not path.exists():
            continue
        html = path.read_text(encoding="utf-8")
        signals = parse_page(html, url)
        schema = generate_schema(signals)
        out_path = output_path_for(signals.canonical_url or url, out_dir)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(render_script(schema), encoding="utf-8")
        print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
