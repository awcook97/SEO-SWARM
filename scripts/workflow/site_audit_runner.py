#!/usr/bin/env python3
"""
Run the full site audit pipeline for a client.

Default behavior: run all steps. Use --crawl-only for cache + inputs.md only.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def run_step(label: str, cmd: list[str], continue_on_error: bool) -> bool:
    print(f"\n==> {label}")
    print(" ".join(cmd))
    proc = subprocess.run(cmd, check=False)
    if proc.returncode == 0:
        print(f"[ok] {label}")
        return True
    print(f"[fail] {label} (exit {proc.returncode})")
    if continue_on_error:
        return False
    raise SystemExit(proc.returncode)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run full site audit pipeline.")
    parser.add_argument("--client", required=True, help="Client display name")
    parser.add_argument("--slug", required=True, help="Client slug under data/outputs/")
    parser.add_argument("--site-url", required=True, help="Base site URL to crawl")
    parser.add_argument("--crawl-only", action="store_true", help="Only crawl and build inputs.md")
    parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help="Continue running steps even if one fails",
    )
    args = parser.parse_args()

    python = sys.executable
    steps: list[tuple[str, list[str]]] = []

    steps.append(
        (
            "Scaffold client + crawl cache + seed inputs",
            [
                python,
                str(REPO_ROOT / "scripts" / "workflow" / "swarm_workflow.py"),
                "--client",
                args.client,
                "--slug",
                args.slug,
                "--site-url",
                args.site_url,
            ],
        )
    )

    if args.crawl_only:
        for label, cmd in steps:
            run_step(label, cmd, args.continue_on_error)
        return

    steps.extend(
        [
            (
                "Build metadata linkmap input",
                [
                    python,
                    str(REPO_ROOT / "scripts" / "ingest" / "metadata_linkmap_builder.py"),
                    "--client-slug",
                    args.slug,
                ],
            ),
            (
                "Generate metadata + internal link map",
                [
                    python,
                    str(REPO_ROOT / "scripts" / "generators" / "metadata_internal_link_map.py"),
                    "--client-slug",
                    args.slug,
                ],
            ),
            (
                "Generate service briefs",
                [
                    python,
                    str(REPO_ROOT / "scripts" / "generators" / "service_brief_generator.py"),
                    "--client-slug",
                    args.slug,
                ],
            ),
            (
                "Summarize service briefs",
                [
                    python,
                    str(REPO_ROOT / "scripts" / "generators" / "brief_summary_report.py"),
                    "--client-slug",
                    args.slug,
                ],
            ),
            (
                "Generate keyword map + KPI (auto from cache)",
                [
                    python,
                    str(REPO_ROOT / "scripts" / "generators" / "keyword_map_kpi.py"),
                    "--client-slug",
                    args.slug,
                    "--auto-from-cache",
                ],
            ),
            (
                "Generate cache schema (with validation)",
                [
                    python,
                    str(REPO_ROOT / "scripts" / "generators" / "cache_schema_generator.py"),
                    "--client-slug",
                    args.slug,
                    "--validate-schemaorg",
                ],
            ),
            (
                "Run technical SEO audit",
                [
                    python,
                    str(REPO_ROOT / "scripts" / "generators" / "technical_seo_audit_scaffold.py"),
                    "--client-slug",
                    args.slug,
                ],
            ),
        ]
    )

    for label, cmd in steps:
        run_step(label, cmd, args.continue_on_error)


if __name__ == "__main__":
    main()
