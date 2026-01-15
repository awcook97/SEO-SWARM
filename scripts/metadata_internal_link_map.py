#!/usr/bin/env python3
"""Generate metadata drafts and internal link maps from approved inputs.

Reads a page plan JSON file and outputs structured metadata/internal link maps
under outputs/<client>/reports/.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SUPPORTED_TYPES = {
    "local-landing",
    "service-page",
    "service-area-article",
    "topical-guide",
}


@dataclass
class ClientInfo:
    name: str
    phone: str
    website: str | None = None


@dataclass
class Defaults:
    contact_url: str | None = None
    service_hub_url: str | None = None
    maintenance_url: str | None = None
    service_pages: dict[str, str] | None = None


def slugify(value: str) -> str:
    slug = "".join(ch.lower() if ch.isalnum() else "-" for ch in value)
    slug = "-".join(part for part in slug.split("-") if part)
    return slug


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_input(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"Input file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc


def parse_client(data: dict[str, Any]) -> ClientInfo:
    client = data.get("client", {})
    name = client.get("name")
    phone = client.get("phone")
    if not name or not phone:
        raise SystemExit("Input must include client.name and client.phone")
    return ClientInfo(name=name, phone=phone, website=client.get("website"))


def parse_defaults(data: dict[str, Any]) -> Defaults:
    defaults = data.get("defaults", {})
    service_pages = defaults.get("service_pages")
    if service_pages is not None and not isinstance(service_pages, dict):
        raise SystemExit("defaults.service_pages must be an object map")
    return Defaults(
        contact_url=defaults.get("contact_url"),
        service_hub_url=defaults.get("service_hub_url"),
        maintenance_url=defaults.get("maintenance_url"),
        service_pages=service_pages,
    )


def require_fields(page: dict[str, Any], fields: list[str]) -> list[str]:
    missing = []
    for field in fields:
        if not page.get(field):
            missing.append(field)
    return missing


def build_metadata(page: dict[str, Any], client: ClientInfo) -> dict[str, Any]:
    page_type = page["type"]
    service = page.get("service")
    city = page.get("city")
    topic = page.get("topic")
    proof_point = page.get("proof_point")

    schema_types: list[str] = []
    title = ""
    meta = ""

    if page_type == "local-landing":
        title = f"{service} in {city} | {client.name}"
        meta = f"{service} in {city} with {client.name}."
        schema_types = ["LocalBusiness", "Service"]
    elif page_type == "service-page":
        title = f"{service} | {client.name}"
        meta = f"{service} with {client.name}."
        schema_types = ["Service", "LocalBusiness"]
    elif page_type == "service-area-article":
        title = f"{service} in {city} | {client.name}"
        meta = f"{service} in {city} with {client.name}."
        schema_types = ["LocalBusiness", "Service"]
    elif page_type == "topical-guide":
        title = f"{topic} | {client.name}"
        meta = f"{topic} guide with {client.name}."
        schema_types = ["Article"]

    if proof_point:
        meta = f"{meta} {proof_point}."
    meta = f"{meta} Call {client.phone}."

    if page.get("include_faq_schema"):
        schema_types.append("FAQPage")

    return {
        "title_tag": title,
        "meta_description": meta.strip(),
        "schema_types": schema_types,
    }


def resolve_service_url(service: str | None, defaults: Defaults) -> str | None:
    if not service or not defaults.service_pages:
        return None
    return defaults.service_pages.get(service)


def normalize_internal_links(links: list[dict[str, Any]]) -> list[dict[str, str]]:
    normalized: list[dict[str, str]] = []
    for link in links:
        label = link.get("label")
        url = link.get("url")
        link_type = link.get("type", "other")
        if not label or not url:
            continue
        normalized.append({"label": str(label), "url": str(url), "type": str(link_type)})
    return normalized


def build_internal_links(page: dict[str, Any], defaults: Defaults) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    page_type = page["type"]
    links: list[dict[str, str]] = []
    missing: list[dict[str, str]] = []

    def add_link(label: str, url: str | None, link_type: str) -> None:
        if url:
            links.append({"label": label, "url": url, "type": link_type})
        else:
            missing.append({"label": label, "type": link_type})

    related_services = page.get("related_services", [])
    for service in related_services:
        add_link(service, resolve_service_url(service, defaults), "related-service")

    if page_type == "service-page":
        for url in page.get("service_area_links", []):
            add_link("Service area", url, "service-area")
        add_link("Maintenance plans", defaults.maintenance_url, "maintenance")
    elif page_type == "local-landing":
        add_link("Service hub", defaults.service_hub_url, "service-hub")
        add_link("Contact", defaults.contact_url, "contact")
    elif page_type == "service-area-article":
        add_link("Service page", resolve_service_url(page.get("service"), defaults), "service-page")
        add_link("Contact", defaults.contact_url, "contact")
    elif page_type == "topical-guide":
        add_link("Relevant service", resolve_service_url(page.get("service"), defaults), "service-page")
        add_link("Contact", defaults.contact_url, "contact")

    links.extend(normalize_internal_links(page.get("internal_links", [])))

    return links, missing


def build_page_entry(page: dict[str, Any], client: ClientInfo, defaults: Defaults) -> dict[str, Any]:
    page_type = page.get("type")
    if page_type not in SUPPORTED_TYPES:
        return {
            "id": page.get("id") or page.get("slug") or "unknown",
            "type": page_type,
            "errors": ["Unsupported page type"],
        }

    required = ["slug"]
    if page_type in {"local-landing", "service-area-article"}:
        required += ["service", "city"]
    if page_type == "service-page":
        required += ["service"]
    if page_type == "topical-guide":
        required += ["topic"]

    missing_fields = require_fields(page, required)
    errors = []
    if missing_fields:
        errors.append(f"Missing required fields: {', '.join(missing_fields)}")

    slug = page.get("slug") or slugify(page.get("service") or page.get("topic") or "page")
    metadata = build_metadata(page, client) if not errors else {}
    links, missing_links = build_internal_links(page, defaults) if not errors else ([], [])

    entry: dict[str, Any] = {
        "id": page.get("id") or slug,
        "type": page_type,
        "slug": slug,
        "inputs": {
            "service": page.get("service"),
            "city": page.get("city"),
            "topic": page.get("topic"),
            "primary_keyword": page.get("primary_keyword"),
        },
        "metadata": metadata,
        "internal_links": links,
        "missing_links": missing_links,
    }
    if errors:
        entry["errors"] = errors
    return entry


def render_markdown(pages: list[dict[str, Any]], client: ClientInfo) -> str:
    lines: list[str] = []
    lines.append(f"# Metadata + Internal Link Map: {client.name}")
    lines.append("")
    for page in pages:
        lines.append(f"## {page.get('id', 'page')} ({page.get('type', 'unknown')})")
        if page.get("errors"):
            lines.append(f"- Errors: {', '.join(page['errors'])}")
            lines.append("")
            continue
        meta = page.get("metadata", {})
        lines.append(f"- Title tag: {meta.get('title_tag', '')}")
        lines.append(f"- Meta description: {meta.get('meta_description', '')}")
        lines.append(f"- Schema: {', '.join(meta.get('schema_types', []))}")
        lines.append("")
        lines.append("### Internal links")
        for link in page.get("internal_links", []):
            lines.append(f"- {link.get('label')} ({link.get('type')}): {link.get('url')}")
        if not page.get("internal_links"):
            lines.append("- [None]")
        if page.get("missing_links"):
            lines.append("")
            lines.append("### Missing link targets")
            for missing in page["missing_links"]:
                lines.append(f"- {missing.get('label')} ({missing.get('type')})")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate metadata + internal link map from a page plan.")
    parser.add_argument("--client-slug", required=True, help="Client slug under outputs/")
    parser.add_argument(
        "--input",
        default="metadata-linkmap-input.json",
        help="Input JSON filename under outputs/<client>/reports/",
    )
    args = parser.parse_args()

    base_dir = Path("outputs") / args.client_slug / "reports"
    input_path = base_dir / args.input
    data = load_input(input_path)

    client = parse_client(data)
    defaults = parse_defaults(data)
    pages_data = data.get("pages")
    if not isinstance(pages_data, list) or not pages_data:
        raise SystemExit("Input must include a non-empty pages list")

    pages = [build_page_entry(page, client, defaults) for page in pages_data]
    output = {
        "generated_at": now_iso(),
        "client": {
            "name": client.name,
            "phone": client.phone,
            "website": client.website,
        },
        "pages": pages,
    }

    base_dir.mkdir(parents=True, exist_ok=True)
    json_path = base_dir / "metadata-internal-link-map.json"
    json_path.write_text(json.dumps(output, indent=2), encoding="utf-8")

    md_path = base_dir / "metadata-internal-link-map.md"
    md_path.write_text(render_markdown(pages, client), encoding="utf-8")

    print(f"wrote {json_path}")
    print(f"wrote {md_path}")


if __name__ == "__main__":
    main()
