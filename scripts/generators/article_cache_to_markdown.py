#!/usr/bin/env python3
"""Extract articles from cached site HTML and convert to markdown.

Reads data/outputs/<client>/reports/site-cache/index.json and extracts
article/blog pages to markdown format.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from bs4 import BeautifulSoup


ARTICLE_RE = re.compile(r"/blog|/article|/post|/news|/resources", re.I)


@dataclass
class Article:
    url: str
    title: str
    meta_description: str
    h1: str
    canonical_url: str
    og_type: str
    og_title: str
    og_description: str
    og_image: str
    published_date: str
    modified_date: str
    author: str
    content_paragraphs: list[str]
    headings: list[str]
    images: list[str]
    internal_links: list[str]
    schema_types: list[str]


def is_article_page(url: str) -> bool:
    """Check if URL is an article/blog page."""
    return bool(ARTICLE_RE.search(url))


def extract_meta(soup: BeautifulSoup) -> tuple[str, str]:
    """Extract title and meta description."""
    title = soup.title.get_text(strip=True) if soup.title else ""
    meta_desc = ""
    desc_tag = soup.find("meta", attrs={"name": "description"})
    if desc_tag and desc_tag.get("content"):
        meta_desc = desc_tag["content"].strip()
    return title, meta_desc


def extract_canonical(soup: BeautifulSoup) -> str:
    """Extract canonical URL."""
    link = soup.find("link", rel="canonical")
    if link and link.get("href"):
        return link["href"].strip()
    return ""


def extract_open_graph(soup: BeautifulSoup) -> tuple[str, str, str, str]:
    """Extract Open Graph metadata."""
    og_type = ""
    og_title = ""
    og_desc = ""
    og_image = ""
    for tag in soup.find_all("meta"):
        prop = tag.get("property")
        content = tag.get("content", "").strip()
        if not prop or not content:
            continue
        if prop == "og:type":
            og_type = content
        elif prop == "og:title":
            og_title = content
        elif prop == "og:description":
            og_desc = content
        elif prop == "og:image":
            og_image = content
    return og_type, og_title, og_desc, og_image


def extract_dates(soup: BeautifulSoup) -> tuple[str, str]:
    """Extract published and modified dates."""
    published = ""
    modified = ""
    for tag in soup.find_all("meta"):
        prop = tag.get("property") or tag.get("name")
        content = tag.get("content", "").strip()
        if not prop or not content:
            continue
        if prop in ("article:published_time", "datePublished"):
            published = content
        elif prop in ("article:modified_time", "dateModified", "og:updated_time"):
            modified = content
    return published, modified


def extract_author(soup: BeautifulSoup) -> str:
    """Extract article author."""
    # Try meta tag
    for tag in soup.find_all("meta"):
        name = tag.get("name")
        if name == "author":
            return tag.get("content", "").strip()
    
    # Try schema.org
    for script in soup.find_all("script", type=re.compile("ld\\+json", re.I)):
        try:
            data = json.loads(script.string or "")
            if isinstance(data, dict) and data.get("@type") in ("Article", "BlogPosting", "NewsArticle"):
                author = data.get("author")
                if isinstance(author, dict):
                    return author.get("name", "")
                elif isinstance(author, str):
                    return author
        except Exception:
            continue
    
    return ""


def extract_content(soup: BeautifulSoup) -> list[str]:
    """Extract main content paragraphs."""
    paragraphs = []
    
    # Try to find article/main content area
    main = soup.find("article") or soup.find("main") or soup.find("div", class_=re.compile(r"content|post|article", re.I))
    
    if main:
        for p in main.find_all("p"):
            text = " ".join(p.stripped_strings)
            if len(text) > 40:  # Filter out very short paragraphs
                paragraphs.append(text)
    else:
        # Fall back to all paragraphs
        for p in soup.find_all("p"):
            text = " ".join(p.stripped_strings)
            if len(text) > 40:
                paragraphs.append(text)
    
    return paragraphs[:20]  # Limit to first 20 paragraphs


def extract_headings(soup: BeautifulSoup) -> list[str]:
    """Extract article headings."""
    headings = []
    
    # Try to find headings in article/main area
    main = soup.find("article") or soup.find("main") or soup.find("div", class_=re.compile(r"content|post|article", re.I))
    container = main if main else soup
    
    for tag in container.find_all(["h2", "h3", "h4"]):
        text = " ".join(tag.stripped_strings)
        if text and text not in headings:
            headings.append(text)
        if len(headings) >= 15:
            break
    
    return headings


def extract_images(soup: BeautifulSoup, base_url: str) -> list[str]:
    """Extract article images."""
    images = []
    
    # Try to find images in article/main area
    main = soup.find("article") or soup.find("main") or soup.find("div", class_=re.compile(r"content|post|article", re.I))
    container = main if main else soup
    
    for img in container.find_all("img"):
        src = img.get("src") or img.get("data-src")
        if src and not src.startswith("data:"):
            images.append(src)
        if len(images) >= 10:
            break
    
    return images


def extract_internal_links(soup: BeautifulSoup, base_url: str) -> list[str]:
    """Extract internal links from article."""
    links = []
    base = urlparse(base_url)
    
    # Try to find links in article/main area
    main = soup.find("article") or soup.find("main") or soup.find("div", class_=re.compile(r"content|post|article", re.I))
    container = main if main else soup
    
    for a in container.find_all("a", href=True):
        href = a.get("href", "").strip()
        if not href or href.startswith("#") or href.startswith("mailto:") or href.startswith("tel:"):
            continue
        
        parsed = urlparse(href)
        if parsed.netloc and parsed.netloc != base.netloc:
            continue
        
        if href not in links:
            links.append(href)
        if len(links) >= 10:
            break
    
    return links


def extract_schema_types(soup: BeautifulSoup) -> list[str]:
    """Extract schema.org types."""
    types = []
    for script in soup.find_all("script", type=re.compile("ld\\+json", re.I)):
        try:
            data = json.loads(script.string or "")
            candidates = []
            if isinstance(data, dict):
                candidates.append(data)
            elif isinstance(data, list):
                candidates.extend([item for item in data if isinstance(item, dict)])
            
            for item in candidates:
                schema_type = item.get("@type")
                if not schema_type:
                    continue
                if isinstance(schema_type, list):
                    types.extend([t for t in schema_type if isinstance(t, str) and t not in types])
                elif isinstance(schema_type, str) and schema_type not in types:
                    types.append(schema_type)
        except Exception:
            continue
    
    return types


def parse_html(html: str, url: str) -> Article:
    """Parse HTML and extract article information."""
    soup = BeautifulSoup(html, "html.parser")
    title, meta_desc = extract_meta(soup)
    canonical_url = extract_canonical(soup)
    og_type, og_title, og_desc, og_image = extract_open_graph(soup)
    published, modified = extract_dates(soup)
    author = extract_author(soup)
    
    h1 = ""
    h1_tag = soup.find("h1")
    if h1_tag:
        h1 = " ".join(h1_tag.stripped_strings)
    
    return Article(
        url=url,
        title=title,
        meta_description=meta_desc,
        h1=h1,
        canonical_url=canonical_url,
        og_type=og_type,
        og_title=og_title,
        og_description=og_desc,
        og_image=og_image,
        published_date=published,
        modified_date=modified,
        author=author,
        content_paragraphs=extract_content(soup),
        headings=extract_headings(soup),
        images=extract_images(soup, url),
        internal_links=extract_internal_links(soup, url),
        schema_types=extract_schema_types(soup),
    )


def load_cache(index_path: Path) -> dict[str, Path]:
    """Load cache index and return URL to path mapping."""
    data = json.loads(index_path.read_text(encoding="utf-8"))
    return {url: Path(meta["path"]) for url, meta in data.items()}


def render_markdown(article: Article) -> str:
    """Render article as markdown."""
    lines = []
    
    # Header with metadata
    lines.append(f"# {article.h1 or article.title}")
    lines.append("")
    lines.append(f"**Source:** {article.url}")
    lines.append("")
    if article.author:
        lines.append(f"**Author:** {article.author}")
    if article.published_date:
        lines.append(f"**Published:** {article.published_date}")
    if article.modified_date:
        lines.append(f"**Modified:** {article.modified_date}")
    if article.author or article.published_date or article.modified_date:
        lines.append("")
    
    # Metadata section
    lines.append("## Metadata")
    lines.append("")
    if article.title:
        lines.append(f"- **Page title:** {article.title}")
    if article.meta_description:
        lines.append(f"- **Meta description:** {article.meta_description}")
    if article.canonical_url:
        lines.append(f"- **Canonical URL:** {article.canonical_url}")
    if article.og_type:
        lines.append(f"- **OG Type:** {article.og_type}")
    if article.og_title:
        lines.append(f"- **OG Title:** {article.og_title}")
    if article.og_description:
        lines.append(f"- **OG Description:** {article.og_description}")
    if article.og_image:
        lines.append(f"- **OG Image:** {article.og_image}")
    if article.schema_types:
        lines.append(f"- **Schema types:** {', '.join(article.schema_types)}")
    lines.append("")
    
    # Headings structure
    if article.headings:
        lines.append("## Content Structure")
        lines.append("")
        for heading in article.headings:
            lines.append(f"- {heading}")
        lines.append("")
    
    # Content preview
    lines.append("## Content Preview")
    lines.append("")
    for i, paragraph in enumerate(article.content_paragraphs[:5], 1):
        lines.append(f"{paragraph}")
        lines.append("")
        if i >= 5:
            if len(article.content_paragraphs) > 5:
                lines.append(f"*...and {len(article.content_paragraphs) - 5} more paragraphs*")
                lines.append("")
            break
    
    # Images
    if article.images:
        lines.append("## Images")
        lines.append("")
        for img in article.images:
            lines.append(f"- {img}")
        lines.append("")
    
    # Internal links
    if article.internal_links:
        lines.append("## Internal Links")
        lines.append("")
        for link in article.internal_links:
            lines.append(f"- {link}")
        lines.append("")
    
    # Footer
    lines.append("---")
    lines.append("")
    lines.append(f"*Extracted from cache: {datetime.now(timezone.utc).isoformat(timespec='seconds')}*")
    lines.append("")
    
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract articles from cached HTML and convert to markdown."
    )
    parser.add_argument("--client-slug", required=True, help="Client slug under data/outputs/")
    args = parser.parse_args()
    
    cache_dir = Path("data") / "outputs" / args.client_slug / "reports" / "site-cache"
    index_path = cache_dir / "index.json"
    if not index_path.exists():
        raise SystemExit(f"Cache index not found: {index_path}")
    
    cache = load_cache(index_path)
    out_dir = Path("data") / "outputs" / args.client_slug / "articles"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    article_count = 0
    for url, path in cache.items():
        if not is_article_page(url):
            continue
        
        html = path.read_text(encoding="utf-8")
        article = parse_html(html, url)
        
        # Create filename from URL path
        slug = urlparse(url).path.strip("/").replace("/", "-")
        if not slug:
            slug = "article"
        
        out_path = out_dir / f"{slug}.md"
        out_path.write_text(render_markdown(article), encoding="utf-8")
        print(f"wrote {out_path}")
        article_count += 1
    
    if article_count == 0:
        print("No article pages found in cache.")
        print("Article pages are identified by URL patterns: /blog, /article, /post, /news, /resources")
    else:
        print(f"\nExtracted {article_count} article(s) to {out_dir}")


if __name__ == "__main__":
    main()
