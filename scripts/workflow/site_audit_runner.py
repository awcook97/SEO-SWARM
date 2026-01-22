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
        "--fail-fast",
        action="store_true",
        help="Stop on the first failing step",
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
            run_step(label, cmd, not args.fail_fast)
        return

    reports_dir = REPO_ROOT / "data" / "outputs" / args.slug / "reports"
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
                "Generate content briefs (scaffold if missing)",
                [
                    python,
                    str(REPO_ROOT / "scripts" / "generators" / "content_brief_generator.py"),
                    "--client-slug",
                    args.slug,
                    "--scaffold",
                ],
            ),
            (
                "Measurement intake (scaffold if missing)",
                [
                    python,
                    str(REPO_ROOT / "scripts" / "generators" / "measurement_intake_generator.py"),
                    "--client-slug",
                    args.slug,
                    "--scaffold",
                ],
            ),
            (
                "Competitor snapshot (scaffold if missing)",
                [
                    python,
                    str(REPO_ROOT / "scripts" / "generators" / "competitor_snapshot_builder.py"),
                    "--client-slug",
                    args.slug,
                    "--scaffold",
                ],
            ),
            (
                "SERP insights (scaffold if missing)",
                [
                    python,
                    str(REPO_ROOT / "scripts" / "generators" / "serp_insights_summary.py"),
                    "--client-slug",
                    args.slug,
                    "--scaffold",
                ],
            ),
            (
                "Keyword map + KPI (auto from cache)",
                [
                    python,
                    str(REPO_ROOT / "scripts" / "generators" / "keyword_map_kpi.py"),
                    "--client-slug",
                    args.slug,
                    "--auto-from-cache",
                ],
            ),
            (
                "GBP update checklist",
                [
                    python,
                    str(REPO_ROOT / "scripts" / "generators" / "gbp_update_checklist.py"),
                    "--client-slug",
                    args.slug,
                ],
            ),
            (
                "Citation update log (scaffold if missing)",
                [
                    python,
                    str(REPO_ROOT / "scripts" / "generators" / "citation_update_log.py"),
                    "--client-slug",
                    args.slug,
                    "--scaffold",
                ],
            ),
            (
                "Local link outreach (scaffold if missing)",
                [
                    python,
                    str(REPO_ROOT / "scripts" / "generators" / "local_link_outreach.py"),
                    "--client-slug",
                    args.slug,
                    "--scaffold",
                ],
            ),
            (
                "Review response templates (scaffold if missing)",
                [
                    python,
                    str(REPO_ROOT / "scripts" / "generators" / "review_response_templates.py"),
                    "--client-slug",
                    args.slug,
                    "--scaffold",
                ],
            ),
            (
                "Compliance risk log",
                [
                    python,
                    str(REPO_ROOT / "scripts" / "generators" / "compliance_risk_log.py"),
                    "--client-slug",
                    args.slug,
                ],
            ),
            (
                "Rank tracking report (scaffold config if missing)",
                [
                    python,
                    str(REPO_ROOT / "scripts" / "generators" / "rank_tracking_report_builder.py"),
                    "--client-slug",
                    args.slug,
                    "--scaffold-config",
                ],
            ),
            (
                "Technical SEO audit",
                [
                    python,
                    str(REPO_ROOT / "scripts" / "generators" / "technical_seo_audit_scaffold.py"),
                    "--client-slug",
                    args.slug,
                ],
            ),
            (
                "Cache schema (geocode + validate)",
                [
                    python,
                    str(REPO_ROOT / "scripts" / "generators" / "cache_schema_generator.py"),
                    "--client-slug",
                    args.slug,
                    "--geocode",
                    "--validate-schemaorg",
                ],
            ),
            (
                "Technical SEO audit (after schema)",
                [
                    python,
                    str(REPO_ROOT / "scripts" / "generators" / "technical_seo_audit_scaffold.py"),
                    "--client-slug",
                    args.slug,
                ],
            ),
            (
                "Internal link validation",
                [
                    python,
                    str(REPO_ROOT / "scripts" / "validation" / "internal_link_validator.py"),
                    "--client-slug",
                    args.slug,
                ],
            ),
            (
                "Draft compliance lint",
                [
                    python,
                    str(REPO_ROOT / "scripts" / "validation" / "draft_compliance_lint.py"),
                    "--client-slug",
                    args.slug,
                ],
            ),
            (
                "FAQ audit (live crawl)",
                [
                    python,
                    str(REPO_ROOT / "scripts" / "validation" / "faq_audit.py"),
                    "--base",
                    args.site_url,
                    "--output",
                    str(reports_dir / "faq-audit.json"),
                ],
            ),
            (
                "SERP fetch (scaffold input if missing)",
                [
                    python,
                    str(REPO_ROOT / "scripts" / "ingest" / "serp_dataforseo_fetch.py"),
                    "--client-slug",
                    args.slug,
                    "--scaffold",
                ],
            ),
            (
                "Review export ingest (scaffold CSV)",
                [
                    python,
                    str(REPO_ROOT / "scripts" / "ingest" / "review_export_ingest.py"),
                    "--client-slug",
                    args.slug,
                    "--input",
                    str(reports_dir / "reviews.csv"),
                    "--scaffold-csv",
                ],
            ),
            (
                "Metadata linkmap ingest (scaffold CSV)",
                [
                    python,
                    str(REPO_ROOT / "scripts" / "ingest" / "metadata_linkmap_ingest.py"),
                    "--client-slug",
                    args.slug,
                    "--input",
                    str(reports_dir / "metadata-linkmap-input.csv"),
                    "--client-name",
                    args.client,
                    "--client-phone",
                    "[add phone]",
                    "--client-website",
                    args.site_url,
                    "--scaffold",
                ],
            ),
            (
                "Crawl export ingest (requires input)",
                [
                    python,
                    str(REPO_ROOT / "scripts" / "ingest" / "crawl_export_ingest.py"),
                    "--client-slug",
                    args.slug,
                ],
            ),
            (
                "GSC export ingest (requires input)",
                [
                    python,
                    str(REPO_ROOT / "scripts" / "ingest" / "gsc_export_ingest.py"),
                    "--client-slug",
                    args.slug,
                ],
            ),
            (
                "GA4 export ingest (requires input)",
                [
                    python,
                    str(REPO_ROOT / "scripts" / "ingest" / "ga4_export_ingest.py"),
                    "--client-slug",
                    args.slug,
                ],
            ),
            (
                "GBP export ingest (requires input)",
                [
                    python,
                    str(REPO_ROOT / "scripts" / "ingest" / "gbp_export_ingest.py"),
                    "--client-slug",
                    args.slug,
                ],
            ),
            (
                "Citation audit ingest (requires input)",
                [
                    python,
                    str(REPO_ROOT / "scripts" / "ingest" / "citation_audit_ingest.py"),
                    "--client-slug",
                    args.slug,
                ],
            ),
            (
                "Rank tracker export ingest (requires input)",
                [
                    python,
                    str(REPO_ROOT / "scripts" / "ingest" / "rank_tracker_export_ingest.py"),
                    "--client-slug",
                    args.slug,
                ],
            ),
        ]
    )

    for label, cmd in steps:
        run_step(label, cmd, not args.fail_fast)


if __name__ == "__main__":
    main()
