#!/usr/bin/env python3
"""Validate internal links using metadata/internal link map output.

Reads data/outputs/<client>/reports/metadata-internal-link-map.json and produces
data/outputs/<client>/reports/internal-link-validation.json/.md.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REQUIRED_LINK_TYPES = {
    "local-landing": ["related-service", "service-hub", "contact"],
    "service-page": ["related-service", "service-area", "maintenance"],
    "service-area-article": ["service-page", "contact"],
    "topical-guide": ["service-page", "contact"],
}

PLACEHOLDER_TOKENS = ("[", "]", "todo", "placeholder")


@dataclass
class ValidationIssue:
    kind: str
    detail: str


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_map(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"Metadata link map not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc


def is_placeholder(value: str) -> bool:
    lower = value.lower()
    return any(token in lower for token in PLACEHOLDER_TOKENS)


def validate_page(page: dict[str, Any]) -> dict[str, Any]:
    issues: list[ValidationIssue] = []
    page_type = page.get("type")
    required = REQUIRED_LINK_TYPES.get(page_type, [])

    internal_links = page.get("internal_links", [])
    missing_links = page.get("missing_links", [])
    errors = page.get("errors", [])

    if errors:
        for err in errors:
            issues.append(ValidationIssue(kind="page-error", detail=str(err)))

    if missing_links:
        for missing in missing_links:
            label = missing.get("label", "unknown")
            link_type = missing.get("type", "other")
            issues.append(
                ValidationIssue(kind="missing-target", detail=f"{label} ({link_type})")
            )

    present_types = {link.get("type") for link in internal_links if link.get("type")}
    for req in required:
        if req not in present_types:
            issues.append(ValidationIssue(kind="missing-required", detail=req))

    for link in internal_links:
        url = link.get("url")
        if not url:
            continue
        if is_placeholder(str(url)):
            issues.append(ValidationIssue(kind="placeholder-url", detail=str(url)))

    return {
        "id": page.get("id"),
        "type": page_type,
        "status": "fail" if issues else "pass",
        "issues": [issue.__dict__ for issue in issues],
    }


def render_markdown(results: list[dict[str, Any]], client_name: str) -> str:
    lines: list[str] = []
    lines.append(f"# Internal Link Validation: {client_name}")
    lines.append("")
    for result in results:
        lines.append(f"## {result.get('id')} ({result.get('type')})")
        lines.append(f"- Status: {result.get('status')}")
        issues = result.get("issues", [])
        if issues:
            lines.append("")
            lines.append("### Issues")
            for issue in issues:
                lines.append(f"- {issue.get('kind')}: {issue.get('detail')}")
        lines.append("")
    return "\n".join(lines)


def summarize(results: list[dict[str, Any]]) -> dict[str, int]:
    total = len(results)
    failed = sum(1 for result in results if result.get("status") == "fail")
    return {"total": total, "failed": failed, "passed": total - failed}


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate internal links from metadata link map.")
    parser.add_argument("--client-slug", required=True, help="Client slug under data/outputs/")
    args = parser.parse_args()

    base_dir = Path("data") / "outputs" / args.client_slug / "reports"
    input_path = base_dir / "metadata-internal-link-map.json"
    data = load_map(input_path)

    client_name = data.get("client", {}).get("name", args.client_slug)
    pages = data.get("pages")
    if not isinstance(pages, list):
        raise SystemExit("metadata-internal-link-map.json must contain a pages array")

    results = [validate_page(page) for page in pages]

    output = {
        "generated_at": now_iso(),
        "client": data.get("client", {}),
        "summary": summarize(results),
        "results": results,
    }

    base_dir.mkdir(parents=True, exist_ok=True)
    json_path = base_dir / "internal-link-validation.json"
    json_path.write_text(json.dumps(output, indent=2), encoding="utf-8")

    md_path = base_dir / "internal-link-validation.md"
    md_path.write_text(render_markdown(results, client_name), encoding="utf-8")

    print(f"wrote {json_path}")
    print(f"wrote {md_path}")


if __name__ == "__main__":
    main()
