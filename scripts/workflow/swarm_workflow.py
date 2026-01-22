#!/usr/bin/env python3
"""
Scaffold a client output folder for the SEO swarm workflow.

This script is intentionally tool-agnostic and uses only the Python stdlib.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


OUTPUT_FILES = [
    "inputs.md",
    "pages/local-landing.md",
    "pages/service-page.md",
    "articles/service-area-article.md",
    "articles/topical-blog-post.md",
    "social/social-posts.md",
    "email/subscriber-email.md",
]


def write_file(base: Path, rel_path: str, content: str) -> None:
    path = base / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return
    path.write_text(content, encoding="utf-8")

def run_crawl_cache(client_slug: str, site_url: str | None) -> None:
    if not site_url:
        return
    script = Path(__file__).resolve().parent.parent / "ingest" / "crawl_cache.py"
    if not script.exists():
        print("crawl_cache.py not found; skipping site cache.")
        return
    cmd = [
        sys.executable,
        str(script),
        "--client-slug",
        client_slug,
        "--base",
        site_url,
    ]
    print(f"Caching site HTML from {site_url} ...")
    proc = subprocess.run(cmd, check=False)
    if proc.returncode != 0:
        print("crawl_cache.py failed. Ensure requests/bs4 are installed and the URL is reachable.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold SEO swarm output folders.")
    parser.add_argument("--client", required=True, help="Client name")
    parser.add_argument("--slug", required=True, help="Output folder slug")
    parser.add_argument(
        "--base-dir",
        default="data/outputs",
        help="Base output directory (default: data/outputs)",
    )
    parser.add_argument(
        "--site-url",
        help="Optional base URL to crawl and cache HTML into reports/site-cache",
    )
    args = parser.parse_args()

    base = Path(args.base_dir) / args.slug
    base.mkdir(parents=True, exist_ok=True)

    header = f"# {args.client} - Swarm Outputs\n\n"
    write_file(base, "README.md", header + "Use this folder to store client deliverables.\n")

    for rel_path in OUTPUT_FILES:
        write_file(base, rel_path, f"# {args.client} - {rel_path}\n\n")

    print(f"Scaffolded outputs at {base}")
    run_crawl_cache(args.slug, args.site_url)


if __name__ == "__main__":
    main()
