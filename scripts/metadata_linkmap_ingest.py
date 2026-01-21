#!/usr/bin/env python3
"""Build metadata/internal link map input JSON from a page plan CSV."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


def normalize_header(value: str) -> str:
    return value.strip().lower().replace(" ", "_")


def load_csv(path: Path) -> list[dict[str, str]]:
    try:
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            if not reader.fieldnames:
                raise SystemExit(f"CSV has no headers: {path}")
            rows: list[dict[str, str]] = []
            for row in reader:
                rows.append({normalize_header(k): (v or "").strip() for k, v in row.items()})
            return rows
    except FileNotFoundError as exc:
        raise SystemExit(f"CSV not found: {path}") from exc


def parse_list(value: str) -> list[str]:
    if not value:
        return []
    for sep in (";", "|"):
        if sep in value:
            return [item.strip() for item in value.split(sep) if item.strip()]
    return [value.strip()]


def parse_internal_links(value: str) -> list[dict[str, str]]:
    links: list[dict[str, str]] = []
    if not value:
        return links
    chunks = [item.strip() for item in value.split(";") if item.strip()]
    for chunk in chunks:
        parts = [part.strip() for part in chunk.split("|")]
        if len(parts) < 2:
            continue
        label, url = parts[0], parts[1]
        link_type = parts[2] if len(parts) > 2 else "other"
        links.append({"label": label, "url": url, "type": link_type})
    return links


def parse_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "y"} if value else False


def build_pages(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    pages: list[dict[str, Any]] = []
    for row in rows:
        page_type = row.get("type")
        slug = row.get("slug")
        if not page_type or not slug:
            continue
        page: dict[str, Any] = {
            "id": row.get("id") or slug,
            "type": page_type,
            "slug": slug,
        }
        if row.get("service"):
            page["service"] = row["service"]
        if row.get("city"):
            page["city"] = row["city"]
        if row.get("topic"):
            page["topic"] = row["topic"]
        if row.get("proof_point"):
            page["proof_point"] = row["proof_point"]
        related = parse_list(row.get("related_services", ""))
        if related:
            page["related_services"] = related
        service_area_links = parse_list(row.get("service_area_links", ""))
        if service_area_links:
            page["service_area_links"] = service_area_links
        internal_links = parse_internal_links(row.get("internal_links", ""))
        if internal_links:
            page["internal_links"] = internal_links
        if parse_bool(row.get("include_faq_schema", "")):
            page["include_faq_schema"] = True
        pages.append(page)
    return pages


def scaffold_csv(path: Path) -> None:
    sample = [
        {
            "id": "service-page-1",
            "type": "service-page",
            "slug": "service-slug",
            "service": "Service Name",
            "city": "",
            "topic": "",
            "proof_point": "",
            "related_services": "Related Service",
            "service_area_links": "/service-areas/city",
            "internal_links": "Blog|/blog|supporting",
            "include_faq_schema": "true",
        }
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(sample[0].keys()))
        writer.writeheader()
        writer.writerows(sample)


def load_service_pages(path: Path | None) -> dict[str, str] | None:
    if not path:
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"Service pages JSON not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit("Service pages JSON must be an object map.")
    return {str(k): str(v) for k, v in data.items()}


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert page plan CSV into metadata linkmap input JSON.")
    parser.add_argument("--client-slug", required=True, help="Client slug under outputs/")
    parser.add_argument("--input", required=True, help="Path to page plan CSV.")
    parser.add_argument("--client-name", required=True, help="Client name.")
    parser.add_argument("--client-phone", required=True, help="Client phone.")
    parser.add_argument("--client-website", default=None, help="Client website.")
    parser.add_argument("--contact-url", default=None, help="Default contact URL.")
    parser.add_argument("--service-hub-url", default=None, help="Default service hub URL.")
    parser.add_argument("--maintenance-url", default=None, help="Default maintenance URL.")
    parser.add_argument(
        "--service-pages",
        default=None,
        help="Path to JSON map of service name -> URL.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output JSON path (default: outputs/<client>/reports/metadata-linkmap-input.json).",
    )
    parser.add_argument("--scaffold", action="store_true", help="Write a scaffold CSV to the input path.")
    args = parser.parse_args()

    input_path = Path(args.input)
    if args.scaffold:
        input_path.parent.mkdir(parents=True, exist_ok=True)
        scaffold_csv(input_path)
        print(f"wrote scaffold CSV to {input_path}")
        return

    output_dir = Path("outputs") / args.client_slug / "reports"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.output) if args.output else output_dir / "metadata-linkmap-input.json"

    rows = load_csv(input_path)
    pages = build_pages(rows)
    if not pages:
        raise SystemExit("No valid pages found in CSV.")

    payload = {
        "client": {
            "name": args.client_name,
            "phone": args.client_phone,
            "website": args.client_website,
        },
        "defaults": {
            "contact_url": args.contact_url,
            "service_hub_url": args.service_hub_url,
            "maintenance_url": args.maintenance_url,
            "service_pages": load_service_pages(Path(args.service_pages)) if args.service_pages else None,
        },
        "pages": pages,
    }
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"wrote {output_path}")


if __name__ == "__main__":
    main()
