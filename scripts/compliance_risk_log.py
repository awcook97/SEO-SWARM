#!/usr/bin/env python3
"""Generate a compliance risk log for draft markdown files."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from draft_compliance_lint import iter_markdown_files, parse_nap


PLACEHOLDER_RE = re.compile(r"\[[^\]]+\](?!\()")
TODO_RE = re.compile(r"\b(TODO|TBD|PLACEHOLDER|FIXME|TK)\b", re.IGNORECASE)
CLAIM_RE = re.compile(
    r"\b(best|top[- ]?rated|#1|number one|award[- ]?winning|guaranteed|guarantee|"
    r"certified|licensed|insured|bonded)\b",
    re.IGNORECASE,
)
SOURCE_RE = re.compile(r"\b(source needed|citation needed|\[source\]|source:\s*\[)\b", re.IGNORECASE)


@dataclass
class Issue:
    file: str
    line: int
    kind: str
    text: str


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def lint_file(path: Path, nap: dict[str, str] | None = None) -> list[Issue]:
    issues: list[Issue] = []
    content = path.read_text(encoding="utf-8")
    for idx, line in enumerate(content.splitlines(), start=1):
        if PLACEHOLDER_RE.search(line):
            issues.append(Issue(file=str(path), line=idx, kind="placeholder", text=line.strip()))
        if TODO_RE.search(line):
            issues.append(Issue(file=str(path), line=idx, kind="todo", text=line.strip()))
        if CLAIM_RE.search(line):
            issues.append(Issue(file=str(path), line=idx, kind="claim", text=line.strip()))
        if SOURCE_RE.search(line):
            issues.append(Issue(file=str(path), line=idx, kind="missing_source", text=line.strip()))
    if nap:
        if nap.get("business_name") and nap["business_name"] not in content:
            issues.append(
                Issue(
                    file=str(path),
                    line=1,
                    kind="nap_missing",
                    text="Business name not found in draft.",
                )
            )
        if nap.get("phone") and nap["phone"] not in content:
            issues.append(
                Issue(
                    file=str(path),
                    line=1,
                    kind="nap_missing",
                    text="Phone number not found in draft.",
                )
            )
    return issues


def render_markdown(issues: list[Issue]) -> str:
    lines: list[str] = []
    lines.append("# Compliance risk log")
    lines.append("")
    lines.append(f"Generated: {now_iso()}")
    lines.append("")
    lines.append(f"Total risks: {len(issues)}")
    lines.append("")

    if not issues:
        lines.append("No compliance risks detected.")
        lines.append("")
        return "\n".join(lines)

    counts: dict[str, int] = {}
    for issue in issues:
        counts[issue.kind] = counts.get(issue.kind, 0) + 1

    lines.append("## Summary")
    for kind, count in sorted(counts.items()):
        lines.append(f"- {kind.replace('_', ' ').title()}: {count}")
    lines.append("")

    lines.append("## Findings")
    for issue in issues:
        lines.append(f"- {issue.kind.upper()} | {issue.file}:{issue.line} | {issue.text}")
    lines.append("")

    lines.append("## Notes")
    lines.append("- Replace placeholders with approved inputs.")
    lines.append("- Add sources for any claims or statistics before publishing.")
    lines.append("- Ensure drafts include approved business name and phone.")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a compliance risk log for draft markdown files.")
    parser.add_argument("--client-slug", required=True, help="Client slug under data/outputs/")
    parser.add_argument(
        "--paths",
        nargs="*",
        default=None,
        help="Optional relative paths under data/outputs/<client> to scan (default: pages and articles).",
    )
    args = parser.parse_args()

    base_dir = Path("data") / "outputs" / args.client_slug
    if not base_dir.exists():
        raise SystemExit(f"Client folder not found: {base_dir}")

    nap = parse_nap(base_dir / "inputs.md")
    if args.paths:
        scan_paths = [base_dir / Path(path) for path in args.paths]
    else:
        scan_paths = [base_dir / "pages", base_dir / "articles"]

    files = iter_markdown_files(scan_paths)
    issues: list[Issue] = []
    for path in files:
        issues.extend(lint_file(path, nap))

    report_dir = base_dir / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    md_path = report_dir / "compliance-risk-log.md"
    json_path = report_dir / "compliance-risk-log.json"

    payload = {
        "generated_at": now_iso(),
        "total": len(issues),
        "issues": [issue.__dict__ for issue in issues],
    }

    md_path.write_text(render_markdown(issues), encoding="utf-8")
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print(f"wrote {md_path}")
    print(f"wrote {json_path}")


if __name__ == "__main__":
    main()
