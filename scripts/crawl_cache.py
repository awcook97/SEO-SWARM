#!/usr/bin/env python3
"""Cache a site's HTML pages with rate limiting.

- Crawls sitemap(s) if available; falls back to homepage link discovery.
- Stores HTML snapshots under outputs/<client>/reports/site-cache/.
- Enforces per-URL minimum interval (default: 20s => 3 requests/min).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


BLOG_RE = re.compile(r"/blog|/category|/tag|/author|/page/", re.I)


@dataclass
class CacheEntry:
    url: str
    fetched_at: str
    path: str


def normalize_url(url: str) -> str:
    parsed = urlparse(url)
    return parsed._replace(fragment="").geturl()


def discover_urls(base: str, timeout: int) -> list[str]:
    candidates = ["/sitemap.xml", "/sitemap_index.xml"]
    urls: set[str] = set()

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

    if not urls:
        resp = requests.get(base, timeout=timeout)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        for a in soup.select("a[href]"):
            href = a.get("href")
            if not href:
                continue
            if href.startswith("/"):
                urls.add(urljoin(base, href))
            elif href.startswith(base):
                urls.add(href)

    cleaned = [normalize_url(u) for u in urls if u.startswith(base)]
    cleaned = [u for u in cleaned if not BLOG_RE.search(u)]
    return sorted(set(cleaned))


def load_index(path: Path) -> dict[str, CacheEntry]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return {
        url: CacheEntry(url=url, fetched_at=meta["fetched_at"], path=meta["path"])
        for url, meta in data.items()
    }


def save_index(path: Path, entries: dict[str, CacheEntry]) -> None:
    payload = {
        url: {"fetched_at": entry.fetched_at, "path": entry.path}
        for url, entry in entries.items()
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def cache_path_for(cache_dir: Path, url: str) -> Path:
    digest = hashlib.sha256(url.encode("utf-8")).hexdigest()[:16]
    return cache_dir / f"{digest}.html"


def should_fetch(entry: CacheEntry | None, max_age_hours: int) -> bool:
    if entry is None:
        return True
    fetched = datetime.fromisoformat(entry.fetched_at)
    return datetime.now(timezone.utc) - fetched > timedelta(hours=max_age_hours)


def enforce_rate_limit(entry: CacheEntry | None, min_interval_seconds: int) -> None:
    if entry is None:
        return
    fetched = datetime.fromisoformat(entry.fetched_at)
    elapsed = (datetime.now(timezone.utc) - fetched).total_seconds()
    remaining = min_interval_seconds - elapsed
    if remaining > 0:
        time.sleep(remaining)


def main() -> None:
    parser = argparse.ArgumentParser(description="Cache site HTML with rate limiting.")
    parser.add_argument("--base", required=True, help="Base site URL, e.g. https://example.com")
    parser.add_argument("--client-slug", required=True, help="Client slug under outputs/")
    parser.add_argument("--timeout", type=int, default=25, help="Request timeout seconds")
    parser.add_argument("--max-age-hours", type=int, default=24, help="Re-fetch cache older than this")
    parser.add_argument("--min-interval-seconds", type=int, default=20, help="Per-URL minimum interval")
    args = parser.parse_args()

    base = args.base.rstrip("/")
    cache_dir = Path("outputs") / args.client_slug / "reports" / "site-cache"
    cache_dir.mkdir(parents=True, exist_ok=True)

    index_path = cache_dir / "index.json"
    index = load_index(index_path)

    urls = discover_urls(base, args.timeout)
    session = requests.Session()
    headers = {"User-Agent": "Mozilla/5.0"}

    for url in urls:
        entry = index.get(url)
        if not should_fetch(entry, args.max_age_hours):
            continue
        enforce_rate_limit(entry, args.min_interval_seconds)
        resp = session.get(url, headers=headers, timeout=args.timeout)
        resp.raise_for_status()
        path = cache_path_for(cache_dir, url)
        path.write_text(resp.text, encoding="utf-8")
        index[url] = CacheEntry(
            url=url,
            fetched_at=datetime.now(timezone.utc).isoformat(),
            path=str(path),
        )
        save_index(index_path, index)
        print(f"cached {url} -> {path}")


if __name__ == "__main__":
    main()
