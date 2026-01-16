#!/usr/bin/env python3
"""Lint draft markdown files for placeholders and risky claims."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


PLACEHOLDER_RE = re.compile(r"\[[^\]]+\](?!\()")
TODO_RE = re.compile(r"\b(TODO|TBD|PLACEHOLDER|FIXME|TK)\b", re.IGNORECASE)
CLAIM_RE = re.compile(
    r"\b(best|top[- ]?rated|#1|number one|award[- ]?winning|guaranteed|guarantee|"
    r"certified|licensed|insured|bonded)\b",
    re.IGNORECASE,
)


@dataclass
class Issue:
    file: str
    line: int
    kind: str
    text: str


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def iter_markdown_files(paths: Iterable[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_dir():
            files.extend(sorted(path.glob("*.md")))
        elif path.is_file() and path.suffix == ".md":
            files.append(path)
    return files


def parse_nap(inputs_path: Path) -> dict[str, str]:
    nap: dict[str, str] = {}
    if not inputs_path.exists():
        return nap
    for raw in inputs_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("- Business name:"):
            nap["business_name"] = line.split(":", 1)[1].strip()
        elif line.startswith("- Phone:"):
            nap["phone"] = line.split(":", 1)[1].strip()
        elif line.startswith("- Website:"):
            nap["website"] = line.split(":", 1)[1].strip()
        elif line.startswith("- Address:"):
            nap["address"] = ""
        elif line.startswith("- Line 1:"):
            nap["address_line1"] = line.split(":", 1)[1].strip()
        elif line.startswith("- City:"):
            nap["city"] = line.split(":", 1)[1].strip()
        elif line.startswith("- State:"):
            nap["state"] = line.split(":", 1)[1].strip()
        elif line.startswith("- Postal code:"):
            nap["postal_code"] = line.split(":", 1)[1].strip()
    return nap


def required_schema_for(path: Path) -> list[str]:
    name = path.name.lower()
    if name in {"service-page.md", "local-landing.md", "service-area-article.md"}:
        return ["Service", "LocalBusiness"]
    if name in {"topical-blog-post.md"}:
        return ["Article"]
    return []


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
    required_schema = required_schema_for(path)
    missing_schema = [schema for schema in required_schema if schema.lower() not in content.lower()]
    if missing_schema:
        issues.append(
            Issue(
                file=str(path),
                line=1,
                kind="schema_missing",
                text=f"Missing schema references: {', '.join(missing_schema)}",
            )
        )
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
    lines.append("# Draft compliance lint report")
    lines.append("")
    lines.append(f"Generated: {now_iso()}")
    lines.append("")
    lines.append(f"Total issues: {len(issues)}")
    lines.append("")

    if not issues:
        lines.append("No issues detected.")
        lines.append("")
        return "\n".join(lines)

    lines.append("## Findings")
    for issue in issues:
        lines.append(f"- {issue.kind.upper()} | {issue.file}:{issue.line} | {issue.text}")
    lines.append("")
    lines.append("## Notes")
    lines.append("- Placeholders must be replaced with approved inputs.")
    lines.append("- Claims require verified sources before publishing.")
    lines.append("- Schema references should match page type (Service, LocalBusiness, Article).")
    lines.append("- Drafts should include approved business name and phone.")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Lint draft markdown files for compliance issues.")
    parser.add_argument("--client-slug", required=True, help="Client slug under outputs/")
    parser.add_argument(
        "--paths",
        nargs="*",
        default=None,
        help="Optional relative paths under outputs/<client> to scan (default: pages and articles).",
    )
    args = parser.parse_args()

    base_dir = Path("outputs") / args.client_slug
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
    md_path = report_dir / "draft-compliance-lint.md"
    json_path = report_dir / "draft-compliance-lint.json"

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
