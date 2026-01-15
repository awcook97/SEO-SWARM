#!/usr/bin/env python3
"""
Scaffold a client output folder for the SEO swarm workflow.

This script is intentionally tool-agnostic and uses only the Python stdlib.
"""

from __future__ import annotations

import argparse
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


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold SEO swarm output folders.")
    parser.add_argument("--client", required=True, help="Client name")
    parser.add_argument("--slug", required=True, help="Output folder slug")
    parser.add_argument(
        "--base-dir",
        default="outputs",
        help="Base output directory (default: outputs)",
    )
    args = parser.parse_args()

    base = Path(args.base_dir) / args.slug
    base.mkdir(parents=True, exist_ok=True)

    header = f"# {args.client} - Swarm Outputs\n\n"
    write_file(base, "README.md", header + "Use this folder to store client deliverables.\n")

    for rel_path in OUTPUT_FILES:
        write_file(base, rel_path, f"# {args.client} - {rel_path}\n\n")

    print(f"Scaffolded outputs at {base}")


if __name__ == "__main__":
    main()
