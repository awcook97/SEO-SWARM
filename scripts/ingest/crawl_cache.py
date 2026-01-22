#!/usr/bin/env python3
"""Cache a site's HTML pages with rate limiting.

- Crawls sitemap(s) if available; falls back to homepage link discovery.
- Stores HTML snapshots under data/outputs/<client>/reports/site-cache/.
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
    status_code: int
    response_time_ms: int
    content_bytes: int


def normalize_url(url: str) -> str:
    parsed = urlparse(url)
    return parsed._replace(fragment="").geturl()


def discover_urls(
    session: requests.Session,
    base: str,
    timeout: int,
    headers: dict[str, str],
) -> list[str]:
    candidates = ["/sitemap.xml", "/sitemap_index.xml"]
    urls: set[str] = set()

    for path in candidates:
        url = urljoin(base, path)
        try:
            resp = session.get(url, headers=headers, timeout=timeout, allow_redirects=True, stream=False)
            if resp.status_code != 200:
                continue
            soup = BeautifulSoup(resp.content, "xml")

            if soup.find("sitemapindex"):
                for loc in soup.find_all("loc", recursive=True):
                    sub_url = loc.get_text(strip=True)
                    try:
                        sub_resp = session.get(sub_url, headers=headers, timeout=timeout)
                        if sub_resp.status_code == 200:
                            subsoup = BeautifulSoup(sub_resp.content, "xml")
                            for subloc in subsoup.find_all("loc", recursive=True):
                                urls.add(subloc.get_text(strip=True))
                    except Exception as e:
                        print(f"Error fetching sub-sitemap {sub_url}: {e}")
                        continue
            else:
                for loc in soup.find_all("loc", recursive=True):
                    urls.add(loc.get_text(strip=True))
        except Exception as e:
            print(f"Error fetching sitemap {url}: {e}")
            continue

    if not urls:
        resp = session.get(base, headers=headers, timeout=timeout)
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
        url: CacheEntry(
            url=url,
            fetched_at=meta["fetched_at"],
            path=meta["path"],
            status_code=meta.get("status_code", 0),
            response_time_ms=meta.get("response_time_ms", 0),
            content_bytes=meta.get("content_bytes", 0),
        )
        for url, meta in data.items()
    }


def save_index(path: Path, entries: dict[str, CacheEntry]) -> None:
    payload = {
        url: {
            "fetched_at": entry.fetched_at,
            "path": entry.path,
            "status_code": entry.status_code,
            "response_time_ms": entry.response_time_ms,
            "content_bytes": entry.content_bytes,
        }
        for url, entry in entries.items()
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def cache_path_for(cache_dir: Path, url: str) -> Path:
    digest = hashlib.sha256(url.encode("utf-8")).hexdigest()[:16]
    return cache_dir / f"{digest}.html"


def is_html_response(resp: requests.Response) -> bool:
    content_type = resp.headers.get("Content-Type", "").lower()
    if "text/html" in content_type or "application/xhtml" in content_type:
        return True
    return False


def is_probable_asset(url: str) -> bool:
    path = urlparse(url).path.lower()
    return path.endswith((".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".ico", ".pdf", ".zip"))

def fetch_with_retries(
    session: requests.Session,
    url: str,
    headers: dict[str, str],
    timeout: int,
    retries: int,
    backoff_seconds: int,
) -> requests.Response | None:
    for attempt in range(retries + 1):
        try:
            resp = session.get(url, headers=headers, timeout=timeout)
            if resp.status_code >= 500 and attempt < retries:
                time.sleep(backoff_seconds * (attempt + 1))
                continue
            return resp
        except requests.RequestException:
            if attempt >= retries:
                return None
            time.sleep(backoff_seconds * (attempt + 1))
    return None


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
    parser.add_argument("--client-slug", required=True, help="Client slug under data/outputs/")
    parser.add_argument("--timeout", type=int, default=25, help="Request timeout seconds")
    parser.add_argument("--max-age-hours", type=int, default=24, help="Re-fetch cache older than this")
    parser.add_argument("--min-interval-seconds", type=int, default=20, help="Per-URL minimum interval")
    parser.add_argument("--retries", type=int, default=3, help="Retries for failed requests")
    parser.add_argument("--backoff-seconds", type=int, default=5, help="Base backoff seconds between retries")
    parser.add_argument(
        "--user-agent",
        default="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        help="User-Agent string for requests",
    )
    args = parser.parse_args()

    base = args.base.rstrip("/")
    cache_dir = Path("data") / "outputs" / args.client_slug / "reports" / "site-cache"
    cache_dir.mkdir(parents=True, exist_ok=True)

    index_path = cache_dir / "index.json"
    index = load_index(index_path)

    session = requests.Session()
    headers = {
        "User-Agent": args.user_agent,
        # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        # "Accept-Language": "en-US,en;q=0.9",
        # "Accept-Encoding": "gzip, deflate, br, zstd",
    }
    urls = discover_urls(session, base, args.timeout, headers)

    for url in urls:
        if is_probable_asset(url):
            continue
        entry = index.get(url)
        if not should_fetch(entry, args.max_age_hours):
            continue
        enforce_rate_limit(entry, args.min_interval_seconds)
        resp = fetch_with_retries(
            session=session,
            url=url,
            headers=headers,
            timeout=args.timeout,
            retries=args.retries,
            backoff_seconds=args.backoff_seconds,
        )
        if resp is None:
            print(f"skip {url} -> request failed after retries")
            continue
        if resp.status_code >= 400:
            print(f"skip {url} -> status {resp.status_code}")
            continue
        if not is_html_response(resp):
            print(f"skip {url} -> non-html content")
            continue
        path = cache_path_for(cache_dir, url)
        path.write_text(resp.text, encoding="utf-8")
        index[url] = CacheEntry(
            url=url,
            fetched_at=datetime.now(timezone.utc).isoformat(),
            path=str(path),
            status_code=resp.status_code,
            response_time_ms=int(resp.elapsed.total_seconds() * 1000),
            content_bytes=len(resp.content),
        )
        save_index(index_path, index)
        print(f"cached {url} -> {path}")


if __name__ == "__main__":
    main()
